# id: sqlite-json
# name: SQLite JSON 列查询模式
# description: 提供 SQLite 数据库中 JSON 列的正确查询方式、contains() 方法使用、会话管理模式
# version: 1.0.0
# author: Claude Code
# tags: [database, sqlite, json, sqlalchemy]

---

## SQLite JSON 列查询模式 Skill

### 项目数据库配置

```python
# 开发环境: SQLite
# 测试环境: 内存 SQLite
# 生产环境: PostgreSQL

# 连接配置
DATABASE_URL = "sqlite:///./tcm.db"

# SQLite 特殊配置
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite 必需
)
```

---

### JSON 列类型定义

```python
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ExampleModel(Base):
    __tablename__ = "examples"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    aliases = Column(JSON, nullable=False, default=list)  # 别名数组
    tags = Column(JSON, nullable=False, default=list)     # 标签数组
    metadata = Column(JSON, nullable=False, default=dict)  # 元数据字典
```

---

### JSON 数组查询

#### ✅ 正确方式：使用 `.contains()`

```python
# 查询 aliases 数组中包含 "山药" 的记录
query = session.query(ExampleModel).filter(
    ExampleModel.aliases.contains("山药")
)

# 查询 suitable_constitutions 中包含 "qi_deficiency" 的记录
query = session.query(Ingredient).filter(
    Ingredient.suitable_constitutions.contains("qi_deficiency")
)

# 多个条件组合（OR）
from sqlalchemy import or_
query = session.query(Ingredient).filter(
    or_(
        Ingredient.suitable_constitutions.contains("qi_deficiency"),
        Ingredient.suitable_constitutions.contains("yang_deficiency")
    )
)
```

#### ❌ 错误方式：使用 `.like()`

```python
# 错误：LIKE 查询在 SQLite JSON 列上不可靠
query = session.query(ExampleModel).filter(
    ExampleModel.aliases.like("%山药%")
)
# 可能匹配失败或返回错误结果
```

---

### JSON 字典查询

```python
# 假设 metadata 格式为: {"author": "张三", "version": "1.0"}

# PostgreSQL 可以这样查询（不适用于 SQLite）
# query = session.query(ExampleModel).filter(
#     ExampleModel.metadata["author"].astext == "张三"
# )

# SQLite 替代方案：使用 Python 过滤
results = session.query(ExampleModel).all()
filtered = [r for r in results if r.metadata.get("author") == "张三"]
```

---

### 创建 JSON 字段数据

```python
# 创建新记录
ingredient = Ingredient(
    name="山药",
    aliases=["怀山药", "淮山", "薯蓣"],        # JSON 数组
    suitable_constitutions=["qi_deficiency"],  # JSON 数组
    avoid_constitutions=[],                    # 空数组
    metadata={"source": "中医典籍", "verified": True}  # JSON 字典
)
session.add(ingredient)
session.commit()
```

---

### 更新 JSON 字段

```python
# 方法1：整体替换
ingredient = session.query(Ingredient).first()
ingredient.aliases = ["怀山药", "淮山", "薯蓣", "山芋"]
session.commit()

# 方法2：追加到数组（Python 操作）
ingredient = session.query(Ingredient).first()
if "新别名" not in ingredient.aliases:
    ingredient.aliases.append("新别名")
session.commit()

# 方法3：从数组移除
ingredient = session.query(Ingredient).first()
if "旧别名" in ingredient.aliases:
    ingredient.aliases.remove("旧别名")
session.commit()
```

---

### 数据库会话管理模式

```python
from api.database import SessionLocal, get_db

# 方式1：FastAPI 依赖注入（推荐）
@app.get("/ingredients/{ingredient_id}")
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    return ingredient
# 会话自动管理，无需手动关闭

# 方式2：手动管理
def process_ingredients():
    db = SessionLocal()
    try:
        ingredients = db.query(Ingredient).all()
        # 处理数据...
        db.commit()  # 提交更改
    except Exception as e:
        db.rollback()  # 回滚
        raise
    finally:
        db.close()  # 关闭会话

# 方式3：上下文管理器（推荐用于脚本）
from contextlib import contextmanager

@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# 使用
with get_db_session() as db:
    ingredients = db.query(Ingredient).all()
```

