"""
单元测试 - 菜谱导入脚本
测试 import_recipes.py 中的函数
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import os

# Import the functions to test
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from scripts.import_recipes import load_excel


class TestLoadExcel:
    """测试 load_excel 函数"""

    def test_load_excel_success(self):
        """测试成功读取有效的 Excel 文件"""
        # 创建临时 Excel 文件
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # 创建测试数据
            data = {
                'title': ['山药小米粥', '西红柿炒蛋', '银耳莲子汤'],
                'steptext': ['步骤1\n步骤2', '步骤1', '步骤1\n步骤2\n步骤3'],
                'QuantityIngredients': ['山药50g,小米100g', '西红柿2个,鸡蛋2个', '银耳10g,莲子20g'],
                'costtime': ['30分钟', '15分钟', '1小时']
            }
            df = pd.DataFrame(data)
            df.to_excel(tmp_path, index=False)

            # 测试读取
            result = load_excel(tmp_path)

            # 验证
            assert len(result) == 3
            assert list(result.columns) == ['title', 'steptext', 'QuantityIngredients', 'costtime']
            assert result['title'].tolist() == ['山药小米粥', '西红柿炒蛋', '银耳莲子汤']
        finally:
            # 清理
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_load_excel_missing_required_columns(self):
        """测试缺少必需列时抛出 ValueError"""
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # 创建缺少必需列的测试数据
            data = {
                'title': ['山药小米粥'],
                'steptext': ['步骤1']
                # 缺少 QuantityIngredients 和 costtime
            }
            df = pd.DataFrame(data)
            df.to_excel(tmp_path, index=False)

            # 测试读取应该抛出 ValueError
            with pytest.raises(ValueError) as exc_info:
                load_excel(tmp_path)

            assert "缺少必需的列" in str(exc_info.value)
            assert "QuantityIngredients" in str(exc_info.value)
            assert "costtime" in str(exc_info.value)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_load_excel_filter_empty_titles(self):
        """测试过滤 title 为空的行"""
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # 创建包含空 title 的测试数据
            data = {
                'title': ['山药小米粥', None, '', '  ', '西红柿炒蛋'],
                'steptext': ['步骤1', '步骤2', '步骤3', '步骤4', '步骤5'],
                'QuantityIngredients': ['山药50g', '小米100g', '银耳10g', '莲子20g', '西红柿2个'],
                'costtime': ['30分钟', '15分钟', '1小时', '45分钟', '20分钟']
            }
            df = pd.DataFrame(data)
            df.to_excel(tmp_path, index=False)

            # 测试读取
            result = load_excel(tmp_path)

            # 应该过滤掉空 title 的行，只保留 2 条
            assert len(result) == 2
            assert result['title'].tolist() == ['山药小米粥', '西红柿炒蛋']
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_load_excel_file_not_found(self):
        """测试文件不存在时抛出 FileNotFoundError"""
        with pytest.raises(FileNotFoundError) as exc_info:
            load_excel('nonexistent_file.xlsx')

        assert "不存在" in str(exc_info.value)

    def test_load_excel_invalid_file(self):
        """测试无效文件时抛出 ValueError"""
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # 写入无效内容（不是有效的 Excel 文件）
            with open(tmp_path, 'w') as f:
                f.write("This is not an Excel file")

            # 测试读取应该抛出 ValueError
            with pytest.raises(ValueError) as exc_info:
                load_excel(tmp_path)

            assert "读取 Excel 文件失败" in str(exc_info.value)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_load_excel_empty_file(self):
        """测试空文件（没有数据行）"""
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # 创建只有列名没有数据的 Excel 文件
            data = {
                'title': [],
                'steptext': [],
                'QuantityIngredients': [],
                'costtime': []
            }
            df = pd.DataFrame(data)
            df.to_excel(tmp_path, index=False)

            # 测试读取
            result = load_excel(tmp_path)

            # 应该返回空 DataFrame
            assert len(result) == 0
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_load_excel_extra_columns_allowed(self):
        """测试包含额外列的文件也能正常读取"""
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # 创建包含额外列的测试数据
            data = {
                'title': ['山药小米粥'],
                'steptext': ['步骤1'],
                'QuantityIngredients': ['山药50g'],
                'costtime': ['30分钟'],
                'extra_column': ['额外数据']  # 额外列
            }
            df = pd.DataFrame(data)
            df.to_excel(tmp_path, index=False)

            # 测试读取应该成功
            result = load_excel(tmp_path)

            # 应该包含所有列
            assert len(result) == 1
            assert 'extra_column' in result.columns
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
