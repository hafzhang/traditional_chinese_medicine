"""
Recipe Schemas
菜谱相关的 Pydantic 验证模型
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


# Difficulty enum values
DIFFICULTY_VALUES = ("easy", "medium", "harder", "hard")

DIFFICULTY_LABELS = {
    "easy": "简单",
    "medium": "中等",
    "harder": "较难",
    "hard": "困难",
}


class RecipeIngredientItem(BaseModel):
    """Recipe ingredient item for response"""
    id: str
    ingredient_id: Optional[str] = None
    ingredient_name: str
    amount: Optional[str] = None
    is_main: bool = False

    class Config:
        from_attributes = True


class RecipeStepItem(BaseModel):
    """Recipe step item for response"""
    id: str
    step_number: int
    description: str
    duration: Optional[int] = None

    class Config:
        from_attributes = True


class RecipeBase(BaseModel):
    """Base recipe schema with common fields"""
    name: str = Field(..., min_length=1, max_length=200, description="菜谱名称")
    desc: Optional[str] = Field(None, description="简介/个人体验")
    tip: Optional[str] = Field(None, description="烹饪贴士")
    cooking_time: Optional[int] = Field(None, ge=0, description="烹饪时间（分钟）")
    difficulty: Optional[str] = Field(None, pattern=r"^(easy|medium|harder|hard)$", description="难度等级")
    cover_image: Optional[str] = Field(None, description="封面图片URL")
    suitable_constitutions: Optional[List[str]] = Field(default_factory=list, description="适用体质")
    avoid_constitutions: Optional[List[str]] = Field(default_factory=list, description="禁忌体质")
    efficacy_tags: Optional[List[str]] = Field(default_factory=list, description="功效标签")
    solar_terms: Optional[List[str]] = Field(default_factory=list, description="节气标签")
    symptoms: Optional[List[str]] = Field(default_factory=list, description="主治症状")
    suitable_seasons: Optional[List[str]] = Field(default_factory=list, description="适用季节")
    type: Optional[str] = Field(None, description="食谱类型")
    servings: Optional[int] = Field(None, ge=1, description="份量")


class RecipeCreate(RecipeBase):
    """Schema for creating a new recipe"""
    pass


class RecipeUpdate(BaseModel):
    """Schema for updating a recipe - all fields optional"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    desc: Optional[str] = None
    tip: Optional[str] = None
    cooking_time: Optional[int] = Field(None, ge=0)
    difficulty: Optional[str] = Field(None, pattern=r"^(easy|medium|harder|hard)$")
    cover_image: Optional[str] = None
    suitable_constitutions: Optional[List[str]] = None
    avoid_constitutions: Optional[List[str]] = None
    efficacy_tags: Optional[List[str]] = None
    solar_terms: Optional[List[str]] = None
    symptoms: Optional[List[str]] = None
    suitable_seasons: Optional[List[str]] = None
    type: Optional[str] = None
    servings: Optional[int] = Field(None, ge=1)


class RecipeResponse(RecipeBase):
    """Full recipe response with all fields"""
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_deleted: bool = False

    # Nutrition fields (optional)
    calories: Optional[float] = None
    protein: Optional[float] = None
    fat: Optional[float] = None
    carbohydrates: Optional[float] = None
    dietary_fiber: Optional[float] = None

    # Additional fields
    efficacy: Optional[str] = None
    health_benefits: Optional[str] = None
    precautions: Optional[str] = None
    tags: Optional[List[str]] = None
    meal_type: Optional[str] = None

    # Statistics
    view_count: int = 0
    favorite_count: int = 0

    class Config:
        from_attributes = True


class RecipeDetailResponse(RecipeResponse):
    """Recipe detail with ingredients and steps"""
    ingredients: List[RecipeIngredientItem] = []
    steps: List[RecipeStepItem] = []


class RecipeListItem(BaseModel):
    """Simplified recipe item for list views"""
    id: str
    name: str
    desc: Optional[str] = None
    cooking_time: Optional[int] = None
    difficulty: Optional[str] = None
    cover_image: Optional[str] = None
    efficacy_tags: List[str] = []
    suitable_constitutions: List[str] = []
    solar_terms: List[str] = []
    view_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class RecipeListResponse(BaseModel):
    """Response wrapper for recipe lists"""
    total: int = Field(..., ge=0, description="Total number of recipes")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, description="Number of items per page")
    items: List[RecipeListItem] = Field(default_factory=list, description="List of recipes")


# Standard response wrapper
class StandardResponse(BaseModel):
    """Standard API response wrapper"""
    code: int = Field(0, description="Response code: 0 for success, -1 for error")
    message: Optional[str] = Field(None, description="Response message")
    data: Optional[dict] = Field(None, description="Response data")
