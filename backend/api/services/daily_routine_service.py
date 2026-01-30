"""
Daily Routine Service
起居作息服务层 - MVP
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime, time

from api.models import DailyRoutine


class DailyRoutineService:
    """起居作息服务类"""

    # 有效的体质代码
    VALID_CONSTITUTIONS = {
        "peace", "qi_deficiency", "yang_deficiency", "yin_deficiency",
        "phlegm_damp", "damp_heat", "blood_stasis", "qi_depression", "special"
    }

    # 季节列表
    VALID_SEASONS = {"spring", "summer", "autumn", "winter"}

    def is_valid_constitution_code(self, code: str) -> bool:
        """验证体质代码是否有效"""
        return code in self.VALID_CONSTITUTIONS

    def get_routine_by_id(self, routine_id: str, db: Session) -> Optional[DailyRoutine]:
        """
        根据ID获取作息方案详情

        Args:
            routine_id: 作息方案ID
            db: 数据库会话

        Returns:
            作息方案对象或None
        """
        return db.query(DailyRoutine).filter(DailyRoutine.id == routine_id).first()

    def get_routine_by_constitution(
        self,
        constitution_code: str,
        db: Session
    ) -> Optional[DailyRoutine]:
        """
        根据体质获取作息方案

        Args:
            constitution_code: 体质代码
            db: 数据库会话

        Returns:
            作息方案对象或None
        """
        if not self.is_valid_constitution_code(constitution_code):
            return None

        routine = db.query(DailyRoutine).filter(
            DailyRoutine.target_constitutions.contains(constitution_code)
        ).first()

        return routine

    def get_all_routines(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 10
    ) -> tuple[List[DailyRoutine], int]:
        """
        获取所有作息方案列表

        Args:
            db: 数据库会话
            skip: 跳过数量
            limit: 限制数量

        Returns:
            (作息方案列表, 总数)
        """
        query = db.query(DailyRoutine)
        total = query.count()
        routines = query.offset(skip).limit(limit).all()

        return routines, total

    def get_seasonal_adjustment(
        self,
        constitution_code: str,
        season: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        获取季节性作息调整

        Args:
            constitution_code: 体质代码
            season: 季节 (spring/summer/autumn/winter)
            db: 数据库会话

        Returns:
            季节调整方案
        """
        if not self.is_valid_constitution_code(constitution_code):
            return {}
        if season not in self.VALID_SEASONS:
            return {}

        routine = self.get_routine_by_constitution(constitution_code, db)
        if not routine or not routine.seasonal_adjustments:
            return {}

        # 获取对应季节的调整
        seasonal_data = routine.seasonal_adjustments
        season_key = {
            "spring": "spring",
            "summer": "summer",
            "autumn": "autumn",
            "winter": "winter"
        }.get(season, season)

        return seasonal_data.get(season_key, {})

    def get_current_season(self) -> str:
        """
        获取当前季节

        Returns:
            当前季节 (spring/summer/autumn/winter)
        """
        month = datetime.now().month
        if month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        elif month in [9, 10, 11]:
            return "autumn"
        else:
            return "winter"

    def generate_today_schedule(
        self,
        user_id: str,
        constitution_code: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        生成今日作息时间表

        Args:
            user_id: 用户ID
            constitution_code: 体质代码
            db: 数据库会话

        Returns:
            {
                "date": "2024-01-15",
                "season": "winter",
                "wake_time": "06:30",
                "sleep_time": "22:00",
                "schedule": [
                    {"time": "06:30", "activity": "起床", "type": "morning"},
                    ...
                ]
            }
        """
        routine = self.get_routine_by_constitution(constitution_code, db)
        if not routine:
            return {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "season": self.get_current_season(),
                "schedule": []
            }

        current_season = self.get_current_season()
        schedule = []

        # 构建完整的时间表
        # 晨间
        if routine.morning_routine:
            for item in routine.morning_routine:
                schedule.append({
                    **item,
                    "type": "morning",
                    "period": "晨间"
                })

        # 午间
        if routine.afternoon_routine:
            for item in routine.afternoon_routine:
                schedule.append({
                    **item,
                    "type": "afternoon",
                    "period": "午间"
                })

        # 晚间
        if routine.evening_routine:
            for item in routine.evening_routine:
                schedule.append({
                    **item,
                    "type": "evening",
                    "period": "晚间"
                })

        # 按时间排序
        schedule.sort(key=lambda x: x.get("time", "00:00"))

        # 应用季节调整
        seasonal_adjustment = self.get_seasonal_adjustment(constitution_code, current_season, db)
        if seasonal_adjustment:
            # 可以根据季节调整某些活动
            for item in schedule:
                activity_name = item.get("activity", "")
                if activity_name in seasonal_adjustment.get("modified_activities", {}):
                    item["seasonal_note"] = seasonal_adjustment["modified_activities"][activity_name]

        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "season": current_season,
            "season_name": self._get_season_name(current_season),
            "wake_time": routine.wake_time,
            "sleep_time": routine.sleep_time,
            "meal_timings": routine.meal_timings or {},
            "schedule": schedule,
            "tips": routine.tips or []
        }

    def _get_season_name(self, season: str) -> str:
        """获取季节中文名"""
        season_names = {
            "spring": "春季",
            "summer": "夏季",
            "autumn": "秋季",
            "winter": "冬季"
        }
        return season_names.get(season, season)

    def get_constitution_routine_summary(
        self,
        constitution_code: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        获取体质作息方案摘要

        Args:
            constitution_code: 体质代码
            db: 数据库会话

        Returns:
            作息方案摘要
        """
        routine = self.get_routine_by_constitution(constitution_code, db)
        if not routine:
            return {}

        return {
            "id": routine.id,
            "name": routine.name,
            "description": routine.description,
            "wake_time": routine.wake_time,
            "sleep_time": routine.sleep_time,
            "target_constitutions": routine.target_constitutions,
            "has_seasonal_adjustments": bool(routine.seasonal_adjustments),
            "tips_count": len(routine.tips) if routine.tips else 0
        }

    def get_routine_with_seasonal_info(
        self,
        constitution_code: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        获取作息方案及季节信息

        Args:
            constitution_code: 体质代码
            db: 数据库会话

        Returns:
            包含当前季节调整的完整作息方案
        """
        routine = self.get_routine_by_constitution(constitution_code, db)
        if not routine:
            return {}

        current_season = self.get_current_season()
        seasonal_adjustment = self.get_seasonal_adjustment(constitution_code, current_season, db)

        return {
            "routine": {
                "id": routine.id,
                "name": routine.name,
                "description": routine.description,
                "wake_time": routine.wake_time,
                "sleep_time": routine.sleep_time,
                "morning_routine": routine.morning_routine,
                "afternoon_routine": routine.afternoon_routine,
                "evening_routine": routine.evening_routine,
                "meal_timings": routine.meal_timings,
                "tips": routine.tips
            },
            "current_season": {
                "code": current_season,
                "name": self._get_season_name(current_season),
                "adjustment": seasonal_adjustment
            }
        }

    def create_routine(
        self,
        name: str,
        target_constitutions: List[str],
        wake_time: str,
        sleep_time: str,
        morning_routine: List[Dict],
        afternoon_routine: List[Dict],
        evening_routine: List[Dict],
        db: Session,
        **kwargs
    ) -> DailyRoutine:
        """
        创建新的作息方案

        Args:
            name: 方案名称
            target_constitutions: 目标体质列表
            wake_time: 起床时间
            sleep_time: 睡眠时间
            morning_routine: 晨间安排
            afternoon_routine: 午间安排
            evening_routine: 晚间安排
            db: 数据库会话
            **kwargs: 其他可选字段

        Returns:
            创建的作息方案对象
        """
        routine = DailyRoutine(
            name=name,
            target_constitutions=target_constitutions,
            wake_time=wake_time,
            sleep_time=sleep_time,
            morning_routine=morning_routine,
            afternoon_routine=afternoon_routine,
            evening_routine=evening_routine,
            description=kwargs.get("description"),
            seasonal_adjustments=kwargs.get("seasonal_adjustments"),
            meal_timings=kwargs.get("meal_timings"),
            tips=kwargs.get("tips", [])
        )

        db.add(routine)
        db.commit()
        db.refresh(routine)

        return routine
