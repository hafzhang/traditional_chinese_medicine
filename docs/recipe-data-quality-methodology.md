# 食谱元数据填充方法论

## 1. 基于中医理论的食材性味归经数据库

### 1.1 建立标准食材库

```python
# 示例：食材性味归经标准
INGREDIENT_DATABASE = {
    "山药": {
        "name": "山药",
        "nature": "平",  # 四气：寒、热、温、凉、平
        "flavor": "甘",  # 五味：酸、苦、甘、辛、咸
        "meridian": ["脾", "肺", "肾"],  # 归经
        "efficacy": ["健脾", "补肺", "固肾", "益精"],
        "suitable_constitutions": ["qi_deficiency", "yin_deficiency", "peace"],
        "avoid_constitutions": ["damp_heat"],  # 湿热质慎用
        "source": "《中国药典》",  # 权威来源
        "solar_terms": ["立秋", "霜降", "冬至"]  # 最佳食用时节
    },
    "绿豆": {
        "name": "绿豆",
        "nature": "寒",
        "flavor": "甘",
        "meridian": ["心", "胃"],
        "efficacy": ["清热", "解毒", "消暑", "利水"],
        "suitable_constitutions": ["damp_heat", "yin_deficiency"],
        "avoid_constitutions": ["yang_deficiency"],  # 阳虚质忌用
        "source": "《本草纲目》",
        "solar_terms": ["立夏", "夏至", "大暑"]
    },
    # ... 更多食材
}
```

### 1.2 判断逻辑改进

**原方法**：简单的关键词匹配
```python
if "绿豆" in ingredients:
    avoid.append("yang_deficiency")
```

**改进方法**：基于食材数据库
```python
def analyze_recipe_ingredients(recipe):
    """综合分析食谱中的所有食材"""
    ingredients = parse_ingredients(recipe['QuantityIngredients'])

    # 统计每种体质的适宜度
    constitution_scores = {c: 0 for c in CONSTITUTIONS}
    efficacy_counts = Counter()
    seasonal_scores = Counter()

    for ingredient in ingredients:
        if ingredient in INGREDIENT_DATABASE:
            data = INGREDIENT_DATABASE[ingredient]

            # 累加适宜体质
            for c in data['suitable_constitutions']:
                constitution_scores[c] += 1

            # 累加禁忌体质（负分）
            for c in data['avoid_constitutions']:
                constitution_scores[c] -= 2

            # 累加功效
            for eff in data['efficacy']:
                efficacy_counts[eff] += 1

            # 累加时节
            for term in data.get('solar_terms', []):
                seasonal_scores[term] += 1

    # 根据分数判断
    suitable = [c for c, score in constitution_scores.items() if score > 0]
    avoid = [c for c, score in constitution_scores.items() if score < -1]

    return {
        'suitable': suitable,
        'avoid': avoid,
        'efficacy': list(efficacy_counts.keys()),
        'solar_terms': [t for t, count in seasonal_scores.most_common(3)]
    }
```

## 2. 难度评估改进

### 2.1 多维度难度评估

```python
def calculate_difficulty(recipe):
    """综合评估食谱难度"""
    score = 0

    # 1. 烹饪时间 (40分)
    time = parse_time(recipe['costtime'])
    if time > 90: score += 40
    elif time > 40: score += 30
    elif time > 15: score += 20
    else: score += 10

    # 2. 食材处理复杂度 (30分)
    ingredients = recipe['QuantityIngredients']
    if "切" in recipe['steptext']: score += 5
    if "腌制" in recipe['steptext']: score += 5
    if "过水" in recipe['steptext'] or "焯水" in recipe['steptext']: score += 5
    if "挂糊" in recipe['steptext'] or "裹粉" in recipe['steptext']: score += 10
    if "打发" in recipe['steptext']: score += 10

    # 3. 烹饪技巧 (30分)
    steps = recipe['steptext']
    if "蒸" in steps: score += 10
    if "炸" in steps: score += 15
    if "火候" in steps or "中小火" in steps: score += 10
    if "勾芡" in steps: score += 10

    # 转换为等级
    if score >= 80: return "困难"
    elif score >= 60: return "较难"
    elif score >= 40: return "中等"
    else: return "简单"
```

## 3. 数据来源权威性分级

```
A级 - 最权威
├── 《中华人民共和国药典》
├── 《本草纲目》
└── 《黄帝内经》

B级 - 专业教材
├── 《中医食疗学》统编教材
├── 《中药学》统编教材
└── 《营养与食品卫生学》

C级 - 专业期刊
└── 核心期刊发表的食疗研究

D级 - 网络资源
└── 仅作参考，需人工审核
```

## 4. 质量保证机制

### 4.1 置信度评分

```python
def calculate_confidence(recipe, analysis_result):
    """计算分析结果的置信度"""
    confidence = 0

    # 1. 食材识别率
    identified_ingredients = count_identified(recipe['QuantityIngredients'])
    total_ingredients = count_total(recipe['QuantityIngredients'])
    confidence += (identified_ingredients / total_ingredients) * 40

    # 2. 判断依据强度
    if analysis_result['source'] == '药典':
        confidence += 30
    elif analysis_result['source'] == '本草纲目':
        confidence += 25
    else:
        confidence += 10

    # 3. 结果一致性
    if all(analysis_result['suitable_constitutions']):
        confidence += 15

    # 4. 数据完整性
    if all(analysis_result.values()):
        confidence += 15

    return min(100, confidence)
```

### 4.2 人工审核流程

```
低置信度(<60%) → 标记需人工审核
中置信度(60-80%) → 抽样审核
高置信度(>80%) → 自动通过
```

## 5. 持续改进机制

### 5.1 反馈学习

```python
# 记录人工修正的数据
corrections = [
    {
        "recipe_id": "xxx",
        "field": "suitable_constitutions",
        "auto_value": ["peace", "qi_deficiency"],
        "manual_value": ["peace", "qi_deficiency", "yang_deficiency"],
        "reason": "该菜含生姜，适合阳虚质"
    }
]

# 定期分析修正原因，优化算法
def analyze_corrections(corrections):
    """分析人工修正模式，改进算法"""
    # 发现缺失的关键词
    # 调整权重
    # 更新食材数据库
```

## 6. 实施建议

### 短期方案（当前）
- ✅ 使用关键词匹配
- ✅ 覆盖基础数据
- ⚠️ 需要人工抽检

### 中期方案（推荐）
1. 建立100-200种常用食材的性味归经数据库
2. 改进难度评估算法（多维度）
3. 添加置信度评分
4. 人工审核低置信度数据

### 长期方案（最佳）
1. 完整的食材数据库（500+种）
2. 机器学习模型（从标注数据学习）
3. 专家审核机制
4. 持续反馈优化

## 7. 参考资料

1. **传统典籍**
   - 《本草纲目》- 李时珍
   - 《黄帝内经》
   - 《神农本草经》

2. **现代标准**
   - 《中华人民共和国药典》（2020版）
   - 《中医食疗学》全国高等中医药院校教材

3. **数据标准**
   - 中医体质分类与判定标准（ZYYXH/T157-2009）
   - 中医营养学标准
