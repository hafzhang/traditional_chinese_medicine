"""
Acupoints Data (Comprehensive 361 Standard Points)
穴位数据 - 完整361标准穴位
使用 acupoints_comprehensive.py 作为数据源
"""

# 从 comprehensive 数据模块导入
from .acupoints_comprehensive import ACUPOINTS_DATA

# 为了向后兼容，保留旧的导出名称
ACUPOINTS = ACUPOINTS_DATA

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
    'get_acupoints_by_meridian',
    'get_acupoints_by_body_part',
    'get_acupoint_by_code',
    'get_meridian_list',
    'get_body_part_list'
]
