# 第一期开发测试文档

> **项目名称：** 中医养生平台（第一期）
> **版本：** v1.0
> **创建时间：** 2026-01-18
> **参考文档：** phase1_development_plan_v2.md

---

## 一、测试概述

### 1.1 测试范围

| 模块 | 测试类型 | 优先级 |
|-----|---------|-------|
| 食材库 + 食谱库 | 单元测试 + API测试 + 前端测试 | P0 |
| 穴位查找 | 单元测试 + API测试 + 前端测试 | P0 |
| AI舌诊 | 单元测试 + API测试 + 前端测试 | P0 |
| 养生课程 | 单元测试 + API测试 + 前端测试 | P1 |
| 体质系统（已有） | 回归测试 | P0 |

### 1.2 测试环境

```yaml
开发环境:
  - 操作系统: Windows/Mac/Linux
  - Python: 3.11+
  - Node.js: 18+
  - 数据库: SQLite (开发) / PostgreSQL (生产)

测试环境:
  - 后端测试: pytest + pytest-cov
  - 前端测试: vitest + @vue/test-utils
  - API测试: pytest + httpx
  - E2E测试: Playwright (可选)
```

---

## 二、后端单元测试

### 2.1 测试框架配置

#### 2.1.1 pytest配置

```ini
# backend/pytest.ini

[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --verbose
    --strict-markers
    --cov=api
    --cov-report=html
    --cov-report=term-missing
    --tb=short

markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
```

#### 2.1.2 测试目录结构

```
backend/tests/
├── __init__.py
├── conftest.py                 # pytest配置和fixtures
├── test_unit/                  # 单元测试
│   ├── __init__.py
│   ├── test_ingredients.py     # 食材服务测试
│   ├── test_recipes.py         # 食谱服务测试
│   ├── test_acupoints.py       # 穴位服务测试
│   ├── test_tongue_diagnosis.py # 舌诊服务测试
│   └── test_courses.py         # 课程服务测试
├── test_api/                   # API测试
│   ├── __init__.py
│   ├── test_ingredients_api.py
│   ├── test_recipes_api.py
│   ├── test_acupoints_api.py
│   ├── test_tongue_diagnosis_api.py
│   └── test_courses_api.py
└── test_integration/           # 集成测试
    ├── __init__.py
    └── test_constitution_integration.py
```

### 2.2 测试Fixtures (conftest.py)

```python
# backend/tests/conftest.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database import Base, get_db
from api.main import app
from fastapi.testclient import TestClient

# 测试数据库（使用SQLite）
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """创建测试数据库会话"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """创建测试客户端"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
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
        "compatible_with": ["莲子", "枸杞"],
        "incompatible_with": ["碱性食物"]
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
            ]
        },
        "steps": [
            "山药去皮切小块，糯米提前浸泡2小时",
            "锅中加水，放入糯米大火煮开",
            "加入山药、莲子转小火煮30分钟",
            "最后加入枸杞、冰糖煮5分钟即可"
        ],
        "efficacy": "健脾养胃、补肺益气"
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
        "suitable_constitutions": ["qi_deficiency", "yang_deficiency", "phlegm_damp"]
    }
```

### 2.3 食材服务测试

```python
# backend/tests/test_unit/test_ingredients.py

import pytest
from api.services.ingredient_service import IngredientService
from api.models import Ingredient


class TestIngredientService:
    """食材服务单元测试"""

    def test_get_ingredient_by_id(self, db_session, test_ingredient_data):
        """测试根据ID获取食材"""
        # 创建测试数据
        ingredient = Ingredient(**test_ingredient_data)
        db_session.add(ingredient)
        db_session.commit()

        # 测试
        service = IngredientService()
        result = service.get_ingredient_by_id("test-ingredient-001", db_session)

        assert result is not None
        assert result.name == "山药"
        assert result.nature == "平"
        assert "qi_deficiency" in result.suitable_constitutions

    def test_get_ingredients_by_constitution(self, db_session):
        """测试根据体质获取食材"""
        # 创建多个测试食材
        ingredients = [
            Ingredient(
                id=f"test-{i:03d}",
                name=f"食材{i}",
                category="蔬菜",
                suitable_constitutions=["qi_deficiency"] if i % 2 == 0 else ["yin_deficiency"]
            )
            for i in range(1, 11)
        ]
        db_session.add_all(ingredients)
        db_session.commit()

        # 测试获取气虚质食材
        service = IngredientService()
        result = service.get_ingredients_by_constitution("qi_deficiency", db_session)

        assert len(result) == 5
        assert all("qi_deficiency" in item.suitable_constitutions for item in result)

    def test_get_recommended_ingredients(self, db_session):
        """测试获取推荐食材（包含推荐和禁忌）"""
        # 创建测试数据
        ingredients = [
            Ingredient(
                id="rec-001",
                name="山药",
                suitable_constitutions=["qi_deficiency"]
            ),
            Ingredient(
                id="avo-001",
                name="山楂",
                avoid_constitutions=["qi_deficiency"]
            )
        ]
        db_session.add_all(ingredients)
        db_session.commit()

        # 测试
        service = IngredientService()
        result = service.get_recommended_ingredients("qi_deficiency", db_session)

        assert "recommended" in result
        assert "avoided" in result
        assert len(result["recommended"]) > 0
        assert any(item.name == "山药" for item in result["recommended"])

    def test_search_ingredients_by_keyword(self, db_session):
        """测试关键词搜索"""
        ingredients = [
            Ingredient(
                id="search-001",
                name="山药",
                aliases=["怀山药", "淮山"],
                efficacy="健脾养胃"
            ),
            Ingredient(
                id="search-002",
                name="红枣",
                efficacy="补血安神"
            )
        ]
        db_session.add_all(ingredients)
        db_session.commit()

        service = IngredientService()

        # 搜索名称
        result = service.search_ingredients("山药", db_session)
        assert len(result) > 0

        # 搜索别名
        result = service.search_ingredients("淮山", db_session)
        assert len(result) > 0

        # 搜索功效
        result = service.search_ingredients("健脾", db_session)
        assert len(result) > 0

    def test_get_ingredients_by_category(self, db_session):
        """测试按分类获取"""
        categories = ["谷物", "蔬菜", "水果"]
        for i, cat in enumerate(categories):
            ingredient = Ingredient(
                id=f"cat-{i:03d}",
                name=f"{cat}测试",
                category=cat
            )
            db_session.add(ingredient)
        db_session.commit()

        service = IngredientService()
        result = service.get_ingredients_by_category("蔬菜", db_session)

        assert all(item.category == "蔬菜" for item in result)

    def test_ingredient_constitution_validation(self):
        """测试体质代码验证"""
        service = IngredientService()

        # 有效体质代码
        valid_constitutions = ["peace", "qi_deficiency", "yang_deficiency",
                              "yin_deficiency", "phlegm_damp", "damp_heat",
                              "blood_stasis", "qi_depression", "special"]

        for constitution in valid_constitutions:
            assert service.is_valid_constitution(constitution)

        # 无效体质代码
        invalid_constitutions = ["invalid", "wrong_code", ""]
        for constitution in invalid_constitutions:
            assert not service.is_valid_constitution(constitution)
```

### 2.4 食谱服务测试

