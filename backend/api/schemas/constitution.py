"""
Pydantic Schemas for Constitution API
体质识别 API 数据模型
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from datetime import datetime


# ============ Request Models ============

class TestSubmitRequest(BaseModel):
    """体质测试提交请求"""

    answers: List[int] = Field(
        ...,
        description="30个问题的答案列表，每个答案为1-5分",
        min_length=30,
        max_length=30
    )
    user_id: Optional[str] = Field(None, description="用户ID（可选）")
    anonymous_id: Optional[str] = Field(None, description="匿名用户ID")
    device_id: Optional[str] = Field(None, description="设备ID")
    platform: Optional[str] = Field("unknown", description="平台：douyin/wechat/h5")

    @validator('answers')
    def validate_answers(cls, v):
        """验证答案范围"""
        for i, answer in enumerate(v, 1):
            if not 1 <= answer <= 5:
                raise ValueError(f"第{i}题答案必须在1-5之间，当前值: {answer}")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "answers": [3, 4, 2, 5] * 7 + [3, 4],  # 30个答案
                "user_id": "uuid-xxx",
                "platform": "douyin"
            }
        }


# ============ Response Models ============

class SecondaryConstitution(BaseModel):
    """次要体质"""
    type: str = Field(..., description="体质类型标识")
    name: str = Field(..., description="体质类型中文名称")
    score: float = Field(..., description="分数")


class TestSubmitResponse(BaseModel):
    """测试提交响应"""
    code: int = Field(0, description="响应码，0表示成功")
    message: str = Field("success", description="响应消息")
    data: Dict[str, Any] = Field(..., description="响应数据")

    class Config:
        json_schema_extra = {
            "example": {
                "code": 0,
                "message": "success",
                "data": {
                    "result_id": "uuid-xxx",
                    "primary_constitution": "qi_deficiency",
                    "primary_constitution_name": "气虚质",
                    "secondary_constitutions": [
                        {
                            "type": "yang_deficiency",
                            "name": "阳虚质",
                            "score": 35.0
                        }
                    ],
                    "scores": {
                        "peace": 25.0,
                        "qi_deficiency": 85.0,
                        "yang_deficiency": 35.0,
                        "yin_deficiency": 20.0,
                        "phlegm_damp": 15.0,
                        "damp_heat": 10.0,
                        "blood_stasis": 5.0,
                        "qi_depression": 25.0,
                        "special": 10.0
                    },
                    "report_url": "/api/v1/result/uuid-xxx"
                }
            }
        }


class ConstitutionCharacteristic(BaseModel):
    """体质特征"""
    title: str
    items: List[str]


class RegulationPrinciple(BaseModel):
    """调理原则"""
    diet: List[str]
    exercise: List[str]
    lifestyle: List[str]
    emotion: Optional[List[str]] = None


class ConstitutionInfo(BaseModel):
    """体质信息"""
    result_id: str
    user_id: Optional[str]
    primary_constitution: str
    primary_constitution_name: str
    secondary_constitutions: List[SecondaryConstitution]
    scores: Dict[str, float]
    characteristics: ConstitutionCharacteristic
    regulation_principles: RegulationPrinciple
    created_at: datetime


class FoodItem(BaseModel):
    """食物条目"""
    name: str
    nature: Optional[str] = None
    flavor: Optional[str] = None
    effects: Optional[List[str]] = None


class FoodRecommendationResponse(BaseModel):
    """饮食推荐响应"""
    code: int
    message: str
    data: Dict[str, Any]

    class Config:
        json_schema_extra = {
            "example": {
                "code": 0,
                "message": "success",
                "data": {
                    "constitution": "qi_deficiency",
                    "constitution_name": "气虚质",
                    "recommended_foods": [
                        {
                            "name": "山药",
                            "nature": "平",
                            "flavor": "甘",
                            "effects": ["补脾养胃", "生津益肺"]
                        }
                    ],
                    "avoid_foods": [
                        {
                            "name": "山楂",
                            "reason": "破气作用"
                        }
                    ],
                    "recipes": [
                        {
                            "name": "黄芪炖鸡",
                            "description": "补气养血"
                        }
                    ]
                }
            }
        }


# ============ Error Models ============

class ErrorResponse(BaseModel):
    """错误响应"""
    code: int = Field(-1, ge=-100, le=0)
    message: str
    detail: Optional[str] = None
