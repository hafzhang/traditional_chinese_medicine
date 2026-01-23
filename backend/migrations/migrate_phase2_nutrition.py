# -*- coding: utf-8 -*-
"""
Database Migration Script for Phase 2 - Nutrition Enhancement
数据库迁移脚本 - Phase 2 营养增强版

This script adds the following new fields:
- Ingredients: Nutritional data, enhanced pairing info, storage/safety info
- Recipes: Nutritional analysis, enhanced TCM info

Run: python migrations/migrate_phase2_nutrition.py
"""

from sqlalchemy import text
from api.database import engine, get_db, Base
from api.models import Ingredient, Recipe  # Import models to ensure they're registered


def migrate_ingredients_table():
    """迁移 ingredients 表 - 添加营养和搭配字段"""

    sql_statements = [
        # 营养数据 (每100g)
        "ALTER TABLE ingredients ADD COLUMN calories FLOAT DEFAULT 0",
        "ALTER TABLE ingredients ADD COLUMN protein FLOAT DEFAULT 0",
        "ALTER TABLE ingredients ADD COLUMN fat FLOAT DEFAULT 0",
        "ALTER TABLE ingredients ADD COLUMN carbohydrates FLOAT DEFAULT 0",
        "ALTER TABLE ingredients ADD COLUMN dietary_fiber FLOAT DEFAULT 0",

        # 维生素含量 (每100g)
        "ALTER TABLE ingredients ADD COLUMN vitamin_a FLOAT",
        "ALTER TABLE ingredients ADD COLUMN vitamin_b1 FLOAT",
        "ALTER TABLE ingredients ADD COLUMN vitamin_b2 FLOAT",
        "ALTER TABLE ingredients ADD COLUMN vitamin_c FLOAT",
        "ALTER TABLE ingredients ADD COLUMN vitamin_e FLOAT",

        # 矿物质含量 (每100g)
        "ALTER TABLE ingredients ADD COLUMN calcium FLOAT",
        "ALTER TABLE ingredients ADD COLUMN iron FLOAT",
        "ALTER TABLE ingredients ADD COLUMN zinc FLOAT",
        "ALTER TABLE ingredients ADD COLUMN potassium FLOAT",
        "ALTER TABLE ingredients ADD COLUMN sodium FLOAT",
        "ALTER TABLE ingredients ADD COLUMN iodine FLOAT",
        "ALTER TABLE ingredients ADD COLUMN selenium FLOAT",

        # 增强搭配信息 (带原因说明)
        "ALTER TABLE ingredients ADD COLUMN compatible_foods JSON",
        "ALTER TABLE ingredients ADD COLUMN incompatible_foods JSON",
        "ALTER TABLE ingredients ADD COLUMN classic_combinations JSON",

        # 储存与安全
        "ALTER TABLE ingredients ADD COLUMN storage_method VARCHAR(50)",
        "ALTER TABLE ingredients ADD COLUMN storage_temperature VARCHAR(30)",
        "ALTER TABLE ingredients ADD COLUMN storage_humidity VARCHAR(30)",
        "ALTER TABLE ingredients ADD COLUMN shelf_life VARCHAR(30)",
        "ALTER TABLE ingredients ADD COLUMN preservation_tips TEXT",

        # 食材安全
        "ALTER TABLE ingredients ADD COLUMN pesticide_risk VARCHAR(20)",
        "ALTER TABLE ingredients ADD COLUMN heavy_metal_risk VARCHAR(20)",
        "ALTER TABLE ingredients ADD COLUMN microbe_risk VARCHAR(20)",
        "ALTER TABLE ingredients ADD COLUMN safety_precautions TEXT",

        # 烹饪方法详情
        "ALTER TABLE ingredients ADD COLUMN cooking_details JSON",

        # 季节推荐
        "ALTER TABLE ingredients ADD COLUMN best_seasons JSON",
        "ALTER TABLE ingredients ADD COLUMN seasonal_benefits JSON"
    ]

    print("Migrating ingredients table...")
    for sql in sql_statements:
        try:
            with engine.connect() as conn:
                conn.execute(text(sql))
                conn.commit()
            print(f"  [OK] {sql[:80]}...")
        except Exception as e:
            if "duplicate column" in str(e).lower():
                print(f"  [SKIP] Column exists: {sql[:80]}...")
            else:
                print(f"  [ERROR] {sql[:80]}...")
                print(f"    Error: {e}")


