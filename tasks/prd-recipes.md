# PRD: 中医养生菜谱功能 (Excel导入版)

## 元数据
- **创建日期**: 2026-01-28
- **版本**: 12.0.0
- **作者**: Claude Code
- **状态**: Active (In Progress)
- **最后更新**: 2026-01-31
- **PRD JSON**: `tasks/prd-recipes.json` (AI Agent 可执行格式)
- **Ralph 分支**: `ralph/recipe-database-import`

### 进度概览
| 指标 | 数值 | 百分比 |
|------|------|--------|
| 总故事数 | 75 | 100% |
| 已完成 | 32 | 43% |
| 进行中 | 0 | 0% |
| 待完成 | 43 | 57% |

### 实现阶段
- ✅ **Phase 1**: 数据模型 (US-001~008) - **已完成**
- ✅ **Phase 2**: 导入配置基础 (US-009~014) - **已完成**
- ✅ **Phase 3**: 导入解析函数 - 已包含在 Phase 2
- ✅ **Phase 4**: 导入脚本核心 (US-015~022) - **已完成**
- ✅ **Phase 5**: 服务层 (US-023~031) - **已完成**
- ⏳ **Phase 6**: 数据库迁移 - **待完成** (US-006)
- ⏳ **Phase 7**: API 路由层 (US-028~032) - **已完成**
- ⏳ **Phase 8**: 前端功能 (US-033~039) - **待完成**
- ⏳ **Phase 9**: 数据导入执行 (US-040~041) - **待完成**
- ⏳ **Phase 10**: 验收测试 (US-042~075) - **待完成**

---

## 0. AI Agent 工作流程 (Claude Code)

### 0.1 核心原则

本项目遵循 **Ralf 模式**（参考 [snarktank/ralph](https://github.com/snarktank/ralph)）进行 AI 辅助开发：

| 原则 | 说明 |
|------|------|
| **小任务** | 每个 US 应在一个上下文窗口内完成（30-60分钟） |
| **反馈循环** | Typecheck → Tests → CI → Browser Verification |
| **知识积累** | 每次迭代后更新 AGENTS.md/CLAUDE.md |
| **状态透明** | 使用 prd.json 跟踪完成状态 |

### 0.2 故事大小标准

**合适的故事大小** ✓
- 添加一个数据库列和迁移
- 为现有页面添加一个 UI 组件
- 更新服务方法的新逻辑
- 为列表添加筛选下拉菜单

**过大的故事（需要拆分）✗**
- "构建整个仪表板"
- "添加完整的认证系统"
- "重构整个 API"

### 0.3 进度跟踪命令

```bash
# 查看哪些故事已完成
cat tasks/prd-recipes.json | jq '.userStories[] | {id, title, passes}'

# 查看待办故事
cat tasks/prd-recipes.json | jq '.userStories[] | select(.passes == false)'

# 查看 Git 历史
git log --oneline -10

# 统计完成进度
cat tasks/prd-recipes.json | jq '[.userStories[] | select(.passes == true)] | length / (.userStories | length) * 100'
```

### 0.4 质量检查门禁

每个用户故事完成前必须通过：

```bash
# 后端代码必须通过
cd backend && python -m mypy api/

# 单元测试必须通过
cd backend && python -m pytest tests/test_unit/ -v

# API 测试必须通过
cd backend && python -m pytest tests/test_api/ -v

# 测试覆盖率检查
cd backend && python -m pytest tests/ --cov=api --cov-report=term-missing
```

### 0.5 前端验证要求

所有前端故事必须包含浏览器验证：

- 验收标准中明确标注 "Verify in browser"
- 使用开发者工具检查控制台无错误
- 测试交互功能（点击、滚动、筛选等）
- 验证响应式布局（如适用）

### 0.6 迭代后的知识更新

完成用户故事后，更新相关文档：

**CLAUDE.md** - 添加发现的内容：
```markdown
## 发现的模式
- 食材关联使用 get_or_create_ingredient() 模式
- JSON 字段查询使用 .contains() 而非 LIKE

## 常见陷阱
- SQLite 中 JSON 字段的 LIKE 查询不工作
- 测试中不要提交事务（会自动回滚）
```

**AGENTS.md**（如存在）- 记录迭代学习：
```markdown
## 2026-01-31 - 食谱功能
- Recipe 模型的 suitable_constitutions 是 JSON 数组
- 导入脚本使用 pandas.read_excel() 读取数据
```

### 0.7 停止条件

当所有用户故事的 `passes` 字段为 `true` 时，输出：

```
<promise>COMPLETE</promise>
```

并总结完成的功能、测试覆盖率和已知问题。

---

## 0.8 功能入口

### 用户入口路径
```
首页 (frontend/src/pages/index.vue)
  ↓ 点击 "食谱库" 功能卡片 (🍲 图标)
  ↓ 点击 "进入食谱" 行动按钮
  → 菜谱列表页面 (frontend/src/pages/recipes/list.vue)
  ↓ 点击菜谱卡片
  → 菜谱详情页面 (frontend/src/pages/recipes/detail.vue)
```

### 导航配置
| 配置项 | 值 |
|--------|-----|
| **位置** | 首页功能导航区域 |
| **图标** | 🍲 |
| **标题** | 食谱库 |
| **描述** | 根据体质推荐的养生食谱和食疗方案 |
| **行动按钮** | "进入食谱" |
| **路由** | `/pages/recipes/list` |
| **前端文件** | `frontend/src/pages/index.vue` |

---

## 1. 需求概述

### 1.1 功能背景

**现有数据资源**:
| 资源类型 | 路径 | 数量 |
|---------|------|------|
| Excel 菜谱数据 | `source_data/dishes_list_ai_filled.xlsx` | 12,785 条 |

**Excel 现有数据列**:
| 列名 | 说明 | 示例 | 填充率 | 导入DB |
|------|------|------|--------|--------|
| title | 菜谱名称 | 山药小米粥 | 100% | ✓ |
| desc | 个人体验/简介 | 这道菜是我家... | 42.2% | ✓ |
| tip | 烹饪贴士 | 山药要去皮... | 45.4% | ✓ |
| costtime | 烹饪时间（分钟） | 30 | 83.3% | ✓ |
| steptext | 制作步骤 | 步骤描述文本 | 100% | ✓ |
| QuantityIngredients | 食材清单 | 山药50g,小米100g | 100% | - |
| **difficulty** | **难度等级 (AI填充)** | 简单/中等/较难/困难 | 100% | ✓ |
| **suitable_constitutions** | **适合体质 (AI填充)** | ["peace","qi_deficiency"] | 100% | ✓ |
| **avoid_constitutions** | **禁忌体质 (AI填充)** | ["phlegm_damp"] | 100% | ✓ |
| **efficacy_tags** | **功效标签 (AI填充)** | ["健脾","养胃"] | 100% | ✓ |
| **solar_terms** | **节气标签 (AI填充)** | ["立冬","小雪","大雪"] | 100% | ✓ |
| confidence | AI置信度 (元数据) | 90 | 100% | ✗ |
| method | 填充方法 (元数据) | "AI" | 100% | ✗ |

**说明**: `confidence` 和 `method` 为 AI 填充元数据字段，仅用于数据质量参考，不导入数据库。

**本功能方案**:
1. Excel 数据导入：解析 Excel 文件，导入 12,785 条菜谱
2. 直接读取 AI 填充字段：difficulty, suitable_constitutions, avoid_constitutions, efficacy_tags, solar_terms
3. 用户端功能：菜谱浏览、搜索、筛选、详情查看

### 1.2 数据库字段映射表

| 用途 | Excel 列 | 数据库字段 | 类型 | 示例值 |
|------|----------|-----------|------|--------|
| 菜谱名称 | title | name | VARCHAR(200) | 山药小米粥 |
| 个人体验 | desc | desc | TEXT | 这道菜是我... |
| 烹饪贴士 | tip | tip | TEXT | 1.山药去皮... |
| 烹饪时间 | costtime | cooking_time | INTEGER | 30 |
| 难度等级 | difficulty | difficulty | VARCHAR(20) | easy/medium/harder/hard |
| 适合体质 | suitable_constitutions | suitable_constitutions | JSON | ["peace","qi_deficiency"] |
| 禁忌体质 | avoid_constitutions | avoid_constitutions | JSON | ["phlegm_damp"] |
| 功效标签 | efficacy_tags | efficacy_tags | JSON | ["健脾","养胃"] |
| 节气标签 | solar_terms | solar_terms | JSON | ["立冬","小雪","大雪"] |

### 1.3 实现笔记 (Lessons Learned)

#### 字段命名对齐
- **问题**: 早期代码使用 `description`/`cook_time`，PRD 规范使用 `desc`/`cooking_time`
- **解决**: 更新模型使用 PRD 规范名称，保留向后兼容
- **影响文件**: `backend/api/models/__init__.py`, `backend/api/schemas/recipe.py`

#### is_primary 字段
- **问题**: 早期代码使用 `is_main`，PRD 规范使用 `is_primary`
- **解决**: 使用 `is_primary`，在 RecipeIngredient 模型中添加
- **影响文件**: `backend/api/models/__init__.py`, `backend/scripts/import_recipes.py`

#### 难度等级
- **问题**: 原映射缺少 "较难" → `harder` 级别
- **解决**: 更新 DIFFICULTY_MAP 添加 `harder` 级别
- **影响文件**: `backend/scripts/recipe_import_config.py`

#### JSON 字段查询 (SQLite)
- **限制**: SQLite 中 JSON 字段的 LIKE 查询不工作
- **解决**: 使用 `.contains()` 方法查询 JSON 数组
- **示例**: `query.filter(Recipe.suitable_constitutions.contains("qi_deficiency"))`

#### 服务层模式
- **模式**: 无状态服务类，所有方法接受 `db: Session` 作为参数
- **好处**: 易于测试，不需要单例
- **示例**: `RecipeService().get_recipes(db=session)`

#### 测试策略
- **单元测试**: 测试服务层逻辑，使用 mock database
- **API 测试**: 测试端点响应，使用 TestClient
- **覆盖率目标**: ≥ 80%
- **命令**: `python -m pytest tests/ --cov=api --cov-report=term-missing`

#### 已知问题
1. **US-006** (数据库迁移) 尚未执行 - 需要运行 `alembic upgrade head`
2. **US-008** (StandardResponse schema) 代码已实现但未在 PRD 中标记完成
3. 前端页面 (US-033~039) 待实现
4. 数据导入 (US-040~041) 待执行

---

## 2. 用户故事（功能开发）

### Phase 1: 数据模型 (优先级 1-8)

---

#### US-001: 创建 Recipe 基础模型类

**描述**: 创建 Recipe ORM 模型类的基本结构

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 backend/api/models/__init__.py 中创建 Recipe 类",
    "Recipe 类继承自 Base",
    "表名: recipes",
    "字段定义:",
    "  - id: Integer, primary_key=True",
    "  - name: String(200), nullable=False",
    "  - desc: Text, nullable=True",
    "  - tip: Text, nullable=True",
    "  - cooking_time: Integer, nullable=True",
    "  - difficulty: String(20), nullable=True",
    "  - suitable_constitutions: JSON, nullable=True",
    "  - avoid_constitutions: JSON, nullable=True",
    "  - efficacy_tags: JSON, nullable=True",
    "  - solar_terms: JSON, nullable=True",
    "  - calories: Integer, nullable=True",
    "  - protein: Float, nullable=True",
    "  - fat: Float, nullable=True",
    "  - carbs: Float, nullable=True",
    "  - created_at: DateTime, default=datetime.utcnow",
    "  - updated_at: DateTime, default=datetime.utcnow, onupdate=datetime.utcnow",
    "添加 __repr__ 方法返回菜谱名称",
    "Typecheck passes: python -m mypy api/models/__init__.py"
  ]
}
```

**优先级**: 1 | **状态**: false

---

#### US-002: 为 Recipe 模型添加索引

**描述**: 为 Recipe 模型添加数据库索引

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 Recipe 类中添加索引定义:",
    "  - idx_name: 在 name 列上，唯一索引",
    "  - idx_difficulty: 在 difficulty 列上",
    "  - idx_cooking_time: 在 cooking_time 列上",
    "  - idx_created_at: 在 created_at 列上",
    "使用 __table_args__ 定义索引",
    "Typecheck passes"
  ]
}
```

