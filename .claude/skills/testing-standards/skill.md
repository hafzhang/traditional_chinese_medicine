# id: testing-standards
# name: 测试规范与模板
# description: 提供项目测试命名规范、服务层/API测试结构、覆盖率目标的标准化能力
# version: 1.0.0
# author: Claude Code
# tags: [testing, pytest, coverage, standards]

---

## 测试规范与模板 Skill

### 项目测试现状

- **测试框架**: Pytest
- **测试覆盖率**: 83%（Phase 1）
- **目标覆盖率**: 80%+
- **数据库**: 内存 SQLite（测试时自动回滚）

---

### 目录结构

```
backend/tests/
├── conftest.py                   # Pytest fixtures（db_session, client）
├── test_unit/                    # 服务层单元测试
│   ├── test_ingredients.py
│   ├── test_recipes.py
│   ├── test_acupoints.py
│   ├── test_tongue_diagnosis.py
│   └── test_courses.py
└── test_api/                     # API 集成测试
    ├── test_ingredients_api.py
    ├── test_recipes_api.py
    ├── test_acupoints_api.py
    ├── test_tongue_diagnosis_api.py
    └── test_courses_api.py
```

---

### 命名规范

#### 文件命名
```
# 单元测试
tests/test_unit/test_{module}.py
# 示例: test_ingredients.py, test_acupoints.py

# API 测试
tests/test_api/test_{module}_api.py
# 示例: test_ingredients_api.py, test_acupoints_api.py
```

#### 测试类命名
```python
# 服务层测试
class Test{ServiceName}Service:
    pass
# 示例: class TestIngredientService, class TestAcupointService

# API 测试
class Test{ModuleName}API:
    pass
# 示例: class TestIngredientsAPI, class TestAcupointsAPI
```

#### 测试方法命名
```python
def test_{action}_{scenario}():
    pass

# 示例:
def test_get_ingredient_by_id_success():
    """成功获取食材"""

def test_get_ingredient_by_id_not_found():
    """获取不存在的食材"""

def test_get_ingredients_by_constitution_invalid_code():
    """使用无效体质代码查询"""
```

---

### Fixtures (conftest.py)

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from api.database import Base, get_db
from main import app

# 内存 SQLite 数据库
TEST_DATABASE_URL = "sqlite:///:memory:"

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
        session.rollback()
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
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
```

---

### 单元测试模板

```python
import pytest
from api.services.ingredient_service import IngredientService

class TestIngredientService:

    def test_get_ingredient_by_id_success(self, db_session):
        """成功获取食材"""
        # Arrange: 创建测试数据
        ingredient = Ingredient(
            name="山药",
            suitable_constitutions=["qi_deficiency"]
        )
        db_session.add(ingredient)
        db_session.commit()

        # Act: 执行测试
        service = IngredientService()
        result = service.get_ingredient_by_id(ingredient.id, db_session)

        # Assert: 验证结果
        assert result is not None
        assert result.name == "山药"
        assert "qi_deficiency" in result.suitable_constitutions

    def test_get_ingredient_by_id_not_found(self, db_session):
        """获取不存在的食材"""
        service = IngredientService()
        result = service.get_ingredient_by_id(999, db_session)
        assert result is None

    def test_is_valid_constitution_code_valid(self, db_session):
        """验证有效的体质代码"""
        service = IngredientService()
        assert service.is_valid_constitution_code("qi_deficiency") is True

    def test_is_valid_constitution_code_invalid(self, db_session):
        """验证无效的体质代码"""
        service = IngredientService()
        assert service.is_valid_constitution_code("invalid_code") is False
```

---

### API 测试模板

```python
import pytest
from fastapi import status

class TestIngredientsAPI:

    def test_get_ingredient_by_id_success(self, client, db_session):
        """成功获取食材"""
        # Arrange: 创建测试数据
        ingredient = Ingredient(name="山药")
        db_session.add(ingredient)
        db_session.commit()

        # Act: 发送请求
        response = client.get(f"/api/ingredients/{ingredient.id}")

        # Assert: 验证响应
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["name"] == "山药"

    def test_get_ingredient_by_id_not_found(self, client, db_session):
        """获取不存在的食材"""
        response = client.get("/api/ingredients/999")
        assert response.status_code == status.HTTP_404_NOT_NOT

    def test_get_ingredients_by_constitution_success(self, client, db_session):
        """成功按体质查询食材"""
        # Arrange: 创建测试数据
        ingredient1 = Ingredient(
            name="山药",
            suitable_constitutions=["qi_deficiency"]
        )
        ingredient2 = Ingredient(
            name="山楂",
            suitable_constitutions=["phlegm_damp"]
        )
        db_session.add_all([ingredient1, ingredient2])
        db_session.commit()

        # Act
        response = client.get("/api/ingredients/by-constitution?qi_deficiency")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["code"] == 0
        assert len(data["data"]["recommended"]) == 1
        assert data["data"]["recommended"][0]["name"] == "山药"
```

---

### 常用命令

```bash
cd backend

# 运行所有测试
python -m pytest tests/ -v

# 运行特定模块
python -m pytest tests/test_unit/test_ingredients.py \
                 tests/test_api/test_ingredients_api.py -v

# 运行单个测试
python -m pytest tests/test_unit/test_ingredients.py::TestIngredientService::test_get_ingredient_by_id_success -v

# 生成覆盖率报告
python -m pytest tests/test_unit/ tests/test_api/ \
    --cov=api \
    --cov-report=term-missing

# 生成 HTML 覆盖率报告
python -m pytest tests/test_unit/ tests/test_api/ \
    --cov=api \
    --cov-report=html
# 在浏览器中打开 htmlcov/index.html
```

---

### 测试数据管理

```python
# 创建测试数据的辅助方法
def create_test_ingredient(db_session, **kwargs):
    """创建测试食材"""
    defaults = {
        "name": "测试食材",
        "category": "蔬菜",
        "nature": "平",
        "taste": "甘",
        "suitable_constitutions": ["peace"],
        "avoid_constitutions": [],
        "aliases": []
    }
    defaults.update(kwargs)
    ingredient = Ingredient(**defaults)
    db_session.add(ingredient)
    db_session.commit()
    db_session.refresh(ingredient)
    return ingredient
```

---

### 覆盖率目标

| 模块 | 最低覆盖率 | 当前状态 |
|------|-----------|---------|
| Ingredient Service | 80% | 100% |
| Recipe Service | 80% | ? |
| Acupoint Service | 80% | ? |
| Tongue Service | 80% | 100% |
| Course Service | 80% | ? |
| **总体** | **80%** | **83%** |

---

### 开发检查清单

编写新功能测试时：
- [ ] 单元测试放在 `tests/test_unit/test_{module}.py`
- [ ] API 测试放在 `tests/test_api/test_{module}_api.py`
- [ ] 测试类使用 `Test{ServiceName}Service` 或 `Test{ModuleName}API`
- [ ] 测试方法使用 `test_{action}_{scenario}` 命名
- [ ] 使用 `db_session` fixture 获取数据库会话
- [ ] 使用 `client` fixture 进行 API 测试
- [ ] 遵循 Arrange-Act-Assert 模式
- [ ] 确保事务不会提交（自动回滚）
- [ ] 运行 `--cov=api` 检查覆盖率

提交前：
- [ ] 运行 `python -m pytest tests/test_unit/ tests/test_api/ -v`
- [ ] 确保所有测试通过
- [ ] 确保覆盖率 >= 80%
