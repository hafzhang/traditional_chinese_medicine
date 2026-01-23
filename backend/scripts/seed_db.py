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
from api.models import Question, Food, Recipe, Ingredient, ConstitutionInfo, Acupoint
from api.data import QUESTIONS_DATA, FOODS_DATA, CONSTITUTION_INFO_DATA
from api.data.acupoints import ACUPOINTS_DATA
from api.config import settings


# 食材数据
INGREDIENTS_DATA = [
    {
        "name": "山药",
        "aliases": ["怀山药", "淮山", "薯蓣"],
        "category": "蔬菜",
        "nature": "平",
        "flavor": "甘",
        "meridians": ["脾", "肺", "肾"],
        "suitable_constitutions": ["qi_deficiency", "yin_deficiency"],
        "avoid_constitutions": ["phlegm_damp"],
        "efficacy": "健脾养胃、补肺益肾",
        "nutrition": "含黏液蛋白、维生素、淀粉酶等",
        "calories": 56,
        "protein": 1.9,
        "fat": 0.2,
        "carbohydrates": 12.4,
        "dietary_fiber": 0.8,
        "cooking_methods": ["蒸", "煮", "炖", "炒"],
        "daily_dosage": "100-200g",
        "best_time": "早晚餐",
        "precautions": "便秘者少食",
        "compatible_foods": ["鸡肉", "排骨", "莲子", "红枣"],
        "incompatible_foods": ["柿子", "香蕉"],
        "classic_combinations": ["山药+莲子：健脾益肾", "山药+排骨：滋补养身", "山药+红枣：补气养血"],
        "image_url": "/images/ingredients/shanyao.jpg",
        "description": "山药是药食两用的滋补佳品，有健脾益胃、补肺益肾的功效。"
    },
    {
        "name": "黄芪",
        "aliases": ["绵黄芪", "北黄芪"],
        "category": "药材",
        "nature": "微温",
        "flavor": "甘",
        "meridians": ["脾", "肺"],
        "suitable_constitutions": ["qi_deficiency"],
        "avoid_constitutions": ["yin_deficiency", "damp_heat"],
        "efficacy": "补气升阳、固表止汗、利水消肿",
        "nutrition": "含黄芪甲苷、黄芪多糖等",
        "calories": 0,
        "cooking_methods": ["煮", "炖", "泡茶"],
        "daily_dosage": "10-30g",
        "best_time": "早晨",
        "precautions": "感冒发热、阴虚火旺者慎用",
        "compatible_foods": ["鸡肉", "党参", "红枣", "枸杞"],
        "incompatible_foods": ["萝卜", "绿茶"],
        "classic_combinations": ["黄芪+鸡肉：补气养血", "黄芪+党参：健脾补气", "黄芪+红枣：益气养血"],
        "image_url": "/images/ingredients/huangqi.jpg",
        "description": "黄芪是补气要药，有补气升阳、固表止汗的作用。"
    },
    {
        "name": "当归",
        "aliases": ["全当归", "秦归"],
        "category": "药材",
        "nature": "温",
        "flavor": "甘、辛",
        "meridians": ["肝", "心", "脾"],
        "suitable_constitutions": ["yang_deficiency", "blood_stasis"],
        "avoid_constitutions": ["damp_heat", "phlegm_damp"],
        "efficacy": "补血活血、调经止痛、润肠通便",
        "nutrition": "含藁本内酯、当归酮等",
        "calories": 0,
        "cooking_methods": ["煮", "炖", "泡酒"],
        "daily_dosage": "6-15g",
        "best_time": "早晚",
        "precautions": "湿盛中满、大便泄泻者慎用",
        "compatible_foods": ["羊肉", "黄芪", "红枣", "枸杞"],
        "incompatible_foods": ["绿茶", "萝卜"],
        "classic_combinations": ["当归+羊肉：温补气血", "当归+黄芪：气血双补", "当归+生姜：温经散寒"],
        "image_url": "/images/ingredients/danggui.jpg",
        "description": "当归是补血要药，有补血活血、调经止痛的功效。"
    },
    {
        "name": "百合",
        "aliases": ["野百合", "白百合"],
        "category": "蔬菜",
        "nature": "微寒",
        "flavor": "甘",
        "meridians": ["肺", "心"],
        "suitable_constitutions": ["yin_deficiency"],
        "avoid_constitutions": ["yang_deficiency"],
        "efficacy": "养阴润肺、清心安神",
        "nutrition": "含秋水仙碱、淀粉、蛋白质等",
        "calories": 162,
        "protein": 3.2,
        "fat": 0.1,
        "carbohydrates": 38.8,
        "dietary_fiber": 1.7,
        "cooking_methods": ["煮", "炖", "炒"],
        "daily_dosage": "10-30g",
        "best_time": "晚餐",
        "precautions": "风寒咳嗽、脾胃虚寒者慎用",
        "compatible_foods": ["银耳", "莲子", "鸡蛋", "绿豆"],
        "incompatible_foods": ["羊肉", "辣椒"],
        "classic_combinations": ["百合+银耳：滋阴润肺", "百合+莲子：养心安神", "百合+鸡蛋：润肺止咳"],
        "image_url": "/images/ingredients/baihe.jpg",
        "description": "百合是养阴润肺佳品，有清心安神的作用。"
    },
    {
        "name": "银耳",
        "aliases": ["白木耳", "雪耳"],
        "category": "菌藻",
        "nature": "平",
        "flavor": "甘",
        "meridians": ["肺", "胃", "肾"],
        "suitable_constitutions": ["yin_deficiency"],
        "avoid_constitutions": [],
        "efficacy": "滋阴润肺、养胃生津",
        "nutrition": "含银耳多糖、膳食纤维等",
        "calories": 200,
        "protein": 10,
        "fat": 1.4,
        "carbohydrates": 36.9,
        "dietary_fiber": 30.4,
        "cooking_methods": ["煮", "炖"],
        "daily_dosage": "6-15g",
        "best_time": "下午",
        "precautions": "外感风寒、糖尿病患者慎用",
        "compatible_foods": ["百合", "莲子", "红枣", "枸杞"],
        "incompatible_foods": ["萝卜", "菠菜"],
        "classic_combinations": ["银耳+百合：滋阴润燥", "银耳+莲子：养心安神", "银耳+红枣：美容养颜"],
        "image_url": "/images/ingredients/yiner.jpg",
        "description": "银耳是滋阴润肺的佳品，有菌中明珠之称。"
    },
    {
        "name": "薏米",
        "aliases": ["薏苡仁", "薏仁米"],
        "category": "谷物",
        "nature": "微寒",
        "flavor": "甘、淡",
        "meridians": ["脾", "胃", "肺", "肾"],
        "suitable_constitutions": ["phlegm_damp", "damp_heat"],
        "avoid_constitutions": ["yang_deficiency"],
        "efficacy": "利水渗湿、健脾止泻",
        "nutrition": "含薏苡仁酯、蛋白质、碳水化合物等",
        "calories": 357,
        "protein": 12.8,
        "fat": 3.3,
        "carbohydrates": 71.1,
        "dietary_fiber": 2,
        "cooking_methods": ["煮", "炖", "炒"],
        "daily_dosage": "10-30g",
        "best_time": "早晚餐",
        "precautions": "孕妇慎用，津液不足者慎用",
        "compatible_foods": ["红豆", "冬瓜", "莲子", "山药"],
        "incompatible_foods": ["海带", "紫菜"],
        "classic_combinations": ["薏米+红豆：利水消肿", "薏米+冬瓜：清热祛湿", "薏米+莲子：健脾祛湿"],
        "image_url": "/images/ingredients/yimi.jpg",
        "description": "薏米是利水渗湿的要药，有健脾止泻的作用。"
    },
    {
        "name": "冬瓜",
        "aliases": ["白瓜", "枕瓜"],
        "category": "蔬菜",
        "nature": "微寒",
        "flavor": "甘、淡",
        "meridians": ["肺", "大肠", "膀胱"],
        "suitable_constitutions": ["phlegm_damp", "damp_heat"],
        "avoid_constitutions": ["yang_deficiency"],
        "efficacy": "清热利水、消肿解毒",
        "nutrition": "含维生素C、钾等",
        "calories": 14,
        "protein": 0.4,
        "fat": 0.1,
        "carbohydrates": 2.7,
        "dietary_fiber": 0.6,
        "cooking_methods": ["煮", "炖", "炒"],
        "daily_dosage": "100-200g",
        "best_time": "午餐",
        "precautions": "脾胃虚寒者少食",
        "compatible_foods": ["薏米", "排骨", "海带", "虾仁"],
        "incompatible_foods": ["鲫鱼", "补酒"],
        "classic_combinations": ["冬瓜+薏米：利水渗湿", "冬瓜+排骨：清热消肿", "冬瓜+海带：化痰利水"],
        "image_url": "/images/ingredients/donggua.jpg",
        "description": "冬瓜是清热利水的佳品，有利尿消肿的作用。"
    },
    {
        "name": "山楂",
        "aliases": ["山里红", "红果"],
        "category": "水果",
        "nature": "微温",
        "flavor": "酸、甘",
        "meridians": ["脾", "胃", "肝"],
        "suitable_constitutions": ["blood_stasis", "qi_depression", "phlegm_damp"],
        "avoid_constitutions": ["qi_deficiency", "yin_deficiency"],
        "efficacy": "消食化积、活血化瘀",
        "nutrition": "含山楂酸、维生素C等",
        "calories": 95,
        "protein": 0.5,
        "fat": 0.6,
        "carbohydrates": 25.1,
        "dietary_fiber": 3.1,
        "cooking_methods": ["煮", "炖", "泡茶", "制酱"],
        "daily_dosage": "10-15g",
        "best_time": "饭后",
        "precautions": "胃酸过多、胃溃疡者慎用",
        "compatible_foods": ["枸杞", "菊花", "麦芽", "神曲"],
        "incompatible_foods": ["海鲜", "黄瓜", "南瓜"],
        "classic_combinations": ["山楂+枸杞：消食化积", "山楂+菊花：疏肝解郁", "山楂+麦芽：健脾消食"],
        "image_url": "/images/ingredients/shanzha.jpg",
        "description": "山楂是消食化积的佳品，有活血化瘀的作用。"
    },
    {
        "name": "生姜",
        "aliases": ["鲜姜", "老姜"],
        "category": "调味品",
        "nature": "温",
        "flavor": "辛",
        "meridians": ["肺", "胃", "脾"],
        "suitable_constitutions": ["yang_deficiency"],
        "avoid_constitutions": ["yin_deficiency", "damp_heat"],
        "efficacy": "温中散寒、温肺止咳",
        "nutrition": "含姜辣素、姜烯等",
        "calories": 46,
        "protein": 1.3,
        "fat": 0.7,
        "carbohydrates": 10.3,
        "cooking_methods": ["煮", "炒", "炖"],
        "daily_dosage": "3-10g",
        "best_time": "早晨",
        "precautions": "阴虚内热、痔疮患者慎用",
        "compatible_foods": ["红糖", "红枣", "羊肉", "葱"],
        "incompatible_foods": ["韭菜", "酒"],
        "classic_combinations": ["生姜+红糖：温中散寒", "生姜+红枣：调和脾胃", "生姜+羊肉：温中补虚"],
        "image_url": "/images/ingredients/shengjiang.jpg",
        "description": "生姜是温中散寒的佳品，有发汗解表的作用。"
    },
    {
        "name": "羊肉",
        "aliases": ["绵羊肉", "山羊肉"],
        "category": "肉类",
        "nature": "温",
        "flavor": "甘",
        "meridians": ["脾", "肾"],
        "suitable_constitutions": ["yang_deficiency", "qi_deficiency"],
        "avoid_constitutions": ["yin_deficiency", "damp_heat"],
        "efficacy": "温中补虚、补肾壮阳",
        "nutrition": "含优质蛋白质、脂肪、维生素B族等",
        "calories": 203,
        "protein": 19.5,
        "fat": 14.3,
        "carbohydrates": 0,
        "cooking_methods": ["炖", "煮", "烤"],
        "daily_dosage": "50-100g",
        "best_time": "冬季",
        "precautions": "发热、牙痛、口舌生疮者慎用",
        "compatible_foods": ["当归", "生姜", "萝卜", "枸杞"],
        "incompatible_foods": ["醋", "西瓜", "茶"],
        "classic_combinations": ["羊肉+当归：温补气血", "羊肉+生姜：温中散寒", "羊肉+萝卜：补虚消食"],
        "image_url": "/images/ingredients/yangrou.jpg",
        "description": "羊肉是温补佳品，有温中补虚、补肾壮阳的作用。"
    }
]


