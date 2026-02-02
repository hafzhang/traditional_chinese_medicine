"""
诊断导入失败的原因
测试前10条可能失败的记录
"""

import sys
import pandas as pd
from pathlib import Path
import traceback

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from api.database import SessionLocal, Base, engine
from scripts.import_recipes import import_single_recipe

# 初始化数据库表
from api.models import Recipe, RecipeIngredient, RecipeStep, Ingredient
Base.metadata.create_all(bind=engine)
print("[OK] Database tables initialized")

# 数据文件路径
excel_path = 'C:/Users/Administrator/Desktop/traditional_chinese_medicine/source_data/dishes_list_ai_filled.xlsx'

# 读取 Excel
df = pd.read_excel(excel_path, sheet_name='Sheet1', engine='openpyxl')
df = df.dropna(subset=['title'])

print(f"总共 {len(df)} 条记录")

# 创建数据库会话
db = SessionLocal()

# 测试前20条记录
errors = []
success = 0
skipped = 0

for idx, row in df.head(20).iterrows():
    name = str(row.get('title', '')).strip()
    print(f"\n--- 测试 {idx + 1}: {name} ---")

    try:
        recipe = import_single_recipe(row, db)
        if recipe is None:
            print(f"  → 跳过 (已存在或空名称)")
            skipped += 1
        else:
            print(f"  → 成功导入 (ID: {recipe.id})")
            success += 1
            # 回滚测试导入
            db.rollback()
    except Exception as e:
        error_msg = f"{name}: {str(e)}"
        print(f"  → 失败: {str(e)}")
        errors.append(error_msg)
        traceback.print_exc()
        db.rollback()

db.close()

print(f"\n{'='*60}")
print(f"测试结果 (前20条)")
print(f"{'='*60}")
print(f"成功:   {success}")
print(f"跳过:   {skipped}")
print(f"失败:   {len(errors)}")

if errors:
    print(f"\n失败详情:")
    for error in errors:
        print(f"  - {error}")
