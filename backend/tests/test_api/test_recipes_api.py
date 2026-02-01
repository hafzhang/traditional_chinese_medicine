"""
食谱API集成测试
Integration Tests for Recipe API
"""

import pytest


class TestRecipesAPI:
    """食谱API集成测试"""

    def test_get_recipes_list(self, client, db_session):
        """测试获取食谱列表"""
        from api.models import Recipe
        recipes = [
            Recipe(
                id=f"api-recipe-{i:03d}",
                name=f"食谱{i}",
                type="粥类"
            )
            for i in range(1, 11)
        ]
        db_session.add_all(recipes)
        db_session.commit()

        response = client.get("/api/v1/recipes")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "data" in data
        assert data["data"]["total"] == 10

    def test_get_recipe_detail(self, client, db_session):
        """测试获取食谱详情"""
        from api.models import Recipe
        recipe = Recipe(
            id="api-recipe-detail-001",
            name="山药莲子粥",
            type="粥类",
            difficulty="简单",
            ingredients={"main": [{"name": "山药", "amount": "100g"}]},
            steps=["步骤1", "步骤2"]
        )
        db_session.add(recipe)
        db_session.commit()

        response = client.get("/api/v1/recipes/api-recipe-detail-001")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["name"] == "山药莲子粥"
        assert "steps" in data["data"]

    def test_get_recipes_by_constitution(self, client, db_session):
        """测试按体质获取食谱"""
        from api.models import Recipe
        recipes = [
            Recipe(
                id=f"api-recipe-const-{i:03d}",
                name=f"食谱{i}",
                type="粥类",
                suitable_constitutions=["qi_deficiency"] if i % 2 == 0 else []
            )
            for i in range(1, 11)
        ]
        db_session.add_all(recipes)
        db_session.commit()

        response = client.get("/api/v1/recipes/recommend/qi_deficiency")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "recipes" in data["data"]

    def test_search_recipes(self, client, db_session):
        """测试搜索食谱"""
        from api.models import Recipe
        recipe = Recipe(
            id="api-recipe-search-001",
            name="山药粥",
            type="粥类",
            tags=["健脾", "养胃"]
        )
        db_session.add(recipe)
        db_session.commit()

        response = client.get("/api/v1/recipes?search=山药")

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) > 0

    def test_recipe_not_found(self, client, db_session):
        """测试食谱不存在"""
        response = client.get("/api/v1/recipes/non-existent-id")

        assert response.status_code == 404

    def test_get_recipes_by_type(self, client, db_session):
        """测试按类型获取食谱"""
        from api.models import Recipe
        recipes = [
            Recipe(
                id=f"type-api-{i:03d}",
                name=f"食谱{i}",
                type="粥类" if i % 2 == 0 else "汤类"
            )
            for i in range(1, 11)
        ]
        db_session.add_all(recipes)
        db_session.commit()

        response = client.get("/api/v1/recipes?type=粥类")

        assert response.status_code == 200
        data = response.json()
        assert all(item["type"] == "粥类" for item in data["data"]["items"])

    # ========== US-011: Additional Comprehensive API Tests ==========

    def test_get_recipes_list_with_pagination(self, client, db_session):
        """测试API分页功能"""
        from api.models import Recipe
        recipes = [
            Recipe(
                id=f"api-page-{i:03d}",
                name=f"食谱{i}",
                type="粥类"
            )
            for i in range(1, 31)
        ]
        db_session.add_all(recipes)
        db_session.commit()

        response = client.get("/api/v1/recipes?skip=0&limit=10")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total"] == 30
        assert len(data["data"]["items"]) == 10

    def test_get_recipes_by_difficulty(self, client, db_session):
        """测试按难度筛选"""
        from api.models import Recipe
        recipes = [
            Recipe(
                id=f"api-diff-{i:03d}",
                name=f"食谱{i}",
                type="粥类",
                difficulty="简单" if i % 2 == 0 else "中等"
            )
            for i in range(1, 11)
        ]
        db_session.add_all(recipes)
        db_session.commit()

        response = client.get("/api/v1/recipes?difficulty=简单")

        assert response.status_code == 200
        data = response.json()
        assert all(item["difficulty"] == "简单" for item in data["data"]["items"])

    def test_get_recipes_by_constitution_filter(self, client, db_session):
        """测试列表API的体质筛选"""
        from api.models import Recipe
        recipes = [
            Recipe(
                id=f"api-const-filter-{i:03d}",
                name=f"食谱{i}",
                type="粥类",
                suitable_constitutions=["qi_deficiency"] if i % 2 == 0 else ["yang_deficiency"]
            )
            for i in range(1, 11)
        ]
        db_session.add_all(recipes)
        db_session.commit()

        response = client.get("/api/v1/recipes?constitution=qi_deficiency")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total"] == 5

    def test_get_recipes_combined_filters(self, client, db_session):
        """测试组合筛选条件"""
        from api.models import Recipe
        recipes = [
            Recipe(
                id=f"api-combo-{i:03d}",
                name=f"山药汤{i}",
                type="粥类" if i % 2 == 0 else "汤类",
                difficulty="简单" if i % 3 == 0 else "中等",
                suitable_constitutions=["qi_deficiency"] if i % 5 == 0 else []
            )
            for i in range(1, 31)
        ]
        db_session.add_all(recipes)
        db_session.commit()

        response = client.get("/api/v1/recipes?type=粥类&difficulty=简单&constitution=qi_deficiency&search=山药")

        assert response.status_code == 200
        data = response.json()
        # 验证所有条件都满足
        for item in data["data"]["items"]:
            assert item["type"] == "粥类"
            assert item["difficulty"] == "简单"
            assert "山药" in item["name"]

    def test_get_recipe_detail_view_count_increments(self, client, db_session):
        """测试访问详情页增加浏览量"""
        from api.models import Recipe
        recipe = Recipe(
            id="api-view-count-001",
            name="浏览量测试食谱",
            type="粥类",
            view_count=10
        )
        db_session.add(recipe)
        db_session.commit()

        # 访问详情页
        response = client.get("/api/v1/recipes/api-view-count-001")

        assert response.status_code == 200
        db_session.refresh(recipe)
        assert recipe.view_count == 11

    def test_get_recipe_recommendation_all_meals(self, client, db_session):
        """测试体质推荐包含所有三餐"""
        from api.models import Recipe
        recipes = [
            Recipe(
                id="api-rec-breakfast-001",
                name="早餐粥",
                type="粥类",
                suitable_constitutions=["qi_deficiency"],
                view_count=100
            ),
            Recipe(
                id="api-rec-lunch-001",
                name="午餐菜",
                type="菜肴",
                suitable_constitutions=["qi_deficiency"],
                view_count=90
            ),
            Recipe(
                id="api-rec-dinner-001",
                name="晚餐汤",
                type="汤类",
                suitable_constitutions=["qi_deficiency"],
                view_count=80
            )
        ]
        db_session.add_all(recipes)
        db_session.commit()

        response = client.get("/api/v1/recipes/recommend/qi_deficiency")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "breakfast" in data["data"]["recipes"]
        assert "lunch" in data["data"]["recipes"]
        assert "dinner" in data["data"]["recipes"]
        assert data["data"]["constitution"] == "qi_deficiency"
        assert data["data"]["constitution_name"] == "气虚质"

    def test_get_recipe_recommendation_invalid_constitution(self, client, db_session):
        """测试无效体质代码返回400错误"""
        response = client.get("/api/v1/recipes/recommend/invalid_constitution")

        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_get_recipe_types_list(self, client, db_session):
        """测试获取食谱类型列表"""
        response = client.get("/api/v1/recipes/types/list")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        types = data["data"]
        assert len(types) == 6
        type_values = [t["value"] for t in types]
        assert "粥类" in type_values
        assert "汤类" in type_values
        assert "茶饮" in type_values
        assert "菜肴" in type_values
        assert "小吃" in type_values
        assert "主食" in type_values

    def test_get_recipe_difficulties_list(self, client, db_session):
        """测试获取食谱难度列表"""
        response = client.get("/api/v1/recipes/difficulties/list")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        difficulties = data["data"]
        assert len(difficulties) == 3
        difficulty_values = [d["value"] for d in difficulties]
        assert "简单" in difficulty_values
        assert "中等" in difficulty_values
        assert "困难" in difficulty_values

    def test_get_recipes_empty_database(self, client, db_session):
        """测试空数据库的响应"""
        response = client.get("/api/v1/recipes")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["total"] == 0
        assert data["data"]["items"] == []

    def test_get_recipes_limit_validation(self, client, db_session):
        """测试limit参数验证"""
        from api.models import Recipe
        recipes = [
            Recipe(
                id=f"api-limit-{i:03d}",
                name=f"食谱{i}",
                type="粥类"
            )
            for i in range(1, 201)
        ]
        db_session.add_all(recipes)
        db_session.commit()

        # 测试limit=100（最大值）
        response = client.get("/api/v1/recipes?limit=100")

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) <= 100

    def test_get_recipes_skip_validation(self, client, db_session):
        """测试skip参数验证（skip>=0）"""
        response = client.get("/api/v1/recipes?skip=-1")

        # skip=-1应该被验证（ge=0）
        assert response.status_code == 422  # Unprocessable Entity

    def test_get_recipes_all_nine_constitutions(self, client, db_session):
        """测试所有9种体质类型的API筛选"""
        from api.models import Recipe
        all_constitutions = [
            "peace", "qi_deficiency", "yang_deficiency", "yin_deficiency",
            "phlegm_damp", "damp_heat", "blood_stasis", "qi_depression", "special"
        ]

        # 为每种体质创建食谱
        recipes = []
        for i, constitution in enumerate(all_constitutions):
            recipes.append(Recipe(
                id=f"api-9-const-{i:03d}",
                name=f"{constitution}食谱",
                type="粥类",
                suitable_constitutions=[constitution]
            ))
        db_session.add_all(recipes)
        db_session.commit()

        # 验证每种体质都能通过API正确筛选
        for constitution in all_constitutions:
            response = client.get(f"/api/v1/recipes?constitution={constitution}")

            assert response.status_code == 200
            data = response.json()
            assert data["data"]["total"] >= 1

    def test_search_with_no_results(self, client, db_session):
        """测试搜索无结果的情况"""
        from api.models import Recipe
        recipe = Recipe(
            id="api-no-search-001",
            name="普通粥",
            type="粥类"
        )
        db_session.add(recipe)
        db_session.commit()

        response = client.get("/api/v1/recipes?search=不存在的关键词")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total"] == 0
        assert data["data"]["items"] == []

    def test_get_recipe_detail_has_all_fields(self, client, db_session):
        """测试食谱详情包含所有字段"""
        from api.models import Recipe
        recipe = Recipe(
            id="api-full-fields-001",
            name="完整字段食谱",
            type="粥类",
            difficulty="简单",
            cook_time=30,
            servings=2,
            desc="这是描述",
            tip="这是小贴士",
            suitable_constitutions=["qi_deficiency"],
            avoid_constitutions=["yin_deficiency"],
            symptoms=["失眠"],
            suitable_seasons=["春", "夏"],
            efficacy_tags=["健脾"],
            solar_terms=["立春"],
            ingredients={"main": [{"name": "山药", "amount": "100g"}]},
            steps=["步骤1", "步骤2"],
            efficacy="功效说明",
            health_benefits="健康益处",
            precautions="注意事项",
            tags=["标签1"],
            view_count=5
        )
        db_session.add(recipe)
        db_session.commit()

        response = client.get("/api/v1/recipes/api-full-fields-001")

        assert response.status_code == 200
        data = response.json()["data"]

        # 验证PRD字段存在
        assert "id" in data
        assert "name" in data
        assert "type" in data
        assert "difficulty" in data
        assert "cooking_time" in data
        assert "servings" in data
        assert "desc" in data
        assert "tip" in data
        assert "suitable_constitutions" in data
        assert "avoid_constitutions" in data
        assert "efficacy_tags" in data
        assert "solar_terms" in data
        assert "view_count" in data

    def test_response_format_standard(self, client, db_session):
        """测试标准响应格式 {code: 0, data: {...}}"""
        from api.models import Recipe
        recipe = Recipe(
            id="api-format-001",
            name="格式测试食谱",
            type="粥类"
        )
        db_session.add(recipe)
        db_session.commit()

        # 测试列表响应格式
        response_list = client.get("/api/v1/recipes")
        assert response_list.status_code == 200
        data_list = response_list.json()
        assert "code" in data_list
        assert "data" in data_list
        assert "message" in data_list
        assert data_list["code"] == 0

        # 测试详情响应格式
        response_detail = client.get("/api/v1/recipes/api-format-001")
        assert response_detail.status_code == 200
        data_detail = response_detail.json()
        assert "code" in data_detail
        assert "data" in data_detail
        assert "message" in data_detail
        assert data_detail["code"] == 0
