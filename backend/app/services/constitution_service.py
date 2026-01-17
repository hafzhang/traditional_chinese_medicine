"""
体质分析服务
基于 CCMQ 量表进行中医体质辨识
"""
from typing import List, Dict, Tuple
from loguru import logger


class ConstitutionService:
    """体质分析服务"""

    # CCMQ 评分转换因子
    SCORE_CONVERT_FACTOR = 2.5  # 转换为百分制 (100/40)

    # 判定阈值
    THRESHOLD_PRIMARY = 40      # 主要体质阈值
    THRESHOLD_SECONDARY = 30    # 次要体质阈值
    THRESHOLD_PEACE = 60        # 平和质阈值

    # 体质类型映射
    CONSTITUTION_NAMES = {
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

    async def analyze(self, answers: List[int], questions: List[Dict]) -> Dict:
        """
        分析体质类型

        Args:
            answers: 用户答案列表 (1-5分)
            questions: 问题列表，包含所属体质类型

        Returns:
            体质分析结果
        """
        logger.info(f"开始分析体质，答案数量: {len(answers)}, 问题数量: {len(questions)}")

        # 1. 计算各维度得分
        scores = self._calculate_scores(answers, questions)

        # 2. 判定体质类型
        result = self._determine_constitution(scores)

        # 3. 生成报告
        report = self._generate_report(result, scores)

        logger.info(f"分析完成，主要体质: {result['primary']}, 次要体质: {[s['type'] for s in result['secondary']]}")

        return {
            "primary": result["primary"],
            "primary_name": self.CONSTITUTION_NAMES.get(result["primary"], "未知"),
            "secondary": result["secondary"],
            "scores": scores,
            "report": report
        }

    def _calculate_scores(self, answers: List[int], questions: List[Dict]) -> Dict[str, float]:
        """计算各体质维度得分"""
        scores = {
            "peace": 0.0,
            "qi_deficiency": 0.0,
            "yang_deficiency": 0.0,
            "yin_deficiency": 0.0,
            "phlegm_damp": 0.0,
            "damp_heat": 0.0,
            "blood_stasis": 0.0,
            "qi_depression": 0.0,
            "special": 0.0
        }

        # 按问题归属累加得分
        for i, question in enumerate(questions):
            constitution_type = question.get("constitution_type")
            answer = answers[i] if i < len(answers) else 0
            scores[constitution_type] = scores.get(constitution_type, 0) + answer

        # 转换为百分制
        for key in scores:
            scores[key] = min(100, round(scores[key] * self.SCORE_CONVERT_FACTOR, 2))

        logger.debug(f"各维度得分: {scores}")
        return scores

    def _determine_constitution(self, scores: Dict[str, float]) -> Dict:
        """判定体质类型"""
        result_types = []
        max_score = 0
        primary_type = ""

        # 收集所有符合阈值的体质
        for ctype, score in scores.items():
            if score >= self.THRESHOLD_SECONDARY:
                result_types.append({
                    "type": ctype,
                    "name": self.CONSTITUTION_NAMES.get(ctype, "未知"),
                    "score": score
                })
                if score > max_score:
                    max_score = score
                    primary_type = ctype

        # 平和质判定（特殊规则）
        if scores.get("peace", 0) >= self.THRESHOLD_PEACE:
            # 检查其他体质是否都低于40分
            other_all_below = all(
                scores.get(k, 0) < self.THRESHOLD_PRIMARY
                for k in scores.keys()
                if k != "peace"
            )
            if other_all_below:
                primary_type = "peace"

        # 过滤次要体质（排除主要体质）
        secondary = [r for r in result_types if r["type"] != primary_type]

        return {
            "primary": primary_type,
            "secondary": secondary
        }

    def _generate_report(self, result: Dict, scores: Dict[str, float]) -> Dict:
        """生成体质报告"""
        primary = result["primary"]

        reports = {
            "peace": {
                "name": "平和质",
                "description": "阴阳气血调和，体态适中，面色红润，精力充沛",
                "characteristics": ["精力充沛", "睡眠良好", "胃口正常", "适应力强"],
                "advice": "保持良好生活习惯，维持健康状态",
                "diet_principle": "饮食均衡，不偏食不挑食",
                "exercise_principle": "适量运动，保持健康"
            },
            "qi_deficiency": {
                "name": "气虚质",
                "description": "元气不足，气息低弱，容易疲乏",
                "characteristics": ["疲乏气短", "易出汗", "容易感冒", "肌肉松软"],
                "advice": "宜食补气食物，选择柔和运动",
                "diet_principle": "补气健脾，少食生冷",
                "exercise_principle": "量力而行，微微出汗"
            },
            "yang_deficiency": {
                "name": "阳虚质",
                "description": "阳气不足，畏寒怕冷，手足不温",
                "characteristics": ["手足不温", "喜热饮食", "畏寒怕冷", "精神不振"],
                "advice": "宜食温补食物，注意保暖",
                "diet_principle": "温补脾肾，忌食生冷",
                "exercise_principle": "动静结合，注意保暖"
            },
            "yin_deficiency": {
                "name": "阴虚质",
                "description": "阴液亏虚，口干咽燥，手足心热",
                "characteristics": ["口干咽燥", "手足心热", "盗汗", "大便干燥"],
                "advice": "宜食滋阴食物，避免熬夜",
                "diet_principle": "滋阴润燥，忌食辛辣",
                "exercise_principle": "适量运动，及时补水"
            },
            "phlegm_damp": {
                "name": "痰湿质",
                "description": "水湿内停，体形肥胖，身重不爽",
                "characteristics": ["体形肥胖", "身重困倦", "面部油腻", "口黏腻"],
                "advice": "宜食化痰利湿食物，加强运动",
                "diet_principle": "健脾利湿，清淡饮食",
                "exercise_principle": "持续运动，强度递增"
            },
            "damp_heat": {
                "name": "湿热质",
                "description": "湿热内蕴，面垢油光，口苦口臭",
                "characteristics": ["面垢油光", "口苦口臭", "大便黏滞", "小便短赤"],
                "advice": "宜食清热利湿食物，保持清爽",
                "diet_principle": "清热利湿，忌食辛辣油腻",
                "exercise_principle": "强度适中，及时补水"
            },
            "blood_stasis": {
                "name": "血瘀质",
                "description": "血行不畅，面色晦暗，易有瘀斑",
                "characteristics": ["面色晦暗", "易有瘀斑", "口唇黯淡", "痛经"],
                "advice": "宜食活血化瘀食物，适量运动",
                "diet_principle": "活血化瘀，避免寒凉",
                "exercise_principle": "循序渐进，持之以恒"
            },
            "qi_depression": {
                "name": "气郁质",
                "description": "气机郁滞，情绪抑郁，胸胁胀满",
                "characteristics": ["情绪抑郁", "胸胁胀满", "善太息", "女性经前乳胀"],
                "advice": "宜食疏肝理气食物，调节情绪",
                "diet_principle": "疏肝理气，清淡饮食",
                "exercise_principle": "动静结合，调节情绪"
            },
            "special": {
                "name": "特禀质",
                "description": "先天失常，易过敏，喷嚏流涕",
                "characteristics": ["容易过敏", "喷嚏流涕", "哮喘", "荨麻疹"],
                "advice": "宜食抗过敏食物，避免过敏原",
                "diet_principle": "清淡饮食，避免过敏原",
                "exercise_principle": "避免过敏，温和运动"
            }
        }

        base_report = reports.get(primary, reports["peace"])

        # 添加得分信息
        base_report["score"] = scores.get(primary, 0)

        return base_report


# 创建服务实例
constitution_service = ConstitutionService()
