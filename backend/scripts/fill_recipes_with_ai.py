"""
AI填充食谱数据 - 主脚本
使用智谱AI GLM-4.7模型填充 dishes_list_ai_filled.xlsx 中 method="simulated" 的数据

功能：
- 读取Excel文件
- 筛选method="simulated"的行
- 调用智谱AI API填充数据
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
PROGRESS_FILE = Path(__file__).parent / "ai_fill_progress.json"
# 备份文件路径
BACKUP_SUFFIX = ".backup"


class AIFillRecipeStats:
    """统计信息类"""
    def __init__(self):
        self.total = 0
        self.success = 0
        self.failed = 0
        self.skipped = 0
        self.errors = []
        self.start_time = None
        self.end_time = None

    def to_dict(self) -> Dict[str, Any]:
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
        # 删除旧备份
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
            # 尝试提取JSON（可能包含在代码块中）
            content = content.strip()
            if content.startswith('```'):
                # 移除代码块标记
                lines = content.split('\n')
                if lines[0].startswith('```json'):
                    content = '\n'.join(lines[1:-1])
                elif lines[0].startswith('```'):
                    content = '\n'.join(lines[1:-1])
                content = content.strip()

            result = json.loads(content)
            return result
        else:
            print(f"[ERROR] API请求失败: {response.status_code} - {response.text}")
            return None

    except requests.Timeout:
        print(f"[ERROR] API请求超时")
        return None
    except requests.RequestException as e:
        print(f"[ERROR] API请求异常: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON解析失败: {e}")
        print(f"[DEBUG] 响应内容: {content if 'content' in locals() else 'N/A'}")
        return None
    except Exception as e:
        print(f"[ERROR] 未知错误: {e}")
        return None


def validate_ai_result(result: Dict[str, Any]) -> bool:
    """
    验证AI返回的结果格式

    Args:
        result: AI返回的结果

    Returns:
        True if valid, False otherwise
    """
    # 检查必需字段
    required_fields = ['suitable_constitutions', 'avoid_constitutions',
                      'efficacy_tags', 'solar_terms', 'confidence']

    for field in required_fields:
        if field not in result:
            print(f"[ERROR] 缺少字段: {field}")
            return False

    # 检查体质代码
    for constitution in result.get('suitable_constitutions', []):
        if constitution not in CONSTITUTION_CODES:
            print(f"[ERROR] 无效的体质代码: {constitution}")
            return False

    for constitution in result.get('avoid_constitutions', []):
        if constitution not in CONSTITUTION_CODES:
            print(f"[ERROR] 无效的体质代码: {constitution}")
            return False

    # 检查功效标签
    for tag in result.get('efficacy_tags', []):
        if tag not in EFFICACY_TAGS:
            print(f"[WARNING] 功效标签不在预定义列表中: {tag}")

    # 检查节气
    for term in result.get('solar_terms', []):
        if term not in SOLAR_TERMS:
            print(f"[WARNING] 节气不在预定义列表中: {term}")

    # 检查置信度
    confidence = result.get('confidence', 0)
    if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 100:
        print(f"[ERROR] 无效的置信度: {confidence}")
        return False

    return True


def process_row(row: pd.Series, df: pd.DataFrame, original_idx: int, stats: AIFillRecipeStats) -> Optional[Dict[str, Any]]:
    """
    处理单行数据

    Args:
        row: Excel行数据
        df: 原始DataFrame（用于更新）
        original_idx: 原始DataFrame中的索引
        stats: 统计信息

    Returns:
        AI结果，失败返回None
    """
    title = row.get('title', '')
    steptext = row.get('steptext', '')
    ingredients = row.get('QuantityIngredients', '')

    print(f"\n[{stats.success + 1}] 处理: {title[:30]}...")

    # 生成提示词
    prompt = get_prompt(title, steptext, ingredients)

    # 调用AI API（带重试）
    result = None
    for retry in range(MAX_RETRIES):
        if retry > 0:
            print(f"[RETRY] 第 {retry + 1} 次重试...")
            time.sleep(RATE_LIMIT_DELAY * retry)

        result = call_zhipu_api(prompt, retry)

        if result:
            break

    if not result:
        print(f"[FAILED] AI API调用失败: {title[:30]}...")
        stats.failed += 1
        stats.errors.append(f"{title[:50]}: AI API调用失败")
        return None

    # 验证结果
    if not validate_ai_result(result):
        print(f"[FAILED] 结果验证失败: {title[:30]}...")
        stats.failed += 1
        stats.errors.append(f"{title[:50]}: 结果验证失败")
        return None

    # 更新DataFrame
    df.at[original_idx, 'suitable_constitutions'] = json.dumps(result['suitable_constitutions'], ensure_ascii=False)
    df.at[original_idx, 'avoid_constitutions'] = json.dumps(result['avoid_constitutions'], ensure_ascii=False)
    df.at[original_idx, 'efficacy_tags'] = json.dumps(result['efficacy_tags'], ensure_ascii=False)
    df.at[original_idx, 'solar_terms'] = json.dumps(result['solar_terms'], ensure_ascii=False)
    df.at[original_idx, 'confidence'] = result['confidence']
    df.at[original_idx, 'method'] = 'AI'

    print(f"[OK] 成功: {title[:30]}... (置信度: {result['confidence']}%)")
    return result


def fill_recipes_with_ai(
    excel_path: str,
    batch_size: int = BATCH_SIZE,
    resume: bool = True,
    dry_run: bool = False,
    test_limit: int = None
) -> AIFillRecipeStats:
    """
    使用AI填充食谱数据

    Args:
        excel_path: Excel文件路径
        batch_size: 批处理大小
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
    processed_indices = []
    if resume:
        progress_data = load_progress()
        processed_indices = progress_data.get('processed_indices', [])
        if processed_indices:
            print(f"[INFO] 从断点续传，已处理 {len(processed_indices)} 条")

    # 备份文件
    if not dry_run:
        backup_file(Path(excel_path))

    # 批处理
    for i in range(0, len(df_simulated), batch_size):
        batch = df_simulated.iloc[i:i + batch_size]
        print(f"\n{'='*60}")
        print(f"批处理: {i + 1}-{min(i + batch_size, len(df_simulated))} / {len(df_simulated)}")
        print(f"{'='*60}")

        for batch_idx, (original_idx, row) in enumerate(batch.iterrows()):
            # 检查是否已处理
            if resume and batch_idx in processed_indices:
                stats.skipped += 1
                continue

            # 处理行
            result = process_row(row, df, original_idx, stats)

            if result:
                stats.success += 1
            else:
                stats.failed += 1

            # 保存进度
            if not dry_run:
                processed_indices.append(batch_idx)
                save_progress(processed_indices)

            # API限流延迟
            time.sleep(RATE_LIMIT_DELAY)

    # 保存更新后的Excel文件
    if not dry_run and stats.success > 0:
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

    if stats.errors:
        print(f"\n失败详情 (最多显示10条):")
        for error in stats.errors[:10]:
            print(f"  - {error}")
        if len(stats.errors) > 10:
            print(f"  ... 还有 {len(stats.errors) - 10} 条错误")


