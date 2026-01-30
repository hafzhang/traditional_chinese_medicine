"""
Daily Routines API Router
起居作息 API 路由 - MVP
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from api.database import get_db
from api.services.daily_routine_service import DailyRoutineService
from pydantic import BaseModel


router = APIRouter(prefix="/routines", tags=["daily_routines"])


# Response Models
class RoutineListResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


class RoutineDetailResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


@router.get("", response_model=RoutineListResponse)
async def get_routines(
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(10, ge=1, le=50, description="限制数量"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取所有作息方案列表
    """
    service = DailyRoutineService()
    routines, total = service.get_all_routines(
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
                    "id": r.id,
                    "name": r.name,
                    "description": r.description,
                    "target_constitutions": r.target_constitutions,
                    "wake_time": r.wake_time,
                    "sleep_time": r.sleep_time
                }
                for r in routines
            ]
        }
    }


@router.get("/constitution/{constitution_code}", response_model=RoutineDetailResponse)
async def get_routine_by_constitution(
    constitution_code: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    根据体质获取作息方案
    """
    service = DailyRoutineService()
    routine = service.get_routine_by_constitution(
        constitution_code=constitution_code,
        db=db
    )

    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found for this constitution")

    return {
        "code": 0,
        "message": "success",
        "data": {
            "id": routine.id,
            "name": routine.name,
            "description": routine.description,
            "target_constitutions": routine.target_constitutions,
            "wake_time": routine.wake_time,
            "sleep_time": routine.sleep_time,
            "morning_routine": routine.morning_routine,
            "afternoon_routine": routine.afternoon_routine,
            "evening_routine": routine.evening_routine,
            "meal_timings": routine.meal_timings,
            "tips": routine.tips
        }
    }


@router.get("/constitution/{constitution_code}/summary", response_model=Dict[str, Any])
async def get_routine_summary(
    constitution_code: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取体质作息方案摘要
    """
    service = DailyRoutineService()
    summary = service.get_constitution_routine_summary(
        constitution_code=constitution_code,
        db=db
    )

    if not summary:
        raise HTTPException(status_code=404, detail="Routine not found for this constitution")

    return {
        "code": 0,
        "message": "success",
        "data": summary
    }


@router.get("/today/{user_id}/{constitution_code}", response_model=RoutineDetailResponse)
async def get_today_schedule(
    user_id: str,
    constitution_code: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    生成今日作息时间表
    """
    service = DailyRoutineService()
    schedule = service.generate_today_schedule(
        user_id=user_id,
        constitution_code=constitution_code,
        db=db
    )

    return {
        "code": 0,
        "message": "success",
        "data": schedule
    }


@router.get("/seasonal/{constitution_code}/{season}", response_model=Dict[str, Any])
async def get_seasonal_adjustment(
    constitution_code: str,
    season: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取季节性作息调整

    season: spring, summer, autumn, winter
    """
    service = DailyRoutineService()
    adjustment = service.get_seasonal_adjustment(
        constitution_code=constitution_code,
        season=season,
        db=db
    )

    return {
        "code": 0,
        "message": "success",
        "data": {
            "constitution": constitution_code,
            "season": season,
            "adjustment": adjustment
        }
    }


@router.get("/constitution/{constitution_code}/full", response_model=RoutineDetailResponse)
async def get_routine_with_seasonal_info(
    constitution_code: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取作息方案及当前季节信息
    """
    service = DailyRoutineService()
    result = service.get_routine_with_seasonal_info(
        constitution_code=constitution_code,
        db=db
    )

    if not result:
        raise HTTPException(status_code=404, detail="Routine not found for this constitution")

    return {
        "code": 0,
        "message": "success",
        "data": result
    }


@router.get("/{routine_id}", response_model=RoutineDetailResponse)
async def get_routine_detail(
    routine_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取作息方案详情
    """
    service = DailyRoutineService()
    routine = service.get_routine_by_id(
        routine_id=routine_id,
        db=db
    )

    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")

    return {
        "code": 0,
        "message": "success",
        "data": {
            "id": routine.id,
            "name": routine.name,
            "description": routine.description,
            "target_constitutions": routine.target_constitutions,
            "wake_time": routine.wake_time,
            "sleep_time": routine.sleep_time,
            "morning_routine": routine.morning_routine,
            "afternoon_routine": routine.afternoon_routine,
            "evening_routine": routine.evening_routine,
            "seasonal_adjustments": routine.seasonal_adjustments,
            "meal_timings": routine.meal_timings,
            "tips": routine.tips
        }
    }
