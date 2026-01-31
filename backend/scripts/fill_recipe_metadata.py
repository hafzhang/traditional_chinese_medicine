#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
完善 dishes_list.xlsx 表格，添加以下字段:
- difficulty: 难度
- suitable_constitutions: 适合体质
- avoid_constitutions: 禁忌体质
- efficacy_tags: 功效标签
- solar_terms: 节气标签
"""

import pandas as pd
import json
import re
import os

# 9种体质列表
CONSTITUTIONS = [
    "peace", "qi_deficiency", "yang_deficiency", "yin_deficiency",
    "phlegm_damp", "damp_heat", "blood_stasis", "qi_depression", "special"
]

# 24节气
SOLAR_TERMS = [
    "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
    "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
    "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
    "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"
]

# 功效标签
EFFICACY_TAGS = [
    "补气", "补血", "滋阴", "助阳", "健脾", "养胃",
    "润肺", "止咳", "祛湿", "清热", "解表", "安神",
    "消食", "理气", "活血", "美容", "减肥", "增强免疫"
]

# 根据烹饪时间判断难度
def get_difficulty(costtime):
    """根据烹饪时间判断难度"""
    if pd.isna(costtime):
        return "简单"

    costtime_str = str(costtime)
    numbers = re.findall(r'\d+', costtime_str)
    if not numbers:
        return "简单"

    max_time = max(int(n) for n in numbers)
    if max_time <= 15:
        return "简单"
    elif max_time <= 40:
        return "中等"
    elif max_time <= 90:
        return "较难"
    else:
        return "困难"

# 根据食材和菜名推断适合的体质
def get_suitable_constitutions(row):
    """根据食材和菜名推断适合的体质"""
    title = str(row.get('title', ''))
    ingredients = str(row.get('QuantityIngredients', ''))
    desc = str(row.get('desc', ''))
    categories = str(row.get('cid', ''))

    all_text = f"{title} {ingredients} {desc} {categories}"
    suitable = ["peace"]  # 默认适合平和质

    # 根据关键词判断
    constitution_keywords = {
        "qi_deficiency": ["补气", "气虚", "乏力", "人参", "黄芪", "山药", "红枣", "桂圆"],
        "yang_deficiency": ["温补", "阳虚", "怕冷", "生姜", "羊肉", "辣椒", "胡椒"],
        "yin_deficiency": ["滋阴", "阴虚", "口干", "梨", "百合", "银耳", "鸭肉"],
        "phlegm_damp": ["祛湿", "化痰", "冬瓜", "薏米", "红豆", "陈皮"],
        "damp_heat": ["清热", "祛湿", "苦瓜", "黄瓜", "绿豆", "芹菜"],
        "blood_stasis": ["活血", "瘀血", "红花", "三七", "当归"],
        "qi_depression": ["理气", "疏肝", "郁", "玫瑰", "陈皮", "佛手"],
        "special": ["清淡", "易过敏", "忌口"]
    }

    for constitution, keywords in constitution_keywords.items():
        for keyword in keywords:
            if keyword in all_text:
                if constitution not in suitable:
                    suitable.append(constitution)
                break

    return suitable

# 根据食材判断禁忌体质
def get_avoid_constitutions(row):
    """根据食材判断禁忌体质"""
    title = str(row.get('title', ''))
    ingredients = str(row.get('QuantityIngredients', ''))
    all_text = f"{title} {ingredients}"
    avoid = []

    # 寒凉食物禁忌阳虚
    cold_keywords = ["绿豆", "苦瓜", "黄瓜", "西瓜", "梨", "冬瓜", "萝卜"]
    if any(kw in all_text for kw in cold_keywords):
        avoid.append("yang_deficiency")

    # 辛辣刺激食物禁忌阴虚、湿热
    spicy_keywords = ["辣椒", "胡椒", "花椒", "姜", "蒜", "羊肉"]
    if any(kw in all_text for kw in spicy_keywords):
        avoid.append("yin_deficiency")
        avoid.append("damp_heat")

    # 油腻食物禁忌湿热、痰湿
    greasy_keywords = ["油炸", "肥肉", "红烧", "糖醋"]
    if any(kw in all_text for kw in greasy_keywords):
        avoid.append("damp_heat")
        avoid.append("phlegm_damp")

    return list(set(avoid))

# 根据功效判断功效标签
def get_efficacy_tags(row):
    """根据功效判断功效标签"""
    title = str(row.get('title', ''))
    desc = str(row.get('desc', ''))
    ingredients = str(row.get('QuantityIngredients', ''))
    all_text = f"{title} {desc} {ingredients}"
    tags = []

    # 功效关键词映射
    efficacy_keywords = {
        "补气": ["补气", "气虚", "人参", "黄芪"],
        "补血": ["补血", "贫血", "当归", "红枣", "桂圆", "菠菜"],
        "滋阴": ["滋阴", "阴虚", "百合", "银耳", "梨"],
        "助阳": ["温阳", "补肾", "羊肉", "韭菜"],
        "健脾": ["健脾", "脾胃", "山药", "白术"],
        "养胃": ["养胃", "胃", "小米", "粥"],
        "润肺": ["润肺", "肺", "梨", "银耳", "百合"],
        "止咳": ["止咳", "咳嗽", "枇杷", "杏"],
        "祛湿": ["祛湿", "湿气", "薏米", "红豆", "冬瓜"],
        "清热": ["清热", "解毒", "绿豆", "苦瓜", "黄瓜"],
        "解表": ["感冒", "发热", "姜", "葱"],
        "安神": ["安神", "失眠", "莲子", "桂圆"],
        "消食": ["消食", "消化", "山楂", "麦芽"],
        "理气": ["理气", "陈皮", "佛手"],
        "活血": ["活血", "瘀血", "当归", "红花"],
        "美容": ["美容", "护肤", "胶原蛋白"],
        "减肥": ["减肥", "瘦身", "冬瓜", "黄瓜"],
        "增强免疫": ["免疫", "抵抗力", "维生素"]
    }

    for tag, keywords in efficacy_keywords.items():
        for keyword in keywords:
            if keyword in all_text:
                if tag not in tags:
                    tags.append(tag)
                break

    return tags

# 根据食材和季节判断节气标签
def get_solar_terms(row):
    """根据食材和季节判断节气标签"""
    ingredients = str(row.get('QuantityIngredients', ''))
    title = str(row.get('title', ''))
    all_text = f"{title} {ingredients}"
    terms = []

    # 春季食材
    spring_ingredients = ["春笋", "韭菜", "菠菜", "荠菜", "香椿"]
    for ingredient in spring_ingredients:
        if ingredient in all_text:
            terms.extend(["立春", "春分", "清明"])
            break

    # 夏季食材
    summer_ingredients = ["西瓜", "苦瓜", "黄瓜", "丝瓜", "冬瓜", "绿豆"]
    for ingredient in summer_ingredients:
        if ingredient in all_text:
            terms.extend(["立夏", "夏至", "大暑"])
            break

    # 秋季食材
    autumn_ingredients = ["梨", "百合", "银耳", "柿子", "螃蟹", "大闸蟹"]
    for ingredient in autumn_ingredients:
        if ingredient in all_text:
            terms.extend(["立秋", "秋分", "霜降"])
            break

    # 冬季食材
    winter_ingredients = ["羊肉", "萝卜", "白菜", "火锅", "冬笋"]
    for ingredient in winter_ingredients:
        if ingredient in all_text:
            terms.extend(["立冬", "冬至", "大寒"])
            break

    return list(set(terms))

# 主函数
def main():
    # 获取项目根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    input_file = os.path.join(project_root, 'source_data', 'dishes_list.xlsx')
    output_file = os.path.join(project_root, 'source_data', 'dishes_list_filled.xlsx')

    print("正在读取 Excel 文件...")
    print(f"文件路径: {input_file}")
    df = pd.read_excel(input_file)
    print(f"总共有 {len(df)} 条食谱")

    # 添加新列
    print("\n正在填充数据...")

    # 1. 难度
    print("填充 difficulty (难度)...")
    df['difficulty'] = df['costtime'].apply(get_difficulty)

    # 2. 适合体质
    print("填充 suitable_constitutions (适合体质)...")
    df['suitable_constitutions'] = df.apply(
        lambda row: json.dumps(get_suitable_constitutions(row), ensure_ascii=False),
        axis=1
    )

    # 3. 禁忌体质
    print("填充 avoid_constitutions (禁忌体质)...")
    df['avoid_constitutions'] = df.apply(
        lambda row: json.dumps(get_avoid_constitutions(row), ensure_ascii=False),
        axis=1
    )

    # 4. 功效标签
    print("填充 efficacy_tags (功效标签)...")
    df['efficacy_tags'] = df.apply(
        lambda row: json.dumps(get_efficacy_tags(row), ensure_ascii=False),
        axis=1
    )

    # 5. 节气标签
    print("填充 solar_terms (节气标签)...")
    df['solar_terms'] = df.apply(
        lambda row: json.dumps(get_solar_terms(row), ensure_ascii=False),
        axis=1
    )

    # 保存到新文件
    print(f"\n正在保存到 {output_file}...")
    df.to_excel(output_file, index=False, engine='openpyxl')

    print("\n完成！")

    # 显示示例数据
    print("\n=== 示例数据 (前5条) ===")
    for i in range(min(5, len(df))):
        print(f"\n【食谱 {i+1}】{df['title'].iloc[i]}")
        print(f"  难度: {df['difficulty'].iloc[i]}")
        print(f"  适合体质: {df['suitable_constitutions'].iloc[i]}")
        print(f"  禁忌体质: {df['avoid_constitutions'].iloc[i]}")
        print(f"  功效标签: {df['efficacy_tags'].iloc[i]}")
        print(f"  节气标签: {df['solar_terms'].iloc[i]}")

    # 统计信息
    print("\n=== 统计信息 ===")
    print("难度分布:")
    print(df['difficulty'].value_counts())
    print(f"\n总功效标签数: {sum(df['efficacy_tags'].apply(lambda x: len(json.loads(x))))}")
    print(f"总节气标签数: {sum(df['solar_terms'].apply(lambda x: len(json.loads(x))))}")

if __name__ == '__main__':
    main()