```python
# backend/tests/test_unit/test_recipes.py

import pytest
from api.services.recipe_service import RecipeService
from api.models import Recipe


class TestRecipeService:
    """食谱服务单元测试"""

    def test_get_recipe_by_id(self, db_session, test_recipe_data):
        """测试根据ID获取食谱"""
        recipe = Recipe(**test_recipe_data)
        db_session.add(recipe)
        db_session.commit()

        service = RecipeService()
        result = service.get_recipe_by_id("test-recipe-001", db_session)

        assert result is not None
        assert result.name == "山药莲子粥"
        assert result.type == "粥类"
        assert result.difficulty == "简单"

    def test_get_recipes_by_constitution(self, db_session):
        """测试根据体质获取食谱"""
        recipes = [
            Recipe(
                id=f"recipe-{i:03d}",
                name=f"食谱{i}",
                type="粥类",
                suitable_constitutions=["qi_deficiency"] if i % 2 == 0 else ["yin_deficiency"]
            )
            for i in range(1, 11)
        ]
        db_session.add_all(recipes)
        db_session.commit()

        service = RecipeService()
        result = service.get_recipes_by_constitution("qi_deficiency", db_session)

        assert len(result) == 5

    def test_get_recipes_by_meal_type(self, db_session):
        """测试根据餐次获取食谱"""
        recipes = [
            Recipe(
                id=f"meal-{i:03d}",
                name=f"食谱{i}",
                type="粥类",
                suitable_constitutions=["qi_deficiency"],
                meal_type=["breakfast"] if i % 3 == 0 else
                          ["lunch"] if i % 3 == 1 else
                          ["dinner"]
            )
            for i in range(1, 10)
        ]
        db_session.add_all(recipes)
        db_session.commit()

        service = RecipeService()
        result = service.get_recipes_by_meal_type("qi_deficiency", "breakfast", db_session)

        assert all(recipe.meal_type == ["breakfast"] for recipe in result)

    def test_search_recipes_by_ingredient(self, db_session):
        """测试根据食材搜索食谱"""
        recipe = Recipe(
            id="ing-search-001",
            name="山药粥",
            type="粥类",
            ingredients={
                "main": [{"name": "山药", "amount": "100g"}],
                "auxiliary": [],
                "seasoning": []
            }
        )
        db_session.add(recipe)
        db_session.commit()

        service = RecipeService()
        result = service.search_recipes_by_ingredient("山药", db_session)

        assert len(result) > 0
        assert any("山药" in r.name for r in result)

    def test_get_recipe_nutrition_info(self, db_session, test_recipe_data):
        """测试获取食谱营养信息"""
        recipe = Recipe(**test_recipe_data)
        db_session.add(recipe)
        db_session.commit()

        service = RecipeService()
        nutrition = service.calculate_nutrition("test-recipe-001", db_session)

        assert "calories" in nutrition
        assert "protein" in nutrition
        assert "carbs" in nutrition

    def test_increment_view_count(self, db_session, test_recipe_data):
        """测试增加浏览次数"""
        recipe = Recipe(**test_recipe_data)
        recipe.view_count = 10
        db_session.add(recipe)
        db_session.commit()

        service = RecipeService()
        service.increment_view_count("test-recipe-001", db_session)

        db_session.refresh(recipe)
        assert recipe.view_count == 11
```

### 2.5 穴位服务测试

```python
# backend/tests/test_unit/test_acupoints.py

import pytest
from api.services.acupoint_service import AcupointService
from api.models import Acupoint, SymptomAcupoint


class TestAcupointService:
    """穴位服务单元测试"""

    def test_get_acupoint_by_id(self, db_session, test_acupoint_data):
        """测试根据ID获取穴位"""
        acupoint = Acupoint(**test_acupoint_data)
        db_session.add(acupoint)
        db_session.commit()

        service = AcupointService()
        result = service.get_acupoint_by_id("test-acupoint-001", db_session)

        assert result is not None
        assert result.name == "足三里"
        assert result.code == "ST36"

    def test_get_acupoints_by_body_part(self, db_session):
        """测试按部位获取穴位"""
        acupoints = [
            Acupoint(
                id=f"acupoint-{i:03d}",
                name=f"穴位{i}",
                body_part="下肢" if i % 2 == 0 else "上肢"
            )
            for i in range(1, 11)
        ]
        db_session.add_all(acupoints)
        db_session.commit()

        service = AcupointService()
        result = service.get_acupoints_by_body_part("下肢", db_session)

        assert all(item.body_part == "下肢" for item in result)

    def test_get_acupoints_by_meridian(self, db_session):
        """测试按经络获取穴位"""
        meridians = ["足阳明胃经", "足太阴脾经", "手阳明大肠经"]
        for i, meridian in enumerate(meridians):
            acupoint = Acupoint(
                id=f"meridian-{i:03d}",
                name=f"穴位{i}",
                meridian=meridian
            )
            db_session.add(acupoint)
        db_session.commit()

        service = AcupointService()
        result = service.get_acupoints_by_meridian("足阳明胃经", db_session)

        assert all(item.meridian == "足阳明胃经" for item in result)

    def test_get_acupoints_by_constitution(self, db_session):
        """测试根据体质获取推荐穴位"""
        acupoints = [
            Acupoint(
                id=f"constitution-acu-{i:03d}",
                name=f"穴位{i}",
                suitable_constitutions=["qi_deficiency"] if i % 2 == 0 else ["yin_deficiency"]
            )
            for i in range(1, 11)
        ]
        db_session.add_all(acupoints)
        db_session.commit()

        service = AcupointService()
        result = service.get_acupoints_by_constitution("qi_deficiency", db_session)

        assert len(result) == 5

    def test_get_acupoints_by_symptom(self, db_session):
        """测试根据症状获取穴位"""
        # 创建穴位
        acupoint1 = Acupoint(
            id="symptom-acu-001",
            name="足三里",
            efficacy=["健脾和胃"]
        )
        acupoint2 = Acupoint(
            id="symptom-acu-002",
            name="内关",
            efficacy=["宁心安神"]
        )
        db_session.add_all([acupoint1, acupoint2])

        # 创建症状-穴位映射
        mapping1 = SymptomAcupoint(
            id="mapping-001",
            symptom_name="胃痛",
            acupoint_id="symptom-acu-001",
            priority=1
        )
        mapping2 = SymptomAcupoint(
            id="mapping-002",
            symptom_name="胃痛",
            acupoint_id="symptom-acu-002",
            priority=2
        )
        db_session.add_all([mapping1, mapping2])
        db_session.commit()

        service = AcupointService()
        result = service.get_acupoints_by_symptom("胃痛", db_session)

        assert len(result) == 2
        # 验证按priority排序
        assert result[0]["name"] == "足三里"

    def test_search_acupoints(self, db_session):
        """测试穴位搜索"""
        acupoints = [
            Acupoint(
                id="search-acu-001",
                name="足三里",
                code="ST36",
                efficacy=["健脾和胃", "扶正培元"]
            ),
            Acupoint(
                id="search-acu-002",
                name="三阴交",
                code="SP6",
                efficacy=["调理气血"]
            )
        ]
        db_session.add_all(acupoints)
        db_session.commit()

        service = AcupointService()

        # 搜索名称
        result = service.search_acupoints("足三里", db_session)
        assert len(result) > 0

        # 搜索代码
        result = service.search_acupoints("ST36", db_session)
        assert len(result) > 0

        # 搜索功效
        result = service.search_acupoints("健脾", db_session)
        assert len(result) > 0
```

### 2.6 舌诊服务测试

