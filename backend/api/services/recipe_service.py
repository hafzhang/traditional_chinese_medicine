"""
Recipe Service
食谱服务层 - Phase 1
"""

import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

from api.models import Recipe, RecipeIngredient, RecipeStep
from sqlalchemy.orm import joinedload

# 配置日志
logger = logging.getLogger(__name__)


class RecipeService:
    """食谱服务类 - 无状态服务"""

    # 有效的体质代码
    VALID_CONSTITUTIONS = {
        "peace", "qi_deficiency", "yang_deficiency", "yin_deficiency",
        "phlegm_damp", "damp_heat", "blood_stasis", "qi_depression", "special"
    }

    # 难度级别
    DIFFICULTY_LEVELS = ["easy", "medium", "harder", "hard"]

    # 四季到节气映射 (使用中文名)
    SEASON_TO_SOLAR_TERMS = {
        'spring': ['立春', '雨水', '惊蛰', '春分', '清明', '谷雨'],
        'summer': ['立夏', '小满', '芒种', '夏至', '小暑', '大暑', '长夏'],
        'autumn': ['立秋', '处暑', '白露', '秋分', '寒露', '霜降'],
        'winter': ['立冬', '小雪', '大雪', '冬至', '小寒', '大寒'],
    }

    def get_recipe_by_id(self, recipe_id: str, db: Session) -> Optional[Recipe]:
        """
        根据ID获取食谱详情

        Args:
            recipe_id: 食谱ID
            db: 数据库会话

        Returns:
            食谱对象或None
        """
        logger.info(f"Fetching recipe with id: {recipe_id}")
        try:
            # ingredients 和 steps 是 JSON 列，会自动加载，不需要 joinedload
            result = db.query(Recipe).filter(Recipe.id == recipe_id).first()
            logger.debug(f"Found recipe: {result.name if result else 'None'}")
            return result
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching recipe {recipe_id}: {e}")
            raise

    def get_recipe_detail_with_ingredients_steps(self, recipe_id: str, db: Session) -> Optional[Dict[str, Any]]:
        """
        根据ID获取食谱详情（包含食材和步骤）

        Args:
            recipe_id: 食谱ID
            db: 数据库会话

        Returns:
            包含食谱详情、食材和步骤的字典，如果找不到返回None
        """
        logger.info(f"Fetching recipe detail with ingredients and steps for id: {recipe_id}")
        try:
            # 获取食谱基本信息
            recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

            if not recipe:
                logger.warning(f"Recipe not found: {recipe_id}")
                return None

            # 获取食材
            ingredients = db.query(RecipeIngredient).filter(
                RecipeIngredient.recipe_id == recipe_id
            ).order_by(RecipeIngredient.display_order).all()

            # 获取步骤
            steps = db.query(RecipeStep).filter(
                RecipeStep.recipe_id == recipe_id
            ).order_by(RecipeStep.step_number).all()

            # 格式化食材
            ingredients_list = []
            for ing in ingredients:
                ingredients_list.append({
                    "name": ing.ingredient_name,
                    "amount": ing.amount,
                    "is_main": ing.is_main,
                    "display_order": ing.display_order
                })

            # 格式化步骤
            steps_list = []
            for step in steps:
                steps_list.append({
                    "step_number": step.step_number,
                    "description": step.description,
                    "duration": step.duration
                })

            return {
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
                "ingredients": ingredients_list,
                "steps": steps_list,
                "view_count": recipe.view_count
            }
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching recipe detail {recipe_id}: {e}")
            raise

    def get_recipes(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 20,
        constitution: Optional[str] = None,
        efficacy: Optional[str] = None,
        difficulty: Optional[str] = None,
        solar_term: Optional[str] = None,
        season: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取食谱列表（支持多种筛选条件）

        Args:
            db: 数据库会话
            page: 页码（从1开始）
            page_size: 每页数量
            constitution: 体质筛选
            efficacy: 功效标签筛选
            difficulty: 难度筛选
            solar_term: 节气筛选
            season: 季节筛选

        Returns:
            {total, page, page_size, items}
        """
        logger.info(f"Fetching recipes with params: page={page}, page_size={page_size}, constitution={constitution}, efficacy={efficacy}, difficulty={difficulty}, solar_term={solar_term}, season={season}")
        try:
            # 验证体质代码
            if constitution and not self.is_valid_constitution_code(constitution):
                raise ValueError(f"Invalid constitution code: {constitution}")

            # 构建查询
            query = db.query(Recipe)

            # 应用筛选条件
            if constitution:
                query = query.filter(Recipe.suitable_constitutions.contains(constitution))

            if efficacy:
                query = query.filter(Recipe.efficacy_tags.contains(efficacy))

            if difficulty:
                if difficulty not in self.DIFFICULTY_LEVELS:
                    raise ValueError(f"Invalid difficulty level: {difficulty}")
                query = query.filter(Recipe.difficulty == difficulty)

            if solar_term:
                query = query.filter(Recipe.solar_terms.contains(solar_term))

            if season:
                solar_terms = self.SEASON_TO_SOLAR_TERMS.get(season, [])
                if solar_terms:
                    # 匹配季节中的任一节气 (SQLite JSON 不支持 overlap，使用 any)
                    conditions = [Recipe.solar_terms.contains(st) for st in solar_terms]
                    query = query.filter(or_(*conditions))

            # 计算总数
            total = query.count()

            # 分页
            offset = (page - 1) * page_size
            items = query.offset(offset).limit(page_size).all()

            logger.debug(f"Found {len(items)} recipes (total: {total})")
            return {
                "total": total,
                "page": page,
                "page_size": page_size,
                "items": items
            }
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching recipes: {e}")
            raise

    def get_recipes_by_constitution(
        self,
        constitution: str,
        db: Session,
        limit: int = 10
    ) -> List[Recipe]:
        """
        根据体质获取推荐食谱

        Args:
            constitution: 体质代码
            db: 数据库会话
            limit: 限制数量

        Returns:
            推荐食谱列表
        """
        logger.info(f"Fetching recipes for constitution: {constitution} (limit: {limit})")
        if not self.is_valid_constitution_code(constitution):
            raise ValueError(f"Invalid constitution code: {constitution}")

        recipes = db.query(Recipe).filter(
            Recipe.suitable_constitutions.contains(constitution)
        ).order_by(Recipe.view_count.desc()).limit(limit).all()
        logger.debug(f"Found {len(recipes)} recipes for constitution: {constitution}")
        return recipes

    def get_recommendations_by_constitution(
        self,
        constitution: str,
        limit: int,
        db: Session
    ) -> List[Recipe]:
        """
        根据体质获取推荐食谱

        Args:
            constitution: 体质代码
            limit: 限制数量
            db: 数据库会话

        Returns:
            推荐食谱列表，优先返回适合该体质，排除禁忌体质
        """
        logger.info(f"Fetching recommendations for constitution: {constitution} (limit: {limit})")
        if not self.is_valid_constitution_code(constitution):
            raise ValueError(f"Invalid constitution code: {constitution}")

        # 查询适合该体质的食谱，排除禁忌该体质的
        recipes = db.query(Recipe).filter(
            Recipe.suitable_constitutions.contains(constitution),
            ~Recipe.avoid_constitutions.contains(constitution)
        ).order_by(Recipe.view_count.desc()).limit(limit).all()
        logger.debug(f"Found {len(recipes)} recommendations for constitution: {constitution}")
        return recipes

    def search_recipes(
        self,
        keyword: str,
        db: Session,
        page: int = 1,
        page_size: int = 20,
        constitution: Optional[str] = None,
        difficulty: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        搜索食谱

        搜索范围: name, efficacy_tags

        Args:
            keyword: 搜索关键词
            db: 数据库会话
            page: 页码（从1开始）
            page_size: 每页数量
            constitution: 体质筛选
            difficulty: 难度筛选

        Returns:
            {total, page, page_size, items}
        """
        logger.info(f"Searching recipes with keyword: {keyword}, filters: constitution={constitution}, difficulty={difficulty}, page={page}, page_size={page_size}")
        # 验证体质代码
        if constitution and not self.is_valid_constitution_code(constitution):
            raise ValueError(f"Invalid constitution code: {constitution}")

        # 验证难度级别
        if difficulty and difficulty not in self.DIFFICULTY_LEVELS:
            raise ValueError(f"Invalid difficulty level: {difficulty}")

        # 构建查询 - 搜索名称和功效标签
        query = db.query(Recipe).filter(
            or_(
                Recipe.name.contains(keyword),
                Recipe.efficacy_tags.contains(keyword)
            )
        )

        # 应用筛选条件
        if constitution:
            query = query.filter(Recipe.suitable_constitutions.contains(constitution))

        if difficulty:
            query = query.filter(Recipe.difficulty == difficulty)

        # 计算总数
        total = query.count()

        # 分页
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        logger.debug(f"Found {len(items)} recipes matching '{keyword}' (total: {total})")
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items
        }

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


def get_recipe_service() -> RecipeService:
    """
    获取食谱服务实例

    Returns:
        RecipeService 实例
    """
    return RecipeService()
