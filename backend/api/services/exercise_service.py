"""
Exercise Service
运动/功法服务层 - MVP
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from api.models import Exercise


class ExerciseService:
    """运动/功法服务类"""

    # 有效的体质代码
    VALID_CONSTITUTIONS = {
        "peace", "qi_deficiency", "yang_deficiency", "yin_deficiency",
        "phlegm_damp", "damp_heat", "blood_stasis", "qi_depression", "special"
    }

    # 有效的运动类型
    VALID_EXERCISE_TYPES = {
        "qigong", "tai_chi", "baduanjin", "yijinjing", "wuqinxi", "breathing"
    }

    # 有效的难度级别
    VALID_DIFFICULTY_LEVELS = {"beginner", "intermediate", "advanced"}

    def is_valid_constitution_code(self, code: str) -> bool:
        """验证体质代码是否有效"""
        return code in self.VALID_CONSTITUTIONS

    def get_exercise_by_id(self, exercise_id: str, db: Session) -> Optional[Exercise]:
        """
        根据ID获取运动详情

        Args:
            exercise_id: 运动ID
            db: 数据库会话

        Returns:
            运动对象或None
        """
        return db.query(Exercise).filter(Exercise.id == exercise_id).first()

    def get_exercises_list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        exercise_type: Optional[str] = None,
        difficulty_level: Optional[str] = None,
        search: Optional[str] = None
    ) -> tuple[List[Exercise], int]:
        """
        获取运动列表

        Args:
            db: 数据库会话
            skip: 跳过数量
            limit: 限制数量
            exercise_type: 运动类型筛选
            difficulty_level: 难度级别筛选
            search: 搜索关键词

        Returns:
            (运动列表, 总数)
        """
        query = db.query(Exercise)

        # 筛选条件
        if exercise_type:
            query = query.filter(Exercise.exercise_type == exercise_type)
        if difficulty_level:
            query = query.filter(Exercise.difficulty_level == difficulty_level)
        if search:
            query = query.filter(
                (Exercise.name.like(f"%{search}%")) |
                (Exercise.description.like(f"%{search}%"))
            )

        # 总数
        total = query.count()

        # 分页
        exercises = query.order_by(Exercise.view_count.desc()).offset(skip).limit(limit).all()

        return exercises, total

    def get_exercises_by_constitution(
        self,
        constitution_code: str,
        db: Session,
        limit: int = 20
    ) -> List[Exercise]:
        """
        根据体质获取推荐运动

        Args:
            constitution_code: 体质代码
            db: 数据库会话
            limit: 限制数量

        Returns:
            推荐运动列表
        """
        if not self.is_valid_constitution_code(constitution_code):
            return []

        exercises = db.query(Exercise).filter(
            Exercise.target_constitutions.contains(constitution_code)
        ).order_by(Exercise.view_count.desc()).limit(limit).all()

        return exercises

    def get_exercises_by_type(
        self,
        exercise_type: str,
        db: Session,
        limit: int = 20
    ) -> List[Exercise]:
        """
        根据运动类型获取运动列表

        Args:
            exercise_type: 运动类型
            db: 数据库会话
            limit: 限制数量

        Returns:
            运动列表
        """
        if exercise_type not in self.VALID_EXERCISE_TYPES:
            return []

        exercises = db.query(Exercise).filter(
            Exercise.exercise_type == exercise_type
        ).order_by(Exercise.view_count.desc()).limit(limit).all()

        return exercises

    def get_personalized_routine(
        self,
        constitution_code: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        获取个性化运动方案（早中晚）

        Args:
            constitution_code: 体质代码
            db: 数据库会话

        Returns:
            {
                "morning": [...],  # 晨间运动（温和）
                "afternoon": [...],  # 午间运动（适中）
                "evening": [...]  # 晚间运动（放松）
            }
        """
        if not self.is_valid_constitution_code(constitution_code):
            return {"morning": [], "afternoon": [], "evening": []}

        # 获取所有适合该体质的运动
        all_exercises = self.get_exercises_by_constitution(constitution_code, db, limit=50)

        # 根据运动类型和难度分组
        morning = []  # 晨间：温和、易上手的运动
        afternoon = []  # 午间：中等强度运动
        evening = []  # 晚间：放松、舒缓运动

        for exercise in all_exercises:
            if exercise.difficulty_level == "beginner":
                morning.append(exercise)
            elif exercise.difficulty_level == "intermediate":
                afternoon.append(exercise)
            elif exercise.difficulty_level == "advanced":
                # 晚间可以包含一些高级但舒缓的运动
                if exercise.exercise_type in ["qigong", "breathing"]:
                    evening.append(exercise)

        # 也可以根据运动类型来分组
        # 晨间推荐：八段锦、易筋经
        morning.extend([e for e in all_exercises if e.exercise_type in ["baduanjin", "yijinjing"] and e not in morning][:3])
        # 晚间推荐：呼吸法、太极
        evening.extend([e for e in all_exercises if e.exercise_type in ["tai_chi", "breathing", "qigong"] and e not in evening][:3])

        return {
            "morning": morning[:5],
            "afternoon": afternoon[:5],
            "evening": evening[:5]
        }

    def get_exercise_plan_week(
        self,
        constitution_code: str,
        week: int,
        db: Session
    ) -> Dict[str, Any]:
        """
        获取周运动计划

        Args:
            constitution_code: 体质代码
            week: 第几周
            db: 数据库会话

        Returns:
            {
                "week": 1,
                "daily_plan": {
                    "monday": [...],
                    "tuesday": [...],
                    ...
                }
            }
        """
        if not self.is_valid_constitution_code(constitution_code):
            return {"week": week, "daily_plan": {}}

        # 获取所有适合该体质的运动
        all_exercises = self.get_exercises_by_constitution(constitution_code, db, limit=20)

        if not all_exercises:
            return {"week": week, "daily_plan": {}}

        # 简单的轮换策略
        days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        daily_plan = {}

        # 根据周数调整计划强度
        if week == 1:
            # 第一周：初学者运动
            beginner_exercises = [e for e in all_exercises if e.difficulty_level == "beginner"]
            for day in days_of_week:
                daily_plan[day] = beginner_exercises[:2] if beginner_exercises else all_exercises[:2]
        elif week == 2:
            # 第二周：混合初学者和中级
            mixed_exercises = [e for e in all_exercises if e.difficulty_level in ["beginner", "intermediate"]]
            for day in days_of_week:
                daily_plan[day] = mixed_exercises[:3] if mixed_exercises else all_exercises[:3]
        else:
            # 第三周及以后：全面运动
            for i, day in enumerate(days_of_week):
                # 轮换不同运动
                start_idx = (i * 2) % len(all_exercises)
                daily_plan[day] = all_exercises[start_idx:start_idx + 3]

        return {
            "week": week,
            "constitution": constitution_code,
            "daily_plan": daily_plan
        }

    def increment_view_count(self, exercise_id: str, db: Session) -> bool:
        """
        增加运动浏览次数

        Args:
            exercise_id: 运动ID
            db: 数据库会话

        Returns:
            是否成功
        """
        exercise = self.get_exercise_by_id(exercise_id, db)
        if exercise:
            exercise.view_count = (exercise.view_count or 0) + 1
            db.commit()
            return True
        return False

    def get_exercise_types(self, db: Session) -> List[Dict[str, str]]:
        """
        获取所有运动类型列表

        Args:
            db: 数据库会话

        Returns:
            [{"code": "qigong", "name": "气功", "name_en": "Qigong"}, ...]
        """
        exercise_types = [
            {"code": "qigong", "name": "气功", "name_en": "Qigong"},
            {"code": "tai_chi", "name": "太极拳", "name_en": "Tai Chi"},
            {"code": "baduanjin", "name": "八段锦", "name_en": "Baduanjin"},
            {"code": "yijinjing", "name": "易筋经", "name_en": "Yijinjing"},
            {"code": "wuqinxi", "name": "五禽戏", "name_en": "Wuqinxi"},
            {"code": "breathing", "name": "呼吸法", "name_en": "Breathing"},
        ]
        return exercise_types
