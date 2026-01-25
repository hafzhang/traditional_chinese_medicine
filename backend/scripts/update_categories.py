#!/usr/bin/env python3
"""
更新食材分类脚本
根据前端标准分类更新CSV中的category列
"""

import csv
import shutil
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).parent.parent
SOURCE_DIR = BASE_DIR.parent / "source_data" / "ingredients"
CSV_FILE = SOURCE_DIR / "ingredients_data.csv"

# 标准分类（来自图片）
STANDARD_CATEGORIES = {
    "谷物",    # 谷物类
    "蔬菜",    # 蔬菜类
    "水果",    # 水果类
    "肉类",    # 肉类
    "海鲜",    # 海鲜类
    "药材",    # 药材类
    "调味品",  # 调味品类
    "坚果",    # 坚果类
    "菌藻",    # 菌藻类
    "豆类",    # 豆类
    "其他"     # 其他
}

# 当前分类到标准分类的映射
CATEGORY_MAPPING = {
    "蔬菜类": "蔬菜",
    "肉类": "肉类",
    "海鲜水产类": "海鲜",
    "水果类": "水果",
    "豆制品及豆类": "豆类",
    "米面杂粮类": "谷物",
    "菌菇类": "菌藻",
    "调料干货类": "调味品",
    "加工食品类": "其他",
    "其他类": "其他",
}

# 特殊食材需要手动指定分类（基于食材名称）
# 格式: {"食材名": "标准分类"}
SPECIAL_INGREDIENTS = {
    # 药材类（根据食材功效判断）
    "枸杞": "药材",
    "当归": "药材",
    "黄芪": "药材",
    "人参": "药材",
    "红枣": "药材",
    "桂圆": "药材",
    "金银花": "药材",
    "菊花": "药材",
    "百合": "药材",
    "莲子": "药材",
    "薏米": "药材",
    "茯苓": "药材",
    "陈皮": "药材",
    "山楂": "药材",
    "麦冬": "药材",
    "冬虫夏草": "药材",
    "灵芝": "药材",

    # 坚果类
    "核桃": "坚果",
    "杏仁": "坚果",
    "花生": "坚果",
    "腰果": "坚果",
    "开心果": "坚果",
    "榛子": "坚果",
    "松子": "坚果",
    "瓜子": "坚果",
    "芝麻": "坚果",
    "夏威夷果": "坚果",
    "碧根果": "坚果",
    "巴旦木": "坚果",
}


def update_categories():
    """更新CSV文件中的分类"""
    print("=" * 60)
    print("食材分类更新脚本")
    print("=" * 60)
    print()

    # 备份原文件
    backup_file = CSV_FILE.with_suffix('.csv.backup')
    shutil.copy2(CSV_FILE, backup_file)
    print(f"已备份原文件到: {backup_file}")

    # 读取CSV
    with open(CSV_FILE, 'r', encoding='gbk') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"读取到 {len(rows)} 条食材数据")
    print()

    # 统计分类变化
    category_stats = {}
    special_count = 0
    updated_count = 0

    for row in rows:
        old_category = row.get('category', '').strip()
        name = row.get('name', '').strip()

        # 优先使用特殊食材分类
        if name in SPECIAL_INGREDIENTS:
            new_category = SPECIAL_INGREDIENTS[name]
            special_count += 1
        # 使用映射表
        elif old_category in CATEGORY_MAPPING:
            new_category = CATEGORY_MAPPING[old_category]
        # 已经是标准分类
        elif old_category in STANDARD_CATEGORIES:
            new_category = old_category
        # 未分类的
        else:
            new_category = "其他"

        # 更新分类
        if row.get('category', '').strip() != new_category:
            row['category'] = new_category
            updated_count += 1

        # 统计
        if new_category not in category_stats:
            category_stats[new_category] = []
        category_stats[new_category].append(name)

    # 写入更新后的CSV
    with open(CSV_FILE, 'w', encoding='gbk', newline='') as f:
        fieldnames = rows[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"更新完成！共更新 {updated_count} 条记录")
    print(f"其中特殊分类食材: {special_count} 条")
    print()
    print("新分类统计:")
    for cat in sorted(category_stats.keys()):
        count = len(category_stats[cat])
        print(f"  {cat}: {count} 个食材")

    print()
    print("特殊分类食材示例:")
    for name, cat in sorted(SPECIAL_INGREDIENTS.items()):
        print(f"  {name} → {cat}")

    print()
    print("=" * 60)
    print("处理完成!")
    print("=" * 60)


if __name__ == "__main__":
    update_categories()
