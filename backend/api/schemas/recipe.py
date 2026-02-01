"""
Pydantic Schemas for Recipe API
菜谱 API 数据模型
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional
from datetime import datetime


# ============ Base Schema ============

class RecipeBase(BaseModel):
    """菜谱基础 Schema"""
    name: str = Field(..., min_length=1, max_length=100, description="菜谱名称")
    desc: Optional[str] = Field(None, description="菜谱描述")
    tip: Optional[str] = Field(None, description="小贴士")
    cooking_time: Optional[int] = Field(None, ge=0, description="烹饪时间（分钟）")
    difficulty: Optional[str] = Field(None, description="难度等级：easy/medium/harder/hard")
    suitable_constitutions: Optional[List[str]] = Field(default_factory=list, description="适用体质列表")
    avoid_constitutions: Optional[List[str]] = Field(default_factory=list, description="禁忌体质列表")
    efficacy_tags: Optional[List[str]] = Field(default_factory=list, description="功效标签")
    solar_terms: Optional[List[str]] = Field(default_factory=list, description="节气标签")

    @field_validator('difficulty')
    @classmethod
    def validate_difficulty(cls, v: Optional[str]) -> Optional[str]:
        """验证难度等级"""
        if v is None:
            return v
        valid_difficulties = ['easy', 'medium', 'harder', 'hard']
        if v not in valid_difficulties:
            raise ValueError(f"难度必须是 {valid_difficulties} 之一，当前值: {v}")
        return v

    @field_validator('suitable_constitutions', 'avoid_constitutions', mode='before')
    @classmethod
    def validate_constitutions(cls, v: Any) -> List[str]:
        """验证体质列表"""
        if v is None:
            return []
        valid_constitutions = {
            'peace', 'qi_deficiency', 'yang_deficiency', 'yin_deficiency',
            'phlegm_damp', 'damp_heat', 'blood_stasis', 'qi_depression', 'special'
        }
        if isinstance(v, list):
            for constitution in v:
                if constitution not in valid_constitutions:
                    raise ValueError(f"无效的体质代码: {constitution}，有效值: {valid_constitutions}")
            return v
        return []

    class Config:
        from_attributes = True


# ============ Create/Update Schemas ============

class RecipeCreate(RecipeBase):
    """创建菜谱 Schema"""
    ingredients: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list,
        description="食材列表，每个元素包含 ingredient_name, amount, is_main 等"
    )
    steps: Optional[List[str]] = Field(
        default_factory=list,
        description="制作步骤列表"
    )


class RecipeUpdate(BaseModel):
    """更新菜谱 Schema（所有字段可选）"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    desc: Optional[str] = None
    tip: Optional[str] = None
    cooking_time: Optional[int] = Field(None, ge=0)
    difficulty: Optional[str] = None
    suitable_constitutions: Optional[List[str]] = None
    avoid_constitutions: Optional[List[str]] = None
    efficacy_tags: Optional[List[str]] = None
    solar_terms: Optional[List[str]] = None
    ingredients: Optional[List[Dict[str, Any]]] = None
    steps: Optional[List[str]] = None

    @field_validator('difficulty')
    @classmethod
    def validate_difficulty(cls, v: Optional[str]) -> Optional[str]:
        """验证难度等级"""
        if v is None:
            return v
        valid_difficulties = ['easy', 'medium', 'harder', 'hard']
        if v not in valid_difficulties:
            raise ValueError(f"难度必须是 {valid_difficulties} 之一，当前值: {v}")
        return v

    @field_validator('suitable_constitutions', 'avoid_constitutions', mode='before')
    @classmethod
    def validate_constitutions(cls, v: Any) -> Optional[List[str]]:
        """验证体质列表"""
        if v is None:
            return None
        valid_constitutions = {
            'peace', 'qi_deficiency', 'yang_deficiency', 'yin_deficiency',
            'phlegm_damp', 'damp_heat', 'blood_stasis', 'qi_depression', 'special'
        }
        if isinstance(v, list):
            for constitution in v:
                if constitution not in valid_constitutions:
                    raise ValueError(f"无效的体质代码: {constitution}")
            return v
        return None


# ============ Response Schemas ============

class RecipeIngredientItem(BaseModel):
    """菜谱食材项"""
    id: str
    ingredient_id: Optional[str] = None
    ingredient_name: str
    amount: Optional[str] = None
    is_main: bool = False
    display_order: int = 0

    class Config:
        from_attributes = True


class RecipeStepItem(BaseModel):
    """菜谱步骤项"""
    id: str
    step_number: int
    description: str
    duration: Optional[int] = None

    class Config:
        from_attributes = True


class RecipeResponse(RecipeBase):
    """菜谱详情响应"""
    id: str
    ingredients: List[RecipeIngredientItem] = Field(default_factory=list)
    steps: List[RecipeStepItem] = Field(default_factory=list)
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============ List Item Schemas ============

