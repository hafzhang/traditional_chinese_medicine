"""
菜谱导入脚本
从 source_data/dishes_list_ai_filled.xlsx 导入菜谱数据到数据库
支持 AI 填充的字段: difficulty, constitutions, efficacy_tags, solar_terms
"""

import sys
import os
import json
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Any

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(scripts_dir))

from api.database import SessionLocal, Base, engine
from api.models import Recipe, RecipeIngredient, RecipeStep, Ingredient
from sqlalchemy.orm import Session
import re

# 导入配置
try:
    from recipe_import_config import (
        COLUMN_MAPPING, ENUM_VALUES, CONSTITUTION_CODES,
        EFFICACY_TAGS, SOLAR_TERMS, MEAL_TYPE_CN_TO_CODE,
        DIFFICULTY_CN_TO_CODE, CONSTITUTION_CN_TO_CODE,
        parse_cooking_time, parse_ingredients, parse_steps, parse_tags,
        parse_difficulty as parse_difficulty_value,  # Use the config function
        parse_json_field  # Import the JSON field parser
    )
    print("[OK] 导入配置文件成功")
except ImportError as e:
    print(f"[ERROR] 导入配置文件失败: {e}")
    sys.exit(1)


def read_excel_file(file_path: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    读取 Excel 文件并返回数据列表

    Args:
        file_path: Excel 文件路径
        limit: 可选，限制返回的记录数量

    Returns:
        数据字典列表，每行数据转换为一个字典

    Raises:
        FileNotFoundError: 如果文件不存在
        Exception: 如果读取文件失败
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    try:
        df = pd.read_excel(file_path, sheet_name='Sheet1', engine='openpyxl')
    except Exception as e:
        raise Exception(f"读取 Excel 失败: {e}")

    # 跳过 title 为空的行
    df = df.dropna(subset=['title'])

    # 应用数量限制
    if limit is not None:
        df = df.head(limit)

    # 转换为字典列表
    return df.to_dict('records')


def check_recipe_exists(name: str, db: Session) -> bool:
    """
    检查菜谱是否已存在

    Args:
        name: 菜谱名称
        db: 数据库会话

    Returns:
        True 如果菜谱已存在，False 否则
    """
    recipe = db.query(Recipe).filter(Recipe.name == name.strip()).first()
    return recipe is not None


def get_or_create_ingredient(name: str, db: Session) -> Ingredient:
    """
    查找或创建食材

    Args:
        name: 食材名称
        db: 数据库会话

    Returns:
        Ingredient 实例
    """
    # 按名称精确查找
    ingredient = db.query(Ingredient).filter(Ingredient.name == name.strip()).first()
    if ingredient:
        return ingredient

    # 按别名查找
    # 这里简化处理，直接创建新食材
    ingredient = Ingredient(
        name=name.strip(),
        category=None,
        nature=None,
        flavor=None,
        suitable_constitutions=None,
        avoid_constitutions=None,
        efficacy=None,
        nutrition=None,
        aliases=None
    )
    db.add(ingredient)
    db.flush()
    return ingredient


def import_single_recipe(row: Dict[str, Any], db: Session) -> Optional[Recipe]:
    """
    导入单条菜谱

    Args:
        row: Excel 行数据字典
        db: 数据库会话

    Returns:
        Recipe 实例，如果已存在返回 None
    """
    # 检查是否已存在
    name = str(row.get('title', '')).strip()
    if not name:
        return None

    if check_recipe_exists(name, db):
        return None

    # 解析数据
    cooking_time = parse_cooking_time(row.get('costtime'))

    # 解析难度
    difficulty = parse_difficulty_value(row.get('difficulty'))
    if difficulty is None:
        # 根据烹饪时间推测
        if cooking_time <= 30:
            difficulty = 'easy'
        elif cooking_time <= 60:
            difficulty = 'medium'
        elif cooking_time <= 120:
            difficulty = 'harder'
        else:
            difficulty = 'hard'

    # 解析体质
    suitable_constitutions = parse_json_field(row.get('suitable_constitutions'))
    avoid_constitutions = parse_json_field(row.get('avoid_constitutions'))

    # 解析标签
    efficacy_tags = parse_json_field(row.get('efficacy_tags'))
    solar_terms = parse_json_field(row.get('solar_terms'))
    if solar_terms:
        solar_terms = [s for s in solar_terms if s in SOLAR_TERMS]
        if not solar_terms:
            solar_terms = None

    # Convert lists to JSON strings explicitly (workaround for SQLite JSON binding issue)
    suitable_constitutions_json = json.dumps(suitable_constitutions, ensure_ascii=False) if suitable_constitutions else None
    avoid_constitutions_json = json.dumps(avoid_constitutions, ensure_ascii=False) if avoid_constitutions else None
    efficacy_tags_json = json.dumps(efficacy_tags, ensure_ascii=False) if efficacy_tags else None
    solar_terms_json = json.dumps(solar_terms, ensure_ascii=False) if solar_terms else None

    # 创建菜谱
    recipe = Recipe(
        name=name,
        description=str(row.get('desc', '')).strip() if row.get('desc') and not pd.isna(row.get('desc')) else None,
        desc=str(row.get('desc', '')).strip() if row.get('desc') and not pd.isna(row.get('desc')) else None,
        tip=str(row.get('tip', '')).strip() if row.get('tip') and not pd.isna(row.get('tip')) else None,
        cooking_time=cooking_time,
        difficulty=difficulty,
        suitable_constitutions=suitable_constitutions_json,
        avoid_constitutions=avoid_constitutions_json,
        efficacy_tags=efficacy_tags_json,
        solar_terms=solar_terms_json,
        servings=2,
        is_published=True,
        view_count=0
    )

    db.add(recipe)
    db.flush()  # 获取 recipe.id

    # 解析并添加食材
    ingredients = parse_ingredients(row.get('QuantityIngredients'))
    for ing in ingredients:
        ingredient = get_or_create_ingredient(ing['name'], db)
        recipe_ing = RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=ingredient.id,
            ingredient_name=ing['name'],
            amount=ing['amount'],
            is_main=ing['is_main'],
            display_order=ing['display_order']
        )
        db.add(recipe_ing)

    # 解析并添加步骤
    steps = parse_steps(row.get('steptext'))
    for step in steps:
        recipe_step = RecipeStep(
            recipe_id=recipe.id,
            step_number=step['step_number'],
            description=step['description'],
            duration=step.get('duration')
        )
        db.add(recipe_step)

    db.commit()
    return recipe


