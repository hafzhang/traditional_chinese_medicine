"""
Check-ins API Router
健康打卡 API 路由 - MVP
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from pydantic import BaseModel

from api.database import get_db
from api.services.checkin_service import CheckInService
from api.services.ai_feedback_service import AIFeedbackService


router = APIRouter(prefix="/checkins", tags=["checkins"])


# Request/Response Models
class CheckInCreateRequest(BaseModel):
    user_id: str
    week_number: int


class DailyEntryUpdateRequest(BaseModel):
    exercises_completed: Optional[List[str]] = []
    exercise_minutes: Optional[int] = 0
    routine_followed: Optional[bool] = False
    mood_score: Optional[int] = None
    energy_level: Optional[int] = None
    sleep_hours: Optional[float] = None
    notes: Optional[str] = ""
    completed: Optional[bool] = False


class CheckInListResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


class CheckInDetailResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


@router.post("", response_model=CheckInDetailResponse)
async def create_weekly_checkin(
    request: CheckInCreateRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    创建新的周打卡记录
    """
    service = CheckInService()
    checkin = service.create_weekly_checkin(
        user_id=request.user_id,
        week_number=request.week_number,
        db=db
    )

    return {
        "code": 0,
        "message": "Check-in created successfully",
        "data": {
            "id": checkin.id,
            "user_id": checkin.user_id,
            "week_number": checkin.week_number,
            "daily_entries": checkin.daily_entries
        }
    }


