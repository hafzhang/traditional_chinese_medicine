"""
Courses API Router
养生课程 API 路由 - Phase 1
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from api.database import get_db_optional
from api.services.course_service import get_course_service
from pydantic import BaseModel


router = APIRouter(prefix="/courses", tags=["courses"])

course_service = get_course_service()


# Response Models
class CourseListResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


class CourseDetailResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


@router.get("", response_model=CourseListResponse)
async def get_courses(
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(20, ge=1, le=100, description="限制数量"),
    category: Optional[str] = Query(None, description="分类筛选"),
    content_type: Optional[str] = Query(None, description="内容类型筛选"),
    constitution: Optional[str] = Query(None, description="体质筛选"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db_optional)
) -> Dict[str, Any]:
    """
    获取课程列表

    支持按分类、内容类型、体质筛选和关键词搜索
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    courses, total = course_service.get_courses_list(
        db=db,
        skip=skip,
        limit=limit,
        category=category,
        content_type=content_type,
        constitution=constitution,
        search=search
    )

    return {
        "code": 0,
        "message": "success",
        "data": {
            "total": total,
            "items": [
                {
                    "id": c.id,
                    "title": c.title,
                    "description": c.description,
                    "category": c.category,
                    "subcategory": c.subcategory,
                    "content_type": c.content_type,
                    "duration": c.duration,
                    "cover_image": c.cover_image,
                    "author": c.author,
                    "author_title": c.author_title,
                    "view_count": c.view_count
                }
                for c in courses
            ]
        }
    }


@router.get("/{course_id}", response_model=CourseDetailResponse)
async def get_course_detail(
    course_id: str,
    db: Session = Depends(get_db_optional)
) -> Dict[str, Any]:
    """
    获取课程详情
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    course = course_service.get_course_by_id(course_id, db)

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # 增加浏览次数
    course_service.increment_view_count(course_id, db)

    return {
        "code": 0,
        "message": "success",
        "data": {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "category": course.category,
            "subcategory": course.subcategory,
            "content_type": course.content_type,
            "content_url": course.content_url,
            "suitable_constitutions": course.suitable_constitutions,
            "tags": course.tags,
            "duration": course.duration,
            "cover_image": course.cover_image,
            "author": course.author,
            "author_title": course.author_title,
            "view_count": course.view_count
        }
    }


@router.get("/recommend/{constitution}", response_model=CourseListResponse)
async def get_course_recommendation(
    constitution: str,
    db: Session = Depends(get_db_optional)
) -> Dict[str, Any]:
    """
    根据体质获取推荐课程

    返回适合该体质调理的课程
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    if not course_service.is_valid_constitution_code(constitution):
        raise HTTPException(status_code=400, detail=f"Invalid constitution code: {constitution}")

    courses = course_service.get_courses_by_constitution(constitution, db)

    return {
        "code": 0,
        "message": "success",
        "data": {
            "constitution": constitution,
            "constitution_name": course_service.get_constitution_name(constitution),
            "items": [
                {
                    "id": c.id,
                    "title": c.title,
                    "description": c.description,
                    "content_type": c.content_type,
                    "duration": c.duration,
                    "cover_image": c.cover_image,
                    "author": c.author,
                    "author_title": c.author_title,
                    "view_count": c.view_count
                }
                for c in courses
            ]
        }
    }


@router.get("/season/{season}")
async def get_season_courses(
    season: str,
    db: Session = Depends(get_db_optional)
) -> Dict[str, Any]:
    """
    根据季节获取养生课程

    返回适合当季的养生课程
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    courses = course_service.get_courses_by_season(season, db)

    season_names = {
        "spring": "春季",
        "summer": "夏季",
        "autumn": "秋季",
        "winter": "冬季"
    }

    return {
        "code": 0,
        "message": "success",
        "data": {
            "season": season,
            "season_name": season_names.get(season, season),
            "items": [
                {
                    "id": c.id,
                    "title": c.title,
                    "description": c.description,
                    "content_type": c.content_type,
                    "duration": c.duration,
                    "cover_image": c.cover_image,
                    "author": c.author
                }
                for c in courses
            ]
        }
    }


@router.get("/categories/list")
async def get_categories() -> Dict[str, Any]:
    """
    获取课程分类列表
    """
    categories = course_service.get_categories()

    return {
        "code": 0,
        "message": "success",
        "data": categories
    }


@router.get("/seasons/list")
async def get_seasons() -> Dict[str, Any]:
    """
    获取季节列表
    """
    seasons = course_service.get_seasons()

    return {
        "code": 0,
        "message": "success",
        "data": seasons
    }