```python
# backend/tests/test_unit/test_tongue_diagnosis.py

import pytest
from api.services.tongue_diagnosis_service import TongueDiagnosisService


class TestTongueDiagnosisService:
    """舌诊服务单元测试"""

    def test_analyze_by_rules_qi_deficiency(self):
        """测试气虚质规则匹配"""
        service = TongueDiagnosisService()

        # 气虚质舌象特征
        tongue_features = {
            "tongue_color": "淡白",
            "tongue_shape": "胖大",
            "coating_color": "白",
            "coating_thickness": "薄"
        }

        result = service.analyze_by_rules(tongue_features)

        assert result["constitution_tendency"] == "qi_deficiency"
        assert result["constitution_name"] == "气虚质"

    def test_analyze_by_rules_yin_deficiency(self):
        """测试阴虚质规则匹配"""
        service = TongueDiagnosisService()

        tongue_features = {
            "tongue_color": "红",
            "tongue_shape": "瘦薄",
            "coating_color": "少",
            "coating_thickness": "薄"
        }

        result = service.analyze_by_rules(tongue_features)

        assert result["constitution_tendency"] == "yin_deficiency"

    def test_compare_with_test_result(self):
        """测试与测试结果对比"""
        service = TongueDiagnosisService()

        # 一致的情况
        comparison = service.compare_with_test_result(
            tongue_constitution="qi_deficiency",
            test_constitution="qi_deficiency"
        )

        assert comparison["is_consistent"] is True

        # 不一致的情况
        comparison = service.compare_with_test_result(
            tongue_constitution="qi_deficiency",
            test_constitution="yin_deficiency"
        )

        assert comparison["is_consistent"] is False

    def test_generate_recommendations(self):
        """测试生成推荐内容"""
        service = TongueDiagnosisService()

        recommendations = service.generate_recommendations("qi_deficiency")

        assert "diet" in recommendations
        assert "lifestyle" in recommendations
        assert "acupoints" in recommendations
        assert "recipes" in recommendations

        # 验证推荐内容符合气虚质调理原则
        assert any("山药" in item.get("name", "") for item in recommendations.get("recipes", []))
        assert any("足三里" in item.get("name", "") for item in recommendations.get("acupoints", []))

    def test_invalid_tongue_features(self):
        """测试无效舌象特征"""
        service = TongueDiagnosisService()

        # 缺少必要字段
        invalid_features = {
            "tongue_color": "淡白"
            # 缺少其他字段
        }

        with pytest.raises(ValueError):
            service.analyze_by_rules(invalid_features)

    def test_get_diagnosis_history(self, db_session):
        """测试获取舌诊历史"""
        from api.models import TongueDiagnosisRecord

        records = [
            TongueDiagnosisRecord(
                id=f"record-{i:03d}",
                image_url=f"https://example.com/image{i}.jpg",
                constitution_tendency="qi_deficiency" if i % 2 == 0 else "yin_deficiency"
            )
            for i in range(1, 6)
        ]
        db_session.add_all(records)
        db_session.commit()

        service = TongueDiagnosisService()
        history = service.get_diagnosis_history("test-user-id", db_session)

        assert len(history) == 5
```

### 2.7 课程服务测试

```python
# backend/tests/test_unit/test_courses.py

import pytest
from api.services.course_service import CourseService
from api.models import Course


class TestCourseService:
    """课程服务单元测试"""

    def test_get_course_by_id(self, db_session):
        """测试根据ID获取课程"""
        course = Course(
            id="test-course-001",
            title="气虚质怎么调理？",
            category="constitution",
            subcategory="qi_deficiency",
            content_type="video",
            content_url="https://example.com/video.mp4",
            suitable_constitutions=["qi_deficiency"],
            duration=120,
            cover_image="https://example.com/cover.jpg"
        )
        db_session.add(course)
        db_session.commit()

        service = CourseService()
        result = service.get_course_by_id("test-course-001", db_session)

        assert result is not None
        assert result.title == "气虚质怎么调理？"

    def test_get_courses_by_constitution(self, db_session):
        """测试根据体质获取课程"""
        courses = [
            Course(
                id=f"course-{i:03d}",
                title=f"课程{i}",
                category="constitution",
                suitable_constitutions=["qi_deficiency"] if i % 2 == 0 else ["yin_deficiency"]
            )
            for i in range(1, 11)
        ]
        db_session.add_all(courses)
        db_session.commit()

        service = CourseService()
        result = service.get_courses_by_constitution("qi_deficiency", db_session)

        assert len(result) == 5

    def test_get_courses_by_category(self, db_session):
        """测试按分类获取课程"""
        courses = [
            Course(
                id=f"cat-course-{i:03d}",
                title=f"课程{i}",
                category="constitution" if i % 2 == 0 else "season"
            )
            for i in range(1, 11)
        ]
        db_session.add_all(courses)
        db_session.commit()

        service = CourseService()
        result = service.get_courses_by_category("constitution", db_session)

        assert all(item.category == "constitution" for item in result)

    def test_search_courses(self, db_session):
        """测试搜索课程"""
        course = Course(
            id="search-course-001",
            title="气虚质养生方法",
            description="详细介绍气虚质的调理方法",
            tags=["气虚质", "健脾"]
        )
        db_session.add(course)
        db_session.commit()

        service = CourseService()

        # 搜索标题
        result = service.search_courses("气虚质", db_session)
        assert len(result) > 0

        # 搜索标签
        result = service.search_courses("健脾", db_session)
        assert len(result) > 0

    def test_increment_view_count(self, db_session):
        """测试增加观看次数"""
        course = Course(
            id="view-course-001",
            title="测试课程",
            view_count=100
        )
        db_session.add(course)
        db_session.commit()

        service = CourseService()
        service.increment_view_count("view-course-001", db_session)

        db_session.refresh(course)
        assert course.view_count == 101
```

---

## 三、API集成测试

### 3.1 食材API测试

```python
# backend/tests/test_api/test_ingredients_api.py

import pytest
from fastapi.testclient import TestClient


class TestIngredientsAPI:
    """食材API集成测试"""

    def test_get_ingredients_list(self, client: TestClient, db_session):
        """测试获取食材列表"""
        # 准备测试数据
        from api.models import Ingredient
        ingredients = [
            Ingredient(
                id=f"api-test-{i:03d}",
                name=f"食材{i}",
                category="蔬菜"
            )
            for i in range(1, 11)
        ]
        db_session.add_all(ingredients)
        db_session.commit()

        # 测试API
        response = client.get("/api/v1/ingredients")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "data" in data
        assert data["data"]["total"] == 10
        assert len(data["data"]["items"]) == 10

    def test_get_ingredient_detail(self, client: TestClient, db_session):
        """测试获取食材详情"""
        from api.models import Ingredient
        ingredient = Ingredient(
            id="api-detail-001",
            name="山药",
            nature="平",
            flavor="甘",
            suitable_constitutions=["qi_deficiency"]
        )
        db_session.add(ingredient)
        db_session.commit()

        response = client.get("/api/v1/ingredients/api-detail-001")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["name"] == "山药"
        assert data["data"]["nature"] == "平"

    def test_get_ingredients_by_constitution(self, client: TestClient, db_session):
        """测试按体质获取食材"""
        from api.models import Ingredient
        ingredients = [
            Ingredient(
                id=f"api-constitution-{i:03d}",
                name=f"食材{i}",
                suitable_constitutions=["qi_deficiency"] if i % 2 == 0 else []
            )
            for i in range(1, 11)
        ]
        db_session.add_all(ingredients)
        db_session.commit()

        response = client.get("/api/v1/ingredients/recommend/qi_deficiency")

        assert response.status_code == 200
        data = response.json()
        assert "recommended" in data["data"]
        assert len(data["data"]["recommended"]) == 5

    def test_search_ingredients(self, client: TestClient, db_session):
        """测试搜索食材"""
        from api.models import Ingredient
        ingredient = Ingredient(
            id="api-search-001",
            name="山药",
            aliases=["怀山药"],
            efficacy="健脾养胃"
        )
        db_session.add(ingredient)
        db_session.commit()

        response = client.get("/api/v1/ingredients?keyword=山药")

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) > 0

    def test_ingredient_not_found(self, client: TestClient):
        """测试食材不存在"""
        response = client.get("/api/v1/ingredients/non-existent-id")

        assert response.status_code == 404
```

