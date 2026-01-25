#!/usr/bin/env python3
"""
为CSV添加使用指导和搭配宜忌列，并生成相关数据
"""

import csv
import shutil
import random
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).parent.parent
SOURCE_DIR = BASE_DIR.parent / "source_data" / "ingredients"
CSV_FILE = SOURCE_DIR / "ingredients_data.csv"

# 使用指导模板（根据性味和功效生成）
USAGE_GUIDE_TEMPLATES = {
    "寒": {
        "蔬菜": "可凉拌、炒食、煮汤，夏季食用最佳，建议每周2-3次，每次50-100g",
        "水果": "直接食用或榨汁，夏季食用最佳，建议每日1个",
        "海鲜": "清蒸、煮汤，避免生食，建议每周1-2次，每次100-150g",
        "default": "炒食、煮汤，建议适量食用，不宜过量"
    },
    "凉": {
        "蔬菜": "可凉拌、炒食、煮汤，夏季食用最佳，建议每周2-3次，每次50-100g",
        "水果": "直接食用或榨汁，夏季食用最佳，建议每日1个",
        "default": "炒食、煮汤，建议适量食用"
    },
    "平": {
        "蔬菜": "可炒食、煮汤、凉拌，四季皆宜，建议每周2-3次，每次50-100g",
        "水果": "直接食用或榨汁，四季皆宜，建议每日1个",
        "肉类": "炒食、炖煮、蒸制，建议每周2-3次，每次100-150g",
        "谷物": "煮粥、蒸饭、制作面食，每日食用，每次50-100g",
        "豆类": "煮粥、炖汤、制作豆制品，建议每周2-3次，每次50-100g",
        "海鲜": "清蒸、煮汤、炒食，建议每周1-2次，每次100-150g",
        "菌藻": "炒食、煮汤、凉拌，建议每周2-3次，每次30-50g",
        "调味品": "调味提鲜，适量使用，每次3-5g",
        "default": "日常食用，适量即可"
    },
    "温": {
        "蔬菜": "炒食、煮汤，冬季食用最佳，建议每周2-3次，每次50-100g",
        "水果": "直接食用，建议每日1个，体质虚寒者适宜",
        "肉类": "炖煮、炒食、烧烤，建议每周2-3次，每次100-150g",
        "谷物": "煮粥、蒸饭，冬季食用最佳，每日食用，每次50-100g",
        "海鲜": "清蒸、煮汤，建议每周1-2次，每次100-150g",
        "default": "炒食、炖煮，体质虚寒者适宜"
    },
    "热": {
        "default": "煮汤、炖煮，体质虚寒者适宜，建议少量食用"
    }
}

# 搭配宜忌模板
COMPATIBILITY_TEMPLATES = {
    "蔬菜": {
        "compatible": "宜与蛋类、豆制品、肉类搭配，营养更均衡",
        "incompatible": "不宜与富含维生素C分解酶的食物同食"
    },
    "水果": {
        "compatible": "宜饭后食用，可搭配酸奶、坚果",
        "incompatible": "不宜与海鲜、萝卜同食，易引起消化不良"
    },
    "肉类": {
        "compatible": "宜与蔬菜、菌菇类搭配，有助于消化吸收",
        "incompatible": "不宜与富含鞣酸的水果（如柿子）同食"
    },
    "海鲜": {
        "compatible": "宜与蔬菜、豆腐搭配，可平衡营养",
        "incompatible": "不宜与富含鞣酸的水果同食，不易消化"
    },
    "谷物": {
        "compatible": "宜与豆类、蔬菜搭配，营养互补",
        "incompatible": "无特殊禁忌"
    },
    "豆类": {
        "compatible": "宜与谷物、蔬菜搭配，蛋白质互补",
        "incompatible": "不宜与生菠菜、空心菜同食，影响钙吸收"
    },
    "菌藻": {
        "compatible": "宜与肉类、蛋类搭配，提升鲜味",
        "incompatible": "不宜与寒凉食物大量同食"
    },
    "调味品": {
        "compatible": "适量使用，提鲜增香",
        "incompatible": "不宜过量，以免掩盖食材本味"
    },
    "default": {
        "compatible": "可与多种食材搭配",
        "incompatible": "适量食用，注意个人体质"
    }
}

