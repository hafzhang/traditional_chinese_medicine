"""
AI填充食谱数据 - 批量API版本
一次API调用处理3条食谱，大幅提升处理速度
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
    CONSTITUTION_CODES, CONSTITUTION_CN_TO_CODE, EFFICACY_TAGS,
    SOLAR_TERMS
)

# 进度文件路径
PROGRESS_FILE = Path(__file__).parent / "ai_fill_progress_batch.json"
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

    def add_success(self, count: int = 1):
        with self._lock:
            self.success += count

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
    return {'processed_batches': []}


def save_progress(processed_batches: List[int]):
    """保存进度"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump({'processed_batches': processed_batches}, f, ensure_ascii=False, indent=2)


def backup_file(file_path: Path) -> Path:
    """备份文件"""
    backup_path = Path(str(file_path) + BACKUP_SUFFIX)
    if backup_path.exists():
        backup_path.unlink()
    shutil.copy(file_path, backup_path)
    print(f"[INFO] 已备份原文件到: {backup_path}")
    return backup_path


def create_batch_prompt(recipes: List[Dict[str, Any]]) -> str:
    """
    创建批量处理的提示词

    Args:
        recipes: 食谱列表，每个元素包含 {title, steptext, ingredients}

    Returns:
        批量处理提示词
    """
    constitutions_str = ", ".join(CONSTITUTION_CODES)
    tags_str = ", ".join(EFFICACY_TAGS)
    terms_str = ", ".join(SOLAR_TERMS)

    prompt = """你是一位中医养生专家。请分析以下{}道菜谱，为每道菜谱推荐适合的体质、禁忌体质、功效标签和适用节气。

体质代码: {}
功效标签: {}
节气: {}

请按以下JSON格式返回分析结果（必须是一个有效的JSON数组）:
{{"results": [
  {{"title": "菜名1", "suitable_constitutions": ["peace", "qi_deficiency"], "avoid_constitutions": ["phlegm_damp"], "efficacy_tags": ["健脾", "养胃"], "solar_terms": ["立春", "雨水"], "confidence": 85}},
  {{"title": "菜名2", "suitable_constitutions": ["peace"], "avoid_constitutions": [], "efficacy_tags": ["补气"], "solar_terms": ["冬季"], "confidence": 90}},
  ...
]}}

菜谱信息:
""".format(len(recipes), constitutions_str, tags_str, terms_str)

    for i, recipe in enumerate(recipes, 1):
        title = recipe.get('title', '未知')
        steptext = recipe.get('steptext', '无')
        ingredients = recipe.get('ingredients', '无')
        prompt += f"\n{i}. 菜名: {title}\n   做法: {steptext[:200] if len(str(steptext)) > 200 else steptext}\n   食材: {ingredients[:200] if len(str(ingredients)) > 200 else ingredients}\n"

    prompt += "\n请只返回JSON数组，不要有其他内容。"
    return prompt


