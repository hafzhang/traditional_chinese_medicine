# PRD: 中医养生菜谱功能

## 元数据
| 项目 | 值 |
|------|-----|
| **版本** | 18.0.0 (Enhanced Simplified) |
| **创建日期** | 2026-01-28 |
| **最后更新** | 2026-02-01 |
| **状态** | Active |
| **总故事数** | 32 |
| **已完成** | 0 |
| **数据源** | `source_data/dishes_list_ai_filled.xlsx` (12,785 条) |

---

## 1. 功能概述

### 1.1 数据源统计

| 字段 | 填充率 | 说明 |
|------|--------|------|
| title | 100% | 菜谱名称 |
| desc | 42.2% | 个人体验/简介 |
| tip | 45.4% | 烹饪贴士 |
| costtime | 83.3% | 烹饪时间 |
| difficulty | 100% | 难度等级 (AI填充) |
| suitable_constitutions | 100% | 适合体质 (AI填充) |
| avoid_constitutions | 100% | 禁忌体质 (AI填充) |
| efficacy_tags | 100% | 功效标签 (AI填充) |
| solar_terms | 100% | 节气标签 (AI填充) |

### 1.2 难度分布

| 难度 | 数量 | 占比 |
|------|------|------|
| 简单 (easy) | 6,114 | 47.8% |
| 中等 (medium) | 4,828 | 37.8% |
| 较难 (harder) | 1,635 | 12.8% |
| 困难 (hard) | 208 | 1.6% |

### 1.3 体质组合统计

| 适合体质组合 | 数量 | 占比 |
|-------------|------|------|
| 平和质单独 | 4,405 | 34.5% |
| 平和+气虚+阳虚 | 1,532 | 12.0% |
| 平和+气虚+阴虚 | 967 | 7.6% |
| 平和+气虚 | 863 | 6.8% |
| 平和+阳虚 | 661 | 5.2% |

### 1.4 核心字段映射

| Excel 列 | 数据库字段 | 类型 | 说明 |
|----------|-----------|------|------|
| title | name | VARCHAR(200) | 菜谱名称 |
| desc | desc | TEXT | 个人体验 |
| tip | tip | TEXT | 烹饪贴士 |
| costtime | cooking_time | INTEGER | 烹饪时间(分钟) |
| difficulty | difficulty | VARCHAR(20) | easy/medium/harder/hard |
| suitable_constitutions | suitable_constitutions | JSON | ["peace","qi_deficiency"] |
| avoid_constitutions | avoid_constitutions | JSON | ["phlegm_damp"] |
| efficacy_tags | efficacy_tags | JSON | ["健脾","养胃"] |
| solar_terms | solar_terms | JSON | ["立冬","小雪"] |
| steptext | → recipe_steps | 关联表 | 制作步骤 |
| QuantityIngredients | → recipe_ingredients | 关联表 | 食材清单 |

---

## 2. 分类体系

### 2.1 体质类型 (9种)

| 代码 | 名称 | 英文 | 特征 |
|------|------|------|------|
| peace | 平和质 | Peaceful | 阴阳气血调和 |
| qi_deficiency | 气虚质 | Qi Deficiency | 乏力、气短、自汗 |
| yang_deficiency | 阳虚质 | Yang Deficiency | 怕冷、手足不温 |
| yin_deficiency | 阴虚质 | Yin Deficiency | 口干、盗汗、手足心热 |
| phlegm_damp | 痰湿质 | Phlegm-Dampness | 体胖、身重、痰多 |
| damp_heat | 湿热质 | Damp-Heat | 面油、痤疮、口苦 |
| blood_stasis | 血瘀质 | Blood Stasis | 肤暗、痛经、易瘀 |
| qi_depression | 气郁质 | Qi Depression | 抑郁、胸闷、善太息 |
| special | 特禀质 | Special | 过敏、喷嚏、荨麻疹 |

### 2.2 节气分类 (四季)

