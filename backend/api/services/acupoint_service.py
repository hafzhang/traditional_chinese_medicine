"""
Acupoint Service
穴位服务层 - Phase 1
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from api.models import Acupoint, SymptomAcupoint


class AcupointService:
    """穴位服务类"""

    # 有效的体质代码
    VALID_CONSTITUTIONS = {
        "peace", "qi_deficiency", "yang_deficiency", "yin_deficiency",
        "phlegm_damp", "damp_heat", "blood_stasis", "qi_depression", "special"
    }

    # 部位列表
    BODY_PARTS = ["头面部", "颈项部", "胸腹部", "腰背部", "上肢", "下肢"]

    def get_acupoint_by_id(self, acupoint_id: str, db: Session) -> Optional[Acupoint]:
        """
        根据ID获取穴位详情

        Args:
            acupoint_id: 穴位ID
            db: 数据库会话

        Returns:
            穴位对象或None
        """
        return db.query(Acupoint).filter(Acupoint.id == acupoint_id).first()

    def get_acupoints_list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        body_part: Optional[str] = None,
        constitution: Optional[str] = None,
        search: Optional[str] = None
    ) -> tuple[List[Acupoint], int]:
        """
        获取穴位列表

        Args:
            db: 数据库会话
            skip: 跳过数量
            limit: 限制数量
            body_part: 部位筛选
            constitution: 体质筛选
            search: 搜索关键词

        Returns:
            (穴位列表, 总数)
        """
        query = db.query(Acupoint)

        # 筛选条件
        if body_part:
            query = query.filter(Acupoint.body_part == body_part)
        if constitution:
            query = query.filter(Acupoint.suitable_constitutions.contains(constitution))
        if search:
            query = query.filter(Acupoint.name.like(f"%{search}%"))

        # 总数
        total = query.count()

        # 分页
        acupoints = query.order_by(Acupoint.name).offset(skip).limit(limit).all()

        return acupoints, total

    def get_acupoints_by_constitution(
        self,
        constitution: str,
        db: Session,
        limit: int = 20
    ) -> List[Acupoint]:
        """
        根据体质获取推荐穴位

        Args:
            constitution: 体质代码
            db: 数据库会话
            limit: 限制数量

        Returns:
            推荐穴位列表
        """
        if not self.is_valid_constitution_code(constitution):
            return []

        acupoints = db.query(Acupoint).filter(
            Acupoint.suitable_constitutions.contains(constitution)
        ).order_by(Acupoint.name).limit(limit).all()

        return acupoints

    def get_acupoints_by_symptom(
        self,
        symptom: str,
        db: Session,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        根据症状查找推荐穴位

        Args:
            symptom: 症状名称
            db: 数据库会话
            limit: 限制数量

        Returns:
            穴位列表（按优先级排序）
        """
        # 通过症状-穴位关联表查找
        symptom_records = db.query(SymptomAcupoint).filter(
            SymptomAcupoint.symptom_name.like(f"%{symptom}%")
        ).order_by(SymptomAcupoint.priority.desc()).limit(limit).all()

        # 获取关联的穴位详情
        acupoint_ids = [r.acupoint_id for r in symptom_records]
        acupoints = db.query(Acupoint).filter(
            Acupoint.id.in_(acupoint_ids)
        ).all()

        # 构建返回数据，包含优先级
        acupoint_map = {a.id: a for a in acupoints}
        result = []
        for record in symptom_records:
            if record.acupoint_id in acupoint_map:
                acupoint = acupoint_map[record.acupoint_id]
                result.append({
                    "acupoint": acupoint,
                    "priority": record.priority
                })

        return result

    def get_acupoints_by_meridian(
        self,
        meridian: str,
        db: Session,
        limit: int = 50
    ) -> List[Acupoint]:
        """
        根据经络获取穴位列表

        Args:
            meridian: 经络名称
            db: 数据库会话
            limit: 限制数量

        Returns:
            穴位列表
        """
        acupoints = db.query(Acupoint).filter(
            Acupoint.meridian.like(f"%{meridian}%")
        ).order_by(Acupoint.code).limit(limit).all()

        return acupoints

    def get_body_parts(self) -> List[Dict[str, str]]:
        """
        获取部位列表

        Returns:
            部位列表
        """
        return [
            {"value": "头面部", "label": "头面部"},
            {"value": "颈项部", "label": "颈项部"},
            {"value": "胸腹部", "label": "胸腹部"},
            {"value": "腰背部", "label": "腰背部"},
            {"value": "上肢", "label": "上肢"},
            {"value": "下肢", "label": "下肢"}
        ]

    def get_meridians(self, db: Session) -> List[str]:
        """
        获取所有经络列表

        Args:
            db: 数据库会话

        Returns:
            经络名称列表
        """
        meridians = db.query(Acupoint.meridian).distinct().all()
        return [m[0] for m in meridians if m[0]]

    def is_valid_constitution_code(self, code: str) -> bool:
        """
        验证体质代码是否有效

        Args:
            code: 体质代码

        Returns:
            是否有效
        """
        return code in self.VALID_CONSTITUTIONS

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
_acupoint_service_instance = None


def get_acupoint_service() -> AcupointService:
    """获取穴位服务实例"""
    global _acupoint_service_instance
    if _acupoint_service_instance is None:
        _acupoint_service_instance = AcupointService()
    return _acupoint_service_instance