def seed_questions(db: Session):
    """种子题目数据"""
    print("[*] Seeding questions...")

    # Check if questions already exist
    existing_count = db.query(Question).count()
    if existing_count >= 30:
        print(f"   [OK] Questions already exist ({existing_count} found)")
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
    print(f"   [OK] Seeded {len(QUESTIONS_DATA)} questions")


def seed_foods(db: Session):
    """种子食物数据"""
    print("[+] Seeding foods...")

    # Check if foods already exist
    existing_count = db.query(Food).count()
    if existing_count >= len(FOODS_DATA):
        print(f"   [OK] Foods already exist ({existing_count} found)")
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
    print(f"   [OK] Seeded {len(FOODS_DATA)} foods")


def seed_ingredients(db: Session):
    """种子食材数据"""
    print("[+] Seeding ingredients...")

    # Check if ingredients already exist
    existing_count = db.query(Ingredient).count()
    if existing_count >= len(INGREDIENTS_DATA):
        print(f"   [OK] Ingredients already exist ({existing_count} found)")
        return

    for i_data in INGREDIENTS_DATA:
        # Check duplicate by name
        exists = db.query(Ingredient).filter(Ingredient.name == i_data["name"]).first()
        if exists:
            continue

        ingredient = Ingredient(
            name=i_data["name"],
            aliases=i_data.get("aliases"),
            category=i_data.get("category"),
            nature=i_data.get("nature"),
            flavor=i_data.get("flavor"),
            meridians=i_data.get("meridians"),
            suitable_constitutions=i_data.get("suitable_constitutions"),
            avoid_constitutions=i_data.get("avoid_constitutions"),
            efficacy=i_data.get("efficacy"),
            nutrition=i_data.get("nutrition"),
            calories=i_data.get("calories", 0),
            protein=i_data.get("protein", 0),
            fat=i_data.get("fat", 0),
            carbohydrates=i_data.get("carbohydrates", 0),
            dietary_fiber=i_data.get("dietary_fiber", 0),
            cooking_methods=i_data.get("cooking_methods"),
            daily_dosage=i_data.get("daily_dosage"),
            best_time=i_data.get("best_time"),
            precautions=i_data.get("precautions"),
            image_url=i_data.get("image_url"),
            description=i_data.get("description")
        )
        db.add(ingredient)

    db.commit()
    print(f"   [OK] Seeded {len(INGREDIENTS_DATA)} ingredients")


