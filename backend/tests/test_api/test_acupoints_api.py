"""
穴位API集成测试
Integration Tests for Acupoint API
"""

import pytest


class TestAcupointsAPI:
    """穴位API集成测试"""

    def test_get_acupoints_list(self, client, db_session):
        """测试获取穴位列表"""
        from api.models import Acupoint
        acupoints = [
            Acupoint(
                id=f"api-acupoint-{i:03d}",
                name=f"穴位{i}",
                body_part="下肢" if i % 2 == 0 else "上肢"
            )
            for i in range(1, 11)
        ]
        db_session.add_all(acupoints)
        db_session.commit()

        response = client.get("/api/v1/acupoints")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["total"] == 10

    def test_get_acupoint_detail(self, client, db_session):
        """测试获取穴位详情"""
        from api.models import Acupoint
        acupoint = Acupoint(
            id="api-acupoint-detail-001",
            name="足三里",
            code="ST36",
            meridian="足阳明胃经",
            body_part="下肢",
            location="犊鼻下3寸",
            simple_location="膝盖下方四横指"
        )
        db_session.add(acupoint)
        db_session.commit()

        response = client.get("/api/v1/acupoints/api-acupoint-detail-001")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["name"] == "足三里"
        assert data["data"]["code"] == "ST36"

    def test_get_acupoints_by_constitution(self, client, db_session):
        """测试按体质获取穴位"""
        from api.models import Acupoint
        acupoints = [
            Acupoint(
                id=f"const-api-{i:03d}",
                name=f"穴位{i}",
                suitable_constitutions=["qi_deficiency"] if i % 2 == 0 else []
            )
            for i in range(1, 11)
        ]
        db_session.add_all(acupoints)
        db_session.commit()

        response = client.get("/api/v1/acupoints/recommend/qi_deficiency")

        assert response.status_code == 200
        data = response.json()
        assert "constitution" in data["data"]
        assert len(data["data"]["items"]) == 5

    def test_get_acupoints_by_symptom(self, client, db_session):
        """测试按症状获取穴位"""
        from api.models import Acupoint, SymptomAcupoint
        acupoint = Acupoint(
            id="symptom-api-acu-001",
            name="足三里",
            efficacy=["健脾和胃"]
        )
        mapping = SymptomAcupoint(
            id="symptom-api-mapping-001",
            symptom_name="胃痛",
            acupoint_id="symptom-api-acu-001",
            priority=1
        )
        db_session.add_all([acupoint, mapping])
        db_session.commit()

        response = client.get("/api/v1/acupoints/symptom/胃痛")

        assert response.status_code == 200
        data = response.json()
        assert "items" in data["data"]
        assert len(data["data"]["items"]) > 0

    def test_get_acupoints_by_meridian(self, client, db_session):
        """测试按经络获取穴位"""
        from api.models import Acupoint
        acupoints = [
            Acupoint(
                id=f"meridian-api-{i:03d}",
                name=f"穴位{i}",
                meridian="足阳明胃经" if i % 2 == 0 else "足太阴脾经"
            )
            for i in range(1, 11)
        ]
        db_session.add_all(acupoints)
        db_session.commit()

        response = client.get("/api/v1/acupoints/meridian/足阳明胃经")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["meridian"] == "足阳明胃经"

    def test_get_body_parts(self, client):
        """测试获取部位列表"""
        response = client.get("/api/v1/acupoints/body-parts/list")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert isinstance(data["data"], list)

    def test_get_meridians(self, client, db_session):
        """测试获取经络列表"""
        from api.models import Acupoint
        # 添加一些穴位
        acupoint = Acupoint(
            id="meridian-list-001",
            name="足三里",
            meridian="足阳明胃经"
        )
        db_session.add(acupoint)
        db_session.commit()

        response = client.get("/api/v1/acupoints/meridians/list")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert isinstance(data["data"], list)

    def test_acupoint_not_found(self, client, db_session):
        """测试穴位不存在"""
        response = client.get("/api/v1/acupoints/non-existent-id")

        assert response.status_code == 404