**优先级**: 2 | **状态**: false | **依赖**: US-001

---

#### US-003: 创建 RecipeIngredient 关联表模型

**描述**: 创建菜谱与食材的多对多关联表

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 backend/api/models/__init__.py 中创建 RecipeIngredient 类",
    "表名: recipe_ingredients",
    "字段定义:",
    "  - id: Integer, primary_key=True",
    "  - recipe_id: Integer, ForeignKey('recipes.id')",
    "  - ingredient_id: Integer, ForeignKey('ingredients.id')",
    "  - amount: String(100), nullable=True",
    "  - is_primary: Boolean, default=False",
    "  - created_at: DateTime, default=datetime.utcnow",
    "添加复合唯一索引: (recipe_id, ingredient_id)",
    "Typecheck passes"
  ]
}
```

**优先级**: 3 | **状态**: false

---

#### US-004: 创建 RecipeStep 关联表模型

**描述**: 创建菜谱制作步骤关联表

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 backend/api/models/__init__.py 中创建 RecipeStep 类",
    "表名: recipe_steps",
    "字段定义:",
    "  - id: Integer, primary_key=True",
    "  - recipe_id: Integer, ForeignKey('recipes.id')",
    "  - step_number: Integer, nullable=False",
    "  - description: Text, nullable=False",
    "  - created_at: DateTime, default=datetime.utcnow",
    "添加复合唯一索引: (recipe_id, step_number)",
    "Typecheck passes"
  ]
}
```

**优先级**: 4 | **状态**: false

---

#### US-005: 添加模型关系定义

**描述**: 为 Recipe 模型添加与其他模型的关系

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 Recipe 类中添加关系:",
    "  - ingredients: relationship('RecipeIngredient', back_populates='recipe')",
    "  - steps: relationship('RecipeStep', order_by='RecipeStep.step_number')",
    "在 RecipeIngredient 类中添加关系:",
    "  - recipe: relationship('Recipe', back_populates='ingredients')",
    "  - ingredient: relationship('Ingredient')",
    "在 RecipeStep 类中添加关系:",
    "  - recipe: relationship('Recipe')",
    "Typecheck passes"
  ]
}
```

**优先级**: 5 | **状态**: false | **依赖**: US-001, US-003, US-004

---

#### US-006: 创建数据库迁移脚本

**描述**: 创建 Alembic 迁移脚本以创建菜谱相关表

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "创建迁移文件: backend/alembic/versions/xxx_create_recipes.py",
    "迁移包含:",
    "  - def upgrade(): 创建 recipes, recipe_ingredients, recipe_steps 表",
    "  - def downgrade(): 删除上述表",
    "运行迁移: alembic upgrade head",
    "验证表已创建: 在数据库客户端中查看表结构",
    "验证外键约束正常工作"
  ]
}
```

**优先级**: 6 | **状态**: false | **依赖**: US-001, US-003, US-004

---

#### US-007: 创建 RecipeBase Schema