def import_recipes(file_path: str, limit: Optional[int] = None, dry_run: bool = False) -> Dict[str, Any]:
    """
    批量导入菜谱

    Args:
        file_path: Excel 文件路径
        limit: 可选，限制导入数量
        dry_run: 模拟运行，不实际写入数据库

    Returns:
        导入统计字典: {total: N, success: X, skipped: Y, failed: Z, errors: [...]}
    """
    # 读取 Excel
    rows = read_excel_file(file_path, limit)

    stats = {
        'total': 0,
        'success': 0,
        'skipped': 0,
        'failed': 0,
        'errors': []
    }

    db = SessionLocal()

    try:
        for idx, row in enumerate(rows):
            stats['total'] += 1

            try:
                if dry_run:
                    # 模拟运行，只检查是否已存在
                    name = str(row.get('title', '')).strip()
                    if name and check_recipe_exists(name, db):
                        stats['skipped'] += 1
                    else:
                        stats['success'] += 1
                else:
                    # 正式导入
                    recipe = import_single_recipe(row, db)
                    if recipe is None:
                        stats['skipped'] += 1
                    else:
                        stats['success'] += 1

                # 每 100 条打印进度
                if (stats['success'] + stats['skipped'] + stats['failed']) % 100 == 0:
                    print(f"进度: 成功 {stats['success']}, 跳过 {stats['skipped']}, 失败 {stats['failed']}")

            except Exception as e:
                stats['failed'] += 1
                error_msg = f"{row.get('title', 'Unknown')}: {str(e)}"
                stats['errors'].append(error_msg)
                db.rollback()

    finally:
        db.close()

    return stats


