"""
AI填充食谱数据 - 多线程版本
使用智谱AI GLM-4.7模型填充 dishes_list_ai_filled.xlsx 中 method="simulated" 的数据

功能：
- 读取Excel文件
- 筛选method="simulated"的行
- 多线程调用智谱AI API填充数据
- 批量处理，支持断点续传
- 生成处理报告
"""

import sys
import os
import json
import time
import pandas as pd
import requests
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import random

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(scripts_dir))

# 导入配置
from ai_fill_config import (
    ZHIPU_API_KEY, API_URL, API_BASE_URL, MODEL, ANTHROPIC_VERSION,
    BATCH_SIZE, MAX_RETRIES, REQUEST_TIMEOUT, RATE_LIMIT_DELAY,
    CONSTITUTION_CODES, CONSTITUTION_CN_TO_CODE, EFFICACY_TAGS,
    SOLAR_TERMS, get_prompt
)

# 进度文件路径
PROGRESS_FILE = Path(__file__).parent / "ai_fill_progress_parallel.json"
# 备份文件路径
BACKUP_SUFFIX = ".backup"


class AIFillRecipeStats:
    """统计信息类 - 线程安全"""
    def __init__(self):
        self._lock = Lock()
        self.total = 0
        self.success = 0
        self.failed = 0
        self.skipped = 0
        self.errors = []
        self.start_time = None
        self.end_time = None

    def add_success(self):
        with self._lock:
            self.success += 1

    def add_failed(self, error_msg: str):
        with self._lock:
            self.failed += 1
            self.errors.append(error_msg)

    def add_skip(self):
        with self._lock:
            self.skipped += 1

    def to_dict(self) -> Dict[str, Any]:
        with self._lock:
            return {
                'total': self.total,
                'success': self.success,
                'failed': self.failed,
                'skipped': self.skipped,
                'error_count': len(self.errors),
                'start_time': self.start_time.isoformat() if self.start_time else None,
                'end_time': self.end_time.isoformat() if self.end_time else None,
            }


def load_progress() -> Dict[str, Any]:
    """加载进度文件"""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'processed_indices': []}