#### 春季 (Spring)
| 节气 | 代码 | 养生重点 |
|------|------|----------|
| 立春 | lichun | 养肝护阳 |
| 雨水 | yushui | 调理脾胃 |
| 惊蛰 | jingzhe | 疏肝理气 |
| 春分 | chunfen | 平衡阴阳 |
| 清明 | qingming | 养肝明目 |
| 谷雨 | guyu | 健脾祛湿 |

#### 夏季 (Summer)
| 节气 | 代码 | 养生重点 |
|------|------|----------|
| 立夏 | lixia | 养心安神 |
| 小满 | xiaoman | 清热解暑 |
| 芒种 | mangzhong | 清补淡食 |
| 夏至 | xiazhi | 养阴护阳 |
| 小暑 | xiaoshu | 清心降火 |
| 大暑 | dashu | 清暑益气 |
| 长夏 | changxia | 健脾祛湿 |

#### 秋季 (Autumn)
| 节气 | 代码 | 养生重点 |
|------|------|----------|
| 立秋 | liqiu | 养肺润燥 |
| 处暑 | chushu | 润肺健脾 |
| 白露 | bailu | 养阴润燥 |
| 秋分 | qiufen | 平衡阴阳 |
| 寒露 | hanlu | 滋阴润肺 |
| 霜降 | shuangjiang | 气血调和 |

#### 冬季 (Winter)
| 节气 | 代码 | 养生重点 |
|------|------|----------|
| 立冬 | lidong | 养藏护阳 |
| 小雪 | xiaoxue | 温补益肾 |
| 大雪 | daxue | 补气养血 |
| 冬至 | dongzhi | 补阳护阴 |
| 小寒 | xiaohan | 温补肾阳 |
| 大寒 | dahan | 强身健体 |

#### 节日 (Festivals)
春节、元宵节、端午、七夕、中秋、重阳、除夕等

### 2.3 功效标签分类 (198种)

#### 补益类
补气、补血、补阴、补阳、补肝肾、补脾胃、补肺、补肾

#### 养生类
健脾、养胃、养肺、养肝、养心、养肾、养血、养阴

#### 清热类
清热、清心、清肝、清肺、清暑、泻火

#### 祛邪类
祛湿、祛痰、祛风、祛寒、化痰、散寒

#### 理气类
理气、疏肝、行气、解郁、宽中

#### 活血类
活血、化瘀、通络

#### 消食类
消食、助消化、健胃、开胃

#### 安神类
安神、养心、宁心

---

## 3. 实施阶段