def dry_run_import(file_path: str, limit: Optional[int] = None) -> None:
    """
    干运行模式，打印解析结果但不写入数据库

    Args:
        file_path: Excel 文件路径
        limit: 可选，限制处理的记录数量
    """
    rows = read_excel_file(file_path, limit)

    print(f"\n{'='*60}")
    print(f"干运行模式 - 共 {len(rows)} 条记录")
    print(f"{'='*60}\n")

    for idx, row in enumerate(rows):
        print(f"\n--- 记录 {idx + 1} ---")
        print(f"标题: {row.get('title', 'N/A')}")
        print(f"描述: {str(row.get('desc', ''))[:50]}..." if row.get('desc') else "描述: N/A")
        print(f"烹饪时间: {row.get('costtime', 'N/A')}")

        # 解析并显示字段
        cooking_time = parse_cooking_time(row.get('costtime'))
        print(f"解析后时间: {cooking_time} 分钟")

        difficulty = parse_difficulty_value(row.get('difficulty'))
        print(f"难度: {difficulty or 'N/A'}")

        constitutions = parse_json_field(row.get('suitable_constitutions'))
        print(f"适合体质: {constitutions or 'N/A'}")

        efficacy_tags = parse_json_field(row.get('efficacy_tags'))
        print(f"功效标签: {efficacy_tags or 'N/A'}")

        solar_terms = parse_json_field(row.get('solar_terms'))
        print(f"节气标签: {solar_terms or 'N/A'}")

        ingredients = parse_ingredients(row.get('QuantityIngredients'))
        print(f"食材数量: {len(ingredients)}")
        if ingredients:
            for ing in ingredients[:3]:  # 只显示前3个
                print(f"  - {ing['name']}: {ing['amount']}")
            if len(ingredients) > 3:
                print(f"  ... 还有 {len(ingredients) - 3} 个食材")

        steps = parse_steps(row.get('steptext'))
        print(f"步骤数量: {len(steps)}")

    print(f"\n{'='*60}")
    print(f"干运行完成")
    print(f"{'='*60}")


def export_failed_recipes(failed: List[Dict[str, Any]], output_path: str) -> None:
    """
    导出失败的菜谱到 CSV 文件

    Args:
        failed: 失败记录列表，每个元素包含 {title: str, error: str}
        output_path: 输出 CSV 文件路径
    """
    import csv

    # 准备数据
    headers = ['title', 'error']
    rows = []
    for item in failed:
        # item 可能是字符串 "title: error" 或字典
        if isinstance(item, dict):
            rows.append([item.get('title', 'N/A'), item.get('error', 'N/A')])
        elif isinstance(item, str):
            # 解析 "title: error" 格式
            parts = item.split(':', 1)
            if len(parts) == 2:
                rows.append([parts[0].strip(), parts[1].strip()])
            else:
                rows.append([item, 'N/A'])
        else:
            rows.append([str(item), 'N/A'])

    # 写入 CSV 文件 (UTF-8 with BOM)
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"已导出 {len(rows)} 条失败记录到: {output_path}")


