#!/usr/bin/env python3
"""
自动生成的食材数据导入脚本
运行此脚本将食材数据导入数据库
"""

import sys
import json
sys.path.insert(0, str(r"C:\Users\Administrator\Desktop\traditional_chinese_medicine\backend"))

from api.database import SessionLocal
from api.models import Ingredient
from datetime import datetime
from pathlib import Path

def import_ingredients():
    """Import ingredients from CSV data"""
    db = SessionLocal()
    try:
        # Load data from JSON file
        data_file = Path(r"C:\Users\Administrator\Desktop\traditional_chinese_medicine\backend\scripts\ingredients_data.json")
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        imported = 0
        for item in data:
            # Check if ingredient already exists
            existing = db.query(Ingredient).filter(Ingredient.name == item['name']).first()
            if existing:
                # Update existing
                for key, value in item.items():
                    setattr(existing, key, value)
                existing.updated_at = datetime.now()
            else:
                # Create new
                ingredient = Ingredient(**item)
                db.add(ingredient)

            imported += 1
            if imported % 100 == 0:
                db.commit()
                print(f"Imported {imported} items...")

        db.commit()
        print(f"Successfully imported {imported} ingredients!")

        # Show some stats
        total = db.query(Ingredient).count()
        with_images = db.query(Ingredient).filter(Ingredient.image_url != None).count()
        print(f"\nTotal ingredients in DB: {total}")
        print(f"With images: {with_images}")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import_ingredients()