---

### 服务层会话模式

```python
class IngredientService:
    def get_ingredient_by_id(self, ingredient_id: int, db: Session) -> Optional[Ingredient]:
        """
        服务层方法必须接收 db: Session 参数
        不要在服务内部创建会话
        """
        return db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()

    def update_ingredient_aliases(
        self,
        ingredient_id: int,
        new_aliases: List[str],
        db: Session
    ) -> bool:
        """更新食材别名"""
        ingredient = db.query(Ingredient).filter(
            Ingredient.id == ingredient_id
        ).first()

        if not ingredient:
            return False

        ingredient.aliases = new_aliases
        db.commit()
        db.refresh(ingredient)
        return True
```

---

### 测试中的 JSON 列

```python
def test_search_by_aliases(db_session):
    """测试通过别名搜索"""
    # Arrange: 创建带别名的数据
    ingredient = Ingredient(
        name="山药",
        aliases=["怀山药", "淮山", "薯蓣"]
    )
    db_session.add(ingredient)
    db_session.commit()

    # Act: 查询（注意：contains 在 SQLite 中用于 JSON 数组）
    result = db_session.query(Ingredient).filter(
        Ingredient.aliases.contains("怀山药")
    ).first()

    # Assert
    assert result is not None
    assert result.name == "山药"

def test_constitution_filter(db_session):
    """测试体质筛选"""
    # Arrange
    ingredient = Ingredient(
        name="山药",
        suitable_constitutions=["qi_deficiency", "yang_deficiency"]
    )
    db_session.add(ingredient)
    db_session.commit()

    # Act
    result = db_session.query(Ingredient).filter(
        Ingredient.suitable_constitutions.contains("qi_deficiency")
    ).all()

    # Assert
    assert len(result) == 1
    assert result[0].name == "山药"
```

---

### 常见问题与解决方案

#### 问题1：JSON 列查询返回空结果

```python
# ❌ 错误
query = session.query(Ingredient).filter(
    Ingredient.aliases.like("%山药%")
)

# ✅ 正确
query = session.query(Ingredient).filter(
    Ingredient.aliases.contains("山药")
)
```

#### 问题2：JSON 数组包含对象时的查询

```python
# 假设结构: [{"name": "张三", "role": "author"}]

# SQLite 无法直接查询
# 解决方案：使用字符串匹配或 Python 过滤
results = session.query(Book).all()
filtered = [
    b for b in results
    if any(a.get("name") == "张三" for a in b.authors)
]
```

#### 问题3：测试数据未回滚

```python
# ❌ 错误：在测试中提交
def test_something(db_session):
    ingredient = Ingredient(name="测试")
    db_session.add(ingredient)
    db_session.commit()  # 错误！会永久保存

# ✅ 正确：让 fixture 自动回滚
def test_something(db_session):
    ingredient = Ingredient(name="测试")
    db_session.add(ingredient)
    db_session.flush()  # 刷新以获取 ID，但不提交
    # 测试结束后 fixture 自动回滚
```

---

### SQLite vs PostgreSQL JSON 差异

| 功能 | SQLite | PostgreSQL |
|------|--------|------------|
| JSON 类型 | `JSON` (文本存储) | `JSONB` (二进制存储) |
| 数组包含查询 | `.contains()` | `.contains()` |
| 字典键查询 | 不支持 | `col["key"].astext` |
| 索引支持 | 不支持 | 支持 (GIN) |
| 性能 | 较慢 | 较快 (JSONB) |

---

### 开发检查清单

使用 JSON 列时：
- [ ] 数组查询使用 `.contains(value)`
- [ ] 不要使用 `.like()` 查询 JSON 列
- [ ] 服务层方法接收 `db: Session` 参数
- [ ] 使用 `db.flush()` 而非 `db.commit()` 在测试中
- [ ] JSON 数组初始化使用 `default=list`
- [ ] JSON 字典初始化使用 `default=dict`
- [ ] 生产环境考虑使用 PostgreSQL 的 JSONB

编写测试时：
- [ ] 测试 JSON 数组的 `contains()` 查询
- [ ] 测试空数组 `[]` 的情况
- [ ] 测试 JSON 字典的 get() 方法
- [ ] 不要在测试中调用 `commit()`
