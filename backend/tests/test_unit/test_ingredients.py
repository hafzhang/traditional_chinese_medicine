"""
食材服务单元测试
Unit Tests for Ingredient Service
"""

import pytest
from api.services.ingredient_service import IngredientService
from api.models import Ingredient


class TestIngredientService:
    """食材服务单元测试"""

    def test_service_import(self):
        """测试服务可以正常导入"""
        from api.services.ingredient_service import IngredientService
        service = IngredientService()
        assert service is not None

    def test_get_ingredient_by_id(self, db_session):
        """测试根据ID获取食材"""
        # 创建测试食材
        ingredient = Ingredient(
            id="test-ingredient-001",
            name="山药",
            aliases=["怀山药", "淮山"],
            category="蔬菜",
            nature="平",
            flavor="甘",
            meridians=["脾", "肺", "肾"],
            suitable_constitutions=["qi_deficiency", "yin_deficiency"],
            avoid_constitutions=["phlegm_damp"],
            efficacy="健脾养胃、补肺益肾",
            image_url="https://example.com/shanyao.jpg"
        )
        db_session.add(ingredient)
        db_session.commit()

        service = IngredientService()
        result = service.get_ingredient_by_id("test-ingredient-001", db_session)

        assert result is not None
        assert result.name == "山药"
        assert result.nature == "平"
        assert "qi_deficiency" in result.suitable_constitutions

    def test_get_ingredient_by_id_not_found(self, db_session):
        """测试获取不存在的食材"""
        service = IngredientService()
        result = service.get_ingredient_by_id("non-existent-id", db_session)
        assert result is None

    def test_get_ingredients_list_basic(self, db_session):
        """测试获取食材列表（基础）"""
        # 创建多个测试食材
        ingredients = [
            Ingredient(
                id=f"list-{i:03d}",
                name=f"食材{i}",
                category="蔬菜",
                nature="平",
                view_count=10 - i
            )
            for i in range(1, 11)
        ]
        db_session.add_all(ingredients)
        db_session.commit()

        service = IngredientService()
        result, total = service.get_ingredients_list(db_session)

        assert total == 10
        assert len(result) == 10
        # 验证按浏览量排序（降序）
        assert result[0].view_count >= result[1].view_count

    def test_get_ingredients_list_with_category_filter(self, db_session):
        """测试按类别筛选食材列表"""
        ingredients = [
            Ingredient(
                id=f"cat-{i:03d}",
                name=f"食材{i}",
                category="蔬菜" if i % 2 == 0 else "水果",
                nature="平"
            )
            for i in range(1, 11)
        ]
        db_session.add_all(ingredients)
        db_session.commit()

        service = IngredientService()
        result, total = service.get_ingredients_list(db_session, category="蔬菜")

        assert all(item.category == "蔬菜" for item in result)
        assert total == 5

    def test_get_ingredients_list_with_nature_filter(self, db_session):
        """测试按性味筛选食材列表"""
        ingredients = [
            Ingredient(
                id=f"nature-{i:03d}",
                name=f"食材{i}",
                category="蔬菜",
                nature="平" if i % 2 == 0 else "温"
            )
            for i in range(1, 11)
        ]
        db_session.add_all(ingredients)
        db_session.commit()

        service = IngredientService()
        result, total = service.get_ingredients_list(db_session, nature="平")

        assert all(item.nature == "平" for item in result)
        assert total == 5

    def test_get_ingredients_list_with_search(self, db_session):
        """测试搜索食材列表（搜索名称和功效）"""
        ingredients = [
            Ingredient(
                id="search-001",
                name="山药",
                aliases=["怀山药", "淮山"],
                category="蔬菜",
                nature="平",
                efficacy="健脾养胃、补肺益肾"
            ),
            Ingredient(
                id="search-002",
                name="红枣",
                aliases=["大枣"],
                category="水果",
                nature="温",
                efficacy="补血安神、养血"
            ),
            Ingredient(
                id="search-003",
                name="莲子",
                aliases=[],
                category="药材",
                nature="平",
                efficacy="养心安神、健脾止泻"
            )
        ]
        db_session.add_all(ingredients)
        db_session.commit()

        service = IngredientService()

        # 搜索名称
        result, total = service.get_ingredients_list(db_session, search="山药")
        assert len(result) >= 1
        assert result[0].name == "山药"

        # 搜索功效关键词 - "健脾"
        result, total = service.get_ingredients_list(db_session, search="健脾")
        assert len(result) >= 1
        assert any("健脾" in item.efficacy for item in result)

        # 搜索功效关键词 - "安神"
        result, total = service.get_ingredients_list(db_session, search="安神")
        assert len(result) >= 1
        assert any("安神" in item.efficacy for item in result)

    def test_get_ingredients_list_with_pagination(self, db_session):
        """测试食材列表分页"""
        ingredients = [
            Ingredient(
                id=f"page-{i:03d}",
                name=f"食材{i}",
                category="蔬菜",
                nature="平"
            )
            for i in range(1, 26)  # 25个
        ]
        db_session.add_all(ingredients)
        db_session.commit()

        service = IngredientService()

        # 第一页
        result, total = service.get_ingredients_list(db_session, skip=0, limit=10)
        assert len(result) == 10
        assert total == 25

        # 第二页
        result, total = service.get_ingredients_list(db_session, skip=10, limit=10)
        assert len(result) == 10

        # 最后一页
        result, total = service.get_ingredients_list(db_session, skip=20, limit=10)
        assert len(result) == 5

    def test_get_ingredients_by_constitution(self, db_session):
        """测试根据体质获取推荐食材"""
        ingredients = [
            Ingredient(
                id=f"constitution-{i:03d}",
                name=f"食材{i}",
                category="蔬菜",
                suitable_constitutions=["qi_deficiency"] if i % 2 == 0 else ["yin_deficiency"]
            )
            for i in range(1, 11)
        ]
        db_session.add_all(ingredients)
        db_session.commit()

        service = IngredientService()
        result = service.get_ingredients_by_constitution("qi_deficiency", db_session)

        assert len(result) == 5
        assert all("qi_deficiency" in item.suitable_constitutions for item in result)

    def test_get_ingredients_by_constitution_invalid_code(self, db_session):
        """测试无效体质代码返回空列表"""
        service = IngredientService()
        result = service.get_ingredients_by_constitution("invalid_code", db_session)
        assert result == []

    def test_get_ingredients_to_avoid(self, db_session):
        """测试根据体质获取禁忌食材"""
        ingredients = [
            Ingredient(
                id="avoid-001",
                name="山楂",
                category="水果",
                avoid_constitutions=["qi_deficiency"]
            ),
            Ingredient(
                id="avoid-002",
                name="萝卜",
                category="蔬菜",
                avoid_constitutions=["qi_deficiency", "yin_deficiency"]
            ),
            Ingredient(
                id="avoid-003",
                name="山药",
                category="蔬菜",
                suitable_constitutions=["qi_deficiency"]
            )
        ]
        db_session.add_all(ingredients)
        db_session.commit()

        service = IngredientService()
        result = service.get_ingredients_to_avoid("qi_deficiency", db_session)

        assert len(result) == 2
        assert all("qi_deficiency" in item.avoid_constitutions for item in result)

    def test_get_ingredients_to_avoid_invalid_code(self, db_session):
        """测试无效体质代码获取禁忌食材返回空列表"""
        service = IngredientService()
        result = service.get_ingredients_to_avoid("invalid_code", db_session)
        assert result == []

    def test_get_recommendation_by_constitution(self, db_session):
        """测试根据体质获取完整推荐信息"""
        ingredients = [
            Ingredient(
                id="rec-001",
                name="山药",
                category="蔬菜",
                nature="平",
                efficacy="健脾养胃、补肺益肾",
                suitable_constitutions=["qi_deficiency"],
                image_url="https://example.com/shanyao.jpg"
            ),
            Ingredient(
                id="avo-001",
                name="山楂",
                category="水果",
                nature="酸",
                efficacy="消食化积",
                avoid_constitutions=["qi_deficiency"]
            )
        ]
        db_session.add_all(ingredients)
        db_session.commit()

        service = IngredientService()
        result = service.get_recommendation_by_constitution("qi_deficiency", db_session)

        assert result["constitution"] == "qi_deficiency"
        assert result["constitution_name"] == "气虚质"
        assert len(result["recommended"]) == 1
        assert len(result["avoided"]) == 1
        assert result["recommended"][0]["name"] == "山药"
        assert result["avoided"][0]["name"] == "山楂"
        assert "reason" in result["recommended"][0]

    def test_search_ingredients_by_symptom(self, db_session):
        """测试根据症状搜索食材"""
        ingredients = [
            Ingredient(
                id="symptom-001",
                name="山药",
                efficacy="健脾养胃、补肺益肾"
            ),
            Ingredient(
                id="symptom-002",
                name="莲子",
                efficacy="养心安神、健脾止泻"
            ),
            Ingredient(
                id="symptom-003",
                name="红枣",
                efficacy="补血安神"
            )
        ]
        db_session.add_all(ingredients)
        db_session.commit()

        service = IngredientService()

        # 搜索健脾相关
        result = service.search_ingredients_by_symptom("健脾", db_session)
        assert len(result) >= 2
        assert any("健脾" in item.efficacy for item in result)

        # 搜索安神相关
        result = service.search_ingredients_by_symptom("安神", db_session)
        assert len(result) >= 1

    def test_increment_view_count(self, db_session):
        """测试增加浏览次数"""
        ingredient = Ingredient(
            id="view-001",
            name="山药",
            category="蔬菜",
            view_count=10
        )
        db_session.add(ingredient)
        db_session.commit()

        service = IngredientService()
        result = service.increment_view_count("view-001", db_session)

        assert result is True
        db_session.refresh(ingredient)
        assert ingredient.view_count == 11

    def test_increment_view_count_not_found(self, db_session):
        """测试增加不存在食材的浏览次数"""
        service = IngredientService()
        result = service.increment_view_count("non-existent-id", db_session)
        assert result is False

    def test_is_valid_constitution_code(self):
        """测试体质代码验证"""
        service = IngredientService()

        # 有效体质代码
        valid_codes = [
            "peace", "qi_deficiency", "yang_deficiency", "yin_deficiency",
            "phlegm_damp", "damp_heat", "blood_stasis", "qi_depression", "special"
        ]

        for code in valid_codes:
            assert service.is_valid_constitution_code(code) is True

        # 无效体质代码
        invalid_codes = ["invalid", "wrong_code", ""]
        for code in invalid_codes:
            assert service.is_valid_constitution_code(code) is False

    def test_get_constitution_name(self):
        """测试获取体质名称"""
        service = IngredientService()

        assert service.get_constitution_name("qi_deficiency") == "气虚质"
        assert service.get_constitution_name("yang_deficiency") == "阳虚质"
        assert service.get_constitution_name("yin_deficiency") == "阴虚质"
        assert service.get_constitution_name("peace") == "平和质"
        # 无效代码返回原始值
        assert service.get_constitution_name("invalid") == "invalid"

    def test_get_recommendation_reason(self, db_session):
        """测试获取推荐理由"""
        service = IngredientService()
        ingredient = Ingredient(
            id="reason-001",
            name="山药",
            category="蔬菜",
            suitable_constitutions=["qi_deficiency"]
        )

        # 测试不同体质的推荐理由
        reason_qi = service._get_recommendation_reason("qi_deficiency", ingredient)
        assert "补气" in reason_qi or "健脾" in reason_qi

        reason_yang = service._get_recommendation_reason("yang_deficiency", ingredient)
        assert "温阳" in reason_yang

    def test_get_avoid_reason(self, db_session):
        """测试获取禁忌理由"""
        service = IngredientService()

        # 寒性食材
        ingredient_cold = Ingredient(
            id="avoid-cold-001",
            name="苦瓜",
            category="蔬菜",
            nature="寒",
            efficacy="清热解毒"
        )
        reason = service._get_avoid_reason("yang_deficiency", ingredient_cold)
        assert "寒" in reason

        # 热性食材
        ingredient_hot = Ingredient(
            id="avoid-hot-001",
            name="生姜",
            category="调料",
            nature="热",
            efficacy="温中散寒"
        )
        reason = service._get_avoid_reason("yin_deficiency", ingredient_hot)
        assert "热" in reason

        # 无功效说明的食材
        ingredient_no_efficy = Ingredient(
            id="avoid-no-001",
            name="测试食材",
            category="其他",
            nature="平"
        )
        reason = service._get_avoid_reason("qi_deficiency", ingredient_no_efficy)
        assert reason == "不建议食用"

    def test_get_ingredients_by_constitution_empty(self, db_session):
        """测试空数据库的体质筛选"""
        service = IngredientService()
        result = service.get_ingredients_by_constitution("qi_deficiency", db_session)
        assert result == []

    def test_get_ingredients_to_avoid_empty(self, db_session):
        """测试空数据库获取禁忌食材"""
        service = IngredientService()
        result = service.get_ingredients_to_avoid("qi_deficiency", db_session)
        assert result == []
