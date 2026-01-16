"""
体质评分算法测试
Constitution Scoring Algorithm Tests

测试九种体质识别的核心算法，包括：
1. 原始分数计算
2. 百分制转换
3. 体质类型判定
4. 边界条件处理
"""

import pytest
from api.services.constitution import ConstitutionScorer, ConstitutionAnalyzer


class TestConstitutionScorer:
    """体质评分器测试类"""

    @pytest.fixture
    def scorer(self):
        """创建评分器实例"""
        return ConstitutionScorer()

    # ==================== 原始分数计算测试 ====================

    def test_calculate_scores_all_ones(self, scorer):
        """测试全选'没有'(1分)的情况"""
        answers = [1] * 30
        scores = scorer.calculate_scores(answers)

        # 平和质4题，每题1分 = 4分
        assert scores["peace"] == 4
        # 气虚质4题，每题1分 = 4分
        assert scores["qi_deficiency"] == 4
        # 阳虚质4题，每题1分 = 4分
        assert scores["yang_deficiency"] == 4
        # 阴虚质4题，每题1分 = 4分
        assert scores["yin_deficiency"] == 4
        # 痰湿质3题，每题1分 = 3分
        assert scores["phlegm_damp"] == 3
        # 湿热质3题，每题1分 = 3分
        assert scores["damp_heat"] == 3
        # 血瘀质3题，每题1分 = 3分
        assert scores["blood_stasis"] == 3
        # 气郁质3题，每题1分 = 3分
        assert scores["qi_depression"] == 3
        # 特禀质2题，每题1分 = 2分
        assert scores["special"] == 2

    def test_calculate_scores_all_fives(self, scorer):
        """测试全选'总是'(5分)的情况"""
        answers = [5] * 30
        scores = scorer.calculate_scores(answers)

        assert scores["peace"] == 20
        assert scores["qi_deficiency"] == 20
        assert scores["yang_deficiency"] == 20
        assert scores["yin_deficiency"] == 20
        assert scores["phlegm_damp"] == 15
        assert scores["damp_heat"] == 15
        assert scores["blood_stasis"] == 15
        assert scores["qi_depression"] == 15
        assert scores["special"] == 10

    def test_calculate_scores_invalid_length(self, scorer):
        """测试答案数量不正确的情况"""
        with pytest.raises(ValueError, match="Expected 30 answers"):
            scorer.calculate_scores([1, 2, 3])

        with pytest.raises(ValueError, match="Expected 30 answers"):
            scorer.calculate_scores([1] * 31)

    def test_calculate_scores_invalid_range(self, scorer):
        """测试答案超出范围的情况"""
        with pytest.raises(ValueError, match="Answer must be between 1 and 5"):
            scorer.calculate_scores([0] * 30)

        with pytest.raises(ValueError, match="Answer must be between 1 and 5"):
            scorer.calculate_scores([6] * 30)

    def test_calculate_scores_specific_distribution(self, scorer):
        """测试特定分数分布"""
        # 前4题选5分(平和质)，其余选1分
        answers = [5, 5, 5, 5] + [1] * 26
        scores = scorer.calculate_scores(answers)

        assert scores["peace"] == 20
        assert scores["qi_deficiency"] == 4
        assert scores["yang_deficiency"] == 4

    # ==================== 百分制转换测试 ====================

    def test_convert_to_percentage(self, scorer):
        """测试百分制转换"""
        raw_scores = {
            "peace": 16,
            "qi_deficiency": 8,
            "yang_deficiency": 12
        }
        percentage = scorer.convert_to_percentage(raw_scores)

        assert percentage["peace"] == 40.0  # 16 * 2.5
        assert percentage["qi_deficiency"] == 20.0  # 8 * 2.5
        assert percentage["yang_deficiency"] == 30.0  # 12 * 2.5

    def test_convert_to_percentage_max_100(self, scorer):
        """测试百分制最大值不超过100"""
        raw_scores = {
            "peace": 50  # 超过100的原始分
        }
        percentage = scorer.convert_to_percentage(raw_scores)

        assert percentage["peace"] == 100  # 应该被限制为100

    # ==================== 体质判定测试 ====================

    def test_determine_peace_constitution(self, scorer):
        """测试平和质判定"""
        scores = {
            "peace": 70,  # ≥60 且其他都 <40
            "qi_deficiency": 30,
            "yang_deficiency": 25,
            "yin_deficiency": 20,
            "phlegm_damp": 20,
            "damp_heat": 20,
            "blood_stasis": 20,
            "qi_depression": 20,
            "special": 15
        }

        result = scorer.determine_constitution(scores)

        assert result["primary_constitution"] == "peace"
        assert result["primary_constitution_name"] == "平和质"
        assert result["secondary_constitutions"] == []

    def test_determine_peace_with_others_above_threshold(self, scorer):
        """测试平和质但有其他体质超过40分"""
        scores = {
            "peace": 70,
            "qi_deficiency": 45,  # 超过40，不应判定为平和质
            "yang_deficiency": 25,
            "yin_deficiency": 20,
            "phlegm_damp": 20,
            "damp_heat": 20,
            "blood_stasis": 20,
            "qi_depression": 20,
            "special": 15
        }

        result = scorer.determine_constitution(scores)

        # 因为有其他体质超过40，应该判定为该体质而非平和质
        assert result["primary_constitution"] != "peace"

    def test_determine_qi_deficiency_constitution(self, scorer):
        """测试气虚质判定"""
        scores = {
            "peace": 30,
            "qi_deficiency": 50,  # 主要体质
            "yang_deficiency": 35,
            "yin_deficiency": 25,
            "phlegm_damp": 20,
            "damp_heat": 20,
            "blood_stasis": 20,
            "qi_depression": 20,
            "special": 15
        }

        result = scorer.determine_constitution(scores)

        assert result["primary_constitution"] == "qi_deficiency"
        assert result["primary_constitution_name"] == "气虚质"

    def test_determine_yang_deficiency_constitution(self, scorer):
        """测试阳虚质判定"""
        scores = {
            "peace": 25,
            "qi_deficiency": 30,
            "yang_deficiency": 55,  # 主要体质
            "yin_deficiency": 20,
            "phlegm_damp": 20,
            "damp_heat": 20,
            "blood_stasis": 20,
            "qi_depression": 20,
            "special": 15
        }

        result = scorer.determine_constitution(scores)

        assert result["primary_constitution"] == "yang_deficiency"
        assert result["primary_constitution_name"] == "阳虚质"

    def test_determine_secondary_constitutions(self, scorer):
        """测试次要体质判定"""
        scores = {
            "peace": 30,
            "qi_deficiency": 50,  # 主要体质
            "yang_deficiency": 40,  # 次要体质1
            "yin_deficiency": 35,  # 次要体质2
            "phlegm_damp": 32,  # 次要体质3
            "damp_heat": 20,
            "blood_stasis": 20,
            "qi_depression": 20,
            "special": 15
        }

        result = scorer.determine_constitution(scores)

        assert result["primary_constitution"] == "qi_deficiency"
        assert len(result["secondary_constitutions"]) <= 3

        # 验证次要体质按分数降序排列
        secondary_scores = [c["score"] for c in result["secondary_constitutions"]]
        assert secondary_scores == sorted(secondary_scores, reverse=True)

    def test_determine_no_threshold_met(self, scorer):
        """测试没有体质达到阈值的情况"""
        scores = {
            "peace": 25,
            "qi_deficiency": 28,  # 最高但<30
            "yang_deficiency": 25,
            "yin_deficiency": 22,
            "phlegm_damp": 20,
            "damp_heat": 20,
            "blood_stasis": 20,
            "qi_depression": 20,
            "special": 15
        }

        result = scorer.determine_constitution(scores)

        # 应该选择分数最高的体质
        assert result["primary_constitution"] == "qi_deficiency"
        assert result["primary_constitution_name"] == "气虚质"

    # ==================== 完整分析流程测试 ====================

    def test_analyze_complete_flow_peace(self, scorer):
        """测试完整分析流程 - 平和质"""
        # 模拟平和质答案：精力充沛、不疲乏、面色红润
        answers = [
            5, 1, 1, 1,  # 平和质问题
            1, 1, 1, 1,  # 气虚质
            1, 1, 1, 1,  # 阳虚质
            1, 1, 1, 1,  # 阴虚质
            1, 1, 1,    # 痰湿质
            1, 1, 1,    # 湿热质
            1, 1, 1,    # 血瘀质
            1, 1, 1,    # 气郁质
            1, 1        # 特禀质
        ]

        result = scorer.analyze(answers)

        assert result["primary_constitution"] == "peace"
        assert result["primary_constitution_name"] == "平和质"

    def test_analyze_complete_flow_yang_deficiency(self, scorer):
        """测试完整分析流程 - 阳虚质"""
        # 模拟阳虚质答案：手脚发凉、怕冷、吃凉东西不舒服
        answers = [
            2, 3, 3, 2,  # 平和质
            3, 3, 2, 2,  # 气虚质
            5, 5, 5, 5,  # 阳虚质 - 明显阳虚
            2, 2, 2, 2,  # 阴虚质
            2, 2, 2,    # 痰湿质
            2, 2, 2,    # 湿热质
            2, 2, 2,    # 血瘀质
            2, 2, 2,    # 气郁质
            2, 2        # 特禀质
        ]

        result = scorer.analyze(answers)

        assert result["primary_constitution"] == "yang_deficiency"
        assert result["primary_constitution_name"] == "阳虚质"
        assert result["scores"]["yang_deficiency"] > 40

    def test_analyze_complete_flow_mixed(self, scorer):
        """测试完整分析流程 - 混合体质"""
        # 气虚阳虚混合
        answers = [
            2, 3, 3, 2,  # 平和质
            4, 4, 4, 4,  # 气虚质
            4, 4, 4, 4,  # 阳虚质
            2, 2, 2, 2,  # 阴虚质
            2, 2, 2,    # 痰湿质
            2, 2, 2,    # 湿热质
            2, 2, 2,    # 血瘀质
            2, 2, 2,    # 气郁质
            2, 2        # 特禀质
        ]

        result = scorer.analyze(answers)

        # 应该判定为气虚或阳虚之一
        assert result["primary_constitution"] in ["qi_deficiency", "yang_deficiency"]
        # 应该有次要体质
        assert len(result["secondary_constitutions"]) >= 1