```
┌─────────────────────────────────────────────────────────────────┐
│  Phase 1: 数据模型 (US-001~004)     ──┐                         │
│  Phase 2: 导入配置 (US-005~006)     ──┤                         │
│  Phase 3: 导入脚本 (US-007~010)     ──┼─→ 后端基础              │
│  Phase 4: 服务层 (US-011~014)       ──┤                         │
│  Phase 5: API路由 (US-015~018)      ──┘                         │
│  Phase 6: 前端页面 (US-019~023)     ──→ 用户界面                │
│  Phase 7: 导入数据 (US-024~026)     ──→ 数据导入                │
│  Phase 8: 验收测试 (US-027~032)     ──→ 质量保证                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. 用户故事

### Phase 1: 数据模型 (4个故事)

#### US-001: Recipe 模型与索引
**目标**: 创建 Recipe ORM 模型，包含字段和索引

**文件**: `backend/api/models/__init__.py`

**验收标准**:
| 项目 | 要求 |
|------|------|
| 表名 | recipes |
| 字段 | id, name, desc, tip, cooking_time, difficulty, suitable_constitutions(JSON), avoid_constitutions(JSON), efficacy_tags(JSON), solar_terms(JSON), cover_image, created_at, updated_at |
| 索引 | idx_name(唯一), idx_difficulty, idx_cooking_time, idx_created_at |
| 质量检查 | Typecheck passes |

**依赖**: 无

---

#### US-002: RecipeIngredient 和 RecipeStep 关联表
**目标**: 创建食材和步骤的关联表

**文件**: `backend/api/models/__init__.py`

**验收标准**:
| 项目 | 要求 |
|------|------|
| RecipeIngredient | id, recipe_id, ingredient_id, amount, is_primary |
| RecipeStep | id, recipe_id, step_number, description |
| 复合唯一索引 | (recipe_id, ingredient_id), (recipe_id, step_number) |
| relationship | Recipe → ingredients, Recipe → steps |

**依赖**: 无

---

#### US-003: Recipe Schema 类
**目标**: 创建 Pydantic 验证模型

**文件**: `backend/api/schemas/recipe.py`

**验收标准**:
| 类 | 用途 |
|------|------|
| RecipeBase | 基础字段，difficulty 验证 easy\|medium\|harder\|hard |
| RecipeCreate | 创建请求 |
| RecipeUpdate | 更新请求，所有字段可选 |
| RecipeResponse | 完整响应 |
| RecipeListItem | 列表简化视图 |
| RecipeListResponse | {total, page, page_size, items} |

**依赖**: 无

---

#### US-004: 数据库表创建
**目标**: 创建数据库表

**说明**: 项目使用 SQLite，不使用 Alembic

**验收**: 通过 `Base.metadata.create_all()` 创建表

---

### Phase 2: 导入配置 (2个故事)

#### US-005: 导入配置常量与解析函数
**目标**: 创建导入配置文件

**文件**: `backend/scripts/recipe_import_config.py`

**验收标准**:
```python
# 常量定义
EXCEL_COLUMN_MAP = {'title': 'name', 'costtime': 'cooking_time'}
DIFFICULTY_MAP = {'简单': 'easy', '中等': 'medium', '较难': 'harder', '困难': 'hard'}
SOLAR_TERMS = ['立春','雨水','惊蛰','春分','清明','谷雨','立夏','小满','芒种','夏至','小暑','大暑','长夏','立秋','处暑','白露','秋分','寒露','霜降','立冬','小雪','大雪','冬至','小寒','大寒']
SEASON_MAP = {
    '春季': ['立春','雨水','惊蛰','春分','清明','谷雨'],
    '夏季': ['立夏','小满','芒种','夏至','小暑','大暑','长夏'],
    '秋季': ['立秋','处暑','白露','秋分','寒露','霜降'],
    '冬季': ['立冬','小雪','大雪','冬至','小寒','大寒']
}

# 解析函数
parse_cooking_time(value) -> Optional[int]  # "30分钟"→30, "1小时"→60
parse_difficulty(value) -> Optional[str]     # "简单"→"easy"
parse_json_field(value) -> Optional[List[str]]  # JSON字符串解析
```

---

#### US-006: 食材与步骤解析函数
**目标**: 实现食材和步骤解析

**文件**: `backend/scripts/recipe_import_config.py`

**验收标准**:
```python
parse_ingredients(text: str) -> List[Dict[str, Any]]
# 输入: "山药50g,小米100克"
# 输出: [{'name': '山药', 'amount': '50g'}, {'name': '小米', 'amount': '100克'}]

