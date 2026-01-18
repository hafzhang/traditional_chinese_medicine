"""
穴位服务单元测试
Unit Tests for Acupoint Service
"""

import pytest
from api.services.acupoint_service import AcupointService
from api.models import Acupoint, SymptomAcupoint


class TestAcupointService:
    """穴位服务单元测试"""

    def test_get_acupoint_by_id(self, db_session):
        """测试根据ID获取穴位"""
        acupoint = Acupoint(
            id="test-acupoint-001",
            name="足三里",
            code="ST36",
            meridian="足阳明胃经",
            body_part="下肢",
            location="犊鼻下3寸，胫骨前缘外一横指",
            simple_location="膝盖骨外侧下方凹陷往下四横指",
            efficacy=["健脾和胃", "扶正培元"]
        )
        db_session.add(acupoint)
        db_session.commit()

        service = AcupointService()
        result = service.get_acupoint_by_id("test-acupoint-001", db_session)

        assert result is not None
        assert result.name == "足三里"
        assert result.code == "ST36"

    def test_get_acupoints_by_body_part(self, db_session):
        """测试按部位获取穴位"""
        acupoints = [
            Acupoint(
                id=f"acupoint-{i:03d}",
                name=f"穴位{i}",
                body_part="下肢" if i % 2 == 0 else "上肢"
            )
            for i in range(1, 11)
        ]
        db_session.add_all(acupoints)
        db_session.commit()

        service = AcupointService()
        result, total = service.get_acupoints_list(db_session, body_part="下肢")

        assert all(item.body_part == "下肢" for item in result)

    def test_get_acupoints_by_meridian(self, db_session):
        """测试按经络获取穴位"""
        meridians = ["足阳明胃经", "足太阴脾经", "手阳明大肠经"]
        for i, meridian in enumerate(meridians):
            acupoint = Acupoint(
                id=f"meridian-{i:03d}",
                name=f"穴位{i}",
                meridian=meridian
            )
            db_session.add(acupoint)
        db_session.commit()

        service = AcupointService()
        result = service.get_acupoints_by_meridian("足阳明胃经", db_session)

        assert all(item.meridian == "足阳明胃经" for item in result)

    def test_get_acupoints_by_constitution(self, db_session):
        """测试根据体质获取推荐穴位"""
        acupoints = [
            Acupoint(
                id=f"constitution-acu-{i:03d}",
                name=f"穴位{i}",
                suitable_constitutions=["qi_deficiency"] if i % 2 == 0 else ["yin_deficiency"]
            )
            for i in range(1, 11)
        ]
        db_session.add_all(acupoints)
        db_session.commit()

        service = AcupointService()
        result = service.get_acupoints_by_constitution("qi_deficiency", db_session)

        assert len(result) == 5
        assert all("qi_deficiency" in item.suitable_constitutions for item in result)

    def test_get_acupoints_by_symptom(self, db_session):
        """测试根据症状获取穴位"""
        # 创建穴位
        acupoint1 = Acupoint(
            id="symptom-acu-001",
            name="足三里",
            efficacy=["健脾和胃"]
        )
        acupoint2 = Acupoint(
            id="symptom-acu-002",
            name="内关",
            efficacy=["宁心安神"]
        )
        db_session.add_all([acupoint1, acupoint2])

        # 创建症状-穴位映射
        # 注意：服务使用 priority.desc()，所以priority值大的排在前面
        mapping1 = SymptomAcupoint(
            id="mapping-001",
            symptom_name="胃痛",
            acupoint_id="symptom-acu-001",
            priority=2  # 更高优先级
        )
        mapping2 = SymptomAcupoint(
            id="mapping-002",
            symptom_name="胃痛",
            acupoint_id="symptom-acu-002",
            priority=1  # 较低优先级
        )
        db_session.add_all([mapping1, mapping2])
        db_session.commit()

        service = AcupointService()
        result = service.get_acupoints_by_symptom("胃痛", db_session)

        assert len(result) == 2
        # 验证按priority降序排序 - 第一个应该是足三里（priority=2）
        assert result[0]["acupoint"].name == "足三里"
        assert result[0]["priority"] == 2

    def test_search_acupoints(self, db_session):
        """测试穴位搜索"""
        acupoints = [
            Acupoint(
                id="search-acu-001",
                name="足三里",
                code="ST36",
                efficacy=["健脾和胃", "扶正培元"]
            ),
            Acupoint(
                id="search-acu-002",
                name="三阴交",
                code="SP6",
                efficacy=["调理气血"]
            )
        ]
        db_session.add_all(acupoints)
        db_session.commit()

        service = AcupointService()

        # 搜索名称
        result, total = service.get_acupoints_list(db_session, search="足三里")
        assert len(result) > 0

    def test_acupoint_not_found(self, db_session):
        """测试穴位不存在"""
        service = AcupointService()
        result = service.get_acupoint_by_id("non-existent-id", db_session)

        assert result is None

    def test_get_body_parts(self, db_session):
        """测试获取部位列表"""
        service = AcupointService()
        body_parts = service.get_body_parts()

        assert isinstance(body_parts, list)
        assert len(body_parts) > 0
        assert any(item["value"] == "下肢" for item in body_parts)

    def test_get_meridians(self, db_session):
        """测试获取经络列表"""
        # 添加一些穴位以便提取经络
        meridians = ["足阳明胃经", "足太阴脾经"]
        for i, meridian in enumerate(meridians):
            acupoint = Acupoint(
                id=f"meridian-test-{i:03d}",
                name=f"穴位{i}",
                meridian=meridian
            )
            db_session.add(acupoint)
        db_session.commit()

        service = AcupointService()
        result = service.get_meridians(db_session)

        assert isinstance(result, list)
        assert len(result) > 0

    def test_get_acupoints_list_pagination(self, db_session):
        """测试分页功能"""
        acupoints = [
            Acupoint(
                id=f"page-acu-{i:03d}",
                name=f"穴位{i}",
                body_part="下肢"
            )
            for i in range(1, 31)
        ]
        db_session.add_all(acupoints)
        db_session.commit()

        service = AcupointService()
        acupoints_page1, total = service.get_acupoints_list(db_session, skip=0, limit=10)
        acupoints_page2, _ = service.get_acupoints_list(db_session, skip=10, limit=10)

        assert total == 30
        assert len(acupoints_page1) == 10
        assert len(acupoints_page2) == 10

    def test_is_valid_constitution_code(self, db_session):
        """测试体质代码验证"""
        service = AcupointService()

        valid_codes = ["peace", "qi_deficiency", "yang_deficiency"]

        for code in valid_codes:
            assert service.is_valid_constitution_code(code) is True

        invalid_codes = ["invalid", "wrong"]
        for code in invalid_codes:
            assert service.is_valid_constitution_code(code) is False

    def test_get_constitution_name(self, db_session):
        """测试获取体质名称"""
        service = AcupointService()

        assert service.get_constitution_name("qi_deficiency") == "气虚质"
        assert service.get_constitution_name("yang_deficiency") == "阳虚质"
        # 对于无效代码，返回原始代码
        assert service.get_constitution_name("invalid") == "invalid"