**描述**: 创建 Recipe 的 Pydantic 基础验证模型

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "创建 backend/api/schemas/recipe.py",
    "创建 RecipeBase 类:",
    "  - name: str, Field(..., min_length=1, max_length=200)",
    "  - desc: Optional[str] = None",
    "  - tip: Optional[str] = None",
    "  - cooking_time: Optional[int] = Field(None, ge=0)",
    "  - difficulty: Optional[str] = Field(None, regex='^(easy|medium|harder|hard)$')",
    "  - suitable_constitutions: Optional[List[str]] = None",
    "  - avoid_constitutions: Optional[List[str]] = None",
    "  - efficacy_tags: Optional[List[str]] = None",
    "  - solar_terms: Optional[List[str]] = None",
    "添加 Config 类: orm_mode = True",
    "Typecheck passes"
  ]
}
```

**优先级**: 7 | **状态**: false

---

#### US-008: 创建完整 Schema 类

**描述**: 创建 Recipe 的完整 Schema 类集合

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 backend/api/schemas/recipe.py 中创建:",
    "  - RecipeCreate: 继承 RecipeBase",
    "  - RecipeUpdate: 继承 RecipeBase，所有字段可选",
    "  - RecipeResponse: 继承 RecipeBase，添加 id, created_at",
    "  - RecipeListItem: 列表页简化视图，包含 id, name, cooking_time, difficulty, efficacy_tags(前3个)",
    "  - RecipeListResponse: 包含 total, page, page_size, items",
    "添加单元测试验证 Schema 验证逻辑",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 8 | **状态**: false | **依赖**: US-007

---

### Phase 2: 导入配置基础 (优先级 9-13)

---

#### US-009: 创建导入配置文件结构和常量

**描述**: 创建 Excel 导入配置文件，定义常量和映射

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "创建 backend/scripts/recipe_import_config.py",
    "定义常量:",
    "  EXCEL_COLUMN_MAP = {'title': 'name', 'desc': 'desc', 'tip': 'tip', 'costtime': 'cooking_time'}",
    "  DIFFICULTY_MAP = {'简单': 'easy', '中等': 'medium', '较难': 'harder', '困难': 'hard'}",
    "  24节气列表: SOLAR_TERMS = ['立春', '雨水', '惊蛰', '春分', '清明', '谷雨', '立夏', '小满', '芒种', '夏至', '小暑', '大暑', '立秋', '处暑', '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪', '冬至', '小寒', '大寒']",
    "添加完整的中文注释",
    "Typecheck passes"
  ]
}
```

**优先级**: 9 | **状态**: false

---

#### US-010: 实现 parse_cooking_time() 函数

**描述**: 实现烹饪时间解析函数

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 recipe_import_config.py 中添加:",
    "  def parse_cooking_time(value: Any) -> Optional[int]:",
    "支持格式:",
    "  - int/float: 直接返回 int(value)",
    "  - str '30': 返回 30",
    "  - str '30分钟': 提取数字",
    "  - str '半小时': 返回 30",
    "  - str '1小时': 返回 60",
    "  - str '1小时30分': 返回 90",
    "  - None/空字符串: 返回 None",
    "添加单元测试覆盖所有分支",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 10 | **状态**: false | **依赖**: US-009

---

#### US-011: 实现 parse_difficulty() 函数

**描述**: 实现难度等级映射函数

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 recipe_import_config.py 中添加:",
    "  def parse_difficulty(value: str) -> Optional[str]:",
    "处理逻辑:",
    "  - 使用 DIFFICULTY_MAP 直接映射: '简单'→easy, '中等'→medium, '较难'→harder, '困难'→hard",
    "  - 如果是英文代码(easy/medium/harder/hard)直接返回",
    "  - 其他情况返回 None",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 11 | **状态**: false | **依赖**: US-009

---

#### US-012: 实现 parse_json_field() 函数

**描述**: 实现 JSON 字段解析函数

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 recipe_import_config.py 中添加:",
    "  def parse_json_field(value: Any) -> Optional[List[str]]:",
    "处理逻辑:",
    "  - 如果是 list，直接返回",
    "  - 如果是 str，尝试 eval() 解析",
    "  - 解析失败返回 None",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 12 | **状态**: false | **依赖**: US-009

---

### Phase 3: 导入解析函数 (优先级 13-14)

---

#### US-013: 实现 parse_ingredients() 函数

**描述**: 实现食材解析函数

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 recipe_import_config.py 中添加:",
    "  def parse_ingredients(text: str) -> List[Dict[str, Any]]:",
    "支持分隔符: 逗号(,、)、分号(；;)、换行",
    "解析格式:",
    "  - '山药50g' → {'name': '山药', 'amount': '50g'}",
    "  - '小米 100克' → {'name': '小米', 'amount': '100克'}",
    "  - '鸡蛋' → {'name': '鸡蛋', 'amount': None}",
    "处理括号备注: '山药(去皮)50g' → name='山药', amount='50g'",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 14 | **状态**: false | **依赖**: US-009

---

#### US-015: 实现 parse_steps() 函数

**描述**: 实现制作步骤解析函数

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 recipe_import_config.py 中添加:",
    "  def parse_steps(text: str) -> List[Dict[str, Any]]:",
    "支持分隔符: #号、换行、数字序号",
    "解析格式:",
    "  - '步骤1: 准备食材\\n步骤2: 开始烹饪' → 2条步骤",
    "  - '1.准备食材\\n2.开始烹饪' → 2条步骤",
    "  - '准备食材#开始烹饪' → 2条步骤",
    "自动编号: 没有编号时自动分配",
    "返回格式: [{'step_number': 1, 'description': '...'}, ...]",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 14 | **状态**: false | **依赖**: US-009

---

### Phase 4: 导入脚本核心 (优先级 15-23)

---

#### US-015: 创建导入脚本基础结构

**描述**: 创建导入脚本的主文件和参数解析

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "创建 backend/scripts/import_recipes.py",
    "添加命令行参数解析:",
    "  - --file: Excel 文件路径 (必需)",
    "  - --limit: 限制导入数量 (可选)",
    "  - --dry-run: 干运行模式 (可选)",
    "  - --verbose: 详细输出 (可选)",
    "添加 main() 函数",
    "添加 --help 文档",
    "执行 python scripts/import_recipes.py --help 验证",
    "Typecheck passes"
  ]
}
```

**优先级**: 15 | **状态**: false

---

#### US-016: 实现 Excel 文件读取函数

**描述**: 实现读取 Excel 文件的函数

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 import_recipes.py 中添加:",
    "  def read_excel_file(file_path: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:",
    "使用 pandas.read_excel() 读取 dishes_list_ai_filled.xlsx",
    "跳过 title 为空的行",
    "支持 limit 参数限制数量",
    "返回 List[Dict]",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 16 | **状态**: false | **依赖**: US-015

---

#### US-017: 实现菜谱去重检查函数

**描述**: 实现检查菜谱是否已存在的函数

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 import_recipes.py 中添加:",
    "  def check_recipe_exists(name: str, db: Session) -> bool:",
    "按 name 字段查询数据库",
    "返回 True/False",
    "添加单元测试 (使用 mock db)",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 17 | **状态**: false | **依赖**: US-015

---

#### US-018: 实现食材查找或创建函数

**描述**: 实现查找或创建食材的函数

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 import_recipes.py 中添加:",
    "  def get_or_create_ingredient(name: str, db: Session) -> Ingredient:",
    "查找逻辑:",
    "  1. 按 name 精确查找",
    "  2. 按别名查找",
    "  3. 创建新食材",
    "创建时设置 aliases=[name]",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 18 | **状态**: false | **依赖**: US-015

---

#### US-019: 实现单条菜谱导入函数

**描述**: 整合单条菜谱导入的完整流程

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 import_recipes.py 中添加:",
    "  def import_single_recipe(row: Dict, db: Session) -> Optional[Recipe]:",
    "流程:",
    "  1. 检查是否已存在 → 跳过",
    "  2. 直接读取 Excel 中的字段:",
    "    - name: title",
    "    - desc, tip, cooking_time: 直接使用",
    "    - difficulty: parse_difficulty() 映射",
    "    - suitable_constitutions, avoid_constitutions: parse_json_field()",
    "    - efficacy_tags, solar_terms: parse_json_field()",
    "  3. 解析食材: parse_ingredients()",
    "  4. 解析步骤: parse_steps()",
    "  5. 提交事务",
    "  6. 返回 Recipe (失败返回 None)",
    "错误处理: 捕获异常并记录",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 19 | **状态**: false | **依赖**: US-012, US-013, US-014, US-017, US-018

---

#### US-020: 实现批量导入主函数

**描述**: 实现批量导入的主逻辑

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 import_recipes.py 中添加:",
    "  def import_recipes(file_path: str, limit: Optional[int] = None, dry_run: bool = False) -> Dict[str, int]:",
    "流程:",
    "  1. 初始化数据库",
    "  2. 读取 Excel",
    "  3. 遍历导入: import_single_recipe()",
    "  4. 统计结果",
    "返回格式: {total, success, skipped, failed}",
    "每 100 条打印进度",
    "Typecheck passes"
  ]
}
```