def export_failed_recipes(stats: AIFillRecipeStats, output_path: str):
    """导出失败的食谱到文件"""
    if not stats.errors:
        return

    with open(output_path, 'w', encoding='utf-8') as f:
        for error in stats.errors:
            f.write(f"{error}\n")

    print(f"[OK] 已导出 {len(stats.errors)} 条失败记录到: {output_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='使用AI填充食谱数据')
    parser.add_argument('--file', '-f',
                       default='../source_data/dishes_list_ai_filled.xlsx',
                       help='Excel 文件路径')
    parser.add_argument('--batch-size', '-b', type=int, default=BATCH_SIZE,
                       help=f'批处理大小 (默认: {BATCH_SIZE})')
    parser.add_argument('--no-resume', action='store_true',
                       help='不从断点续传，重新开始')
    parser.add_argument('--dry-run', action='store_true',
                       help='模拟运行，不实际修改文件')
    parser.add_argument('--clear-progress', action='store_true',
                       help='清除进度文件')
    parser.add_argument('--test', '-t', type=int, metavar='N',
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
        # 尝试相对于脚本目录的路径
        script_dir = Path(__file__).parent
        alt_path = script_dir / args.file
        if alt_path.exists():
            file_path = alt_path
        else:
            print(f"[ERROR] 文件不存在: {args.file}")
            sys.exit(1)

    print(f"\n{'='*60}")
    print("AI填充食谱数据")
    print(f"{'='*60}")
    print(f"文件:        {file_path}")
    print(f"批处理大小:  {args.batch_size}")
    print(f"断点续传:    {not args.no_resume}")
    print(f"模拟运行:    {args.dry_run}")
    if args.test:
        print(f"测试模式:    仅处理前 {args.test} 条")
    print(f"{'='*60}\n")

    # 执行填充
    stats = fill_recipes_with_ai(
        str(file_path),
        batch_size=args.batch_size,
        resume=not args.no_resume,
        dry_run=args.dry_run,
        test_limit=args.test
    )

    # 打印摘要
    print_summary(stats)

    # 导出失败记录
    if stats.failed > 0:
        failed_path = Path(__file__).parent / "ai_fill_failed.txt"
        export_failed_recipes(stats, str(failed_path))


if __name__ == '__main__':
    main()
