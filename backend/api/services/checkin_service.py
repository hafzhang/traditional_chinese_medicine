"""
Check-In Service
健康打卡服务层 - MVP
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
import calendar

from api.models import UserCheckIn, User


class CheckInService:
    """健康打卡服务类"""

    def create_weekly_checkin(
        self,
        user_id: str,
        week_number: int,
        db: Session
    ) -> UserCheckIn:
        """
        创建新的周打卡记录

        Args:
            user_id: 用户ID
            week_number: 第几周
            db: 数据库会话

        Returns:
            创建的打卡记录对象
        """
        # 初始化7天的空打卡数据
        daily_entries = []
        today = date.today()

        # 计算本周的起始日期（假设周一为第一天）
        start_of_week = today - timedelta(days=today.weekday())

        for day in range(7):
            day_date = start_of_week + timedelta(days=day)
            daily_entries.append({
                "day": day + 1,
                "date": day_date.strftime("%Y-%m-%d"),
                "weekday": calendar.day_name[day_date.weekday()],
                "exercises_completed": [],
                "exercise_minutes": 0,
                "routine_followed": False,
                "mood_score": None,
                "energy_level": None,
                "sleep_hours": None,
                "notes": "",
                "completed": False
            })

        checkin = UserCheckIn(
            user_id=user_id,
            week_number=week_number,
            daily_entries=daily_entries,
            exercise_completion_rate=0.0,
            routine_adherence_rate=0.0
        )

        db.add(checkin)
        db.commit()
        db.refresh(checkin)

        return checkin

    def get_checkin_by_id(self, checkin_id: str, db: Session) -> Optional[UserCheckIn]:
        """
        根据ID获取打卡记录

        Args:
            checkin_id: 打卡记录ID
            db: 数据库会话

        Returns:
            打卡记录对象或None
        """
        return db.query(UserCheckIn).filter(UserCheckIn.id == checkin_id).first()

    def get_user_checkins(
        self,
        user_id: str,
        db: Session,
        skip: int = 0,
        limit: int = 10
    ) -> tuple[List[UserCheckIn], int]:
        """
        获取用户的打卡记录列表

        Args:
            user_id: 用户ID
            db: 数据库会话
            skip: 跳过数量
            limit: 限制数量

        Returns:
            (打卡记录列表, 总数)
        """
        query = db.query(UserCheckIn).filter(UserCheckIn.user_id == user_id)
        total = query.count()
        checkins = query.order_by(UserCheckIn.week_number.desc()).offset(skip).limit(limit).all()

        return checkins, total

    def get_current_week_checkin(
        self,
        user_id: str,
        db: Session
    ) -> Optional[UserCheckIn]:
        """
        获取用户本周的打卡记录

        Args:
            user_id: 用户ID
            db: 数据库会话

        Returns:
            本周打卡记录或None
        """
        # 获取最新的打卡记录
        checkin = db.query(UserCheckIn).filter(
            UserCheckIn.user_id == user_id
        ).order_by(UserCheckIn.week_number.desc()).first()

        # 检查是否是本周的记录
        if checkin:
            today = date.today()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)

            for entry in checkin.daily_entries:
                entry_date = datetime.strptime(entry["date"], "%Y-%m-%d").date()
                if start_of_week <= entry_date <= end_of_week:
                    return checkin

        return None

    def update_daily_entry(
        self,
        checkin_id: str,
        day: int,
        data: Dict[str, Any],
        db: Session
    ) -> Optional[UserCheckIn]:
        """
        更新某日的打卡数据

        Args:
            checkin_id: 打卡记录ID
            day: 第几天 (1-7)
            data: 打卡数据
            db: 数据库会话

        Returns:
            更新后的打卡记录对象或None
        """
        checkin = self.get_checkin_by_id(checkin_id, db)
        if not checkin:
            return None

        if day < 1 or day > 7:
            return None

        # 更新指定天的数据
        for i, entry in enumerate(checkin.daily_entries):
            if entry["day"] == day:
                # 更新字段
                if "exercises_completed" in data:
                    checkin.daily_entries[i]["exercises_completed"] = data["exercises_completed"]
                if "exercise_minutes" in data:
                    checkin.daily_entries[i]["exercise_minutes"] = data["exercise_minutes"]
                if "routine_followed" in data:
                    checkin.daily_entries[i]["routine_followed"] = data["routine_followed"]
                if "mood_score" in data:
                    checkin.daily_entries[i]["mood_score"] = data["mood_score"]
                if "energy_level" in data:
                    checkin.daily_entries[i]["energy_level"] = data["energy_level"]
                if "sleep_hours" in data:
                    checkin.daily_entries[i]["sleep_hours"] = data["sleep_hours"]
                if "notes" in data:
                    checkin.daily_entries[i]["notes"] = data["notes"]
                if "completed" in data:
                    checkin.daily_entries[i]["completed"] = data["completed"]
                break

        # 重新计算完成率
        self._recalculate_completion_rates(checkin)

        db.commit()
        db.refresh(checkin)

        return checkin

    def _recalculate_completion_rates(self, checkin: UserCheckIn) -> None:
        """
        重新计算完成率

        Args:
            checkin: 打卡记录对象
        """
        if not checkin.daily_entries:
            checkin.exercise_completion_rate = 0.0
            checkin.routine_adherence_rate = 0.0
            return

        # 计算运动完成率（有运动即视为完成）
        exercise_days = sum(1 for entry in checkin.daily_entries if entry.get("exercises_completed"))
        total_days = len(checkin.daily_entries)
        checkin.exercise_completion_rate = (exercise_days / total_days * 100) if total_days > 0 else 0

        # 计算作息遵守率
        routine_days = sum(1 for entry in checkin.daily_entries if entry.get("routine_followed"))
        checkin.routine_adherence_rate = (routine_days / total_days * 100) if total_days > 0 else 0

        # 计算平均情绪分
        mood_scores = [entry.get("mood_score") for entry in checkin.daily_entries if entry.get("mood_score")]
        if mood_scores:
            checkin.mood_score = sum(mood_scores) / len(mood_scores)

    def get_week_summary(
        self,
        checkin_id: str,
        db: Session
    ) -> Optional[Dict[str, Any]]:
        """
        获取周打卡汇总

        Args:
            checkin_id: 打卡记录ID
            db: 数据库会话

        Returns:
            周汇总数据
        """
        checkin = self.get_checkin_by_id(checkin_id, db)
        if not checkin:
            return None

        # 统计数据
        completed_days = sum(1 for entry in checkin.daily_entries if entry.get("completed"))
        total_exercise_minutes = sum(entry.get("exercise_minutes", 0) for entry in checkin.daily_entries)
        routine_followed_days = sum(1 for entry in checkin.daily_entries if entry.get("routine_followed"))

        # 情绪统计
        mood_scores = [entry.get("mood_score") for entry in checkin.daily_entries if entry.get("mood_score")]
        avg_mood = sum(mood_scores) / len(mood_scores) if mood_scores else None

        # 能量统计
        energy_levels = [entry.get("energy_level") for entry in checkin.daily_entries if entry.get("energy_level")]
        avg_energy = sum(energy_levels) / len(energy_levels) if energy_levels else None

        # 睡眠统计
        sleep_hours = [entry.get("sleep_hours") for entry in checkin.daily_entries if entry.get("sleep_hours")]
        avg_sleep = sum(sleep_hours) / len(sleep_hours) if sleep_hours else None

        return {
            "week_number": checkin.week_number,
            "total_days": 7,
            "completed_days": completed_days,
            "completion_rate": (completed_days / 7 * 100) if 7 > 0 else 0,
            "exercise_completion_rate": checkin.exercise_completion_rate,
            "routine_adherence_rate": checkin.routine_adherence_rate,
            "total_exercise_minutes": total_exercise_minutes,
            "avg_exercise_minutes_per_day": (total_exercise_minutes / 7) if 7 > 0 else 0,
            "routine_followed_days": routine_followed_days,
            "avg_mood_score": avg_mood,
            "avg_energy_level": avg_energy,
            "avg_sleep_hours": avg_sleep,
            "symptoms_improved": checkin.symptoms_improved or [],
            "ai_recommendations": checkin.ai_recommendations,
            "coach_feedback": checkin.coach_feedback
        }

    def calculate_progress_streak(
        self,
        user_id: str,
        db: Session
    ) -> int:
        """
        计算用户连续打卡天数

        Args:
            user_id: 用户ID
            db: 数据库会话

        Returns:
            连续打卡天数
        """
        checkins, _ = self.get_user_checkins(user_id, db, limit=100)

        if not checkins:
            return 0

        streak = 0
        for checkin in reversed(checkins):  # 从最近的开始
            for entry in reversed(checkin.daily_entries):
                if entry.get("completed"):
                    streak += 1
                else:
                    # 如果今天没完成，检查是否是今天
                    entry_date = datetime.strptime(entry["date"], "%Y-%m-%d").date()
                    if entry_date < date.today():
                        return streak
                    return streak

        return streak

    def generate_weekly_report(
        self,
        checkin_id: str,
        db: Session
    ) -> Optional[Dict[str, Any]]:
        """
        生成周报数据

        Args:
            checkin_id: 打卡记录ID
            db: 数据库会话

        Returns:
            周报数据
        """
        summary = self.get_week_summary(checkin_id, db)
        if not summary:
            return None

        checkin = self.get_checkin_by_id(checkin_id, db)

        # 按天统计
        daily_stats = []
        for entry in checkin.daily_entries:
            daily_stats.append({
                "day": entry["day"],
                "date": entry["date"],
                "weekday": entry["weekday"],
                "completed": entry.get("completed", False),
                "exercises_count": len(entry.get("exercises_completed", [])),
                "exercise_minutes": entry.get("exercise_minutes", 0),
                "routine_followed": entry.get("routine_followed", False),
                "mood_score": entry.get("mood_score"),
                "energy_level": entry.get("energy_level"),
                "sleep_hours": entry.get("sleep_hours"),
                "notes": entry.get("notes", "")
            })

        return {
            **summary,
            "daily_stats": daily_stats
        }

    def get_user_progress_overview(
        self,
        user_id: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        获取用户整体进度概览

        Args:
            user_id: 用户ID
            db: 数据库会话

        Returns:
            进度概览数据
        """
        checkins, total = self.get_user_checkins(user_id, db, limit=100)

        if not checkins:
            return {
                "total_weeks": 0,
                "current_streak": 0,
                "total_exercise_minutes": 0,
                "avg_completion_rate": 0,
                "latest_week": None
            }

        total_exercise_minutes = 0
        total_completion_rate = 0

        for checkin in checkins:
            for entry in checkin.daily_entries:
                total_exercise_minutes += entry.get("exercise_minutes", 0)
            total_completion_rate += (checkin.exercise_completion_rate or 0)

        return {
            "total_weeks": total,
            "current_streak": self.calculate_progress_streak(user_id, db),
            "total_exercise_minutes": total_exercise_minutes,
            "avg_completion_rate": (total_completion_rate / total) if total > 0 else 0,
            "latest_week": {
                "week_number": checkins[0].week_number,
                "completion_rate": checkins[0].exercise_completion_rate,
                "mood_score": checkins[0].mood_score
            }
        }