### 3.2 食谱API测试

```python
# backend/tests/test_api/test_recipes_api.py

import pytest


class TestRecipesAPI:
    """食谱API集成测试"""

    def test_get_recipes_list(self, client: TestClient, db_session):
        """测试获取食谱列表"""
        from api.models import Recipe
        recipes = [
            Recipe(
                id=f"api-recipe-{i:03d}",
                name=f"食谱{i}",
                type="粥类"
            )
            for i in range(1, 11)
        ]
        db_session.add_all(recipes)
        db_session.commit()

        response = client.get("/api/v1/recipes")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total"] == 10

    def test_get_recipe_detail(self, client: TestClient, db_session):
        """测试获取食谱详情"""
        from api.models import Recipe
        recipe = Recipe(
            id="api-recipe-detail-001",
            name="山药莲子粥",
            type="粥类",
            ingredients={"main": [{"name": "山药", "amount": "100g"}]},
            steps=["步骤1", "步骤2"]
        )
        db_session.add(recipe)
        db_session.commit()

        response = client.get("/api/v1/recipes/api-recipe-detail-001")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["name"] == "山药莲子粥"
        assert "steps" in data["data"]

    def test_get_recipes_by_constitution(self, client: TestClient, db_session):
        """测试按体质获取食谱"""
        from api.models import Recipe
        recipes = [
            Recipe(
                id=f"api-recipe-const-{i:03d}",
                name=f"食谱{i}",
                suitable_constitutions=["qi_deficiency"] if i % 2 == 0 else []
            )
            for i in range(1, 11)
        ]
        db_session.add_all(recipes)
        db_session.commit()

        response = client.get("/api/v1/recipes/recommend/qi_deficiency")

        assert response.status_code == 200
        data = response.json()
        assert "recipes" in data["data"]

    def test_search_recipes(self, client: TestClient, db_session):
        """测试搜索食谱"""
        from api.models import Recipe
        recipe = Recipe(
            id="api-recipe-search-001",
            name="山药粥",
            tags=["健脾", "养胃"]
        )
        db_session.add(recipe)
        db_session.commit()

        response = client.get("/api/v1/recipes?keyword=山药")

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) > 0
```

### 3.3 穴位API测试

```python
# backend/tests/test_api/test_acupoints_api.py

import pytest


class TestAcupointsAPI:
    """穴位API集成测试"""

    def test_get_acupoints_list(self, client: TestClient, db_session):
        """测试获取穴位列表"""
        from api.models import Acupoint
        acupoints = [
            Acupoint(
                id=f"api-acupoint-{i:03d}",
                name=f"穴位{i}",
                body_part="下肢" if i % 2 == 0 else "上肢"
            )
            for i in range(1, 11)
        ]
        db_session.add_all(acupoints)
        db_session.commit()

        response = client.get("/api/v1/acupoints")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total"] == 10

    def test_get_acupoint_detail(self, client: TestClient, db_session):
        """测试获取穴位详情"""
        from api.models import Acupoint
        acupoint = Acupoint(
            id="api-acupoint-detail-001",
            name="足三里",
            code="ST36",
            meridian="足阳明胃经"
        )
        db_session.add(acupoint)
        db_session.commit()

        response = client.get("/api/v1/acupoints/api-acupoint-detail-001")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["name"] == "足三里"

    def test_get_acupoints_by_symptom(self, client: TestClient, db_session):
        """测试按症状获取穴位"""
        from api.models import Acupoint, SymptomAcupoint
        acupoint = Acupoint(
            id="symptom-api-acu-001",
            name="足三里",
            efficacy=["健脾和胃"]
        )
        mapping = SymptomAcupoint(
            id="symptom-api-mapping-001",
            symptom_name="胃痛",
            acupoint_id="symptom-api-acu-001",
            priority=1
        )
        db_session.add_all([acupoint, mapping])
        db_session.commit()

        response = client.get("/api/v1/acupoints/by-symptom?symptom=胃痛")

        assert response.status_code == 200
        data = response.json()
        assert "acupoints" in data["data"]
```

### 3.4 舌诊API测试

```python
# backend/tests/test_api/test_tongue_diagnosis_api.py

import pytest
import base64


class TestTongueDiagnosisAPI:
    """舌诊API集成测试"""

    def test_analyze_tongue_image(self, client: TestClient):
        """测试舌诊图片分析"""
        # 模拟base64图片
        fake_image = base64.b64encode(b"fake_image_data").decode()

        response = client.post(
            "/api/v1/tongue-diagnosis/analyze",
            json={"image": fake_image}
        )

        assert response.status_code == 200
        data = response.json()
        assert "analysis" in data["data"]
        assert "conclusion" in data["data"]

    def test_analyze_with_user_result_id(self, client: TestClient, db_session):
        """测试带用户测试结果的舌诊分析"""
        from api.models import ConstitutionResult
        result = ConstitutionResult(
            id="test-result-for-comparison",
            primary_constitution="qi_deficiency",
            scores={"qi_deficiency": 50}
        )
        db_session.add(result)
        db_session.commit()

        fake_image = base64.b64encode(b"fake_image_data").decode()

        response = client.post(
            "/api/v1/tongue-diagnosis/analyze",
            json={
                "image": fake_image,
                "user_result_id": "test-result-for-comparison"
            }
        )

        assert response.status_code == 200
        data = response.json()
        # 验证有对比结果
        assert "comparison" in data["data"]["conclusion"]

    def test_invalid_image(self, client: TestClient):
        """测试无效图片"""
        response = client.post(
            "/api/v1/tongue-diagnosis/analyze",
            json={"image": "invalid_base64"}
        )

        assert response.status_code == 400

    def test_get_diagnosis_history(self, client: TestClient, db_session):
        """测试获取舌诊历史"""
        from api.models import TongueDiagnosisRecord
        record = TongueDiagnosisRecord(
            id="history-001",
            image_url="https://example.com/image.jpg",
            constitution_tendency="qi_deficiency"
        )
        db_session.add(record)
        db_session.commit()

        response = client.get("/api/v1/tongue-diagnosis/history")

        assert response.status_code == 200
        data = response.json()
        assert "items" in data["data"]
```

### 3.5 课程API测试

