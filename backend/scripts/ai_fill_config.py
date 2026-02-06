"""
AI填充食谱数据 - 配置文件
"""

# 智谱AI API配置 - 使用 Anthropic 兼容接口
ZHIPU_API_KEY = "5b85db241b734c7eb861bf232a65ecbc.cYi4vthV4l4cQf0c"
API_URL = "https://open.bigmodel.cn/api/anthropic/v1/messages"
API_BASE_URL = "https://open.bigmodel.cn/api/anthropic"
MODEL = "glm-4.7"
ANTHROPIC_VERSION = "2023-06-01"

# 批处理配置
BATCH_SIZE = 20  # 每批处理行数
MAX_RETRIES = 3  # API失败重试次数
REQUEST_TIMEOUT = 60  # 请求超时（秒）
RATE_LIMIT_DELAY = 1  # API请求间隔（秒）

# 体质代码列表（9种）
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

# 体质中文名称映射
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

# 功效标签列表（常用）
EFFICACY_TAGS = [
    '健脾', '养胃', '补气', '补血', '养阴',
    '温阳', '化痰', '祛湿', '活血', '疏肝', '安神',
    '润肺', '补肾', '清热', '解毒', '止痛',
    '消食', '止咳', '平喘', '止泻', '通便',
    '利尿', '止血', '止汗', '生津', '明目',
]

# 节气标签列表（24节气 + 四季）
SOLAR_TERMS = [
    # 春季
    '立春', '雨水', '惊蛰', '春分', '清明', '谷雨', '春季',
    # 夏季
    '立夏', '小满', '芒种', '夏至', '小暑', '大暑', '夏季',
    # 秋季
    '立秋', '处暑', '白露', '秋分', '寒露', '霜降', '秋季',
    # 冬季
    '立冬', '小雪', '大雪', '冬至', '小寒', '大寒', '冬季',
]

# AI提示词模板
AI_PROMPT_TEMPLATE = """你是一位中医养生专家，请根据以下菜谱信息分析其适合的体质、禁忌体质、功效标签和适用节气。

菜谱信息：
- 菜名：{title}
- 做法：{steptext}
- 食材：{ingredients}

请按以下JSON格式返回分析结果：
{{
  "suitable_constitutions": ["peace", "qi_deficiency", ...],
  "avoid_constitutions": ["phlegm_damp", ...],
  "efficacy_tags": ["健脾", "养胃", ...],
  "solar_terms": ["立春", "雨水", ...],
  "confidence": 85
}}

注意事项：
1. suitable_constitutions: 适合的体质，使用体质代码：{constitution_codes}
2. avoid_constitutions: 禁忌体质，使用体质代码：{constitution_codes}
3. efficacy_tags: 功效标签，使用中文标签，从以下选择：{efficacy_tags}
4. solar_terms: 适用节气，从以下选择：{solar_terms}
5. confidence: 置信度分数（80-95），表示你对分析结果的信心程度

请只返回JSON，不要有其他内容。"""

# 替换提示词中的占位符
def get_prompt(title: str, steptext: str, ingredients: str) -> str:
    """生成AI提示词"""
    return AI_PROMPT_TEMPLATE.format(
        title=title or "未知",
        steptext=steptext or "无",
        ingredients=ingredients or "无",
        constitution_codes=", ".join(CONSTITUTION_CODES),
        efficacy_tags=", ".join(EFFICACY_TAGS),
        solar_terms=", ".join(SOLAR_TERMS)
    )
