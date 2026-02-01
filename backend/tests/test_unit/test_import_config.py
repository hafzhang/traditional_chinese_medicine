"""
Unit tests for recipe_import_config
测试导入配置和解析函数
"""

import pytest
from scripts.recipe_import_config import (
    EXCEL_COLUMN_MAP,
    DIFFICULTY_MAP,
    SOLAR_TERMS,
    SOLAR_TERMS_CN,
    SEASON_TO_SOLAR_TERMS,
    CONSTITUTION_CODES,
    parse_cooking_time,
    parse_difficulty,
    parse_json_field,
    parse_ingredients,
    parse_steps,
)


class TestImportConfigConstants:
    """测试常量定义"""

    def test_excel_column_map_exists(self):
        """测试 EXCEL_COLUMN_MAP 存在"""
        assert EXCEL_COLUMN_MAP is not None
        assert isinstance(EXCEL_COLUMN_MAP, dict)
        # 检查关键字段映射
        assert 'title' in EXCEL_COLUMN_MAP
        assert 'desc' in EXCEL_COLUMN_MAP
        assert 'costtime' in EXCEL_COLUMN_MAP
        assert 'difficulty' in EXCEL_COLUMN_MAP
        assert 'suitable_constitutions' in EXCEL_COLUMN_MAP
        assert 'efficacy_tags' in EXCEL_COLUMN_MAP
        assert 'solar_terms' in EXCEL_COLUMN_MAP

    def test_difficulty_map_exists(self):
        """测试 DIFFICULTY_MAP 存在且正确"""
        assert DIFFICULTY_MAP is not None
        assert isinstance(DIFFICULTY_MAP, dict)
        assert '简单' in DIFFICULTY_MAP
        assert '中等' in DIFFICULTY_MAP
        assert '较难' in DIFFICULTY_MAP
        assert '困难' in DIFFICULTY_MAP
        assert DIFFICULTY_MAP['简单'] == 'easy'
        assert DIFFICULTY_MAP['中等'] == 'medium'
        assert DIFFICULTY_MAP['较难'] == 'harder'
        assert DIFFICULTY_MAP['困难'] == 'hard'

    def test_solar_terms_24_items(self):
        """测试 24 节气列表"""
        assert SOLAR_TERMS is not None
        assert isinstance(SOLAR_TERMS, list)
        assert len(SOLAR_TERMS) == 24
        # 检查春季节气
        assert 'lichun' in SOLAR_TERMS
        assert 'yushui' in SOLAR_TERMS
        assert 'chunfen' in SOLAR_TERMS
        # 检查夏季节气
        assert 'lixia' in SOLAR_TERMS
        assert 'xiazhi' in SOLAR_TERMS
        # 检查秋季节气
        assert 'liqiu' in SOLAR_TERMS
        assert 'qiufen' in SOLAR_TERMS
        # 检查冬季节气
        assert 'lidong' in SOLAR_TERMS
        assert 'dongzhi' in SOLAR_TERMS

    def test_solar_terms_cn_exists(self):
        """测试中文节气名称列表"""
        assert SOLAR_TERMS_CN is not None
        assert isinstance(SOLAR_TERMS_CN, list)
        # 检查四季
        assert '春季' in SOLAR_TERMS_CN
        assert '夏季' in SOLAR_TERMS_CN
        assert '秋季' in SOLAR_TERMS_CN
        assert '冬季' in SOLAR_TERMS_CN
        # 检查节气
        assert '立春' in SOLAR_TERMS_CN
        assert '春分' in SOLAR_TERMS_CN
        assert '夏至' in SOLAR_TERMS_CN

    def test_season_to_solar_terms_mapping(self):
        """测试四季到节气映射"""
        assert SEASON_TO_SOLAR_TERMS is not None
        assert isinstance(SEASON_TO_SOLAR_TERMS, dict)
        assert 'spring' in SEASON_TO_SOLAR_TERMS
        assert 'summer' in SEASON_TO_SOLAR_TERMS
        assert 'autumn' in SEASON_TO_SOLAR_TERMS
        assert 'winter' in SEASON_TO_SOLAR_TERMS
        # 每个季节应该有 6 个节气
        assert len(SEASON_TO_SOLAR_TERMS['spring']) == 6
        assert len(SEASON_TO_SOLAR_TERMS['summer']) == 6
        assert len(SEASON_TO_SOLAR_TERMS['autumn']) == 6
        assert len(SEASON_TO_SOLAR_TERMS['winter']) == 6

    def test_constitution_codes(self):
        """测试体质代码列表"""
        assert CONSTITUTION_CODES is not None
        assert isinstance(CONSTITUTION_CODES, list)
        assert len(CONSTITUTION_CODES) == 9
        assert 'peace' in CONSTITUTION_CODES
        assert 'qi_deficiency' in CONSTITUTION_CODES
        assert 'yang_deficiency' in CONSTITUTION_CODES
        assert 'yin_deficiency' in CONSTITUTION_CODES
        assert 'phlegm_damp' in CONSTITUTION_CODES
        assert 'damp_heat' in CONSTITUTION_CODES
        assert 'blood_stasis' in CONSTITUTION_CODES
        assert 'qi_depression' in CONSTITUTION_CODES
        assert 'special' in CONSTITUTION_CODES


