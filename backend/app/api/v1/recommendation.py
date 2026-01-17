"""
养生推荐 API 路由
"""
from fastapi import APIRouter
from typing import Dict

router = APIRouter()


# 养生推荐数据库（MVP 版本使用硬编码数据）
RECOMMENDATIONS: Dict[str, Dict] = {
    "peace": {
        "diet": {
            "suitable": ["山药", "莲子", "百合", "银耳", "绿豆"],
            "avoid": ["辛辣", "油腻"],
            "recipes": ["银耳莲子汤", "百合粥"]
        },
        "exercise": {
            "recommended": ["散步", "太极拳", "瑜伽"],
            "avoid": [],
            "advice": "适量运动，保持健康"
        },
        "lifestyle": {
            "sleep_time": "22:00-23:00",
            "sleep_duration": "7-8小时",
            "advice": "保持规律作息"
        }
    },
    "qi_deficiency": {
        "diet": {
            "suitable": ["糯米", "大枣", "山药", "鸡肉", "牛肉", "香菇"],
            "avoid": ["山楂", "大蒜", "薄荷", "荷叶", "绿豆"],
            "recipes": ["黄芪炖鸡", "山药粥", "红枣茶"]
        },
        "exercise": {
            "recommended": ["八段锦", "太极拳", "散步"],
            "avoid": ["剧烈运动", "大汗淋漓"],
            "advice": "量力而行，微微出汗"
        },
        "lifestyle": {
            "sleep_time": "22:00前",
            "sleep_duration": "7-8小时",
            "advice": "避免熬夜，午休30分钟"
        }
    },
    "yang_deficiency": {
        "diet": {
            "suitable": ["羊肉", "牛肉", "鸡肉", "韭菜", "生姜", "桂圆"],
            "avoid": ["生冷食物", "冰饮", "西瓜", "苦瓜"],
            "recipes": ["当归羊肉汤", "姜枣茶", "韭菜炒蛋"]
        },
        "exercise": {
            "recommended": ["慢跑", "快走", "瑜伽"],
            "avoid": ["游泳", "冷水运动"],
            "advice": "动静结合，注意保暖"
        },
        "lifestyle": {
            "sleep_time": "21:30前",
            "sleep_duration": "8-9小时",
            "advice": "注意保暖，适当晒太阳"
        }
    },
    "yin_deficiency": {
        "diet": {
            "suitable": ["百合", "银耳", "梨", "桑葚", "鸭肉", "黑芝麻"],
            "avoid": ["辛辣", "炸烤", "羊肉", "荔枝"],
            "recipes": ["百合银耳汤", "桑葚粥", "雪梨汤"]
        },
        "exercise": {
            "recommended": ["散步", "太极", "气功"],
            "avoid": ["高温环境运动"],
            "advice": "适量运动，及时补水"
        },
        "lifestyle": {
            "sleep_time": "22:30前",
            "sleep_duration": "7-8小时",
            "advice": "睡前泡脚，避免熬夜"
        }
    },
    "phlegm_damp": {
        "diet": {
            "suitable": ["冬瓜", "赤小豆", "薏米", "白萝卜", "海带"],
            "avoid": ["甜食", "油腻", "生冷"],
            "recipes": ["冬瓜薏米汤", "赤小豆粥", "萝卜汤"]
        },
        "exercise": {
            "recommended": ["有氧运动", "跑步", "游泳"],
            "avoid": ["久坐少动"],
            "advice": "持续运动，强度递增"
        },
        "lifestyle": {
            "sleep_time": "22:00前",
            "sleep_duration": "7-8小时",
            "advice": "规律作息，饭后不立即睡"
        }
    },
    "damp_heat": {
        "diet": {
            "suitable": ["绿豆", "苦瓜", "黄瓜", "冬瓜", "莲藕"],
            "avoid": ["辛辣", "油腻", "酒类"],
            "recipes": ["绿豆汤", "苦瓜炒蛋", "冬瓜汤"]
        },
        "exercise": {
            "recommended": ["游泳", "跑步", "球类"],
            "avoid": ["高温环境运动"],
            "advice": "强度适中，及时补水"
        },
        "lifestyle": {
            "sleep_time": "22:00前",
            "sleep_duration": "7-8小时",
            "advice": "保持清爽，卧室通风"
        }
    },
    "blood_stasis": {
        "diet": {
            "suitable": ["山楂", "桃仁", "红花", "黑豆", "黑木耳"],
            "avoid": ["生冷", "寒凉"],
            "recipes": ["山楂茶", "桃仁粥", "黑木耳汤"]
        },
        "exercise": {
            "recommended": ["太极", "舞蹈", "瑜伽"],
            "avoid": ["久坐不动"],
            "advice": "循序渐进，持之以恒"
        },
        "lifestyle": {
            "sleep_time": "22:00前",
            "sleep_duration": "7-8小时",
            "advice": "睡前放松，适当活动"
        }
    },
    "qi_depression": {
        "diet": {
            "suitable": ["玫瑰花", "菊花", "陈皮", "佛手", "芹菜"],
            "avoid": ["咖啡", "浓茶", "酒精"],
            "recipes": ["玫瑰花茶", "陈皮粥", "芹菜炒百合"]
        },
        "exercise": {
            "recommended": ["太极", "瑜伽", "舞蹈"],
            "avoid": ["剧烈竞技"],
            "advice": "动静结合，调节情绪"
        },
        "lifestyle": {
            "sleep_time": "22:00前",
            "sleep_duration": "7-8小时",
            "advice": "睡前冥想，放松心情"
        }
    },
    "special": {
        "diet": {
            "suitable": ["蜂蜜", "红枣", "胡萝卜", "西兰花"],
            "avoid": ["海鲜", "花粉", "芒果", "个人过敏原"],
            "recipes": ["红枣茶", "胡萝卜汁"]
        },
        "exercise": {
            "recommended": ["太极", "散步", "瑜伽"],
            "avoid": ["接触过敏原运动"],
            "advice": "避免过敏，温和运动"
        },
        "lifestyle": {
            "sleep_time": "22:00前",
            "sleep_duration": "8小时",
            "advice": "避免过敏原，卧室清洁"
        }
    }
}


