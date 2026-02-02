"""
Recipes API Router
食谱 API 路由 - Phase 1
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import logging

from api.database import get_db
from api.services.recipe_service import get_recipe_service
from pydantic import BaseModel


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recipes", tags=["recipes"])


# Response Models
class RecipeListResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


class RecipeDetailResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


class RecipeSearchResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


class RecipeRecommendationResponse(BaseModel):
    code: int
    message: str
    data: list


@router.get("", response_model=RecipeListResponse)
async def get_recipes(
    page: int = Query(1, ge=1, description="页码（从1开始）"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    constitution: Optional[str] = Query(None, description="体质筛选"),
    efficacy: Optional[str] = Query(None, description="功效标签筛选"),
    difficulty: Optional[str] = Query(None, description="难度筛选"),
    solar_term: Optional[str] = Query(None, description="节气筛选"),
    season: Optional[str] = Query(None, description="季节筛选"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取食谱列表

    支持按体质、功效、难度、节气、季节筛选
    """
    logger.info(f"API: get_recipes called with params: page={page}, page_size={page_size}, constitution={constitution}, efficacy={efficacy}, difficulty={difficulty}, solar_term={solar_term}, season={season}")

    try:
        recipe_service = get_recipe_service()
        result = recipe_service.get_recipes(
            db=db,
            page=page,
            page_size=page_size,
            constitution=constitution,
            efficacy=efficacy,
            difficulty=difficulty,
            solar_term=solar_term,
            season=season
        )

        # 转换 Recipe 对象为字典
        items = []
        for r in result["items"]:
            items.append({
                "id": r.id,
                "name": r.name,
                "desc": getattr(r, 'desc', None),
                "tip": getattr(r, 'tip', None),
                "cooking_time": r.cooking_time,
                "difficulty": r.difficulty,
                "servings": r.servings,
                "suitable_constitutions": r.suitable_constitutions,
                "avoid_constitutions": r.avoid_constitutions,
                "efficacy_tags": r.efficacy_tags,
                "solar_terms": r.solar_terms,
                "cover_image": r.cover_image,
                "view_count": r.view_count
            })

        return {
            "code": 0,
            "message": "Success",
            "data": {
                "total": result["total"],
                "page": result["page"],
                "page_size": result["page_size"],
                "items": items
            }
        }
    except ValueError as e:
        logger.error(f"API: Validation error in get_recipes: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"API: Error in get_recipes: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/search", response_model=RecipeSearchResponse)
async def search_recipes(
    keyword: str = Query(..., description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码（从1开始）"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    constitution: Optional[str] = Query(None, description="体质筛选"),
    difficulty: Optional[str] = Query(None, description="难度筛选"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    搜索食谱

    搜索范围: 名称、功效标签
    """
    logger.info(f"API: search_recipes called with keyword={keyword}, constitution={constitution}, difficulty={difficulty}")

    try:
        recipe_service = get_recipe_service()
        result = recipe_service.search_recipes(
            keyword=keyword,
            db=db,
            page=page,
            page_size=page_size,
            constitution=constitution,
            difficulty=difficulty
        )

        # 转换 Recipe 对象为字典
        items = []
        for r in result["items"]:
            items.append({
                "id": r.id,
                "name": r.name,
                "desc": getattr(r, 'desc', None),
                "cooking_time": r.cooking_time,
                "difficulty": r.difficulty,
                "efficacy_tags": r.efficacy_tags,
                "cover_image": r.cover_image
            })

        return {
            "code": 0,
            "message": "Success",
            "data": {
                "total": result["total"],
                "page": result["page"],
                "page_size": result["page_size"],
                "items": items
            }
        }
    except ValueError as e:
        logger.error(f"API: Validation error in search_recipes: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"API: Error in search_recipes: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/recommendations", response_model=RecipeRecommendationResponse)
async def get_recommendations(
    constitution: str = Query(..., description="体质代码"),
    limit: int = Query(10, ge=1, le=50, description="限制数量"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    根据体质获取推荐食谱

    优先返回适合该体质，排除禁忌体质
    """
    logger.info(f"API: get_recommendations called with constitution={constitution}, limit={limit}")

    try:
        recipe_service = get_recipe_service()
        recipes = recipe_service.get_recommendations_by_constitution(
            constitution=constitution,
            limit=limit,
            db=db
        )

        # 转换 Recipe 对象为字典
        items = []
        for r in recipes:
            items.append({
                "id": r.id,
                "name": r.name,
                "desc": getattr(r, 'desc', None),
                "cooking_time": r.cooking_time,
                "difficulty": r.difficulty,
                "efficacy_tags": r.efficacy_tags,
                "cover_image": r.cover_image
            })

        return {
            "code": 0,
            "message": "Success",
            "data": items
        }
    except ValueError as e:
        logger.error(f"API: Validation error in get_recommendations: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"API: Error in get_recommendations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{recipe_id}", response_model=RecipeDetailResponse)
async def get_recipe_detail(
    recipe_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取食谱详情
    """
    logger.info(f"API: get_recipe_detail called with recipe_id={recipe_id}")

    try:
        recipe_service = get_recipe_service()
        recipe = recipe_service.get_recipe_by_id(recipe_id, db)

        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")

        return {
            "code": 0,
            "message": "Success",
            "data": {
                "id": recipe.id,
                "name": recipe.name,
                "desc": getattr(recipe, 'desc', None),
                "tip": getattr(recipe, 'tip', None),
                "cooking_time": recipe.cooking_time,
                "difficulty": recipe.difficulty,
                "servings": recipe.servings,
                "suitable_constitutions": recipe.suitable_constitutions,
                "avoid_constitutions": recipe.avoid_constitutions,
                "efficacy_tags": recipe.efficacy_tags,
                "solar_terms": recipe.solar_terms,
                "cover_image": recipe.cover_image,
                "ingredients": recipe.ingredients,
                "steps": recipe.steps,
                "view_count": recipe.view_count
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"API: Error in get_recipe_detail: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