parse_steps(text: str) -> List[Dict[str, Any]]
# 输入: "步骤1:准备食材\n步骤2:开始烹饪"
# 输出: [{'step_number': 1, 'description': '准备食材'}, ...]
```

---

### Phase 3: 导入脚本 (4个故事)

#### US-007: 导入脚本基础结构
**目标**: 创建导入脚本主文件

**文件**: `backend/scripts/import_recipes.py`

**验收标准**:
| 参数 | 说明 |
|------|------|
| --file | Excel 文件路径 (必需) |
| --limit | 限制导入数量 (可选) |
| --dry-run | 干运行模式 (可选) |
| --verbose | 详细输出 (可选) |

---

#### US-008: Excel 读取与去重
**目标**: 实现 Excel 文件读取和去重检查

**文件**: `backend/scripts/import_recipes.py`

**验收标准**:
```python
read_excel_file(file_path: str, limit: Optional[int]) -> List[Dict]
check_recipe_exists(name: str, db: Session) -> bool
```

---

#### US-009: 单条与批量导入
**目标**: 实现导入核心逻辑

**文件**: `backend/scripts/import_recipes.py`

**验收标准**:
```python
get_or_create_ingredient(name: str, db: Session) -> Ingredient
import_single_recipe(row: Dict, db: Session) -> Optional[Recipe]
import_recipes(file_path: str, limit: Optional[int], dry_run: bool) -> Dict
# 返回: {total: N, success: X, skipped: Y, failed: Z}
```

---

#### US-010: 干运行与失败导出
**目标**: 添加测试辅助功能

**文件**: `backend/scripts/import_recipes.py`

**验收标准**:
```python
dry_run_import(file_path: str, limit: Optional[int]) -> None
export_failed_recipes(failed: List[Dict], output_path: str) -> None
```

---

### Phase 4: 服务层 (4个故事)

#### US-011: RecipeService 基础与查询方法
**目标**: 创建服务层和基础查询

**文件**: `backend/api/services/recipe_service.py`

**验收标准**:
```python
class RecipeService:
    def get_recipes(
        page: int, page_size: int,
        constitution: Optional[str],  # 体质筛选
        efficacy: Optional[str],       # 功效筛选
        difficulty: Optional[str],     # 难度筛选
        solar_term: Optional[str],     # 节气筛选
        season: Optional[str],         # 季节筛选
        db: Session
    ) -> Dict[str, Any]

    def get_recipe_by_id(id: int, db: Session) -> Optional[Recipe]
```

---

#### US-012: 搜索与推荐方法
**目标**: 实现搜索和推荐功能

**文件**: `backend/api/services/recipe_service.py`

**验收标准**:
```python
def search_recipes(
    keyword: str, page: int, page_size: int,
    constitution: Optional[str], difficulty: Optional[str],
    db: Session
) -> Dict[str, Any]
# 搜索范围: name, ingredients, efficacy_tags

def get_recommendations_by_constitution(
    constitution: str, limit: int, db: Session
) -> List[Recipe]
# 优先返回适合该体质，排除禁忌体质
```

---

#### US-013: 错误处理与日志
**目标**: 完善服务层质量

**文件**: `backend/api/services/recipe_service.py`

**验收标准**: 参数验证、异常处理、日志记录

---

#### US-014: 服务层工厂函数
**目标**: 创建服务实例工厂

**文件**: `backend/api/services/recipe_service.py`

**验收标准**:
```python
def get_recipe_service() -> RecipeService
```

---

### Phase 5: API 路由 (4个故事)

#### US-015: API 路由基础与列表接口
**目标**: 创建 API 路由和列表接口

**文件**: `backend/api/routers/recipes.py`

**验收标准**:
```python
router = APIRouter(prefix='/api/v1/recipes', tags=['recipes'])

