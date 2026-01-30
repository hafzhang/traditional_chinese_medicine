# -*- coding: utf-8 -*-
"""
Database Migration Script for Recipe Tables
数据库迁移脚本 - 菜谱表

This script ensures the following tables and columns exist:
- recipes: Main recipe table with all Excel import fields
- recipe_ingredients: Recipe-ingredient association table
- recipe_steps: Recipe steps table

Run: python migrations/migrate_recipes.py
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text, inspect
from api.database import engine, Base
from api.models import Recipe, RecipeIngredient, RecipeStep


def migrate_recipes_table():
    """迁移 recipes 表 - 添加缺失的字段"""

    inspector = inspect(engine)
    existing_columns = [c['name'] for c in inspector.get_columns('recipes')] if 'recipes' in inspector.get_table_names() else []

    # Check if carbs column exists (it should be named 'carbs' for Excel import)
    if 'carbs' not in existing_columns:
        print("Adding 'carbs' column to recipes table...")
        try:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE recipes ADD COLUMN carbs FLOAT DEFAULT 0"))
                conn.commit()
            print("  [OK] Added 'carbs' column")
        except Exception as e:
            print(f"  [ERROR] Failed to add 'carbs' column: {e}")
    else:
        print("  [SKIP] 'carbs' column already exists")


def verify_tables_and_indexes():
    """验证表结构和索引"""

    inspector = inspect(engine)
    print("\n=== Verification ===\n")

    # 1. Verify recipes table
    print("1. recipes table:")
    if 'recipes' in inspector.get_table_names():
        columns = [c['name'] for c in inspector.get_columns('recipes')]
        required_fields = ['id', 'name', 'description', 'desc', 'tip', 'cover_image', 'cooking_time', 'difficulty', 'suitable_constitutions', 'avoid_constitutions', 'efficacy_tags', 'solar_terms', 'calories', 'protein', 'fat', 'carbs', 'is_published', 'view_count', 'created_at', 'updated_at']
        missing = [f for f in required_fields if f not in columns]
        if missing:
            print(f"   [FAIL] Missing fields: {missing}")
            return False
        else:
            print("   [PASS] All required fields present")
    else:
        print("   [FAIL] Table does not exist")
        return False

    # 2. Verify recipe_ingredients table
    print("\n2. recipe_ingredients table:")
    if 'recipe_ingredients' in inspector.get_table_names():
        columns = [c['name'] for c in inspector.get_columns('recipe_ingredients')]
        required_fields = ['id', 'recipe_id', 'ingredient_id', 'amount', 'is_main', 'display_order']
        missing = [f for f in required_fields if f not in columns]
        if missing:
            print(f"   [FAIL] Missing fields: {missing}")
            return False
        else:
            print("   [PASS] All required fields present")

        # Check unique constraint
        indexes = inspector.get_indexes('recipe_ingredients')
        unique_indexes = [i for i in indexes if i.get('unique', False)]
        if any('recipe_id' in str(i.get('column_names', [])) and 'ingredient_id' in str(i.get('column_names', [])) for i in unique_indexes):
            print("   [PASS] Unique constraint on (recipe_id, ingredient_id) exists")
        else:
            print("   [FAIL] Unique constraint on (recipe_id, ingredient_id) missing")
            return False
    else:
        print("   [FAIL] Table does not exist")
        return False

    # 3. Verify recipe_steps table
    print("\n3. recipe_steps table:")
    if 'recipe_steps' in inspector.get_table_names():
        columns = [c['name'] for c in inspector.get_columns('recipe_steps')]
        required_fields = ['id', 'recipe_id', 'step_number', 'description', 'image_url', 'duration']
        missing = [f for f in required_fields if f not in columns]
        if missing:
            print(f"   [FAIL] Missing fields: {missing}")
            return False
        else:
            print("   [PASS] All required fields present")
    else:
        print("   [FAIL] Table does not exist")
        return False

    # 4. Verify recipes.name index
    print("\n4. recipes.name index:")
    indexes = inspector.get_indexes('recipes')
    if any('name' in str(i.get('column_names', [])) for i in indexes):
        print("   [PASS] recipes.name index exists")
    else:
        print("   [FAIL] recipes.name index missing")
        return False

    # 5. Verify foreign key constraints
    print("\n5. Foreign key constraints:")
    with engine.connect() as conn:
        result = conn.execute(text('PRAGMA foreign_key_check'))
        fk_checks = result.fetchall()
        if fk_checks:
            print(f"   [FAIL] Foreign key violations: {fk_checks}")
            return False
        else:
            print("   [PASS] No foreign key violations")

    return True


def main():
    """主函数"""
    print("=" * 60)
    print("菜谱表 - 数据库迁移")
    print("=" * 60)

    try:
        # 首先创建所有表（如果不存在）
        print("\nCreating database tables...")
        Base.metadata.create_all(bind=engine)
        print("  [OK] Tables created/verified")

        # 添加缺失的字段
        print("\nMigrating recipes table...")
        migrate_recipes_table()

        # 验证表结构
        success = verify_tables_and_indexes()

        if success:
            print("\n" + "=" * 60)
            print("Migration completed successfully!")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("Migration verification failed!")
            print("=" * 60)
            sys.exit(1)

    except Exception as e:
        print(f"\nMigration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