class RecipeListItem(BaseModel):
    """菜谱列表项"""
    id: str
    name: str
    desc: Optional[str] = None
    cooking_time: Optional[int] = None
    difficulty: Optional[str] = None
    suitable_constitutions: List[str] = Field(default_factory=list)
    efficacy_tags: List[str] = Field(default_factory=list)
    solar_terms: List[str] = Field(default_factory=list)
    created_at: datetime

    class Config:
        from_attributes = True


class RecipeListResponse(BaseModel):
    """菜谱列表响应"""
    total: int = Field(..., ge=0, description="总数")
    page: int = Field(..., ge=1, description="当前页码")
    page_size: int = Field(..., ge=1, description="每页数量")
    items: List[RecipeListItem] = Field(default_factory=list, description="菜谱列表")


# ============ Import Schema (for Excel import) ============

class RecipeImportBase(BaseModel):
    """导入专用 Schema - 允许额外字段"""
    name: Optional[str] = None
    desc: Optional[str] = None
    tip: Optional[str] = None
    cooking_time: Optional[str] = None  # 原始字符串，需要解析
    difficulty: Optional[str] = None
    suitable_constitutions: Optional[Any] = None  # 可能是字符串或列表
    avoid_constitutions: Optional[Any] = None
    efficacy_tags: Optional[Any] = None
    solar_terms: Optional[Any] = None
    ingredients_str: Optional[str] = None  # 食材字符串，需要解析
    steps_str: Optional[str] = None  # 步骤字符串，需要解析

    class Config:
        extra = 'allow'  # 允许额外字段，因为 Excel 可能有未预期的列


# ============ Search/Filter Schemas ============

class RecipeSearchRequest(BaseModel):
    """菜谱搜索请求"""
    keyword: str = Field(..., min_length=1, description="搜索关键词")
    constitution: Optional[str] = Field(None, description="按体质筛选")
    difficulty: Optional[str] = Field(None, description="按难度筛选")
    solar_term: Optional[str] = Field(None, description="按节气筛选")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")

    @field_validator('constitution')
    @classmethod
    def validate_constitution(cls, v: Optional[str]) -> Optional[str]:
        """验证体质代码"""
        if v is None:
            return v
        valid_constitutions = {
            'peace', 'qi_deficiency', 'yang_deficiency', 'yin_deficiency',
            'phlegm_damp', 'damp_heat', 'blood_stasis', 'qi_depression', 'special'
        }
        if v not in valid_constitutions:
            raise ValueError(f"无效的体质代码: {v}")
        return v

    @field_validator('difficulty')
    @classmethod
    def validate_difficulty(cls, v: Optional[str]) -> Optional[str]:
        """验证难度等级"""
        if v is None:
            return v
        valid_difficulties = ['easy', 'medium', 'harder', 'hard']
        if v not in valid_difficulties:
            raise ValueError(f"难度必须是 {valid_difficulties} 之一")
        return v


class RecipeRecommendationRequest(BaseModel):
    """菜谱推荐请求"""
    constitution: str = Field(..., description="体质类型")
    limit: int = Field(20, ge=1, le=100, description="返回数量限制")

    @field_validator('constitution')
    @classmethod
    def validate_constitution(cls, v: str) -> str:
        """验证体质代码"""
        valid_constitutions = {
            'peace', 'qi_deficiency', 'yang_deficiency', 'yin_deficiency',
            'phlegm_damp', 'damp_heat', 'blood_stasis', 'qi_depression', 'special'
        }
        if v not in valid_constitutions:
            raise ValueError(f"无效的体质代码: {v}")
        return v


# ============ Batch Request Schema ============

class RecipeBatchRequest(BaseModel):
    """批量获取菜谱请求"""
    ids: List[str] = Field(..., min_length=1, max_length=100, description="菜谱ID列表")

    @field_validator('ids')
    @classmethod
    def validate_ids(cls, v: List[str]) -> List[str]:
        """验证ID列表"""
        if not v:
            raise ValueError("ID列表不能为空")
        if len(v) > 100:
            raise ValueError("一次最多查询100个菜谱")
        return v


# ============ Statistics Schema ============

class RecipeStatistics(BaseModel):
    """菜谱统计信息"""
    total_recipes: int = Field(..., ge=0, description="菜谱总数")
    with_difficulty: int = Field(..., ge=0, description="有难度等级的菜谱数")
    with_constitutions: int = Field(..., ge=0, description="有体质标签的菜谱数")
    with_efficacy_tags: int = Field(..., ge=0, description="有功效标签的菜谱数")
    with_solar_terms: int = Field(..., ge=0, description="有节气标签的菜谱数")

    difficulty_distribution: Dict[str, int] = Field(default_factory=dict, description="难度分布")
    constitution_coverage: Dict[str, int] = Field(default_factory=dict, description="体质覆盖数")