@router.get('', response_model=StandardResponse[RecipeListResponse])
# 查询参数: page, page_size, constitution, efficacy, difficulty, solar_term, season
```

---

#### US-016: 详情、搜索、推荐接口
**目标**: 实现核心查询接口

**文件**: `backend/api/routers/recipes.py`

**验收标准**:
```python
@router.get('/{id}', response_model=StandardResponse[RecipeResponse])
@router.get('/search', response_model=StandardResponse[RecipeListResponse])
@router.get('/recommendations', response_model=StandardResponse[List[RecipeListItem]])
```

---

#### US-017: API 错误处理
**目标**: 统一错误处理

**文件**: `backend/api/routers/recipes.py`

**验收标准**: 返回格式 `{code: -1, message: '...'}`

---

#### US-018: API 日志
**目标**: 添加请求日志

**文件**: `backend/api/routers/recipes.py`

**验收标准**: 记录请求参数、响应状态、处理时间

---

### Phase 6: 前端页面 (5个故事)

#### US-019: 首页食谱库卡片
**目标**: 添加首页功能入口

**文件**: `frontend/src/pages/index.vue`

**验收标准**:
- 图标🍲, 标题"食谱库"
- 描述: "根据体质推荐的养生食谱和食疗方案"
- 按钮: "进入食谱"
- 跳转: `/pages/recipes/list`

---

#### US-020: 列表页面结构
**目标**: 创建列表页基础结构

**文件**: `frontend/src/pages/recipes/list.vue`

**验收标准**:
- 顶部导航: 返回按钮 + 标题"食谱库"
- 筛选器区域: 横向滚动
- 菜谱列表区域
- 加载状态和空状态

---

#### US-021: 列表页筛选与卡片
**目标**: 实现筛选器和菜谱卡片

**文件**: `frontend/src/pages/recipes/list.vue`

**验收标准**:
| 筛选器 | 选项 |
|--------|------|
| 体质 | 9种体质标签 |
| 季节 | 春季、夏季、秋季、冬季 |
| 难度 | 简单、中等、较难、困难 |

菜谱卡片:
- 封面图 (有图显示/无图占位)
- 菜谱名称
- 难度标签: easy=绿, medium=橙, hard=红
- 功效标签 (前3个)
- 点击跳转详情

---

#### US-022: 详情页面结构
**目标**: 创建详情页基础结构

**文件**: `frontend/src/pages/recipes/detail.vue`

**验收标准**:
- 顶部导航: 返回 + 分享
- 封面图区域
- 基本信息: 名称 + 时间 + 难度
- 内容区域: desc、tip、体质、功效、食材、步骤

---

#### US-023: 详情页内容与API客户端
**目标**: 完善详情页内容

**文件**: `frontend/src/pages/recipes/detail.vue`, `frontend/src/api/recipes.js`

**验收标准**:
| 区域 | 样式 | 内容 |
|------|------|------|
| desc | 蓝色背景 #e3f2fd | 个人体验 |
| tip | 黄色背景 #fff9c4 | 烹饪贴士 |
| 体质 | 适合(绿) + 禁忌(红) | 中文名称 |
| 功效 | 标签云 | 可点击筛选 |
| 食材 | 可展开折叠 | 名称 + 用量 |
| 步骤 | 序号显示 | 描述文本 |

API 客户端函数:
```javascript
getRecipes(params)
getRecipeById(id)
searchRecipes(params)
getRecommendations(constitution)
```

---

### Phase 7: 导入数据 (3个故事)

#### US-024: 干运行测试
**目标**: 测试导入功能

**命令**:
```bash
python scripts/import_recipes.py --file ../source_data/dishes_list_ai_filled.xlsx --dry-run --limit 100
```

**验收**: 抽样检查10条输出

---

#### US-025: 正式导入数据
**目标**: 导入全部菜谱数据

**命令**:
```bash
python scripts/import_recipes.py --file ../source_data/dishes_list_ai_filled.xlsx
```

**验收标准**:
| 指标 | 目标 |
|------|------|
| 总菜谱数 | > 12,500 (98%+) |
| difficulty | 100% |
| suitable_constitutions | ≥ 80% |
| efficacy_tags | ≥ 80% |
| 失败率 | < 2% |

---

#### US-026: 智能字段质量验证
**目标**: 验证 AI 填充字段质量

**验收标准**:
| 指标 | 目标 |
|------|------|
| difficulty 分布 | 简单47%, 中等38%, 较难13%, 困难2% |
| 平和质占比 | > 70% |
| efficacy_tags 多样性 | > 10 种 |
| 四季分布 | 相对均衡 |

---

### Phase 8: 验收测试 (6个故事)

#### US-027: 后端字段完整性测试
**目标**: 验证数据库字段完整性

**验收**: difficulty 100%, 体质≥80%, 功效≥80%

---

#### US-028: API 字段测试
**目标**: 验证 API 返回字段

**验收**: 返回 cooking_time, cover_image, difficulty, code=0

---

#### US-029: 功能入口测试
**目标**: 验证前端功能入口

**验收**: 首页卡片显示，点击跳转列表页

---

#### US-030: 列表页功能测试
**目标**: 验证列表页功能

**验收**: 筛选器工作、卡片跳转、下拉刷新、滚动加载

---

#### US-031: 详情页功能测试
**目标**: 验证详情页功能

**验收**: 封面图、desc/tip 背景、体质中文、食材展开

---

#### US-032: 完整流程测试
**目标**: 验证完整用户流程

**验收**: 首页 → 列表页 → 筛选 → 详情页 → 返回 → 搜索 → 详情

---

## 5. 附录

### 5.1 体质类型

| 代码 | 名称 | 英文 |
|------|------|------|
| peace | 平和质 | Peaceful |
| qi_deficiency | 气虚质 | Qi Deficiency |
| yang_deficiency | 阳虚质 | Yang Deficiency |
| yin_deficiency | 阴虚质 | Yin Deficiency |
| phlegm_damp | 痰湿质 | Phlegm-Dampness |
| damp_heat | 湿热质 | Damp-Heat |
| blood_stasis | 血瘀质 | Blood Stasis |
| qi_depression | 气郁质 | Qi Depression |
| special | 特禀质 | Special |

### 5.2 难度等级

| 代码 | 中文 | 占比 |
|------|------|------|
| easy | 简单 | 47.8% |
| medium | 中等 | 37.8% |
| harder | 较难 | 12.8% |
| hard | 困难 | 1.6% |

### 5.3 质量门禁

```bash
# Typecheck
cd backend && python -m mypy api/

