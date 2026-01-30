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
from api.models import Recipe, Ingredient, RecipeIngredient, RecipeStep

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


def validate_and_link_ingredients(parsed_ingredients: List[Dict[str, Any]], db: Session) -> List[RecipeIngredient]:
    """
    验证并关联食材
    遍历解析后的食材列表，查询ingredients表验证食材是否存在
    食材不存在时记录警告并跳过
    食材存在时创建RecipeIngredient对象，第一个设is_main=True
    返回RecipeIngredient对象列表

    Args:
        parsed_ingredients: 解析后的食材列表，格式: [{'name': '山药', 'amount': '50g'}, ...]
        db: 数据库会话

    Returns:
        RecipeIngredient对象列表
    """
    from scripts.recipe_import_config import FOOD_SYNONYMS

    ingredient_relations = []

    for idx, parsed_ingredient in enumerate(parsed_ingredients):
        ingredient_name = parsed_ingredient.get('name')
        amount = parsed_ingredient.get('amount', '')

        if not ingredient_name:
            logger.warning(f"食材名称为空，跳过: {parsed_ingredient}")
            continue

        # 查询食材表
        ingredient = db.query(Ingredient).filter_by(name=ingredient_name).first()

        # 如果直接查询没找到，尝试用同义词查找
        if ingredient is None:
            # 遍历同义词字典，查找是否有匹配
            for standard_name, synonyms in FOOD_SYNONYMS.items():
                if ingredient_name in synonyms:
                    ingredient = db.query(Ingredient).filter_by(name=standard_name).first()
                    if ingredient:
                        logger.info(f"使用同义词匹配: '{ingredient_name}' -> '{standard_name}'")
                        break

        # 如果食材不存在，跳过
        if ingredient is None:
            logger.warning(f"食材不存在，跳过: {ingredient_name}")
            continue

        # 创建RecipeIngredient对象
        # 第一个食材设为主料
        is_main = (idx == 0)

        ingredient_relation = RecipeIngredient(
            ingredient_id=ingredient.id,
            amount=amount,
            is_main=is_main,
            display_order=idx
        )

        ingredient_relations.append(ingredient_relation)
        logger.info(f"关联食材: {ingredient_name} ({amount}) - {'主料' if is_main else '配料'}")

    return ingredient_relations


def import_single_recipe(row: Dict[str, Any], image_map: Dict[str, str], db: Session, dry_run: bool) -> Optional[Recipe]:
    """
    导入单条菜谱
    将Excel行数据转为数据库记录

    步骤1: check_recipe_exists() 检查是否存在
    步骤2: 解析字段 (cooking_time, difficulty, tags)
    步骤3: 智能推测 (constitutions, efficacy, solar_terms)
    步骤4: 解析食材和步骤
    步骤5: validate_and_link_ingredients() 验证食材
    步骤6: match_recipe_image() 匹配图片
    步骤7: 创建Recipe对象并设置所有字段
    步骤8: 添加到db.session (dry_run=False时)

    Args:
        row: Excel行数据 (pandas Series或Dict)
        image_map: 图片文件名映射字典
        db: 数据库会话
        dry_run: 是否为模拟运行

    Returns:
        创建的Recipe对象，失败或跳过时返回None
    """
    from scripts.recipe_import_config import (
        COLUMN_MAPPING,
        parse_cooking_time,
        parse_difficulty,
        parse_tags,
        guess_constitutions,
        guess_efficacy_tags,
        guess_solar_terms,
        parse_ingredients,
        parse_steps,
        match_recipe_image,
        CONSTITUTION_MAP
    )
    import uuid

    # 步骤1: 检查菜谱是否已存在
    recipe_name = row.get('title')
    if not recipe_name:
        logger.warning("菜谱名称为空，跳过")
        return None

    if check_recipe_exists(recipe_name, db):
        return None  # 已存在，跳过

    logger.info(f"开始导入菜谱: {recipe_name}")

    try:
        # 步骤2: 解析基本字段
        # 解析烹饪时间
        cooking_time_str = row.get('costtime')
        cooking_time = parse_cooking_time(cooking_time_str)

        # 解析难度
        difficulty_value = row.get('difficulty')
        difficulty = parse_difficulty(difficulty_value, cooking_time)

        # 步骤3: 智能推测字段
        # 解析食材列表（用于智能推测）
        ingredients_text = row.get('QuantityIngredients', '')
        parsed_ingredients = parse_ingredients(ingredients_text)
        ingredient_names = [ing['name'] for ing in parsed_ingredients]

        # 解析步骤文本（用于提取功效）
        steps_text = row.get('steptext', '')

        # 智能推测功效标签
        efficacy_tags = guess_efficacy_tags(ingredient_names)

        # 智能推测体质
        suitable_constitutions = guess_constitutions(ingredient_names, efficacy_tags, db)

        # 智能推测节气
        solar_terms = guess_solar_terms(ingredient_names, efficacy_tags)

        # 步骤4: 解析食材和步骤
        # 食材已在步骤3中解析

        # 解析步骤
        parsed_steps = parse_steps(steps_text)

        # 步骤5: 验证并关联食材
        ingredient_relations = validate_and_link_ingredients(parsed_ingredients, db)

        # 步骤6: 匹配图片
        cover_image = match_recipe_image(recipe_name, image_map)
        if cover_image:
            logger.info(f"匹配到图片: {cover_image}")
        else:
            logger.info(f"未找到匹配的图片")

        # 步骤7: 创建Recipe对象
        recipe = Recipe(
            id=str(uuid.uuid4()),
            name=recipe_name,
            description=row.get('description', row.get('desc', '')),
            desc=row.get('desc', ''),
            tip=row.get('tip', ''),
            cover_image=cover_image or '',
            cooking_time=cooking_time,
            difficulty=difficulty,
            suitable_constitutions=suitable_constitutions,
            avoid_constitutions=[],  # 暂时为空，后续可扩展
            efficacy_tags=efficacy_tags,
            solar_terms=solar_terms,
            ingredients={'parsed': parsed_ingredients},  # 存储原始解析数据
            steps={'parsed': parsed_steps},  # 存储原始解析数据
            is_published=True,
            view_count=0
        )

        # 添加食材关联
        for relation in ingredient_relations:
            relation.recipe_id = recipe.id
            recipe.ingredient_relations.append(relation)

        # 添加步骤关联
        for step_data in parsed_steps:
            step = RecipeStep(
                id=str(uuid.uuid4()),
                recipe_id=recipe.id,
                step_number=step_data.get('step_number', 0),
                description=step_data.get('description', ''),
                image_url=step_data.get('image_url', ''),
                duration=step_data.get('duration')
            )
            recipe.step_relations.append(step)

        # 步骤8: 添加到数据库
        if not dry_run:
            db.add(recipe)
            db.commit()
            logger.info(f"成功导入菜谱: {recipe_name} (ID: {recipe.id})")
        else:
            logger.info(f"[DRY-RUN] 菜谱导入成功: {recipe_name}")

        return recipe

    except Exception as e:
        logger.error(f"导入菜谱失败: {recipe_name} - {e}")
        db.rollback()
        return None


