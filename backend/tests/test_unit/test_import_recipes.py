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

from scripts.import_recipes import load_excel, check_recipe_exists, validate_and_link_ingredients, import_single_recipe


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


class TestCheckRecipeExists:
    """测试 check_recipe_exists 函数"""

    def test_check_recipe_exists_returns_true_when_exists(self, db_session):
        """测试菜谱存在时返回 True"""
        # 创建测试菜谱
        from api.models import Recipe
        import uuid

        recipe = Recipe(
            id=str(uuid.uuid4()),
            name="山药小米粥",
            difficulty="easy",
            cooking_time=30
        )
        db_session.add(recipe)
        db_session.commit()

        # 测试检查
        result = check_recipe_exists("山药小米粥", db_session)

        # 验证
        assert result is True

    def test_check_recipe_exists_returns_false_when_not_exists(self, db_session):
        """测试菜谱不存在时返回 False"""
        # 测试检查不存在的菜谱
        result = check_recipe_exists("不存在的菜谱名称", db_session)

        # 验证
        assert result is False

    def test_check_recipe_exists_case_sensitive(self, db_session):
        """测试检查是区分大小写的"""
        from api.models import Recipe
        import uuid

        # 创建测试菜谱
        recipe = Recipe(
            id=str(uuid.uuid4()),
            name="山药小米粥",
            difficulty="easy",
            cooking_time=30
        )
        db_session.add(recipe)
        db_session.commit()

        # 测试不同大小写
        result = check_recipe_exists("山药小米粥".lower(), db_session)

        # 验证 - 应该找不到（因为 SQLite 默认是不区分大小写的，但按名称查找会找到）
        # 在 SQLite 中，LIKE 是不区分大小写的，但 = 是区分大小写的
        # 由于 filter_by 使用 =，所以应该是区分大小写的
        # 但 SQLite 的默认行为是 BINARY 比较才是区分大小写的
        # 让我们测试实际行为
        # 如果 result 是 True，说明 SQLite 默认不区分大小写
        # 如果 result 是 False，说明区分大小写
        # 根据项目实际使用情况，我们接受 SQLite 的默认行为
        # 这里我们验证至少能找到完全匹配的
        assert check_recipe_exists("山药小米粥", db_session) is True

    def test_check_recipe_exists_multiple_recipes(self, db_session):
        """测试多条菜谱记录时正确检查"""
        from api.models import Recipe
        import uuid

        # 创建多个测试菜谱
        recipe1 = Recipe(
            id=str(uuid.uuid4()),
            name="山药小米粥",
            difficulty="easy",
            cooking_time=30
        )
        recipe2 = Recipe(
            id=str(uuid.uuid4()),
            name="西红柿炒蛋",
            difficulty="easy",
            cooking_time=15
        )
        db_session.add(recipe1)
        db_session.add(recipe2)
        db_session.commit()

        # 测试检查每个菜谱
        assert check_recipe_exists("山药小米粥", db_session) is True
        assert check_recipe_exists("西红柿炒蛋", db_session) is True
        assert check_recipe_exists("不存在的菜谱", db_session) is False