def save_progress(processed_indices: List[int]):
    """保存进度"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump({'processed_indices': processed_indices}, f, ensure_ascii=False, indent=2)


def backup_file(file_path: Path) -> Path:
    """备份文件"""
    backup_path = Path(str(file_path) + BACKUP_SUFFIX)
    if backup_path.exists():
        backup_path.unlink()
    shutil.copy(file_path, backup_path)
    print(f"[INFO] 已备份原文件到: {backup_path}")
    return backup_path


def call_zhipu_api(prompt: str, retry_count: int = 0) -> Optional[Dict[str, Any]]:
    """
    调用智谱AI API (使用 Anthropic 兼容接口)

    Args:
        prompt: 提示词
        retry_count: 重试次数

    Returns:
        AI返回的解析结果，失败返回None
    """
    # 使用 Anthropic API 格式
    headers = {
        "x-api-key": ZHIPU_API_KEY,
        "anthropic-version": ANTHROPIC_VERSION,
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "max_tokens": 2000,
        "temperature": 0.7,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        # 添加随机延迟避免API限流
        time.sleep(random.uniform(0.1, 0.5))

        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT
        )

        if response.status_code == 200:
            data = response.json()
            content = data['content'][0]['text']

            # 解析JSON响应
            content = content.strip()
            if content.startswith('```'):
                lines = content.split('\n')
                if lines[0].startswith('```json'):
                    content = '\n'.join(lines[1:-1])
                elif lines[0].startswith('```'):
                    content = '\n'.join(lines[1:-1])
                content = content.strip()

            result = json.loads(content)
            return result
        else:
            print(f"[ERROR] API请求失败: {response.status_code} - {response.text[:100]}")
            return None

    except requests.Timeout:
        print(f"[ERROR] API请求超时")
        return None
    except requests.RequestException as e:
        print(f"[ERROR] API请求异常: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON解析失败: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] 未知错误: {e}")
        return None


def validate_ai_result(result: Dict[str, Any]) -> bool:
    """验证AI返回的结果格式"""
    required_fields = ['suitable_constitutions', 'avoid_constitutions',
                      'efficacy_tags', 'solar_terms', 'confidence']

    for field in required_fields:
        if field not in result:
            return False

    for constitution in result.get('suitable_constitutions', []):
        if constitution not in CONSTITUTION_CODES:
            return False

    for constitution in result.get('avoid_constitutions', []):
        if constitution not in CONSTITUTION_CODES:
            return False

    confidence = result.get('confidence', 0)
    if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 100:
        return False

    return True


def process_single_row(args: tuple) -> Dict[str, Any]:
    """
    处理单行数据 - 用于多线程

    Args:
        args: (row, df, original_idx, batch_idx)

    Returns:
        处理结果字典
    """
    row, df, original_idx, batch_idx = args

    title = row.get('title', '')
    steptext = row.get('steptext', '')
    ingredients = row.get('QuantityIngredients', '')

    result_info = {
        'batch_idx': batch_idx,
        'original_idx': original_idx,
        'title': title,
        'success': False,
        'result': None,
        'error': None
    }

    # 生成提示词
    prompt = get_prompt(title, steptext, ingredients)

    # 调用AI API（带重试）
    result = None
    for retry in range(MAX_RETRIES):
        if retry > 0:
            time.sleep(RATE_LIMIT_DELAY * retry)
        result = call_zhipu_api(prompt, retry)
        if result:
            break

    if not result:
        result_info['error'] = 'AI API调用失败'
        return result_info

    # 验证结果
    if not validate_ai_result(result):
        result_info['error'] = '结果验证失败'
        return result_info

    # 更新DataFrame
    df.at[original_idx, 'suitable_constitutions'] = json.dumps(result['suitable_constitutions'], ensure_ascii=False)
    df.at[original_idx, 'avoid_constitutions'] = json.dumps(result['avoid_constitutions'], ensure_ascii=False)
    df.at[original_idx, 'efficacy_tags'] = json.dumps(result['efficacy_tags'], ensure_ascii=False)
    df.at[original_idx, 'solar_terms'] = json.dumps(result['solar_terms'], ensure_ascii=False)
    df.at[original_idx, 'confidence'] = result['confidence']
    df.at[original_idx, 'method'] = 'AI'

    result_info['success'] = True
    result_info['result'] = result
    return result_info


def fill_recipes_with_ai_parallel(
    excel_path: str,
    batch_size: int = 5,
    num_threads: int = 4,
    resume: bool = True,
    dry_run: bool = False,
    test_limit: int = None
) -> AIFillRecipeStats:
    """
    使用AI多线程填充食谱数据

    Args:
        excel_path: Excel文件路径
        batch_size: 每批次处理行数
        num_threads: 线程数
        resume: 是否从断点续传
        dry_run: 模拟运行，不实际修改文件
        test_limit: 测试模式，仅处理前N条记录

    Returns:
        统计信息
    """
    stats = AIFillRecipeStats()
    stats.start_time = datetime.now()

    # 读取Excel文件
    print(f"[INFO] 读取文件: {excel_path}")
    try:
        df = pd.read_excel(excel_path, sheet_name='Sheet1', engine='openpyxl')
        print(f"[OK] 成功读取 {len(df)} 条记录")
    except Exception as e:
        print(f"[ERROR] 读取 Excel 失败: {e}")
        return stats

    # 筛选 method="simulated" 的行
    df_simulated = df[df['method'] == 'simulated'].copy()
    print(f"[INFO] 筛选 method='simulated' 的行: {len(df_simulated)} 条")

    if len(df_simulated) == 0:
        print("[WARN] 没有需要处理的行")
        return stats

    # 测试模式：限制处理数量
    if test_limit:
        df_simulated = df_simulated.head(test_limit)
        print(f"[TEST] 测试模式，仅处理前 {test_limit} 条记录")

    stats.total = len(df_simulated)

    # 加载进度（如果启用断点续传）
    processed_set = set()
    if resume:
        progress_data = load_progress()
        processed_set = set(progress_data.get('processed_indices', []))
        if processed_set:
            print(f"[INFO] 从断点续传，已处理 {len(processed_set)} 条")

    # 备份文件
    if not dry_run:
        backup_file(Path(excel_path))

    # 多线程处理
    print(f"[INFO] 启动 {num_threads} 个线程，每批处理 {batch_size} 条记录")

    # 准备任务列表
    tasks = []
    for batch_idx, (original_idx, row) in enumerate(df_simulated.iterrows()):
        if resume and batch_idx in processed_set:
            stats.add_skip()
            continue
        tasks.append((row, df, original_idx, batch_idx))

    print(f"[INFO] 待处理任务数: {len(tasks)}")

    # 分批处理
    completed_count = 0
    save_interval = 10  # 每处理10条保存一次进度

    for i in range(0, len(tasks), batch_size):
        batch = tasks[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(tasks) + batch_size - 1) // batch_size

        print(f"\n{'='*60}")
        print(f"批次: {batch_num}/{total_batches} (记录 {i+1}-{min(i+batch_size, len(tasks))} / {len(tasks)})")
        print(f"{'='*60}")

        # 使用线程池处理当前批次
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = {executor.submit(process_single_row, task): task for task in batch}

            for future in as_completed(futures):
                result_info = future.result()

                if result_info['success']:
                    stats.add_success()
                    completed_count += 1
                    print(f"[OK] ({completed_count}/{len(tasks)}) {result_info['title'][:30]}... (置信度: {result_info['result']['confidence']}%)")
                else:
                    stats.add_failed(f"{result_info['title'][:50]}: {result_info['error']}")
                    print(f"[FAILED] ({stats.failed}) {result_info['title'][:30]}...: {result_info['error']}")

        # 定期保存进度和Excel
        if not dry_run and completed_count % save_interval == 0:
            # 保存Excel
            try:
                df.to_excel(excel_path, index=False, engine='openpyxl')
                print(f"[SAVE] 已保存Excel文件 (已完成 {completed_count} 条)")
            except Exception as e:
                print(f"[ERROR] 保存Excel失败: {e}")

            # 保存进度
            processed_indices = list(range(completed_count))
            save_progress(processed_indices)

    # 最终保存
    if not dry_run:
        try:
            df.to_excel(excel_path, index=False, engine='openpyxl')
            print(f"[OK] 已保存更新后的文件: {excel_path}")
        except Exception as e:
            print(f"[ERROR] 保存文件失败: {e}")

    stats.end_time = datetime.now()
    return stats


def print_summary(stats: AIFillRecipeStats):
    """打印统计摘要"""
    duration = (stats.end_time - stats.start_time).total_seconds() if stats.start_time and stats.end_time else 0

    print(f"\n{'='*60}")
    print("处理摘要")
    print(f"{'='*60}")
    print(f"总数:       {stats.total}")
    print(f"成功:       {stats.success}")
    print(f"跳过:       {stats.skipped}")
    print(f"失败:       {stats.failed}")
    print(f"耗时:       {duration:.2f} 秒")

    if stats.success > 0:
        print(f"平均耗时:   {duration / stats.success:.2f} 秒/条")

    if stats.failed > 0:
        print(f"\n失败详情 (最多显示10条):")
        with stats._lock:
            for error in stats.errors[:10]:
                print(f"  - {error}")
            if len(stats.errors) > 10:
                print(f"  ... 还有 {len(stats.errors) - 10} 条错误")


def export_failed_recipes(stats: AIFillRecipeStats, output_path: str):
    """导出失败的食谱到文件"""
    with stats._lock:
        if not stats.errors:
            return

        with open(output_path, 'w', encoding='utf-8') as f:
            for error in stats.errors:
                f.write(f"{error}\n")

        print(f"[OK] 已导出 {len(stats.errors)} 条失败记录到: {output_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='使用AI多线程填充食谱数据')
    parser.add_argument('--file', '-f',
                       default='../source_data/dishes_list_ai_filled.xlsx',
                       help='Excel 文件路径')
    parser.add_argument('--batch-size', '-b', type=int, default=5,
                       help=f'每批处理行数 (默认: 5)')
    parser.add_argument('--threads', '-t', type=int, default=4,
                       help=f'线程数 (默认: 4)')
    parser.add_argument('--no-resume', action='store_true',
                       help='不从断点续传，重新开始')
    parser.add_argument('--dry-run', action='store_true',
                       help='模拟运行，不实际修改文件')
    parser.add_argument('--clear-progress', action='store_true',
                       help='清除进度文件')
    parser.add_argument('--test', type=int, metavar='N',
                       help='测试模式：仅处理前N条记录')
    args = parser.parse_args()

    # 清除进度文件
    if args.clear_progress:
        if PROGRESS_FILE.exists():
            PROGRESS_FILE.unlink()
            print(f"[OK] 已清除进度文件: {PROGRESS_FILE}")

    # 检查文件是否存在
    file_path = Path(args.file)
    if not file_path.exists():
        script_dir = Path(__file__).parent
        alt_path = script_dir / args.file
        if alt_path.exists():
            file_path = alt_path
        else:
            print(f"[ERROR] 文件不存在: {args.file}")
            sys.exit(1)

    print(f"\n{'='*60}")
    print("AI填充食谱数据 (多线程版)")
    print(f"{'='*60}")
    print(f"文件:        {file_path}")
    print(f"每批处理:    {args.batch_size} 条")
    print(f"线程数:      {args.threads}")
    print(f"断点续传:    {not args.no_resume}")
    print(f"模拟运行:    {args.dry_run}")
    if args.test:
        print(f"测试模式:    仅处理前 {args.test} 条")
    print(f"{'='*60}\n")

    # 执行填充
    stats = fill_recipes_with_ai_parallel(
        str(file_path),
        batch_size=args.batch_size,
        num_threads=args.threads,
        resume=not args.no_resume,
        dry_run=args.dry_run,
        test_limit=args.test
    )

    # 打印摘要
    print_summary(stats)

    # 导出失败记录
    export_failed_recipes(stats, str(Path(__file__).parent / "ai_fill_failed_parallel.txt"))


if __name__ == '__main__':
    main()
