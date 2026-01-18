"""
Pytest configuration and fixtures
"""

import pytest
import sys
import os

# Add backend directory to path - handle both direct and subdirectory runs
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Test database (SQLite)
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """创建测试数据库会话"""
    from api.database import Base
    # Import all models to ensure tables are created
    from api.models import (
        User, ConstitutionResult, Question, Food, Recipe,
        Ingredient, ConstitutionInfo, Acupoint, SymptomAcupoint,
        TongueDiagnosisRecord, Course
    )

    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Clean up
        session.rollback()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """创建测试客户端"""
    from api.database import get_db, get_db_optional
    from main import app

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    def override_get_db_optional():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_db_optional] = override_get_db_optional
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_ingredient_data():
    """测试食材数据"""
    return {
        "id": "test-ingredient-001",
        "name": "山药",
        "aliases": ["怀山药", "淮山"],
        "category": "蔬菜",
        "nature": "平",
        "flavor": "甘",
        "meridians": ["脾", "肺", "肾"],
        "suitable_constitutions": ["qi_deficiency", "yin_deficiency"],
        "avoid_constitutions": ["phlegm_damp"],
        "efficacy": "健脾养胃、补肺益肾",
        "cooking_methods": ["蒸", "煮", "炖"],
        "daily_dosage": "50-100g",
        "best_time": "早晚餐",
        "compatible_with": ["莲子", "枸杞"],
        "incompatible_with": ["碱性食物"],
        "image_url": "https://example.com/yam.jpg",
        "description": "山药是常见的药食同源食材"
    }


@pytest.fixture
def test_recipe_data():
    """测试食谱数据"""
    return {
        "id": "test-recipe-001",
        "name": "山药莲子粥",
        "type": "粥类",
        "difficulty": "简单",
        "cook_time": 30,
        "servings": 2,
        "suitable_constitutions": ["qi_deficiency"],
        "symptoms": ["食欲不振", "疲劳乏力"],
        "suitable_seasons": ["春", "秋", "冬"],
        "ingredients": {
            "main": [
                {"name": "山药", "amount": "100g"},
                {"name": "糯米", "amount": "50g"}
            ],
            "auxiliary": [
                {"name": "莲子", "amount": "20g"},
                {"name": "枸杞", "amount": "10g"}
            ],
            "seasoning": [
                {"name": "冰糖", "amount": "适量"}
            ]
        },
        "steps": [
            "山药去皮切小块，糯米提前浸泡2小时",
            "锅中加水，放入糯米大火煮开",
            "加入山药、莲子转小火煮30分钟",
            "最后加入枸杞、冰糖煮5分钟即可"
        ],
        "efficacy": "健脾养胃、补肺益气",
        "health_benefits": "适合脾胃虚弱、食欲不振者",
        "precautions": "糖尿病患者慎用",
        "tags": ["健脾养胃", "补气"],
        "image_url": "https://example.com/congee.jpg",
        "description": "经典健脾养胃粥"
    }


@pytest.fixture
def test_acupoint_data():
    """测试穴位数据"""
    return {
        "id": "test-acupoint-001",
        "name": "足三里",
        "code": "ST36",
        "meridian": "足阳明胃经",
        "body_part": "下肢",
        "location": "犊鼻下3寸，胫骨前缘外一横指",
        "simple_location": "膝盖骨外侧下方凹陷往下四横指",
        "efficacy": ["健脾和胃", "扶正培元", "调理气血"],
        "indications": ["胃痛", "消化不良", "失眠", "疲劳"],
        "massage_method": "用拇指指腹按压",
        "massage_duration": "3-5分钟",
        "massage_frequency": "每日1-2次",
        "precautions": "孕妇慎用",
        "suitable_constitutions": ["qi_deficiency", "yang_deficiency", "phlegm_damp"],
        "constitution_benefit": "健脾和胃，增强体质",
        "image_url": "https://example.com/zusanli.jpg"
    }


@pytest.fixture
def test_course_data():
    """测试课程数据"""
    return {
        "id": "test-course-001",
        "title": "气虚质怎么调理？",
        "description": "详细介绍气虚质的成因、表现和调理方法",
        "category": "constitution",
        "subcategory": "qi_deficiency",
        "content_type": "video",
        "content_url": "https://example.com/video.mp4",
        "suitable_constitutions": ["qi_deficiency"],
        "tags": ["气虚质", "健脾", "养生"],
        "duration": 120,
        "cover_image": "https://example.com/cover.jpg",
        "author": "张医师",
        "author_title": "中医执业医师"
    }
