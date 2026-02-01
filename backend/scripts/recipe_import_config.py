"""
菜谱 Excel 导入配置
定义字段映射关系和验证规则
"""

import pandas as pd

# Excel 列名到数据库字段的映射
COLUMN_MAPPING = {
    # 基本信息映射
    'title': 'name',                    # 菜谱名称 -> name
    'desc': 'description',              # 描述 -> description
    'costtime': 'cooking_time',         # 烹饪时间字符串 -> cooking_time (需要解析)
    'QuantityIngredients': None,        # 食材用量 -> 单独处理
    'steptext': None,                   # 步骤文本 -> 单独处理
    'tip': 'tip',                       # 小贴士
    'zid': 'zid',                       # 分类/分组ID

    # 新增字段映射
    'meal_type': 'meal_type',           # 餐次类型
    'difficulty': 'difficulty',         # 难度等级
    'suitable_constitutions': 'suitable_constitutions',  # 适合体质
    'avoid_constitutions': 'avoid_constitutions',        # 禁忌体质
    'efficacy_tags': 'efficacy_tags',    # 功效标签
    'solar_terms': 'solar_terms',        # 节气标签
    'servings': 'servings',              # 份量
    'cover_image': 'cover_image',        # 封面图片
    'confidence': 'confidence',          # AI置信度分数
    'method': 'cooking_method',          # 烹饪方法
}

# 枚举值定义
ENUM_VALUES = {
    'meal_type': ['breakfast', 'lunch', 'dinner', 'snack', 'soup'],
    'difficulty': ['easy', 'medium', 'harder', 'hard'],
}

# 体质代码列表
CONSTITUTION_CODES = [
    'peace',           # 平和质
    'qi_deficiency',   # 气虚质
    'yang_deficiency', # 阳虚质
    'yin_deficiency',  # 阴虚质
    'phlegm_damp',     # 痰湿质
    'damp_heat',       # 湿热质
    'blood_stasis',    # 血瘀质
    'qi_depression',   # 气郁质
    'special',         # 特禀质
]

# 功效标签列表
EFFICACY_TAGS = [
    '健脾', '养胃', '补气', '补血', '养阴',
    '温阳', '化痰', '祛湿', '活血', '疏肝', '安神',
    '润肺', '补肾', '清热', '解毒', '止痛'
]

# 节气标签列表
SOLAR_TERMS = [
    # 四季
    '春季', '夏季', '秋季', '冬季',
    # 24节气
    '立春', '雨水', '惊蛰', '春分', '清明', '谷雨',
    '立夏', '小满', '芒种', '夏至', '小暑', '大暑',
    '立秋', '处暑', '白露', '秋分', '寒露', '霜降',
    '立冬', '小雪', '大雪', '冬至', '小寒', '大寒',
]

# 中文到代码的映射
MEAL_TYPE_CN_TO_CODE = {
    '早餐': 'breakfast',
    '午餐': 'lunch',
    '晚餐': 'dinner',
    '小食': 'snack',
    '汤品': 'soup',
}

DIFFICULTY_CN_TO_CODE = {
    '简单': 'easy',
    '中等': 'medium',
    '较难': 'harder',
    '困难': 'hard',
}

CONSTITUTION_CN_TO_CODE = {
    '平和质': 'peace',
    '气虚质': 'qi_deficiency',
    '阳虚质': 'yang_deficiency',
    '阴虚质': 'yin_deficiency',
    '痰湿质': 'phlegm_damp',
    '湿热质': 'damp_heat',
    '血瘀质': 'blood_stasis',
    '气郁质': 'qi_depression',
    '特禀质': 'special',
}

# 烹饪时间解析规则
def parse_cooking_time(time_str):
    """
    解析烹饪时间字符串
    支持格式:
    - "10-30分钟"
    - "10~30分钟"
    - "30分钟"
    - "1小时"
    - "1.5小时"
    """
    import re

    if not time_str or pd.isna(time_str):
        return 30  # 默认30分钟

    time_str = str(time_str).strip()

    # 匹配 "X分钟" 或 "X分钟" 格式
    minute_match = re.search(r'(\d+)\s*[分分钟]', time_str)
    if minute_match:
        return int(minute_match.group(1))

    # 匹配 "X小时" 格式
    hour_match = re.search(r'(\d+\.?\d*)\s*[小时h]', time_str)
    if hour_match:
        return int(float(hour_match.group(1)) * 60)

    # 匹配范围 "10-30分钟" 取中间值
    range_match = re.search(r'(\d+)\s*[-~]\s*(\d+)\s*分钟', time_str)
    if range_match:
        return (int(range_match.group(1)) + int(range_match.group(2))) // 2

    return 30  # 默认30分钟

# 食材解析函数
def parse_ingredients(ingredients_str):
    """
    解析食材字符串
    格式: "山药50g、枸杞20g、红枣3颗"
    返回: [{"name": "山药", "amount": "50g"}, ...]
    """
    if not ingredients_str or pd.isna(ingredients_str):
        return []

    ingredients = []
    # 按分隔符分割
    parts = str(ingredients_str).replace('、', ',').replace('，', ',').split(',')

    for part in parts:
        part = part.strip()
        if not part:
            continue

        # 提取数字和单位
        import re
        match = re.search(r'^(.+?)(\d+\.?\d*)(克|g|毫升|ml|个|只|根|片|把|勺|适量|少许)$', part)
        if match:
            name = match.group(1).strip()
            amount = match.group(2) + (match.group(3) if match.group(3) != '适量' and match.group(3) != '少许' else '')
            is_main = False  # 默认不是主料，可以根据名称判断
            ingredients.append({
                'name': name,
                'amount': amount if amount else '适量',
                'is_main': is_main,
                'display_order': len(ingredients)
            })
        else:
            # 没有具体用量的，当作适量
            ingredients.append({
                'name': part,
                'amount': '适量',
                'is_main': False,
                'display_order': len(ingredients)
            })

    return ingredients

# 步骤解析函数
def parse_steps(step_text):
    """
    解析步骤文本
    格式: "1.步骤一\n2.步骤二\n..."
    返回: [{"step_number": 1, "description": "步骤一", ...}, ...]
    """
    if not step_text or pd.isna(step_text):
        return []

    steps = []
    # 按 # 或换行分割
    lines = str(step_text).replace('#', '\n').split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 提取步骤编号
        import re
        match = re.match(r'^(\d+)[.、]\s*(.+)', line)
        if match:
            step_number = int(match.group(1))
            description = match.group(2).strip()
            steps.append({
                'step_number': step_number,
                'description': description,
                'duration': None  # 可以从描述中解析
            })

    return steps

# 标签解析函数
def parse_tags(tags_str, valid_values):
    """
    解析标签字符串
    支持逗号、顿号分隔
    """
    if not tags_str or pd.isna(tags_str):
        return []

    tags = str(tags_str).replace('，', ',').replace('、', ',').split(',')
    return [tag.strip() for tag in tags if tag.strip() and tag.strip() in valid_values]
