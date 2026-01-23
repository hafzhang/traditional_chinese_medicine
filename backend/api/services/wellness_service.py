"""
Wellness Service
养生服务层 - 季节推荐与食材搭配
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from api.models import Ingredient, Recipe


class WellnessService:
    """养生服务类 - 季节养生与食材搭配"""

    # 季节列表
    SEASONS = ["春", "夏", "秋", "冬"]

    # 季节养生原则
    SEASONAL_PRINCIPLES = {
        "春": {
            "name": "春季",
            "principle": "春季养阳，宜升发疏泄",
            "diet_principles": [
                "宜辛温发散，以助阳气升发",
                "宜食清淡，忌油腻生冷",
                "多食绿色蔬菜，以应春生之气"
            ],
            "recommended_foods": ["韭菜", "葱", "蒜", "芥菜", "菠菜", "芹菜", "春笋"],
            "avoid_foods": ["酸冷食物", "油腻食物"],
            "suitable_constitutions": ["平和质", "气虚质", "阳虚质"],
            "care_constitutions": ["阴虚质", "湿热质"]
        },
        "夏": {
            "name": "夏季",
            "principle": "夏季养长，宜清热祛暑",
            "diet_principles": [
                "宜清淡爽口，忌辛辣油腻",
                "宜食苦味以清心火",
                "多食清凉解暑之品"
            ],
            "recommended_foods": ["绿豆", "西瓜", "黄瓜", "苦瓜", "冬瓜", "丝瓜", "西红柿"],
            "avoid_foods": ["温热食物", "油腻食物", "羊肉"],
            "suitable_constitutions": ["平和质", "湿热质", "阴虚质"],
            "care_constitutions": ["阳虚质", "脾胃虚寒"]
        },
        "秋": {
            "name": "秋季",
            "principle": "秋季养收，宜滋阴润燥",
            "diet_principles": [
                "宜滋阴润肺，少食辛辣",
                "宜食酸甘化阴",
                "多食润燥生津之品"
            ],
            "recommended_foods": ["梨", "银耳", "百合", "莲子", "山药", "萝卜", "蜂蜜"],
            "avoid_foods": ["辛辣食物", "干燥食物"],
            "suitable_constitutions": ["平和质", "阴虚质", "燥热体质"],
            "care_constitutions": ["痰湿质", "湿热质"]
        },
        "冬": {
            "name": "冬季",
            "principle": "冬季养藏，宜温补肾阳",
            "diet_principles": [
                "宜温补，忌生冷",
                "早食温热，晚食少",
                "多食补肾填精之品"
            ],
            "recommended_foods": ["羊肉", "牛肉", "核桃", "栗子", "山药", "红枣", "桂圆"],
            "avoid_foods": ["生冷食物", "寒凉食物"],
            "suitable_constitutions": ["平和质", "阳虚质", "气虚质"],
            "care_constitutions": ["阴虚质", "湿热质"]
        }
    }

    def get_seasonal_principles(self, season: str) -> Optional[Dict[str, Any]]:
        """
        获取季节养生原则

        Args:
            season: 季节 (春/夏/秋/冬)

        Returns:
            季节养生原则字典
        """
        return self.SEASONAL_PRINCIPLES.get(season)

    def get_seasonal_ingredients(
        self,
        season: str,
        db: Session,
        limit: int = 20
    ) -> List[Ingredient]:
        """
        获取季节推荐食材

        Args:
            season: 季节 (春/夏/秋/冬)
            db: 数据库会话
            limit: 限制数量

        Returns:
            推荐食材列表
        """
        if season not in self.SEASONS:
            return []

        # 查询适合该季节的食材
        query = db.query(Ingredient).filter(
            Ingredient.is_deleted == False
        )

        # 通过 JSON contains 查询
        query = query.filter(
            Ingredient.best_seasons.contains(season)
        )

        ingredients = query.order_by(Ingredient.view_count.desc()).limit(limit).all()

        # 如果没有结果，返回该季节推荐的食物类别
        if not ingredients:
            season_info = self.SEASONAL_PRINCIPLES.get(season, {})
            recommended_names = season_info.get("recommended_foods", [])
            if recommended_names:
                # 通过名称搜索
                ingredients = db.query(Ingredient).filter(
                    Ingredient.is_deleted == False,
                    Ingredient.name.in_(recommended_names)
                ).all()

        return ingredients

    def get_seasonal_recipes(
        self,
        season: str,
        db: Session,
        constitution: Optional[str] = None,
        limit: int = 10
    ) -> List[Recipe]:
        """
        获取季节推荐食谱

        Args:
            season: 季节 (春/夏/秋/冬)
            db: 数据库会话
            constitution: 体质代码 (可选)
            limit: 限制数量

        Returns:
            推荐食谱列表
        """
        if season not in self.SEASONS:
            return []

        query = db.query(Recipe).filter(
            Recipe.is_deleted == False
        )

        # 筛选适合该季节的食谱
        query = query.filter(
            Recipe.suitable_seasons.contains(season)
        )

        # 如果指定了体质，进一步筛选
        if constitution:
            query = query.filter(
                Recipe.suitable_constitutions.contains(constitution)
            )

        recipes = query.order_by(Recipe.view_count.desc()).limit(limit).all()

        return recipes

    def get_seasonal_wellness_plan(
        self,
        season: str,
        constitution: Optional[str] = None,
        db: Session = None
    ) -> Dict[str, Any]:
        """
        获取季节养生方案

        Args:
            season: 季节 (春/夏/秋/冬)
            constitution: 体质代码 (可选)
            db: 数据库会话 (可选)

        Returns:
            养生方案字典
        """
        season_info = self.SEASONAL_PRINCIPLES.get(season)
        if not season_info:
            return {}

        plan = {
            "season": season,
            "season_name": season_info["name"],
            "principle": season_info["principle"],
            "diet_principles": season_info["diet_principles"],
            "recommended_foods": season_info["recommended_foods"],
            "avoid_foods": season_info["avoid_foods"],
            "suitable_constitutions": season_info["suitable_constitutions"],
            "care_constitutions": season_info["care_constitutions"]
        }

        # 如果提供了数据库会话，添加推荐的食材和食谱
        if db:
            ingredients = self.get_seasonal_ingredients(season, db, limit=10)
            recipes = self.get_seasonal_recipes(season, db, constitution, limit=5)

            plan["ingredients"] = [
                {
                    "id": ing.id,
                    "name": ing.name,
                    "category": ing.category,
                    "nature": ing.nature,
                    "efficacy": ing.efficacy,
                    "image_url": ing.image_url
                }
                for ing in ingredients
            ]

            plan["recipes"] = [
                {
                    "id": recipe.id,
                    "name": recipe.name,
                    "type": recipe.type,
                    "difficulty": recipe.difficulty,
                    "efficacy": recipe.efficacy,
                    "image_url": recipe.image_url
                }
                for recipe in recipes
            ]

        return plan

    def check_food_pairing(
        self,
        food1_name: str,
        food2_name: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        检查两食材的搭配相容性

        Args:
            food1_name: 食材1名称
            food2_name: 食材2名称
            db: 数据库会话

        Returns:
            搭配检查结果
        """
        # 查询两个食材
        food1 = db.query(Ingredient).filter(
            Ingredient.is_deleted == False,
            Ingredient.name == food1_name
        ).first()

        food2 = db.query(Ingredient).filter(
            Ingredient.is_deleted == False,
            Ingredient.name == food2_name
        ).first()

        if not food1 or not food2:
            return {
                "compatible": None,
                "reason": "食材信息不完整",
                "food1_found": food1 is not None,
                "food2_found": food2 is not None
            }

        # 检查是否在忌配列表中
        food1_incompatible = food1.incompatible_foods or []
        food2_incompatible = food2.incompatible_foods or []

        # 检查是否相克
        is_incompatible = False
        incompatible_reason = None

        # 检查 food1 的忌配列表
        for item in food1_incompatible:
            if isinstance(item, dict):
                item_name = item.get("name", "")
                if item_name in [food2_name, food2.name]:
                    is_incompatible = True
                    incompatible_reason = item.get("reason", "")
                    break
            elif isinstance(item, str):
                if item in [food2_name, food2.name]:
                    is_incompatible = True
                    incompatible_reason = f"{food1_name}与{food2_name}不宜同食"
                    break

        # 检查 food2 的忌配列表
        if not is_incompatible:
            for item in food2_incompatible:
                if isinstance(item, dict):
                    item_name = item.get("name", "")
                    if item_name in [food1_name, food1.name]:
                        is_incompatible = True
                        incompatible_reason = item.get("reason", "")
                        break
                elif isinstance(item, str):
                    if item in [food1_name, food1.name]:
                        is_incompatible = True
                        incompatible_reason = f"{food1_name}与{food2_name}不宜同食"
                        break

        # 检查是否在宜配列表中
        food1_compatible = food1.compatible_foods or []
        food2_compatible = food2.compatible_foods or []

        is_compatible = False
        compatible_reason = None
        compatible_benefit = None

        for item in food1_compatible:
            if isinstance(item, dict):
                item_name = item.get("name", "")
                if item_name in [food2_name, food2.name]:
                    is_compatible = True
                    compatible_reason = item.get("reason", "")
                    compatible_benefit = item.get("benefit", "")
                    break
            elif isinstance(item, str):
                if item in [food2_name, food2.name]:
                    is_compatible = True
                    compatible_reason = f"{food1_name}与{food2_name}宜搭配食用"
                    break

        if not is_compatible:
            for item in food2_compatible:
                if isinstance(item, dict):
                    item_name = item.get("name", "")
                    if item_name in [food1_name, food1.name]:
                        is_compatible = True
                        compatible_reason = item.get("reason", "")
                        compatible_benefit = item.get("benefit", "")
                        break
                elif isinstance(item, str):
                    if item in [food1_name, food1.name]:
                        is_compatible = True
                        compatible_reason = f"{food1_name}与{food2_name}宜搭配食用"
                        break

        # 体质兼容性检查
        constitution_conflict = False
        food1_suitable = set(food1.suitable_constitutions or [])
        food1_avoid = set(food1.avoid_constitutions or [])
        food2_suitable = set(food2.suitable_constitutions or [])
        food2_avoid = set(food2.avoid_constitutions or [])

        # 如果一个食材的适用体质是另一个食材的禁忌体质
        if food1_suitable & food2_avoid:
            constitution_conflict = True
        if food2_suitable & food1_avoid:
            constitution_conflict = True

        return {
            "food1": {
                "name": food1.name,
                "nature": food1.nature,
                "category": food1.category
            },
            "food2": {
                "name": food2.name,
                "nature": food2.nature,
                "category": food2.category
            },
            "compatible": is_compatible,
            "incompatible": is_incompatible,
            "compatible_reason": compatible_reason,
            "compatible_benefit": compatible_benefit,
            "incompatible_reason": incompatible_reason,
            "constitution_conflict": constitution_conflict,
            "recommendation": self._get_pairing_recommendation(
                is_compatible, is_incompatible, constitution_conflict
            )
        }

    def _get_pairing_recommendation(
        self,
        is_compatible: bool,
        is_incompatible: bool,
        constitution_conflict: bool
    ) -> str:
        """获取搭配推荐"""
        if is_incompatible:
            return "不建议搭配"
        if constitution_conflict:
            return "谨慎搭配，注意体质"
        if is_compatible:
            return "推荐搭配"
        return "可以搭配"

    def get_ingredient_pairing_suggestions(
        self,
        ingredient_id: str,
        db: Session,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        获取食材搭配建议

        Args:
            ingredient_id: 食材ID
            db: 数据库会话
            limit: 限制数量

        Returns:
            搭配建议字典
        """
        ingredient = db.query(Ingredient).filter(
            Ingredient.id == ingredient_id,
            Ingredient.is_deleted == False
        ).first()

        if not ingredient:
            return {}

        result = {
            "ingredient": {
                "id": ingredient.id,
                "name": ingredient.name,
                "nature": ingredient.nature,
                "category": ingredient.category
            },
            "compatible_foods": [],
            "incompatible_foods": [],
            "classic_combinations": []
        }

        # 宜配食材
        compatible = ingredient.compatible_foods or []
        for item in compatible[:limit]:
            if isinstance(item, dict):
                # 查询食材详情
                related_ingredient = db.query(Ingredient).filter(
                    Ingredient.name == item.get("name"),
                    Ingredient.is_deleted == False
                ).first()
                if related_ingredient:
                    result["compatible_foods"].append({
                        "id": related_ingredient.id,
                        "name": related_ingredient.name,
                        "reason": item.get("reason", ""),
                        "benefit": item.get("benefit", ""),
                        "image_url": related_ingredient.image_url
                    })

        # 忌配食材
        incompatible = ingredient.incompatible_foods or []
        for item in incompatible[:limit]:
            if isinstance(item, dict):
                result["incompatible_foods"].append({
                    "name": item.get("name", ""),
                    "reason": item.get("reason", ""),
                    "effect": item.get("effect", "")
                })
            elif isinstance(item, str):
                result["incompatible_foods"].append({
                    "name": item,
                    "reason": "不宜同食",
                    "effect": ""
                })

        # 经典搭配
        combinations = ingredient.classic_combinations or []
        for combo in combinations[:limit]:
            if isinstance(combo, dict):
                result["classic_combinations"].append({
                    "name": combo.get("name", ""),
                    "benefit": combo.get("benefit", ""),
                    "target": combo.get("target", "")
                })

        return result


# 单例模式
_wellness_service_instance = None


def get_wellness_service() -> WellnessService:
    """获取养生服务实例"""
    global _wellness_service_instance
    if _wellness_service_instance is None:
        _wellness_service_instance = WellnessService()
    return _wellness_service_instance
