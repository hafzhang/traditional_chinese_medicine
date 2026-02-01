"""
菜谱导入脚本
从 source_data/dishes_list_ai_filled.xlsx 导入菜谱数据到数据库
支持 AI 填充的字段: difficulty, constitutions, efficacy_tags, solar_terms
"""

import sys
import os
import pandas as pd
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

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
        parse_cooking_time, parse_ingredients, parse_steps, parse_tags
    )
    print("[OK] 导入配置文件成功")
except ImportError as e:
    print(f"[ERROR] 导入配置文件失败: {e}")
    sys.exit(1)


class RecipeImporter:
    """菜谱导入器"""

    def __init__(self, excel_path: str, db: Session):
        self.excel_path = excel_path
        self.db = db
        self.stats = {
            'total': 0,
            'success': 0,
            'skipped': 0,
            'failed': 0,
            'errors': []
        }

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

    def parse_constitutions(self, value: str) -> list:
        """解析体质标签（中文转代码）"""
        if pd.isna(value) or not value:
            return []

        tags = str(value).replace('，', ',').replace('、', ',').split(',')
        codes = []
        for tag in tags:
            tag = tag.strip()
            if tag in CONSTITUTION_CN_TO_CODE:
                codes.append(CONSTITUTION_CN_TO_CODE[tag])
            elif tag in CONSTITUTION_CODES:
                codes.append(tag)
        return codes

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

    def parse_difficulty(self, value: str, cooking_time: int) -> str:
        """解析难度等级"""
        if pd.isna(value) or not value:
            # 根据烹饪时间推测
            if cooking_time <= 30:
                return 'easy'
            elif cooking_time <= 60:
                return 'medium'
            else:
                return 'hard'

        value = str(value).strip()
        if value in DIFFICULTY_CN_TO_CODE:
            return DIFFICULTY_CN_TO_CODE[value]
        if value in ENUM_VALUES['difficulty']:
            return value
        return 'easy'  # 默认

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

                # 解析标签
                efficacy_tags = None
                if 'efficacy_tags' in row and not pd.isna(row['efficacy_tags']):
                    efficacy_tags = parse_tags(str(row['efficacy_tags']), EFFICACY_TAGS)
                    if not efficacy_tags:
                        efficacy_tags = None

                solar_terms = None
                if 'solar_terms' in row and not pd.isna(row['solar_terms']):
                    solar_terms = parse_tags(str(row['solar_terms']), SOLAR_TERMS)
                    if not solar_terms:
                        solar_terms = None

                # 创建菜谱
                recipe = Recipe(
                    name=str(row['title']).strip(),
                    zid=int(row['zid']) if 'zid' in row and not pd.isna(row['zid']) else None,
                    description=str(row['desc']).strip() if 'desc' in row and not pd.isna(row['desc']) else None,
                    desc=str(row['desc']).strip() if 'desc' in row and not pd.isna(row['desc']) else None,  # PRD 字段
                    tip=str(row['tip']).strip() if 'tip' in row and not pd.isna(row['tip']) else None,
                    meal_type=meal_type,
                    cook_time=cooking_time,  # 向后兼容字段
                    cooking_time=cooking_time,  # PRD 标准字段
                    difficulty=difficulty,
                    servings=int(row.get('servings', 2)) if not pd.isna(row.get('servings')) else 2,
                    suitable_constitutions=suitable_constitutions,
                    avoid_constitutions=avoid_constitutions,
                    efficacy_tags=efficacy_tags,
                    solar_terms=solar_terms,
                    cover_image=row.get('cover_image') if 'cover_image' in row and not pd.isna(row.get('cover_image')) else None,
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
        importer = RecipeImporter(args.file, db)
        df = importer.validate_and_clean_data(df)
        importer.import_recipes(df, dry_run=args.dry_run)
        importer.print_summary()

    finally:
        db.close()


if __name__ == '__main__':
    main()
