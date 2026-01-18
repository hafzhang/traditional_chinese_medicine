"""
Course Service
养生课程服务层 - Phase 1
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from api.models import Course


class CourseService:
    """养生课程服务类"""

    # 有效的体质代码
    VALID_CONSTITUTIONS = {
        "peace", "qi_deficiency", "yang_deficiency", "yin_deficiency",
        "phlegm_damp", "damp_heat", "blood_stasis", "qi_depression", "special"
    }

    # 课程分类
    CATEGORIES = ["constitution", "season", "diet", "meridian"]

    # 内容类型
    CONTENT_TYPES = ["video", "article"]

    def get_course_by_id(self, course_id: str, db: Session) -> Optional[Course]:
        """
        根据ID获取课程详情

        Args:
            course_id: 课程ID
            db: 数据库会话

        Returns:
            课程对象或None
        """
        return db.query(Course).filter(Course.id == course_id).first()

    def get_courses_list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        category: Optional[str] = None,
        content_type: Optional[str] = None,
        constitution: Optional[str] = None,
        search: Optional[str] = None
    ) -> tuple[List[Course], int]:
        """
        获取课程列表

        Args:
            db: 数据库会话
            skip: 跳过数量
            limit: 限制数量
            category: 分类筛选
            content_type: 内容类型筛选
            constitution: 体质筛选
            search: 搜索关键词

        Returns:
            (课程列表, 总数)
        """
        query = db.query(Course)

        # 筛选条件
        if category:
            query = query.filter(Course.category == category)
        if content_type:
            query = query.filter(Course.content_type == content_type)
        if constitution:
            query = query.filter(Course.suitable_constitutions.contains(constitution))
        if search:
            query = query.filter(Course.title.like(f"%{search}%"))

        # 总数
        total = query.count()

        # 分页
        courses = query.order_by(Course.view_count.desc()).offset(skip).limit(limit).all()

        return courses, total

    def get_courses_by_constitution(
        self,
        constitution: str,
        db: Session,
        limit: int = 20
    ) -> List[Course]:
        """
        根据体质获取推荐课程

        Args:
            constitution: 体质代码
            db: 数据库会话
            limit: 限制数量

        Returns:
            推荐课程列表
        """
        if not self.is_valid_constitution_code(constitution):
            return []

        courses = db.query(Course).filter(
            Course.category == "constitution",
            Course.suitable_constitutions.contains(constitution)
        ).order_by(Course.view_count.desc()).limit(limit).all()

        return courses

    def get_courses_by_season(
        self,
        season: str,
        db: Session,
        limit: int = 20
    ) -> List[Course]:
        """
        根据季节获取课程

        Args:
            season: 季节 (spring, summer, autumn, winter)
            db: 数据库会话
            limit: 限制数量

        Returns:
            课程列表
        """
        courses = db.query(Course).filter(
            Course.category == "season",
            Course.subcategory == season
        ).order_by(Course.view_count.desc()).limit(limit).all()

        return courses

    def increment_view_count(self, course_id: str, db: Session) -> bool:
        """
        增加浏览次数

        Args:
            course_id: 课程ID
            db: 数据库会话

        Returns:
            是否成功
        """
        course = self.get_course_by_id(course_id, db)
        if course:
            course.view_count = (course.view_count or 0) + 1
            db.commit()
            return True
        return False

    def get_categories(self) -> List[Dict[str, str]]:
        """
        获取课程分类列表

        Returns:
            分类列表
        """
        return [
            {"value": "constitution", "label": "体质调理"},
            {"value": "season", "label": "季节养生"},
            {"value": "diet", "label": "饮食养生"},
            {"value": "meridian", "label": "经络养生"}
        ]

    def get_seasons(self) -> List[Dict[str, str]]:
        """
        获取季节列表

        Returns:
            季节列表
        """
        return [
            {"value": "spring", "label": "春季"},
            {"value": "summer", "label": "夏季"},
            {"value": "autumn", "label": "秋季"},
            {"value": "winter", "label": "冬季"}
        ]

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
_course_service_instance = None


def get_course_service() -> CourseService:
    """获取课程服务实例"""
    global _course_service_instance
    if _course_service_instance is None:
        _course_service_instance = CourseService()
    return _course_service_instance
