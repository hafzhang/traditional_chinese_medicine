"""
Recipes API Router
食谱 API 路由 - Phase 1
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from api.database import get_db
from api.services.recipe_service import get_recipe_service
from pydantic import BaseModel


router = APIRouter(prefix="/recipes", tags=["recipes"])

recipe_service = get_recipe_service()


# Response Models
class RecipeListResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


class RecipeDetailResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


class RecipeRecommendationResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


@router.get("", response_model=RecipeListResponse)
async def get_recipes(
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(20, ge=1, le=100, description="限制数量"),
    type: Optional[str] = Query(None, description="类型筛选"),
    difficulty: Optional[str] = Query(None, description="难度筛选"),
    constitution: Optional[str] = Query(None, description="体质筛选"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取食谱列表

    支持按类型、难度、体质筛选和关键词搜索
    """
    recipes, total = recipe_service.get_recipes_list(
        db=db,
        skip=skip,
        limit=limit,
        type=type,
        difficulty=difficulty,
        constitution=constitution,
        search=search
    )

    return {
        "code": 0,
        "message": "success",
        "data": {
            "total": total,
            "items": [
                {
                    "id": r.id,
                    "name": r.name,
                    "type": r.type,
                    "difficulty": r.difficulty,
                    "cooking_time": r.cooking_time or r.cook_time,  # PRD 字段，fallback 到旧字段
                    "servings": r.servings,
                    "image_url": r.image_url,
                    "cover_image": getattr(r, 'cover_image', None),  # PRD 字段
                    "view_count": r.view_count
                }
                for r in recipes
            ]
        }
    }


@router.get("/{recipe_id}", response_model=RecipeDetailResponse)
async def get_recipe_detail(
    recipe_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取食谱详情
    """
    recipe = recipe_service.get_recipe_by_id(recipe_id, db)

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # 增加浏览次数
    recipe_service.increment_view_count(recipe_id, db)

    return {
        "code": 0,
        "message": "success",
        "data": {
            "id": recipe.id,
            "name": recipe.name,
            "type": recipe.type,
            "difficulty": recipe.difficulty,
            "cooking_time": recipe.cooking_time or recipe.cook_time,  # PRD 字段，fallback 到旧字段
            "servings": recipe.servings,
            "desc": getattr(recipe, 'desc', None),  # PRD 字段
            "tip": getattr(recipe, 'tip', None),  # PRD 字段
            "suitable_constitutions": recipe.suitable_constitutions,
            "avoid_constitutions": getattr(recipe, 'avoid_constitutions', None),  # PRD 字段
            "symptoms": recipe.symptoms,
            "suitable_seasons": recipe.suitable_seasons,
            "efficacy_tags": getattr(recipe, 'efficacy_tags', None),  # PRD 字段
            "solar_terms": getattr(recipe, 'solar_terms', None),  # PRD 字段
            "ingredients": recipe.ingredients,
            "steps": recipe.steps,
            "efficacy": recipe.efficacy,
            "health_benefits": recipe.health_benefits,
            "precautions": recipe.precautions,
            "tags": recipe.tags,
            "cover_image": getattr(recipe, 'cover_image', None),  # PRD 字段
            "image_url": recipe.image_url,
            "description": recipe.description,
            "view_count": recipe.view_count
        }
    }


@router.get("/recommend/{constitution}", response_model=RecipeRecommendationResponse)
async def get_recipe_recommendation(
    constitution: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    根据体质获取三餐推荐食谱

    返回早餐、午餐、晚餐的推荐食谱
    """
    if not recipe_service.is_valid_constitution_code(constitution):
        raise HTTPException(status_code=400, detail=f"Invalid constitution code: {constitution}")

    result = recipe_service.get_recommendations_by_constitution(constitution, db)

    return {
        "code": 0,
        "message": "success",
        "data": result
    }


@router.get("/types/list")
async def get_recipe_types() -> Dict[str, Any]:
    """
    获取食谱类型列表
    """
    types = [
        {"value": "粥类", "label": "粥类"},
        {"value": "汤类", "label": "汤类"},
        {"value": "茶饮", "label": "茶饮"},
        {"value": "菜肴", "label": "菜肴"},
        {"value": "小吃", "label": "小吃"},
        {"value": "主食", "label": "主食"}
    ]

    return {
        "code": 0,
        "message": "success",
        "data": types
    }


@router.get("/difficulties/list")
async def get_recipe_difficulties() -> Dict[str, Any]:
    """
    获取食谱难度列表
    """
    difficulties = [
        {"value": "简单", "label": "简单"},
        {"value": "中等", "label": "中等"},
        {"value": "困难", "label": "困难"}
    ]

    return {
        "code": 0,
        "message": "success",
        "data": difficulties
    }
