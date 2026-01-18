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
            query = query.filter(
                (Ingredient.name.like(f"%{search}%")) |
                (Ingredient.aliases.like(f"%{search}%"))
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


# 单例模式
_ingredient_service_instance = None


def get_ingredient_service() -> IngredientService:
    """获取食材服务实例"""
    global _ingredient_service_instance
    if _ingredient_service_instance is None:
        _ingredient_service_instance = IngredientService()
    return _ingredient_service_instance
