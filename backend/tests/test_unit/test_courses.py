"""
课程服务单元测试
Unit Tests for Course Service
"""

import pytest
from api.services.course_service import CourseService
from api.models import Course


class TestCourseService:
    """课程服务单元测试"""

    def test_get_course_by_id(self, db_session):
        """测试根据ID获取课程"""
        course = Course(
            id="test-course-001",
            title="气虚质怎么调理？",
            category="constitution",
            subcategory="qi_deficiency",
            content_type="video",
            content_url="https://example.com/video.mp4",
            suitable_constitutions=["qi_deficiency"],
            duration=120,
            cover_image="https://example.com/cover.jpg"
        )
        db_session.add(course)
        db_session.commit()

        service = CourseService()
        result = service.get_course_by_id("test-course-001", db_session)

        assert result is not None
        assert result.title == "气虚质怎么调理？"
        assert result.category == "constitution"

    def test_get_courses_by_constitution(self, db_session):
        """测试根据体质获取课程"""
        courses = [
            Course(
                id=f"course-{i:03d}",
                title=f"课程{i}",
                category="constitution",
                suitable_constitutions=["qi_deficiency"] if i % 2 == 0 else ["yin_deficiency"]
            )
            for i in range(1, 11)
        ]
        db_session.add_all(courses)
        db_session.commit()

        service = CourseService()
        result = service.get_courses_by_constitution("qi_deficiency", db_session)

        assert len(result) == 5
        assert all("qi_deficiency" in item.suitable_constitutions for item in result)

    def test_get_courses_by_category(self, db_session):
        """测试按分类获取课程"""
        courses = [
            Course(
                id=f"cat-course-{i:03d}",
                title=f"课程{i}",
                category="constitution" if i % 2 == 0 else "season"
            )
            for i in range(1, 11)
        ]
        db_session.add_all(courses)
        db_session.commit()

        service = CourseService()
        result, total = service.get_courses_list(db_session, category="constitution")

        assert all(item.category == "constitution" for item in result)

    def test_search_courses(self, db_session):
        """测试搜索课程"""
        course = Course(
            id="search-course-001",
            title="气虚质养生方法",
            description="详细介绍气虚质的调理方法",
            tags=["气虚质", "健脾"]
        )
        db_session.add(course)
        db_session.commit()

        service = CourseService()

        # 搜索标题
        result, total = service.get_courses_list(db_session, search="气虚质")
        assert total > 0

    def test_increment_view_count(self, db_session):
        """测试增加观看次数"""
        course = Course(
            id="view-course-001",
            title="测试课程",
            category="constitution",
            view_count=100
        )
        db_session.add(course)
        db_session.commit()

        service = CourseService()
        service.increment_view_count("view-course-001", db_session)

        db_session.refresh(course)
        assert course.view_count == 101

    def test_get_courses_by_season(self, db_session):
        """测试按季节获取课程"""
        courses = [
            Course(
                id=f"season-{i:03d}",
                title=f"课程{i}",
                category="season",
                subcategory="spring" if i % 4 == 0 else "summer" if i % 4 == 1 else "autumn" if i % 4 == 2 else "winter"
            )
            for i in range(1, 9)
        ]
        db_session.add_all(courses)
        db_session.commit()

        service = CourseService()
        result = service.get_courses_by_season("spring", db_session)

        assert all(item.subcategory == "spring" for item in result)

    def test_get_courses_by_content_type(self, db_session):
        """测试按内容类型获取课程"""
        courses = [
            Course(
                id=f"content-{i:03d}",
                title=f"课程{i}",
                category="constitution",
                content_type="video" if i % 2 == 0 else "article"
            )
            for i in range(1, 11)
        ]
        db_session.add_all(courses)
        db_session.commit()

        service = CourseService()
        result, total = service.get_courses_list(db_session, content_type="video")

        assert all(item.content_type == "video" for item in result)

    def test_course_not_found(self, db_session):
        """测试课程不存在"""
        service = CourseService()
        result = service.get_course_by_id("non-existent-id", db_session)

        assert result is None

    def test_get_courses_list_pagination(self, db_session):
        """测试分页功能"""
        courses = [
            Course(
                id=f"page-{i:03d}",
                title=f"课程{i}",
                category="constitution"
            )
            for i in range(1, 31)
        ]
        db_session.add_all(courses)
        db_session.commit()

        service = CourseService()
        courses_page1, total = service.get_courses_list(db_session, skip=0, limit=10)
        courses_page2, _ = service.get_courses_list(db_session, skip=10, limit=10)

        assert total == 30
        assert len(courses_page1) == 10
        assert len(courses_page2) == 10

    def test_is_valid_constitution_code(self, db_session):
        """测试体质代码验证"""
        service = CourseService()

        valid_codes = ["peace", "qi_deficiency", "yang_deficiency"]

        for code in valid_codes:
            assert service.is_valid_constitution_code(code) is True

        invalid_codes = ["invalid", "wrong"]
        for code in invalid_codes:
            assert service.is_valid_constitution_code(code) is False

    def test_increment_view_count_nonexistent(self, db_session):
        """测试增加不存在课程的浏览次数（不应报错）"""
        service = CourseService()
        # 应该不报错，只是没有效果
        service.increment_view_count("non-existent-id", db_session)
