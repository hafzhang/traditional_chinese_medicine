# 后端测试规范

## 目录

1. [测试框架配置](#测试框架配置)
2. [测试结构](#测试结构)
3. [Fixtures 使用](#fixtures-使用)
4. [单元测试](#单元测试)
5. [API 测试](#api-测试)
6. [数据库测试策略](#数据库测试策略)
7. [Mock 和 Stub](#mock-和-stub)
8. [Phase 1 测试案例](#phase-1-测试案例)
9. [性能测试](#性能测试)
10. [最佳实践](#最佳实践)

---

## 测试框架配置

### Pytest 配置

项目使用 Pytest 作为测试框架，配置文件为 `backend/tests/conftest.py`。

```python
# backend/tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# 测试数据库配置
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)
```

### 依赖安装

```bash
pip install pytest pytest-cov pytest-asyncio
```

### Pytest 配置文件 (可选)

在 `backend/pytest.ini` 中：

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=api
    --cov-report=term-missing
    --cov-report=html
```

---

## 测试结构

```
backend/tests/
├── conftest.py                     # Pytest 配置和共享 fixtures
├── __init__.py
├── test_unit/                      # 单元测试目录
│   ├── __init__.py
│   ├── test_ingredients.py         # 食材服务测试
│   ├── test_recipes.py             # 食谱服务测试
│   ├── test_acupoints.py           # 穴位服务测试
│   ├── test_tongue_diagnosis.py    # 舌诊服务测试
│   └── test_courses.py             # 课程服务测试
└── test_api/                       # API 集成测试目录
    ├── __init__.py
    ├── test_ingredients_api.py
    ├── test_recipes_api.py
    ├── test_acupoints_api.py
    ├── test_tongue_diagnosis_api.py
    └── test_courses_api.py
```

---

## Fixtures 使用

### 可用 Fixtures

#### `db_session` - 数据库会话

```python
def test_create_ingredient(db_session):
    """测试：创建食材"""
    from api.models import Ingredient

    ingredient = Ingredient(
        name="山药",
        category="药材",
        nature="平",
        flavor="甘"
    )
    db_session.add(ingredient)
    db_session.commit()

    assert ingredient.id is not None
```

#### `client` - API 测试客户端

```python
def test_get_ingredient_api(client, db_session):
    """测试：获取食材 API"""
    from api.models import Ingredient

    ingredient = Ingredient(name="山药")
    db_session.add(ingredient)
    db_session.commit()

    response = client.get(f"/ingredients/{ingredient.id}")
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "山药"
```

#### `test_ingredient_data` - 测试食材数据

```python
def test_with_fixture_data(db_session, test_ingredient_data):
    """测试：使用 fixture 数据"""
    from api.models import Ingredient

    ingredient = Ingredient(**test_ingredient_data)
    db_session.add(ingredient)
    db_session.commit()

    assert ingredient.name == "山药"
```

#### `test_recipe_data` - 测试食谱数据

```python
def test_create_recipe(db_session, test_recipe_data):
    """测试：创建食谱"""
    from api.models import Recipe

    recipe = Recipe(**test_recipe_data)
    db_session.add(recipe)
    db_session.commit()

    assert recipe.name == "山药莲子粥"
```

#### `test_acupoint_data` - 测试穴位数据

```python
def test_create_acupoint(db_session, test_acupoint_data):
    """测试：创建穴位"""
    from api.models import Acupoint

    acupoint = Acupoint(**test_acupoint_data)
    db_session.add(acupoint)
    db_session.commit()

    assert acupoint.name == "足三里"
```

#### `test_course_data` - 测试课程数据

```python
def test_create_course(db_session, test_course_data):
    """测试：创建课程"""
    from api.models import Course

    course = Course(**test_course_data)
    db_session.add(course)
    db_session.commit()

    assert course.title == "气虚质怎么调理？"
```

### 自定义 Fixtures

```python
# 在 conftest.py 中添加
@pytest.fixture
def sample_ingredient(db_session):
    """创建示例食材"""
    ingredient = Ingredient(
        name="黄芪",
        category="药材",
        nature="温",
        flavor="甘",
        suitable_constitutions=["qi_deficiency"]
    )
    db_session.add(ingredient)
    db_session.commit()
    db_session.refresh(ingredient)
    return ingredient

# 使用
def test_with_sample(sample_ingredient):
    assert sample_ingredient.name == "黄芪"
```

---

## 单元测试

### 测试服务层方法

```python
# tests/test_unit/test_ingredients.py
class TestIngredientService:
    """食材服务单元测试"""

    def test_get_ingredient_by_id_success(self, db_session):
        """测试：根据 ID 成功获取食材"""
        # Arrange
        from api.models import Ingredient
        from api.services.ingredient_service import IngredientService

        ingredient = Ingredient(name="山药", category="药材")
        db_session.add(ingredient)
        db_session.commit()

        # Act
        service = IngredientService()
        result = service.get_ingredient_by_id(ingredient.id, db_session)

        # Assert
        assert result is not None
        assert result.name == "山药"
        assert result.category == "药材"

    def test_get_ingredient_by_id_not_found(self, db_session):
        """测试：根据 ID 获取不存在的食材"""
        from api.services.ingredient_service import IngredientService

        service = IngredientService()
        result = service.get_ingredient_by_id("non-existent-id", db_session)

        assert result is None

    def test_get_ingredients_by_constitution(self, db_session):
        """测试：根据体质获取推荐食材"""
        from api.models import Ingredient
        from api.services.ingredient_service import IngredientService

        # 创建测试数据
        ingredient1 = Ingredient(
            name="黄芪",
            suitable_constitutions=["qi_deficiency"]
        )
        ingredient2 = Ingredient(
            name="枸杞",
            suitable_constitutions=["yin_deficiency"]
        )
        db_session.add_all([ingredient1, ingredient2])
        db_session.commit()

        # Act
        service = IngredientService()
        results = service.get_ingredients_by_constitution("qi_deficiency", db_session)

        # Assert
        assert len(results) == 1
        assert results[0].name == "黄芪"

    def test_get_ingredients_to_avoid(self, db_session):
        """测试：根据体质获取禁忌食材"""
        from api.models import Ingredient
        from api.services.ingredient_service import IngredientService

        ingredient = Ingredient(
            name="蜂蜜",
            avoid_constitutions=["phlegm_damp"]
        )
        db_session.add(ingredient)
        db_session.commit()

        service = IngredientService()
        results = service.get_ingredients_to_avoid("phlegm_damp", db_session)

        assert len(results) == 1
        assert results[0].name == "蜂蜜"
```

### 测试边界条件

```python
def test_get_ingredients_list_pagination(self, db_session):
    """测试：食材列表分页"""
    from api.models import Ingredient
    from api.services.ingredient_service import IngredientService

    # 创建 25 个食材
    for i in range(25):
        ingredient = Ingredient(name=f"食材{i}", category="药材")
        db_session.add(ingredient)
    db_session.commit()

    service = IngredientService()

    # 测试第一页
    items, total = service.get_ingredients_list(db_session, skip=0, limit=20)
    assert total == 25
    assert len(items) == 20

    # 测试第二页
    items, total = service.get_ingredients_list(db_session, skip=20, limit=20)
    assert len(items) == 5

def test_invalid_constitution_code(self, db_session):
    """测试：无效的体质代码"""
    from api.services.ingredient_service import IngredientService

    service = IngredientService()
    results = service.get_ingredients_by_constitution("invalid_code", db_session)

    assert results == []
```

### 参数化测试

```python
import pytest

@pytest.mark.parametrize("constitution,expected_count", [
    ("qi_deficiency", 1),
    ("yin_deficiency", 1),
    ("phlegm_damp", 0),
])
def test_get_ingredients_by_constitution_parametrized(
    self, db_session, constitution, expected_count
):
    """参数化测试：根据体质获取食材"""
    from api.models import Ingredient
    from api.services.ingredient_service import IngredientService

    ingredient = Ingredient(
        name="山药",
        suitable_constitutions=["qi_deficiency", "yin_deficiency"]
    )
    db_session.add(ingredient)
    db_session.commit()

    service = IngredientService()
    results = service.get_ingredients_by_constitution(constitution, db_session)

    assert len(results) == expected_count
```

---

## API 测试

### 基本 API 测试

```python
# tests/test_api/test_ingredients_api.py
class TestIngredientsAPI:
    """食材 API 测试"""

    def test_get_ingredients_list(self, client):
        """测试：获取食材列表"""
        response = client.get("/ingredients?skip=0&limit=20")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "data" in data
        assert "total" in data["data"]
        assert "items" in data["data"]

    def test_get_ingredients_with_filters(self, client, db_session):
        """测试：带筛选条件的食材列表"""
        from api.models import Ingredient

        ingredient = Ingredient(
            name="山药",
            category="药材",
            nature="平"
        )
        db_session.add(ingredient)
        db_session.commit()

        # 按类别筛选
        response = client.get("/ingredients?category=药材")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) >= 1

        # 按性味筛选
        response = client.get("/ingredients?nature=平")
        assert response.status_code == 200

    def test_get_ingredient_by_id(self, client, db_session):
        """测试：根据 ID 获取食材详情"""
        from api.models import Ingredient

        ingredient = Ingredient(
            name="山药",
            category="药材",
            nature="平",
            flavor="甘"
        )
        db_session.add(ingredient)
        db_session.commit()

        response = client.get(f"/ingredients/{ingredient.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["name"] == "山药"
        assert data["data"]["category"] == "药材"

    def test_get_ingredient_by_id_not_found(self, client):
        """测试：获取不存在的食材返回 404"""
        response = client.get("/ingredients/non-existent-id")
        assert response.status_code == 404

    def test_get_ingredient_recommendation(self, client, db_session):
        """测试：根据体质获取食材推荐"""
        from api.models import Ingredient

        ingredient = Ingredient(
            name="山药",
            suitable_constitutions=["qi_deficiency"],
            avoid_constitutions=["phlegm_damp"]
        )
        db_session.add(ingredient)
        db_session.commit()

        response = client.get("/ingredients/recommend/qi_deficiency")

        assert response.status_code == 200
        data = response.json()
        assert "recommended" in data["data"]
        assert "avoided" in data["data"]

    def test_invalid_constitution_code(self, client):
        """测试：无效的体质代码返回 400"""
        response = client.get("/ingredients/recommend/invalid_code")
        assert response.status_code == 400
```

### 测试请求头和认证

```python
def test_authenticated_request(self, client):
    """测试：需要认证的请求"""
    response = client.get(
        "/user/profile",
        headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 200
```

### 测试文件上传

```python
def test_upload_tongue_image(self, client):
    """测试：上传舌诊图片"""
    from io import BytesIO

    # 创建模拟图片
    image_content = b"fake_image_data"
    files = {"image": ("tongue.jpg", BytesIO(image_content), "image/jpeg")}

    response = client.post(
        "/tongue/analyze",
        files=files,
        data={
            "tongue_color": "淡白",
            "tongue_shape": "胖大",
            "coating_color": "白苔",
            "coating_thickness": "薄苔"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "analysis" in data["data"]
```

---

## 数据库测试策略

### 事务回滚

每个测试使用独立的事务，测试结束后自动回滚：

```python
@pytest.fixture(scope="function")
def db_session():
    """创建测试数据库会话，测试后自动回滚"""
    from api.database import Base

    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        session.rollback()
        Base.metadata.drop_all(bind=engine)
```

### 数据隔离

每个测试使用独立的数据库会话，确保测试之间互不影响：

```python
def test_ingredient_1(db_session):
    """测试 1"""
    ingredient = Ingredient(name="山药")
    db_session.add(ingredient)
    db_session.commit()
    assert ingredient.id is not None

def test_ingredient_2(db_session):
    """测试 2 - 不会看到测试 1 的数据"""
    ingredients = db_session.query(Ingredient).all()
    assert len(ingredients) == 0  # 数据已回滚
```

### JSON 字段查询

```python
def test_json_field_query(db_session):
    """测试：JSON 字段查询"""
    from api.models import Ingredient

    # 正确方式：使用 .contains()
    ingredient = Ingredient(
        name="山药",
        suitable_constitutions=["qi_deficiency", "yin_deficiency"]
    )
    db_session.add(ingredient)
    db_session.commit()

    # 查询
    results = db_session.query(Ingredient).filter(
        Ingredient.suitable_constitutions.contains("qi_deficiency")
    ).all()

    assert len(results) == 1
```

---

## Mock 和 Stub

### 使用 pytest-mock

```python
def test_with_mock(self, db_session, mocker):
    """测试：使用 mock"""
    from api.services.ingredient_service import IngredientService

    # Mock 外部 API 调用
    mock_response = {"data": {"name": "山药"}}
    mocker.patch("api.external_ingredient_api.fetch", return_value=mock_response)

    service = IngredientService()
    result = service.fetch_from_external_api("山药")

    assert result["name"] == "山药"
```

### 使用 Monkeypatch

```python
def test_with_monkeypatch(self, db_session, monkeypatch):
    """测试：使用 monkeypatch"""
    import api.services.ingredient_service as service_module

    def mock_get_data():
        return {"name": "山药"}

    monkeypatch.setattr(service_module, "get_data", mock_get_data)

    from api.services.ingredient_service import IngredientService
    service = IngredientService()
    result = service.get_data()

    assert result["name"] == "山药"
```

### Mock 数据库查询

```python
def test_with_mock_query(self, mocker):
    """测试：Mock 数据库查询"""
    # Mock 查询结果
    mock_ingredient = Ingredient(id="test-id", name="山药")
    mocker.patch(
        "api.services.ingredient_service.db_session.query",
        return_value=mocker.Mock(first=lambda: mock_ingredient)
    )

    service = IngredientService()
    result = service.get_ingredient_by_id("test-id", mocker.Mock())

    assert result.name == "山药"
```

---

## Phase 1 测试案例

### 食材服务完整测试

```python
# tests/test_unit/test_ingredients.py
class TestIngredientService:
    """食材服务完整测试套件"""

    def test_get_ingredient_by_id_success(self, db_session):
        """测试：根据 ID 成功获取食材"""
        from api.models import Ingredient
        from api.services.ingredient_service import IngredientService

        ingredient = Ingredient(
            name="山药",
            category="药材",
            nature="平",
            flavor="甘"
        )
        db_session.add(ingredient)
        db_session.commit()

        service = IngredientService()
        result = service.get_ingredient_by_id(ingredient.id, db_session)

        assert result is not None
        assert result.name == "山药"
        assert result.nature == "平"

    def test_get_ingredients_list_empty(self, db_session):
        """测试：空列表"""
        from api.services.ingredient_service import IngredientService

        service = IngredientService()
        items, total = service.get_ingredients_list(db_session)

        assert total == 0
        assert items == []

    def test_get_ingredients_by_constitution_qi_deficiency(self, db_session):
        """测试：获取气虚质推荐食材"""
        from api.models import Ingredient
        from api.services.ingredient_service import IngredientService

        ingredients = [
            Ingredient(name="黄芪", suitable_constitutions=["qi_deficiency"]),
            Ingredient(name="枸杞", suitable_constitutions=["yin_deficiency"]),
        ]
        db_session.add_all(ingredients)
        db_session.commit()

        service = IngredientService()
        results = service.get_ingredients_by_constitution("qi_deficiency", db_session)

        assert len(results) == 1
        assert results[0].name == "黄芪"

    def test_get_recommendation_by_constitution(self, db_session):
        """测试：获取推荐和禁忌食材"""
        from api.models import Ingredient
        from api.services.ingredient_service import IngredientService

        recommended_ingredient = Ingredient(
            name="山药",
            suitable_constitutions=["qi_deficiency"]
        )
        avoided_ingredient = Ingredient(
            name="蜂蜜",
            avoid_constitutions=["qi_deficiency"]
        )
        db_session.add_all([recommended_ingredient, avoided_ingredient])
        db_session.commit()

        service = IngredientService()
        result = service.get_recommendation_by_constitution("qi_deficiency", db_session)

        assert "recommended" in result
        assert "avoided" in result
        assert len(result["recommended"]) == 1
        assert len(result["avoided"]) == 1

    def test_increment_view_count(self, db_session):
        """测试：增加浏览次数"""
        from api.models import Ingredient
        from api.services.ingredient_service import IngredientService

        ingredient = Ingredient(name="山药", view_count=0)
        db_session.add(ingredient)
        db_session.commit()

        service = IngredientService()
        service.increment_view_count(ingredient.id, db_session)

        db_session.refresh(ingredient)
        assert ingredient.view_count == 1
```

### 食谱服务完整测试

```python
# tests/test_unit/test_recipes.py
class TestRecipeService:
    """食谱服务完整测试套件"""

    def test_get_recipes_by_constitution(self, db_session):
        """测试：根据体质获取推荐食谱"""
        from api.models import Recipe
        from api.services.recipe_service import RecipeService

        recipe = Recipe(
            name="山药红枣粥",
            type="粥类",
            suitable_constitutions=["qi_deficiency"]
        )
        db_session.add(recipe)
        db_session.commit()

        service = RecipeService()
        results = service.get_recipes_by_constitution("qi_deficiency", db_session)

        assert len(results) == 1
        assert results[0].name == "山药红枣粥"

    def test_get_recommendations_by_constitution(self, db_session):
        """测试：根据体质获取三餐推荐"""
        from api.models import Recipe
        from api.services.recipe_service import RecipeService

        recipes = [
            Recipe(name="山药粥", type="粥类", suitable_constitutions=["qi_deficiency"]),
            Recipe(name="山药汤", type="汤类", suitable_constitutions=["qi_deficiency"]),
        ]
        db_session.add_all(recipes)
        db_session.commit()

        service = RecipeService()
        result = service.get_recommendations_by_constitution("qi_deficiency", db_session)

        assert "recipes" in result
        assert "breakfast" in result["recipes"]
        assert "lunch" in result["recipes"]
        assert "dinner" in result["recipes"]
```

### 穴位服务完整测试

```python
# tests/test_unit/test_acupoints.py
class TestAcupointService:
    """穴位服务完整测试套件"""

    def test_get_acupoints_by_symptom(self, db_session):
        """测试：根据症状查找穴位"""
        from api.models import Acupoint, SymptomAcupoint
        from api.services.acupoint_service import AcupointService

        acupoint = Acupoint(
            name="神门",
            code="HT7",
            indications=["失眠", "心悸"]
        )
        db_session.add(acupoint)
        db_session.commit()

        symptom_acupoint = SymptomAcupoint(
            symptom_name="失眠",
            acupoint_id=acupoint.id,
            priority=10
        )
        db_session.add(symptom_acupoint)
        db_session.commit()

        service = AcupointService()
        results = service.get_acupoints_by_symptom("失眠", db_session)

        assert len(results) > 0
        assert results[0]["priority"] == 10

    def test_get_acupoints_by_meridian(self, db_session):
        """测试：根据经络获取穴位"""
        from api.models import Acupoint
        from api.services.acupoint_service import AcupointService

        acupoint = Acupoint(
            name="足三里",
            code="ST36",
            meridian="足阳明胃经"
        )
        db_session.add(acupoint)
        db_session.commit()

        service = AcupointService()
        results = service.get_acupoints_by_meridian("胃经", db_session)

        assert len(results) > 0
```

### 舌诊服务完整测试

```python
# tests/test_unit/test_tongue_diagnosis.py
class TestTongueDiagnosisService:
    """舌诊服务完整测试套件"""

    def test_analyze_tongue_qi_deficiency(self, db_session):
        """测试：气虚质舌象分析"""
        from api.services.tongue_service import TongueService

        service = TongueService()
        result = service.analyze_tongue(
            tongue_color="淡白",
            tongue_shape="胖大",
            coating_color="白苔",
            coating_thickness="薄苔",
            db=db_session
        )

        assert result["constitution_tendency"] == "qi_deficiency"
        assert result["confidence"] >= 70

    def test_analyze_tongue_yin_deficiency(self, db_session):
        """测试：阴虚质舌象分析"""
        from api.services.tongue_service import TongueService

        service = TongueService()
        result = service.analyze_tongue(
            tongue_color="红",
            tongue_shape="瘦薄",
            coating_color="黄苔",
            coating_thickness="薄苔",
            db=db_session
        )

        assert result["constitution_tendency"] == "yin_deficiency"

    def test_compare_with_test_consistent(self):
        """测试：舌诊与测试结果一致"""
        from api.services.tongue_service import TongueService

        service = TongueService()
        result = service.compare_with_test(
            tongue_constitution="qi_deficiency",
            test_constitution="qi_deficiency"
        )

        assert result["is_consistent"] is True
        assert "一致" in result["message"]

    def test_compare_with_test_inconsistent(self):
        """测试：舌诊与测试结果不一致"""
        from api.services.tongue_service import TongueService

        service = TongueService()
        result = service.compare_with_test(
            tongue_constitution="qi_deficiency",
            test_constitution="yin_deficiency"
        )

        assert result["is_consistent"] is False
        assert "不同" in result["message"]
```

### 课程服务完整测试

```python
# tests/test_unit/test_courses.py
class TestCourseService:
    """课程服务完整测试套件"""

    def test_get_courses_by_constitution(self, db_session):
        """测试：根据体质获取课程"""
        from api.models import Course
        from api.services.course_service import CourseService

        course = Course(
            title="气虚质调理指南",
            category="constitution",
            suitable_constitutions=["qi_deficiency"]
        )
        db_session.add(course)
        db_session.commit()

        service = CourseService()
        results = service.get_courses_by_constitution("qi_deficiency", db_session)

        assert len(results) == 1
        assert results[0].title == "气虚质调理指南"

    def test_get_courses_by_season_spring(self, db_session):
        """测试：获取春季养生课程"""
        from api.models import Course
        from api.services.course_service import CourseService

        course = Course(
            title="春季养肝正当时",
            category="season",
            subcategory="spring"
        )
        db_session.add(course)
        db_session.commit()

        service = CourseService()
        results = service.get_courses_by_season("spring", db_session)

        assert len(results) == 1
```

---

## 性能测试

### 使用 pytest-benchmark

```bash
pip install pytest-benchmark
```

```python
def test_get_ingredients_performance(self, db_session, benchmark):
    """性能测试：获取食材列表"""
    from api.models import Ingredient
    from api.services.ingredient_service import IngredientService

    # 创建 1000 个食材
    for i in range(1000):
        ingredient = Ingredient(name=f"食材{i}", category="药材")
        db_session.add(ingredient)
    db_session.commit()

    service = IngredientService()

    # 基准测试
    result = benchmark(
        service.get_ingredients_list,
        db_session, 0, 20
    )

    # 断言执行时间小于 100ms
    assert result is not None
```

### 使用 pytest-timeout

```bash
pip install pytest-timeout
```

```python
@pytest.mark.timeout(5)
def test_slow_operation(self, db_session):
    """测试：操作应在 5 秒内完成"""
    # 测试代码
    pass
```

---

## 最佳实践

### 1. AAA 模式

```python
def test_ingredient_service(db_session):
    """Arrange - 准备测试数据"""
    from api.models import Ingredient
    from api.services.ingredient_service import IngredientService

    ingredient = Ingredient(name="山药")
    db_session.add(ingredient)
    db_session.commit()

    """Act - 执行被测试的操作"""
    service = IngredientService()
    result = service.get_ingredient_by_id(ingredient.id, db_session)

    """Assert - 验证结果"""
    assert result is not None
    assert result.name == "山药"
```

### 2. 测试命名

```python
# 好的命名
def test_get_ingredient_by_id_success(db_session)
def test_get_ingredient_by_id_not_found(db_session)
def test_get_ingredients_by_constitution_empty_result(db_session)

# 不好的命名
def test_ingredient(db_session)
def test_1(db_session)
def test_success(db_session)
```

### 3. 使用描述性断言

```python
# 好的断言
assert result.name == "山药", f"Expected '山药', got '{result.name}'"
assert len(results) == 3, f"Expected 3 results, got {len(results)}"

# 不好的断言
assert result
assert results
```

### 4. 测试单一职责

```python
# 好的测试
def test_get_ingredient_by_id_success(db_session):
    """只测试成功获取的场景"""
    pass

def test_get_ingredient_by_id_not_found(db_session):
    """只测试不存在的场景"""
    pass

# 不好的测试
def test_get_ingredient_by_id(db_session):
    """测试了太多场景"""
    # 测试成功
    # 测试失败
    # 测试边界
    # 测试异常
```

### 5. 使用测试标记

```python
import pytest

@pytest.mark.unit
@pytest.mark.ingredients
def test_ingredient_service(db_session):
    pass

@pytest.mark.integration
@pytest.mark.api
def test_ingredient_api(client):
    pass

# 运行特定标记的测试
# pytest -m unit
# pytest -m "not slow"
```

---

## 运行测试

### 运行所有测试

```bash
cd backend
python -m pytest tests/test_unit/ tests/test_api/ -v
```

### 运行特定模块

```bash
# 食材模块
pytest tests/test_unit/test_ingredients.py tests/test_api/test_ingredients_api.py -v

# 舌诊模块
pytest tests/test_unit/test_tongue_diagnosis.py tests/test_api/test_tongue_diagnosis_api.py -v
```

### 生成覆盖率报告

```bash
# HTML 报告
pytest tests/ --cov=api --cov-report=html

# 在浏览器中查看
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### 只运行失败的测试

```bash
pytest --lf  # last-failed
```

### 并行运行测试

```bash
pip install pytest-xdist
pytest -n auto  # 使用所有 CPU 核心
```

---

## 故障排除

### 问题：数据库已存在

```bash
# 解决方案：删除测试数据库
rm backend/test.db
```

### 问题：导入错误

```bash
# 解决方案：设置 PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
# 或在 pytest.ini 中配置
```

### 问题：异步测试失败

```bash
# 安装异步支持
pip install pytest-asyncio

# 在测试文件中添加
@pytest.mark.asyncio
async def test_async_function():
    pass
```

---

**文档版本**: v1.0
**最后更新**: 2026-01-20
**相关文档**: [docs/testing.md](../testing.md)
