#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
基于中医理论和权威食材数据库的食谱元数据填充脚本 v2.0

改进点：
1. 使用基于《中国药典》、《本草纲目》的权威食材数据库
2. 综合分析所有食材，而非简单关键词匹配
3. 增加置信度评分
4. 改进难度评估算法（多维度）
"""

import pandas as pd
import json
import re
import os
import sys

# 添加脚本目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ingredient_database import (
    INGREDIENT_TCM_DATABASE,
    SOLAR_TERM_INGREDIENTS,
    CONSTITUTION_INGREDIENTS
)

# 9种体质代码
CONSTITUTIONS = [
    "peace", "qi_deficiency", "yang_deficiency", "yin_deficiency",
    "phlegm_damp", "damp_heat", "blood_stasis", "qi_depression", "special"
]

# 食材别名映射（处理同义词）
INGREDIENT_ALIASES = {
    "土豆": "红薯",
    "洋芋": "红薯",
    "蕃茄": "西红柿",
    "番茄": "西红柿",
    "青椒": "辣椒",
    "菜椒": "辣椒",
    "花菜": "白菜",
    "包菜": "白菜",
    "圆白菜": "白菜",
    "卷心菜": "白菜",
    "金针菇": "香菇",
    "木耳": "木耳",
    "黑木耳": "木耳",
    "白木耳": "银耳",
    "银耳": "银耳",
}

# 解析食材列表
def parse_ingredients(ingredients_text):
    """从食材文本中提取食材名称"""
    if pd.isna(ingredients_text):
        return []

    ingredients_text = str(ingredients_text)

    # 提取中文食材名（2-4个汉字）
    ingredient_pattern = r'[\u4e00-\u9fa5]{2,4}'
    matches = re.findall(ingredient_pattern, ingredients_text)

    # 过滤掉明显不是食材的词
    not_ingredients = ['分钟', '个', '克', '毫升', '适量', '少许', '做法', '步骤', '贴士']
    ingredients = [m for m in matches if m not in not_ingredients]

    # 别名规范化
    normalized = []
    for ing in ingredients:
        if ing in INGREDIENT_ALIASES:
            normalized.append(INGREDIENT_ALIASES[ing])
        else:
            normalized.append(ing)

    return list(set(normalized))  # 去重

# 分析食谱的适合体质
def analyze_suitable_constitutions(ingredients_list):
    """基于食材数据库分析适合的体质"""
    constitution_scores = {c: 0 for c in CONSTITUTIONS}

    for ingredient in ingredients_list:
        if ingredient in INGREDIENT_TCM_DATABASE:
            data = INGREDIENT_TCM_DATABASE[ingredient]

            # 根据食材的适合体质加分
            for constitution in data.get("suitable", []):
                if constitution in constitution_scores:
                    constitution_scores[constitution] += 2

    # 获取得分最高的体质
    max_score = max(constitution_scores.values())

    # 所有得分 >= 最高分*0.6 的体质都纳入
    threshold = max(1, max_score * 0.6)
    suitable = [c for c, score in constitution_scores.items() if score >= threshold]

    # 如果没有任何匹配，默认平和质
    if not suitable or max_score == 0:
        return ["peace"]

    return suitable

# 分析食谱的禁忌体质
def analyze_avoid_constitutions(ingredients_list):
    """基于食材数据库分析禁忌体质"""
    constitution_scores = {c: 0 for c in CONSTITUTIONS}

    for ingredient in ingredients_list:
        if ingredient in INGREDIENT_TCM_DATABASE:
            data = INGREDIENT_TCM_DATABASE[ingredient]

            # 根据食材的禁忌体质加分（负分）
            for constitution in data.get("avoid", []):
                if constitution in constitution_scores:
                    constitution_scores[constitution] -= 2

            # 根据食材性质推断
            nature = data.get("nature", "")
            if nature in ["寒", "凉"]:
                constitution_scores["yang_deficiency"] -= 1
            elif nature in ["温", "热"]:
                constitution_scores["yin_deficiency"] -= 1
                constitution_scores["damp_heat"] -= 1

    # 负分的体质为禁忌
    avoid = [c for c, score in constitution_scores.items() if score < -1]

    return avoid

# 分析食谱的功效标签
def analyze_efficacy_tags(ingredients_list):
    """基于食材数据库分析功效标签"""
    efficacy_counter = {}

    for ingredient in ingredients_list:
        if ingredient in INGREDIENT_TCM_DATABASE:
            data = INGREDIENT_TCM_DATABASE[ingredient]

            # 累加功效
            for efficacy in data.get("efficacy", []):
                if efficacy not in efficacy_counter:
                    efficacy_counter[efficacy] = 0
                efficacy_counter[efficacy] += 1

    # 按出现次数排序，返回前5个
    sorted_eff = sorted(efficacy_counter.items(), key=lambda x: x[1], reverse=True)
    return [eff[0] for eff in sorted_eff[:5]]

# 分析食谱的节气标签
def analyze_solar_terms(ingredients_list):
    """基于食材分析节气标签"""
    term_scores = {}

    # 遍历所有节气
    for term, term_ingredients in SOLAR_TERM_INGREDIENTS.items():
        score = 0
        for ingredient in ingredients_list:
            if ingredient in term_ingredients:
                score += 1

        if score > 0:
            term_scores[term] = score

    # 按分数排序，返回前3个
    if not term_scores:
        return []

    sorted_terms = sorted(term_scores.items(), key=lambda x: x[1], reverse=True)
    return [term[0] for term in sorted_terms[:3]]

# 改进的难度评估
def calculate_difficulty_improved(row):
    """多维度评估食谱难度"""
    score = 0

    # 1. 烹饪时间 (40分)
    costtime = str(row.get('costtime', ''))
    numbers = re.findall(r'\d+', costtime)
    if numbers:
        max_time = max(int(n) for n in numbers)
        if max_time > 90: score += 40
        elif max_time > 40: score += 30
        elif max_time > 15: score += 20
        else: score += 10

    # 2. 步骤复杂度 (30分)
    steptext = str(row.get('steptext', ''))
    step_count = steptext.count('#') + steptext.count('。')
    if step_count > 10: score += 30
    elif step_count > 5: score += 20
    elif step_count > 3: score += 10
    else: score += 5

    # 3. 食材处理复杂度 (30分)
    ingredients = str(row.get('QuantityIngredients', ''))
    if "切" in steptext: score += 5
    if "腌制" in steptext or "腌" in steptext: score += 5
    if "焯水" in steptext or "过水" in steptext: score += 5
    if "挂糊" in steptext or "裹粉" in steptext: score += 15
    if "打发" in steptext: score += 15

    # 转换为等级
    if score >= 80: return "困难"
    elif score >= 60: return "较难"
    elif score >= 40: return "中等"
    else: return "简单"

# 计算置信度
def calculate_confidence(ingredients_list, analysis_result):
    """计算分析结果的置信度"""
    confidence = 0

    # 1. 食材识别率 (40分)
    identified_count = sum(1 for ing in ingredients_list if ing in INGREDIENT_TCM_DATABASE)
    total_count = len(ingredients_list) if ingredients_list else 1
    recognition_rate = identified_count / total_count
    confidence += recognition_rate * 40

    # 2. 分析完整性 (30分)
    if analysis_result.get('suitable'): confidence += 10
    if analysis_result.get('efficacy'): confidence += 10
    if analysis_result.get('solar_terms'): confidence += 10

    # 3. 数据一致性 (30分)
    # 检查适合体质和禁忌体质是否冲突
    suitable = set(analysis_result.get('suitable', []))
    avoid = set(analysis_result.get('avoid', []))
    if suitable and avoid:
        overlap = suitable & avoid
        if not overlap:
            confidence += 30
        else:
            confidence += 10  # 有冲突，扣分
    else:
        confidence += 20

    return min(100, int(confidence))

# 主函数
def main():
    # 获取项目根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    input_file = os.path.join(project_root, 'source_data', 'dishes_list.xlsx')
    output_file = os.path.join(project_root, 'source_data', 'dishes_list_filled_v2.xlsx')

    print("=" * 60)
    print("食谱元数据填充脚本 v2.0")
    print("基于《中国药典》、《本草纲目》等权威典籍")
    print("=" * 60)

    print("\n正在读取 Excel 文件...")
    print(f"文件路径: {input_file}")
    df = pd.read_excel(input_file)
    print(f"总共有 {len(df)} 条食谱")

    # 添加新列
    print("\n正在填充数据...")

    results = []

    # 批量处理
    batch_size = 100
    for i in range(0, len(df), batch_size):
        batch_end = min(i + batch_size, len(df))
        print(f"处理进度: {i+1}-{batch_end}/{len(df)}")

        for idx in range(i, batch_end):
            row = df.iloc[idx]

            # 解析食材
            ingredients_list = parse_ingredients(row.get('QuantityIngredients', ''))

            # 分析各项数据
            suitable = analyze_suitable_constitutions(ingredients_list)
            avoid = analyze_avoid_constitutions(ingredients_list)
            efficacy = analyze_efficacy_tags(ingredients_list)
            solar_terms = analyze_solar_terms(ingredients_list)
            difficulty = calculate_difficulty_improved(row)

            # 计算置信度
            analysis = {
                'suitable': suitable,
                'avoid': avoid,
                'efficacy': efficacy,
                'solar_terms': solar_terms
            }
            confidence = calculate_confidence(ingredients_list, analysis)

            results.append({
                'difficulty': difficulty,
                'suitable_constitutions': json.dumps(suitable, ensure_ascii=False),
                'avoid_constitutions': json.dumps(avoid, ensure_ascii=False),
                'efficacy_tags': json.dumps(efficacy, ensure_ascii=False),
                'solar_terms': json.dumps(solar_terms, ensure_ascii=False),
                'confidence': confidence
            })

    # 添加结果到 DataFrame
    df['difficulty'] = [r['difficulty'] for r in results]
    df['suitable_constitutions'] = [r['suitable_constitutions'] for r in results]
    df['avoid_constitutions'] = [r['avoid_constitutions'] for r in results]
    df['efficacy_tags'] = [r['efficacy_tags'] for r in results]
    df['solar_terms'] = [r['solar_terms'] for r in results]
    df['confidence'] = [r['confidence'] for r in results]

    # 保存到新文件
    print(f"\n正在保存到 {output_file}...")
    df.to_excel(output_file, index=False, engine='openpyxl')

    print("\n" + "=" * 60)
    print("处理完成！")
    print("=" * 60)

    # 显示示例数据
    print("\n=== 示例数据 (前3条) ===")
    for i in range(min(3, len(df))):
        print(f"\n【食谱 {i+1}】{df['title'].iloc[i]}")
        print(f"  难度: {df['difficulty'].iloc[i]}")
        print(f"  适合体质: {df['suitable_constitutions'].iloc[i]}")
        print(f"  禁忌体质: {df['avoid_constitutions'].iloc[i]}")
        print(f"  功效标签: {df['efficacy_tags'].iloc[i]}")
        print(f"  节气标签: {df['solar_terms'].iloc[i]}")
        print(f"  置信度: {df['confidence'].iloc[i]}%")

    # 统计信息
    print("\n=== 统计信息 ===")
    print("难度分布:")
    print(df['difficulty'].value_counts().to_string())

    print(f"\n置信度分布:")
    print(f"  高置信度(>80%): {sum(df['confidence'] > 80)} 条")
    print(f"  中置信度(60-80%): {sum((df['confidence'] >= 60) & (df['confidence'] <= 80))} 条")
    print(f"  低置信度(<60%): {sum(df['confidence'] < 60)} 条")

    print(f"\n功效标签总数: {sum(df['efficacy_tags'].apply(lambda x: len(json.loads(x))))}")
    print(f"节气标签总数: {sum(df['solar_terms'].apply(lambda x: len(json.loads(x))))}")

    # 建议人工审核的记录
    low_confidence = df[df['confidence'] < 60]
    if len(low_confidence) > 0:
        print(f"\n建议人工审核的记录 (置信度<60%): {len(low_confidence)} 条")
        print("可使用以下命令导出:")
        print(f"  df[df['confidence'] < 60].to_excel('low_confidence_recipes.xlsx', index=False)")

if __name__ == '__main__':
    main()
