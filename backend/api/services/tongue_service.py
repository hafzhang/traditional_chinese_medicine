"""
Tongue Diagnosis Service
舌诊服务层 - Phase 1
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from api.models import TongueDiagnosisRecord


class TongueService:
    """舌诊服务类"""

    # 舌质颜色选项
    TONGUE_COLORS = ["淡白", "淡红", "红", "绛", "紫"]

    # 舌质形态选项
    TONGUE_SHAPES = ["正常", "胖大", "瘦薄", "齿痕", "裂纹"]

    # 苔色选项
    COATING_COLORS = ["白苔", "黄苔", "灰黑苔"]

    # 苔质选项
    COATING_THICKNESS = ["薄苔", "厚苔", "腻苔", "剥落"]

    # 体质对应的舌象特征（简化版）
    # 按优先级排序，优先级高的先匹配（当特征相同时优先返回前面的）
    CONSTITUTION_TONGUE_MAP = {
        "peace": {
            "tongue_color": "淡红",
            "tongue_shape": "正常",
            "coating_color": "白苔",
            "coating_thickness": "薄苔"
        },
        "qi_deficiency": {
            "tongue_color": "淡白",
            "tongue_shape": "胖大",
            "coating_color": "白苔",
            "coating_thickness": "薄苔"
        },
        "yin_deficiency": {
            "tongue_color": "红",
            "tongue_shape": "瘦薄",
            "coating_color": "黄苔",
            "coating_thickness": "薄苔"
        },
        "phlegm_damp": {
            "tongue_color": "淡白",
            "tongue_shape": "胖大",
            "coating_color": "白苔",
            "coating_thickness": "厚苔"
        },
        "yang_deficiency": {
            "tongue_color": "淡白",
            "tongue_shape": "胖大",
            "coating_color": "白苔",
            "coating_thickness": "腻苔"
        },
        "damp_heat": {
            "tongue_color": "红",
            "tongue_shape": "正常",
            "coating_color": "黄苔",
            "coating_thickness": "腻苔"
        },
        "blood_stasis": {
            "tongue_color": "紫",
            "tongue_shape": "正常",
            "coating_color": "白苔",
            "coating_thickness": "薄苔"
        },
        "qi_depression": {
            "tongue_color": "淡红",
            "tongue_shape": "齿痕",
            "coating_color": "白苔",
            "coating_thickness": "薄苔"
        },
        "special": {
            "tongue_color": "淡红",
            "tongue_shape": "裂纹",
            "coating_color": "白苔",
            "coating_thickness": "薄苔"
        }
    }

    def analyze_tongue(
        self,
        tongue_color: str,
        tongue_shape: str,
        coating_color: str,
        coating_thickness: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        分析舌象判断体质倾向

        Args:
            tongue_color: 舌质颜色
            tongue_shape: 舌质形态
            coating_color: 苔色
            coating_thickness: 苔质
            db: 数据库会话

        Returns:
            分析结果
        """
        # 简化版判断逻辑
        # 计算与各体质舌象的匹配度
        scores = {}
        for constitution, tongue_features in self.CONSTITUTION_TONGUE_MAP.items():
            score = 0
            if tongue_features["tongue_color"] == tongue_color:
                score += 30
            if tongue_features["tongue_shape"] == tongue_shape:
                score += 35
            if tongue_features["coating_color"] == coating_color:
                score += 20
            if tongue_features["coating_thickness"] == coating_thickness:
                score += 15
            scores[constitution] = score

        # 找出最高分的体质
        max_score = max(scores.values())
        best_match = [k for k, v in scores.items() if v == max_score][0]

        # 计算置信度（基于最高分）
        confidence = min(100, (max_score / 100) * 100)

        return {
            "constitution_tendency": best_match,
            "constitution_name": self.get_constitution_name(best_match),
            "confidence": round(confidence, 2),
            "scores": scores,
            "tongue_features": {
                "tongue_color": tongue_color,
                "tongue_shape": tongue_shape,
                "coating_color": coating_color,
                "coating_thickness": coating_thickness
            }
        }

    def save_diagnosis_record(
        self,
        user_id: Optional[str],
        result_id: Optional[str],
        image_url: str,
        analysis_result: Dict[str, Any],
        db: Session
    ) -> TongueDiagnosisRecord:
        """
        保存舌诊记录

        Args:
            user_id: 用户ID
            result_id: 测试结果ID
            image_url: 图片URL
            analysis_result: 分析结果
            db: 数据库会话

        Returns:
            舌诊记录对象
        """
        features = analysis_result.get("tongue_features", {})

        record = TongueDiagnosisRecord(
            user_id=user_id,
            result_id=result_id,
            image_url=image_url,
            tongue_color=features.get("tongue_color"),
            tongue_shape=features.get("tongue_shape"),
            coating_color=features.get("coating_color"),
            coating_thickness=features.get("coating_thickness"),
            constitution_tendency=analysis_result.get("constitution_tendency"),
            confidence=analysis_result.get("confidence"),
            advice=self._generate_advice(analysis_result.get("constitution_tendency"))
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return record

    def compare_with_test(
        self,
        tongue_constitution: str,
        test_constitution: str
    ) -> Dict[str, Any]:
        """
        对比舌诊结果与测试结果

        Args:
            tongue_constitution: 舌诊体质
            test_constitution: 测试体质

        Returns:
            对比结果
        """
        is_consistent = tongue_constitution == test_constitution

        result = {
            "is_consistent": is_consistent,
            "tongue_constitution": tongue_constitution,
            "tongue_constitution_name": self.get_constitution_name(tongue_constitution),
            "test_constitution": test_constitution,
            "test_constitution_name": self.get_constitution_name(test_constitution)
        }

        if is_consistent:
            result["message"] = "舌诊结果与测试结果一致，证实了您的体质类型。"
        else:
            result["message"] = f"舌诊结果({result['tongue_constitution_name']})与测试结果({result['test_constitution_name']})有所不同，建议结合两者的综合判断。"

        return result

    def get_user_records(
        self,
        user_id: str,
        db: Session,
        limit: int = 10
    ) -> List[TongueDiagnosisRecord]:
        """
        获取用户的舌诊记录

        Args:
            user_id: 用户ID
            db: 数据库会话
            limit: 限制数量

        Returns:
            舌诊记录列表
        """
        records = db.query(TongueDiagnosisRecord).filter(
            TongueDiagnosisRecord.user_id == user_id
        ).order_by(TongueDiagnosisRecord.created_at.desc()).limit(limit).all()

        return records

    def _generate_advice(self, constitution: str) -> Dict[str, str]:
        """
        生成调理建议

        Args:
            constitution: 体质代码

        Returns:
            调理建议字典
        """
        advice_map = {
            "peace": {
                "diet": "保持均衡饮食，不偏食挑食",
                "lifestyle": "作息规律，适度运动"
            },
            "qi_deficiency": {
                "diet": "多吃补气健脾食物，如山药、黄芪、红枣",
                "lifestyle": "避免过度劳累，保证充足睡眠"
            },
            "yang_deficiency": {
                "diet": "多吃温补食物，如羊肉、韭菜、生姜",
                "lifestyle": "注意保暖，避免受凉"
            },
            "yin_deficiency": {
                "diet": "多吃滋阴润燥食物，如百合、银耳、梨",
                "lifestyle": "避免熬夜，保持心情舒畅"
            },
            "phlegm_damp": {
                "diet": "多吃健脾利湿食物，如薏米、赤小豆、冬瓜",
                "lifestyle": "加强运动，保持居住环境干燥"
            },
            "damp_heat": {
                "diet": "多吃清热利湿食物，如绿豆、苦瓜、芹菜",
                "lifestyle": "避免辛辣油腻，保持皮肤清洁"
            },
            "blood_stasis": {
                "diet": "多吃活血化瘀食物，如山楂、红花、桃仁",
                "lifestyle": "适度运动，避免久坐"
            },
            "qi_depression": {
                "diet": "多吃疏肝理气食物，如玫瑰花、陈皮、佛手",
                "lifestyle": "保持心情舒畅，适当户外活动"
            },
            "special": {
                "diet": "避免过敏原，多吃抗过敏食物，如蜂蜜、红枣",
                "lifestyle": "保持室内清洁，避免接触过敏源"
            }
        }

        return advice_map.get(constitution, advice_map["peace"])

    def get_constitution_name(self, code: str) -> str:
        """
        获取体质中文名称

        Args:
            code: 体质代码

        Returns:
            体质中文名称
        """
        names = {
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
        return names.get(code, code)


# 单例模式
_tongue_service_instance = None


def get_tongue_service() -> TongueService:
    """获取舌诊服务实例"""
    global _tongue_service_instance
    if _tongue_service_instance is None:
        _tongue_service_instance = TongueService()
    return _tongue_service_instance
