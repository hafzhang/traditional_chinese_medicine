# id: ingredient-dietary
# name: 食材与食疗推荐系统
# description: 提供9种体质的食材推荐/禁忌、食谱筛选、食材别名搜索的专业能力
# version: 1.0.0
# author: Claude Code
# tags: [tcm, dietary, ingredient, recipe, constitution]

---

## 食材与食疗推荐系统 Skill

### 核心数据结构

#### Ingredient 模型
```python
class Ingredient(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    category = Column(String(50))  # 分类：谷类、蔬菜、水果、肉类等
    nature = Column(String(20))  # 性味：寒、凉、平、温、热
    taste = Column(String(50))  # 味道：酸、苦、甘、辛、咸
    efficacy = Column(Text)  # 功效描述
    nutritional_value = Column(Text)  # 营养价值
    contraindications = Column(Text)  # 禁忌人群
    suitable_constitutions = Column(JSON, nullable=False, default=list)  # 适合体质数组
    avoid_constitutions = Column(JSON, nullable=False, default=list)  # 禁忌体质数组
    aliases = Column(JSON, nullable=False, default=list)  # 别名数组
    image_url = Column(String(500))
```

#### Recipe 模型
```python
class Recipe(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    meal_type = Column(String(20))  # 餐次：breakfast, lunch, dinner, snack
    cooking_method = Column(String(50))  # 烹饪方式：蒸、煮、炒等
    cooking_time = Column(Integer)  # 烹饪时间（分钟）
    difficulty = Column(String(20))  # 难度：简单、中等、困难
    ingredients = Column(JSON, nullable=False)  # 食材列表
    steps = Column(JSON, nullable=False)  # 制作步骤
    tips = Column(Text)  # 小贴士
    suitable_constitutions = Column(JSON, nullable=False, default=list)
    image_url = Column(String(500))
```

---

### 9种体质代码

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

---

### 服务层模式

#### IngredientService 核心方法

```python
class IngredientService:
    def get_ingredient_by_id(
        self,
        ingredient_id: int,
        db: Session
    ) -> Optional[Ingredient]:
        """根据ID获取食材"""

    def search_ingredients(
        self,
        keyword: str,
        db: Session,
        skip: int = 0,
        limit: int = 20
    ) -> List[Ingredient]:
        """
        关键词搜索
        - 搜索名称
        - 搜索别名（使用 or_() 查询）
        - 搜索分类
        """

    def get_ingredients_by_constitution(
        self,
        constitution: str,
        db: Session
    ) -> Dict[str, List[Ingredient]]:
        """
        根据体质获取推荐/禁忌食材

        返回:
        {
            "recommended": [...],   # suitable_constitutions 包含该体质
            "avoided": [...]        # avoid_constitutions 包含该体质
        }
        """

    def is_valid_constitution_code(self, code: str) -> bool:
        """验证体质代码是否有效"""
```

#### RecipeService 核心方法

```python
class RecipeService:
    def get_recipe_by_id(
        self,
        recipe_id: int,
        db: Session
    ) -> Optional[Recipe]:

    def get_recipes_by_constitution(
        self,
        constitution: str,
        db: Session,
        meal_type: Optional[str] = None  # 餐次筛选
    ) -> List[Recipe]:
        """
        根据体质获取食谱
        - meal_type: breakfast, lunch, dinner, snack
        """

    def search_recipes(
        self,
        keyword: str,
        db: Session
    ) -> List[Recipe]:
        """关键词搜索食谱名称"""

    def get_recipes_by_ingredient(
        self,
        ingredient_name: str,
        db: Session
    ) -> List[Recipe]:
        """根据食材查找食谱"""
```

---

### JSON 字段查询规范

#### SQLite JSON 数组查询
```python
# 正确：检查数组是否包含值
query.filter(Ingredient.suitable_constitutions.contains("qi_deficiency"))

# 错误：LIKE 查询在 SQLite JSON 列上不可靠
# query.filter(Ingredient.suitable_constitutions.like("%qi_deficiency%"))
```

#### JSON 字段操作
```python
# 创建时
ingredient = Ingredient(
    name="山药",
    aliases=["怀山药", "淮山", "薯蓣"],
    suitable_constitutions=["qi_deficiency", "yang_deficiency"]
)

# 查询别名（使用 SQLAlchemy 的 JSON 操作）
from sqlalchemy import or_
query = query.filter(
    or_(
        Ingredient.name.ilike(f"%{keyword}%"),
        # 别名搜索需要具体实现，见下方
    )
)
```

---

### API 端点规范

#### 食材端点
| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/ingredients` | GET | 获取食材列表（分页） |
| `/api/ingredients/{id}` | GET | 获取食材详情 |
| `/api/ingredients/search` | GET | 关键词搜索 |
| `/api/ingredients/by-constitution` | GET | 按体质查询（推荐+禁忌） |
| `/api/ingredients/categories` | GET | 获取分类列表 |

#### 食谱端点
| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/recipes` | GET | 获取食谱列表 |
| `/api/recipes/{id}` | GET | 获取食谱详情 |
| `/api/recipes/by-constitution` | GET | 按体质查询 |
| `/api/recipes/by-meal-type` | GET | 按餐次查询 |
| `/api/recipes/by-ingredient` | GET | 按食材查询 |

---

### 响应格式标准

```python
# 成功
{
    "code": 0,
    "data": {...},
    "message": "Success"
}

# 错误
{
    "code": -1,
    "message": "错误描述"
}

# 按体质查询食材的响应
{
    "code": 0,
    "data": {
        "constitution": "qi_deficiency",
        "constitution_name": "气虚质",
        "recommended": [
            {
                "id": 1,
                "name": "山药",
                "nature": "平",
                "taste": "甘",
                "efficacy": "补脾养胃..."
            }
        ],
        "avoided": [
            {
                "id": 2,
                "name": "山楂",
                "nature": "温",
                "contraindications": "气虚者慎用..."
            }
        ]
    }
}
```

---

### 开发检查清单

添加新食材时：
- [ ] 确认体质代码使用标准值（9种）
- [ ] 添加 `suitable_constitutions` 数组
- [ ] 添加 `avoid_constitutions` 数组（如有禁忌）
- [ ] 添加常用别名到 `aliases`
- [ ] 填写 `nature`（性味）和 `taste`（味道）

添加新食谱时：
- [ ] 确认 `meal_type` 值：`breakfast`, `lunch`, `dinner`, `snack`
- [ ] `ingredients` 格式：`[{"name": "山药", "amount": "100g"}]`
- [ ] `steps` 格式：`["步骤1描述", "步骤2描述"]`
- [ ] 添加 `suitable_constitutions`

搜索功能实现：
- [ ] 名称搜索使用 `ilike()`
- [ ] 别名搜索需要展开 JSON 数组
- [ ] 使用 `or_()` 组合多个条件