def import_recipes_batch(
    df: pd.DataFrame,
    limit: Optional[int],
    db: Session,
    dry_run: bool
) -> ImportStats:
    """
    批量导入菜谱
    扫描图片目录，遍历DataFrame导入数据，支持进度显示和事务管理

    扫描图片目录: image_map = scan_dish_images()
    遍历DataFrame (limit限制数量)
    每10条输出进度，每100条提交一次事务
    调用 import_single_recipe() 导入单条
    更新stats: success/skipped/failed
    完成后提交剩余事务
    异常时回滚: db.session.rollback()
    返回ImportStats

    Args:
        df: Excel数据的DataFrame
        limit: 限制导入数量，None表示不限制
        db: 数据库会话
        dry_run: 是否为模拟运行

    Returns:
        ImportStats导入统计对象
    """
    from scripts.recipe_import_config import scan_dish_images

    stats = ImportStats()
    stats.total = min(len(df), limit) if limit else len(df)

    logger.info(f"开始批量导入，总计 {stats.total} 条菜谱")

    # 扫描图片目录
    logger.info("扫描图片目录...")
    # Get project root: scripts/ -> backend/ -> project root
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(scripts_dir)
    project_root = os.path.dirname(backend_dir)
    image_dir = os.path.join(project_root, 'source_data', 'dishes_images')
    image_map = scan_dish_images(image_dir)
    logger.info(f"图片扫描完成，找到 {len(image_map)} 张图片")

    # 确定要处理的行数
    rows_to_process = df.head(limit) if limit else df

    # 遍历导入
    for idx, row in rows_to_process.iterrows():
        try:
            # 调用单条导入
            recipe = import_single_recipe(row, image_map, db, dry_run)

            if recipe is None:
                # 跳过的菜谱（已存在）
                stats.skipped += 1
            else:
                # 成功导入
                stats.success += 1

            # 每10条输出进度
            if (stats.success + stats.skipped + stats.failed) % 10 == 0:
                progress = (stats.success + stats.skipped + stats.failed)
                logger.info(f"进度: {progress}/{stats.total} - {stats}")

            # 每100条提交一次事务（非dry-run模式）
            if not dry_run and (stats.success + stats.skipped + stats.failed) % 100 == 0:
                db.commit()
                logger.info(f"事务提交: 已处理 {stats.success + stats.skipped + stats.failed} 条")

        except Exception as e:
            # 单条导入失败
            recipe_name = row.get('title', '未知')
            error_msg = f"{recipe_name}: {str(e)}"
            stats.add_error(error_msg)
            stats.failed += 1
            logger.error(f"导入失败: {error_msg}")

            # 回滚当前事务
            db.rollback()

    # 提交剩余事务
    if not dry_run and stats.success > 0:
        try:
            db.commit()
            logger.info("最终事务提交完成")
        except Exception as e:
            logger.error(f"最终提交失败: {e}")
            db.rollback()

    return stats


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

    # 已实现的功能:
    # US-017: ✅ 加载Excel文件
    # US-018: ✅ 检查菜谱是否存在
    # US-019: ✅ 验证和关联食材
    # US-020: ✅ 单条导入逻辑
    # US-021: ✅ 批量导入逻辑

    db = None
    stats = ImportStats()

    try:
        # US-017: 加载 Excel 文件
        df = load_excel(args.file)

        # 创建数据库会话
        db = SessionLocal()

        # US-021: 批量导入
        stats = import_recipes_batch(df, args.limit, db, args.dry_run)

        logger.info("导入完成")
        print_summary(stats)

    except FileNotFoundError as e:
        logger.error(f"文件错误: {e}")
        stats.failed = 1
        print_summary(stats)
    except ValueError as e:
        logger.error(f"数据验证错误: {e}")
        stats.failed = 1
        print_summary(stats)
    except Exception as e:
        logger.error(f"导入过程出错: {e}")
        stats.failed = 1
        print_summary(stats)
    finally:
        if db:
            db.close()


if __name__ == '__main__':
    main()
