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
        """测试按体质获取食谱 - 使用新的recommend endpoint"""
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

        # 使用新的 recommend endpoint
        response = client.get("/api/v1/recipes/recommend?recommend_type=constitution&constitution=qi_deficiency")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "items" in data["data"]

    def test_search_recipes(self, client, db_session):
        """测试搜索食谱 - 使用新的search endpoint"""
        from api.models import Recipe
        recipe = Recipe(
            id="api-recipe-search-001",
            name="山药粥",
            type="粥类",
            tags=["健脾", "养胃"]
        )
        db_session.add(recipe)
        db_session.commit()

        # 使用新的 search endpoint
        response = client.get("/api/v1/recipes/search?keyword=山药")

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) > 0

    def test_recipe_not_found(self, client, db_session):
        """测试食谱不存在"""
        response = client.get("/api/v1/recipes/non-existent-id")

        assert response.status_code == 404

    def test_get_recipes_by_type(self, client, db_session):
        """测试按类型获取食谱 - 注：新API不支持type筛选，移除此测试"""
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

        # 新API不支持type筛选，测试基本列表功能
        response = client.get("/api/v1/recipes")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total"] == 10

    def test_get_recipes_with_filters(self, client, db_session):
        """测试筛选功能 - constitution, difficulty, efficacy等"""
        from api.models import Recipe
        recipes = [
            Recipe(
                id=f"filter-api-{i:03d}",
                name=f"食谱{i}",
                type="粥类",
                difficulty="简单" if i % 2 == 0 else "困难",
                suitable_constitutions=["qi_deficiency"] if i % 3 == 0 else [],
                efficacy_tags=["健脾"] if i % 2 == 0 else []
            )
            for i in range(1, 11)
        ]
        db_session.add_all(recipes)
        db_session.commit()

        # 测试体质筛选
        response = client.get("/api/v1/recipes?constitution=qi_deficiency")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["total"] > 0

        # 测试难度筛选
        response = client.get("/api/v1/recipes?difficulty=简单")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0

    def test_recommend_invalid_type(self, client, db_session):
        """测试无效的推荐类型"""
        response = client.get("/api/v1/recipes/recommend?recommend_type=invalid")

        assert response.status_code == 400

    def test_recommend_missing_params(self, client, db_session):
        """测试缺少必需参数"""
        response = client.get("/api/v1/recipes/recommend?recommend_type=constitution")

        assert response.status_code == 400

    def test_pagination(self, client, db_session):
        """测试分页"""
        from api.models import Recipe
        recipes = [
            Recipe(
                id=f"page-api-{i:03d}",
                name=f"食谱{i}",
                type="粥类"
            )
            for i in range(1, 26)
        ]
        db_session.add_all(recipes)
        db_session.commit()

        # 第一页
        response = client.get("/api/v1/recipes?page=1&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total"] == 25
        assert data["data"]["page"] == 1
        assert len(data["data"]["items"]) == 10

        # 第二页
        response = client.get("/api/v1/recipes?page=2&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["page"] == 2
