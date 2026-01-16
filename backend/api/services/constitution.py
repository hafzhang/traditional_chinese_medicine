"""
Constitution Analysis Service
体质分析服务 - 核心业务逻辑
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from api.config import settings


class ConstitutionScorer:
    """体质评分计算器"""

    SCORE_CONVERT_FACTOR = settings.SCORE_CONVERT_FACTOR  # 2.5
    THRESHOLD_PRIMARY = settings.THRESHOLD_PRIMARY  # 40
    THRESHOLD_SECONDARY = settings.THRESHOLD_SECONDARY  # 30
    THRESHOLD_PEACE = settings.THRESHOLD_PEACE  # 60

    # 体质类型映射
    CONSTITUTION_TYPES = {
        "peace": "平和质",
        "qi_deficiency": "气虚质",
        "yang_deficiency": "阳虚质",
        "yin_deficiency": "阴虚质",
        "phlegm_damp": "痰湿质",
        "damp_heat": "湿热质",
        "blood_stasis": "血瘀质",
        "qi_depression": "气郁质",
        "special": "特禀质"
    }

    # 题目到体质类型的映射
    QUESTION_TYPE_MAPPING = {
        # 平和质 (题目 1-4)
        1: "peace", 2: "peace", 3: "peace", 4: "peace",
        # 气虚质 (题目 5-8)
        5: "qi_deficiency", 6: "qi_deficiency", 7: "qi_deficiency", 8: "qi_deficiency",
        # 阳虚质 (题目 9-12)
        9: "yang_deficiency", 10: "yang_deficiency", 11: "yang_deficiency", 12: "yang_deficiency",
        # 阴虚质 (题目 13-16)
        13: "yin_deficiency", 14: "yin_deficiency", 15: "yin_deficiency", 16: "yin_deficiency",
        # 痰湿质 (题目 17-19)
        17: "phlegm_damp", 18: "phlegm_damp", 19: "phlegm_damp",
        # 湿热质 (题目 20-22)
        20: "damp_heat", 21: "damp_heat", 22: "damp_heat",
        # 血瘀质 (题目 23-25)
        23: "blood_stasis", 24: "blood_stasis", 25: "blood_stasis",
        # 气郁质 (题目 26-28)
        26: "qi_depression", 27: "qi_depression", 28: "qi_depression",
        # 特禀质 (题目 29-30)
        29: "special", 30: "special"
    }

    def calculate_scores(self, answers: List[int]) -> Dict[str, float]:
        """
        计算各体质维度分数

        Args:
            answers: 30个问题的答案列表（1-5分）

        Returns:
            各体质类型的原始分数字典
        """
        if len(answers) != 30:
            raise ValueError(f"Expected 30 answers, got {len(answers)}")

        # 验证答案范围
        for answer in answers:
            if not 1 <= answer <= 5:
                raise ValueError(f"Answer must be between 1 and 5, got {answer}")

        # 初始化各维度分数
        raw_scores = {
            "peace": 0,
            "qi_deficiency": 0,
            "yang_deficiency": 0,
            "yin_deficiency": 0,
            "phlegm_damp": 0,
            "damp_heat": 0,
            "blood_stasis": 0,
            "qi_depression": 0,
            "special": 0
        }

        # 按题目归属累加分数
        for i, answer in enumerate(answers, start=1):
            constitution_type = self.QUESTION_TYPE_MAPPING.get(i)
            if constitution_type:
                raw_scores[constitution_type] += answer

        return raw_scores

    def convert_to_percentage(self, raw_scores: Dict[str, float]) -> Dict[str, float]:
        """
        转换为百分制

        Args:
            raw_scores: 原始分数字典

        Returns:
            百分制分数字典
        """
        percentage_scores = {}
        for constitution_type, score in raw_scores.items():
            percentage_scores[constitution_type] = min(100, score * self.SCORE_CONVERT_FACTOR)

        return percentage_scores

    def determine_constitution(self, scores: Dict[str, float]) -> Dict[str, Any]:
        """
        判定体质类型

        Args:
            scores: 百分制分数字典

        Returns:
            判定结果字典，包含主要体质、次要体质等
        """
        result_types = []
        max_score = 0
        primary_type = ""

        # 找出所有达到阈值的体质
        for ctype, score in scores.items():
            if score >= self.THRESHOLD_SECONDARY:
                result_types.append({
                    "type": ctype,
                    "name": self.CONSTITUTION_TYPES[ctype],
                    "score": round(score, 2)
                })
                if score > max_score:
                    max_score = score
                    primary_type = ctype

        # 平和质判定
        if scores.get("peace", 0) >= self.THRESHOLD_PEACE:
            # 检查其他体质是否都低于40分
            others_below_threshold = all(
                scores.get(ctype, 0) < 40 for ctype in scores if ctype != "peace"
            )
            if others_below_threshold:
                return {
                    "primary_constitution": "peace",
                    "primary_constitution_name": "平和质",
                    "secondary_constitutions": [],
                    "scores": scores
                }

        # 偏颇体质判定
        if not result_types:
            # 如果没有体质达到阈值，选择分数最高的
            for ctype, score in scores.items():
                if score > max_score:
                    max_score = score
                    primary_type = ctype
            result_types.append({
                "type": primary_type,
                "name": self.CONSTITUTION_TYPES.get(primary_type, primary_type),
                "score": round(max_score, 2)
            })

        # 确定次要体质（排除主要体质）
        secondary_constitutions = [
            rt for rt in result_types if rt["type"] != primary_type
        ]
        # 按分数降序排列
        secondary_constitutions.sort(key=lambda x: x["score"], reverse=True)

        return {
            "primary_constitution": primary_type,
            "primary_constitution_name": self.CONSTITUTION_TYPES.get(
                primary_type, primary_type
            ),
            "secondary_constitutions": secondary_constitutions[:3],  # 最多3个次要体质
            "scores": scores
        }

    def analyze(self, answers: List[int]) -> Dict[str, Any]:
        """
        完整分析流程

        Args:
            answers: 30个问题的答案列表

        Returns:
            完整的分析结果
        """
        # 计算原始分数
        raw_scores = self.calculate_scores(answers)

        # 转换为百分制
        percentage_scores = self.convert_to_percentage(raw_scores)

        # 判定体质类型
        result = self.determine_constitution(percentage_scores)

        return result


class ConstitutionAnalyzer:
    """体质分析器（单例模式）"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.scorer = ConstitutionScorer()
        return cls._instance

    def analyze(self, answers: List[int]) -> Dict[str, Any]:
        """
        分析体质类型

        Args:
            answers: 答案列表

        Returns:
            分析结果
        """
        return self.scorer.analyze(answers)
