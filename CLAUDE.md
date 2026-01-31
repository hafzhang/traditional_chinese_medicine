
# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此代码仓库中工作时提供指导。

---

## 项目概述

这是一个**中医养生平台**，基于 CCMQ 标准（王琦院士9种体质标准量表）提供体质识别和个性化养生建议。系统包括：

- **后端**: FastAPI + SQLAlchemy + PostgreSQL（测试环境使用 SQLite）
- **前端**: uni-app (Vue 3)，支持微信小程序、抖音小程序和 H5
- **核心功能**: 30题体质测试，提供个性化食材/穴位/课程推荐

---

## 架构设计

### 目录结构

```
backend/
├── main.py                          # 应用入口
├── api/
│   ├── config.py                    # 配置管理（基于环境变量）
│   ├── database.py                  # 数据库连接与会话管理
│   ├── models/__init__.py          # SQLAlchemy ORM 模型（User, ConstitutionResult, Ingredient, Recipe, Acupoint, Course 等）
│   ├── schemas/                     # Pydantic 验证模型
│   ├── services/                    # 业务逻辑层（无状态服务）
│   ├── routers/                     # FastAPI 路由处理器（瘦控制器）
│   └── data/                        # 静态数据（问题、体质信息）
└── tests/
    ├── conftest.py                   # Pytest fixtures（db_session, client）
    ├── test_unit/                    # 服务层单元测试
    └── test_api/                     # API 集成测试

frontend/src/
├── pages/                            # uni-app 页面（index, test, result, detail, ingredients, recipes, acupoints, courses）
├── api/                              # API 客户端封装
└── utils/                            # 工具函数
```

### 服务层模式

服务是**无状态**类（不是单例，尽管存在 `get_*_service()` 函数）。每个服务方法：
- 将 `db: Session` 作为必需参数
- 返回领域对象或字典
- 包含业务逻辑和验证

**示例：**
```python
service = IngredientService()
ingredients = service.get_ingredients_by_constitution("qi_deficiency", db)
```

### 体质类型（9种）

| 代码 | 名称 | 英文名称 |
|------|------|---------|
| peace | 平和质 | Peaceful |
| qi_deficiency | 气虚质 | Qi Deficiency |
| yang_deficiency | 阳虚质 | Yang Deficiency |
| yin_deficiency | 阴虚质 | Yin Deficiency |
| phlegm_damp | 痰湿质 | Phlegm-Dampness |
| damp_heat | 湿热质 | Damp-Heat |
| blood_stasis | 血瘀质 | Blood Stasis |
| qi_depression | 气郁质 | Qi Depression |
| special | 特禀质 | Special |

**验证方式**: 服务通过 `is_valid_constitution_code()` 方法验证体质代码。

### Phase 1 功能

当前已实现（测试覆盖率 83%）：
- **食材库** (`api/services/ingredient_service.py`): 基于体质推荐的食物库
- **食谱库** (`api/services/recipe_service.py`): 支持餐次筛选的食谱库
- **穴位查找** (`api/services/acupoint_service.py`): 按症状/部位/经络查找穴位
- **AI舌诊** (`api/services/tongue_service.py`): 基于规则的舌象分析与体质映射
- **养生课程** (`api/services/course_service.py`): 按体质分类的健康课程

---

## 常用命令

### 后端开发

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
python main.py
# 服务运行在 http://localhost:8000
# API 文档位于 http://localhost:8000/docs

# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试模块
python -m pytest tests/test_unit/test_ingredients.py tests/test_api/test_ingredients_api.py -v

# 运行测试并生成覆盖率报告
python -m pytest tests/test_unit/ tests/test_api/ --cov=api --cov-report=term-missing

# 运行单个测试文件
python -m pytest tests/test_unit/test_tongue_diagnosis.py -v

# 运行特定测试用例
python -m pytest tests/test_unit/test_tongue_diagnosis.py::TestTongueDiagnosisService::test_analyze_tongue_qi_deficiency -v
```

### 数据库操作

```bash
# 初始化/填充数据库
cd backend
python scripts/seed_db.py

# 或使用 Alembic 迁移（如果已配置）
alembic upgrade head
```

### 前端开发

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 开发模式（H5）
npm run dev:h5

# 开发模式（微信小程序、抖音小程序）
npm run dev:mp-weixin

# 构建
npm run build:h5
npm run build:mp-weixin
```

### E2E 测试 (Playwright)

```bash
# 进入前端目录
cd frontend

# 运行所有 E2E 测试
npx playwright test

# 运行特定测试文件
npx playwright test 01-navigation

# 运行特定项目
npx playwright test --project=chromium
npx playwright test --project=API

# 运行测试并显示 UI 模式
npx playwright test --ui

# 查看测试报告
npx playwright show-report

# 安装 Playwright 浏览器（首次运行或更新后）
npx playwright install chromium
```

**重要提示**:
- E2E 测试需要后端服务器运行在 `http://localhost:8000`
- API 测试项目使用 HTTP 请求，不依赖浏览器
- 测试配置文件: `frontend/playwright.config.ts`
- 测试文件目录: `frontend/tests/e2e/recipes/`

---

## 重要架构说明

### 1. SQLite 中的 JSON 列