```python
# backend/tests/test_api/test_courses_api.py

import pytest


class TestCoursesAPI:
    """课程API集成测试"""

    def test_get_courses_list(self, client: TestClient, db_session):
        """测试获取课程列表"""
        from api.models import Course
        courses = [
            Course(
                id=f"api-course-{i:03d}",
                title=f"课程{i}",
                category="constitution",
                content_type="video"
            )
            for i in range(1, 11)
        ]
        db_session.add_all(courses)
        db_session.commit()

        response = client.get("/api/v1/courses")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total"] == 10

    def test_get_course_detail(self, client: TestClient, db_session):
        """测试获取课程详情"""
        from api.models import Course
        course = Course(
            id="api-course-detail-001",
            title="气虚质养生",
            content_type="video",
            duration=120
        )
        db_session.add(course)
        db_session.commit()

        response = client.get("/api/v1/courses/api-course-detail-001")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["title"] == "气虚质养生"

    def test_get_courses_by_constitution(self, client: TestClient, db_session):
        """测试按体质获取课程"""
        from api.models import Course
        courses = [
            Course(
                id=f"api-course-const-{i:03d}",
                title=f"课程{i}",
                category="constitution",
                suitable_constitutions=["qi_deficiency"] if i % 2 == 0 else []
            )
            for i in range(1, 11)
        ]
        db_session.add_all(courses)
        db_session.commit()

        response = client.get("/api/v1/courses/by-constitution/qi_deficiency")

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 5
```

---

## 四、前端测试

### 4.1 测试配置

```javascript
// frontend/vitest.config.js

import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./tests/setup.js'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/mockData',
        'dist/**'
      ]
    }
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  }
})
```

```javascript
// frontend/tests/setup.js

import { vi } from 'vitest'
import { config } from '@vue/test-utils'

// Mock uni-app API
global.uni = {
  request: vi.fn(),
  navigateTo: vi.fn(),
  redirectTo: vi.fn(),
  switchTab: vi.fn(),
  showToast: vi.fn(),
  getStorageSync: vi.fn(),
  setStorageSync: vi.fn()
}

// Mock onLoad
global.onLoad = (callback) => {
  callback({ constitution: 'qi_deficiency' })
}
```

### 4.2 API工具测试

```javascript
// frontend/tests/unit/api.spec.js

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { getIngredients, getIngredientDetail, getRecommendedIngredients } from '@/api/ingredients.js'
import { get, post } from '@/utils/request.js'

vi.mock('@/utils/request.js')

describe('Ingredients API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should get ingredients list', async () => {
    const mockData = {
      code: 0,
      data: {
        total: 2,
        items: [
          { id: '001', name: '山药', nature: '平' },
          { id: '002', name: '红枣', nature: '温' }
        ]
      }
    }

    get.mockResolvedValue(mockData)

    const result = await getIngredients({ page: 1, page_size: 10 })

    expect(get).toHaveBeenCalledWith('/api/v1/ingredients', {
      page: 1,
      page_size: 10
    })
    expect(result.data.items).toHaveLength(2)
  })

  it('should get ingredient detail', async () => {
    const mockData = {
      code: 0,
      data: {
        id: '001',
        name: '山药',
        nature: '平',
        suitable_constitutions: ['qi_deficiency']
      }
    }

    get.mockResolvedValue(mockData)

    const result = await getIngredientDetail('001')

    expect(get).toHaveBeenCalledWith('/api/v1/ingredients/001')
    expect(result.data.name).toBe('山药')
  })

  it('should get recommended ingredients by constitution', async () => {
    const mockData = {
      code: 0,
      data: {
        constitution: 'qi_deficiency',
        constitution_name: '气虚质',
        recommended: [
          { id: '001', name: '山药', reason: '健脾养胃' }
        ],
        avoided: [
          { id: '002', name: '山楂', reason: '破气耗气' }
        ]
      }
    }

    get.mockResolvedValue(mockData)

    const result = await getRecommendedIngredients('qi_deficiency')

    expect(get).toHaveBeenCalledWith('/api/v1/ingredients/recommend/qi_deficiency')
    expect(result.data.recommended).toHaveLength(1)
    expect(result.data.avoided).toHaveLength(1)
  })
})
```

### 4.3 食材列表页测试

```javascript
// frontend/tests/unit/ingredients/list.spec.js

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import IngredientsList from '@/pages/ingredients/list.vue'
import { getIngredients, getRecommendedIngredients } from '@/api/ingredients.js'

vi.mock('@/api/ingredients.js')

describe('IngredientsList Page', () => {
  let wrapper

  const mockIngredients = [
    { id: '001', name: '山药', nature: '平', category: '蔬菜' },
    { id: '002', name: '红枣', nature: '温', category: '水果' },
    { id: '003', name: '莲子', nature: '平', category: '药材' }
  ]

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should render ingredients list', async () => {
    getIngredients.mockResolvedValue({
      data: {
        items: mockIngredients,
        total: 3
      }
    })

    wrapper = mount(IngredientsList, {
      props: {
        constitution: 'qi_deficiency'
      }
    })

    await wrapper.vm.$nextTick()

    expect(wrapper.findAll('.ingredient-item')).toHaveLength(3)
  })

  it('should filter by constitution', async () => {
    getRecommendedIngredients.mockResolvedValue({
      data: {
        recommended: mockIngredients,
        avoided: []
      }
    })

    wrapper = mount(IngredientsList, {
      props: {
        constitution: 'qi_deficiency'
      }
    })

    await wrapper.vm.loadByConstitution('qi_deficiency')
    await wrapper.vm.$nextTick()

    expect(getRecommendedIngredients).toHaveBeenCalledWith('qi_deficiency')
  })

  it('should handle search functionality', async () => {
    getIngredients.mockResolvedValue({
      data: {
        items: [mockIngredients[0]],
        total: 1
      }
    })

    wrapper = mount(IngredientsList)

    await wrapper.vm.searchIngredients('山药')
    await wrapper.vm.$nextTick()

    expect(wrapper.findAll('.ingredient-item')).toHaveLength(1)
  })

  it('should navigate to detail page', async () => {
    const navigateTo = vi.fn()
    global.uni.navigateTo = navigateTo

    wrapper = mount(IngredientsList)

    wrapper.vm.goToDetail('001')
    await wrapper.vm.$nextTick()

    expect(navigateTo).toHaveBeenCalledWith({
      url: '/pages/ingredients/detail?id=001'
    })
  })
})
```

### 4.4 食材详情页测试

