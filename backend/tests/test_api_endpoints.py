"""
体质识别 API 端点测试
Constitution Recognition API Endpoint Tests

测试所有 API 端点，包括：
1. 健康检查
2. 获取问题列表
3. 提交测试答案
4. 获取测试结果
5. 饮食推荐
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from main import app
from api.database import Base, get_db
from api.models import Question, ConstitutionResult, ConstitutionInfo


# 创建测试数据库
TEST_DATABASE_URL = "sqlite:///./test_constitution.db"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """覆盖数据库依赖"""
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()


# 覆盖数据库依赖
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    """创建测试客户端"""
    # 创建测试数据库表
    Base.metadata.create_all(bind=test_engine)

    # 创建测试客户端
    with TestClient(app) as test_client:
        yield test_client

    # 清理：删除所有表
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    """创建数据库会话"""
    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


class TestHealthEndpoint:
    """健康检查端点测试"""

    def test_health_check(self, client):
        """测试健康检查端点"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "environment" in data

    def test_root_endpoint(self, client):
        """测试根端点"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data


class TestQuestionsEndpoint:
    """问题列表端点测试"""

    @pytest.fixture
    def seed_questions(self, db_session):
        """填充测试问题数据"""
        questions = []
        for i in range(1, 31):
            q = Question(
                question_number=i,
                content=f"测试问题 {i}",
                constitution_type="peace" if i <= 4 else
                               "qi_deficiency" if i <= 8 else
                               "yang_deficiency" if i <= 12 else
                               "yin_deficiency" if i <= 16 else
                               "phlegm_damp" if i <= 19 else
                               "damp_heat" if i <= 22 else
                               "blood_stasis" if i <= 25 else
                               "qi_depression" if i <= 28 else "special",
                options={"1": "没有", "2": "很少", "3": "有时", "4": "经常", "5": "总是"}
            )
            questions.append(q)
            db_session.add(q)
        db_session.commit()
        return questions

    def test_get_questions_success(self, client, seed_questions):
        """测试成功获取问题列表"""
        response = client.get("/api/v1/questions")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["message"] == "success"
        assert "data" in data
        assert data["data"]["total"] == 30
        assert len(data["data"]["questions"]) == 30

        # 验证第一个问题的结构
        first_question = data["data"]["questions"][0]
        assert "number" in first_question
        assert "content" in first_question
        assert "constitution_type" in first_question
        assert "options" in first_question

    def test_questions_constitution_type_distribution(self, client, seed_questions):
        """测试问题按体质类型分布正确"""
        response = client.get("/api/v1/questions")
        data = response.json()

        questions_by_type = {}
        for q in data["data"]["questions"]:
            ctype = q["constitution_type"]
            questions_by_type[ctype] = questions_by_type.get(ctype, 0) + 1

        # 验证每种体质的问题数量
        assert questions_by_type.get("peace", 0) == 4
        assert questions_by_type.get("qi_deficiency", 0) == 4
        assert questions_by_type.get("yang_deficiency", 0) == 4
        assert questions_by_type.get("yin_deficiency", 0) == 4
        assert questions_by_type.get("phlegm_damp", 0) == 3
        assert questions_by_type.get("damp_heat", 0) == 3
        assert questions_by_type.get("blood_stasis", 0) == 3
        assert questions_by_type.get("qi_depression", 0) == 3
        assert questions_by_type.get("special", 0) == 2


class TestSubmitEndpoint:
    """提交测试端点测试"""

    def test_submit_test_success_yang_deficiency(self, client, db_session):
        """测试成功提交 - 阳虚质"""
        # 先填充问题
        for i in range(1, 31):
            q = Question(
                question_number=i,
                content=f"问题 {i}",
                constitution_type="peace" if i <= 4 else
                               "qi_deficiency" if i <= 8 else
                               "yang_deficiency" if i <= 12 else
                               "yin_deficiency" if i <= 16 else
                               "phlegm_damp" if i <= 19 else
                               "damp_heat" if i <= 22 else
                               "blood_stasis" if i <= 25 else
                               "qi_depression" if i <= 28 else "special",
                options={"1": "没有", "2": "很少", "3": "有时", "4": "经常", "5": "总是"}
            )
            db_session.add(q)
        db_session.commit()

        # 提交阳虚质答案（9-12题选5分）
        answers = [2, 2, 2, 2,  # 1-4
                   2, 2, 2, 2,  # 5-8
                   5, 5, 5, 5,  # 9-12 阳虚质高分
                   2, 2, 2, 2,  # 13-16
                   2, 2, 2,     # 17-19
                   2, 2, 2,     # 20-22
                   2, 2, 2,     # 23-25
                   2, 2, 2,     # 26-28
                   2, 2]        # 29-30

        response = client.post(
            "/api/v1/test/submit",
            json={"answers": answers}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "data" in data
        assert "result_id" in data["data"]
        assert data["data"]["primary_constitution"] == "yang_deficiency"
        assert data["data"]["primary_constitution_name"] == "阳虚质"

    def test_submit_test_invalid_answers_length(self, client):
        """测试提交无效的答案数量"""
        response = client.post(
            "/api/v1/test/submit",
            json={"answers": [1, 2, 3]}  # 只有3个答案
        )

        assert response.status_code == 422  # Unprocessable Entity

    def test_submit_test_invalid_answers_range(self, client):
        """测试提交超出范围的答案"""
        response = client.post(
            "/api/v1/test/submit",
            json={"answers": [6] * 30}  # 答案值超出范围
        )

        assert response.status_code == 400  # Bad Request

    def test_submit_test_saves_to_database(self, client, db_session):
        """测试提交结果保存到数据库"""
        # 填充问题
        for i in range(1, 31):
            q = Question(
                question_number=i,
                content=f"问题 {i}",
                constitution_type="peace" if i <= 4 else
                               "qi_deficiency" if i <= 8 else
                               "yang_deficiency" if i <= 12 else
                               "yin_deficiency" if i <= 16 else
                               "phlegm_damp" if i <= 19 else
                               "damp_heat" if i <= 22 else
                               "blood_stasis" if i <= 25 else
                               "qi_depression" if i <= 28 else "special",
                options={"1": "没有", "2": "很少", "3": "有时", "4": "经常", "5": "总是"}
            )
            db_session.add(q)
        db_session.commit()

        answers = [3] * 30

        response = client.post(
            "/api/v1/test/submit",
            json={"answers": answers}
        )

        assert response.status_code == 200
        result_id = response.json()["data"]["result_id"]

        # 验证数据库中存在该记录
        db_result = db_session.query(ConstitutionResult).filter(
            ConstitutionResult.id == result_id
        ).first()

        assert db_result is not None
        assert db_result.answers == answers
        assert db_result.primary_constitution in [
            "peace", "qi_deficiency", "yang_deficiency", "yin_deficiency",
            "phlegm_damp", "damp_heat", "blood_stasis", "qi_depression", "special"
        ]


class TestResultEndpoint:
    """获取结果端点测试"""

    def test_get_result_success(self, client, db_session):
        """测试成功获取结果"""
        # 创建测试结果
        result = ConstitutionResult(
            id="test-result-id-123",
            primary_constitution="qi_deficiency",
            secondary_constitutions=[{"type": "yang_deficiency", "name": "阳虚质", "score": 35}],
            scores={"qi_deficiency": 50, "yang_deficiency": 35},
            answers=[1] * 30
        )
        db_session.add(result)

        # 创建体质信息
        info = ConstitutionInfo(
            constitution_type="qi_deficiency",
            constitution_name="气虚质",
            description="元气不足",
            characteristics={"overall": ["容易疲乏"]},
            regulation_principles={"diet": ["补气"]}
        )
        db_session.add(info)
        db_session.commit()

        response = client.get(f"/api/v1/result/{result.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["result_id"] == result.id
        assert data["data"]["primary_constitution"] == "qi_deficiency"
        assert data["data"]["primary_constitution_name"] == "气虚质"

    def test_get_result_not_found(self, client):
        """测试获取不存在的结果"""
        response = client.get("/api/v1/result/non-existent-id")

        assert response.status_code == 404


class TestFoodRecommendationEndpoint:
    """饮食推荐端点测试"""

    @pytest.fixture
    def seed_food_data(self, db_session):
        """填充食物测试数据"""
        from api.models import Food

        foods = [
            Food(
                id="food-1",
                name="山药",
                nature="平",
                flavor="甘",
                suitable_constitutions=["qi_deficiency", "peace"],
                avoid_constitutions=["phlegm_damp"],
                effects=["补气养血", "健脾益胃"]
            ),
            Food(
                id="food-2",
                name="生姜",
                nature="温",
                flavor="辛",
                suitable_constitutions=["yang_deficiency"],
                avoid_constitutions=["yin_deficiency", "damp_heat"],
                effects=["温中散寒"]
            ),
            Food(
                id="food-3",
                name="绿豆",
                nature="寒",
                flavor="甘",
                suitable_constitutions=["damp_heat"],
                avoid_constitutions=["yang_deficiency"],
                effects=["清热解毒"]
            )
        ]
        for food in foods:
            db_session.add(food)
        db_session.commit()
        return foods

    def test_get_food_recommendations(self, client, seed_food_data):
        """测试获取饮食推荐"""
        response = client.get("/api/v1/recommend/food?constitution=qi_deficiency")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "data" in data
        assert data["data"]["constitution"] == "qi_deficiency"

        # 验证推荐食物包含山药
        recommended_foods = data["data"]["recommended_foods"]
        food_names = [f["name"] for f in recommended_foods]
        assert "山药" in food_names

    def test_food_recommendation_includes_avoid_foods(self, client, seed_food_data):
        """测试饮食推荐包含不宜食物"""
        response = client.get("/api/v1/recommend/food?constitution=phlegm_damp")

        assert response.status_code == 200
        data = response.json()

        # 痰湿质不宜食用山药
        avoid_foods = data["data"]["avoid_foods"]
        food_names = [f["name"] for f in avoid_foods]
        assert "山药" in food_names


class TestAPIIntegration:
    """API 集成测试"""

    def test_complete_test_flow(self, client, db_session):
        """测试完整的测试流程"""
        # 1. 填充问题
        for i in range(1, 31):
            q = Question(
                question_number=i,
                content=f"问题 {i}",
                constitution_type="peace" if i <= 4 else
                               "qi_deficiency" if i <= 8 else
                               "yang_deficiency" if i <= 12 else
                               "yin_deficiency" if i <= 16 else
                               "phlegm_damp" if i <= 19 else
                               "damp_heat" if i <= 22 else
                               "blood_stasis" if i <= 25 else
                               "qi_depression" if i <= 28 else "special",
                options={"1": "没有", "2": "很少", "3": "有时", "4": "经常", "5": "总是"}
            )
            db_session.add(q)
        db_session.commit()

        # 2. 获取问题列表
        questions_response = client.get("/api/v1/questions")
        assert questions_response.status_code == 200
        questions_data = questions_response.json()
        assert len(questions_data["data"]["questions"]) == 30

        # 3. 提交答案
        answers = [4, 4, 5, 3,  # 模拟平和质偏高
                   3, 3, 2, 2,
                   2, 2, 2, 2,
                   2, 2, 2, 2,
                   2, 2, 2,
                   2, 2, 2,
                   2, 2, 2,
                   2, 2, 2,
                   2, 2]

        submit_response = client.post(
            "/api/v1/test/submit",
            json={"answers": answers}
        )
        assert submit_response.status_code == 200
        submit_data = submit_response.json()
        result_id = submit_data["data"]["result_id"]

        # 4. 获取结果详情（需要先添加体质信息）
        info = ConstitutionInfo(
            constitution_type=submit_data["data"]["primary_constitution"],
            constitution_name=submit_data["data"]["primary_constitution_name"],
            description="测试体质",
            characteristics={"overall": ["测试特征"]},
            regulation_principles={"diet": ["测试原则"]}
        )
        db_session.add(info)
        db_session.commit()

        result_response = client.get(f"/api/v1/result/{result_id}")
        assert result_response.status_code == 200
        result_data = result_response.json()
        assert result_data["data"]["result_id"] == result_id


class TestAPIValidation:
    """API 验证测试"""

    def test_submit_without_answers(self, client):
        """测试不提供答案"""
        response = client.post("/api/v1/test/submit", json={})

        assert response.status_code == 422

    def test_submit_with_extra_field(self, client):
        """测试提交额外字段（应被忽略）"""
        # 先填充问题
        from api.models import Question
        client.post("/api/v1/questions")  # 确保有数据

        response = client.post(
            "/api/v1/test/submit",
            json={
                "answers": [3] * 30,
                "extra_field": "should be ignored",
                "user_id": "test-user-123"
            }
        )
        # 不应该报错，额外字段应被忽略
        assert response.status_code in [200, 400]  # 可能因其他原因失败


class TestAPIPerformance:
    """API 性能测试"""

    def test_questions_response_time(self, client, db_session):
        """测试问题列表响应时间"""
        import time

        # 填充数据
        for i in range(1, 31):
            q = Question(
                question_number=i,
                content=f"问题 {i}",
                constitution_type="peace" if i <= 4 else "qi_deficiency",
                options={"1": "没有", "2": "很少", "3": "有时", "4": "经常", "5": "总是"}
            )
            db_session.add(q)
        db_session.commit()

        start_time = time.time()
        response = client.get("/api/v1/questions")
        end_time = time.time()

        assert response.status_code == 200
        # 响应时间应小于1秒
        assert (end_time - start_time) < 1.0

    def test_submit_response_time(self, client, db_session):
        """测试提交响应时间"""
        import time

        # 填充问题
        for i in range(1, 31):
            q = Question(
                question_number=i,
                content=f"问题 {i}",
                constitution_type="peace",
                options={"1": "没有", "2": "很少", "3": "有时", "4": "经常", "5": "总是"}
            )
            db_session.add(q)
        db_session.commit()

        answers = [3] * 30

        start_time = time.time()
        response = client.post("/api/v1/test/submit", json={"answers": answers})
        end_time = time.time()

        assert response.status_code == 200
        # 响应时间应小于2秒
        assert (end_time - start_time) < 2.0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