def migrate_recipes_table():
    """迁移 recipes 表 - 添加营养分析字段"""

    sql_statements = [
        # 营养分析 (每份)
        "ALTER TABLE recipes ADD COLUMN calories FLOAT DEFAULT 0",
        "ALTER TABLE recipes ADD COLUMN protein FLOAT DEFAULT 0",
        "ALTER TABLE recipes ADD COLUMN fat FLOAT DEFAULT 0",
        "ALTER TABLE recipes ADD COLUMN carbohydrates FLOAT DEFAULT 0",
        "ALTER TABLE recipes ADD COLUMN dietary_fiber FLOAT DEFAULT 0",

        # 营养素含量详情
        "ALTER TABLE recipes ADD COLUMN nutrition_summary JSON",
        "ALTER TABLE recipes ADD COLUMN key_nutrients JSON",

        # 烹饪方法详情
        "ALTER TABLE recipes ADD COLUMN cooking_method VARCHAR(30)",
        "ALTER TABLE recipes ADD COLUMN cooking_temperature VARCHAR(30)",
        "ALTER TABLE recipes ADD COLUMN nutrition_tips TEXT",

        # 中医食疗信息
        "ALTER TABLE recipes ADD COLUMN tcm_efficacy TEXT",
        "ALTER TABLE recipes ADD COLUMN tcm_target JSON",
        "ALTER TABLE recipes ADD COLUMN contraindications JSON",

        # 餐次类型
        "ALTER TABLE recipes ADD COLUMN meal_type VARCHAR(20)",

        # 来源
        "ALTER TABLE recipes ADD COLUMN source VARCHAR(100)",

        # 评分和评论
        "ALTER TABLE recipes ADD COLUMN rating FLOAT DEFAULT 0",
        "ALTER TABLE recipes ADD COLUMN review_count INTEGER DEFAULT 0"
    ]

    print("Migrating recipes table...")
    for sql in sql_statements:
        try:
            with engine.connect() as conn:
                conn.execute(text(sql))
                conn.commit()
            print(f"  [OK] {sql[:80]}...")
        except Exception as e:
            if "duplicate column" in str(e).lower():
                print(f"  [SKIP] Column exists: {sql[:80]}...")
            else:
                print(f"  [ERROR] {sql[:80]}...")
                print(f"    Error: {e}")