@router.get("/{constitution_type}")
async def get_recommendations(constitution_type: str):
    """
    获取体质养生推荐

    Args:
        constitution_type: 体质类型
    """
    if constitution_type not in RECOMMENDATIONS:
        return {
            "code": 404,
            "message": "未找到该体质类型",
            "data": None
        }

    return {
        "code": 0,
        "message": "success",
        "data": {
            "constitution_type": constitution_type,
            **RECOMMENDATIONS[constitution_type]
        }
    }


@router.get("/diet/{constitution_type}")
async def get_diet_recommendation(constitution_type: str):
    """获取饮食推荐"""
    if constitution_type not in RECOMMENDATIONS:
        return {"code": 404, "message": "未找到该体质类型"}

    return {
        "code": 0,
        "message": "success",
        "data": RECOMMENDATIONS[constitution_type]["diet"]
    }


@router.get("/exercise/{constitution_type}")
async def get_exercise_recommendation(constitution_type: str):
    """获取运动推荐"""
    if constitution_type not in RECOMMENDATIONS:
        return {"code": 404, "message": "未找到该体质类型"}

    return {
        "code": 0,
        "message": "success",
        "data": RECOMMENDATIONS[constitution_type]["exercise"]
    }


@router.get("/lifestyle/{constitution_type}")
async def get_lifestyle_recommendation(constitution_type: str):
    """获取作息推荐"""
    if constitution_type not in RECOMMENDATIONS:
        return {"code": 404, "message": "未找到该体质类型"}

    return {
        "code": 0,
        "message": "success",
        "data": RECOMMENDATIONS[constitution_type]["lifestyle"]
    }