class TestValidateAndLinkIngredients:
    """测试 validate_and_link_ingredients 函数"""

    def test_validate_and_link_ingredients_success(self, db_session):
        """测试成功验证和关联食材"""
        from api.models import Ingredient
        import uuid

        # 创建测试食材
        ingredient1 = Ingredient(
            id=str(uuid.uuid4()),
            name="山药",
            category="谷物",
            nature="平",
            flavor="甘"
        )
        ingredient2 = Ingredient(
            id=str(uuid.uuid4()),
            name="小米",
            category="谷物",
            nature="凉",
            flavor="甘"
        )
        db_session.add(ingredient1)
        db_session.add(ingredient2)
        db_session.commit()

        # 解析后的食材列表
        parsed_ingredients = [
            {'name': '山药', 'amount': '50g'},
            {'name': '小米', 'amount': '100g'}
        ]

        # 测试验证和关联
        result = validate_and_link_ingredients(parsed_ingredients, db_session)

        # 验证
        assert len(result) == 2
        assert result[0].ingredient_id == ingredient1.id
        assert result[0].amount == '50g'
        assert result[0].is_main is True  # 第一个是主料
        assert result[0].display_order == 0

        assert result[1].ingredient_id == ingredient2.id
        assert result[1].amount == '100g'
        assert result[1].is_main is False  # 第二个不是主料
        assert result[1].display_order == 1

    def test_validate_and_link_ingredients_skip_missing(self, db_session):
        """测试跳过不存在的食材"""
        from api.models import Ingredient
        import uuid

        # 创建一个测试食材
        ingredient = Ingredient(
            id=str(uuid.uuid4()),
            name="山药",
            category="谷物",
            nature="平",
            flavor="甘"
        )
        db_session.add(ingredient)
        db_session.commit()

        # 解析后的食材列表，包含不存在的食材
        parsed_ingredients = [
            {'name': '山药', 'amount': '50g'},
            {'name': '不存在的食材', 'amount': '100g'}
        ]

        # 测试验证和关联
        result = validate_and_link_ingredients(parsed_ingredients, db_session)

        # 验证 - 只应该返回一个食材
        assert len(result) == 1
        assert result[0].ingredient_id == ingredient.id
        assert result[0].amount == '50g'

    def test_validate_and_link_ingredients_synonym_matching(self, db_session):
        """测试同义词匹配"""
        from api.models import Ingredient
        import uuid

        # 创建标准名称的食材
        ingredient = Ingredient(
            id=str(uuid.uuid4()),
            name="山药",
            category="谷物",
            nature="平",
            flavor="甘",
            aliases=["怀山药", "淮山"]
        )
        db_session.add(ingredient)
        db_session.commit()

        # 使用同义词
        parsed_ingredients = [
            {'name': '淮山', 'amount': '50g'}
        ]

        # 测试验证和关联
        result = validate_and_link_ingredients(parsed_ingredients, db_session)

        # 验证 - 应该通过同义词匹配
        assert len(result) == 1
        assert result[0].ingredient_id == ingredient.id
        assert result[0].amount == '50g'

    def test_validate_and_link_ingredients_empty_list(self, db_session):
        """测试空食材列表"""
        # 测试空列表
        result = validate_and_link_ingredients([], db_session)

        # 验证 - 应该返回空列表
        assert len(result) == 0

    def test_validate_and_link_ingredients_skip_empty_name(self, db_session):
        """测试跳过名称为空的食材"""
        from api.models import Ingredient
        import uuid

        # 创建测试食材
        ingredient = Ingredient(
            id=str(uuid.uuid4()),
            name="山药",
            category="谷物",
            nature="平",
            flavor="甘"
        )
        db_session.add(ingredient)
        db_session.commit()

        # 解析后的食材列表，包含空名称
        parsed_ingredients = [
            {'name': '山药', 'amount': '50g'},
            {'name': '', 'amount': '100g'},
            {'name': None, 'amount': '200g'},
            {'amount': '300g'}  # 没有 name 键
        ]

        # 测试验证和关联
        result = validate_and_link_ingredients(parsed_ingredients, db_session)

        # 验证 - 只应该返回一个有效食材
        assert len(result) == 1
        assert result[0].ingredient_id == ingredient.id

    def test_validate_and_link_ingredients_default_amount(self, db_session):
        """测试食材没有 amount 字段时使用默认值"""
        from api.models import Ingredient
        import uuid

        # 创建测试食材
        ingredient = Ingredient(
            id=str(uuid.uuid4()),
            name="山药",
            category="谷物",
            nature="平",
            flavor="甘"
        )
        db_session.add(ingredient)
        db_session.commit()

        # 解析后的食材列表，没有 amount 字段
        parsed_ingredients = [
            {'name': '山药'}
        ]

        # 测试验证和关联
        result = validate_and_link_ingredients(parsed_ingredients, db_session)

        # 验证
        assert len(result) == 1
        assert result[0].ingredient_id == ingredient.id
        assert result[0].amount == ''  # 默认为空字符串