def call_zhipu_api_batch(prompt: str, retry_count: int = 0) -> Optional[List[Dict[str, Any]]]:
    """
    调用智谱AI API - 批量处理版本

    Args:
        prompt: 提示词
        retry_count: 重试次数

    Returns:
        AI返回的结果列表，失败返回None
    """
    headers = {
        "x-api-key": ZHIPU_API_KEY,
        "anthropic-version": ANTHROPIC_VERSION,
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "max_tokens": 4000,  # 增加token限制以支持批量响应
        "temperature": 0.7,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        time.sleep(random.uniform(0.1, 0.3))

        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT if 'REQUEST_TIMEOUT' in globals() else 60
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

            # 尝试解析
            try:
                result = json.loads(content)
                if 'results' in result:
                    return result['results']
                # 如果直接返回数组
                if isinstance(result, list):
                    return result
            except:
                pass

            print(f"[ERROR] JSON解析失败，响应前100字符: {content[:100]}")
            return None
        else:
            print(f"[ERROR] API请求失败: {response.status_code}")
            return None

    except requests.Timeout:
        print(f"[ERROR] API请求超时")
        return None
    except requests.RequestException as e:
        print(f"[ERROR] API请求异常: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] 未知错误: {e}")
        return None


def validate_ai_result(result: Dict[str, Any]) -> bool:
    """验证AI返回的单条结果格式"""
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


def process_batch(args: tuple) -> Dict[str, Any]:
    """
    处理一批数据 - 用于多线程

    Args:
        args: (recipes_batch, df, original_indices, batch_num)

    Returns:
        处理结果字典
    """
    recipes_batch, df, original_indices, batch_num = args

    result_info = {
        'batch_num': batch_num,
        'original_indices': original_indices,
        'success_count': 0,
        'failed_count': 0,
        'results': [],
        'errors': []
    }

    # 准备食谱数据
    recipes_data = []
    for i, idx in enumerate(original_indices):
        row = df.iloc[idx]
        recipes_data.append({
            'title': row.get('title', ''),
            'steptext': row.get('steptext', ''),
            'ingredients': row.get('QuantityIngredients', ''),
            'df_idx': idx
        })

    # 创建批量提示词
    prompt = create_batch_prompt(recipes_data)

    # 调用API（带重试）
    results = None
    max_retries = 3
    for retry in range(max_retries):
        if retry > 0:
            time.sleep(1 * retry)
        results = call_zhipu_api_batch(prompt, retry)
        if results:
            break

    if not results:
        # 批量失败，尝试逐个处理
        print(f"[WARN] 批次{batch_num}批量处理失败，尝试逐个处理...")
        results = []  # 初始化 results 列表
        for recipe_data in recipes_data:
            single_prompt = create_batch_prompt([recipe_data])
            single_result = call_zhipu_api_batch(single_prompt, 0)
            if single_result and len(single_result) > 0:
                results.append(single_result[0])
            else:
                results.append(None)

    # 处理结果
    for i, result in enumerate(results):
        df_idx = recipes_data[i]['df_idx']
        title = recipes_data[i]['title']

        if result and validate_ai_result(result):
            # 更新DataFrame
            df.at[df_idx, 'suitable_constitutions'] = json.dumps(result['suitable_constitutions'], ensure_ascii=False)
            df.at[df_idx, 'avoid_constitutions'] = json.dumps(result['avoid_constitutions'], ensure_ascii=False)
            df.at[df_idx, 'efficacy_tags'] = json.dumps(result['efficacy_tags'], ensure_ascii=False)
            df.at[df_idx, 'solar_terms'] = json.dumps(result['solar_terms'], ensure_ascii=False)
            df.at[df_idx, 'confidence'] = result['confidence']
            df.at[df_idx, 'method'] = 'AI'

            result_info['success_count'] += 1
            result_info['results'].append(result)
        else:
            result_info['failed_count'] += 1
            result_info['errors'].append(f"{title}: 处理失败")

    return result_info


def fill_recipes_with_ai_batch(
    excel_path: str,
    batch_size: int = 3,
    num_threads: int = 4,
    resume: bool = True,
    dry_run: bool = False,
    test_limit: int = None
) -> AIFillRecipeStats:
    """
    使用AI批量填充食谱数据

    Args:
        excel_path: Excel文件路径
        batch_size: 每批处理行数（API调用一次处理多少条）
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

    # 加载进度
    processed_batches = set()
    if resume:
        progress_data = load_progress()
        processed_batches = set(progress_data.get('processed_batches', []))
        if processed_batches:
            print(f"[INFO] 从断点续传，已处理 {len(processed_batches)} 个批次")

    # 备份文件
    if not dry_run:
        backup_file(Path(excel_path))

    # 准备批次任务
    print(f"[INFO] 启动 {num_threads} 个线程，每API调用处理 {batch_size} 条记录")

    tasks = []
    batch_num = 0
    for i in range(0, len(df_simulated), batch_size):
        if batch_num in processed_batches:
            batch_num += 1
            stats.add_skip()
            continue

        batch_indices = df_simulated.iloc[i:i+batch_size].index.tolist()
        # 获取原始DataFrame索引
        original_indices = [df.index.get_loc(idx) for idx in batch_indices]

        tasks.append((batch_indices, df, original_indices, batch_num))
        batch_num += 1

    print(f"[INFO] 待处理批次数: {len(tasks)}")
    print(f"[INFO] 预计总API调用次数: {len(tasks)}")

    # 分批处理（使用线程池）
    completed_count = 0
    total_batches = len(tasks)

    # 每次处理多个批次
    concurrent_batches = max(1, num_threads // 2)  # 每次处理的批次数

    for i in range(0, len(tasks), concurrent_batches):
        current_batch = tasks[i:i + concurrent_batches]
        start_batch = i // concurrent_batches * concurrent_batches + 1
        end_batch = min(i + concurrent_batches, len(tasks))

        print(f"\n{'='*60}")
        print(f"处理批次组: {start_batch}-{end_batch} / {total_batches}")
        print(f"{'='*60}")

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = {executor.submit(process_batch, task): task for task in current_batch}

            for future in as_completed(futures):
                result_info = future.result()

                if result_info['success_count'] > 0:
                    stats.add_success(result_info['success_count'])
                    completed_count += result_info['success_count']
                    print(f"[OK] 批次{result_info['batch_num']}: 成功 {result_info['success_count']} 条 (总计 {completed_count}/{stats.total})")

                if result_info['failed_count'] > 0:
                    stats.add_failed(f"批次{result_info['batch_num']}: {result_info['failed_count']} 条失败")
                    for err in result_info['errors']:
                        print(f"[FAILED] {err}")

        # 定期保存
        if not dry_run and completed_count % 50 == 0:
            try:
                df.to_excel(excel_path, index=False, engine='openpyxl')
                print(f"[SAVE] 已保存Excel文件 (已完成 {completed_count} 条)")

                processed = list(range(i // concurrent_batches))
                save_progress(processed)
            except Exception as e:
                print(f"[ERROR] 保存失败: {e}")

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
    print(f"耗时:       {duration:.2f} 秒 ({duration/60:.1f} 分钟)")

    if stats.success > 0:
        print(f"平均耗时:   {duration / stats.success:.2f} 秒/条")

    if stats.failed > 0:
        print(f"\n失败详情 (最多显示10条):")
        with stats._lock:
            for error in stats.errors[:10]:
                print(f"  - {error}")
            if len(stats.errors) > 10:
                print(f"  ... 还有 {len(stats.errors) - 10} 条错误")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='使用AI批量填充食谱数据（一次API调用处理多条）')
    parser.add_argument('--file', '-f',
                       default='../source_data/dishes_list_ai_filled.xlsx',
                       help='Excel 文件路径')
    parser.add_argument('--batch-size', '-b', type=int, default=3,
                       help=f'每API调用处理行数 (默认: 3)')
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
    print("AI填充食谱数据 (批量API版)")
    print(f"{'='*60}")
    print(f"文件:        {file_path}")
    print(f"每API调用:    {args.batch_size} 条")
    print(f"线程数:      {args.threads}")
    print(f"断点续传:    {not args.no_resume}")
    print(f"模拟运行:    {args.dry_run}")
    if args.test:
        print(f"测试模式:    仅处理前 {args.test} 条")
    print(f"{'='*60}\n")

    # 执行填充
    stats = fill_recipes_with_ai_batch(
        str(file_path),
        batch_size=args.batch_size,
        num_threads=args.threads,
        resume=not args.no_resume,
        dry_run=args.dry_run,
        test_limit=args.test
    )

    # 打印摘要
    print_summary(stats)


if __name__ == '__main__':
    main()
