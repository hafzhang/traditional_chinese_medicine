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

    def test_get_ingredient_by_id_not_found(self, db_session):
        """测试获取不存在的食材"""
        service = IngredientService()
        result = service.get_ingredient_by_id("non-existent-id", db_session)
        assert result is None

    def test_get_ingredients_by_constitution_empty(self, db_session):
        """测试空数据库的体质筛选"""
        service = IngredientService()
        result = service.get_ingredients_by_constitution("qi_deficiency", db_session)
        assert result == []

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