def seed_recipes(db: Session):
    """种子食谱数据"""
    print("[+] Seeding recipes...")

    # Sample recipes for each constitution
    recipes_data = [
        {
            "name": "黄芪炖鸡",
            "type": "汤类",
            "difficulty": "简单",
            "cook_time": 120,
            "servings": 4,
            "suitable_constitutions": ["qi_deficiency"],
            "symptoms": ["疲劳乏力", "食欲不振"],
            "suitable_seasons": ["秋", "冬"],
            "ingredients": {
                "main": [{"name": "鸡肉", "amount": "500g"}],
                "auxiliary": [{"name": "黄芪", "amount": "30g"}],
                "seasoning": [{"name": "生姜", "amount": "3片"}]
            },
            "steps": [
                "鸡肉切块焯水",
                "黄芪洗净备用",
                "所有材料放入砂锅",
                "加水炖煮2小时"
            ],
            "efficacy": "补气养血、健脾益肺",
            "health_benefits": "增强体质、改善疲劳",
            "precautions": "感冒发热时不宜食用",
            "tags": ["补气", "健脾", "增强免疫"],
            "meal_type": "晚餐",
            "image_url": "/images/recipes/huangqi_dunji.jpg",
            "description": "补气养血，适合气虚体质"
        },
        {
            "name": "当归生姜羊肉汤",
            "type": "汤类",
            "difficulty": "简单",
            "cook_time": 120,
            "servings": 4,
            "suitable_constitutions": ["yang_deficiency"],
            "symptoms": ["畏寒肢冷", "腰膝酸软"],
            "suitable_seasons": ["冬"],
            "ingredients": {
                "main": [{"name": "羊肉", "amount": "500g"}],
                "auxiliary": [{"name": "当归", "amount": "15g"}],
                "seasoning": [{"name": "生姜", "amount": "30g"}]
            },
            "steps": [
                "羊肉切块焯水",
                "当归、生姜洗净",
                "所有材料放入砂锅",
                "加水炖煮2小时"
            ],
            "efficacy": "温阳散寒、补血活血",
            "health_benefits": "温暖身体、改善循环",
            "precautions": "阴虚火旺者慎用",
            "tags": ["温阳", "散寒", "补血"],
            "meal_type": "晚餐",
            "image_url": "/images/recipes/danggui_yangrou.jpg",
            "description": "温阳散寒，适合阳虚体质"
        },
        {
            "name": "百合银耳汤",
            "type": "汤类",
            "difficulty": "简单",
            "cook_time": 60,
            "servings": 2,
            "suitable_constitutions": ["yin_deficiency"],
            "symptoms": ["口干咽燥", "干咳少痰"],
            "suitable_seasons": ["秋", "冬"],
            "ingredients": {
                "main": [{"name": "百合", "amount": "30g"}],
                "auxiliary": [{"name": "银耳", "amount": "15g"}],
                "seasoning": [{"name": "冰糖", "amount": "适量"}]
            },
            "steps": [
                "银耳泡发撕成小朵",
                "百合洗净",
                "放入锅中加适量水",
                "小火炖煮1小时，加冰糖调味即可"
            ],
            "efficacy": "滋阴润燥、清心安神",
            "health_benefits": "润肺止咳、改善睡眠",
            "precautions": "风寒咳嗽者慎用",
            "tags": ["滋阴", "润肺", "安神"],
            "meal_type": "晚餐",
            "image_url": "/images/recipes/baihe_yiner.jpg",
            "description": "滋阴润燥，适合阴虚体质"
        },
        {
            "name": "冬瓜薏米汤",
            "type": "汤类",
            "difficulty": "简单",
            "cook_time": 60,
            "servings": 3,
            "suitable_constitutions": ["phlegm_damp", "damp_heat"],
            "symptoms": ["肢体困重", "食欲不振"],
            "suitable_seasons": ["夏"],
            "ingredients": {
                "main": [{"name": "冬瓜", "amount": "300g"}],
                "auxiliary": [{"name": "薏米", "amount": "50g"}],
                "seasoning": [{"name": "生姜", "amount": "2片"}]
            },
            "steps": [
                "冬瓜去皮切块",
                "薏米提前浸泡",
                "所有材料放入锅中",
                "加水煮1小时"
            ],
            "efficacy": "利水渗湿、清热解毒",
            "health_benefits": "利尿消肿、帮助消化",
            "precautions": "脾胃虚寒者少食",
            "tags": ["祛湿", "利尿", "清热"],
            "meal_type": "午餐",
            "image_url": "/images/recipes/donggua_yimi.jpg",
            "description": "利水渗湿，适合痰湿质和湿热质"
        },
        {
            "name": "山楂玫瑰花茶",
            "type": "茶饮",
            "difficulty": "简单",
            "cook_time": 10,
            "servings": 1,
            "suitable_constitutions": ["blood_stasis", "qi_depression"],
            "symptoms": ["胸闷不舒", "情绪抑郁"],
            "suitable_seasons": ["春"],
            "ingredients": {
                "main": [{"name": "山楂", "amount": "10g"}],
                "auxiliary": [{"name": "玫瑰花", "amount": "5g"}],
                "seasoning": [{"name": "冰糖", "amount": "适量"}]
            },
            "steps": [
                "山楂、玫瑰花洗净",
                "用开水冲泡",
                "焖10分钟即可饮用"
            ],
            "efficacy": "活血化瘀、疏肝解郁",
            "health_benefits": "改善情绪、促进血液循环",
            "precautions": "胃酸过多者慎用",
            "tags": ["活血", "解郁", "疏肝"],
            "meal_type": "加餐",
            "image_url": "/images/recipes/shanzha_meigui.jpg",
            "description": "活血化瘀，疏肝解郁"
        }
    ]

    # Check if recipes already exist
    existing_count = db.query(Recipe).count()
    if existing_count >= len(recipes_data):
        print(f"   [OK] Recipes already exist ({existing_count} found)")
        return

    for r_data in recipes_data:
        recipe = Recipe(
            name=r_data["name"],
            type=r_data.get("type"),
            difficulty=r_data.get("difficulty"),
            cook_time=r_data.get("cook_time"),
            servings=r_data.get("servings"),
            suitable_constitutions=r_data.get("suitable_constitutions"),
            symptoms=r_data.get("symptoms"),
            suitable_seasons=r_data.get("suitable_seasons"),
            ingredients=r_data.get("ingredients"),
            steps=r_data.get("steps"),
            efficacy=r_data.get("efficacy"),
            health_benefits=r_data.get("health_benefits"),
            precautions=r_data.get("precautions"),
            tags=r_data.get("tags"),
            meal_type=r_data.get("meal_type"),
            image_url=r_data.get("image_url"),
            description=r_data.get("description")
        )
        db.add(recipe)

    db.commit()
    print(f"   [OK] Seeded {len(recipes_data)} recipes")


