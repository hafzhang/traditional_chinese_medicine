"""
Recipe Service
食谱服务层 - Phase 1 + Excel Import
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session, joinedload

from api.models import Recipe, RecipeIngredient, RecipeStep, Ingredient


class RecipeService:
    """食谱服务类 (无状态)"""

    # 有效的体质代码
    VALID_CONSTITUTIONS = {
        "peace", "qi_deficiency", "yang_deficiency", "yin_deficiency",
        "phlegm_damp", "damp_heat", "blood_stasis", "qi_depression", "special"
    }

    # 食谱类型
    RECIPE_TYPES = ["粥类", "汤类", "茶饮", "菜肴", "小吃", "主食"]

    # 难度级别
    DIFFICULTY_LEVELS = ["简单", "中等", "困难"]

    def _get_recipe_entity_by_id(self, recipe_id: str, db: Session) -> Optional[Recipe]:
        """
        内部方法：根据ID获取Recipe实体对象

        Args:
            recipe_id: 食谱ID
            db: 数据库会话

        Returns:
            Recipe对象或None
        """
        return db.query(Recipe).filter(
            Recipe.id == recipe_id,
            Recipe.is_deleted == False
        ).first()

    def get_recipe_by_id(self, recipe_id: str, db: Session) -> Optional[Dict[str, Any]]:
        """
        根据ID获取食谱详情 (返回字典格式)

        Args:
            recipe_id: 食谱ID
            db: 数据库会话

        Returns:
            包含ingredients(含nature/taste)、steps、desc、tip的完整字典，不存在返回None
        """
        recipe = db.query(Recipe).options(
            joinedload(Recipe.ingredient_relations).joinedload(RecipeIngredient.ingredient),
            joinedload(Recipe.step_relations)
        ).filter(
            Recipe.id == recipe_id,
            Recipe.is_deleted == False
        ).first()

        if not recipe:
            return None

        # Build ingredients list with nature/taste
        ingredients_data = []
        for rel in recipe.ingredient_relations:
            ingredient_info = {
                "name": rel.ingredient.name if rel.ingredient else rel.amount,
                "amount": rel.amount,
                "is_main": rel.is_main
            }
            if rel.ingredient:
                ingredient_info["nature"] = rel.ingredient.nature
                ingredient_info["taste"] = rel.ingredient.flavor
            ingredients_data.append(ingredient_info)

        # Build steps list
        steps_data = []
        for step in recipe.step_relations:
            steps_data.append({
                "step_number": step.step_number,
                "description": step.description,
                "image_url": step.image_url,
                "duration": step.duration
            })

        return {
            "id": recipe.id,
            "name": recipe.name,
            "type": recipe.type,
            "difficulty": recipe.difficulty,
            "cooking_time": recipe.cooking_time or recipe.cook_time,
            "description": recipe.description,
            "desc": recipe.desc,
            "tip": recipe.tip,
            "cover_image": recipe.cover_image or recipe.image_url,
            "suitable_constitutions": recipe.suitable_constitutions,
            "avoid_constitutions": recipe.avoid_constitutions,
            "efficacy_tags": recipe.efficacy_tags,
            "solar_terms": recipe.solar_terms,
            "ingredients": ingredients_data,
            "steps": steps_data,
            "calories": recipe.calories,
            "protein": recipe.protein,
            "fat": recipe.fat,
            "carbs": recipe.carbs or recipe.carbohydrates,
            "view_count": recipe.view_count,
            "created_at": recipe.created_at.isoformat() if recipe.created_at else None
        }

    def get_recipe_object(self, recipe_id: str, db: Session) -> Optional[Recipe]:
        """
        根据ID获取Recipe对象 (Phase 1 兼容方法)

        Args:
            recipe_id: 食谱ID
            db: 数据库会话

        Returns:
            Recipe对象或None
        """
        return self._get_recipe_entity_by_id(recipe_id, db)

    def get_recipes_list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        type: Optional[str] = None,
        difficulty: Optional[str] = None,
        constitution: Optional[str] = None,
        search: Optional[str] = None
    ) -> tuple[List[Recipe], int]:
        """
        获取食谱列表

        Args:
            db: 数据库会话
            skip: 跳过数量
            limit: 限制数量
            type: 类型筛选
            difficulty: 难度筛选
            constitution: 体质筛选
            search: 搜索关键词

        Returns:
            (食谱列表, 总数)
        """
        query = db.query(Recipe).filter(Recipe.is_deleted == False)

        # 筛选条件
        if type:
            query = query.filter(Recipe.type == type)
        if difficulty:
            query = query.filter(Recipe.difficulty == difficulty)
        if constitution:
            query = query.filter(Recipe.suitable_constitutions.contains(constitution))
        if search:
            query = query.filter(Recipe.name.like(f"%{search}%"))

        # 总数
        total = query.count()

        # 分页
        recipes = query.order_by(Recipe.view_count.desc()).offset(skip).limit(limit).all()

        return recipes, total

    def get_recipes_by_constitution(
        self,
        constitution: str,
        db: Session,
        meal_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Recipe]:
        """
        根据体质获取推荐食谱

        Args:
            constitution: 体质代码
            db: 数据库会话
            meal_type: 餐型 (breakfast, lunch, dinner)
            limit: 限制数量

        Returns:
            推荐食谱列表
        """
        if not self.is_valid_constitution_code(constitution):
            return []

        query = db.query(Recipe).filter(
            Recipe.is_deleted == False,
            Recipe.suitable_constitutions.contains(constitution)
        )

        # 可以根据餐型进一步筛选
        # 这里简单返回所有适合的食谱
        recipes = query.order_by(Recipe.view_count.desc()).limit(limit).all()

        return recipes

    def get_recommendations_by_constitution(
        self,
        constitution: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        根据体质获取三餐推荐食谱

        Args:
            constitution: 体质代码
            db: 数据库会话

        Returns:
            三餐推荐字典
        """
        constitution_name = self.get_constitution_name(constitution)

        # 获取所有适合的食谱
        all_recipes = self.get_recipes_by_constitution(constitution, db, limit=30)

        # 按类型分类
        breakfast = [r for r in all_recipes if r.type in ["粥类", "主食"]][:3]
        lunch = [r for r in all_recipes if r.type in ["菜肴", "汤类"]][:3]
        dinner = [r for r in all_recipes if r.type in ["粥类", "汤类", "菜肴"]][:3]

        return {
            "constitution": constitution,
            "constitution_name": constitution_name,
            "recipes": {
                "breakfast": [
                    {
                        "id": r.id,
                        "name": r.name,
                        "type": r.type,
                        "difficulty": r.difficulty,
                        "cook_time": r.cook_time,
                        "image_url": r.image_url,
                        "reason": f"健脾养胃，适合早餐"
                    }
                    for r in breakfast
                ],
                "lunch": [
                    {
                        "id": r.id,
                        "name": r.name,
                        "type": r.type,
                        "difficulty": r.difficulty,
                        "cook_time": r.cook_time,
                        "image_url": r.image_url,
                        "reason": "补充营养，提供能量"
                    }
                    for r in lunch
                ],
                "dinner": [
                    {
                        "id": r.id,
                        "name": r.name,
                        "type": r.type,
                        "difficulty": r.difficulty,
                        "cook_time": r.cook_time,
                        "image_url": r.image_url,
                        "reason": "清淡易消化，养心安神"
                    }
                    for r in dinner
                ]
            }
        }

    def get_recipes_by_symptom(
        self,
        symptom: str,
        db: Session,
        limit: int = 20
    ) -> List[Recipe]:
        """
        根据症状搜索食谱

        Args:
            symptom: 症状关键词
            db: 数据库会话
            limit: 限制数量

        Returns:
            相关食谱列表
        """
        # 通过症状和功效字段搜索
        recipes = db.query(Recipe).filter(
            Recipe.is_deleted == False,
            Recipe.symptoms.contains(symptom)
        ).order_by(Recipe.view_count.desc()).limit(limit).all()

        return recipes

    def increment_view_count(self, recipe_id: str, db: Session) -> bool:
        """
        增加浏览次数

        Args:
            recipe_id: 食谱ID
            db: 数据库会话

        Returns:
            是否成功
        """
        recipe = self._get_recipe_entity_by_id(recipe_id, db)
        if recipe:
            recipe.view_count = (recipe.view_count or 0) + 1
            db.commit()
            return True
        return False

    def is_valid_constitution_code(self, code: str) -> bool:
        """
        验证体质代码是否有效

        Args:
            code: 体质代码

        Returns:
            是否有效
        """
        return code in self.VALID_CONSTITUTIONS

    def get_constitution_name(self, code: str) -> str:
        """
        获取体质中文名称

        Args:
            code: 体质代码

        Returns:
            体质中文名称
        """
        names = {
            "peace": "平和质",
            "qi_deficiency": "气虚质",
            "yang_deficiency": "阳虚质",
            "yin_deficiency": "阴虚质",
            "phlegm_damp": "痰湿质",
            "damp_heat": "湿热质",
            "blood_stasis": "血瘀质",
            "qi_depression": "气郁质",
            "special": "特禀质"
        }
        return names.get(code, code)


# 单例模式
_recipe_service_instance = None


def get_recipe_service() -> RecipeService:
    """获取食谱服务实例"""
    global _recipe_service_instance
    if _recipe_service_instance is None:
        _recipe_service_instance = RecipeService()
    return _recipe_service_instance
