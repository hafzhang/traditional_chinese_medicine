"""
Exercises API Router
运动/功法 API 路由 - MVP
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List

from api.database import get_db
from api.services.exercise_service import ExerciseService
from pydantic import BaseModel


router = APIRouter(prefix="/exercises", tags=["exercises"])


# Response Models
class ExerciseListResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


class ExerciseDetailResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


@router.get("", response_model=ExerciseListResponse)
async def get_exercises(
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(20, ge=1, le=100, description="限制数量"),
    exercise_type: Optional[str] = Query(None, description="运动类型筛选"),
    difficulty_level: Optional[str] = Query(None, description="难度级别筛选"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取运动列表

    支持按运动类型、难度级别筛选和关键词搜索
    """
    service = ExerciseService()
    exercises, total = service.get_exercises_list(
        db=db,
        skip=skip,
        limit=limit,
        exercise_type=exercise_type,
        difficulty_level=difficulty_level,
        search=search
    )

    return {
        "code": 0,
        "message": "success",
        "data": {
            "total": total,
            "items": [
                {
                    "id": ex.id,
                    "name": ex.name,
                    "name_en": ex.name_en,
                    "description": ex.description,
                    "exercise_type": ex.exercise_type,
                    "difficulty_level": ex.difficulty_level,
                    "duration_seconds": ex.duration_seconds,
                    "video_url": ex.video_url,
                    "image_url": ex.image_url,
                    "target_constitutions": ex.target_constitutions,
                    "view_count": ex.view_count
                }
                for ex in exercises
            ]
        }
    }


@router.get("/types", response_model=Dict[str, Any])
async def get_exercise_types() -> Dict[str, Any]:
    """
    获取运动类型列表
    """
    service = ExerciseService()
    types = service.get_exercise_types(None)

    return {
        "code": 0,
        "message": "success",
        "data": {
            "types": types
        }
    }


@router.get("/constitution/{constitution_code}", response_model=ExerciseListResponse)
async def get_exercises_by_constitution(
    constitution_code: str,
    limit: int = Query(20, ge=1, le=100, description="限制数量"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    根据体质获取推荐运动
    """
    service = ExerciseService()
    exercises = service.get_exercises_by_constitution(
        constitution_code=constitution_code,
        db=db,
        limit=limit
    )

    return {
        "code": 0,
        "message": "success",
        "data": {
            "constitution": constitution_code,
            "total": len(exercises),
            "items": [
                {
                    "id": ex.id,
                    "name": ex.name,
                    "name_en": ex.name_en,
                    "description": ex.description,
                    "exercise_type": ex.exercise_type,
                    "difficulty_level": ex.difficulty_level,
                    "duration_seconds": ex.duration_seconds,
                    "video_url": ex.video_url,
                    "image_url": ex.image_url,
                    "target_constitutions": ex.target_constitutions,
                    "view_count": ex.view_count
                }
                for ex in exercises
            ]
        }
    }


@router.get("/routine/{constitution_code}", response_model=Dict[str, Any])
async def get_personalized_routine(
    constitution_code: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取个性化运动方案（早中晚）
    """
    service = ExerciseService()
    routine = service.get_personalized_routine(
        constitution_code=constitution_code,
        db=db
    )

    return {
        "code": 0,
        "message": "success",
        "data": {
            "constitution": constitution_code,
            "routine": {
                "morning": [
                    {
                        "id": ex.id,
                        "name": ex.name,
                        "exercise_type": ex.exercise_type,
                        "difficulty_level": ex.difficulty_level,
                        "duration_seconds": ex.duration_seconds,
                        "video_url": ex.video_url,
                        "image_url": ex.image_url
                    }
                    for ex in routine.get("morning", [])
                ],
                "afternoon": [
                    {
                        "id": ex.id,
                        "name": ex.name,
                        "exercise_type": ex.exercise_type,
                        "difficulty_level": ex.difficulty_level,
                        "duration_seconds": ex.duration_seconds,
                        "video_url": ex.video_url,
                        "image_url": ex.image_url
                    }
                    for ex in routine.get("afternoon", [])
                ],
                "evening": [
                    {
                        "id": ex.id,
                        "name": ex.name,
                        "exercise_type": ex.exercise_type,
                        "difficulty_level": ex.difficulty_level,
                        "duration_seconds": ex.duration_seconds,
                        "video_url": ex.video_url,
                        "image_url": ex.image_url
                    }
                    for ex in routine.get("evening", [])
                ]
            }
        }
    }


@router.get("/plan/{constitution_code}/{week}", response_model=Dict[str, Any])
async def get_exercise_plan_week(
    constitution_code: str,
    week: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取周运动计划
    """
    service = ExerciseService()
    plan = service.get_exercise_plan_week(
        constitution_code=constitution_code,
        week=week,
        db=db
    )

    return {
        "code": 0,
        "message": "success",
        "data": plan
    }


@router.get("/{exercise_id}", response_model=ExerciseDetailResponse)
async def get_exercise_detail(
    exercise_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取运动详情
    """
    service = ExerciseService()
    exercise = service.get_exercise_by_id(exercise_id, db)

    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    # 增加浏览次数
    service.increment_view_count(exercise_id, db)

    return {
        "code": 0,
        "message": "success",
        "data": {
            "id": exercise.id,
            "name": exercise.name,
            "name_en": exercise.name_en,
            "description": exercise.description,
            "exercise_type": exercise.exercise_type,
            "difficulty_level": exercise.difficulty_level,
            "target_constitutions": exercise.target_constitutions,
            "video_url": exercise.video_url,
            "image_url": exercise.image_url,
            "step_images": exercise.step_images,
            "instructions": exercise.instructions,
            "duration_seconds": exercise.duration_seconds,
            "repetitions": exercise.repetitions,
            "target_body_areas": exercise.target_body_areas,
            "contraindications": exercise.contraindications,
            "caution_notes": exercise.caution_notes,
            "benefits": exercise.benefits,
            "tags": exercise.tags,
            "view_count": exercise.view_count
        }
    }


@router.post("/{exercise_id}/view", response_model=Dict[str, Any])
async def increment_exercise_view(
    exercise_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    增加运动浏览次数
    """
    service = ExerciseService()
    success = service.increment_view_count(exercise_id, db)

    if not success:
        raise HTTPException(status_code=404, detail="Exercise not found")

    return {
        "code": 0,
        "message": "View count incremented",
        "data": {"exercise_id": exercise_id}
    }