@router.get("", response_model=CheckInListResponse)
async def get_user_checkins(
    user_id: str = Query(..., description="用户ID"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(10, ge=1, le=50, description="限制数量"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取用户的打卡记录列表
    """
    service = CheckInService()
    checkins, total = service.get_user_checkins(
        user_id=user_id,
        db=db,
        skip=skip,
        limit=limit
    )

    return {
        "code": 0,
        "message": "success",
        "data": {
            "total": total,
            "items": [
                {
                    "id": c.id,
                    "user_id": c.user_id,
                    "week_number": c.week_number,
                    "exercise_completion_rate": c.exercise_completion_rate,
                    "routine_adherence_rate": c.routine_adherence_rate,
                    "mood_score": c.mood_score,
                    "created_at": c.created_at.isoformat() if c.created_at else None
                }
                for c in checkins
            ]
        }
    }


@router.get("/current/{user_id}", response_model=CheckInDetailResponse)
async def get_current_week_checkin(
    user_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取用户本周的打卡记录
    """
    service = CheckInService()
    checkin = service.get_current_week_checkin(
        user_id=user_id,
        db=db
    )

    if not checkin:
        raise HTTPException(status_code=404, detail="No check-in found for current week")

    return {
        "code": 0,
        "message": "success",
        "data": {
            "id": checkin.id,
            "user_id": checkin.user_id,
            "week_number": checkin.week_number,
            "daily_entries": checkin.daily_entries,
            "exercise_completion_rate": checkin.exercise_completion_rate,
            "routine_adherence_rate": checkin.routine_adherence_rate,
            "mood_score": checkin.mood_score,
            "ai_recommendations": checkin.ai_recommendations,
            "coach_feedback": checkin.coach_feedback
        }
    }


@router.get("/{checkin_id}", response_model=CheckInDetailResponse)
async def get_checkin_detail(
    checkin_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取打卡记录详情
    """
    service = CheckInService()
    checkin = service.get_checkin_by_id(
        checkin_id=checkin_id,
        db=db
    )

    if not checkin:
        raise HTTPException(status_code=404, detail="Check-in not found")

    return {
        "code": 0,
        "message": "success",
        "data": {
            "id": checkin.id,
            "user_id": checkin.user_id,
            "week_number": checkin.week_number,
            "daily_entries": checkin.daily_entries,
            "exercise_completion_rate": checkin.exercise_completion_rate,
            "routine_adherence_rate": checkin.routine_adherence_rate,
            "mood_score": checkin.mood_score,
            "symptoms_improved": checkin.symptoms_improved,
            "ai_recommendations": checkin.ai_recommendations,
            "coach_feedback": checkin.coach_feedback,
            "created_at": checkin.created_at.isoformat() if checkin.created_at else None,
            "updated_at": checkin.updated_at.isoformat() if checkin.updated_at else None
        }
    }


@router.put("/{checkin_id}/day/{day}", response_model=CheckInDetailResponse)
async def update_daily_entry(
    checkin_id: str,
    day: int,
    request: DailyEntryUpdateRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    更新某日的打卡数据

    day: 1-7 (第1-7天)
    """
    service = CheckInService()
    checkin = service.update_daily_entry(
        checkin_id=checkin_id,
        day=day,
        data=request.dict(exclude_unset=True),
        db=db
    )

    if not checkin:
        raise HTTPException(status_code=404, detail="Check-in not found or invalid day")

    return {
        "code": 0,
        "message": "Daily entry updated successfully",
        "data": {
            "id": checkin.id,
            "week_number": checkin.week_number,
            "daily_entries": checkin.daily_entries,
            "exercise_completion_rate": checkin.exercise_completion_rate,
            "routine_adherence_rate": checkin.routine_adherence_rate,
            "mood_score": checkin.mood_score
        }
    }


@router.get("/{checkin_id}/summary", response_model=Dict[str, Any])
async def get_week_summary(
    checkin_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取周打卡汇总
    """
    service = CheckInService()
    summary = service.get_week_summary(
        checkin_id=checkin_id,
        db=db
    )

    if not summary:
        raise HTTPException(status_code=404, detail="Check-in not found")

    return {
        "code": 0,
        "message": "success",
        "data": summary
    }


@router.get("/{checkin_id}/report", response_model=Dict[str, Any])
async def get_weekly_report(
    checkin_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    生成周报数据
    """
    service = CheckInService()
    report = service.generate_weekly_report(
        checkin_id=checkin_id,
        db=db
    )

    if not report:
        raise HTTPException(status_code=404, detail="Check-in not found")

    return {
        "code": 0,
        "message": "success",
        "data": report
    }


@router.get("/streak/{user_id}", response_model=Dict[str, Any])
async def get_progress_streak(
    user_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    计算用户连续打卡天数
    """
    service = CheckInService()
    streak = service.calculate_progress_streak(
        user_id=user_id,
        db=db
    )

    return {
        "code": 0,
        "message": "success",
        "data": {
            "user_id": user_id,
            "current_streak": streak
        }
    }


@router.get("/progress/{user_id}/overview", response_model=Dict[str, Any])
async def get_user_progress_overview(
    user_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取用户整体进度概览
    """
    service = CheckInService()
    overview = service.get_user_progress_overview(
        user_id=user_id,
        db=db
    )

    return {
        "code": 0,
        "message": "success",
        "data": overview
    }


@router.get("/{checkin_id}/recommendations", response_model=Dict[str, Any])
async def get_weekly_recommendations(
    checkin_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取AI周建议
    """
    ai_service = AIFeedbackService()
    recommendations = ai_service.generate_weekly_recommendations(
        checkin_id=checkin_id,
        db=db
    )

    return {
        "code": 0,
        "message": "success",
        "data": recommendations
    }


@router.get("/motivational/{user_id}", response_model=Dict[str, Any])
async def get_motivational_message(
    user_id: str,
    streak: int = Query(0, ge=0, description="连续打卡天数"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    生成鼓励信息
    """
    ai_service = AIFeedbackService()
    message = ai_service.generate_motivational_message(
        user_id=user_id,
        streak=streak,
        db=db
    )

    return {
        "code": 0,
        "message": "success",
        "data": {
            "user_id": user_id,
            "streak": streak,
            "motivational_message": message
        }
    }


@router.get("/risks/{user_id}", response_model=Dict[str, Any])
async def identify_risk_factors(
    user_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    识别风险因素
    """
    ai_service = AIFeedbackService()
    risks = ai_service.identify_risk_factors(
        user_id=user_id,
        db=db
    )

    return {
        "code": 0,
        "message": "success",
        "data": {
            "user_id": user_id,
            "risk_factors": risks
        }
    }