```javascript
// frontend/tests/unit/ingredients/detail.spec.js

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import IngredientDetail from '@/pages/ingredients/detail.vue'
import { getIngredientDetail } from '@/api/ingredients.js'

vi.mock('@/api/ingredients.js')

describe('IngredientDetail Page', () => {
  let wrapper

  const mockIngredient = {
    id: '001',
    name: '山药',
    aliases: ['怀山药', '淮山'],
    nature: '平',
    flavor: '甘',
    meridians: ['脾', '肺', '肾'],
    suitable_constitutions: ['qi_deficiency', 'yin_deficiency'],
    avoid_constitutions: ['phlegm_damp'],
    efficacy: '健脾养胃、补肺益肾',
    cooking_methods: ['蒸', '煮', '炖'],
    compatible_with: ['莲子', '枸杞'],
    incompatible_with: ['碱性食物']
  }

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should render ingredient detail', async () => {
    getIngredientDetail.mockResolvedValue({ data: mockIngredient })

    wrapper = mount(IngredientDetail, {
      props: {
        id: '001'
      }
    })

    await wrapper.vm.$nextTick()

    expect(wrapper.vm.ingredient.name).toBe('山药')
    expect(wrapper.vm.ingredient.nature).toBe('平')
  })

  it('should display suitable constitutions', async () => {
    getIngredientDetail.mockResolvedValue({ data: mockIngredient })

    wrapper = mount(IngredientDetail, {
      props: {
        id: '001'
      }
    })

    await wrapper.vm.loadDetail()
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.ingredient.suitable_constitutions).toContain('qi_deficiency')
    expect(wrapper.findAll('.constitution-tag.suitable')).toHaveLength(2)
  })

  it('should display avoided constitutions', async () => {
    getIngredientDetail.mockResolvedValue({ data: mockIngredient })

    wrapper = mount(IngredientDetail, {
      props: {
        id: '001'
      }
    })

    await wrapper.vm.loadDetail()
    await wrapper.vm.$nextTick()

    expect(wrapper.findAll('.constitution-tag.avoided')).toHaveLength(1)
  })

  it('should show related recipes', async () => {
    getIngredientDetail.mockResolvedValue({
      data: {
        ...mockIngredient,
        related_recipes: [
          { id: 'r001', name: '山药莲子粥' },
          { id: 'r002', name: '山药炖鸡汤' }
        ]
      }
    })

    wrapper = mount(IngredientDetail, {
      props: {
        id: '001'
      }
    })

    await wrapper.vm.loadDetail()
    await wrapper.vm.$nextTick()

    expect(wrapper.findAll('.recipe-item')).toHaveLength(2)
  })

  it('should handle favorite action', async () => {
    getIngredientDetail.mockResolvedValue({ data: mockIngredient })

    const setStorageSync = vi.fn()
    global.uni.setStorageSync = setStorageSync
    const showToast = vi.fn()
    global.uni.showToast = showToast

    wrapper = mount(IngredientDetail, {
      props: {
        id: '001'
      }
    })

    await wrapper.vm.toggleFavorite()
    await wrapper.vm.$nextTick()

    expect(setStorageSync).toHaveBeenCalled()
    expect(showToast).toHaveBeenCalledWith({
      title: '已收藏',
      icon: 'success'
    })
  })
})
```

### 4.5 食谱列表页测试

```javascript
// frontend/tests/unit/recipes/list.spec.js

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import RecipesList from '@/pages/recipes/list.vue'
import { getRecipes, getRecommendedRecipes } from '@/api/recipes.js'

vi.mock('@/api/recipes.js')

describe('RecipesList Page', () => {
  let wrapper

  const mockRecipes = [
    { id: 'r001', name: '山药莲子粥', type: '粥类', difficulty: '简单' },
    { id: 'r002', name: '黄芪炖鸡汤', type: '汤类', difficulty: '中等' }
  ]

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should render recipes list', async () => {
    getRecipes.mockResolvedValue({
      data: {
        items: mockRecipes,
        total: 2
      }
    })

    wrapper = mount(RecipesList)

    await wrapper.vm.loadRecipes()
    await wrapper.vm.$nextTick()

    expect(wrapper.findAll('.recipe-item')).toHaveLength(2)
  })

  it('should get recipes by constitution', async () => {
    getRecommendedRecipes.mockResolvedValue({
      data: {
        constitution: 'qi_deficiency',
        recipes: {
          breakfast: mockRecipes,
          lunch: [],
          dinner: []
        }
      }
    })

    wrapper = mount(RecipesList, {
      props: {
        constitution: 'qi_deficiency'
      }
    })

    await wrapper.vm.loadByConstitution('qi_deficiency')
    await wrapper.vm.$nextTick()

    expect(getRecommendedRecipes).toHaveBeenCalledWith('qi_deficiency')
  })

  it('should filter by meal type', async () => {
    getRecipes.mockResolvedValue({
      data: {
        items: mockRecipes,
        total: 2
      }
    })

    wrapper = mount(RecipesList)

    await wrapper.vm.filterByMealType('breakfast')
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.selectedMealType).toBe('breakfast')
  })
})
```

### 4.6 穴位列表页测试

```javascript
// frontend/tests/unit/acupoints/list.spec.js

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import AcupointsList from '@/pages/acupoints/list.vue'
import { getAcupoints, getAcupointsBySymptom } from '@/api/acupoints.js'

vi.mock('@/api/acupoints.js')

describe('AcupointsList Page', () => {
  let wrapper

  const mockAcupoints = [
    { id: 'a001', name: '足三里', code: 'ST36', body_part: '下肢' },
    { id: 'a002', name: '三阴交', code: 'SP6', body_part: '下肢' }
  ]

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should render acupoints list', async () => {
    getAcupoints.mockResolvedValue({
      data: {
        items: mockAcupoints,
        total: 2
      }
    })

    wrapper = mount(AcupointsList)

    await wrapper.vm.loadAcupoints()
    await wrapper.vm.$nextTick()

    expect(wrapper.findAll('.acupoint-item')).toHaveLength(2)
  })

  it('should filter by body part', async () => {
    getAcupoints.mockResolvedValue({
      data: {
        items: mockAcupoints,
        total: 2
      }
    })

    wrapper = mount(AcupointsList)

    await wrapper.vm.filterByBodyPart('下肢')
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.selectedBodyPart).toBe('下肢')
  })

  it('should get acupoints by symptom', async () => {
    getAcupointsBySymptom.mockResolvedValue({
      data: {
        symptom: '胃痛',
        acupoints: mockAcupoints
      }
    })

    wrapper = mount(AcupointsList)

    await wrapper.vm.searchBySymptom('胃痛')
    await wrapper.vm.$nextTick()

    expect(getAcupointsBySymptom).toHaveBeenCalledWith('胃痛')
  })
})
```

### 4.7 体质结果页测试（验证新增功能）

```javascript
// frontend/tests/unit/result/integration.spec.js

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import ResultPage from '@/pages/result/result.vue'
import { getResult } from '@/api/constitution.js'

vi.mock('@/api/constitution.js')

describe('Result Page - Integration Tests', () => {
  let wrapper

  const mockResult = {
    result_id: 'test-result-001',
    primary_constitution: 'qi_deficiency',
    primary_constitution_name: '气虚质',
    scores: {
      qi_deficiency: 50,
      yin_deficiency: 30
    }
  }

  beforeEach(() => {
    vi.clearAllMocks()
    global.uni.getStorageSync.mockReturnValue(mockResult)
    global.uni.navigateTo = vi.fn()
  })

  it('should have ingredient recommendation button', async () => {
    getResult.mockResolvedValue({ data: mockResult })

    wrapper = mount(ResultPage, {
      props: {
        resultId: 'test-result-001'
      }
    })

    await wrapper.vm.loadResult()
    await wrapper.vm.$nextTick()

    expect(wrapper.find('.recommend-ingredients-btn').exists()).toBe(true)
  })

  it('should have recipe recommendation button', async () => {
    getResult.mockResolvedValue({ data: mockResult })

    wrapper = mount(ResultPage, {
      props: {
        resultId: 'test-result-001'
      }
    })

    await wrapper.vm.loadResult()
    await wrapper.vm.$nextTick()

    expect(wrapper.find('.recommend-recipes-btn').exists()).toBe(true)
  })

  it('should navigate to ingredients list with constitution', async () => {
    getResult.mockResolvedValue({ data: mockResult })

    wrapper = mount(ResultPage, {
      props: {
        resultId: 'test-result-001'
      }
    })

    await wrapper.vm.loadResult()
    await wrapper.vm.$nextTick()

    await wrapper.vm.goToIngredients()

    expect(global.uni.navigateTo).toHaveBeenCalledWith({
      url: '/pages/ingredients/list?constitution=qi_deficiency'
    })
  })

  it('should navigate to recipes list with constitution', async () => {
    getResult.mockResolvedValue({ data: mockResult })

    wrapper = mount(ResultPage, {
      props: {
        resultId: 'test-result-001'
      }
    })

    await wrapper.vm.loadResult()
    await wrapper.vm.$nextTick()

    await wrapper.vm.goToRecipes()

    expect(global.uni.navigateTo).toHaveBeenCalledWith({
      url: '/pages/recipes/list?constitution=qi_deficiency'
    })
  })
})
```

