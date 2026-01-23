"""
Ingredient Service
食材服务层 - Phase 1
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from api.models import Ingredient


class IngredientService:
    """食材服务类"""

    # 有效的体质代码
    VALID_CONSTITUTIONS = {
        "peace", "qi_deficiency", "yang_deficiency", "yin_deficiency",
        "phlegm_damp", "damp_heat", "blood_stasis", "qi_depression", "special"
    }

    def get_ingredient_by_id(self, ingredient_id: str, db: Session) -> Optional[Ingredient]:
        """
        根据ID获取食材详情

        Args:
            ingredient_id: 食材ID
            db: 数据库会话

        Returns:
            食材对象或None
        """
        return db.query(Ingredient).filter(
            Ingredient.id == ingredient_id,
            Ingredient.is_deleted == False
        ).first()

    def get_ingredients_list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        category: Optional[str] = None,
        nature: Optional[str] = None,
        search: Optional[str] = None
    ) -> tuple[List[Ingredient], int]:
        """
        获取食材列表

        Args:
            db: 数据库会话
            skip: 跳过数量
            limit: 限制数量
            category: 类别筛选
            nature: 性味筛选
            search: 搜索关键词

        Returns:
            (食材列表, 总数)
        """
        query = db.query(Ingredient).filter(Ingredient.is_deleted == False)

        # 筛选条件
        if category:
            query = query.filter(Ingredient.category == category)
        if nature:
            query = query.filter(Ingredient.nature == nature)
        if search:
            # 搜索名称和功效（使用 OR 条件）
            query = query.filter(
                (Ingredient.name.like(f"%{search}%")) |
                (Ingredient.efficacy.like(f"%{search}%"))
            )

        # 总数
        total = query.count()

        # 分页
        ingredients = query.order_by(Ingredient.view_count.desc()).offset(skip).limit(limit).all()

        return ingredients, total

    def get_ingredients_by_constitution(
        self,
        constitution: str,
        db: Session,
        limit: int = 20
    ) -> List[Ingredient]:
        """
        根据体质获取推荐食材

        Args:
            constitution: 体质代码
            db: 数据库会话
            limit: 限制数量

        Returns:
            推荐食材列表
        """
        if not self.is_valid_constitution_code(constitution):
            return []

        # 查询适合该体质的食材
        ingredients = db.query(Ingredient).filter(
            Ingredient.is_deleted == False,
            Ingredient.suitable_constitutions.contains(constitution)
        ).order_by(Ingredient.view_count.desc()).limit(limit).all()

        return ingredients

    def get_ingredients_to_avoid(
        self,
        constitution: str,
        db: Session,
        limit: int = 10
    ) -> List[Ingredient]:
        """
        根据体质获取禁忌食材

        Args:
            constitution: 体质代码
            db: 数据库会话
            limit: 限制数量

        Returns:
            禁忌食材列表
        """
        if not self.is_valid_constitution_code(constitution):
            return []

        # 查询该体质禁忌的食材
        ingredients = db.query(Ingredient).filter(
            Ingredient.is_deleted == False,
            Ingredient.avoid_constitutions.contains(constitution)
        ).order_by(Ingredient.view_count.desc()).limit(limit).all()

        return ingredients

    def get_recommendation_by_constitution(
        self,
        constitution: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        根据体质获取推荐和禁忌食材

        Args:
            constitution: 体质代码
            db: 数据库会话

        Returns:
            推荐结果字典
        """
        constitution_name = self.get_constitution_name(constitution)

        recommended = self.get_ingredients_by_constitution(constitution, db)
        avoided = self.get_ingredients_to_avoid(constitution, db)

        return {
            "constitution": constitution,
            "constitution_name": constitution_name,
            "recommended": [
                {
                    "id": ing.id,
                    "name": ing.name,
                    "category": ing.category,
                    "nature": ing.nature,
                    "efficacy": ing.efficacy,
                    "image_url": ing.image_url,
                    "reason": self._get_recommendation_reason(constitution, ing)
                }
                for ing in recommended
            ],
            "avoided": [
                {
                    "id": ing.id,
                    "name": ing.name,
                    "category": ing.category,
                    "reason": self._get_avoid_reason(constitution, ing)
                }
                for ing in avoided
            ]
        }

    def search_ingredients_by_symptom(
        self,
        symptom: str,
        db: Session,
        limit: int = 20
    ) -> List[Ingredient]:
        """
        根据症状搜索食材

        Args:
            symptom: 症状关键词
            db: 数据库会话
            limit: 限制数量

        Returns:
            相关食材列表
        """
        # 通过功效字段搜索
        ingredients = db.query(Ingredient).filter(
            Ingredient.is_deleted == False,
            Ingredient.efficacy.like(f"%{symptom}%")
        ).order_by(Ingredient.view_count.desc()).limit(limit).all()

        return ingredients

    def increment_view_count(self, ingredient_id: str, db: Session) -> bool:
        """
        增加浏览次数

        Args:
            ingredient_id: 食材ID
            db: 数据库会话

        Returns:
            是否成功
        """
        ingredient = self.get_ingredient_by_id(ingredient_id, db)
        if ingredient:
            ingredient.view_count = (ingredient.view_count or 0) + 1
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

    def _get_recommendation_reason(self, constitution: str, ingredient: Ingredient) -> str:
        """获取推荐理由"""
        reason_map = {
            "qi_deficiency": "补气健脾，增强体质",
            "yang_deficiency": "温阳散寒，温暖身体",
            "yin_deficiency": "滋阴润燥，清热生津",
            "phlegm_damp": "健脾化痰，祛湿利水",
            "damp_heat": "清热利湿，泻火解毒",
            "blood_stasis": "活血化瘀，通经止痛",
            "qi_depression": "疏肝理气，解郁安神",
            "special": "益气固表，扶正祛邪",
            "peace": "营养均衡，调和五脏"
        }
        return reason_map.get(constitution, "适合您的体质")

    def _get_avoid_reason(self, constitution: str, ingredient: Ingredient) -> str:
        """获取禁忌理由"""
        if ingredient.efficacy:
            # 如果有功效说明，可以生成更具体的理由
            if "寒" in ingredient.nature or "凉" in ingredient.nature:
                return f"{ingredient.nature}性，可能伤及{self.get_constitution_name(constitution)}"
            elif "热" in ingredient.nature or "温" in ingredient.nature:
                return f"{ingredient.nature}性，可能加重{self.get_constitution_name(constitution)}"
        return "不建议食用"

    def get_ingredients_by_nutrition(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        min_calories: Optional[float] = None,
        max_calories: Optional[float] = None,
        min_protein: Optional[float] = None,
        max_fat: Optional[float] = None,
        high_fiber: bool = False,
        sort_by: Optional[str] = None
    ) -> tuple[List[Ingredient], int]:
        """
        按营养素筛选食材

        Args:
            db: 数据库会话
            skip: 跳过数量
            limit: 限制数量
            min_calories: 最小热量
            max_calories: 最大热量
            min_protein: 最小蛋白质
            max_fat: 最大脂肪
            high_fiber: 高纤维
            sort_by: 排序字段 (calories, protein, fat, fiber)

        Returns:
            (食材列表, 总数)
        """
        query = db.query(Ingredient).filter(Ingredient.is_deleted == False)

        # 热量筛选
        if min_calories is not None:
            query = query.filter(Ingredient.calories >= min_calories)
        if max_calories is not None:
            query = query.filter(Ingredient.calories <= max_calories)

        # 蛋白质筛选
        if min_protein is not None:
            query = query.filter(Ingredient.protein >= min_protein)

        # 脂肪筛选
        if max_fat is not None:
            query = query.filter(Ingredient.fat <= max_fat)

        # 高纤维筛选
        if high_fiber:
            query = query.filter(Ingredient.dietary_fiber >= 5.0)

        # 总数
        total = query.count()

        # 排序
        if sort_by == "calories":
            ingredients = query.order_by(Ingredient.calories.desc()).offset(skip).limit(limit).all()
        elif sort_by == "protein":
            ingredients = query.order_by(Ingredient.protein.desc()).offset(skip).limit(limit).all()
        elif sort_by == "fiber":
            ingredients = query.order_by(Ingredient.dietary_fiber.desc()).offset(skip).limit(limit).all()
        else:
            ingredients = query.order_by(Ingredient.view_count.desc()).offset(skip).limit(limit).all()

        return ingredients, total

    def get_ingredient_nutrition_detail(
        self,
        ingredient_id: str,
        db: Session
    ) -> Optional[Dict[str, Any]]:
        """
        获取食材营养详情

        Args:
            ingredient_id: 食材ID
            db: 数据库会话

        Returns:
            营养详情字典
        """
        ingredient = self.get_ingredient_by_id(ingredient_id, db)
        if not ingredient:
            return None

        return {
            "id": ingredient.id,
            "name": ingredient.name,
            "category": ingredient.category,
            "nature": ingredient.nature,
            "flavor": ingredient.flavor,
            "meridians": ingredient.meridians,

            # 基础营养 (每100g)
            "basic_nutrition": {
                "calories": ingredient.calories,
                "protein": ingredient.protein,
                "fat": ingredient.fat,
                "carbohydrates": ingredient.carbohydrates,
                "dietary_fiber": ingredient.dietary_fiber
            },

            # 维生素
            "vitamins": {
                "vitamin_a": ingredient.vitamin_a,
                "vitamin_b1": ingredient.vitamin_b1,
                "vitamin_b2": ingredient.vitamin_b2,
                "vitamin_c": ingredient.vitamin_c,
                "vitamin_e": ingredient.vitamin_e
            },

            # 矿物质
            "minerals": {
                "calcium": ingredient.calcium,
                "iron": ingredient.iron,
                "zinc": ingredient.zinc,
                "potassium": ingredient.potassium,
                "sodium": ingredient.sodium,
                "iodine": ingredient.iodine,
                "selenium": ingredient.selenium
            },

            # 食用指导
            "consumption_guide": {
                "daily_dosage": ingredient.daily_dosage,
                "best_time": ingredient.best_time,
                "cooking_methods": ingredient.cooking_methods,
                "precautions": ingredient.precautions
            },

            # 搭配信息
            "pairing": {
                "compatible_foods": ingredient.compatible_foods,
                "incompatible_foods": ingredient.incompatible_foods,
                "classic_combinations": ingredient.classic_combinations
            },

            # 储存与安全
            "storage_safety": {
                "storage_method": ingredient.storage_method,
                "storage_temperature": ingredient.storage_temperature,
                "storage_humidity": ingredient.storage_humidity,
                "shelf_life": ingredient.shelf_life,
                "preservation_tips": ingredient.preservation_tips,
                "pesticide_risk": ingredient.pesticide_risk,
                "heavy_metal_risk": ingredient.heavy_metal_risk,
                "microbe_risk": ingredient.microbe_risk,
                "safety_precautions": ingredient.safety_precautions
            },

            # 烹饪详情
            "cooking_details": ingredient.cooking_details,

            # 季节推荐
            "seasonal_info": {
                "best_seasons": ingredient.best_seasons,
                "seasonal_benefits": ingredient.seasonal_benefits
            },

            # 其他
            "image_url": ingredient.image_url,
            "description": ingredient.description,
            "efficacy": ingredient.efficacy
        }

    def get_nutrient_rich_ingredients(
        self,
        nutrient: str,
        db: Session,
        limit: int = 20
    ) -> List[Ingredient]:
        """
        获取富含特定营养素的食材

        Args:
            nutrient: 营养素名称 (protein, fiber, calcium, iron, vitamin_c, etc.)
            db: 数据库会话
            limit: 限制数量

        Returns:
            食材列表
        """
        query = db.query(Ingredient).filter(
            Ingredient.is_deleted == False
        )

        # 根据营养素名称排序
        nutrient_column_map = {
            "protein": Ingredient.protein,
            "fiber": Ingredient.dietary_fiber,
            "calcium": Ingredient.calcium,
            "iron": Ingredient.iron,
            "zinc": Ingredient.zinc,
            "potassium": Ingredient.potassium,
            "vitamin_a": Ingredient.vitamin_a,
            "vitamin_c": Ingredient.vitamin_c,
            "vitamin_e": Ingredient.vitamin_e,
            "calories": Ingredient.calories
        }

        column = nutrient_column_map.get(nutrient)
        if column:
            # 筛选该营养素大于0的食材
            query = query.filter(column > 0)
            ingredients = query.order_by(column.desc()).limit(limit).all()
        else:
            # 默认按浏览量排序
            ingredients = query.order_by(Ingredient.view_count.desc()).limit(limit).all()

        return ingredients


# 单例模式
_ingredient_service_instance = None


def get_ingredient_service() -> IngredientService:
    """获取食材服务实例"""
    global _ingredient_service_instance
    if _ingredient_service_instance is None:
        _ingredient_service_instance = IngredientService()
    return _ingredient_service_instance
