"""
舌诊API集成测试
API Integration Tests for Tongue Diagnosis
"""

import pytest
import base64
from fastapi.testclient import TestClient


class TestTongueDiagnosisAPI:
    """舌诊API集成测试"""

    def test_get_tongue_options(self, client: TestClient):
        """测试获取舌诊选项列表"""
        response = client.get("/api/v1/tongue/options")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "data" in data

        # 验证选项列表
        options = data["data"]
        assert "tongue_colors" in options
        assert "tongue_shapes" in options
        assert "coating_colors" in options
        assert "coating_thickness" in options

        # 验证舌质颜色选项
        tongue_colors = options["tongue_colors"]
        color_values = [item["value"] for item in tongue_colors]
        assert "淡白" in color_values
        assert "淡红" in color_values
        assert "红" in color_values

    def test_analyze_tongue_valid_input(self, client: TestClient, db_session):
        """测试有效的舌象分析"""
        # 创建测试结果（用于对比）
        from api.models import ConstitutionResult
        test_result = ConstitutionResult(
            id="test-result-for-tongue",
            primary_constitution="qi_deficiency",
            scores={"qi_deficiency": 50}
        )
        db_session.add(test_result)
        db_session.commit()

        # 测试有效的舌象分析
        response = client.post(
            "/api/v1/tongue/analyze",
            data={
                "tongue_color": "淡白",
                "tongue_shape": "胖大",
                "coating_color": "白苔",
                "coating_thickness": "薄苔"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "data" in data

        result = data["data"]
        assert "analysis" in result
        assert "record_id" in result
        assert result["analysis"]["constitution_tendency"] == "qi_deficiency"

    def test_analyze_tongue_with_test_result_comparison(self, client: TestClient, db_session):
        """测试带测试结果对比的舌诊分析"""
        # 创建测试结果
        from api.models import ConstitutionResult
        test_result = ConstitutionResult(
            id="test-result-for-comparison",
            primary_constitution="qi_deficiency",
            scores={"qi_deficiency": 50}
        )
        db_session.add(test_result)
        db_session.commit()

        # 舌诊分析（与测试结果一致）
        response = client.post(
            "/api/v1/tongue/analyze",
            data={
                "tongue_color": "淡白",
                "tongue_shape": "胖大",
                "coating_color": "白苔",
                "coating_thickness": "薄苔",
                "result_id": "test-result-for-comparison"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0

        result = data["data"]
        assert "comparison" in result
        assert result["comparison"]["is_consistent"] is True

    def test_analyze_tongue_invalid_tongue_color(self, client: TestClient):
        """测试无效的舌质颜色"""
        response = client.post(
            "/api/v1/tongue/analyze",
            data={
                "tongue_color": "invalid_color",
                "tongue_shape": "胖大",
                "coating_color": "白苔",
                "coating_thickness": "薄苔"
            }
        )

        assert response.status_code == 400

    def test_analyze_tongue_invalid_tongue_shape(self, client: TestClient):
        """测试无效的舌质形态"""
        response = client.post(
            "/api/v1/tongue/analyze",
            data={
                "tongue_color": "淡白",
                "tongue_shape": "invalid_shape",
                "coating_color": "白苔",
                "coating_thickness": "薄苔"
            }
        )

        assert response.status_code == 400

    def test_analyze_tongue_invalid_coating_color(self, client: TestClient):
        """测试无效的苔色"""
        response = client.post(
            "/api/v1/tongue/analyze",
            data={
                "tongue_color": "淡白",
                "tongue_shape": "胖大",
                "coating_color": "invalid_color",
                "coating_thickness": "薄苔"
            }
        )

        assert response.status_code == 400

    def test_analyze_tongue_invalid_coating_thickness(self, client: TestClient):
        """测试无效的苔质"""
        response = client.post(
            "/api/v1/tongue/analyze",
            data={
                "tongue_color": "淡白",
                "tongue_shape": "胖大",
                "coating_color": "白苔",
                "coating_thickness": "invalid_thickness"
            }
        )

        assert response.status_code == 400

    def test_get_user_records_empty(self, client: TestClient, db_session):
        """测试获取空的用户记录"""
        response = client.get("/api/v1/tongue/records/test-user-001")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["total"] == 0
        assert data["data"]["items"] == []

    def test_get_user_records_with_data(self, client: TestClient, db_session):
        """测试获取用户记录（有数据）"""
        from api.models import TongueDiagnosisRecord

        # 创建测试记录
        records = [
            TongueDiagnosisRecord(
                id=f"record-{i:03d}",
                user_id="test-user-records",
                tongue_color="淡白",
                constitution_tendency="qi_deficiency"
            )
            for i in range(1, 4)
        ]
        for record in records:
            db_session.add(record)
        db_session.commit()

        response = client.get("/api/v1/tongue/records/test-user-records")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total"] == 3
        assert len(data["data"]["items"]) == 3

    def test_analyze_all_constitutions(self, client: TestClient):
        """测试所有9种体质的舌象分析"""
        test_cases = [
            # (tongue_color, tongue_shape, coating_color, coating_thickness, expected_constitution)
            # 注意：特征匹配基于评分系统，最高分的体质会被返回
            # phlegm_damp使用"厚苔"与yang_deficiency的"腻苔"区分
            ("淡白", "正常", "白苔", "薄苔", "peace"),  # 70分(正常35)
            ("淡白", "胖大", "白苔", "薄苔", "qi_deficiency"),  # 100分(全部匹配)
            ("淡白", "胖大", "白苔", "腻苔", "yang_deficiency"),  # 100分(全部匹配)
            ("红", "瘦薄", "黄苔", "薄苔", "yin_deficiency"),  # 100分(全部匹配)
            ("淡白", "胖大", "白苔", "厚苔", "phlegm_damp"),  # 90分(苔厚厚苔0腻苔15)
            ("红", "正常", "黄苔", "腻苔", "damp_heat"),  # 100分(全部匹配)
            ("紫", "正常", "白苔", "薄苔", "blood_stasis"),  # 100分(全部匹配)
            ("淡红", "齿痕", "白苔", "薄苔", "qi_depression"),  # 95分(齿痕35-正常0)
            ("淡红", "裂纹", "白苔", "薄苔", "special"),  # 95分(裂纹35-正常0)
            ("淡红", "正常", "白苔", "薄苔", "peace"),  # 100分(全部匹配)
        ]

        for color, shape, coating, thickness, expected in test_cases:
            response = client.post(
                "/api/v1/tongue/analyze",
                data={
                    "tongue_color": color,
                    "tongue_shape": shape,
                    "coating_color": coating,
                    "coating_thickness": thickness
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 0
            assert data["data"]["analysis"]["constitution_tendency"] == expected

    def test_database_unavailable(self, client: TestClient):
        """测试数据库不可用的情况"""
        # 这个测试需要mock数据库不可用的场景
        # 在实际环境中，可以通过修改依赖注入来测试
        # 这里暂时跳过
        pass
