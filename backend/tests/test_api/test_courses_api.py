"""
课程API集成测试
Integration Tests for Course API
"""

import pytest


class TestCoursesAPI:
    """课程API集成测试"""

    def test_get_courses_list(self, client, db_session):
        """测试获取课程列表"""
        from api.models import Course
        courses = [
            Course(
                id=f"api-course-{i:03d}",
                title=f"课程{i}",
                category="constitution",
                content_type="video"
            )
            for i in range(1, 11)
        ]
        db_session.add_all(courses)
        db_session.commit()

        response = client.get("/api/v1/courses")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["total"] == 10

    def test_get_course_detail(self, client, db_session):
        """测试获取课程详情"""
        from api.models import Course
        course = Course(
            id="api-course-detail-001",
            title="气虚质养生",
            category="constitution",
            content_type="video",
            duration=120
        )
        db_session.add(course)
        db_session.commit()

        response = client.get("/api/v1/courses/api-course-detail-001")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["title"] == "气虚质养生"

    def test_get_courses_by_constitution(self, client, db_session):
        """测试按体质获取课程"""
        from api.models import Course
        courses = [
            Course(
                id=f"api-course-const-{i:03d}",
                title=f"课程{i}",
                category="constitution",
                suitable_constitutions=["qi_deficiency"] if i % 2 == 0 else []
            )
            for i in range(1, 11)
        ]
        db_session.add_all(courses)
        db_session.commit()

        response = client.get("/api/v1/courses?constitution=qi_deficiency")

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 5

    def test_get_courses_by_category(self, client, db_session):
        """测试按分类获取课程"""
        from api.models import Course
        courses = [
            Course(
                id=f"cat-api-{i:03d}",
                title=f"课程{i}",
                category="constitution" if i % 2 == 0 else "season"
            )
            for i in range(1, 11)
        ]
        db_session.add_all(courses)
        db_session.commit()

        response = client.get("/api/v1/courses?category=constitution")

        assert response.status_code == 200
        data = response.json()
        assert all(item["category"] == "constitution" for item in data["data"]["items"])

    def test_get_courses_by_season(self, client, db_session):
        """测试按季节获取课程"""
        from api.models import Course
        courses = [
            Course(
                id=f"season-api-{i:03d}",
                title=f"课程{i}",
                category="season",
                subcategory="spring" if i % 2 == 0 else "summer"
            )
            for i in range(1, 11)
        ]
        db_session.add_all(courses)
        db_session.commit()

        response = client.get("/api/v1/courses/season/spring")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["season"] == "spring"
        # 验证返回的课程数量正确（春季课程）
        assert len(data["data"]["items"]) == 5

    def test_search_courses(self, client, db_session):
        """测试搜索课程"""
        from api.models import Course
        course = Course(
            id="search-api-001",
            title="气虚质养生方法",
            tags=["气虚质", "健脾"]
        )
        db_session.add(course)
        db_session.commit()

        response = client.get("/api/v1/courses?search=气虚质")

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) > 0

    def test_course_not_found(self, client, db_session):
        """测试课程不存在"""
        response = client.get("/api/v1/courses/non-existent-id")

        assert response.status_code == 404