---

## 五、端到端测试（可选）

### 5.1 E2E测试场景

```typescript
// frontend/tests/e2e/constitution-flow.spec.ts

import { test, expect } from '@playwright/test'

test.describe('体质测试完整流程', () => {
  test('用户完成体质测试并查看推荐内容', async ({ page }) => {
    // 1. 打开首页
    await page.goto('http://localhost:5173/#/pages/index/index')

    // 2. 点击开始测试
    await page.click('.start-test-btn')

    // 3. 等待跳转到测试页
    await page.waitForURL('/pages/test/test')

    // 4. 完成30题
    for (let i = 0; i < 30; i++) {
      await page.click(`.option-item:nth-child(1)`)  // 选择"没有"
      await page.click('.btn-primary')  // 下一题
    }

    // 5. 提交测试
    await page.click('.btn-large')

    // 6. 等待跳转到结果页
    await page.waitForURL('/pages/result/result*')

    // 7. 验证结果页显示
    await expect(page.locator('.constitution-name')).toBeVisible()

    // 8. 点击推荐食材
    await page.click('.recommend-ingredients-btn')

    // 9. 验证跳转到食材列表页
    await page.waitForURL('/pages/ingredients/list*')

    // 10. 验证显示推荐的食材
    await expect(page.locator('.ingredient-item').first()).toBeVisible()
  })
})

test.describe('食材浏览流程', () => {
  test('用户浏览食材详情并查看相关食谱', async ({ page }) => {
    // 1. 直接访问食材列表页（带体质参数）
    await page.goto('http://localhost:5173/#/pages/ingredients/list?constitution=qi_deficiency')

    // 2. 点击第一个食材
    await page.click('.ingredient-item:first-child')

    // 3. 验证跳转到详情页
    await page.waitForURL('/pages/ingredients/detail*')

    // 4. 验证显示食材详情
    await expect(page.locator('.ingredient-name')).toBeVisible()
    await expect(page.locator('.nature-tag')).toBeVisible()

    // 5. 验证显示推荐食谱
    await expect(page.locator('.recipe-item').first()).toBeVisible()

    // 6. 点击相关食谱
    await page.click('.recipe-item:first-child')

    // 7. 验证跳转到食谱详情页
    await page.waitForURL('/pages/recipes/detail*')
  })
})

test.describe('穴位查找流程', () => {
  test('用户按症状查找穴位', async ({ page }) => {
    // 1. 访问穴位列表页
    await page.goto('http://localhost:5173/#/pages/acupoints/list')

    // 2. 点击症状搜索
    await page.click('.symptom-search-btn')

    // 3. 输入症状"失眠"
    await page.fill('.symptom-input', '失眠')

    // 4. 点击搜索
    await page.click('.search-btn')

    // 5. 验证显示相关穴位
    await expect(page.locator('.acupoint-item').first()).toBeVisible()

    // 6. 点击第一个穴位
    await page.click('.acupoint-item:first-child')

    // 7. 验证跳转到穴位详情页
    await page.waitForURL('/pages/acupoints/detail*')

    // 8. 验证显示穴位位置和按摩方法
    await expect(page.locator('.location-text')).toBeVisible()
    await expect(page.locator('.massage-method')).toBeVisible()
  })
})
```

---

## 六、性能测试

### 6.1 API性能测试

```python
# backend/tests/test_performance/api_performance.py

import pytest
import time
from fastapi.testclient import TestClient


class TestAPIPerformance:
    """API性能测试"""

    def test_ingredients_list_response_time(self, client: TestClient, db_session):
        """测试食材列表响应时间（应< 200ms）"""
        from api.models import Ingredient

        # 创建100个测试食材
        ingredients = [
            Ingredient(
                id=f"perf-{i:03d}",
                name=f"食材{i}",
                category="蔬菜"
            )
            for i in range(100)
        ]
        db_session.add_all(ingredients)
        db_session.commit()

        start_time = time.time()
        response = client.get("/api/v1/ingredients")
        end_time = time.time()

        response_time = (end_time - start_time) * 1000  # 转换为毫秒

        assert response.status_code == 200
        assert response_time < 200, f"响应时间 {response_time}ms 超过 200ms"

    def test_recipe_detail_response_time(self, client: TestClient, db_session):
        """测试食谱详情响应时间（应< 100ms）"""
        from api.models import Recipe

        recipe = Recipe(
            id="perf-recipe-001",
            name="测试食谱",
            ingredients={"main": [{"name": "食材1", "amount": "100g"}] * 10},
            steps=["步骤1"] * 10
        )
        db_session.add(recipe)
        db_session.commit()

        start_time = time.time()
        response = client.get("/api/v1/recipes/perf-recipe-001")
        end_time = time.time()

        response_time = (end_time - start_time) * 1000

        assert response.status_code == 200
        assert response_time < 100

    def test_search_performance(self, client: TestClient, db_session):
        """测试搜索性能"""
        from api.models import Ingredient

        # 创建1000个测试食材
        ingredients = [
            Ingredient(
                id=f"search-perf-{i:03d}",
                name=f"食材{i}山药测试",
                category="蔬菜"
            )
            for i in range(1000)
        ]
        db_session.add_all(ingredients)
        db_session.commit()

        start_time = time.time()
        response = client.get("/api/v1/ingredients?keyword=山药")
        end_time = time.time()

        response_time = (end_time - start_time) * 1000

        assert response.status_code == 200
        assert response_time < 300
```

### 6.2 前端性能测试

```javascript
// frontend/tests/e2e/performance.spec.ts

import { test, expect } from '@playwright/test'

test.describe('前端性能测试', () => {
  test('食材列表页加载性能', async ({ page }) => {
    // 开始性能监控
    await page.goto('http://localhost:5173/#/pages/ingredients/list')

    // 等待页面加载完成
    await page.waitForLoadState('networkidle')

    // 获取性能指标
    const metrics = await page.evaluate(() => {
      const perfData = performance.getEntriesByType('navigation')[0]
      return {
        loadTime: perfData.loadEventEnd - perfData.fetchStart,
        domContentLoaded: perfData.domContentLoadedEventEnd - perfData.fetchStart,
        firstPaint: perfData.responseStart - perfData.fetchStart
      }
    })

    // 验证性能指标
    expect(metrics.loadTime).toBeLessThan(3000)  // 总加载时间 < 3秒
    expect(metrics.domContentLoaded).toBeLessThan(1500)  // DOM加载 < 1.5秒
  })

  test('页面滚动性能', async ({ page }) => {
    await page.goto('http://localhost:5173/#/pages/ingredients/list')
    await page.waitForLoadState('networkidle')

    // 模拟滚动
    const scrollTimes = []
    for (let i = 0; i < 10; i++) {
      const start = performance.now()
      await page.evaluate(() => {
        window.scrollBy(0, window.innerHeight)
      })
      await page.waitForTimeout(100)  // 等待滚动完成
      scrollTimes.push(performance.now() - start)
    }

    // 验证滚动流畅（每次滚动 < 100ms）
    const avgScrollTime = scrollTimes.reduce((a, b) => a + b, 0) / scrollTimes.length
    expect(avgScrollTime).toBeLessThan(100)
  })
})
```

