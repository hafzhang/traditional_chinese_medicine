"""
Unit tests for RecipeService
测试食谱服务层
"""

import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from api.services.recipe_service import RecipeService, get_recipe_service


class TestRecipeService:
    """测试 RecipeService 类"""

    def test_service_is_stateless(self):
        """测试服务是无状态的"""
        service1 = RecipeService()
        service2 = RecipeService()
        # 两个实例应该独立（不是单例）
        assert service1 is not service2

    def test_get_recipe_service_returns_new_instance(self):
        """测试工厂函数返回新实例"""
        service1 = get_recipe_service()
        service2 = get_recipe_service()
        # 工厂函数应该返回新实例（不是单例）
        assert isinstance(service1, RecipeService)
        assert isinstance(service2, RecipeService)
        # 但每次调用都返回新实例
        assert service1 is not service2

    def test_valid_constitutions(self):
        """测试有效的体质代码"""
        service = RecipeService()
        assert service.VALID_CONSTITUTIONS == {
            "peace", "qi_deficiency", "yang_deficiency", "yin_deficiency",
            "phlegm_damp", "damp_heat", "blood_stasis", "qi_depression", "special"
        }

    def test_difficulty_levels(self):
        """测试难度级别"""
        service = RecipeService()
        assert service.DIFFICULTY_LEVELS == ["easy", "medium", "harder", "hard"]

    def test_season_to_solar_terms_mapping(self):
        """测试四季到节气映射"""
        service = RecipeService()
        assert 'spring' in service.SEASON_TO_SOLAR_TERMS
        assert 'summer' in service.SEASON_TO_SOLAR_TERMS
        assert 'autumn' in service.SEASON_TO_SOLAR_TERMS
        assert 'winter' in service.SEASON_TO_SOLAR_TERMS
        assert len(service.SEASON_TO_SOLAR_TERMS['spring']) == 6
        assert len(service.SEASON_TO_SOLAR_TERMS['summer']) == 7  # includes changxia

    @patch('api.services.recipe_service.joinedload')
    @patch('api.services.recipe_service.Recipe')
    def test_get_recipe_by_id(self, mock_recipe_class, mock_joinedload):
        """测试根据ID获取食谱"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query

        # Mock joinedload chain
        mock_joinedload1 = Mock()
        mock_joinedload2 = Mock()
        mock_joinedload.return_value = mock_joinedload1
        mock_joinedload1.return_value = mock_joinedload2
        mock_query.options.return_value = mock_query
        mock_filter = Mock()
        mock_query.filter.return_value = mock_filter
        mock_recipe = Mock(id=1)
        mock_filter.first.return_value = mock_recipe

        service = RecipeService()
        result = service.get_recipe_by_id(1, mock_db)

        assert result == mock_recipe
        mock_db.query.assert_called_once()

    @patch('api.services.recipe_service.joinedload')
    @patch('api.services.recipe_service.Recipe')
    def test_get_recipe_by_id_not_found(self, mock_recipe_class, mock_joinedload):
        """测试根据ID获取不存在的食谱"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query

        # Mock joinedload chain
        mock_joinedload1 = Mock()
        mock_joinedload2 = Mock()
        mock_joinedload.return_value = mock_joinedload1
        mock_joinedload1.return_value = mock_joinedload2
        mock_query.options.return_value = mock_query
        mock_filter = Mock()
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None

        service = RecipeService()
        result = service.get_recipe_by_id(999, mock_db)

        assert result is None

    def test_get_recipes_basic(self):
        """测试基本列表查询"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 100
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = [Mock(id=1), Mock(id=2)]

        service = RecipeService()
        result = service.get_recipes(mock_db, page=1, page_size=20)

        assert result['total'] == 100
        assert result['page'] == 1
        assert result['page_size'] == 20
        assert len(result['items']) == 2

    def test_get_recipes_with_constitution_filter(self):
        """测试体质筛选"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 10
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = []

        service = RecipeService()
        result = service.get_recipes(mock_db, constitution='qi_deficiency')

        # 验证筛选条件被应用
        assert mock_query.filter.call_count >= 1
        assert result['total'] == 10

    def test_get_recipes_invalid_constitution_raises_error(self):
        """测试无效体质代码抛出错误"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query

        service = RecipeService()
        with pytest.raises(ValueError, match="Invalid constitution code"):
            service.get_recipes(mock_db, constitution='invalid_code')

    def test_get_recipes_with_difficulty_filter(self):
        """测试难度筛选"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 5
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = []

        service = RecipeService()
        result = service.get_recipes(mock_db, difficulty='easy')

        assert result['total'] == 5

    def test_get_recipes_invalid_difficulty_raises_error(self):
        """测试无效难度级别抛出错误"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query

        service = RecipeService()
        with pytest.raises(ValueError, match="Invalid difficulty level"):
            service.get_recipes(mock_db, difficulty='invalid')

    def test_get_recipes_with_season_filter(self):
        """测试季节筛选"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 15
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = []

        service = RecipeService()
        result = service.get_recipes(mock_db, season='spring')

        assert result['total'] == 15

    def test_get_recipes_pagination(self):
        """测试分页计算"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 100
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = []

        service = RecipeService()
        result = service.get_recipes(mock_db, page=3, page_size=10)

        # 验证 offset 计算正确: (3-1) * 10 = 20
        mock_query.offset.assert_called_with(20)
        assert result['page'] == 3

    def test_is_valid_constitution_code_valid(self):
        """测试有效的体质代码验证"""
        service = RecipeService()
        assert service.is_valid_constitution_code('peace') is True
        assert service.is_valid_constitution_code('qi_deficiency') is True
        assert service.is_valid_constitution_code('special') is True

    def test_is_valid_constitution_code_invalid(self):
        """测试无效的体质代码验证"""
        service = RecipeService()
        assert service.is_valid_constitution_code('invalid') is False
        assert service.is_valid_constitution_code('') is False
        assert service.is_valid_constitution_code('qi') is False

    def test_get_constitution_name(self):
        """测试获取体质中文名称"""
        service = RecipeService()
        assert service.get_constitution_name('peace') == '平和质'
        assert service.get_constitution_name('qi_deficiency') == '气虚质'
        assert service.get_constitution_name('yang_deficiency') == '阳虚质'
        assert service.get_constitution_name('invalid') == 'invalid'  # 返回原值

    @patch('api.services.recipe_service.Recipe')
    def test_get_recipes_by_constitution(self, mock_recipe_class):
        """测试根据体质获取食谱列表"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_filter = Mock()
        mock_query.filter.return_value = mock_filter
        mock_order = Mock()
        mock_filter.order_by.return_value = mock_order
        mock_limit = Mock()
        mock_order.limit.return_value = mock_limit
        mock_recipes = [Mock(id=1), Mock(id=2)]
        mock_limit.all.return_value = mock_recipes

        service = RecipeService()
        result = service.get_recipes_by_constitution('qi_deficiency', mock_db, limit=10)

        assert len(result) == 2
        assert result == mock_recipes

    @patch('api.services.recipe_service.Recipe')
    def test_get_recipes_by_constitution_invalid_raises_error(self, mock_recipe_class):
        """测试无效体质代码抛出错误"""
        mock_db = Mock()

        service = RecipeService()
        with pytest.raises(ValueError, match="Invalid constitution code"):
            service.get_recipes_by_constitution('invalid', mock_db)

    @patch('api.services.recipe_service.Recipe')
    def test_get_recommendations_by_constitution(self, mock_recipe_class):
        """测试根据体质获取推荐"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_filter = Mock()
        mock_query.filter.return_value = mock_filter
        mock_order = Mock()
        mock_filter.order_by.return_value = mock_order
        mock_limit = Mock()
        mock_order.limit.return_value = mock_limit
        mock_recipes = [Mock(id=1)]
        mock_limit.all.return_value = mock_recipes

        service = RecipeService()
        result = service.get_recommendations_by_constitution('qi_deficiency', limit=5, db=mock_db)

        assert len(result) == 1
        # 验证同时检查适合和禁忌体质
        assert mock_query.filter.call_count == 1

    @patch('api.services.recipe_service.Recipe')
    def test_get_recommendations_by_constitution_invalid_raises_error(self, mock_recipe_class):
        """测试无效体质代码抛出错误"""
        mock_db = Mock()

        service = RecipeService()
        with pytest.raises(ValueError, match="Invalid constitution code"):
            service.get_recommendations_by_constitution('invalid', limit=5, db=mock_db)


class TestRecipeServiceSearch:
    """测试 RecipeService 搜索功能"""

    @patch('sqlalchemy.or_')
    @patch('api.services.recipe_service.Recipe')
    def test_search_recipes_basic(self, mock_recipe_class, mock_or):
        """测试基本搜索"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 5
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = [Mock(id=1), Mock(id=2)]

        service = RecipeService()
        result = service.search_recipes('山药', mock_db)

        assert result['total'] == 5
        assert len(result['items']) == 2
        assert mock_query.filter.call_count >= 1  # 至少有搜索条件的 filter

    @patch('sqlalchemy.or_')
    @patch('api.services.recipe_service.Recipe')
    def test_search_recipes_with_constitution(self, mock_recipe_class, mock_or):
        """测试带体质筛选的搜索"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 3
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = []

        service = RecipeService()
        result = service.search_recipes('山药', mock_db, constitution='qi_deficiency')

        assert result['total'] == 3

    @patch('sqlalchemy.or_')
    @patch('api.services.recipe_service.Recipe')
    def test_search_recipes_with_difficulty(self, mock_recipe_class, mock_or):
        """测试带难度筛选的搜索"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 2
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = []

        service = RecipeService()
        result = service.search_recipes('汤', mock_db, difficulty='easy')

        assert result['total'] == 2

    @patch('sqlalchemy.or_')
    @patch('api.services.recipe_service.Recipe')
    def test_search_recipes_invalid_constitution_raises_error(self, mock_recipe_class, mock_or):
        """测试无效体质代码抛出错误"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query

        service = RecipeService()
        with pytest.raises(ValueError, match="Invalid constitution code"):
            service.search_recipes('山药', mock_db, constitution='invalid')

    @patch('sqlalchemy.or_')
    @patch('api.services.recipe_service.Recipe')
    def test_search_recipes_invalid_difficulty_raises_error(self, mock_recipe_class, mock_or):
        """测试无效难度级别抛出错误"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query

        service = RecipeService()
        with pytest.raises(ValueError, match="Invalid difficulty level"):
            service.search_recipes('汤', mock_db, difficulty='invalid')


