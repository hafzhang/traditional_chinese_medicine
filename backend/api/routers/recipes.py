"""
Recipes API Router
食谱 API 路由 - Excel Import
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

from api.database import get_db
from api.services.recipe_service import get_recipe_service


router = APIRouter(prefix="/recipes", tags=["recipes"])

recipe_service = get_recipe_service()


# Request/Response Models
class RecipeListParams(BaseModel):
    """菜谱列表查询参数"""
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")
    constitution: Optional[str] = Field(None, description="体质筛选")
    efficacy: Optional[str] = Field(None, description="功效标签筛选")
    solar_term: Optional[str] = Field(None, description="节气筛选")
    difficulty: Optional[str] = Field(None, description="难度筛选")
    max_cooking_time: Optional[int] = Field(None, ge=0, description="最大烹饪时间(分钟)")
    sort_by: Optional[str] = Field("created_at_desc", description="排序方式")


class RecipeListResponse(BaseModel):
    code: int
    data: Dict[str, Any]


class RecipeDetailResponse(BaseModel):
    code: int
    data: Dict[str, Any]


class RecipeSearchResponse(BaseModel):
    code: int
    data: Dict[str, Any]


class RecipeRecommendationResponse(BaseModel):
    code: int
    data: Dict[str, Any]


@router.get("", response_model=RecipeListResponse)
async def get_recipes(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    constitution: Optional[str] = Query(None, description="体质筛选"),
    efficacy: Optional[str] = Query(None, description="功效标签筛选"),
    solar_term: Optional[str] = Query(None, description="节气筛选"),
    difficulty: Optional[str] = Query(None, description="难度筛选"),
    max_cooking_time: Optional[int] = Query(None, ge=0, description="最大烹饪时间(分钟)"),
    sort_by: Optional[str] = Query("created_at_desc", description="排序方式: created_at_desc, view_count_desc, cooking_time_asc"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取菜谱列表

    支持按体质、功效、节气、难度、烹饪时间筛选，支持分页和排序
    不需要认证
    """
    # Build filters dict
    filters = {}
    if constitution:
        filters["constitution"] = constitution
    if efficacy:
        filters["efficacy"] = efficacy
    if solar_term:
        filters["solar_term"] = solar_term
    if difficulty:
        filters["difficulty"] = difficulty
    if max_cooking_time is not None:
        filters["max_cooking_time"] = max_cooking_time
    if sort_by:
        filters["sort_by"] = sort_by

    # Call service
    result = recipe_service.get_recipes(
        filters=filters,
        page=page,
        page_size=page_size,
        db=db
    )

    return {
        "code": 0,
        "data": result
    }


@router.get("/search", response_model=RecipeSearchResponse)
async def search_recipes(
    keyword: str = Query(..., min_length=1, description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    搜索菜谱

    按菜谱名称、食材、功效标签搜索
    不需要认证
    """
    result = recipe_service.search_recipes(
        keyword=keyword,
        page=page,
        page_size=page_size,
        db=db
    )

    return {
        "code": 0,
        "data": result
    }


@router.get("/recommend", response_model=RecipeRecommendationResponse)
async def get_recommendations(
    recommend_type: str = Query(..., description="推荐类型: constitution, solar_term, efficacy"),
    constitution: Optional[str] = Query(None, description="体质代码 (当recommend_type=constitution时必需)"),
    solar_term: Optional[str] = Query(None, description="节气名称 (当recommend_type=solar_term时必需)"),
    efficacy: Optional[str] = Query(None, description="功效标签 (当recommend_type=efficacy时必需)"),
    limit: int = Query(10, ge=1, le=50, description="限制数量"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取推荐菜谱

    支持按体质、节气、功效推荐
    不需要认证
    """
    # Build params dict
    params = {}
    if recommend_type == "constitution":
        if not constitution:
            raise HTTPException(status_code=400, detail="constitution parameter is required for constitution recommendations")
        params["constitution"] = constitution
    elif recommend_type == "solar_term":
        if not solar_term:
            raise HTTPException(status_code=400, detail="solar_term parameter is required for solar_term recommendations")
        params["solar_term"] = solar_term
    elif recommend_type == "efficacy":
        if not efficacy:
            raise HTTPException(status_code=400, detail="efficacy parameter is required for efficacy recommendations")
        params["efficacy"] = efficacy
    else:
        raise HTTPException(status_code=400, detail=f"Invalid recommend_type: {recommend_type}. Must be one of: constitution, solar_term, efficacy")

    result = recipe_service.get_recommendations(
        recommend_type=recommend_type,
        params=params,
        limit=limit,
        db=db
    )

    return {
        "code": 0,
        "data": result
    }


@router.get("/{recipe_id}", response_model=RecipeDetailResponse)
async def get_recipe_detail(
    recipe_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取菜谱详情

    返回含desc、tip、ingredients(含nature/taste)、steps的完整数据
    不需要认证
    """
    recipe = recipe_service.get_recipe_by_id(recipe_id, db)

    if not recipe:
        raise HTTPException(status_code=404, detail="菜谱不存在")

    # 增加浏览次数
    recipe_service.increment_view_count(recipe_id, db)

    return {
        "code": 0,
        "data": recipe
    }


# Static list routes (must come before dynamic routes)
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
        "data": difficulties
    }
