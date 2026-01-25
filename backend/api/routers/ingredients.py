"""
Ingredients API Router
食材 API 路由 - Phase 1
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List

from api.database import get_db
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
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取食材列表

    支持按类别、性味筛选和关键词搜索
    """
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


# 静态列表路由必须放在动态路由之前
@router.get("/categories/list")
async def get_ingredient_categories():
    """
    获取食材类别列表

    标准分类: 谷物、蔬菜、水果、肉类、海鲜、调味品、菌藻、豆类、其他
    """
    categories = [
        {"value": "谷物", "label": "谷物"},
        {"value": "蔬菜", "label": "蔬菜"},
        {"value": "水果", "label": "水果"},
        {"value": "肉类", "label": "肉类"},
        {"value": "海鲜", "label": "海鲜"},
        {"value": "调味品", "label": "调味品"},
        {"value": "菌藻", "label": "菌藻"},
        {"value": "豆类", "label": "豆类"},
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


# 动态路由
@router.get("/recommend/{constitution}", response_model=IngredientRecommendationResponse)
async def get_ingredient_recommendation(
    constitution: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    根据体质获取推荐食材

    返回适合该体质的食材和禁忌食材
    """
    if not ingredient_service.is_valid_constitution_code(constitution):
        raise HTTPException(status_code=400, detail=f"Invalid constitution code: {constitution}")

    result = ingredient_service.get_recommendation_by_constitution(constitution, db)

    return {
        "code": 0,
        "message": "success",
        "data": result
    }


@router.get("/{ingredient_id}", response_model=IngredientDetailResponse)
async def get_ingredient_detail(
    ingredient_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取食材详情
    """
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
            "compatible_foods": ingredient.compatible_foods,
            "incompatible_foods": ingredient.incompatible_foods,
            "classic_combinations": ingredient.classic_combinations,
            "image_url": ingredient.image_url,
            "description": ingredient.description,
            "view_count": ingredient.view_count,
            # 新增营养字段
            "calories": ingredient.calories,
            "protein": ingredient.protein,
            "fat": ingredient.fat,
            "carbohydrates": ingredient.carbohydrates,
            "dietary_fiber": ingredient.dietary_fiber,
            "storage_method": ingredient.storage_method,
            "shelf_life": ingredient.shelf_life
        }
    }


@router.get("/nutrition/filter")
async def filter_ingredients_by_nutrition(
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(20, ge=1, le=100, description="限制数量"),
    min_calories: Optional[float] = Query(None, description="最小热量"),
    max_calories: Optional[float] = Query(None, description="最大热量"),
    min_protein: Optional[float] = Query(None, description="最小蛋白质"),
    max_fat: Optional[float] = Query(None, description="最大脂肪"),
    high_fiber: bool = Query(False, description="高纤维"),
    sort_by: Optional[str] = Query(None, description="排序字段"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    按营养素筛选食材

    支持按热量、蛋白质、脂肪、膳食纤维等筛选
    """
    ingredients, total = ingredient_service.get_ingredients_by_nutrition(
        db=db,
        skip=skip,
        limit=limit,
        min_calories=min_calories,
        max_calories=max_calories,
        min_protein=min_protein,
        max_fat=max_fat,
        high_fiber=high_fiber,
        sort_by=sort_by
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
                    "category": ing.category,
                    "nature": ing.nature,
                    "flavor": ing.flavor,
                    "efficacy": ing.efficacy,
                    "calories": ing.calories,
                    "protein": ing.protein,
                    "fat": ing.fat,
                    "carbohydrates": ing.carbohydrates,
                    "dietary_fiber": ing.dietary_fiber,
                    "image_url": ing.image_url
                }
                for ing in ingredients
            ]
        }
    }


@router.get("/nutrition/{ingredient_id}")
async def get_ingredient_nutrition_detail(
    ingredient_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取食材营养详情

    包含基础营养、维生素、矿物质、食用指导、搭配信息、储存安全、烹饪详情等
    """
    detail = ingredient_service.get_ingredient_nutrition_detail(ingredient_id, db)

    if not detail:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    return {
        "code": 0,
        "message": "success",
        "data": detail
    }


@router.get("/nutrient-rich/{nutrient}")
async def get_nutrient_rich_ingredients(
    nutrient: str,
    limit: int = Query(20, ge=1, le=50, description="限制数量"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取富含特定营养素的食材

    支持的营养素: protein, fiber, calcium, iron, zinc, potassium, vitamin_a, vitamin_c, vitamin_e, calories
    """
    ingredients = ingredient_service.get_nutrient_rich_ingredients(
        nutrient=nutrient,
        db=db,
        limit=limit
    )

    # 营养素中文名称映射
    nutrient_names = {
        "protein": "蛋白质",
        "fiber": "膳食纤维",
        "calcium": "钙",
        "iron": "铁",
        "zinc": "锌",
        "potassium": "钾",
        "vitamin_a": "维生素A",
        "vitamin_c": "维生素C",
        "vitamin_e": "维生素E",
        "calories": "热量"
    }

    return {
        "code": 0,
        "message": "success",
        "data": {
            "nutrient": nutrient,
            "nutrient_name": nutrient_names.get(nutrient, nutrient),
            "total": len(ingredients),
            "items": [
                {
                    "id": ing.id,
                    "name": ing.name,
                    "category": ing.category,
                    "nature": ing.nature,
                    "efficacy": ing.efficacy,
                    "calories": ing.calories,
                    "protein": ing.protein,
                    "fat": ing.fat,
                    "carbohydrates": ing.carbohydrates,
                    "dietary_fiber": ing.dietary_fiber,
                    "image_url": ing.image_url
                }
                for ing in ingredients
            ]
        }
    }