**优先级**: 20 | **状态**: false | **依赖**: US-016, US-019

---

#### US-021: 实现干运行模式

**描述**: 实现干运行模式用于测试

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 import_recipes.py 中添加:",
    "  def dry_run_import(file_path: str, limit: Optional[int] = None) -> None:",
    "流程:",
    "  1. 读取 Excel",
    "  2. 遍历解析但不写入数据库",
    "  3. 打印解析结果",
    "输出格式: '[OK] 山药小米粥 | 30分钟 | easy | 体质: [peace, qi_deficiency]'",
    "执行: python scripts/import_recipes.py --dry-run --limit 10",
    "Typecheck passes"
  ]
}
```

**优先级**: 21 | **状态**: false | **依赖**: US-016

---

#### US-022: 实现失败导出功能

**描述**: 实现导出失败菜谱到 CSV

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 import_recipes.py 中添加:",
    "  def export_failed_recipes(failed: List[Dict], output_path: str) -> None:",
    "输入: failed 列表, 每项包含 {row, error}",
    "输出: CSV 文件, 列名为 title, desc, costtime, error",
    "编码: UTF-8 with BOM",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 22 | **状态**: false | **依赖**: US-015

---

#### US-023: 添加导入进度日志

**描述**: 为导入过程添加详细的进度日志

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 import_recipes.py 中添加日志记录:",
    "  - 记录导入开始和结束",
    "  - 每 100 条打印进度",
    "  - 记录成功/跳过/失败数量",
    "  - 记录失败的菜谱名称和错误",
    "使用 logging 模块",
    "添加单元测试验证日志",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 23 | **状态**: false | **依赖**: US-020

---

### Phase 5: 服务层 (优先级 24-30)

---

#### US-024: 创建 RecipeService 基础结构

**描述**: 创建菜谱服务类的基础结构

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "创建 backend/api/services/recipe_service.py",
    "创建 RecipeService 类 (无状态)",
    "所有方法接受 db: Session 参数",
    "添加类型提示和文档字符串",
    "Typecheck passes"
  ]
}
```

**优先级**: 24 | **状态**: false

---

#### US-025: 实现 get_recipes() 方法

**描述**: 实现菜谱列表查询方法

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 RecipeService 中添加:",
    "  def get_recipes(",
    "    page: int = 1,",
    "    page_size: int = 20,",
    "    constitution: Optional[str] = None,",
    "    efficacy: Optional[str] = None,",
    "    difficulty: Optional[str] = None,",
    "    solar_term: Optional[str] = None,",
    "    db: Session = None",
    "  ) -> Dict[str, Any]:",
    "支持筛选和分页",
    "返回 {total, page, page_size, items}",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 25 | **状态**: false | **依赖**: US-024

---

#### US-026: 实现 get_recipe_by_id() 方法

**描述**: 实现菜谱详情查询方法

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 RecipeService 中添加:",
    "  def get_recipe_by_id(id: int, db: Session) -> Optional[Recipe]:",
    "按 id 查询",
    "预加载 ingredients 和 steps",
    "未找到返回 None",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 26 | **状态**: false | **依赖**: US-024

---

#### US-027: 实现 search_recipes() 方法

**描述**: 实现菜谱搜索方法

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 RecipeService 中添加:",
    "  def search_recipes(",
    "    keyword: str,",
    "    page: int = 1,",
    "    page_size: int = 20,",
    "    constitution: Optional[str] = None,",
    "    difficulty: Optional[str] = None,",
    "    db: Session = None,",
    "  ) -> Dict[str, Any]:",
    "搜索范围: name, ingredients, efficacy_tags",
    "支持组合筛选",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 27 | **状态**: false | **依赖**: US-024

---

#### US-028: 实现 get_recommendations_by_constitution() 方法

**描述**: 实现基于体质的推荐方法

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 RecipeService 中添加:",
    "  def get_recommendations_by_constitution(",
    "    constitution: str,",
    "    limit: int = 10,",
    "    db: Session = None,",
    "  ) -> List[Recipe]:",
    "优先返回适合该体质的菜谱",
    "排除禁忌该体质的菜谱",
    "按 created_at DESC 排序",
    "验证体质代码有效性",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 28 | **状态**: false | **依赖**: US-024

---

#### US-029: 添加服务层错误处理

**描述**: 为服务层添加错误处理

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 RecipeService 中添加:",
    "  - 验证 constitution 参数有效性",
    "  - 无效体质抛出 ValueError",
    "  - 处理数据库异常",
    "  - 返回清晰的错误消息",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 29 | **状态**: false | **依赖**: US-025, US-026, US-027, US-028

---

#### US-030: 添加服务层日志

**描述**: 为服务层添加日志记录

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 RecipeService 方法中添加日志:",
    "  - 记录查询参数",
    "  - 记录结果数量",
    "  - 记录错误信息",
    "使用 logging 模块",
    "添加单元测试验证日志",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 30 | **状态**: false | **依赖**: US-029

---

#### US-031: 创建服务层工厂函数

**描述**: 创建获取服务实例的工厂函数

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 recipe_service.py 中添加:",
    "  def get_recipe_service() -> RecipeService:",
    "返回 RecipeService 实例",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 31 | **状态**: false | **依赖**: US-030

---

### Phase 6: CRUD 和验证层 (优先级 32-48)

---

#### US-032: 创建 StandardResponse Schema