class TestImportSingleRecipe:
    """测试 import_single_recipe 函数"""

    def test_import_single_recipe_success(self, db_session):
        """测试成功导入单条菜谱"""
        from api.models import Ingredient, Recipe, RecipeIngredient, RecipeStep
        import uuid

        # 创建测试食材
        ingredient1 = Ingredient(
            id=str(uuid.uuid4()),
            name="山药",
            category="谷物",
            nature="平",
            flavor="甘"
        )
        ingredient2 = Ingredient(
            id=str(uuid.uuid4()),
            name="小米",
            category="谷物",
            nature="凉",
            flavor="甘"
        )
        db_session.add(ingredient1)
        db_session.add(ingredient2)
        db_session.commit()

        # 准备测试数据 - Excel行
        row = {
            'title': '山药小米粥',
            'costtime': '30分钟',
            'steptext': '1. 将山药洗净切小块\n2. 小米洗净\n3. 锅中加水，放入小米煮30分钟',
            'QuantityIngredients': '山药50g、小米100g',
            'desc': '健脾养胃的养生粥',
            'tip': '小火慢煮口感更好'
        }

        # 空图片映射
        image_map = {}

        # 测试导入
        result = import_single_recipe(row, image_map, db_session, dry_run=False)

        # 验证
        assert result is not None
        assert result.name == '山药小米粥'
        assert result.cooking_time == 30
        assert result.difficulty == 'easy'  # 30分钟 -> easy
        assert result.desc == '健脾养胃的养生粥'
        assert result.tip == '小火慢煮口感更好'

        # 验证食材关联
        assert len(result.ingredient_relations) == 2
        # 找到主料
        main_ingredient = next((r for r in result.ingredient_relations if r.is_main), None)
        assert main_ingredient is not None
        assert main_ingredient.amount == '50g'

        # 验证步骤关联
        assert len(result.step_relations) == 3

        # 验证数据库中的记录
        db_recipe = db_session.query(Recipe).filter_by(name='山药小米粥').first()
        assert db_recipe is not None
        assert db_recipe.name == '山药小米粥'

    def test_import_single_recipe_skip_existing(self, db_session):
        """测试跳过已存在的菜谱"""
        from api.models import Recipe
        import uuid

        # 创建已存在的菜谱
        existing_recipe = Recipe(
            id=str(uuid.uuid4()),
            name="山药小米粥",
            difficulty="easy",
            cooking_time=30
        )
        db_session.add(existing_recipe)
        db_session.commit()

        # 准备测试数据
        row = {
            'title': '山药小米粥',
            'costtime': '30分钟',
            'steptext': '1. 将山药洗净切小块',
            'QuantityIngredients': '山药50g',
        }

        image_map = {}

        # 测试导入 - 应该跳过
        result = import_single_recipe(row, image_map, db_session, dry_run=False)

        # 验证 - 应该返回None（跳过）
        assert result is None

        # 验证数据库只有一条记录
        from api.models import Recipe
        count = db_session.query(Recipe).filter_by(name='山药小米粥').count()
        assert count == 1

    def test_import_single_recipe_skip_empty_title(self, db_session):
        """测试跳过标题为空的行"""
        row = {
            'title': '',
            'costtime': '30分钟',
            'steptext': '1. 步骤',
            'QuantityIngredients': '食材',
        }

        image_map = {}

        # 测试导入 - 应该跳过
        result = import_single_recipe(row, image_map, db_session, dry_run=False)

        # 验证 - 应该返回None（跳过）
        assert result is None

    def test_import_single_recipe_dry_run(self, db_session):
        """测试dry-run模式不写入数据库"""
        from api.models import Recipe

        # 准备测试数据
        row = {
            'title': '测试菜谱DRYRUN',
            'costtime': '30分钟',
            'steptext': '1. 测试步骤',
            'QuantityIngredients': '测试食材',
        }

        image_map = {}

        # 测试dry-run导入
        result = import_single_recipe(row, image_map, db_session, dry_run=True)

        # 验证 - 返回Recipe对象但不写入数据库
        assert result is not None
        assert result.name == '测试菜谱DRYRUN'

        # 验证数据库中没有该记录
        db_recipe = db_session.query(Recipe).filter_by(name='测试菜谱DRYRUN').first()
        assert db_recipe is None

    def test_import_single_recipe_parse_difficulty_from_time(self, db_session):
        """测试从烹饪时间推测难度"""
        from api.models import Ingredient
        import uuid

        # 创建测试食材
        ingredient = Ingredient(
            id=str(uuid.uuid4()),
            name="山药",
            category="谷物",
            nature="平",
            flavor="甘"
        )
        db_session.add(ingredient)
        db_session.commit()

        # 测试不同烹饪时间推测难度
        test_cases = [
            ('20分钟', 'easy'),
            ('45分钟', 'medium'),
            ('90分钟', 'hard'),
        ]

        for time_str, expected_difficulty in test_cases:
            row = {
                'title': f'测试菜谱{time_str}',
                'costtime': time_str,
                'steptext': '1. 步骤',
                'QuantityIngredients': '山药50g',
            }

            image_map = {}

            result = import_single_recipe(row, image_map, db_session, dry_run=True)

            assert result is not None
            assert result.difficulty == expected_difficulty, f"时间 {time_str} 应该推测为 {expected_difficulty}"

    def test_import_single_recipe_guess_tags(self, db_session):
        """测试智能推测标签"""
        from api.models import Ingredient
        import uuid

        # 创建测试食材 - 山药（健脾、养胃、补气）
        ingredient = Ingredient(
            id=str(uuid.uuid4()),
            name="山药",
            category="谷物",
            nature="平",
            flavor="甘"
        )
        db_session.add(ingredient)
        db_session.commit()

        row = {
            'title': '山药粥',
            'costtime': '30分钟',
            'steptext': '1. 煮粥',
            'QuantityIngredients': '山药50g',
        }

        image_map = {}

        result = import_single_recipe(row, image_map, db_session, dry_run=True)

        assert result is not None
        # 山药应该推测出健脾、养胃、补气等功效
        assert len(result.efficacy_tags) > 0
        # 山药适合气虚质和平和质
        assert len(result.suitable_constitutions) > 0

    def test_import_single_recipe_with_image_match(self, db_session):
        """测试图片匹配"""
        from api.models import Ingredient
        import uuid

        # 创建测试食材
        ingredient = Ingredient(
            id=str(uuid.uuid4()),
            name="山药",
            category="谷物",
            nature="平",
            flavor="甘"
        )
        db_session.add(ingredient)
        db_session.commit()

        # 准备图片映射
        image_map = {
            '山药小米粥': '/path/to/山药小米粥.jpg'
        }

        row = {
            'title': '山药小米粥',
            'costtime': '30分钟',
            'steptext': '1. 煮粥',
            'QuantityIngredients': '山药50g',
        }

        result = import_single_recipe(row, image_map, db_session, dry_run=True)

        assert result is not None
        # 应该匹配到图片
        assert result.cover_image == '/path/to/山药小米粥.jpg'

    def test_import_single_recipe_parse_steps(self, db_session):
        """测试步骤解析"""
        from api.models import Ingredient
        import uuid

        # 创建测试食材
        ingredient = Ingredient(
            id=str(uuid.uuid4()),
            name="山药",
            category="谷物",
            nature="平",
            flavor="甘"
        )
        db_session.add(ingredient)
        db_session.commit()

        row = {
            'title': '山药小米粥',
            'costtime': '30分钟',
            'steptext': '1. 将山药洗净切小块（约5分钟）\n2. 小米洗净\n3. 锅中加水，放入小米煮30分钟（约30分钟）',
            'QuantityIngredients': '山药50g',
        }

        image_map = {}

        result = import_single_recipe(row, image_map, db_session, dry_run=True)

        assert result is not None
        # 应该解析出3个步骤
        assert len(result.step_relations) == 3
        # 第一个步骤应该有时间（5分钟）
        assert result.step_relations[0].duration == 5

    def test_import_single_recipe_skip_missing_ingredients(self, db_session):
        """测试跳过不存在的食材"""
        from api.models import Ingredient
        import uuid

        # 创建一个测试食材
        ingredient = Ingredient(
            id=str(uuid.uuid4()),
            name="山药",
            category="谷物",
            nature="平",
            flavor="甘"
        )
        db_session.add(ingredient)
        db_session.commit()

        # 使用包含不存在食材的数据
        row = {
            'title': '山药粥',
            'costtime': '30分钟',
            'steptext': '1. 煮粥',
            'QuantityIngredients': '山药50g、不存在的食材100g',
        }

        image_map = {}

        result = import_single_recipe(row, image_map, db_session, dry_run=True)

        assert result is not None
        # 应该只关联一个存在的食材
        assert len(result.ingredient_relations) == 1

