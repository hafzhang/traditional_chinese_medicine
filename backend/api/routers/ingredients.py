"""
Ingredients API Router
食材 API 路由 - Phase 1
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List

from api.database import get_db_optional
from api.services.ingredient_service import get_ingredient_service
from pydantic import BaseModel


router = APIRouter(prefix="/ingredients", tags=["ingredients"])

ingredient_service = get_ingredient_service()


# Response Models
class IngredientListResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


class IngredientDetailResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


class IngredientRecommendationResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


@router.get("", response_model=IngredientListResponse)
async def get_ingredients(
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(20, ge=1, le=100, description="限制数量"),
    category: Optional[str] = Query(None, description="类别筛选"),
    nature: Optional[str] = Query(None, description="性味筛选"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db_optional)
) -> Dict[str, Any]:
    """
    获取食材列表

    支持按类别、性味筛选和关键词搜索
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    ingredients, total = ingredient_service.get_ingredients_list(
        db=db,
        skip=skip,
        limit=limit,
        category=category,
        nature=nature,
        search=search
    )

    return {
        "code": 0,
        "message": "success",
        "data": {
            "total": total,
            "items": [
                {
                    "id": ing.id,
                    "name": ing.name,
                    "aliases": ing.aliases,
                    "category": ing.category,
                    "nature": ing.nature,
                    "flavor": ing.flavor,
                    "efficacy": ing.efficacy,
                    "image_url": ing.image_url,
                    "view_count": ing.view_count
                }
                for ing in ingredients
            ]
        }
    }


@router.get("/{ingredient_id}", response_model=IngredientDetailResponse)
async def get_ingredient_detail(
    ingredient_id: str,
    db: Session = Depends(get_db_optional)
) -> Dict[str, Any]:
    """
    获取食材详情
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    ingredient = ingredient_service.get_ingredient_by_id(ingredient_id, db)

    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    # 增加浏览次数
    ingredient_service.increment_view_count(ingredient_id, db)

    return {
        "code": 0,
        "message": "success",
        "data": {
            "id": ingredient.id,
            "name": ingredient.name,
            "aliases": ingredient.aliases,
            "category": ingredient.category,
            "nature": ingredient.nature,
            "flavor": ingredient.flavor,
            "meridians": ingredient.meridians,
            "suitable_constitutions": ingredient.suitable_constitutions,
            "avoid_constitutions": ingredient.avoid_constitutions,
            "efficacy": ingredient.efficacy,
            "nutrition": ingredient.nutrition,
            "cooking_methods": ingredient.cooking_methods,
            "daily_dosage": ingredient.daily_dosage,
            "best_time": ingredient.best_time,
            "precautions": ingredient.precautions,
            "compatible_with": ingredient.compatible_with,
            "incompatible_with": ingredient.incompatible_with,
            "image_url": ingredient.image_url,
            "description": ingredient.description,
            "view_count": ingredient.view_count
        }
    }


@router.get("/recommend/{constitution}", response_model=IngredientRecommendationResponse)
async def get_ingredient_recommendation(
    constitution: str,
    db: Session = Depends(get_db_optional)
) -> Dict[str, Any]:
    """
    根据体质获取推荐食材

    返回适合该体质的食材和禁忌食材
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    if not ingredient_service.is_valid_constitution_code(constitution):
        raise HTTPException(status_code=400, detail=f"Invalid constitution code: {constitution}")

    result = ingredient_service.get_recommendation_by_constitution(constitution, db)

    return {
        "code": 0,
        "message": "success",
        "data": result
    }


@router.get("/categories/list")
async def get_ingredient_categories() -> Dict[str, Any]:
    """
    获取食材类别列表
    """
    categories = [
        {"value": "谷物", "label": "谷物"},
        {"value": "蔬菜", "label": "蔬菜"},
        {"value": "水果", "label": "水果"},
        {"value": "肉类", "label": "肉类"},
        {"value": "水产", "label": "水产"},
        {"value": "药材", "label": "药材"},
        {"value": "调味品", "label": "调味品"},
        {"value": "其他", "label": "其他"}
    ]

    return {
        "code": 0,
        "message": "success",
        "data": categories
    }


@router.get("/natures/list")
async def get_ingredient_natures() -> Dict[str, Any]:
    """
    获取食材性味列表
    """
    natures = [
        {"value": "寒", "label": "寒"},
        {"value": "凉", "label": "凉"},
        {"value": "平", "label": "平"},
        {"value": "温", "label": "温"},
        {"value": "热", "label": "热"}
    ]

    return {
        "code": 0,
        "message": "success",
        "data": natures
    }