**描述**: 创建统一的 API 响应格式 Schema

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "创建 backend/api/schemas/common.py",
    "定义泛型响应类:",
    "  class StandardResponse(BaseModel, Generic[T]):",
    "    code: int = Field(0, description='响应码，0表示成功')",
    "    data: Optional[T] = Field(None, description='响应数据')",
    "    message: str = Field('Success', description='响应消息')",
    "添加类型提示: from typing import TypeVar, Generic, Optional",
    "Typecheck passes"
  ]
}
```

**优先级**: 32 | **状态**: false

---

#### US-033: 实现 create_recipe() 服务方法

**描述**: 实现创建菜谱的服务方法

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 RecipeService 中添加:",
    "  def create_recipe(",
    "    recipe_data: RecipeCreate,",
    "    ingredients_data: List[Dict[str, Any]],",
    "    steps_data: List[Dict[str, Any]],",
    "    db: Session",
    "  ) -> Recipe:",
    "验证名称唯一性",
    "处理食材关联（查找或创建）",
    "创建步骤记录",
    "提交事务",
    "返回创建的 Recipe",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 33 | **状态**: false | **依赖**: US-024, US-018

---

#### US-034: 实现 update_recipe() 服务方法

**描述**: 实现更新菜谱的服务方法

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 RecipeService 中添加:",
    "  def update_recipe(",
    "    id: int,",
    "    recipe_data: RecipeUpdate,",
    "    ingredients_data: Optional[List[Dict[str, Any]]],",
    "    steps_data: Optional[List[Dict[str, Any]]],",
    "    db: Session",
    "  ) -> Optional[Recipe]:",
    "检查菜谱是否存在",
    "更新基础字段",
    "如提供食材数据，重新关联食材",
    "如提供步骤数据，重新创建步骤",
    "返回更新后的 Recipe",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 34 | **状态**: false | **依赖**: US-033

---

#### US-035: 实现 delete_recipe() 服务方法

**描述**: 实现删除菜谱的服务方法

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 RecipeService 中添加:",
    "  def delete_recipe(id: int, db: Session) -> bool:",
    "检查菜谱是否存在",
    "级联删除关联的食材和步骤",
    "删除菜谱记录",
    "返回 True/False",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 35 | **状态**: false | **依赖**: US-024

---

#### US-036: 添加体质代码验证函数

**描述**: 创建体质代码验证工具函数

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "创建 backend/api/utils/validators.py",
    "定义常量: VALID_CONSTITUTIONS = {'peace', 'qi_deficiency', ...}",
    "添加函数:",
    "  def is_valid_constitution_code(code: str) -> bool:",
    "    return code in VALID_CONSTITUTIONS",
    "  def validate_constitution_list(codes: List[str]) -> bool:",
    "    return all(is_valid_constitution_code(c) for c in codes)",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 36 | **状态**: false

---

#### US-037: 添加难度等级验证函数

**描述**: 创建难度等级验证工具函数

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 validators.py 中添加:",
    "  VALID_DIFFICULTIES = {'easy', 'medium', 'harder', 'hard'}",
    "  def is_valid_difficulty(code: str) -> bool:",
    "    return code in VALID_DIFFICULTIES",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 37 | **状态**: false

---

#### US-038: 创建 Schema 验证辅助函数

**描述**: 创建 Schema 层的验证辅助函数

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 backend/api/schemas/recipe.py 中添加:",
    "  from pydantic import validator",
    "  添加体质验证:",
    "    @validator('suitable_constitutions')",
    "    def validate_constituations(cls, v):",
    "      if v and not all(c in VALID_CONSTITUTIONS for c in v):",
    "        raise ValueError('Invalid constitution code')",
    "      return v",
    "  添加难度验证:",
    "    @validator('difficulty')",
    "    def validate_difficulty(cls, v):",
    "      if v and v not in VALID_DIFFICULTIES:",
    "        raise ValueError('Invalid difficulty')",
    "      return v",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 38 | **状态**: false | **依赖**: US-008, US-036, US-037

---

#### US-039: 创建导入验证 Schema

**描述**: 创建导入专用的验证 Schema

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 backend/api/schemas/recipe.py 中添加:",
    "  class RecipeImportBase(BaseModel):",
    "    name: str",
    "    desc: Optional[str] = None",
    "    tip: Optional[str] = None",
    "    cooking_time_raw: Optional[str] = None  # 原始时间字符串",
    "    difficulty_raw: Optional[str] = None  # 原始难度字符串",
    "    ingredients_raw: str  # 原始食材字符串",
    "    steps_raw: str  # 原始步骤字符串",
    "添加配置类: Config = {'extra': 'allow'}  # 允许额外字段",
    "Typecheck passes"
  ]
}
```

**优先级**: 39 | **状态**: false | **依赖**: US-007

---

#### US-040: 创建菜谱统计服务方法

**描述**: 实现菜谱统计功能的服务方法

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 RecipeService 中添加:",
    "  def get_statistics(db: Session) -> Dict[str, Any]:",
    "统计内容:",
    "  - total_recipes: 总菜谱数",
    "  - by_difficulty: 各难度等级数量",
    "  - by_constitution: 各体质相关菜谱数",
    "  - with_images: 有封面图的菜谱数",
    "  - avg_cooking_time: 平均烹饪时间",
    "返回统计字典",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 40 | **状态**: false | **依赖**: US-024

---

#### US-041: 实现批量获取菜谱方法

**描述**: 实现批量获取菜谱详情的服务方法

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 RecipeService 中添加:",
    "  def get_recipes_by_ids(",
    "    ids: List[int],",
    "    db: Session",
    "  ) -> List[Recipe]:",
    "验证 ID 列表非空",
    "限制最多 100 个 ID",
    "预加载食材和步骤",
    "返回菜谱列表",
    "添加单元测试",
    "Typecheck passes",
    "Tests pass"
  ]
}
```

**优先级**: 41 | **状态**: false | **依赖**: US-026

---

#### US-042: 实现 POST /api/v1/recipes 接口

**描述**: 实现创建菜谱的 API 接口

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 recipes.py 中添加:",
    "  @router.post('', response_model=StandardResponse[RecipeResponse], status_code=201)",
    "请求体: RecipeCreate",
    "可选参数: ingredients (List), steps (List)",
    "调用 RecipeService.create_recipe()",
    "验证失败返回 422",
    "名称重复返回 400",
    "添加 API 测试",
    "验证: curl -X POST http://localhost:8000/api/v1/recipes -d '{...}'",
    "Tests pass"
  ]
}
```

**优先级**: 42 | **状态**: false | **依赖**: US-033, US-049

---

#### US-043: 实现 PUT /api/v1/recipes/{id} 接口

**描述**: 实现更新菜谱的 API 接口

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 recipes.py 中添加:",
    "  @router.put('/{id}', response_model=StandardResponse[RecipeResponse])",
    "请求体: RecipeUpdate",
    "可选参数: ingredients, steps",
    "调用 RecipeService.update_recipe()",
    "菜谱不存在返回 404",
    "添加 API 测试",
    "验证: curl -X PUT http://localhost:8000/api/v1/recipes/1 -d '{...}'",
    "Tests pass"
  ]
}
```

**优先级**: 43 | **状态**: false | **依赖**: US-034, US-049

---

#### US-044: 实现 DELETE /api/v1/recipes/{id} 接口

**描述**: 实现删除菜谱的 API 接口

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 recipes.py 中添加:",
    "  @router.delete('/{id}', response_model=StandardResponse[None])",
    "调用 RecipeService.delete_recipe()",
    "菜谱不存在返回 404",
    "成功返回 204",
    "添加 API 测试",
    "验证: curl -X DELETE http://localhost:8000/api/v1/recipes/1",
    "Tests pass"
  ]
}
```

**优先级**: 44 | **状态**: false | **依赖**: US-035, US-049

---

#### US-045: 实现 GET /api/v1/recipes/statistics 接口

**描述**: 实现菜谱统计的 API 接口

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 recipes.py 中添加:",
    "  @router.get('/statistics', response_model=StandardResponse[Dict[str, Any]])",
    "调用 RecipeService.get_statistics()",
    "返回统计信息",
    "添加 API 测试",
    "验证: curl http://localhost:8000/api/v1/recipes/statistics",
    "Tests pass"
  ]
}
```

**优先级**: 45 | **状态**: false | **依赖**: US-040, US-049

---

#### US-046: 实现 POST /api/v1/recipes/batch 接口

**描述**: 实现批量获取菜谱的 API 接口

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 recipes.py 中添加:",
    "  @router.post('/batch', response_model=StandardResponse[List[RecipeListItem]])",
    "请求体: {'ids': List[int]}",
    "验证 ID 列表非空且 <= 100",
    "调用 RecipeService.get_recipes_by_ids()",
    "添加 API 测试",
    "验证: curl -X POST http://localhost:8000/api/v1/recipes/batch -d '{\"ids\": [1,2,3]}'",
    "Tests pass"
  ]
}
```

