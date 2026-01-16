"""
Constitution API Router
体质识别 API 路由
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
import uuid

from api.database import get_db
from api.models import ConstitutionResult, User
from api.schemas.constitution import (
    TestSubmitRequest,
    TestSubmitResponse,
    FoodRecommendationResponse
)
from api.services.constitution import ConstitutionAnalyzer


router = APIRouter(tags=["constitution"])

# Initialize analyzer (singleton)
analyzer = ConstitutionAnalyzer()


@router.post("/test/submit", response_model=TestSubmitResponse)
async def submit_test(
    request_data: TestSubmitRequest,
    request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    提交体质测试

    Args:
        request_data: 测试答案数据
        request: FastAPI Request对象
        db: 数据库会话

    Returns:
        测试结果，包含主要体质、次要体质和各项分数
    """
    try:
        # 1. 调用分析服务进行体质判定
        analysis_result = analyzer.analyze(request_data.answers)

        # 2. 生成结果ID
        result_id = str(uuid.uuid4())

        # 3. 查找或创建用户
        user_id = None
        if request_data.user_id:
            from api.models import User
            user = db.query(User).filter(User.id == request_data.user_id).first()
            if user:
                user_id = user.id

        # 4. 保存测试结果到数据库
        result = ConstitutionResult(
            id=result_id,
            user_id=user_id,
            primary_constitution=analysis_result["primary_constitution"],
            secondary_constitutions=analysis_result["secondary_constitutions"],
            scores=analysis_result["scores"],
            answers=request_data.answers,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )
        db.add(result)
        db.commit()

        # 5. 构建响应数据
        response_data = {
            "result_id": result_id,
            "primary_constitution": analysis_result["primary_constitution"],
            "primary_constitution_name": analysis_result["primary_constitution_name"],
            "secondary_constitutions": analysis_result["secondary_constitutions"],
            "scores": analysis_result["scores"],
            "report_url": f"/api/v1/result/{result_id}"
        }

        return TestSubmitResponse(
            code=0,
            message="success",
            data=response_data
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/result/{result_id}")
async def get_result(
    result_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取测试结果详情

    Args:
        result_id: 结果ID
        db: 数据库会话

    Returns:
        完整的测试结果，包含体质特征和调理建议
    """
    # 查询结果
    result = db.query(ConstitutionResult).filter(
        ConstitutionResult.id == result_id
    ).first()

    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    # 获取体质信息（静态数据）
    from api.data.constitution_info import CONSTITUTION_INFO_DATA
    constitution_info = CONSTITUTION_INFO_DATA.get(
        result.primary_constitution,
        CONSTITUTION_INFO_DATA.get("peace", {})
    )

    # 构建响应
    response_data = {
        "result_id": str(result.id),
        "user_id": str(result.user_id) if result.user_id else None,
        "primary_constitution": result.primary_constitution,
        "primary_constitution_name": constitution_info.get("name", "未知"),
        "secondary_constitutions": result.secondary_constitutions or [],
        "scores": result.scores,
        "characteristics": constitution_info.get("characteristics", {}),
        "regulation_principles": constitution_info.get("regulation_principles", {}),
        "created_at": result.created_at.isoformat() if result.created_at else None
    }

    return {
        "code": 0,
        "message": "success",
        "data": response_data
    }


@router.get("/recommend/food", response_model=FoodRecommendationResponse)
async def get_food_recommendations(
    constitution: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取饮食推荐

    Args:
        constitution: 体质类型
        db: 数据库会话

    Returns:
        推荐食物、不宜食物和推荐食谱
    """
    from api.models import Food, Recipe

    # 查询推荐食物
    recommended_foods = db.query(Food).filter(
        Food.suitable_constitutions.contains([constitution])
    ).limit(10).all()

    # 查询不宜食物
    avoid_foods = db.query(Food).filter(
        Food.avoid_constitutions.contains([constitution])
    ).limit(10).all()

    # 查询推荐食谱
    recipes = db.query(Recipe).filter(
        Recipe.suitable_constitutions.contains([constitution])
    ).limit(5).all()

    # 构建响应
    response_data = {
        "constitution": constitution,
        "constitution_name": analyzer.scorer.CONSTITUTION_TYPES.get(
            constitution, constitution
        ),
        "recommended_foods": [
            {
                "name": food.name,
                "nature": food.nature,
                "flavor": food.flavor,
                "effects": food.effects
            }
            for food in recommended_foods
        ],
        "avoid_foods": [
            {
                "name": food.name,
                "reason": "不宜该体质食用"
            }
            for food in avoid_foods
        ],
        "recipes": [
            {
                "name": recipe.name,
                "description": recipe.description
            }
            for recipe in recipes
        ]
    }

    return FoodRecommendationResponse(
        code=0,
        message="success",
        data=response_data
    )


@router.get("/questions")
async def get_questions(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    获取测试题目列表

    Args:
        db: 数据库会话

    Returns:
        30个测试题目
    """
    from api.models import Question

    questions = db.query(Question).order_by(Question.question_number).all()

    questions_data = [
        {
            "number": q.question_number,
            "content": q.content,
            "constitution_type": q.constitution_type,
            "options": q.options or {
                "1": "没有",
                "2": "很少",
                "3": "有时",
                "4": "经常",
                "5": "总是"
            }
        }
        for q in questions
    ]

    return {
        "code": 0,
        "message": "success",
        "data": {
            "total": len(questions_data),
            "questions": questions_data
        }
    }
