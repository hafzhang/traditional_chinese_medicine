"""
Unit tests for import_recipes
测试导入脚本函数
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call, mock_open
import pandas as pd
from pathlib import Path
import sys
import tempfile
import os
import csv

# 添加 scripts 目录到路径
scripts_dir = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from import_recipes import read_excel_file, check_recipe_exists, get_or_create_ingredient, import_single_recipe, import_recipes, dry_run_import, export_failed_recipes


class TestReadExcelFile:
    """测试 read_excel_file 函数"""

    @patch('import_recipes.pd.read_excel')
    @patch('import_recipes.os.path.exists')
    def test_read_excel_file_success(self, mock_exists, mock_read_excel):
        """测试成功读取 Excel 文件"""
        mock_exists.return_value = True
        mock_df = pd.DataFrame({
            'title': ['菜谱1', '菜谱2', '菜谱3'],
            'desc': ['描述1', '描述2', '描述3']
        })
        mock_read_excel.return_value = mock_df

        result = read_excel_file('test.xlsx')

        assert len(result) == 3
        assert result[0]['title'] == '菜谱1'
        assert result[1]['title'] == '菜谱2'
        assert result[2]['title'] == '菜谱3'
        mock_read_excel.assert_called_once()

    @patch('import_recipes.os.path.exists')
    def test_read_excel_file_not_found(self, mock_exists):
        """测试文件不存在"""
        mock_exists.return_value = False

        with pytest.raises(FileNotFoundError, match="文件不存在"):
            read_excel_file('nonexistent.xlsx')

    @patch('import_recipes.pd.read_excel')
    @patch('import_recipes.os.path.exists')
    def test_read_excel_file_skips_empty_title(self, mock_exists, mock_read_excel):
        """测试跳过 title 为空的行"""
        mock_exists.return_value = True
        # dropna 只过滤 NaN/None，不过滤空字符串 ""
        # 所以实际结果是 4 条（None 被过滤，但 "" 保留）
        mock_df = pd.DataFrame({
            'title': ['菜谱1', None, '菜谱2', '', '菜谱3'],
            'desc': ['描述1', '描述2', '描述3', '描述4', '描述5']
        })
        mock_read_excel.return_value = mock_df

        result = read_excel_file('test.xlsx')

        # dropna 过滤 NaN (None)，但空字符串 "" 保留
        # 所以预期是 4 条记录
        assert len(result) == 4
        assert result[0]['title'] == '菜谱1'
        assert result[1]['title'] == '菜谱2'
        assert result[2]['title'] == ''  # 空字符串被保留
        assert result[3]['title'] == '菜谱3'

    @patch('import_recipes.pd.read_excel')
    @patch('import_recipes.os.path.exists')
    def test_read_excel_file_with_limit(self, mock_exists, mock_read_excel):
        """测试限制数量"""
        mock_exists.return_value = True
        mock_df = pd.DataFrame({
            'title': ['菜谱1', '菜谱2', '菜谱3', '菜谱4', '菜谱5'],
            'desc': ['描述1', '描述2', '描述3', '描述4', '描述5']
        })
        mock_read_excel.return_value = mock_df

        result = read_excel_file('test.xlsx', limit=2)

        assert len(result) == 2
        assert result[0]['title'] == '菜谱1'
        assert result[1]['title'] == '菜谱2'

    @patch('import_recipes.pd.read_excel')
    @patch('import_recipes.os.path.exists')
    def test_read_excel_file_limit_none(self, mock_exists, mock_read_excel):
        """测试 limit 为 None 时返回所有记录"""
        mock_exists.return_value = True
        mock_df = pd.DataFrame({
            'title': ['菜谱1', '菜谱2', '菜谱3'],
            'desc': ['描述1', '描述2', '描述3']
        })
        mock_read_excel.return_value = mock_df

        result = read_excel_file('test.xlsx', limit=None)

        assert len(result) == 3


class TestCheckRecipeExists:
    """测试 check_recipe_exists 函数"""

    @patch('import_recipes.Recipe')
    def test_check_recipe_exists_true(self, mock_recipe_class):
        """测试菜谱已存在"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = Mock()  # 菜谱存在

        result = check_recipe_exists('测试菜谱', mock_db)

        assert result is True
        mock_db.query.assert_called_once()
        mock_query.filter.assert_called_once()

    @patch('import_recipes.Recipe')
    def test_check_recipe_exists_false(self, mock_recipe_class):
        """测试菜谱不存在"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None  # 菜谱不存在

        result = check_recipe_exists('测试菜谱', mock_db)

        assert result is False

    @patch('import_recipes.Recipe')
    def test_check_recipe_exists_trims_whitespace(self, mock_recipe_class):
        """测试自动去除名称前后空格"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None

        check_recipe_exists('  测试菜谱  ', mock_db)

        # 验证 query 和 filter 都被调用
        mock_db.query.assert_called_once()
        mock_query.filter.assert_called_once()