def seed_sample_nutrition_data():
    """添加示例营养数据"""

    print("\nAdding sample nutrition data...")

    # 山药营养数据
    sample_data = [
        {
            "name": "山药",
            "calories": 56,
            "protein": 1.9,
            "fat": 0.2,
            "carbohydrates": 11.6,
            "dietary_fiber": 0.8,
            "compatible_foods": [
                {"name": "红枣", "reason": "健脾益气", "benefit": "适合气血两虚"},
                {"name": "枸杞", "reason": "滋补肝肾", "benefit": "适合肝肾阴虚"},
                {"name": "莲子", "reason": "健脾止泻", "benefit": "适合脾虚泄泻"}
            ],
            "classic_combinations": [
                {"name": "山药+红枣", "benefit": "健脾益气", "target": "气血两虚"}
            ],
            "best_seasons": ["秋", "冬"],
            "seasonal_benefits": [
                {"season": "秋", "benefit": "滋阴润燥"},
                {"season": "冬", "benefit": "补脾益肾"}
            ]
        },
        {
            "name": "小米",
            "calories": 358,
            "protein": 9.0,
            "fat": 3.1,
            "carbohydrates": 73.5,
            "dietary_fiber": 1.6,
            "compatible_foods": [
                {"name": "红枣", "reason": "补血安神", "benefit": "适合失眠多梦"},
                {"name": "百合", "reason": "滋阴润肺", "benefit": "适合肺燥咳嗽"}
            ],
            "best_seasons": ["春", "夏", "秋", "冬"],
            "seasonal_benefits": [
                {"season": "春", "benefit": "健脾养胃"}
            ]
        },
        {
            "name": "绿豆",
            "calories": 316,
            "protein": 21.6,
            "fat": 0.8,
            "carbohydrates": 62.0,
            "dietary_fiber": 6.4,
            "best_seasons": ["夏"],
            "seasonal_benefits": [
                {"season": "夏", "benefit": "清热解暑"}
            ]
        },
        {
            "name": "红豆",
            "calories": 303,
            "protein": 20.2,
            "fat": 0.5,
            "carbohydrates": 63.4,
            "dietary_fiber": 12.2,
            "best_seasons": ["夏", "秋"],
            "seasonal_benefits": [
                {"season": "夏", "benefit": "利水消肿"},
                {"season": "秋", "benefit": "健脾利湿"}
            ]
        }
    ]

    for data in sample_data:
        try:
            with engine.connect() as conn:
                # 构建UPDATE语句
                update_fields = []
                params = {}

                if "calories" in data:
                    update_fields.append("calories = :calories")
                    params["calories"] = data["calories"]
                if "protein" in data:
                    update_fields.append("protein = :protein")
                    params["protein"] = data["protein"]
                if "fat" in data:
                    update_fields.append("fat = :fat")
                    params["fat"] = data["fat"]
                if "carbohydrates" in data:
                    update_fields.append("carbohydrates = :carbohydrates")
                    params["carbohydrates"] = data["carbohydrates"]
                if "dietary_fiber" in data:
                    update_fields.append("dietary_fiber = :dietary_fiber")
                    params["dietary_fiber"] = data["dietary_fiber"]
                if "compatible_foods" in data:
                    update_fields.append("compatible_foods = :compatible_foods")
                    import json
                    params["compatible_foods"] = json.dumps(data["compatible_foods"])
                if "classic_combinations" in data:
                    update_fields.append("classic_combinations = :classic_combinations")
                    import json
                    params["classic_combinations"] = json.dumps(data["classic_combinations"])
                if "best_seasons" in data:
                    update_fields.append("best_seasons = :best_seasons")
                    import json
                    params["best_seasons"] = json.dumps(data["best_seasons"])
                if "seasonal_benefits" in data:
                    update_fields.append("seasonal_benefits = :seasonal_benefits")
                    import json
                    params["seasonal_benefits"] = json.dumps(data["seasonal_benefits"])

                if update_fields:
                    sql = f"UPDATE ingredients SET {', '.join(update_fields)} WHERE name = :name"
                    params["name"] = data["name"]
                    conn.execute(text(sql), params)
                    conn.commit()
                    print(f"  [OK] Updated {data['name']} nutrition data")
        except Exception as e:
            print(f"  [ERROR] Failed to update {data['name']}: {e}")


def main():
    """主函数"""
    print("=" * 60)
    print("Phase 2 营养增强版 - 数据库迁移")
    print("=" * 60)

    try:
        # 首先创建所有表
        print("\nCreating database tables...")
        Base.metadata.create_all(bind=engine)
        print("  [OK] Tables created")

        # 迁移 ingredients 表
        migrate_ingredients_table()

        # 迁移 recipes 表
        migrate_recipes_table()

        # 添加示例数据
        seed_sample_nutrition_data()

        print("\n" + "=" * 60)
        print("Migration completed!")
        print("=" * 60)

    except Exception as e:
        print(f"\nMigration failed: {e}")
        raise


if __name__ == "__main__":
    main()
