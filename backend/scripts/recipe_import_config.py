"""
菜谱 Excel 导入配置
定义字段映射关系和验证规则
"""

from typing import Optional, Dict, List, Any
import re


# Excel 列名到数据库字段的映射
COLUMN_MAPPING = {
    # 基本信息映射
    'title': 'name',                    # 菜谱名称 -> name
    'costtime': 'cooking_time',         # 烹饪时间字符串 -> cooking_time (需要解析)
    'steptext': 'steps_text',           # 步骤文本 -> steps_text (需要解析)
    'QuantityIngredients': 'ingredients_text',  # 食材用量 -> ingredients_text (需要解析)
    'desc': 'description',              # 描述 -> description
    'tip': 'tip',                       # 小贴士 -> tip

    # 新增字段映射
    'meal_type': 'meal_type',           # 餐次类型
    'difficulty': 'difficulty',         # 难度等级
    'suitable_constitutions': 'suitable_constitutions',  # 适合体质
    'avoid_constitutions': 'avoid_constitutions',        # 禁忌体质
    'efficacy_tags': 'efficacy_tags',    # 功效标签
    'solar_terms': 'solar_terms',        # 节气标签
    'servings': 'servings',              # 份量
    'cover_image': 'cover_image',        # 封面图片
}

# 枚举值定义
ENUM_VALUES = {
    'meal_type': ['breakfast', 'lunch', 'dinner', 'snack', 'soup'],
    'difficulty': ['easy', 'medium', 'hard'],
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

# DIFFICULTY_MAP: 难度中文到代码的映射
DIFFICULTY_MAP = {
    '简单': 'easy',
    '中等': 'medium',
    '困难': 'hard',
}

# CONSTITUTION_MAP: 体质中文名到代码的映射
CONSTITUTION_MAP = {
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

# FOOD_SYNONYMS: 食材同义词字典
FOOD_SYNONYMS = {
    '西红柿': ['番茄', '洋柿子'],
    '土豆': ['马铃薯', '洋芋'],
    '红薯': ['甘薯', '地瓜'],
    '山药': ['淮山', '怀山药', '薯蓣'],
    '茄子': ['落苏'],
    '辣椒': ['海椒', '辣子'],
    '黄瓜': ['青瓜'],
    '洋葱': ['葱头'],
    '花生': ['落花生'],
    '玉米': ['包谷', '棒子'],
    '菠菜': ['菠薐'],
    '芹菜': ['药芹'],
    '香菜': ['芫荽'],
    '莴笋': ['莴苣'],
    '豆腐': ['菽乳'],
}

# 烹饪时间解析规则
def parse_cooking_time(value: Any) -> Optional[int]:
    """
    解析烹饪时间字符串
    支持格式:
    - "10-30分钟" 返回 30 (取最大值)
    - "约30分钟" 返回 30
    - "半小时" 返回 30
    - "1小时" 返回 60
    - 无法解析时返回 None
    """
    if not value or value == '':
        return None

    time_str = str(value).strip()

    # 匹配 "X小时" 格式 (先匹配，因为包含数字)
    hour_match = re.search(r'(\d+\.?\d*)\s*[小时h]', time_str)
    if hour_match:
        return int(float(hour_match.group(1)) * 60)

    # 匹配范围 "10-30分钟" 取最大值 (在单个数字前匹配)
    range_match = re.search(r'(\d+)\s*[-~]\s*(\d+)\s*分钟', time_str)
    if range_match:
        return int(range_match.group(2))  # 返回最大值

    # 匹配 "X分钟" 或 "约X分钟" 格式
    minute_match = re.search(r'(?:约)?(\d+)\s*[分分钟]', time_str)
    if minute_match:
        return int(minute_match.group(1))

    # 匹配 "半小时"
    if '半小时' in time_str or '半钟' in time_str:
        return 30

    # 无法解析
    return None

# 食材解析函数
def parse_ingredients(value: str) -> List[Dict[str, Any]]:
    r"""
    解析食材字符串
    支持分隔符: 顿号、逗号、换行
    解析格式: '山药50g' → {'name': '山药', 'amount': '50g'}
    解析格式: '枸杞 20克' → {'name': '枸杞', 'amount': '20克'}
    使用正则: ([\u4e00-\u9fa5]+)\s*([\d\.]+\s*[克g个ml斤两]*)
    """
    if not value or value == '':
        return []

    ingredients = []
    # 按分隔符分割: 顿号、逗号、换行
    parts = str(value).replace('、', '\n').replace('，', '\n').replace(',', '\n').split('\n')

    for part in parts:
        part = part.strip()
        if not part:
            continue

        # 使用正则匹配: 中文名称 + 可选空格 + 数字+单位
        match = re.search(r'([\u4e00-\u9fa5]+)\s*([\d\.]+\s*[克g个ml斤两]*)', part)
        if match:
            name = match.group(1).strip()
            amount = match.group(2).strip()
            ingredients.append({
                'name': name,
                'amount': amount
            })

    return ingredients

# 步骤解析函数
def parse_steps(value: str) -> List[Dict[str, Any]]:
    """
    解析步骤文本
    支持分隔符: # 或换行
    提取步骤编号: '1.'、'2.'、'步骤1:'、'第一步:'
    返回格式: [{'step_number': 1, 'description': '...', 'duration': None}]
    可选解析时间: '（约5分钟）' → duration=5
    """
    if not value or value == '':
        return []

    steps = []
    # 按 # 或换行分割
    lines = str(value).replace('#', '\n').split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 提取步骤编号: 支持多种格式
        # '1.' 或 '1、' 或 '步骤1:' 或 '第一步:'
        match = re.match(r'^(?:步骤|第)?(\d+)[\.、:：]\s*(.+)', line)
        if match:
            step_number = int(match.group(1))
            description = match.group(2).strip()

            # 尝试从描述中提取时间，如 "（约5分钟）" 或 "(约5分钟)"
            duration = None
            duration_match = re.search(r'[（(]\s*约?\s*(\d+)\s*(?:分|钟|分钟)\s*[）)]', description)
            if duration_match:
                duration = int(duration_match.group(1))
                # 从描述中移除时间部分
                description = re.sub(r'[（(]\s*约?\s*\d+\s*(?:分|钟|分钟)\s*[）)]', '', description).strip()

            steps.append({
                'step_number': step_number,
                'description': description,
                'duration': duration
            })

    return steps

# 标签解析函数
def parse_tags(value: Any, mapping: Optional[Dict[str, str]] = None) -> List[str]:
    """
    解析标签字符串
    支持逗号、顿号、换行符分隔
    value为None返回空列表
    提供mapping时将标签转换为代码
    """
    if not value or value == '':
        return []

    # 按多种分隔符分割
    tags = str(value).replace('，', ',').replace('、', ',').replace('\n', ',').split(',')

    # 去除首尾空格，过滤空字符串
    result = [tag.strip() for tag in tags if tag.strip()]

    # 如果提供了映射，转换为代码
    if mapping:
        result = [mapping.get(tag, tag) for tag in result if tag in mapping or tag in mapping.values()]

    return result


def parse_difficulty(value: Any, cooking_time: Optional[int] = None) -> str:
    """
    解析难度或智能推测
    如果value是中文('简单'/'中等'/'困难')，映射为'easy'/'medium'/'hard'
    如果value已经是代码，直接返回
    如果value为None且cooking_time不为None，根据时间推测:
      - ≤30分钟 → easy
      - 31-60分钟 → medium
      - >60分钟 → hard
    都为None时默认返回'medium'
    """
    # 如果value已经是代码，直接返回
    if value in ['easy', 'medium', 'hard']:
        return value

    # 如果value是中文，映射为代码
    if value and value in DIFFICULTY_MAP:
        return DIFFICULTY_MAP[value]

    # 根据cooking_time推测
    if cooking_time is not None:
        if cooking_time <= 30:
            return 'easy'
        elif cooking_time <= 60:
            return 'medium'
        else:
            return 'hard'

    # 默认返回medium
    return 'medium'


def guess_constitutions(ingredients: List[str], efficacy: List[str], db: Optional[Any] = None) -> List[str]:
    """
    智能推测适合体质
    根据食材名称查询ingredients表获取性味(nature/taste)
    性味规则:
      - 温性 → yang_deficiency
      - 凉性 → yin_deficiency
      - 平性 → peace
    功效关键词:
      - '补气' → qi_deficiency
      - '健脾' → qi_deficiency + peace
    返回去重的体质代码列表
    """
    constitutions = set()

    # 根据功效关键词推测
    for tag in efficacy:
        if '补气' in tag or '益气' in tag:
            constitutions.add('qi_deficiency')
        if '健脾' in tag or '养胃' in tag:
            constitutions.add('qi_deficiency')
            constitutions.add('peace')
        if '温阳' in tag or '补阳' in tag:
            constitutions.add('yang_deficiency')
        if '养阴' in tag or '滋阴' in tag:
            constitutions.add('yin_deficiency')
        if '祛湿' in tag or '化痰' in tag:
            constitutions.add('phlegm_damp')
        if '活血' in tag:
            constitutions.add('blood_stasis')
        if '疏肝' in tag:
            constitutions.add('qi_depression')

    # TODO: 如果提供了db，可以查询食材的性味进行更精确的推测
    # 这需要数据库查询，暂时只基于功效标签

    return list(constitutions)


def guess_efficacy_tags(ingredients: List[str]) -> List[str]:
    """
    智能推测功效标签
    定义 FOOD_EFFICACY_MAP 字典: 食材到功效的映射
    根据食材性味推测:
      - 甘味 → 健脾
      - 苦味 → 清热
      - 辛味 → 发散
    返回去重的功效标签列表，最多5个
    """
    # 食材到功效的映射
    FOOD_EFFICACY_MAP = {
        '山药': ['健脾', '养胃', '补气'],
        '红枣': ['补血', '安神'],
        '枸杞': ['补血', '养阴'],
        '莲子': ['健脾', '安神'],
        '百合': ['养阴', '润肺', '安神'],
        '银耳': ['养阴', '润肺'],
        '黑木耳': ['补血', '活血'],
        '生姜': ['温阳', '化痰'],
        '葱白': ['发散', '解表'],
        '大蒜': ['温阳', '解毒'],
        '绿豆': ['清热', '祛湿'],
        '红豆': ['祛湿', '补血'],
        '薏米': ['祛湿', '健脾'],
        '冬瓜': ['清热', '祛湿'],
        '丝瓜': ['清热', '化痰'],
        '南瓜': ['健脾', '补气'],
        '胡萝卜': ['健脾', '养胃'],
        '白萝卜': ['化痰', '消食'],
        '西红柿': ['清热', '生津'],
        '黄瓜': ['清热', '解毒'],
        '小米': ['健脾', '养胃'],
        '大米': ['健脾', '补气'],
        '糯米': ['补气', '温阳'],
        '玉米': ['健脾', '祛湿'],
        '红薯': ['补气', '健脾'],
        '鸡肉': ['补气', '温阳'],
        '牛肉': ['补气', '补血'],
        '猪肉': ['补血', '滋阴'],
        '羊肉': ['温阳', '补气'],
        '鸡蛋': ['补血', '养阴'],
    }

    tags = []

    # 根据食材名称查找功效
    for ingredient in ingredients:
        # 检查是否是标准名称
        if ingredient in FOOD_EFFICACY_MAP:
            tags.extend(FOOD_EFFICACY_MAP[ingredient])
        else:
            # 检查是否是同义词
            for standard_name, synonyms in FOOD_SYNONYMS.items():
                if ingredient in synonyms and standard_name in FOOD_EFFICACY_MAP:
                    tags.extend(FOOD_EFFICACY_MAP[standard_name])
                    break

    # 去重并限制数量
    unique_tags = list(dict.fromkeys(tags))  # 保持顺序的去重

    return unique_tags[:5]


def guess_solar_terms(ingredients: List[str], efficacy: List[str]) -> List[str]:
    """
    智能推测节气标签
    定义 FOOD_SEASON_MAP 字典: 食材到季节的映射
    根据食材时令推测:
      - 春季食材 → ['春季', '立春', '雨水']
      - 夏季食材 → ['夏季', '立夏', '小暑']
    根据功效匹配:
      - '清热' → ['夏季']
      - '温补' → ['冬季']
    返回去重的节气标签列表
    """
    # 食材到季节的映射
    FOOD_SEASON_MAP = {
        # 春季
        '韭菜': ['春季'],
        '菠菜': ['春季'],
        '芹菜': ['春季'],
        '春笋': ['春季'],
        # 夏季
        '黄瓜': ['夏季'],
        '西红柿': ['夏季'],
        '丝瓜': ['夏季'],
        '苦瓜': ['夏季'],
        '绿豆': ['夏季'],
        '西瓜': ['夏季'],
        # 秋季
        '南瓜': ['秋季'],
        '莲藕': ['秋季'],
        '梨': ['秋季'],
        '银耳': ['秋季'],
        # 冬季
        '萝卜': ['冬季'],
        '白菜': ['冬季'],
        '羊肉': ['冬季'],
        '红枣': ['冬季'],
        '山药': ['冬季'],
    }

    solar_terms = set()

    # 根据食材推测季节
    for ingredient in ingredients:
        if ingredient in FOOD_SEASON_MAP:
            solar_terms.update(FOOD_SEASON_MAP[ingredient])
        else:
            # 检查同义词
            for standard_name, synonyms in FOOD_SYNONYMS.items():
                if ingredient in synonyms and standard_name in FOOD_SEASON_MAP:
                    solar_terms.update(FOOD_SEASON_MAP[standard_name])
                    break

    # 根据功效匹配季节
    for tag in efficacy:
        if '清热' in tag or '解暑' in tag or '祛湿' in tag:
            solar_terms.add('夏季')
            solar_terms.add('立夏')
            solar_terms.add('小暑')
            solar_terms.add('大暑')
        if '温补' in tag or '温阳' in tag or '补气' in tag:
            solar_terms.add('冬季')
            solar_terms.add('立冬')
            solar_terms.add('大寒')

    return list(solar_terms)


def scan_dish_images(image_dir: str) -> Dict[str, str]:
    """
    扫描图片目录
    扫描 source_data/dishes_images/ 目录
    支持格式: .jpg, .jpeg, .png, .webp (不区分大小写)
    返回: {'山药小米粥': '/full/path/山药小米粥.jpg', ...}
    文件名键转为小写并去除扩展名
    """
    import os

    image_map = {}

    if not os.path.exists(image_dir):
        print(f"Warning: Image directory {image_dir} does not exist")
        return image_map

    # 支持的图片格式
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp'}

    # 使用 os.walk 递归扫描
    for root, dirs, files in os.walk(image_dir):
        for filename in files:
            # 检查扩展名
            ext = os.path.splitext(filename)[1].lower()
            if ext in image_extensions:
                # 去除扩展名，转为小写作为键
                name_without_ext = os.path.splitext(filename)[0]
                key = name_without_ext.lower()
                # 完整路径作为值
                full_path = os.path.join(root, filename)
                image_map[key] = full_path

    print(f"Scanned {len(image_map)} images from {image_dir}")
    return image_map


def match_recipe_image(recipe_name: str, image_map: Dict[str, str]) -> Optional[str]:
    """
    图片模糊匹配
    步骤1: 精确匹配 (去除空格后直接匹配)
    步骤2: 标准化匹配 (统一空格、下划线、括号)
    步骤3: 同义词匹配 (使用 FOOD_SYNONYMS 替换)
    步骤4: 包含匹配 (recipe_name包含image_key或反之)
    匹配成功返回图片完整路径，失败返回None
    """
    import re

    # 标准化函数: 统一空格、下划线、括号
    def normalize(s: str) -> str:
        s = s.lower()
        s = re.sub(r'[\s\-_]+', '', s)  # 去除空格、横线、下划线
        s = re.sub(r'[()（）\[\]【】]', '', s)  # 去除括号
        return s

    # 步骤1: 精确匹配
    key = recipe_name.lower()
    if key in image_map:
        return image_map[key]

    # 步骤2: 标准化匹配
    normalized_name = normalize(recipe_name)
    for image_key, image_path in image_map.items():
        if normalize(image_key) == normalized_name:
            return image_path

    # 步骤3: 同义词匹配
    for standard_name, synonyms in FOOD_SYNONYMS.items():
        if recipe_name in synonyms:
            # 尝试用标准名称匹配
            for image_key, image_path in image_map.items():
                if standard_name.lower() in image_key or image_key in standard_name.lower():
                    return image_path

    # 步骤4: 包含匹配
    for image_key, image_path in image_map.items():
        if recipe_name.lower() in image_key or image_key in recipe_name.lower():
            return image_path

    # 未找到匹配
    return None