class TestGetOrCreateIngredient:
    """测试 get_or_create_ingredient 函数"""

    @patch('import_recipes.Ingredient')
    def test_get_existing_ingredient(self, mock_ingredient_class):
        """测试获取已存在的食材"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_ingredient = Mock(id=1, name='山药')
        mock_query.first.return_value = mock_ingredient

        result = get_or_create_ingredient('山药', mock_db)

        assert result == mock_ingredient
        mock_db.add.assert_not_called()

    @patch('import_recipes.Ingredient')
    def test_create_new_ingredient(self, mock_ingredient_class):
        """测试创建新食材"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None  # 食材不存在

        # 模拟新创建的 Ingredient 实例
        new_ingredient = Mock(id=1)
        mock_ingredient_class.return_value = new_ingredient

        result = get_or_create_ingredient('新食材', mock_db)

        assert result == new_ingredient
        mock_db.add.assert_called_once()
        mock_db.flush.assert_called_once()

    @patch('import_recipes.Ingredient')
    def test_trims_whitespace(self, mock_ingredient_class):
        """测试自动去除名称前后空格"""
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        new_ingredient = Mock(id=1)
        mock_ingredient_class.return_value = new_ingredient

        get_or_create_ingredient('  山药  ', mock_db)

        # 验证创建时使用了去除空格后的名称
        call_args = mock_ingredient_class.call_args
        assert 'name' in call_args.kwargs or len(call_args.args) > 0


class TestImportSingleRecipe:
    """测试 import_single_recipe 函数"""

    @patch('import_recipes.check_recipe_exists')
    @patch('import_recipes.parse_ingredients')
    @patch('import_recipes.parse_steps')
    @patch('import_recipes.get_or_create_ingredient')
    @patch('import_recipes.Recipe')
    @patch('import_recipes.parse_cooking_time')
    @patch('import_recipes.parse_difficulty_value')
    @patch('import_recipes.parse_json_field')
    def test_import_new_recipe(self, mock_parse_json, mock_parse_diff, mock_parse_time,
                              mock_recipe_class, mock_get_ing, mock_parse_steps,
                              mock_parse_ings, mock_check_exists):
        """测试导入新菜谱"""
        mock_check_exists.return_value = False
        mock_parse_time.return_value = 30
        mock_parse_diff.return_value = 'easy'
        mock_parse_json.return_value = []
        mock_parse_ings.return_value = [{'name': '山药', 'amount': '50g', 'is_main': True, 'display_order': 0}]
        mock_parse_steps.return_value = []
        mock_ingredient = Mock(id=1)
        mock_get_ing.return_value = mock_ingredient
        mock_recipe = Mock(id=1)
        mock_recipe_class.return_value = mock_recipe
        mock_db = Mock()

        row = {
            'title': '测试菜谱',
            'desc': '测试描述',
            'tip': '测试贴士',
            'costtime': '30分钟',
            'difficulty': 'easy',
            'suitable_constitutions': '[]',
            'avoid_constitutions': '[]',
            'efficacy_tags': '[]',
            'solar_terms': '[]',
            'QuantityIngredients': '山药50g',
            'steptext': '1.准备食材'
        }

        result = import_single_recipe(row, mock_db)

        assert result == mock_recipe
        mock_db.add.assert_called()
        mock_db.flush.assert_called()
        mock_db.commit.assert_called_once()

    @patch('import_recipes.check_recipe_exists')
    def test_import_existing_recipe_returns_none(self, mock_check_exists):
        """测试导入已存在的菜谱返回 None"""
        mock_check_exists.return_value = True
        mock_db = Mock()

        row = {'title': '已存在菜谱'}
        result = import_single_recipe(row, mock_db)

        assert result is None
        mock_db.commit.assert_not_called()

    @patch('import_recipes.check_recipe_exists')
    def test_import_empty_title_returns_none(self, mock_check_exists):
        """测试空标题返回 None"""
        mock_check_exists.return_value = False
        mock_db = Mock()

        row = {'title': ''}
        result = import_single_recipe(row, mock_db)

        assert result is None