**优先级**: 46 | **状态**: false | **依赖**: US-041, US-049

---

#### US-047: 添加请求日志中间件

**描述**: 为菜谱 API 添加请求日志中间件

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 recipes.py 中添加中间件:",
    "  记录请求方法和路径",
    "  记录查询参数",
    "  记录请求体（脱敏）",
    "  记录响应状态和耗时",
    "使用 logging 模块",
    "添加 API 测试验证日志",
    "Tests pass"
  ]
}
```

**优先级**: 47 | **状态**: false | **依赖**: US-049

---

#### US-048: 添加 API 限流保护

**描述**: 为菜谱 API 添加限流保护

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "使用 slowapi 或类似库",
    "配置限流规则:",
    "  - 列表接口: 60次/分钟",
    "  - 详情接口: 120次/分钟",
    "  - 搜索接口: 30次/分钟",
    "  - CRUD接口: 20次/分钟",
    "超限返回 429 和 Retry-After 头",
    "添加 API 测试",
    "Tests pass"
  ]
}
```

**优先级**: 48 | **状态**: false | **依赖**: US-049

---

### Phase 7: API 路由层 (优先级 49-55)

---

#### US-049: 创建菜谱 API 路由基础

**描述**: 创建菜谱 API 路由的基础结构

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "创建 backend/api/routers/recipes.py",
    "创建 APIRouter: prefix='/api/v1/recipes', tags=['recipes']",
    "在 main.py 中注册路由",
    "添加 CORS 支持",
    "启动服务器验证: http://localhost:8000/docs",
    "Typecheck passes"
  ]
}
```

**优先级**: 49 | **状态**: false | **依赖**: US-008

---

#### US-050: 实现 GET /api/v1/recipes 接口

**描述**: 实现菜谱列表接口

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 recipes.py 中添加:",
    "  @router.get('', response_model=StandardResponse[RecipeListResponse])",
    "查询参数: page, page_size, constitution, efficacy, difficulty, solar_term",
    "调用 RecipeService.get_recipes()",
    "返回格式: {code: 0, data: {...}, message: 'Success'}",
    "添加 API 测试",
    "验证: curl 'http://localhost:8000/api/v1/recipes?page=1&page_size=5'",
    "Tests pass"
  ]
}
```

**优先级**: 50 | **状态**: false | **依赖**: US-042, US-049

---

#### US-051: 实现 GET /api/v1/recipes/{id} 接口

**描述**: 实现菜谱详情接口

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 recipes.py 中添加:",
    "  @router.get('/{id}', response_model=StandardResponse[RecipeResponse])",
    "参数: id: int = Path(..., ge=1)",
    "调用 RecipeService.get_recipe_by_id()",
    "菜谱不存在返回 404",
    "添加 API 测试",
    "验证: curl 'http://localhost:8000/api/v1/recipes/1'",
    "Tests pass"
  ]
}
```

**优先级**: 51 | **状态**: false | **依赖**: US-043, US-049

---

#### US-052: 实现 GET /api/v1/recipes/search 接口

**描述**: 实现菜谱搜索接口

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 recipes.py 中添加:",
    "  @router.get('/search', response_model=StandardResponse[RecipeListResponse])",
    "查询参数: keyword (必需), page, page_size, constitution, difficulty",
    "调用 RecipeService.search_recipes()",
    "添加 API 测试",
    "验证: curl 'http://localhost:8000/api/v1/recipes/search?keyword=山药'",
    "Tests pass"
  ]
}
```

**优先级**: 52 | **状态**: false | **依赖**: US-044, US-049

---

#### US-053: 实现 GET /api/v1/recipes/recommendations 接口

**描述**: 实现体质推荐接口

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 recipes.py 中添加:",
    "  @router.get('/recommendations', response_model=StandardResponse[List[RecipeListItem]])",
    "查询参数: constitution (必需), limit",
    "调用 RecipeService.get_recommendations_by_constitution()",
    "无效体质返回 400",
    "添加 API 测试",
    "验证: curl 'http://localhost:8000/api/v1/recipes/recommendations?constitution=qi_deficiency'",
    "Tests pass"
  ]
}
```

**优先级**: 53 | **状态**: false | **依赖**: US-045, US-049

---

#### US-054: 添加 API 错误处理

**描述**: 为 API 添加统一的错误处理

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 recipes.py 中添加:",
    "  - 参数验证错误处理",
    "  - 业务逻辑错误处理",
    "  - 数据库错误处理",
    "  - 返回标准错误格式: {code: -1, message: '...'}",
    "添加 API 测试",
    "Tests pass"
  ]
}
```

**优先级**: 54 | **状态**: false | **依赖**: US-050, US-051, US-052, US-053

---

#### US-055: 添加 API 日志

**描述**: 为 API 添加请求日志

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 recipes.py 中添加:",
    "  - 记录每个请求的参数",
    "  - 记录响应状态",
    "  - 记录处理时间",
    "使用 logging 模块",
    "添加 API 测试验证日志",
    "Tests pass"
  ]
}
```

**优先级**: 55 | **状态**: false | **依赖**: US-054

---

### Phase 8: 前端功能 (优先级 56-62)

---

#### US-056: 添加首页食谱库卡片

**描述**: 在首页添加食谱库功能入口

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 frontend/src/pages/index.vue 的功能导航区域添加卡片",
    "卡片内容: 图标🍲, 标题'食谱库', 描述, 按钮'进入食谱'",
    "点击跳转到 /pages/recipes/list",
    "样式与其他卡片一致",
    "在浏览器中验证",
    "Verify in browser (Chrome)"
  ]
}
```

**优先级**: 56 | **状态**: false

---

#### US-057: 创建菜谱列表页面基础结构

**描述**: 创建菜谱列表页面的基础结构

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "创建 frontend/src/pages/recipes/list.vue",
    "页面结构:",
    "  - 顶部导航: 返回按钮 + 标题'食谱库'",
    "  - 筛选器区域: 横向滚动",
    "  - 菜谱列表区域",
    "  - 加载状态",
    "  - 空状态",
    "在浏览器中验证布局",
    "Verify in browser"
  ]
}
```

**优先级**: 57 | **状态**: false

---

#### US-058: 实现列表页筛选器

**描述**: 实现菜谱列表页的筛选器组件

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 list.vue 中添加筛选器:",
    "  - 体质筛选: 9种体质标签",
    "  - 节气筛选: 春夏秋冬",
    "  - 难度筛选: 简单/中等/困难",
    "点击标签触发筛选",
    "选中的标签高亮显示",
    "可取消筛选",
    "在浏览器中验证",
    "Verify in browser"
  ]
}
```

**优先级**: 58 | **状态**: false | **依赖**: US-057

---

#### US-059: 实现列表页菜谱卡片

**描述**: 实现菜谱卡片组件

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 list.vue 中添加菜谱卡片:",
    "  - 封面图: 有图显示图, 无图显示占位",
    "  - 菜谱名称",
    "  - 难度标签: easy=绿, medium=橙, hard=红",
    "  - 功效标签: 显示前3个",
    "点击卡片跳转详情页",
    "下拉刷新支持",
    "滚动加载更多",
    "在浏览器中验证",
    "Verify in browser"
  ]
}
```

**优先级**: 59 | **状态**: false | **依赖**: US-057

---

#### US-060: 创建菜谱详情页面基础结构

**描述**: 创建菜谱详情页面的基础结构

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "创建 frontend/src/pages/recipes/detail.vue",
    "页面结构:",
    "  - 顶部导航: 返回 + 分享",
    "  - 封面图区域",
    "  - 基本信息区域",
    "  - 内容区域",
    "  - 加载状态",
    "在浏览器中验证布局",
    "Verify in browser"
  ]
}
```