class TestRecipeServiceErrorHandling:
    """测试 RecipeService 错误处理和日志"""

    @patch('api.services.recipe_service.logger')
    @patch('api.services.recipe_service.joinedload')
    @patch('api.services.recipe_service.Recipe')
    def test_get_recipe_by_id_logs_and_handles_db_error(self, mock_recipe_class, mock_joinedload, mock_logger):
        """测试 get_recipe_by_id 处理数据库错误并记录日志"""
        from sqlalchemy.exc import SQLAlchemyError

        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query

        # Setup mock chain that raises SQLAlchemyError
        mock_joinedload.return_value = Mock()
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.side_effect = SQLAlchemyError("Database connection failed")

        service = RecipeService()
        with pytest.raises(SQLAlchemyError):
            service.get_recipe_by_id(1, mock_db)

        # 验证日志被调用
        assert mock_logger.info.called
        assert mock_logger.error.called

    @patch('api.services.recipe_service.logger')
    @patch('api.services.recipe_service.Recipe')
    def test_get_recipes_logs_and_handles_db_error(self, mock_recipe_class, mock_logger):
        """测试 get_recipes 处理数据库错误并记录日志"""
        from sqlalchemy.exc import SQLAlchemyError

        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        # count() 抛出异常
        mock_query.count.side_effect = SQLAlchemyError("Query failed")

        service = RecipeService()
        with pytest.raises(SQLAlchemyError):
            service.get_recipes(mock_db, page=1)

        # 验证 info 日志记录了参数
        assert mock_logger.info.called
        # 验证 error 日志记录了错误
        assert mock_logger.error.called

    @patch('api.services.recipe_service.logger')
    def test_get_recipe_by_id_logs_info(self, mock_logger):
        """测试 get_recipe_by_id 记录 info 日志"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query

        # Mock joinedload chain
        from unittest.mock import MagicMock
        mock_options_result = MagicMock()
        mock_query.options.return_value = mock_options_result
        mock_filter_result = MagicMock()
        mock_options_result.filter.return_value = mock_filter_result
        mock_filter_result.first.return_value = None

        service = RecipeService()
        service.get_recipe_by_id(1, mock_db)

        # 验证 info 日志被调用（记录 recipe_id）
        assert any('Fetching recipe with id: 1' in str(call) for call in mock_logger.info.call_args_list)

    @patch('api.services.recipe_service.logger')
    def test_get_recipes_logs_params(self, mock_logger):
        """测试 get_recipes 记录查询参数"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 0
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = []

        service = RecipeService()
        service.get_recipes(mock_db, page=2, page_size=10, constitution='qi_deficiency')

        # 验证 info 日志记录了参数
        assert any('page=2' in str(call) for call in mock_logger.info.call_args_list)
        assert any('constitution=qi_deficiency' in str(call) for call in mock_logger.info.call_args_list)

    @patch('api.services.recipe_service.logger')
    def test_search_recipes_logs_keyword(self, mock_logger):
        """测试 search_recipes 记录搜索关键词"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 0
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = []

        service = RecipeService()
        service.search_recipes('山药', mock_db)

        # 验证 info 日志记录了关键词
        assert any('keyword: 山药' in str(call) for call in mock_logger.info.call_args_list)

    @patch('api.services.recipe_service.logger')
    def test_get_recipes_by_constitution_logs_params(self, mock_logger):
        """测试 get_recipes_by_constitution 记录参数"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_filter = Mock()
        mock_query.filter.return_value = mock_filter
        mock_order = Mock()
        mock_filter.order_by.return_value = mock_order
        mock_limit = Mock()
        mock_order.limit.return_value = mock_limit
        mock_limit.all.return_value = []

        service = RecipeService()
        service.get_recipes_by_constitution('qi_deficiency', mock_db, limit=5)

        # 验证 info 日志记录了参数
        assert any('constitution: qi_deficiency' in str(call) for call in mock_logger.info.call_args_list)
        assert any('limit: 5' in str(call) for call in mock_logger.info.call_args_list)

    @patch('api.services.recipe_service.logger')
    def test_get_recommendations_by_constitution_logs_params(self, mock_logger):
        """测试 get_recommendations_by_constitution 记录参数"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_filter = Mock()
        mock_query.filter.return_value = mock_filter
        mock_order = Mock()
        mock_filter.order_by.return_value = mock_order
        mock_limit = Mock()
        mock_order.limit.return_value = mock_limit
        mock_limit.all.return_value = []

        service = RecipeService()
        service.get_recommendations_by_constitution('qi_deficiency', limit=10, db=mock_db)

        # 验证 info 日志记录了参数
        assert any('constitution: qi_deficiency' in str(call) for call in mock_logger.info.call_args_list)