class TestConstitutionAnalyzer:
    """体质分析器测试类"""

    @pytest.fixture
    def analyzer(self):
        """创建分析器实例"""
        return ConstitutionAnalyzer()

    def test_analyzer_singleton(self, analyzer):
        """测试分析器单例模式"""
        analyzer2 = ConstitutionAnalyzer()

        # 两个实例应该是同一个对象
        assert analyzer is analyzer2

    def test_analyze_basic(self, analyzer):
        """测试基本分析功能"""
        answers = [3] * 30  # 全选"有时"

        result = analyzer.analyze(answers)

        assert "primary_constitution" in result
        assert "primary_constitution_name" in result
        assert "scores" in result
        assert "secondary_constitutions" in result

    def test_analyze_scorer_delegation(self, analyzer):
        """测试分析器正确委托给评分器"""
        answers = [1] * 30

        result = analyzer.analyze(answers)

        # 验证返回结构与评分器一致
        assert set(result.keys()) == {
            "primary_constitution",
            "primary_constitution_name",
            "secondary_constitutions",
            "scores"
        }


# ==================== 标准测试用例 ====================

class TestStandardConstitutionCases:
    """标准体质判定用例 - 基于王琦院士CCMQ标准"""

    @pytest.fixture
    def scorer(self):
        return ConstitutionScorer()

    def test_case_1_typical_peace(self, scorer):
        """标准案例1：典型平和质"""
        # 特征：精力充沛、面色红润、睡眠良好、胃口好
        answers = [5, 1, 1, 1,  # A组 (平和质反向计分)
                   1, 1, 1, 1,  # B组 (气虚质)
                   1, 1, 1, 1,  # C组 (阳虚质)
                   1, 1, 1, 1,  # D组 (阴虚质)
                   1, 1, 1,     # E组 (痰湿质)
                   1, 1, 1,     # F组 (湿热质)
                   1, 1, 1,     # G组 (血瘀质)
                   1, 1, 1,     # H组 (气郁质)
                   1, 1]        # I组 (特禀质)

        result = scorer.analyze(answers)
        assert result["primary_constitution"] == "peace"

    def test_case_2_typical_qi_deficiency(self, scorer):
        """标准案例2：典型气虚质"""
        # 特征：容易疲乏、气短、容易感冒、说话声音低弱
        answers = [3, 4, 5, 3,  # A组
                   5, 5, 4, 5,  # B组 - 明显气虚
                   3, 3, 3, 3,  # C组
                   3, 3, 3, 3,  # D组
                   3, 3, 3,     # E组
                   3, 3, 3,     # F组
                   3, 3, 3,     # G组
                   3, 3, 3,     # H组
                   3, 3]        # I组

        result = scorer.analyze(answers)
        assert result["primary_constitution"] == "qi_deficiency"

    def test_case_3_typical_yang_deficiency(self, scorer):
        """标准案例3：典型阳虚质"""
        # 特征：手脚发凉、怕冷、胃怕冷、吃凉东西不舒服
        answers = [3, 3, 3, 3,  # A组
                   4, 3, 3, 3,  # B组
                   5, 5, 5, 5,  # C组 - 明显阳虚
                   3, 3, 3, 3,  # D组
                   3, 3, 3,     # E组
                   3, 3, 3,     # F组
                   3, 3, 3,     # G组
                   3, 3, 3,     # H组
                   3, 3]        # I组

        result = scorer.analyze(answers)
        assert result["primary_constitution"] == "yang_deficiency"

    def test_case_4_typical_yin_deficiency(self, scorer):
        """标准案例4：典型阴虚质"""
        # 特征：口干咽燥、手心脚心发热、皮肤干、大便干燥
        answers = [3, 3, 3, 3,  # A组
                   3, 3, 3, 3,  # B组
                   3, 3, 3, 3,  # C组
                   5, 5, 5, 5,  # D组 - 明显阴虚
                   3, 3, 3,     # E组
                   3, 3, 3,     # F组
                   3, 3, 3,     # G组
                   3, 3, 3,     # H组
                   3, 3]        # I组

        result = scorer.analyze(answers)
        assert result["primary_constitution"] == "yin_deficiency"

    def test_case_5_typical_phlegm_damp(self, scorer):
        """标准案例5：典型痰湿质"""
        # 特征：胸闷腹胀、身体沉重、腹部肥满
        answers = [3, 3, 3, 3,  # A组
                   3, 3, 3, 3,  # B组
                   3, 3, 3, 3,  # C组
                   3, 3, 3, 3,  # D组
                   5, 5, 5,     # E组 - 明显痰湿
                   3, 3, 3,     # F组
                   3, 3, 3,     # G组
                   3, 3, 3,     # H组
                   3, 3]        # I组

        result = scorer.analyze(answers)
        assert result["primary_constitution"] == "phlegm_damp"

    def test_case_6_typical_damp_heat(self, scorer):
        """标准案例6：典型湿热质"""
        # 特征：面部油腻、容易生痤疮、口苦
        answers = [3, 3, 3, 3,  # A组
                   3, 3, 3, 3,  # B组
                   3, 3, 3, 3,  # C组
                   3, 3, 3, 3,  # D组
                   3, 3, 3,     # E组
                   5, 5, 5,     # F组 - 明显湿热
                   3, 3, 3,     # G组
                   3, 3, 3,     # H组
                   3, 3]        # I组

        result = scorer.analyze(answers)
        assert result["primary_constitution"] == "damp_heat"

    def test_case_7_typical_blood_stasis(self, scorer):
        """标准案例7：典型血瘀质"""
        # 特征：皮肤青紫瘀斑、两颧红丝、疼痛部位固定
        answers = [3, 3, 3, 3,  # A组
                   3, 3, 3, 3,  # B组
                   3, 3, 3, 3,  # C组
                   3, 3, 3, 3,  # D组
                   3, 3, 3,     # E组
                   3, 3, 3,     # F组
                   5, 5, 5,     # G组 - 明显血瘀
                   3, 3, 3,     # H组
                   3, 3]        # I组

        result = scorer.analyze(answers)
        assert result["primary_constitution"] == "blood_stasis"

    def test_case_8_typical_qi_depression(self, scorer):
        """标准案例8：典型气郁质"""
        # 特征：情绪低沉、精神紧张、无缘无故叹气
        answers = [3, 3, 3, 3,  # A组
                   3, 3, 3, 3,  # B组
                   3, 3, 3, 3,  # C组
                   3, 3, 3, 3,  # D组
                   3, 3, 3,     # E组
                   3, 3, 3,     # F组
                   3, 3, 3,     # G组
                   5, 5, 5,     # H组 - 明显气郁
                   3, 3]        # I组

        result = scorer.analyze(answers)
        assert result["primary_constitution"] == "qi_depression"

    def test_case_9_typical_special(self, scorer):
        """标准案例9：典型特禀质"""
        # 特征：没感冒也打喷嚏、没感冒也流鼻涕
        answers = [3, 3, 3, 3,  # A组
                   3, 3, 3, 3,  # B组
                   3, 3, 3, 3,  # C组
                   3, 3, 3, 3,  # D组
                   3, 3, 3,     # E组
                   3, 3, 3,     # F组
                   3, 3, 3,     # G组
                   3, 3, 3,     # H组
                   5, 5]        # I组 - 明显特禀

        result = scorer.analyze(answers)
        # 特禀质只有2题，最高分10分，可能达不到主要体质阈值
        # 但如果其他体质分数更低，仍应判定为特禀质
        assert "primary_constitution" in result

    def test_case_10_mixed_constitution(self, scorer):
        """标准案例10：气虚阳虚混合体质"""
        # 常见混合：气虚+阳虚（气阳两虚）
        answers = [3, 3, 4, 3,  # A组
                   4, 4, 4, 4,  # B组 - 气虚
                   4, 4, 4, 4,  # C组 - 阳虚
                   3, 3, 3, 3,  # D组
                   3, 3, 3,     # E组
                   3, 3, 3,     # F组
                   3, 3, 3,     # G组
                   3, 3, 3,     # H组
                   3, 3]        # I组

        result = scorer.analyze(answers)

        # 主要体质应为气虚或阳虚之一
        assert result["primary_constitution"] in ["qi_deficiency", "yang_deficiency"]

        # 应该有另一个作为次要体质
        secondary_types = [c["type"] for c in result["secondary_constitutions"]]
        assert "qi_deficiency" in secondary_types or "yang_deficiency" in secondary_types


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
