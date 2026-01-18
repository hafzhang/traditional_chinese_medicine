"""
食材API集成测试
API Integration Tests for Ingredients
"""

import pytest
from fastapi.testclient import TestClient


class TestIngredientsAPI:
    """食材API集成测试"""

    def test_get_ingredients_list_empty(self, client: TestClient, db_session):
        """测试获取空食材列表"""
        response = client.get("/api/v1/ingredients")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["total"] == 0
        assert data["data"]["items"] == []

    def test_get_ingredient_not_found(self, client: TestClient):
        """测试获取不存在的食材"""
        response = client.get("/api/v1/ingredients/non-existent-id")

        assert response.status_code == 404

    def test_get_recommended_ingredients_no_constitutions(self, client: TestClient, db_session):
        """测试获取推荐食材（无数据）"""
        response = client.get("/api/v1/ingredients/recommend/qi_deficiency")

        assert response.status_code == 200
        data = response.json()
        assert "recommended" in data["data"]
        assert "avoided" in data["data"]
