"""
舌诊服务单元测试
Unit Tests for Tongue Diagnosis Service
"""

import pytest
from api.services.tongue_service import TongueService
from api.models import TongueDiagnosisRecord, ConstitutionResult


class TestTongueDiagnosisService:
    """舌诊服务单元测试"""

    def test_analyze_tongue_qi_deficiency(self, db_session):
        """测试分析气虚质舌象"""
        service = TongueService()

        # 气虚质舌象特征
        result = service.analyze_tongue(
            tongue_color="淡白",
            tongue_shape="胖大",
            coating_color="白苔",
            coating_thickness="薄苔",
            db=db_session
        )

        assert result["constitution_tendency"] == "qi_deficiency"
        assert result["constitution_name"] == "气虚质"
        assert result["confidence"] > 0
        assert "tongue_features" in result

    def test_analyze_tongue_yin_deficiency(self, db_session):
        """测试分析阴虚质舌象"""
        service = TongueService()

        result = service.analyze_tongue(
            tongue_color="红",
            tongue_shape="瘦薄",
            coating_color="黄苔",
            coating_thickness="薄苔",
            db=db_session
        )

        assert result["constitution_tendency"] == "yin_deficiency"
        assert result["constitution_name"] == "阴虚质"

    def test_analyze_tongue_peace(self, db_session):
        """测试分析平和质舌象"""
        service = TongueService()

        result = service.analyze_tongue(
            tongue_color="淡红",
            tongue_shape="正常",
            coating_color="白苔",
            coating_thickness="薄苔",
            db=db_session
        )

        assert result["constitution_tendency"] == "peace"
        assert result["constitution_name"] == "平和质"

    def test_compare_with_test_result_consistent(self):
        """测试与测试结果对比（一致）"""
        service = TongueService()

        comparison = service.compare_with_test(
            tongue_constitution="qi_deficiency",
            test_constitution="qi_deficiency"
        )

        assert comparison["is_consistent"] is True
        assert "一致" in comparison["message"]
        assert comparison["tongue_constitution_name"] == "气虚质"

    def test_compare_with_test_result_inconsistent(self):
        """测试与测试结果对比（不一致）"""
        service = TongueService()

        comparison = service.compare_with_test(
            tongue_constitution="qi_deficiency",
            test_constitution="yin_deficiency"
        )

        assert comparison["is_consistent"] is False
        assert "不同" in comparison["message"]
        assert comparison["tongue_constitution_name"] == "气虚质"
        assert comparison["test_constitution_name"] == "阴虚质"

    def test_save_diagnosis_record(self, db_session):
        """测试保存舌诊记录"""
        service = TongueService()

        analysis_result = {
            "constitution_tendency": "qi_deficiency",
            "constitution_name": "气虚质",
            "confidence": 0.85,
            "tongue_features": {
                "tongue_color": "淡白",
                "tongue_shape": "胖大",
                "coating_color": "白苔",
                "coating_thickness": "薄苔"
            }
        }

        record = service.save_diagnosis_record(
            user_id="test-user-001",
            result_id=None,
            image_url="https://example.com/tongue.jpg",
            analysis_result=analysis_result,
            db=db_session
        )

        assert record.id is not None
        assert record.constitution_tendency == "qi_deficiency"
        assert record.tongue_color == "淡白"
        assert record.tongue_shape == "胖大"

    def test_save_diagnosis_record_with_comparison(self, db_session):
        """测试保存舌诊记录（带测试结果对比）"""
        # 先创建测试结果
        constitution_result = ConstitutionResult(
            id="test-result-001",
            primary_constitution="qi_deficiency",
            scores={"qi_deficiency": 50}
        )
        db_session.add(constitution_result)
        db_session.commit()

        service = TongueService()

        analysis_result = {
            "constitution_tendency": "qi_deficiency",
            "constitution_name": "气虚质",
            "confidence": 0.85,
            "tongue_features": {
                "tongue_color": "淡白",
                "tongue_shape": "胖大",
                "coating_color": "白苔",
                "coating_thickness": "薄苔"
            }
        }

        record = service.save_diagnosis_record(
            user_id="test-user-001",
            result_id="test-result-001",
            image_url="https://example.com/tongue.jpg",
            analysis_result=analysis_result,
            db=db_session
        )

        assert record.result_id == "test-result-001"
        assert record.constitution_tendency == "qi_deficiency"

    def test_get_user_records(self, db_session):
        """测试获取用户舌诊记录"""
        service = TongueService()

        # 创建多个记录
        for i in range(1, 6):
            analysis_result = {
                "constitution_tendency": "qi_deficiency" if i % 2 == 0 else "yin_deficiency",
                "constitution_name": f"体质{i}",
                "confidence": 0.8,
                "tongue_features": {
                    "tongue_color": "淡白",
                    "tongue_shape": "胖大",
                    "coating_color": "白苔",
                    "coating_thickness": "薄苔"
                }
            }

            service.save_diagnosis_record(
                user_id="test-user-records",
                result_id=f"test-result-{i}",
                image_url=f"https://example.com/tongue{i}.jpg",
                analysis_result=analysis_result,
                db=db_session
            )

        records = service.get_user_records("test-user-records", db_session)

        assert len(records) == 5
        # 验证按时间倒序排列
        assert records[0].created_at >= records[1].created_at

    def test_generate_advice_qi_deficiency(self):
        """测试生成气虚质调理建议"""
        service = TongueService()

        advice = service._generate_advice("qi_deficiency")

        assert "diet" in advice
        assert "lifestyle" in advice
        assert "山药" in advice["diet"]
        assert "黄芪" in advice["diet"]

    def test_generate_advice_yang_deficiency(self):
        """测试生成阳虚质调理建议"""
        service = TongueService()

        advice = service._generate_advice("yang_deficiency")

        assert "diet" in advice
        assert "lifestyle" in advice
        assert "羊肉" in advice["diet"]
        assert "生姜" in advice["diet"]

    def test_get_constitution_name(self):
        """测试获取体质名称"""
        service = TongueService()

        assert service.get_constitution_name("qi_deficiency") == "气虚质"
        assert service.get_constitution_name("yang_deficiency") == "阳虚质"
        assert service.get_constitution_name("yin_deficiency") == "阴虚质"
        assert service.get_constitution_name("peace") == "平和质"
        # 无效代码返回原始值
        assert service.get_constitution_name("invalid") == "invalid"

    def test_tongue_colors_list(self):
        """测试舌质颜色列表"""
        service = TongueService()

        colors = service.TONGUE_COLORS
        assert "淡白" in colors
        assert "淡红" in colors
        assert "红" in colors
        assert "绛" in colors
        assert "紫" in colors

    def test_tongue_shapes_list(self):
        """测试舌质形态列表"""
        service = TongueService()

        shapes = service.TONGUE_SHAPES
        assert "正常" in shapes
        assert "胖大" in shapes
        assert "瘦薄" in shapes
        assert "齿痕" in shapes
        assert "裂纹" in shapes

    def test_coating_colors_list(self):
        """测试苔色列表"""
        service = TongueService()

        colors = service.COATING_COLORS
        assert "白苔" in colors
        assert "黄苔" in colors
        assert "灰黑苔" in colors

    def test_coating_thickness_list(self):
        """测试苔质列表"""
        service = TongueService()

        thickness = service.COATING_THICKNESS
        assert "薄苔" in thickness
        assert "厚苔" in thickness
        assert "腻苔" in thickness
        assert "剥落" in thickness

    def test_constitution_tongue_map_completeness(self):
        """测试体质-舌象映射完整性"""
        service = TongueService()

        # 所有9种体质都应该有映射
        required_constitutions = [
            "peace", "qi_deficiency", "yang_deficiency", "yin_deficiency",
            "phlegm_damp", "damp_heat", "blood_stasis", "qi_depression", "special"
        ]

        for constitution in required_constitutions:
            assert constitution in service.CONSTITUTION_TONGUE_MAP
            tongue_features = service.CONSTITUTION_TONGUE_MAP[constitution]
            assert "tongue_color" in tongue_features
            assert "tongue_shape" in tongue_features
            assert "coating_color" in tongue_features
            assert "coating_thickness" in tongue_features

    def test_analyze_tongue_all_constitutions(self, db_session):
        """测试分析所有9种体质的舌象"""
        service = TongueService()

        # 测试每种体质都有对应的舌象
        # 注意：phlegm_damp使用"厚苔"与yang_deficiency的"腻苔"区分
        test_cases = [
            ("淡红", "正常", "白苔", "薄苔", "peace"),
            ("淡白", "胖大", "白苔", "薄苔", "qi_deficiency"),
            ("淡白", "胖大", "白苔", "腻苔", "yang_deficiency"),
            ("红", "瘦薄", "黄苔", "薄苔", "yin_deficiency"),
            ("淡白", "胖大", "白苔", "厚苔", "phlegm_damp"),
            ("红", "正常", "黄苔", "腻苔", "damp_heat"),
            ("紫", "正常", "白苔", "薄苔", "blood_stasis"),
            ("淡红", "齿痕", "白苔", "薄苔", "qi_depression"),
            ("淡红", "裂纹", "白苔", "薄苔", "special"),
        ]

        for color, shape, coating, thickness, expected in test_cases:
            result = service.analyze_tongue(color, shape, coating, thickness, db_session)
            assert result["constitution_tendency"] == expected, f"Failed for {expected}"

    def test_analyze_confidence_calculation(self, db_session):
        """测试置信度计算"""
        service = TongueService()

        # 完全匹配的舌象应该有高置信度
        result = service.analyze_tongue("淡白", "胖大", "白苔", "薄苔", db_session)

        # 气虚质特征：淡白(30) + 胖大(35) + 白苔(20) + 薄苔(15) = 100分
        assert result["constitution_tendency"] == "qi_deficiency"
        assert result["confidence"] >= 0.85  # 应该有较高置信度

    def test_comparison_message_format(self):
        """测试对比消息格式"""
        service = TongueService()

        # 一致的情况
        result_consistent = service.compare_with_test("qi_deficiency", "qi_deficiency")
        assert "message" in result_consistent
        assert len(result_consistent["message"]) > 0

        # 不一致的情况
        result_inconsistent = service.compare_with_test("qi_deficiency", "yin_deficiency")
        assert "message" in result_inconsistent
        assert len(result_inconsistent["message"]) > 0
