# -*- coding: utf-8 -*-
"""
Create Ingredients Table Script
创建 ingredients 表
"""

import sqlite3

def create_ingredients_table():
    """创建 ingredients 表"""
    sql = """
    CREATE TABLE IF NOT EXISTS ingredients (
        id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        aliases JSON,
        category VARCHAR(50),
        nature VARCHAR(20),
        flavor VARCHAR(50),
        meridians JSON,
        suitable_constitutions JSON,
        avoid_constitutions JSON,
        efficacy TEXT,
        nutrition TEXT,
        calories FLOAT DEFAULT 0,
        protein FLOAT DEFAULT 0,
        fat FLOAT DEFAULT 0,
        carbohydrates FLOAT DEFAULT 0,
        dietary_fiber FLOAT DEFAULT 0,
        vitamin_a FLOAT,
        vitamin_b1 FLOAT,
        vitamin_b2 FLOAT,
        vitamin_c FLOAT,
        vitamin_e FLOAT,
        calcium FLOAT,
        iron FLOAT,
        zinc FLOAT,
        potassium FLOAT,
        sodium FLOAT,
        iodine FLOAT,
        selenium FLOAT,
        cooking_methods JSON,
        daily_dosage VARCHAR(50),
        best_time VARCHAR(50),
        precautions TEXT,
        compatible_with JSON,
        incompatible_with JSON,
        compatible_foods JSON,
        incompatible_foods JSON,
        classic_combinations JSON,
        storage_method VARCHAR(50),
        storage_temperature VARCHAR(30),
        storage_humidity VARCHAR(30),
        shelf_life VARCHAR(30),
        preservation_tips TEXT,
        pesticide_risk VARCHAR(20),
        heavy_metal_risk VARCHAR(20),
        microbe_risk VARCHAR(20),
        safety_precautions TEXT,
        cooking_details JSON,
        best_seasons JSON,
        seasonal_benefits JSON,
        image_url VARCHAR(255),
        description TEXT,
        view_count INTEGER DEFAULT 0,
        favorite_count INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME,
        is_deleted BOOLEAN DEFAULT 0
    );
    """

    conn = sqlite3.connect('constitution.db')
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        conn.commit()
        print('[OK] Ingredients table created')
    except Exception as e:
        print(f'[ERROR] Failed to create table: {e}')
    finally:
        conn.close()


def update_recipes_table():
    """更新 recipes 表 - 添加营养字段"""
    sql_commands = [
        "ALTER TABLE recipes ADD COLUMN calories FLOAT DEFAULT 0",
        "ALTER TABLE recipes ADD COLUMN protein FLOAT DEFAULT 0",
        "ALTER TABLE recipes ADD COLUMN fat FLOAT DEFAULT 0",
        "ALTER TABLE recipes ADD COLUMN carbohydrates FLOAT DEFAULT 0",
        "ALTER TABLE recipes ADD COLUMN dietary_fiber FLOAT DEFAULT 0",
        "ALTER TABLE recipes ADD COLUMN nutrition_summary JSON",
        "ALTER TABLE recipes ADD COLUMN key_nutrients JSON",
        "ALTER TABLE recipes ADD COLUMN cooking_method VARCHAR(30)",
        "ALTER TABLE recipes ADD COLUMN cooking_temperature VARCHAR(30)",
        "ALTER TABLE recipes ADD COLUMN nutrition_tips TEXT",
        "ALTER TABLE recipes ADD COLUMN tcm_efficacy TEXT",
        "ALTER TABLE recipes ADD COLUMN tcm_target JSON",
        "ALTER TABLE recipes ADD COLUMN contraindications JSON",
        "ALTER TABLE recipes ADD COLUMN meal_type VARCHAR(20)",
        "ALTER TABLE recipes ADD COLUMN source VARCHAR(100)",
        "ALTER TABLE recipes ADD COLUMN rating FLOAT DEFAULT 0",
        "ALTER TABLE recipes ADD COLUMN review_count INTEGER DEFAULT 0"
    ]

    conn = sqlite3.connect('constitution.db')
    cursor = conn.cursor()

    print("Updating recipes table...")
    for sql in sql_commands:
        try:
            cursor.execute(sql)
            conn.commit()
            print(f'  [OK] {sql[:60]}...')
        except Exception as e:
            if "duplicate column" in str(e).lower():
                print(f'  [SKIP] Column exists: {sql[:60]}...')
            else:
                print(f'  [ERROR] {sql[:60]}...')
                print(f'    Error: {e}')

    conn.close()


if __name__ == "__main__":
    print("Creating ingredients table...")
    create_ingredients_table()

    print("\nUpdating recipes table...")
    update_recipes_table()

    print("\nDone!")
