#!/usr/bin/env python3
"""
Database Seeding Script
数据库初始化脚本
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from api.database import engine, SessionLocal, Base
from api.models import Question, Food, Recipe, ConstitutionInfo
from api.data import QUESTIONS_DATA, FOODS_DATA, CONSTITUTION_INFO_DATA
from api.config import settings


def seed_questions(db: Session):
    """种子题目数据"""
    print("📝 Seeding questions...")

    # Check if questions already exist
    existing_count = db.query(Question).count()
    if existing_count >= 30:
        print(f"   ✓ Questions already exist ({existing_count} found)")
        return

    for q_data in QUESTIONS_DATA:
        question = Question(
            question_number=q_data["number"],
            content=q_data["content"],
            constitution_type=q_data["constitution_type"],
            options={
                "1": "没有",
                "2": "很少",
                "3": "有时",
                "4": "经常",
                "5": "总是"
            }
        )
        db.add(question)

    db.commit()
    print(f"   ✓ Seeded {len(QUESTIONS_DATA)} questions")


def seed_foods(db: Session):
    """种子食物数据"""
    print("🍎 Seeding foods...")

    # Check if foods already exist
    existing_count = db.query(Food).count()
    if existing_count >= len(FOODS_DATA):
        print(f"   ✓ Foods already exist ({existing_count} found)")
        return

    for f_data in FOODS_DATA:
        food = Food(
            name=f_data["name"],
            name_en=f_data.get("name_en"),
            nature=f_data.get("nature"),
            flavor=f_data.get("flavor"),
            meridians=f_data.get("meridians", []),
            suitable_constitutions=f_data.get("suitable_constitutions", []),
            avoid_constitutions=f_data.get("avoid_constitutions", []),
            effects=f_data.get("effects", []),
            recipes=f_data.get("recipes", [])
        )
        db.add(food)

    db.commit()
    print(f"   ✓ Seeded {len(FOODS_DATA)} foods")


def seed_recipes(db: Session):
    """种子食谱数据"""
    print("🍳 Seeding recipes...")

    # Sample recipes for each constitution
    recipes_data = [
        {
            "name": "黄芪炖鸡",
            "name_en": "Astragalus Chicken Stew",
            "suitable_constitutions": ["qi_deficiency"],
            "ingredients": [
                {"name": "鸡肉", "amount": "500g"},
                {"name": "黄芪", "amount": "30g"},
                {"name": "生姜", "amount": "3片"}
            ],
            "steps": [
                "鸡肉切块焯水",
                "黄芪洗净备用",
                "所有材料放入砂锅",
                "加水炖煮2小时"
            ],
            "description": "补气养血，适合气虚体质",
            "servings": 4,
            "preparation_time": 120,
            "difficulty": "简单"
        },
        {
            "name": "当归生姜羊肉汤",
            "name_en": "Angelica Lamb Soup",
            "suitable_constitutions": ["yang_deficiency"],
            "ingredients": [
                {"name": "羊肉", "amount": "500g"},
                {"name": "当归", "amount": "15g"},
                {"name": "生姜", "amount": "30g"}
            ],
            "steps": [
                "羊肉切块焯水",
                "当归、生姜洗净",
                "所有材料放入砂锅",
                "加水炖煮2小时"
            ],
            "description": "温阳散寒，适合阳虚体质",
            "servings": 4,
            "preparation_time": 120,
            "difficulty": "简单"
        },
        {
            "name": "百合银耳汤",
            "name_en": "Lily Bulb White Fungus Soup",
            "suitable_constitutions": ["yin_deficiency"],
            "ingredients": [
                {"name": "百合", "amount": "30g"},
                {"name": "银耳", "amount": "15g"},
                {"name": "冰糖", "amount": "适量"}
            ],
            "steps": [
                "银耳泡发撕成小朵",
                "百合洗净",
                "放入锅中加适量水",
                "小火炖煮1小时，加冰糖调味即可"
            ],
            "description": "滋阴润燥，适合阴虚体质",
            "servings": 2,
            "preparation_time": 60,
            "difficulty": "简单"
        },
        {
            "name": "冬瓜薏米汤",
            "name_en": "Winter Melon Coix Seed Soup",
            "suitable_constitutions": ["phlegm_damp", "damp_heat"],
            "ingredients": [
                {"name": "冬瓜", "amount": "300g"},
                {"name": "薏米", "amount": "50g"},
                {"name": "生姜", "amount": "2片"}
            ],
            "steps": [
                "冬瓜去皮切块",
                "薏米提前浸泡",
                "所有材料放入锅中",
                "加水煮1小时"
            ],
            "description": "利水渗湿，适合痰湿质和湿热质",
            "servings": 3,
            "preparation_time": 60,
            "difficulty": "简单"
        },
        {
            "name": "山楂玫瑰花茶",
            "name_en": "Hawthorn Rose Tea",
            "suitable_constitutions": ["blood_stasis", "qi_depression"],
            "ingredients": [
                {"name": "山楂", "amount": "10g"},
                {"name": "玫瑰花", "amount": "5g"},
                {"name": "冰糖", "amount": "适量"}
            ],
            "steps": [
                "山楂、玫瑰花洗净",
                "用开水冲泡",
                "焖10分钟即可饮用"
            ],
            "description": "活血化瘀，疏肝解郁",
            "servings": 1,
            "preparation_time": 10,
            "difficulty": "简单"
        }
    ]

    # Check if recipes already exist
    existing_count = db.query(Recipe).count()
    if existing_count >= len(recipes_data):
        print(f"   ✓ Recipes already exist ({existing_count} found)")
        return

    for r_data in recipes_data:
        recipe = Recipe(
            name=r_data["name"],
            name_en=r_data.get("name_en"),
            suitable_constitutions=r_data["suitable_constitutions"],
            ingredients=r_data["ingredients"],
            steps=r_data["steps"],
            description=r_data.get("description"),
            servings=r_data.get("servings"),
            preparation_time=r_data.get("preparation_time"),
            difficulty=r_data.get("difficulty")
        )
        db.add(recipe)

    db.commit()
    print(f"   ✓ Seeded {len(recipes_data)} recipes")


def seed_constitution_info(db: Session):
    """种子体质信息数据"""
    print("📋 Seeding constitution info...")

    # Check if constitution info already exists
    existing_count = db.query(ConstitutionInfo).count()
    if existing_count >= 9:
        print(f"   ✓ Constitution info already exists ({existing_count} found)")
        return

    for ctype, c_data in CONSTITUTION_INFO_DATA.items():
        info = ConstitutionInfo(
            constitution_type=ctype,
            constitution_name=c_data["name"],
            description=c_data.get("description"),
            characteristics=c_data.get("characteristics"),
            regulation_principles=c_data.get("regulation_principles"),
            taboos=c_data.get("taboos")
        )
        db.add(info)

    db.commit()
    print(f"   ✓ Seeded {len(CONSTITUTION_INFO_DATA)} constitution types")


def main():
    """主函数"""
    print("=" * 50)
    print("🌱 Database Seeding")
    print("=" * 50)
    print(f"Database: {settings.DATABASE_URL[:30]}...")
    print()

    # Create all tables
    print("🔨 Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("   ✓ Tables created")
    print()

    # Get database session
    db = SessionLocal()

    try:
        # Seed all data
        seed_questions(db)
        seed_foods(db)
        seed_recipes(db)
        seed_constitution_info(db)

        print()
        print("=" * 50)
        print("✅ Database seeding completed successfully!")
        print("=" * 50)

    except Exception as e:
        print()
        print("=" * 50)
        print(f"❌ Error during seeding: {e}")
        print("=" * 50)
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