class RecipeImporter:
    """菜谱导入器"""

    def __init__(self, excel_path: str, db: Session, verbose: bool = False):
        self.excel_path = excel_path
        self.db = db
        self.verbose = verbose
        self.stats = {
            'total': 0,
            'success': 0,
            'skipped': 0,
            'failed': 0,
            'errors': []
        }

    def log(self, message: str, level: str = "info"):
        """输出日志"""
        if self.verbose or level in ["error", "warning"]:
            print(f"[{level.upper()}] {message}")

    def validate_and_clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """验证和清理数据"""
        print(f"\n原始数据: {len(df)} 条")

        # 删除没有标题的行
        df = df.dropna(subset=['title'])
        print(f"清理后: {len(df)} 条")

        return df

    def get_ingredient_id(self, ingredient_name: str) -> int:
        """根据食材名称查找 ID"""
        ingredient = self.db.query(Ingredient).filter(
            Ingredient.name == ingredient_name
        ).first()

        if ingredient:
            return ingredient.id

        # 如果不存在，可以选择创建或跳过
        # 这里选择返回 None，后续记录错误
        return None

    def parse_constitutions(self, value) -> list:
        """解析体质标签（JSON数组或中文转代码）"""
        if pd.isna(value) or not value:
            return []

        # First try to parse as JSON array
        result = parse_json_field(value)
        if result:
            return result

        # Fallback to Chinese-to-code mapping
        tags = str(value).replace('，', ',').replace('、', ',').split(',')
        codes = []
        for tag in tags:
            tag = tag.strip()
            if tag in CONSTITUTION_CN_TO_CODE:
                codes.append(CONSTITUTION_CN_TO_CODE[tag])
            elif tag in CONSTITUTION_CODES:
                codes.append(tag)
        return codes if codes else []

    def parse_meal_type(self, value: str) -> str:
        """解析餐次类型（中文转代码）"""
        if pd.isna(value) or not value:
            # 根据 title 或 cid 推测
            return self.guess_meal_type(value)

        value = str(value).strip()
        if value in MEAL_TYPE_CN_TO_CODE:
            return MEAL_TYPE_CN_TO_CODE[value]
        if value in ENUM_VALUES['meal_type']:
            return value
        return 'dinner'  # 默认

    def guess_meal_type(self, title: str) -> str:
        """根据菜名推测餐次类型"""
        if not title or pd.isna(title):
            return 'dinner'

        title = str(title)
        if any(word in title for word in ['粥', '汤', '豆浆', '牛奶', '早餐', '燕麦']):
            return 'breakfast'
        elif any(word in title for word in ['面', '粉', '饭', '包', '饺']):
            return 'lunch'
        elif any(word in title for word in ['甜品', '糕点', '小食']):
            return 'snack'
        elif any(word in title for word in ['汤', '羹']):
            return 'soup'
        return 'dinner'

    def parse_difficulty(self, value: str, cooking_time: int = 30) -> str:
        """解析难度等级 - wrapper for config function"""
        # Use the imported parse_difficulty_value function
        result = parse_difficulty_value(value)
        if result is None:
            # Fallback: estimate from cooking time
            if cooking_time <= 30:
                return 'easy'
            elif cooking_time <= 60:
                return 'medium'
            elif cooking_time <= 120:
                return 'harder'
            else:
                return 'hard'
        return result

    def import_recipes(self, df: pd.DataFrame, dry_run: bool = False):
        """导入菜谱"""
        print(f"\n{'='*60}")
        print(f"导入模式: {'模拟运行 (dry-run)' if dry_run else '正式导入'}")
        print(f"{'='*60}\n")

        for idx, row in df.iterrows():
            self.stats['total'] += 1

            try:
                # 检查是否已存在
                existing = self.db.query(Recipe).filter(
                    Recipe.name == str(row['title']).strip()
                ).first()

                if existing:
                    self.stats['skipped'] += 1
                    if self.stats['skipped'] <= 5:
                        print(f"[SKIP] 跳过 (已存在): {row['title']}")
                    continue

                # 解析数据
                cooking_time = parse_cooking_time(row.get('costtime'))
                meal_type = self.parse_meal_type(row.get('meal_type'))
                difficulty = self.parse_difficulty(row.get('difficulty'), cooking_time)
                suitable_constitutions = self.parse_constitutions(row.get('suitable_constitutions'))
                avoid_constitutions = self.parse_constitutions(row.get('avoid_constitutions'))

                # 解析标签 - use parse_json_field for JSON arrays
                efficacy_tags = parse_json_field(row.get('efficacy_tags'))
                # Filter to only valid tags if needed, or keep all
                # For now, keep whatever is in the Excel since efficacy_tags may contain Chinese values

                solar_terms = parse_json_field(row.get('solar_terms'))
                # Filter to only valid solar terms
                if solar_terms:
                    solar_terms = [s for s in solar_terms if s in SOLAR_TERMS]
                    if not solar_terms:
                        solar_terms = None

                # Convert lists to JSON strings explicitly (workaround for SQLite JSON binding issue)
                suitable_constitutions_json = json.dumps(suitable_constitutions, ensure_ascii=False) if suitable_constitutions else None
                avoid_constitutions_json = json.dumps(avoid_constitutions, ensure_ascii=False) if avoid_constitutions else None
                efficacy_tags_json = json.dumps(efficacy_tags, ensure_ascii=False) if efficacy_tags else None
                solar_terms_json = json.dumps(solar_terms, ensure_ascii=False) if solar_terms else None

                # 创建菜谱
                recipe = Recipe(
                    name=str(row['title']).strip(),
                    # zid: Excel's zid contains Chinese text, not numeric IDs - skip it
                    # cid: Excel's cid contains multi-line text, not IDs - skip it
                    zid=None,  # No valid numeric ID in Excel
                    description=str(row['desc']).strip() if 'desc' in row and not pd.isna(row['desc']) else None,
                    desc=str(row['desc']).strip() if 'desc' in row and not pd.isna(row['desc']) else None,  # PRD 字段

                    tip=str(row['tip']).strip() if 'tip' in row and not pd.isna(row['tip']) else None,
                    meal_type=meal_type,
                    cook_time=cooking_time,  # 向后兼容字段
                    cooking_time=cooking_time,  # PRD 标准字段
                    difficulty=difficulty,

                    servings=2,  # Default value since Excel doesn't have servings column
                    suitable_constitutions=suitable_constitutions_json,
                    avoid_constitutions=avoid_constitutions_json,
                    efficacy_tags=efficacy_tags_json,
                    solar_terms=solar_terms_json,
                    cover_image=None,  # No cover_image column in Excel
                    confidence=float(row['confidence']) if 'confidence' in row and not pd.isna(row['confidence']) else None,
                    cooking_method=str(row['method']).strip() if 'method' in row and not pd.isna(row['method']) else None,
                    is_published=True,
                    view_count=0
                )

                if not dry_run:
                    self.db.add(recipe)
                    self.db.flush()  # 获取 recipe.id

                    # 解析并添加食材
                    ingredients = parse_ingredients(row.get('QuantityIngredients'))
                    for ing in ingredients:
                        ing_id = self.get_ingredient_id(ing['name'])
                        # 创建 RecipeIngredient 记录，无论 ingredient_id 是否存在
                        recipe_ing = RecipeIngredient(
                            recipe_id=recipe.id,
                            ingredient_id=ing_id,  # 可以为 None，如果食材不在库中
                            ingredient_name=ing['name'],  # 保存食材名称
                            amount=ing['amount'],
                            is_main=ing['is_main'],
                            display_order=ing['display_order']
                        )
                        self.db.add(recipe_ing)

                    # 解析并添加步骤
                    steps = parse_steps(row.get('steptext'))
                    for step in steps:
                        recipe_step = RecipeStep(
                            recipe_id=recipe.id,
                            step_number=step['step_number'],
                            description=step['description'],
                            duration=step.get('duration')
                        )
                        self.db.add(recipe_step)

                    self.db.commit()

                self.stats['success'] += 1
                if self.stats['success'] <= 10 or self.stats['success'] % 100 == 0:
                    print(f"[OK] 导入成功 ({self.stats['success']}): {row['title'][:30]}...")

            except Exception as e:
                self.stats['failed'] += 1
                error_msg = f"{row.get('title', 'Unknown')}: {str(e)}"
                self.stats['errors'].append(error_msg)
                if self.stats['failed'] <= 5:
                    print(f"[ERROR] 导入失败: {error_msg}")
                self.db.rollback()

    def print_summary(self):
        """打印导入摘要"""
        print(f"\n{'='*60}")
        print("导入摘要")
        print(f"{'='*60}")
        print(f"总数:       {self.stats['total']}")
        print(f"成功:       {self.stats['success']}")
        print(f"跳过:       {self.stats['skipped']}")
        print(f"失败:       {self.stats['failed']}")

        if self.stats['errors']:
            print(f"\n失败详情:")
            for error in self.stats['errors'][:10]:
                print(f"  - {error}")
            if len(self.stats['errors']) > 10:
                print(f"  ... 还有 {len(self.stats['errors']) - 10} 条错误")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='导入菜谱数据')
    parser.add_argument('--file', default='../source_data/dishes_list_ai_filled.xlsx', help='Excel 文件路径')
    parser.add_argument('--dry-run', action='store_true', help='模拟运行，不实际导入')
    parser.add_argument('--limit', type=int, help='限制导入数量（测试用）')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出模式')
    args = parser.parse_args()

    # 检查文件是否存在
    if not os.path.exists(args.file):
        print(f"文件不存在: {args.file}")
        # 尝试相对于脚本目录的路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        alt_path = os.path.join(script_dir, args.file)
        if not os.path.exists(alt_path):
            print(f"尝试备用路径: {alt_path}")
            print(f"文件不存在: {alt_path}")
            sys.exit(1)
        args.file = alt_path

    print(f"读取文件: {args.file}")

    # 读取 Excel - 使用 engine='openpyxl' 以获得更好的兼容性
    try:
        df = pd.read_excel(args.file, sheet_name='Sheet1', engine='openpyxl')
        print(f"[OK] 成功读取 {len(df)} 条记录")
        print(f"[INFO] 列名: {list(df.columns)[:10]}...")  # 只显示前10列
    except Exception as e:
        print(f"[ERROR] 读取 Excel 失败: {e}")
        sys.exit(1)

    # 限制数量（测试用）
    if args.limit:
        df = df.head(args.limit)
        print(f"限制导入数量为: {args.limit}")

    # 创建数据库会话
    db = SessionLocal()

    try:
        # 导入
        importer = RecipeImporter(args.file, db, verbose=args.verbose)
        df = importer.validate_and_clean_data(df)
        importer.import_recipes(df, dry_run=args.dry_run)
        importer.print_summary()

    finally:
        db.close()


if __name__ == '__main__':
    main()