**优先级**: 60 | **状态**: false

---

#### US-061: 实现详情页各区域

**描述**: 实现详情页的各个内容区域

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在 detail.vue 中添加区域:",
    "  - 封面图: 大图显示, 失败显示占位",
    "  - 基本信息: 名称 + 时间 + 难度",
    "  - desc 区域: 蓝色背景(#e3f2fd), 标题'个人体验'",
    "  - tip 区域: 黄色背景(#fff9c4), 标题'烹饪贴士'",
    "  - 体质区域: 适合(绿) + 禁忌(红)",
    "  - 功效/节气标签",
    "  - 食材列表: 可展开折叠",
    "  - 制作步骤: 按序号显示",
    "体质标签显示中文名",
    "在浏览器中验证",
    "Verify in browser"
  ]
}
```

**优先级**: 61 | **状态**: false | **依赖**: US-060

---

#### US-062: 创建前端 API 客户端

**描述**: 创建菜谱 API 客户端模块

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "创建 frontend/src/api/recipes.js",
    "导出函数:",
    "  - getRecipes(params)",
    "  - getRecipeById(id)",
    "  - searchRecipes(params)",
    "  - getRecommendations(constitution)",
    "字段映射: cooking_time, cover_image",
    "体质映射: CONSTITUTION_MAP",
    "难度映射: DIFFICULTY_MAP",
    "统一错误处理",
    "在浏览器控制台测试",
    "Verify in browser"
  ]
}
```

**优先级**: 62 | **状态**: false | **依赖**: US-049

---

### Phase 9: 数据导入执行 (优先级 63-65)

---

#### US-063: 执行干运行测试

**描述**: 执行干运行模式测试导入功能

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "执行命令:",
    "  cd backend && python scripts/import_recipes.py --file ../source_data/dishes_list.xlsx --dry-run --limit 100",
    "验证项目:",
    "  - 菜谱名称解析正确",
    "  - 时间解析正确",
    "  - 难度推测合理",
    "  - 食材解析正确",
    "  - 步骤解析正确",
    "  - 图片匹配率 > 30%",
    "  - 标签推测合理",
    "抽样检查 10 条输出",
    "Tests pass"
  ]
}
```

**优先级**: 63 | **状态**: false | **依赖**: US-039, 前置所有配置

---

#### US-064: 正式导入数据

**描述**: 执行完整的菜谱数据导入

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "执行命令:",
    "  cd backend && python scripts/import_recipes.py --file ../source_data/dishes_list.xlsx",
    "验证数据库:",
    "  - 总菜谱数 > 12,500 (98%+)",
    "  - 有 desc 的 > 40%",
    "  - 有 tip 的 > 45%",
    "  - 有 difficulty 的 = 100%",
    "  - 有 suitable_constitutions 的 > 80%",
    "  - 有 efficacy_tags 的 > 80%",
    "  - 有 cover_image 的 > 30%",
    "  - 失败率 < 2%",
    "抽样检查 10 条数据",
    "Tests pass"
  ]
}
```

**优先级**: 64 | **状态**: false | **依赖**: US-038, US-063

---

#### US-065: 验证智能字段质量

**描述**: 验证智能填充的字段质量

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "运行验证脚本检查:",
    "  - difficulty 分布合理",
    "  - suitable_constitutions 包含平和质的 > 70%",
    "  - efficacy_tags 多样性 > 10 种",
    "  - solar_terms 包含标签的 > 50%",
    "  - 四季分布相对均衡",
    "抽样检查 20 条人工验证",
    "修正明显错误的规则",
    "Tests pass"
  ]
}
```

**优先级**: 65 | **状态**: false | **依赖**: US-064

---

## 3. 用户故事（验收测试）

### Phase 10: 验收测试 (优先级 66-75)

---

#### US-066: 验收 - 字段完整性测试

**描述**: 验证数据库字段完整性

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "运行数据库验证:",
    "  cd backend && python -c \"",
    "  from api.database import get_db;",
    "  from api.models import Recipe;",
    "  db = next(get_db());",
    "  total = db.query(Recipe).count();",
    "  assert db.query(Recipe).filter(Recipe.difficulty != None).count() == total, 'difficulty 必须 100%';",
    "  assert db.query(Recipe).filter(Recipe.suitable_constitutions != None).count() / total >= 0.8, '体质 >= 80%';",
    "  assert db.query(Recipe).filter(Recipe.efficacy_tags != None).count() / total >= 0.8, '功效 >= 80%';",
    "  print('✓ 字段完整性验证通过')",
    "  \"",
    "Tests pass"
  ]
}
```

**优先级**: 66 | **状态**: false | **依赖**: US-064

---

#### US-067: 验收 - 图片匹配测试

**描述**: 验证图片匹配功能

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "运行验证:",
    "  cd backend && python -c \"",
    "  from api.database import get_db;",
    "  from api.models import Recipe;",
    "  db = next(get_db());",
    "  total = db.query(Recipe).count();",
    "  with_image = db.query(Recipe).filter(Recipe.cover_image != None).count();",
    "  assert with_image / total >= 0.3, '图片匹配率 >= 30%';",
    "  print(f'✓ 图片匹配率: {with_image/total*100:.1f}%')",
    "  \"",
    "抽样验证 20 张图片文件存在",
    "Tests pass"
  ]
}
```

**优先级**: 67 | **状态**: false | **依赖**: US-064

---

#### US-068: 验收 - API 字段测试

**描述**: 验证 API 返回字段正确性

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "运行 API 测试:",
    "  cd backend && python -c \"",
    "  import requests;",
    "  r = requests.get('http://localhost:8000/api/v1/recipes?page=1&page_size=5');",
    "  data = r.json();",
    "  assert data['code'] == 0;",
    "  item = data['data']['items'][0];",
    "  assert 'cooking_time' in item, '必须有 cooking_time';",
    "  assert 'cover_image' in item, '必须有 cover_image';",
    "  assert 'difficulty' in item, '必须有 difficulty';",
    "  print('✓ API 字段验证通过')",
    "  \"",
    "Tests pass"
  ]
}
```

**优先级**: 68 | **状态**: false | **依赖**: US-050

---

#### US-069: 验收 - 功能入口测试

**描述**: 验证前端功能入口

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在浏览器中验证:",
    "  1. 打开首页",
    "  2. 找到食谱库卡片",
    "  3. 验证图标、标题、描述、按钮",
    "  4. 点击按钮",
    "  5. 验证跳转到列表页",
    "Verify in browser (Chrome)"
  ]
}
```

**优先级**: 69 | **状态**: false | **依赖**: US-056

---

#### US-070: 验收 - 列表页功能测试

**描述**: 验证列表页功能

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在浏览器中验证:",
    "  1. 列表正确加载",
    "  2. 点击体质筛选, 列表更新",
    "  3. 点击节气筛选, 列表更新",
    "  4. 点击难度筛选, 列表更新",
    "  5. 点击卡片跳转详情",
    "  6. 下拉刷新工作",
    "  7. 滚动加载更多",
    "Verify in browser"
  ]
}
```

**优先级**: 70 | **状态**: false | **依赖**: US-057, US-058, US-059

---

#### US-071: 验收 - 详情页功能测试