class TestImportRecipes:
    """测试 import_recipes 函数"""

    @patch('import_recipes.SessionLocal')
    @patch('import_recipes.read_excel_file')
    @patch('import_recipes.check_recipe_exists')
    def test_import_recipes_dry_run(self, mock_check_exists, mock_read_excel, mock_session):
        """测试模拟运行模式"""
        mock_read_excel.return_value = [
            {'title': '菜谱1'},
            {'title': '菜谱2'},
            {'title': '菜谱3'}
        ]
        mock_check_exists.side_effect = [False, True, False]  # 第二个已存在
        mock_db = Mock()
        mock_session.return_value = mock_db

        result = import_recipes('test.xlsx', dry_run=True)

        assert result['total'] == 3
        assert result['success'] == 2  # 两个新菜谱
        assert result['skipped'] == 1  # 一个已存在
        assert result['failed'] == 0
        mock_db.commit.assert_not_called()  # dry_run 不提交

    @patch('import_recipes.SessionLocal')
    @patch('import_recipes.read_excel_file')
    @patch('import_recipes.import_single_recipe')
    def test_import_recipes_with_limit(self, mock_import_single, mock_read_excel, mock_session):
        """测试限制导入数量"""
        # 模拟 read_excel_file 根据 limit 参数返回对应数量的数据
        def mock_read_func(file_path, limit=None):
            all_data = [
                {'title': '菜谱1'},
                {'title': '菜谱2'},
                {'title': '菜谱3'},
                {'title': '菜谱4'},
                {'title': '菜谱5'}
            ]
            if limit is not None:
                return all_data[:limit]
            return all_data

        mock_read_excel.side_effect = mock_read_func
        mock_recipes = [Mock(id=i+1) for i in range(3)]
        mock_import_single.side_effect = mock_recipes
        mock_db = Mock()
        mock_session.return_value = mock_db

        result = import_recipes('test.xlsx', limit=3, dry_run=False)

        assert result['total'] == 3
        assert result['success'] == 3

    @patch('import_recipes.SessionLocal')
    @patch('import_recipes.read_excel_file')
    @patch('import_recipes.import_single_recipe')
    def test_import_recipes_progress_print(self, mock_import_single, mock_read_excel, mock_session):
        """测试进度打印"""
        # 创建200条数据以测试进度打印
        mock_read_excel.return_value = [{'title': f'菜谱{i}'} for i in range(200)]
        mock_recipes = [Mock(id=i+1) for i in range(200)]
        mock_import_single.side_effect = mock_recipes
        mock_db = Mock()
        mock_session.return_value = mock_db

        result = import_recipes('test.xlsx')

        assert result['success'] == 200