# 特定食材的详细搭配（覆盖模板）
SPECIFIC_COMPATIBILITY = {
    "山药": {
        "compatible": "宜与红枣、莲子、百合搭配，健脾益气",
        "incompatible": "不宜与碱性药物同服，不宜与鲤鱼同食"
    },
    "红枣": {
        "compatible": "宜与桂圆、枸杞、莲子搭配，补气养血",
        "incompatible": "不宜与黄瓜、萝卜、动物肝脏同食"
    },
    "莲子": {
        "compatible": "宜与百合、红枣、山药搭配，健脾养心",
        "incompatible": "不宜与猪肚同食"
    },
    "百合": {
        "compatible": "宜与莲子、银耳、枸杞搭配，润肺安神",
        "incompatible": "不宜与羊肉同食"
    },
    "薏米": {
        "compatible": "宜与红豆、冬瓜、山药搭配，健脾祛湿",
        "incompatible": "孕妇慎用，不宜过量"
    },
    "桂圆": {
        "compatible": "宜与红枣、枸杞、莲子搭配，补气养血",
        "incompatible": "体内有热、上火者慎用"
    },
    "山楂": {
        "compatible": "宜与红枣、枸杞、麦芽搭配，消食化积",
        "incompatible": "不宜与人参、黄瓜同食，脾胃虚弱者慎用"
    },
    "花生": {
        "compatible": "宜与红枣、猪蹄搭配，补血养颜",
        "incompatible": "不宜与香瓜、螃蟹同食"
    },
    "核桃": {
        "compatible": "宜与红枣、芝麻搭配，补脑益智",
        "incompatible": "不宜与白酒同食"
    },
    "生姜": {
        "compatible": "宜与红糖、红枣搭配，温中散寒",
        "incompatible": "不宜与兔肉、酒同食"
    },
    "大蒜": {
        "compatible": "宜与生姜、醋搭配，杀菌消毒",
        "incompatible": "不宜与蜂蜜同食"
    },
    "韭菜": {
        "compatible": "宜与鸡蛋、虾米搭配，补肾壮阳",
        "incompatible": "不宜与牛肉、蜂蜜同食"
    },
    "萝卜": {
        "compatible": "宜与排骨、豆腐搭配，消食化痰",
        "incompatible": "不宜与人参、胡萝卜同食"
    },
    "胡萝卜": {
        "compatible": "宜与肉类、排骨搭配，补肝明目",
        "incompatible": "不宜与萝卜、酒同食"
    },
    "南瓜": {
        "compatible": "宜与小米、红枣搭配，健脾养胃",
        "incompatible": "不宜与羊肉同食"
    },
    "绿豆": {
        "compatible": "宜与冰糖、百合搭配，清热解毒",
        "incompatible": "不宜与鲤鱼、榧子同食"
    },
    "红豆": {
        "compatible": "宜与薏米、红枣搭配，健脾利湿",
        "incompatible": "不宜与羊肝同食"
    },
    "黑豆": {
        "compatible": "宜与红枣、桂圆搭配，补肾益气",
        "incompatible": "不宜与蓖麻子、厚朴同食"
    },
    "豆腐": {
        "compatible": "宜与鱼、肉、蔬菜搭配，营养互补",
        "incompatible": "不宜与菠菜、蜂蜜同食"
    },
    "菠菜": {
        "compatible": "宜与鸡蛋、猪肝搭配，补血养血",
        "incompatible": "不宜与豆腐、鳝鱼同食"
    },
    "芹菜": {
        "compatible": "宜与西红柿、红枣搭配，降压安神",
        "incompatible": "不宜与黄瓜、鸡肉同食"
    },
    "西红柿": {
        "compatible": "宜与鸡蛋、牛肉搭配，营养丰富",
        "incompatible": "不宜与黄瓜、红薯同食"
    },
    "黄瓜": {
        "compatible": "宜与木耳、西红柿搭配，清热利水",
        "incompatible": "不宜与花生、西红柿同食"
    },
    "冬瓜": {
        "compatible": "宜与排骨、海带搭配，利水消肿",
        "incompatible": "不宜与鲫鱼同食（久服）"
    },
    "丝瓜": {
        "compatible": "宜与鸡蛋、虾米搭配，清热化痰",
        "incompatible": "无特殊禁忌"
    },
    "苦瓜": {
        "compatible": "宜与鸡蛋、瘦肉搭配，清热解暑",
        "incompatible": "脾胃虚寒者慎用"
    },
    "茄子": {
        "compatible": "宜与肉类、大蒜搭配，保护血管",
        "incompatible": "不宜与螃蟹同食"
    },
    "辣椒": {
        "compatible": "宜与肉类、蛋类搭配，增进食欲",
        "incompatible": "火热体质、痔疮患者慎用"
    },
    "猪肉": {
        "compatible": "宜与白菜、萝卜、木耳搭配",
        "incompatible": "不宜与豆类、香菜同食"
    },
    "牛肉": {
        "compatible": "宜与土豆、胡萝卜、洋葱搭配",
        "incompatible": "不宜与韭菜、栗子同食"
    },
    "羊肉": {
        "compatible": "宜与胡萝卜、生姜、当归搭配",
        "incompatible": "不宜与西瓜、南瓜同食"
    },
    "鸡肉": {
        "compatible": "宜与木耳、枸杞、红枣搭配",
        "incompatible": "不宜与鲤鱼、大蒜同食"
    },
    "鸭肉": {
        "compatible": "宜与冬瓜、山药搭配，清热滋阴",
        "incompatible": "不宜与栗子、木耳同食"
    },
    "鱼肉": {
        "compatible": "宜与豆腐、生姜搭配，营养互补",
        "incompatible": "不宜与咸菜、甘草同食"
    },
    "虾": {
        "compatible": "宜与韭菜、芹菜搭配，补肾壮阳",
        "incompatible": "不宜与猪肉、葡萄同食"
    },
    "螃蟹": {
        "compatible": "宜与生姜、醋搭配，驱寒杀菌",
        "incompatible": "不宜与梨、柿子、花生同食"
    }
}


