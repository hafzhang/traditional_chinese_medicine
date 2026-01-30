"""
食谱服务单元测试
Unit Tests for Recipe Service
"""

import pytest
from api.services.recipe_service import RecipeService
from api.models import Recipe


class TestRecipeService:
    """食谱服务单元测试"""

    def test_get_recipe_by_id(self, db_session):
        """测试根据ID获取食谱 (返回字典格式)"""
        recipe = Recipe(
            id="test-recipe-001",
            name="山药莲子粥",
            type="粥类",
            difficulty="简单",
            cook_time=30,
            servings=2,
            suitable_constitutions=["qi_deficiency"],
            ingredients={"main": [{"name": "山药", "amount": "100g"}]},
            steps=["步骤1", "步骤2"]
        )
        db_session.add(recipe)
        db_session.commit()

        service = RecipeService()
        result = service.get_recipe_by_id("test-recipe-001", db_session)

        # get_recipe_by_id 现在返回字典
        assert result is not None
        assert result["name"] == "山药莲子粥"
        assert result["type"] == "粥类"
        assert result["difficulty"] == "简单"

    def test_get_recipes_by_constitution(self, db_session):
        """测试根据体质获取食谱"""
        recipes = [
            Recipe(
                id=f"recipe-{i:03d}",
                name=f"食谱{i}",
                type="粥类",
                suitable_constitutions=["qi_deficiency"] if i % 2 == 0 else ["yin_deficiency"]
            )
            for i in range(1, 11)
        ]
        db_session.add_all(recipes)
        db_session.commit()

        service = RecipeService()
        result = service.get_recipes_by_constitution("qi_deficiency", db_session)

        assert len(result) == 5
        assert all("qi_deficiency" in item.suitable_constitutions for item in result)

    def test_search_recipes(self, db_session):
        """测试搜索食谱"""
        recipe = Recipe(
            id="search-001",
            name="山药粥",
            type="粥类",
            suitable_constitutions=["qi_deficiency"]
        )
        db_session.add(recipe)
        db_session.commit()

        service = RecipeService()
        recipes, total = service.get_recipes_list(db_session, search="山药")

        assert total > 0
        assert any("山药" in r.name for r in recipes)

    def test_increment_view_count(self, db_session):
        """测试增加浏览次数"""
        recipe = Recipe(
            id="view-001",
            name="测试食谱",
            type="粥类",
            view_count=10
        )
        db_session.add(recipe)
        db_session.commit()

        service = RecipeService()
        service.increment_view_count("view-001", db_session)

        db_session.refresh(recipe)
        assert recipe.view_count == 11

    def test_get_recipes_by_type(self, db_session):
        """测试按类型获取食谱"""
        recipes = [
            Recipe(
                id=f"type-{i:03d}",
                name=f"食谱{i}",
                type="粥类" if i % 2 == 0 else "汤类"
            )
            for i in range(1, 11)
        ]
        db_session.add_all(recipes)
        db_session.commit()

        service = RecipeService()
        result, total = service.get_recipes_list(db_session, type="粥类")

        assert all(item.type == "粥类" for item in result)

    def test_get_recipes_by_difficulty(self, db_session):
        """测试按难度获取食谱"""
        recipes = [
            Recipe(
                id=f"diff-{i:03d}",
                name=f"食谱{i}",
                difficulty="简单" if i % 3 == 0 else "中等" if i % 3 == 1 else "复杂"
            )
            for i in range(1, 10)
        ]
        db_session.add_all(recipes)
        db_session.commit()

        service = RecipeService()
        result, total = service.get_recipes_list(db_session, difficulty="简单")

        assert all(item.difficulty == "简单" for item in result)

    def test_recipe_not_found(self, db_session):
        """测试食谱不存在"""
        service = RecipeService()
        result = service.get_recipe_by_id("non-existent-id", db_session)

        assert result is None

    def test_get_recipes_list_pagination(self, db_session):
        """测试分页功能"""
        recipes = [
            Recipe(
                id=f"page-{i:03d}",
                name=f"食谱{i}",
                type="粥类"
            )
            for i in range(1, 31)
        ]
        db_session.add_all(recipes)
        db_session.commit()

        service = RecipeService()
        recipes_page1, total = service.get_recipes_list(db_session, skip=0, limit=10)
        recipes_page2, _ = service.get_recipes_list(db_session, skip=10, limit=10)

        assert total == 30
        assert len(recipes_page1) == 10
        assert len(recipes_page2) == 10

    def test_is_valid_constitution_code(self, db_session):
        """测试体质代码验证"""
        service = RecipeService()

        valid_codes = ["peace", "qi_deficiency", "yang_deficiency", "yin_deficiency"]

        for code in valid_codes:
            assert service.is_valid_constitution_code(code) is True

        invalid_codes = ["invalid", "wrong", ""]
        for code in invalid_codes:
            assert service.is_valid_constitution_code(code) is False

    def test_increment_view_count_nonexistent(self, db_session):
        """测试增加不存在食谱的浏览次数（不应报错）"""
        service = RecipeService()
        # 应该不报错，只是没有效果
        service.increment_view_count("non-existent-id", db_session)
