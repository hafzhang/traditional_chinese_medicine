"""
Recipe Schema Unit Tests
菜谱 Schema 单元测试
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from api.schemas.recipe import (
    RecipeBase,
    RecipeCreate,
    RecipeUpdate,
    RecipeResponse,
    RecipeListItem,
    RecipeListResponse,
    RecipeIngredientItem,
    RecipeStepItem,
    RecipeImportBase,
    RecipeSearchRequest,
    RecipeRecommendationRequest,
    RecipeBatchRequest,
    RecipeStatistics,
)


class TestRecipeBase:
    """测试 RecipeBase Schema"""

    def test_valid_recipe_base(self):
        """测试有效的菜谱基础数据"""
        data = {
            "name": "山药莲子粥",
            "desc": "健脾养胃的养生粥",
            "tip": "山药要新鲜",
            "cooking_time": 60,
            "difficulty": "easy",
            "suitable_constitutions": ["qi_deficiency", "peace"],
            "avoid_constitutions": ["phlegm_damp"],
            "efficacy_tags": ["健脾养胃", "补气"],
            "solar_terms": ["立春", "雨水"]
        }
        schema = RecipeBase(**data)

        assert schema.name == "山药莲子粥"
        assert schema.desc == "健脾养胃的养生粥"
        assert schema.cooking_time == 60
        assert schema.difficulty == "easy"
        assert "qi_deficiency" in schema.suitable_constitutions

    def test_minimal_recipe_base(self):
        """测试最小化菜谱数据（仅必需字段）"""
        schema = RecipeBase(name="测试菜谱")
        assert schema.name == "测试菜谱"
        assert schema.desc is None
        assert schema.suitable_constitutions == []

    def test_invalid_difficulty(self):
        """测试无效的难度等级"""
        with pytest.raises(ValidationError) as exc_info:
            RecipeBase(name="测试", difficulty="invalid")
        assert "difficulty" in str(exc_info.value).lower()

    def test_valid_difficulties(self):
        """测试所有有效的难度等级"""
        valid_difficulties = ["easy", "medium", "harder", "hard"]
        for diff in valid_difficulties:
            schema = RecipeBase(name="测试", difficulty=diff)
            assert schema.difficulty == diff

    def test_invalid_constitution(self):
        """测试无效的体质代码"""
        with pytest.raises(ValidationError) as exc_info:
            RecipeBase(name="测试", suitable_constitutions=["invalid_code"])
        assert "constitution" in str(exc_info.value).lower()

    def test_valid_constitutions(self):
        """测试所有有效的体质代码"""
        valid_constitutions = [
            "peace", "qi_deficiency", "yang_deficiency", "yin_deficiency",
            "phlegm_damp", "damp_heat", "blood_stasis", "qi_depression", "special"
        ]
        schema = RecipeBase(name="测试", suitable_constitutions=valid_constitutions)
        assert len(schema.suitable_constitutions) == 9

    def test_name_validation(self):
        """测试名称验证"""
        # 名称太短
        with pytest.raises(ValidationError):
            RecipeBase(name="")

        # 名称太长
        with pytest.raises(ValidationError):
            RecipeBase(name="a" * 101)

    def test_cooking_time_validation(self):
        """测试烹饪时间验证"""
        # 负数时间
        with pytest.raises(ValidationError):
            RecipeBase(name="测试", cooking_time=-10)

        # 零时间（应该有效）
        schema = RecipeBase(name="测试", cooking_time=0)
        assert schema.cooking_time == 0


class TestRecipeCreate:
    """测试 RecipeCreate Schema"""

    def test_recipe_create_with_ingredients_and_steps(self):
        """测试包含食材和步骤的创建数据"""
        data = {
            "name": "测试菜谱",
            "desc": "测试描述",
            "cooking_time": 30,
            "difficulty": "medium",
            "ingredients": [
                {"ingredient_name": "山药", "amount": "100g", "is_main": True},
                {"ingredient_name": "红枣", "amount": "5个", "is_main": False}
            ],
            "steps": [
                "将山药去皮切块",
                "将红枣洗净去核",
                "将食材放入锅中煮30分钟"
            ]
        }
        schema = RecipeCreate(**data)

        assert schema.name == "测试菜谱"
        assert len(schema.ingredients) == 2
        assert len(schema.steps) == 3


class TestRecipeUpdate:
    """测试 RecipeUpdate Schema"""

    def test_recipe_update_partial(self):
        """测试部分更新"""
        schema = RecipeUpdate(name="新名称")
        assert schema.name == "新名称"
        assert schema.difficulty is None

    def test_recipe_update_all_fields(self):
        """测试更新所有字段"""
        data = {
            "name": "更新名称",
            "desc": "更新描述",
            "cooking_time": 45,
            "difficulty": "harder",
            "suitable_constitutions": ["yin_deficiency"]
        }
        schema = RecipeUpdate(**data)
        assert schema.name == "更新名称"
        assert schema.difficulty == "harder"

    def test_recipe_update_empty(self):
        """测试空更新"""
        schema = RecipeUpdate()
        assert schema.name is None
        assert schema.difficulty is None


class RecipeIngredientItem:
    """测试 RecipeIngredientItem Schema"""

    def test_recipe_ingredient_item(self):
        """测试食材项"""
        data = {
            "id": "ing-001",
            "ingredient_id": "ingredient-123",
            "ingredient_name": "山药",
            "amount": "100g",
            "is_main": True,
            "display_order": 1
        }
        schema = RecipeIngredientItem(**data)

        assert schema.ingredient_name == "山药"
        assert schema.is_main is True
        assert schema.display_order == 1


class RecipeStepItem:
    """测试 RecipeStepItem Schema"""

    def test_recipe_step_item(self):
        """测试步骤项"""
        data = {
            "id": "step-001",
            "step_number": 1,
            "description": "将山药去皮切块",
            "duration": 5
        }
        schema = RecipeStepItem(**data)

        assert schema.step_number == 1
        assert schema.description == "将山药去皮切块"
        assert schema.duration == 5


class TestRecipeResponse:
    """测试 RecipeResponse Schema"""

    def test_recipe_response(self):
        """测试菜谱响应"""
        now = datetime.now()
        data = {
            "id": "recipe-001",
            "name": "山药莲子粥",
            "desc": "健脾养胃",
            "cooking_time": 60,
            "difficulty": "easy",
            "suitable_constitutions": ["qi_deficiency"],
            "ingredients": [],
            "steps": [],
            "created_at": now.isoformat()
        }
        schema = RecipeResponse(**data)

        assert schema.id == "recipe-001"
        assert schema.name == "山药莲子粥"
        assert isinstance(schema.ingredients, list)


class TestRecipeListItem:
    """测试 RecipeListItem Schema"""

    def test_recipe_list_item(self):
        """测试菜谱列表项"""
        now = datetime.now()
        data = {
            "id": "recipe-001",
            "name": "山药莲子粥",
            "desc": "健脾养胃",
            "cooking_time": 60,
            "difficulty": "easy",
            "suitable_constitutions": ["qi_deficiency"],
            "efficacy_tags": ["健脾"],
            "solar_terms": [],
            "created_at": now.isoformat()
        }
        schema = RecipeListItem(**data)

        assert schema.id == "recipe-001"
        assert schema.name == "山药莲子粥"


class TestRecipeListResponse:
    """测试 RecipeListResponse Schema"""

    def test_recipe_list_response(self):
        """测试菜谱列表响应"""
        now = datetime.now()
        data = {
            "total": 100,
            "page": 1,
            "page_size": 20,
            "items": [
                {
                    "id": "recipe-001",
                    "name": "菜谱1",
                    "suitable_constitutions": [],
                    "efficacy_tags": [],
                    "solar_terms": [],
                    "created_at": now.isoformat()
                }
            ]
        }
        schema = RecipeListResponse(**data)

        assert schema.total == 100
        assert schema.page == 1
        assert len(schema.items) == 1


class TestRecipeImportBase:
    """测试 RecipeImportBase Schema"""

    def test_recipe_import_base(self):
        """测试导入 Schema"""
        data = {
            "name": "山药粥",
            "cooking_time": "30分钟",  # 字符串形式
            "difficulty": "简单",
            "suitable_constitutions": "气虚质,平和质",  # 字符串形式
            "ingredients_str": "山药100g, 糯米50g",
            "extra_field": "额外字段应该被允许"
        }
        schema = RecipeImportBase(**data)

        assert schema.name == "山药粥"
        assert schema.cooking_time == "30分钟"
        # extra_field 应该被允许但不会在 schema 中


class TestRecipeSearchRequest:
    """测试 RecipeSearchRequest Schema"""

    def test_valid_search_request(self):
        """测试有效的搜索请求"""
        data = {
            "keyword": "山药",
            "constitution": "qi_deficiency",
            "difficulty": "easy",
            "page": 1,
            "page_size": 20
        }
        schema = RecipeSearchRequest(**data)

        assert schema.keyword == "山药"
        assert schema.constitution == "qi_deficiency"

    def test_search_keyword_required(self):
        """测试关键词必填"""
        with pytest.raises(ValidationError):
            RecipeSearchRequest(constitution="qi_deficiency")

    def test_search_page_validation(self):
        """测试分页验证"""
        with pytest.raises(ValidationError):
            RecipeSearchRequest(keyword="测试", page=0)

        with pytest.raises(ValidationError):
            RecipeSearchRequest(keyword="测试", page_size=0)

        with pytest.raises(ValidationError):
            RecipeSearchRequest(keyword="测试", page_size=101)

    def test_search_invalid_constitution(self):
        """测试无效的体质筛选"""
        with pytest.raises(ValidationError):
            RecipeSearchRequest(keyword="测试", constitution="invalid")

    def test_search_invalid_difficulty(self):
        """测试无效的难度筛选"""
        with pytest.raises(ValidationError):
            RecipeSearchRequest(keyword="测试", difficulty="invalid")


class TestRecipeRecommendationRequest:
    """测试 RecipeRecommendationRequest Schema"""

    def test_valid_recommendation_request(self):
        """测试有效的推荐请求"""
        schema = RecipeRecommendationRequest(constitution="qi_deficiency")
        assert schema.constitution == "qi_deficiency"
        assert schema.limit == 20  # 默认值

    def test_recommendation_constitution_required(self):
        """测试体质必填"""
        with pytest.raises(ValidationError):
            RecipeRecommendationRequest()

    def test_recommendation_invalid_constitution(self):
        """测试无效的体质"""
        with pytest.raises(ValidationError):
            RecipeRecommendationRequest(constitution="invalid")

    def test_recommendation_limit_validation(self):
        """测试限制数量验证"""
        with pytest.raises(ValidationError):
            RecipeRecommendationRequest(constitution="qi_deficiency", limit=0)

        with pytest.raises(ValidationError):
            RecipeRecommendationRequest(constitution="qi_deficiency", limit=101)


class TestRecipeBatchRequest:
    """测试 RecipeBatchRequest Schema"""

    def test_valid_batch_request(self):
        """测试有效的批量请求"""
        schema = RecipeBatchRequest(ids=["recipe-001", "recipe-002", "recipe-003"])
        assert len(schema.ids) == 3

    def test_batch_ids_required(self):
        """测试 ID 列表必填"""
        with pytest.raises(ValidationError):
            RecipeBatchRequest()

    def test_batch_ids_max_length(self):
        """测试 ID 列表最大长度"""
        ids = [f"recipe-{i:03d}" for i in range(101)]
        with pytest.raises(ValidationError):
            RecipeBatchRequest(ids=ids)

    def test_batch_ids_min_length(self):
        """测试 ID 列表最小长度"""
        with pytest.raises(ValidationError):
            RecipeBatchRequest(ids=[])


class TestRecipeStatistics:
    """测试 RecipeStatistics Schema"""

    def test_valid_statistics(self):
        """测试有效的统计数据"""
        data = {
            "total_recipes": 1000,
            "with_difficulty": 800,
            "with_constitutions": 700,
            "with_efficacy_tags": 750,
            "with_solar_terms": 600,
            "difficulty_distribution": {
                "easy": 300,
                "medium": 400,
                "harder": 200,
                "hard": 100
            },
            "constitution_coverage": {
                "qi_deficiency": 300,
                "yin_deficiency": 250,
                "peace": 150
            }
        }
        schema = RecipeStatistics(**data)

        assert schema.total_recipes == 1000
        assert schema.with_difficulty == 800
        assert len(schema.difficulty_distribution) == 4

    def test_statistics_defaults(self):
        """测试统计默认值"""
        schema = RecipeStatistics(
            total_recipes=100,
            with_difficulty=80,
            with_constitutions=70,
            with_efficacy_tags=75,
            with_solar_terms=60
        )

        assert schema.difficulty_distribution == {}
        assert schema.constitution_coverage == {}

    def test_statistics_negative_values(self):
        """测试负数验证"""
        with pytest.raises(ValidationError):
            RecipeStatistics(
                total_recipes=-100,
                with_difficulty=80,
                with_constitutions=70,
                with_efficacy_tags=75,
                with_solar_terms=60
            )