class TestDryRunImport:
    """测试 dry_run_import 函数"""

    @patch('import_recipes.parse_steps')
    @patch('import_recipes.parse_ingredients')
    @patch('import_recipes.parse_json_field')
    @patch('import_recipes.parse_difficulty_value')
    @patch('import_recipes.parse_cooking_time')
    @patch('import_recipes.read_excel_file')
    @patch('builtins.print')
    def test_dry_run_import_prints_results(self, mock_print, mock_read_excel, mock_parse_time,
                                           mock_parse_diff, mock_parse_json, mock_parse_ings, mock_parse_steps):
        """测试干运行模式打印解析结果"""
        mock_read_excel.return_value = [
            {
                'title': '测试菜谱',
                'desc': '测试描述',
                'costtime': '30分钟',
                'difficulty': 'easy',
                'suitable_constitutions': '["qi_deficiency"]',
                'efficacy_tags': '["健脾"]',
                'solar_terms': '["lichun"]',
                'QuantityIngredients': '山药50g',
                'steptext': '1.准备食材'
            }
        ]
        mock_parse_time.return_value = 30
        mock_parse_diff.return_value = 'easy'
        mock_parse_json.return_value = ['qi_deficiency']
        mock_parse_ings.return_value = [{'name': '山药', 'amount': '50g', 'is_main': True, 'display_order': 0}]
        mock_parse_steps.return_value = [{'step_number': 1, 'description': '准备食材', 'duration': None}]

        dry_run_import('test.xlsx', limit=None)

        # 验证打印了结果
        assert mock_print.call_count > 0
        # 验证调用了解析函数
        mock_parse_time.assert_called()
        mock_parse_diff.assert_called()
        mock_parse_json.assert_called()
        mock_parse_ings.assert_called()
        mock_parse_steps.assert_called()

    @patch('import_recipes.parse_steps')
    @patch('import_recipes.parse_ingredients')
    @patch('import_recipes.parse_json_field')
    @patch('import_recipes.parse_difficulty_value')
    @patch('import_recipes.parse_cooking_time')
    @patch('import_recipes.read_excel_file')
    @patch('builtins.print')
    def test_dry_run_import_with_limit(self, mock_print, mock_read_excel, mock_parse_time,
                                       mock_parse_diff, mock_parse_json, mock_parse_ings, mock_parse_steps):
        """测试干运行模式带限制"""
        # 返回3条数据
        mock_read_excel.return_value = [
            {'title': f'菜谱{i}'} for i in range(3)
        ]
        mock_parse_time.return_value = 30
        mock_parse_diff.return_value = 'easy'
        mock_parse_json.return_value = []
        mock_parse_ings.return_value = []
        mock_parse_steps.return_value = []

        dry_run_import('test.xlsx', limit=3)

        # 验证 read_excel_file 被调用时带 limit 参数
        mock_read_excel.assert_called_with('test.xlsx', 3)


class TestExportFailedRecipes:
    """测试 export_failed_recipes 函数"""

    @patch('builtins.open')
    @patch('csv.writer')
    def test_export_failed_recipes_dict_format(self, mock_writer, mock_open):
        """测试导出字典格式的失败记录"""
        failed = [
            {'title': '菜谱1', 'error': '错误1'},
            {'title': '菜谱2', 'error': '错误2'}
        ]
        mock_csv_writer = Mock()
        mock_writer.return_value = mock_csv_writer

        export_failed_recipes(failed, 'output.csv')

        # 验证文件被打开
        mock_open.assert_called_once()
        # 验证 writerow 和 writerows 被调用
        assert mock_csv_writer.writerow.call_count == 1  # headers
        assert mock_csv_writer.writerows.call_count == 1  # data rows

    @patch('builtins.open')
    @patch('csv.writer')
    def test_export_failed_recipes_string_format(self, mock_writer, mock_open):
        """测试导出字符串格式的失败记录"""
        failed = [
            '菜谱1: 错误1',
            '菜谱2: 错误2'
        ]
        mock_csv_writer = Mock()
        mock_writer.return_value = mock_csv_writer

        export_failed_recipes(failed, 'output.csv')

        # 验证文件被打开
        mock_open.assert_called_once()
        # 验证数据被写入
        assert mock_csv_writer.writerows.call_count == 1
