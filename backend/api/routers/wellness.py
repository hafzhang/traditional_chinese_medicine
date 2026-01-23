"""
Wellness Router
养生路由 - 季节推荐与食材搭配
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.database import get_db
from api.services.wellness_service import get_wellness_service, WellnessService

router = APIRouter(prefix="/wellness", tags=["wellness"])


@router.get("/seasons/{season}/principles")
async def get_seasonal_principles(
    season: str,
    wellness_service: WellnessService = Depends(get_wellness_service)
):
    """
    获取季节养生原则

    Args:
        season: 季节 (春/夏/秋/冬)

    Returns:
        季节养生原则
    """
    principles = wellness_service.get_seasonal_principles(season)
    if not principles:
        raise HTTPException(status_code=404, detail=f"季节 {season} 的养生原则未找到")

    return {
        "code": 0,
        "data": principles,
        "message": "Success"
    }


@router.get("/seasons/{season}/ingredients")
async def get_seasonal_ingredients(
    season: str,
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(20, ge=1, le=100, description="限制数量"),
    db: Session = Depends(get_db),
    wellness_service: WellnessService = Depends(get_wellness_service)
):
    """
    获取季节推荐食材

    Args:
        season: 季节 (春/夏/秋/冬)
        skip: 跳过数量
        limit: 限制数量

    Returns:
        推荐食材列表
    """
    if season not in ["春", "夏", "秋", "冬"]:
        raise HTTPException(status_code=400, detail="季节参数错误，应为: 春/夏/秋/冬")

    # 获取食材（暂时跳过分页，服务层未实现）
    ingredients = wellness_service.get_seasonal_ingredients(season, db, limit)

    return {
        "code": 0,
        "data": {
            "season": season,
            "ingredients": [
                {
                    "id": ing.id,
                    "name": ing.name,
                    "category": ing.category,
                    "nature": ing.nature,
                    "flavor": ing.flavor,
                    "efficacy": ing.efficacy,
                    "calories": ing.calories,
                    "protein": ing.protein,
                    "image_url": ing.image_url
                }
                for ing in ingredients
            ],
            "total": len(ingredients)
        },
        "message": "Success"
    }


@router.get("/seasons/{season}/recipes")
async def get_seasonal_recipes(
    season: str,
    constitution: str = Query(None, description="体质代码"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(10, ge=1, le=50, description="限制数量"),
    db: Session = Depends(get_db),
    wellness_service: WellnessService = Depends(get_wellness_service)
):
    """
    获取季节推荐食谱

    Args:
        season: 季节 (春/夏/秋/冬)
        constitution: 体质代码 (可选)
        skip: 跳过数量
        limit: 限制数量

    Returns:
        推荐食谱列表
    """
    if season not in ["春", "夏", "秋", "冬"]:
        raise HTTPException(status_code=400, detail="季节参数错误，应为: 春/夏/秋/冬")

    recipes = wellness_service.get_seasonal_recipes(season, db, constitution, limit)

    return {
        "code": 0,
        "data": {
            "season": season,
            "constitution": constitution,
            "recipes": [
                {
                    "id": recipe.id,
                    "name": recipe.name,
                    "type": recipe.type,
                    "difficulty": recipe.difficulty,
                    "cook_time": recipe.cook_time,
                    "servings": recipe.servings,
                    "efficacy": recipe.efficacy,
                    "calories": recipe.calories,
                    "protein": recipe.protein,
                    "image_url": recipe.image_url
                }
                for recipe in recipes
            ],
            "total": len(recipes)
        },
        "message": "Success"
    }


@router.get("/seasons/{season}/wellness-plan")
async def get_seasonal_wellness_plan(
    season: str,
    constitution: str = Query(None, description="体质代码"),
    db: Session = Depends(get_db),
    wellness_service: WellnessService = Depends(get_wellness_service)
):
    """
    获取季节养生方案

    Args:
        season: 季节 (春/夏/秋/冬)
        constitution: 体质代码 (可选)

    Returns:
        季节养生方案
    """
    if season not in ["春", "夏", "秋", "冬"]:
        raise HTTPException(status_code=400, detail="季节参数错误，应为: 春/夏/秋/冬")

    plan = wellness_service.get_seasonal_wellness_plan(season, constitution, db)

    return {
        "code": 0,
        "data": plan,
        "message": "Success"
    }


@router.get("/food-pairing/check")
async def check_food_pairing(
    food1: str = Query(..., description="食材1名称"),
    food2: str = Query(..., description="食材2名称"),
    db: Session = Depends(get_db),
    wellness_service: WellnessService = Depends(get_wellness_service)
):
    """
    检查两食材的搭配相容性

    Args:
        food1: 食材1名称
        food2: 食材2名称

    Returns:
        搭配检查结果
    """
    result = wellness_service.check_food_pairing(food1, food2, db)

    return {
        "code": 0,
        "data": result,
        "message": "Success"
    }


@router.get("/ingredients/{ingredient_id}/pairing")
async def get_ingredient_pairing_suggestions(
    ingredient_id: str,
    limit: int = Query(10, ge=1, le=50, description="限制数量"),
    db: Session = Depends(get_db),
    wellness_service: WellnessService = Depends(get_wellness_service)
):
    """
    获取食材搭配建议

    Args:
        ingredient_id: 食材ID
        limit: 限制数量

    Returns:
        搭配建议
    """
    suggestions = wellness_service.get_ingredient_pairing_suggestions(ingredient_id, db, limit)

    if not suggestions:
        raise HTTPException(status_code=404, detail="食材未找到")

    return {
        "code": 0,
        "data": suggestions,
        "message": "Success"
    }


@router.get("/seasons/list")
async def list_seasons():
    """获取所有季节列表"""
    return {
        "code": 0,
        "data": {
            "seasons": [
                {"value": "春", "name": "春季"},
                {"value": "夏", "name": "夏季"},
                {"value": "秋", "name": "秋季"},
                {"value": "冬", "name": "冬季"}
            ]
        },
        "message": "Success"
    }
