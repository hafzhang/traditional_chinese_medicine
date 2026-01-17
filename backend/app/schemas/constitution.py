"""
体质相关的数据模型
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class QuestionItem(BaseModel):
    """问卷题目"""
    id: str
    question_text: str
    constitution_type: str
    order_index: int


class QuizSubmitRequest(BaseModel):
    """提交问卷请求"""
    answers: List[int] = Field(..., description="用户答案列表，每个问题1-5分")
    user_info: Optional[Dict] = None


class ScoreItem(BaseModel):
    """得分项"""
    type: str
    name: str
    score: float


class ConstitutionReport(BaseModel):
    """体质报告"""
    name: str
    description: str
    characteristics: List[str]
    advice: str
    score: float
    diet_principle: str
    exercise_principle: str


class QuizResponse(BaseModel):
    """问卷响应"""
    code: int = 0
    message: str = "success"
    data: Dict = None


class RecommendationResponse(BaseModel):
    """推荐响应"""
    code: int = 0
    message: str = "success"
    data: Dict = None