# Tests
cd backend && python -m pytest tests/ -v

# Coverage
cd backend && python -m pytest tests/ --cov=api --cov-report=term-missing

# Target: ≥80%
```

### 5.4 API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/recipes | 菜谱列表 |
| GET | /api/v1/recipes/{id} | 菜谱详情 |
| GET | /api/v1/recipes/search | 搜索菜谱 |
| GET | /api/v1/recipes/recommendations | 体质推荐 |

### 5.5 前端路由

| 路由 | 页面 | 说明 |
|------|------|------|
| /pages/index | 首页 | 功能入口 |
| /pages/recipes/list | 列表页 | 菜谱列表 |
| /pages/recipes/detail | 详情页 | 菜谱详情 |

### 5.6 开发分支指南

本 PRD 使用 `feat/prd-recipes-enhancement` 分支进行开发。

#### 分支管理

```bash
# 切换到开发分支
git checkout feat/prd-recipes-enhancement

# 如果分支不存在，创建新分支
git checkout -b feat/prd-recipes-enhancement

# 查看当前分支
git branch

# 查看分支状态
git status
```

#### 提交规范

```bash
# 提交格式
git commit -m "feat: US-XXX - 描述内容"

# 示例
git commit -m "feat: US-001 - 创建 Recipe 模型与索引"
git commit -m "feat: US-005 - 导入配置常量与解析函数"
```

#### Pull Request 流程

```bash
# 1. 确保所有测试通过
cd backend && python -m pytest tests/ -v

# 2. 运行 typecheck
cd backend && python -m mypy api/

# 3. 检查测试覆盖率
cd backend && python -m pytest tests/ --cov=api --cov-report=term-missing

# 4. 推送到远程分支
git push origin feat/prd-recipes-enhancement

# 5. 创建 Pull Request 到 master 分支
```

#### PR 描述模板

```markdown
## 概述

实现了 US-XXX: {用户故事标题}

## 更改内容

- 更改点 1
- 更改点 2
- ...

## 测试

- 单元测试: 通过 (X 个测试)
- API 测试: 通过
- 手动测试: 已验证

## 截图

(如适用)

## 检查清单

- [ ] 所有测试通过
- [ ] Typecheck 通过
- [ ] 测试覆盖率 >= 80%
- [ ] 代码符合项目规范
```

#### 合并前检查

- [ ] 所有 User Story 验收标准已满足
- [ ] 单元测试通过
- [ ] API 测试通过
- [ ] 前端功能在浏览器中验证通过
- [ ] 测试覆盖率 >= 80%
- [ ] Typecheck 无错误