项目使用 SQLite 进行测试。JSON 列（如 `aliases`、`suitable_constitutions`）可以工作，但：
- **搜索限制**: 对 JSON 列的 `LIKE` 查询可能无法按预期工作
- **替代方案**: 对 JSON 数组查询使用 `.contains()`

```python
# 在 JSON 数组中搜索的正确方式
query.filter(Ingredient.suitable_constitutions.contains("qi_deficiency"))
```

### 2. 数据库会话管理

测试使用内存 SQLite 数据库。`db_session` fixture：
- 在每个测试前创建所有表
- 在每个测试后回滚事务
- 测试完成后删除所有表

**切勿提交测试事务** - 它们会自动回滚。

### 3. 舌诊评分系统

舌诊使用加权评分系统：
- `tongue_color`: 30 分
- `tongue_shape`: 35 分
- `coating_color`: 20 分
- `coating_thickness`: 15 分

总计：每种体质匹配 100 分。

**重要提示**: `yang_deficiency` 和 `phlegm_damp` 通过使用不同的 `coating_thickness` 值（"腻苔" vs "厚苔"）进行区分。

### 4. 响应格式标准

所有 API 响应遵循此格式：

```python
# 成功
{
    "code": 0,
    "data": {...},
    "message": "Success"  # 可选
}

# 错误
{
    "code": -1,
    "message": "错误描述"
}
```

### 5. 测试命名规范

- 单元测试: `tests/test_unit/test_{module}.py` (例如 `test_ingredients.py`)
- API 测试: `tests/test_api/test_{module}_api.py` (例如 `test_ingredients_api.py`)
- 测试类: `Test{ServiceName}Service` 或 `Test{ModuleName}API`
- 测试方法: `test_{action}_{scenario}` (例如 `test_get_ingredient_by_id_not_found`)

### 6. Phase 1 测试状态

- **测试**: 109 个测试通过（仅 Phase 1）
- **覆盖率**: 总体 83%（目标: 80%+）
- **食材服务**: 100% 覆盖率（从 67% 提升）
- **舌诊服务**: 100% 覆盖率

---

## 模块特定说明

### 舌诊 (`api/services/tongue_service.py`)

- **基于规则**: 无 AI 模型，使用 `CONSTITUTION_TONGUE_MAP` 进行匹配
- **特征选择**: 用户手动选择舌象特征（尚未实现图像分析）
- **对比功能**: 可将舌诊结果与问卷测试结果进行对比

### 体质评分 (`api/services/constitution.py`)

- **公式**: `原始分 × 2.5 = 百分制分数`
- **平和质判定**: ≥60分 且其他 8 种体质均 < 40 分
- **主要体质**: 分数最高的体质
- **次要体质**: ≥30 分的其他体质

### 食材与食谱

- 两者都使用 `suitable_constitutions` JSON 字段进行筛选
- `get_recommendation_by_constitution()` 同时返回推荐和禁忌项目
- 别名以 JSON 数组形式存储，例如 `["怀山药", "淮山"]`

### 穴位

- 使用 `SymptomAcupoint` 关联表进行 症状→穴位映射
- `priority` 字段决定搜索结果中的排序
- 部位和经络有专用的列表端点

---

## 已知问题与限制

1. **体质 API 异步问题**: 旧的体质测试 API 有 9 个测试失败（异步上下文问题） - 不属于 Phase 1
2. **前端测试**: 尚未配置（vitest 环境待配置）
3. **食材搜索**: SQLite 中 JSON 字段搜索受限 - 建议使用名称搜索

---

## 开发工作流

### 添加新的 Phase 1 功能

1. 在 `api/models/__init__.py` 中创建模型
2. 在 `api/services/{feature}_service.py` 中创建服务
3. 在 `api/routers/{feature}.py` 中创建路由
4. 在 `main.py` 中注册路由
5. 在 `tests/test_unit/test_{feature}.py` 中添加单元测试
6. 在 `tests/test_api/test_{feature}_api.py` 中添加 API 测试
7. 如需要，更新 `conftest.py` 中的 fixtures

### 提交前运行测试

```bash
cd backend
python -m pytest tests/test_unit/ tests/test_api/ -v --tb=short
```

### 生成覆盖率报告

```bash
python -m pytest tests/test_unit/ tests/test_api/ --cov=api --cov-report=html
# 在浏览器中打开 htmlcov/index.html
```

---

## 文件路径参考

- **后端根目录**: `backend/`
- **前端根目录**: `frontend/`
- **测试目录**: `backend/tests/`
- **API 路由**: `backend/api/routers/*.py`
- **服务层**: `backend/api/services/*.py`
- **模型**: `backend/api/models/__init__.py`
- **文档**: `docs/`
- **Phase 1 文档**: `docs/phase1_*.md`

---

## 体质数据结构

```python
# 9种体质及其特征
CONSTITUTION_INFO = {
    "qi_deficiency": {
        "name": "气虚质",
        "regulation": {
            "diet": ["多吃补气健脾食物"],
            "lifestyle": ["避免过度劳累"]
        }
    },
    # ... 等
}
```

访问方式: `from api.data.constitution_info import CONSTITUTION_INFO`