class TestParseCookingTime:
    """测试 parse_cooking_time 函数"""

    def test_parse_minutes(self):
        """测试解析分钟格式"""
        assert parse_cooking_time("30分钟") == 30
        assert parse_cooking_time("10分") == 10
        assert parse_cooking_time("60分种") == 60  # 错别字

    def test_parse_hours(self):
        """测试解析小时格式"""
        assert parse_cooking_time("1小时") == 60
        assert parse_cooking_time("1.5小时") == 90
        assert parse_cooking_time("2h") == 120

    def test_parse_range(self):
        """测试解析范围格式"""
        assert parse_cooking_time("10-30分钟") == 20  # (10+30)//2
        assert parse_cooking_time("10~30分钟") == 20
        assert parse_cooking_time("5-15分钟") == 10

    def test_parse_none_or_empty(self):
        """测试解析空值"""
        assert parse_cooking_time(None) == 30  # 默认30分钟
        assert parse_cooking_time("") == 30
        assert parse_cooking_time("未知") == 30  # 无法解析，返回默认值


class TestParseDifficulty:
    """测试 parse_difficulty 函数"""

    def test_parse_chinese_difficulty(self):
        """测试解析中文难度"""
        assert parse_difficulty("简单") == "easy"
        assert parse_difficulty("中等") == "medium"
        assert parse_difficulty("较难") == "harder"
        assert parse_difficulty("困难") == "hard"

    def test_parse_english_difficulty(self):
        """测试解析英文难度代码"""
        assert parse_difficulty("easy") == "easy"
        assert parse_difficulty("medium") == "medium"
        assert parse_difficulty("harder") == "harder"
        assert parse_difficulty("hard") == "hard"

    def test_parse_case_insensitive(self):
        """测试不区分大小写"""
        assert parse_difficulty("EASY") == "easy"
        assert parse_difficulty("Medium") == "medium"

    def test_parse_invalid_difficulty(self):
        """测试解析无效难度"""
        assert parse_difficulty("未知") is None
        assert parse_difficulty("") is None
        assert parse_difficulty(None) is None


class TestParseJsonField:
    """测试 parse_json_field 函数"""

    def test_parse_json_array(self):
        """测试解析 JSON 数组"""
        result = parse_json_field('["健脾", "养胃", "补气"]')
        assert result == ['健脾', '养胃', '补气']

    def test_parse_comma_separated(self):
        """测试解析逗号分隔"""
        assert parse_json_field("健脾,养胃,补气") == ['健脾', '养胃', '补气']
        assert parse_json_field("健脾，养胃，补气") == ['健脾', '养胃', '补气']

    def test_parse_chinese_pause_separated(self):
        """测试解析顿号分隔"""
        assert parse_json_field("健脾、养胃、补气") == ['健脾', '养胃', '补气']

    def test_parse_already_list(self):
        """测试已经是列表的输入"""
        assert parse_json_field(['健脾', '养胃']) == ['健脾', '养胃']
        assert parse_json_field(['健脾', None, '养胃', '']) == ['健脾', '养胃']

    def test_parse_none_or_empty(self):
        """测试解析空值"""
        assert parse_json_field(None) is None
        assert parse_json_field("") is None
        assert parse_json_field("   ") is None


class TestParseIngredients:
    """测试 parse_ingredients 函数"""

    def test_parse_simple_ingredients(self):
        """测试解析简单食材"""
        result = parse_ingredients("山药50g,小米100克")
        assert len(result) == 2
        assert result[0]['name'] == '山药'
        assert result[0]['amount'] == '50g'
        assert result[1]['name'] == '小米'
        assert result[1]['amount'] == '100克'

    def test_parse_ingredients_with_special_amount(self):
        """测试解析特殊用量的食材"""
        result = parse_ingredients("枸杞适量,红枣少许")
        assert len(result) >= 2
        # 查找枸杞和红枣
        huawei_items = [item for item in result if '枸杞' in item['name']]
        hongzao_items = [item for item in result if '红枣' in item['name']]
        assert len(huawei_items) > 0
        assert len(hongzao_items) > 0

    def test_parse_empty_ingredients(self):
        """测试解析空食材"""
        assert parse_ingredients(None) == []
        assert parse_ingredients("") == []

    def test_parse_ingredients_structure(self):
        """测试解析食材结构"""
        result = parse_ingredients("山药50g")
        assert len(result) == 1
        assert 'name' in result[0]
        assert 'amount' in result[0]
        assert 'is_main' in result[0]
        assert 'display_order' in result[0]
        assert result[0]['display_order'] == 0


class TestParseSteps:
    """测试 parse_steps 函数"""

    def test_parse_numbered_steps(self):
        """测试解析带编号的步骤"""
        result = parse_steps("1.准备食材\n2.开始烹饪\n3.完成")
        assert len(result) == 3
        assert result[0]['step_number'] == 1
        assert result[0]['description'] == '准备食材'
        assert result[1]['step_number'] == 2
        assert result[2]['step_number'] == 3

    def test_parse_steps_with_chinese_period(self):
        """测试解析中文顿号分隔的步骤"""
        result = parse_steps("1、准备食材\n2、开始烹饪")
        assert len(result) == 2
        assert result[0]['step_number'] == 1
        assert result[1]['step_number'] == 2

    def test_parse_steps_with_hash(self):
        """测试解析 # 分隔的步骤"""
        result = parse_steps("1.准备食材#2.开始烹饪")
        assert len(result) == 2

    def test_parse_empty_steps(self):
        """测试解析空步骤"""
        assert parse_steps(None) == []
        assert parse_steps("") == []

    def test_parse_steps_structure(self):
        """测试解析步骤结构"""
        result = parse_steps("1.准备食材")
        assert len(result) == 1
        assert 'step_number' in result[0]
        assert 'description' in result[0]
        assert 'duration' in result[0]
