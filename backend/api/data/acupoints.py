"""
Acupoints Data (Comprehensive 361 Standard Points)
穴位数据 - 完整361标准穴位
使用 acupoints_comprehensive.py 作为数据源
"""

# 从 comprehensive 数据模块导入
from .acupoints_comprehensive import ACUPOINTS_DATA

# 为了向后兼容，保留旧的导出名称
ACUPOINTS = ACUPOINTS_DATA

# 部位与经络的映射关系
# 用于根据经络推断穴位所在部位
BODY_PART_MERIDIAN_MAP = {
    "head": [
        "督脉", "任脉", "足阳明胃经(头)", "足少阳胆经(头)", "足太阳膀胱经(头)",
        "手阳明大肠经(头)", "手少阳三焦经(头)", "手太阳小肠经(头)"
    ],
    "neck": [
        "督脉(颈)", "任脉(颈)", "足阳明胃经(颈)", "足少阳胆经(颈)"
    ],
    "shoulder": [
        "手阳明大肠经(肩)", "手少阳三焦经(肩)", "手太阳小肠经(肩)",
        "足少阳胆经(肩)"
    ],
    "arm_upper": [
        "手太阴肺经(臂)", "手阳明大肠经(臂)", "手少阴心经(臂)",
        "手太阳小肠经(臂)", "手厥阴心包经(臂)", "手少阳三焦经(臂)"
    ],
    "arm_lower": [
        "手太阴肺经(前臂)", "手阳明大肠经(前臂)", "手少阴心经(前臂)",
        "手太阳小肠经(前臂)", "手厥阴心包经(前臂)", "手少阳三焦经(前臂)"
    ],
    "hand": [
        "手太阴肺经(手)", "手阳明大肠经(手)", "手少阴心经(手)",
        "手太阳小肠经(手)", "手厥阴心包经(手)", "手少阳三焦经(手)"
    ],
    "chest": [
        "任脉(胸)", "足太阴脾经(胸)", "足少阴肾经(胸)",
        "足阳明胃经(胸)"
    ],
    "abdomen": [
        "任脉(腹)", "足太阴脾经(腹)", "足阳明胃经(腹)",
        "足少阴肾经(腹)"
    ],
    "back": [
        "督脉(背)", "足太阳膀胱经(背)", "足少阴肾经(背)"
    ],
    "thigh_upper": [
        "足阳明胃经(大腿)", "足少阳胆经(大腿)", "足太阴脾经(大腿)",
        "足厥阴肝经(大腿)", "足太阳膀胱经(大腿)"
    ],
    "thigh_lower": [
        "足阳明胃经(小腿)", "足少阳胆经(小腿)", "足太阴脾经(小腿)",
        "足厥阴肝经(小腿)", "足太阳膀胱经(小腿)", "足少阴肾经(小腿)"
    ],
    "foot": [
        "足阳明胃经(足)", "足少阳胆经(足)", "足太阴脾经(足)",
        "足厥阴肝经(足)", "足太阳膀胱经(足)", "足少阴肾经(足)"
    ]
}

# 经络名称标准化映射
# 将 Excel 中的经络名称映射到标准代码
MERIDIAN_NAME_MAP = {
    "手太阴肺经": "lung_lung",
    "手阳明大肠经": "large_intestine",
    "足阳明胃经": "stomach",
    "足太阴脾经": "spleen",
    "手少阴心经": "heart",
    "手太阳小肠经": "small_intestine",
    "足太阳膀胱经": "bladder",
    "足少阴肾经": "kidney",
    "手厥阴心包经": "pericardium",
    "手少阳三焦经": "sanjiao",
    "足少阳胆经": "gallbladder",
    "足厥阴肝经": "liver",
    "督脉": "governing_vessel",
    "任脉": "conception_vessel"
}

# 添加便捷函数
def get_acupoints_by_meridian(meridian_code: str = None):
    """根据经络代码获取穴位列表"""
    if meridian_code:
        return [a for a in ACUPOINTS_DATA if a["code"].startswith(meridian_code)]
    return ACUPOINTS_DATA

def get_acupoints_by_body_part(body_part: str = None):
    """根据部位获取穴位列表"""
    if body_part:
        return [a for a in ACUPOINTS_DATA if a["body_part"] == body_part]
    return ACUPOINTS_DATA

def get_acupoint_by_code(code: str):
    """根据代码获取单个穴位"""
    for a in ACUPOINTS_DATA:
        if a["code"] == code:
            return a
    return None

def get_meridian_list():
    """获取所有经络列表"""
    meridians = {}
    for a in ACUPOINTS_DATA:
        if a["meridian"] not in meridians:
            meridians[a["meridian"]] = {
                "name": a["meridian"],
                "count": 0,
                "body_part": a["body_part"]
            }
        meridians[a["meridian"]]["count"] += 1
    return list(meridians.values())

def get_body_part_list():
    """获取所有部位列表"""
    parts = set(a["body_part"] for a in ACUPOINTS_DATA)
    return [{"value": p, "label": p} for p in sorted(parts)]

# 导出
__all__ = [
    'ACUPOINTS_DATA',
    'ACUPOINTS',
    'BODY_PART_MERIDIAN_MAP',
    'MERIDIAN_NAME_MAP',
    'get_acupoints_by_meridian',
    'get_acupoints_by_body_part',
    'get_acupoint_by_code',
    'get_meridian_list',
    'get_body_part_list'
]