def generate_usage_guide(nature, category):
    """生成使用指导"""
    if nature in USAGE_GUIDE_TEMPLATES:
        if category in USAGE_GUIDE_TEMPLATES[nature]:
            return USAGE_GUIDE_TEMPLATES[nature][category]
        else:
            return USAGE_GUIDE_TEMPLATES[nature]["default"]
    return USAGE_GUIDE_TEMPLATES["平"]["default"]


def generate_compatibility(name, category):
    """生成搭配宜忌"""
    if name in SPECIFIC_COMPATIBILITY:
        return SPECIFIC_COMPATIBILITY[name]
    if category in COMPATIBILITY_TEMPLATES:
        return COMPATIBILITY_TEMPLATES[category]
    return COMPATIBILITY_TEMPLATES["default"]


def add_usage_and_compatibility():
    """添加使用指导和搭配宜忌列"""
    print("=" * 60)
    print("添加使用指导和搭配宜忌列")
    print("=" * 60)
    print()

    # 备份原文件
    backup_file = CSV_FILE.with_suffix('.csv.backup3')
    shutil.copy2(CSV_FILE, backup_file)
    print(f"已备份原文件到: {backup_file}")

    # 读取CSV
    with open(CSV_FILE, 'r', encoding='gbk') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"读取到 {len(rows)} 条食材数据")
    print()

    # 添加新列数据
    updated_rows = []
    for row in rows:
        name = row.get('name', '').strip()
        nature = row.get('nature', '').strip()
        category = row.get('category', '').strip()

        # 生成使用指导
        usage_guide = generate_usage_guide(nature, category)

        # 生成搭配宜忌
        compat = generate_compatibility(name, category)

        # 添加新列
        row['usage_guide'] = usage_guide
        row['compatibility'] = f"宜配：{compat['compatible']}；忌配：{compat['incompatible']}"

        updated_rows.append(row)

    # 写入更新后的CSV
    with open(CSV_FILE, 'w', encoding='gbk', newline='') as f:
        fieldnames = list(updated_rows[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print("添加完成！")
    print()
    print("新增列:")
    print(f"  - usage_guide: 使用指导")
    print(f"  - compatibility: 搭配宜忌")
    print()
    print("示例数据:")
    for i, row in enumerate(updated_rows[:5]):
        print(f"\n{row['name']}:")
        print(f"  使用指导: {row['usage_guide']}")
        print(f"  搭配宜忌: {row['compatibility']}")

    print()
    print("=" * 60)
    print("处理完成!")
    print("=" * 60)


if __name__ == "__main__":
    add_usage_and_compatibility()
