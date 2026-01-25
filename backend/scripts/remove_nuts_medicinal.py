#!/usr/bin/env python3
"""
移除坚果和药材分类，重新分配食材
"""

import csv
import shutil
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
SOURCE_DIR = BASE_DIR.parent / "source_data" / "ingredients"
CSV_FILE = SOURCE_DIR / "ingredients_data.csv"

# 坚果和药材重新分类映射
RECLASSIFY_MAPPING = {
    # 坚果类
    "花生": "豆类",

    # 药材类
    "百合": "蔬菜",
    "桂圆": "水果",
    "红枣": "水果",
    "莲子": "豆类",
    "山楂": "水果",
    "薏米": "谷物",
}


def remove_nuts_medicinal_categories():
    """移除坚果和药材分类，重新分配食材"""
    print("=" * 60)
    print("移除坚果和药材分类")
    print("=" * 60)
    print()

    # 备份原文件
    backup_file = CSV_FILE.with_suffix('.csv.backup2')
    shutil.copy2(CSV_FILE, backup_file)
    print(f"已备份原文件到: {backup_file}")

    # 读取CSV
    with open(CSV_FILE, 'r', encoding='gbk') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"读取到 {len(rows)} 条食材数据")
    print()

    # 统计和更新
    updated_count = 0
    reclassify_stats = {}

    for row in rows:
        name = row.get('name', '').strip()
        category = row.get('category', '').strip()

        # 检查是否需要重新分类
        if name in RECLASSIFY_MAPPING:
            old_category = category
            new_category = RECLASSIFY_MAPPING[name]

            row['category'] = new_category
            updated_count += 1

            if old_category not in reclassify_stats:
                reclassify_stats[old_category] = []
            reclassify_stats[old_category].append({
                'name': name,
                'old': old_category,
                'new': new_category
            })

    # 写入更新后的CSV
    with open(CSV_FILE, 'w', encoding='gbk', newline='') as f:
        fieldnames = rows[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"更新完成！共重新分类 {updated_count} 个食材")
    print()
    print("重新分类详情:")
    for old_cat, items in reclassify_stats.items():
        print(f"\n从 [{old_cat}] 重新分配:")
        for item in items:
            print(f"  {item['name']} → {item['new']}")

    # 统计新分类
    print()
    print("=" * 60)
    new_category_stats = {}
    for row in rows:
        cat = row.get('category', '').strip()
        if cat not in new_category_stats:
            new_category_stats[cat] = 0
        new_category_stats[cat] += 1

    print("更新后的分类统计:")
    for cat, count in sorted(new_category_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count}")

    print()
    print("=" * 60)
    print("处理完成!")
    print("=" * 60)


if __name__ == "__main__":
    remove_nuts_medicinal_categories()
