#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
菜谱导入脚本
从 Excel 文件导入菜谱数据到数据库
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

import pandas as pd
from sqlalchemy.orm import Session

# Setup path to import from parent directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.database import SessionLocal
from api.models import Recipe

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ImportStats:
    """导入统计信息"""

    def __init__(self):
        self.total: int = 0
        self.success: int = 0
        self.skipped: int = 0
        self.failed: int = 0
        self.errors: List[str] = []

    def add_error(self, error: str):
        """添加错误信息"""
        self.errors.append(error)

    def __str__(self) -> str:
        return (
            f"总数: {self.total}, "
            f"成功: {self.success}, "
            f"跳过: {self.skipped}, "
            f"失败: {self.failed}"
        )


def print_summary(stats: ImportStats):
    """打印导入统计摘要"""
    logger.info("=" * 60)
    logger.info("导入摘要")
    logger.info("=" * 60)
    logger.info(f"总数:       {stats.total}")
    logger.info(f"成功:       {stats.success}")
    logger.info(f"跳过:       {stats.skipped}")
    logger.info(f"失败:       {stats.failed}")

    if stats.errors:
        logger.info(f"\n失败详情 (显示前10条):")
        for error in stats.errors[:10]:
            logger.info(f"  - {error}")
        if len(stats.errors) > 10:
            logger.info(f"  ... 还有 {len(stats.errors) - 10} 条错误")


def load_excel(file_path: str) -> pd.DataFrame:
    """
    加载并验证 Excel 文件
    使用 pandas.read_excel() 读取文件
    验证必需列存在: title, steptext, QuantityIngredients, costtime
    缺失列时抛出 ValueError 并列出缺失列名
    过滤 title 为空的行
    返回 DataFrame
    """
    logger.info(f"正在读取 Excel 文件: {file_path}")

    # 检查文件是否存在
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Excel 文件不存在: {file_path}")

    # 读取 Excel 文件
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        raise ValueError(f"读取 Excel 文件失败: {e}")

    logger.info(f"读取成功，共 {len(df)} 行数据")

    # 验证必需列
    required_columns = ['title', 'steptext', 'QuantityIngredients', 'costtime']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(
            f"Excel 文件缺少必需的列: {', '.join(missing_columns)}\n"
            f"当前列: {', '.join(df.columns.tolist())}"
        )

    # 过滤 title 为空的行
    original_count = len(df)
    df = df[df['title'].notna() & (df['title'].astype(str).str.strip() != '')]
    filtered_count = original_count - len(df)

    if filtered_count > 0:
        logger.warning(f"过滤掉 {filtered_count} 行 title 为空的数据")

    logger.info(f"验证通过，有效数据 {len(df)} 行")

    return df


def check_recipe_exists(name: str, db: Session) -> bool:
    """
    检查菜谱是否已存在
    查询: db.query(Recipe).filter_by(name=name).first()
    找到记录返回True，否则返回False
    记录日志: '跳过已存在: {name}'
    """
    recipe = db.query(Recipe).filter_by(name=name).first()
    if recipe is not None:
        logger.info(f"跳过已存在: {name}")
        return True
    return False


def main():
    """主函数 - 导入脚本入口"""
    parser = argparse.ArgumentParser(
        description='从Excel文件导入菜谱数据到数据库',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python import_recipes.py --file ../source_data/dishes_list.xlsx
  python import_recipes.py --file ../source_data/dishes_list.xlsx --dry-run
  python import_recipes.py --file ../source_data/dishes_list.xlsx --limit 10
        """
    )

    parser.add_argument(
        '--file',
        required=True,
        help='Excel文件路径 (必需)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='模拟运行，不实际写入数据库'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='限制导入数量 (用于测试)'
    )

    args = parser.parse_args()

    logger.info("菜谱导入脚本启动")
    logger.info(f"文件路径: {args.file}")
    if args.dry_run:
        logger.info("模式: 模拟运行 (dry-run)")
    if args.limit:
        logger.info(f"限制数量: {args.limit}")

    # TODO: 后续用户故事将实现完整的导入逻辑
    # US-017: ✅ 加载Excel文件
    # US-018: ✅ 检查菜谱是否存在
    # US-019: 验证和关联食材
    # US-020: 单条导入逻辑
    # US-021: 批量导入逻辑

    try:
        # US-017: 加载 Excel 文件
        df = load_excel(args.file)
        stats = ImportStats()
        stats.total = len(df)
        logger.info(f"Excel 文件加载成功，共 {stats.total} 条菜谱数据")
    except Exception as e:
        logger.error(f"加载 Excel 文件失败: {e}")
        stats = ImportStats()
        stats.failed = 1

    print_summary(stats)


if __name__ == '__main__':
    main()