def seed_constitution_info(db: Session):
    """种子体质信息数据"""
    print("[+] Seeding constitution info...")

    # Check if constitution info already exists
    existing_count = db.query(ConstitutionInfo).count()
    if existing_count >= 9:
        print(f"   [OK] Constitution info already exists ({existing_count} found)")
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
    print(f"   [OK] Seeded {len(CONSTITUTION_INFO_DATA)} constitution types")


def seed_acupoints(db: Session):
    """种子穴位数据"""
    print("[+] Seeding acupoints...")

    # Always try to seed/update acupoints as we expanded the dataset
    # existing_count = db.query(Acupoint).count()
    # if existing_count >= len(ACUPOINTS_DATA):
    #     print(f"   [OK] Acupoints already exist ({existing_count} found)")
    #     return

    count_new = 0
    count_updated = 0

    for a_data in ACUPOINTS_DATA:
        # Check duplicate by name or code
        # Using name as primary key for check as in original script
        exists = db.query(Acupoint).filter(Acupoint.name == a_data["name"]).first()
        
        if exists:
            # Update existing record
            exists.code = a_data["code"]
            exists.meridian = a_data["meridian"]
            exists.body_part = a_data["body_part"]
            exists.location = a_data["location"]
            exists.simple_location = a_data["simple_location"]
            exists.efficacy = a_data["efficacy"]
            exists.indications = a_data["indications"]
            exists.massage_method = a_data["massage_method"]
            exists.image_url = a_data["image_url"]
            exists.anatomical_image_url = a_data.get("anatomical_image_url")
            exists.model_3d_url = a_data.get("model_3d_url")
            count_updated += 1
        else:
            # Create new record
            acupoint = Acupoint(
                name=a_data["name"],
                code=a_data["code"],
                meridian=a_data["meridian"],
                body_part=a_data["body_part"],
                location=a_data["location"],
                simple_location=a_data["simple_location"],
                efficacy=a_data["efficacy"],
                indications=a_data["indications"],
                massage_method=a_data["massage_method"],
                image_url=a_data["image_url"],
                anatomical_image_url=a_data.get("anatomical_image_url"),
                model_3d_url=a_data.get("model_3d_url")
            )
            db.add(acupoint)
            count_new += 1

    db.commit()
    print(f"   [OK] Processed {len(ACUPOINTS_DATA)} acupoints (New: {count_new}, Updated: {count_updated})")


def main():
    """主函数"""
    print("=" * 50)
    print("[+] Database Seeding")
    print("=" * 50)
    print(f"Database: {settings.DATABASE_URL[:30]}...")
    print()

    # Create all tables
    print("[+] Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("   [OK] Tables created")
    print()

    # Get database session
    db = SessionLocal()

    try:
        # Seed all data
        seed_questions(db)
        seed_foods(db)
        seed_ingredients(db)
        seed_recipes(db)
        seed_constitution_info(db)
        seed_acupoints(db)

        print()
        print("=" * 50)
        print("[OK] Database seeding completed successfully!")
        print("=" * 50)

    except Exception as e:
        print()
        print("=" * 50)
        print(f"[ERROR] Error during seeding: {e}")
        print("=" * 50)
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