---

## 七、数据验证测试

### 7.1 体质关联数据验证

```python
# backend/tests/test_validation/data_validation.py

import pytest
from api.services.validation_service import ValidationService


class TestDataValidation:
    """数据验证测试"""

    def test_validate_constitution_codes(self):
        """验证体质代码有效性"""
        validator = ValidationService()

        valid_codes = [
            "peace", "qi_deficiency", "yang_deficiency", "yin_deficiency",
            "phlegm_damp", "damp_heat", "blood_stasis", "qi_depression", "special"
        ]

        for code in valid_codes:
            assert validator.is_valid_constitution_code(code)

    def test_validate_ingredient_constitution_mapping(self, db_session):
        """验证食材体质映射"""
        from api.models import Ingredient

        # 创建测试食材
        ingredient = Ingredient(
            id="validation-001",
            name="山药",
            suitable_constitutions=["qi_deficiency", "yin_deficiency"],
            avoid_constitutions=["phlegm_damp"]
        )
        db_session.add(ingredient)
        db_session.commit()

        validator = ValidationService()
        is_valid = validator.validate_ingredient_constitution_mapping("validation-001", db_session)

        assert is_valid is True

    def test_validate_recipe_ingredients(self, db_session):
        """验证食谱食材完整性"""
        from api.models import Recipe

        recipe = Recipe(
            id="validation-recipe-001",
            name="测试食谱",
            ingredients={
                "main": [{"name": "山药", "amount": "100g"}],
                "auxiliary": [],
                "seasoning": []
            }
        )
        db_session.add(recipe)
        db_session.commit()

        validator = ValidationService()
        is_valid = validator.validate_recipe_ingredients("validation-recipe-001", db_session)

        assert is_valid is True

    def test_validate_acupoint_meridian_code(self):
        """验证穴位经络代码格式"""
        validator = ValidationService()

        # 有效代码
        valid_codes = ["ST36", "SP6", "CV12", "GV4", "KI1"]
        for code in valid_codes:
            assert validator.is_valid_meridian_code(code)

        # 无效代码
        invalid_codes = ["XX00", "ST999", ""]
        for code in invalid_codes:
            assert not validator.is_valid_meridian_code(code)

    def test_validate_tongue_diagnosis_mapping(self):
        """验证舌诊体质映射完整性"""
        validator = ValidationService()

        # 所有9种体质都应该有映射规则
        required_constitutions = [
            "peace", "qi_deficiency", "yang_deficiency", "yin_deficiency",
            "phlegm_damp", "damp_heat", "blood_stasis", "qi_depression", "special"
        ]

        mapping = validator.get_tongue_constitution_mapping()

        for constitution in required_constitutions:
            assert constitution in mapping
```

---

## 八、测试运行指南

### 8.1 后端测试运行

```bash
# 进入后端目录
cd backend

# 安装测试依赖
pip install pytest pytest-cov pytest-asyncio httpx

# 运行所有测试
pytest

# 运行单元测试
pytest tests/test_unit/

# 运行API测试
pytest tests/test_api/

# 生成覆盖率报告
pytest --cov=api --cov-report=html

# 运行特定测试文件
pytest tests/test_unit/test_ingredients.py -v

# 运行带标记的测试
pytest -m unit
```

### 8.2 前端测试运行

```bash
# 进入前端目录
cd frontend

# 运行所有测试
npm run test

# 运行单元测试
npm run test:unit

# 运行E2E测试
npm run test:e2e

# 生成覆盖率报告
npm run test:coverage

# UI模式
npm run test:ui
```

### 8.3 测试数据准备

```bash
# 准备测试数据脚本
cd backend/scripts
python prepare_test_data.py

# 这将创建测试数据库并插入测试数据
```

---

## 九、测试验收标准

### 9.1 代码覆盖率要求

| 模块 | 单元测试覆盖率 | API测试覆盖率 |
|-----|---------------|--------------|
| 食材服务 | > 80% | > 90% |
| 食谱服务 | > 80% | > 90% |
| 穴位服务 | > 80% | > 90% |
| 舌诊服务 | > 70% | > 85% |
| 课程服务 | > 75% | > 85% |

### 9.2 性能要求

| 指标 | 目标值 |
|-----|--------|
| API响应时间 | < 200ms (列表) |
| API响应时间 | < 100ms (详情) |
| 页面加载时间 | < 3秒 |
| 首次渲染时间 | < 1.5秒 |

### 9.3 功能验收清单

#### 食材库
- [x] 可以查看食材列表
- [x] 可以查看食材详情
- [x] 可以按体质筛选食材
- [x] 可以搜索食材
- [x] 可以收藏食材
- [x] 从体质结果页可跳转

#### 食谱库
- [x] 可以查看食谱列表
- [x] 可以查看食谱详情
- [x] 可以按体质推荐食谱
- [x] 可以按餐次筛选
- [x] 可以收藏食谱
- [x] 显示相关食材

#### 穴位查找
- [x] 可以查看穴位列表
- [x] 可以查看穴位详情
- [x] 可以按症状查找
- [x] 可以按部位筛选
- [x] 显示按摩方法

#### AI舌诊
- [x] 可以拍照上传
- [x] 可以生成分析报告
- [x] 可以与测试结果对比
- [x] 可以查看历史记录

#### 养生课程
- [x] 可以查看课程列表
- [x] 可以查看课程详情
- [x] 可以按体质分类
- [x] 可以播放视频

---

## 十、测试报告模板

### 10.1 测试执行报告

```markdown
# 测试执行报告

**测试日期：** YYYY-MM-DD
**测试人员：** XXX
**测试版本：** v1.0

## 测试概览

| 测试类型 | 计划用例 | 执行用例 | 通过 | 失败 | 通过率 |
|---------|---------|---------|-----|-----|--------|
| 单元测试 | 150 | 150 | 148 | 2 | 98.7% |
| API测试 | 80 | 80 | 78 | 2 | 97.5% |
| 前端测试 | 60 | 60 | 58 | 2 | 96.7% |
| E2E测试 | 20 | 20 | 20 | 0 | 100% |
| 性能测试 | 10 | 10 | 10 | 0 | 100% |
| **总计** | **320** | **320** | **314** | **6** | **98.1%** |

## 缺陷统计

| 严重程度 | 数量 | 已修复 | 待修复 |
|---------|-----|-------|--------|
| 严重 | 0 | 0 | 0 |
| 重要 | 2 | 2 | 0 |
| 一般 | 4 | 3 | 1 |
| 轻微 | 5 | 4 | 1 |

## 测试结论

- [x] 通过验收标准
- [x] 性能达到要求
- [x] 可以发布

## 遗留问题

1. 食材搜索性能待优化（计划优化到 < 100ms）
2. 舌诊规则准确性待提升（需要更多真实数据验证）
```

---

## 文档更新记录

| 版本 | 日期 | 更新内容 | 更新人 |
|-----|-----|---------|--------|
| v1.0 | 2026-01-18 | 第一期测试计划初版 | Claude |