**描述**: 验证详情页功能

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在浏览器中验证:",
    "  1. 详情正确加载",
    "  2. 封面图显示",
    "  3. desc 区域蓝色背景",
    "  4. tip 区域黄色背景",
    "  5. 体质标签显示中文名",
    "  6. 功效标签可点击",
    "  7. 食材列表可展开",
    "  8. 步骤按序号显示",
    "Verify in browser"
  ]
}
```

**优先级**: 71 | **状态**: false | **依赖**: US-060, US-061

---

#### US-072: 验收 - 体质筛选测试

**描述**: 验证体质筛选功能

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "后端验证:",
    "  curl 'http://localhost:8000/api/v1/recipes?constitution=qi_deficiency&page_size=20'",
    "  验证返回的菜谱都包含 qi_deficiency",
    "前端验证:",
    "  1. 点击'气虚质'标签",
    "  2. 验证列表更新",
    "  3. 验证显示的菜谱适合气虚质",
    "  4. 测试其他体质",
    "Verify in browser",
    "Tests pass"
  ]
}
```

**优先级**: 72 | **状态**: false | **依赖**: US-058

---

#### US-073: 验收 - 节气筛选测试

**描述**: 验证节气筛选功能

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "后端验证:",
    "  curl 'http://localhost:8000/api/v1/recipes?solar_term=春季&page_size=20'",
    "  验证返回的菜谱都包含春季标签",
    "前端验证:",
    "  1. 点击'春季'标签",
    "  2. 验证列表更新",
    "  3. 测试其他季节",
    "Verify in browser",
    "Tests pass"
  ]
}
```

**优先级**: 73 | **状态**: false | **依赖**: US-058

---

#### US-074: 验收 - 搜索功能测试

**描述**: 验证搜索功能

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "后端验证:",
    "  curl 'http://localhost:8000/api/v1/recipes/search?keyword=山药&page_size=20'",
    "  验证搜索结果包含关键词",
    "前端验证:",
    "  1. 输入'山药'搜索",
    "  2. 验证结果显示",
    "  3. 测试组合搜索",
    "Verify in browser",
    "Tests pass"
  ]
}
```

**优先级**: 74 | **状态**: false | **依赖**: US-052

---

#### US-075: 验收 - 完整流程测试

**描述**: 验证完整的用户使用流程

**验收标准**:
```json
{
  "acceptanceCriteria": [
    "在浏览器中验证完整流程:",
    "  1. 首页 → 点击食谱库",
    "  2. 列表页 → 筛选气虚质",
    "  3. 点击菜谱卡片",
    "  4. 详情页 → 查看完整信息",
    "  5. 返回列表 → 搜索'山药'",
    "  6. 点击搜索结果",
    "  7. 验证详情正确",
    "Verify in browser",
    "Tests pass"
  ]
}
```

**优先级**: 75 | **状态**: false | **依赖**: 所有前端功能

---

## 4. 附录

### 4.1 体质类型映射

| 代码 | 中文名称 | 英文名称 |
|------|---------|---------|
| peace | 平和质 | Peaceful |
| qi_deficiency | 气虚质 | Qi Deficiency |
| yang_deficiency | 阳虚质 | Yang Deficiency |
| yin_deficiency | 阴虚质 | Yin Deficiency |
| phlegm_damp | 痰湿质 | Phlegm-Dampness |
| damp_heat | 湿热质 | Damp-Heat |
| blood_stasis | 血瘀质 | Blood Stasis |
| qi_depression | 气郁质 | Qi Depression |
| special | 特禀质 | Special |

### 4.2 难度等级映射

| 代码 | 中文 | 说明 |
|------|------|------|
| easy | 简单 | 容易制作的菜谱 |
| medium | 中等 | 需要一定烹饪技巧 |
| harder | 较难 | 制作步骤复杂 |
| hard | 困难 | 需要专业技巧 |

### 4.3 24节气列表

立春、雨水、惊蛰、春分、清明、谷雨、立夏、小满、芒种、夏至、小暑、大暑、立秋、处暑、白露、秋分、寒露、霜降、立冬、小雪、大雪、冬至、小寒、大寒

### 4.4 质量门禁标准

所有用户故事必须包含：

| 验收类型 | 命令 | 说明 |
|---------|------|------|
| **Typecheck** | `python -m mypy api/` | 后端代码类型检查通过 |
| **Tests** | `python -m pytest tests/ -v` | 单元测试和 API 测试通过 |
| **Coverage** | `python -m pytest tests/ --cov=api` | 覆盖率 ≥ 80% |
| **Browser** | 手动验证 | 前端在浏览器中验证 |

**前端验证检查清单**:
- [ ] 页面正确加载
- [ ] 控制台无错误
- [ ] 交互功能正常（点击、筛选、搜索等）
- [ ] 响应式布局正确（移动端/桌面端）
- [ ] API 调用返回正确数据

### 4.5 故事大小标准

**单个故事应该在 30-60 分钟内完成**

| 任务类型 | 预计时间 | 单个故事 |
|---------|---------|----------|
| 添加数据库列 + 迁移 | 20-30 分钟 | ✓ |
| 添加 UI 组件到现有页面 | 30-45 分钟 | ✓ |
| 更新服务方法逻辑 | 20-40 分钟 | ✓ |
| 添加筛选下拉菜单 | 30-45 分钟 | ✓ |
| 完整的 CRUD API | 60-90 分钟 | → 拆分为多个 |
| 整个前端页面 | 120+ 分钟 | → 拆分为多个 |

**拆分原则**:
1. 数据模型变更独立（迁移脚本）
2. 服务层逻辑独立（单元测试可验证）
3. API 路由独立（API 测试可验证）
4. 前端组件独立（浏览器可验证）
5. 每个故事必须可独立验收

### 4.6 prd.json 结构

状态跟踪文件 `tasks/prd-recipes.json` 格式：

```json
{
  "metadata": {
    "title": "中医养生菜谱功能",
    "version": "10.0.0",
    "lastUpdated": "2026-01-31",
    "totalStories": 75,
    "completedStories": 0
  },
  "userStories": [
    {
      "id": "US-001",
      "title": "创建 Recipe 基础模型类",
      "phase": 1,
      "priority": 1,
      "status": "pending",
      "passes": false,
      "dependencies": [],
      "completedAt": null
    }
  ]
}
```

**状态值**:
- `pending`: 待开始
- `in_progress`: 进行中
- `completed`: 已完成
- `skipped`: 已跳过
- `blocked`: 被阻塞

### 4.7 变更历史

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| 12.0.0 | 2026-01-31 | 添加进度概览和实现阶段跟踪；添加实现笔记 (Lessons Learned) 包括字段命名对齐、JSON 查询模式、服务层设计等；更新 32/75 故事状态为已完成 |
| 11.0.0 | 2026-01-31 | 添加 prd-recipes.json（AI Agent 可执行格式），包含 75 个用户故事的结构化数据、依赖关系、验收标准、预计时间等 |
| 10.0.0 | 2026-01-31 | 添加 Phase 6 (CRUD 和验证层)，包含 US-032~US-048：StandardResponse Schema、CRUD 服务方法、验证函数、统计和批量获取、CRUD API 接口、日志和限流 |
| 9.0.0 | 2026-01-31 | 根据 dishes_list_ai_filled.xlsx 实际数据更新：移除图片功能、难度改为4档、节气改为24节气、移除智能推测逻辑、confidence和method不导入DB |
| 8.0.0 | 2026-01-31 | 参考 prd-ralph-analysis.md 重写，拆分大故事，功能开发与验收分离 |
| 7.0.0 | 2026-01-31 | 添加详细用户故事和验收标准 |
| 1.0.0 | 2024-01-28 | 初始版本 |
