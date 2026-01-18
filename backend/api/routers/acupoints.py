"""
Acupoints API Router
穴位 API 路由 - Phase 1
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from api.database import get_db_optional
from api.services.acupoint_service import get_acupoint_service
from pydantic import BaseModel


router = APIRouter(prefix="/acupoints", tags=["acupoints"])

acupoint_service = get_acupoint_service()


# Response Models
class AcupointListResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


class AcupointDetailResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


@router.get("", response_model=AcupointListResponse)
async def get_acupoints(
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(20, ge=1, le=100, description="限制数量"),
    body_part: Optional[str] = Query(None, description="部位筛选"),
    constitution: Optional[str] = Query(None, description="体质筛选"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db_optional)
) -> Dict[str, Any]:
    """
    获取穴位列表

    支持按部位、体质筛选和关键词搜索
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    acupoints, total = acupoint_service.get_acupoints_list(
        db=db,
        skip=skip,
        limit=limit,
        body_part=body_part,
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
                    "id": a.id,
                    "name": a.name,
                    "code": a.code,
                    "meridian": a.meridian,
                    "body_part": a.body_part,
                    "location": a.simple_location,
                    "efficacy": a.efficacy,
                    "image_url": a.image_url
                }
                for a in acupoints
            ]
        }
    }


@router.get("/{acupoint_id}", response_model=AcupointDetailResponse)
async def get_acupoint_detail(
    acupoint_id: str,
    db: Session = Depends(get_db_optional)
) -> Dict[str, Any]:
    """
    获取穴位详情
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    acupoint = acupoint_service.get_acupoint_by_id(acupoint_id, db)

    if not acupoint:
        raise HTTPException(status_code=404, detail="Acupoint not found")

    return {
        "code": 0,
        "message": "success",
        "data": {
            "id": acupoint.id,
            "name": acupoint.name,
            "code": acupoint.code,
            "meridian": acupoint.meridian,
            "body_part": acupoint.body_part,
            "location": acupoint.location,
            "simple_location": acupoint.simple_location,
            "efficacy": acupoint.efficacy,
            "indications": acupoint.indications,
            "massage_method": acupoint.massage_method,
            "massage_duration": acupoint.massage_duration,
            "massage_frequency": acupoint.massage_frequency,
            "precautions": acupoint.precautions,
            "suitable_constitutions": acupoint.suitable_constitutions,
            "constitution_benefit": acupoint.constitution_benefit,
            "image_url": acupoint.image_url
        }
    }


@router.get("/recommend/{constitution}", response_model=AcupointListResponse)
async def get_acupoint_recommendation(
    constitution: str,
    db: Session = Depends(get_db_optional)
) -> Dict[str, Any]:
    """
    根据体质获取推荐穴位

    返回适合该体质调理的穴位
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    if not acupoint_service.is_valid_constitution_code(constitution):
        raise HTTPException(status_code=400, detail=f"Invalid constitution code: {constitution}")

    acupoints = acupoint_service.get_acupoints_by_constitution(constitution, db)

    return {
        "code": 0,
        "message": "success",
        "data": {
            "constitution": constitution,
            "constitution_name": acupoint_service.get_constitution_name(constitution),
            "items": [
                {
                    "id": a.id,
                    "name": a.name,
                    "code": a.code,
                    "meridian": a.meridian,
                    "body_part": a.body_part,
                    "simple_location": a.simple_location,
                    "efficacy": a.efficacy,
                    "constitution_benefit": a.constitution_benefit,
                    "image_url": a.image_url
                }
                for a in acupoints
            ]
        }
    }


@router.get("/symptom/{symptom}", response_model=AcupointListResponse)
async def get_acupoints_by_symptom(
    symptom: str,
    db: Session = Depends(get_db_optional)
) -> Dict[str, Any]:
    """
    根据症状查找推荐穴位

    返回适合该症状调理的穴位（按优先级排序）
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    result = acupoint_service.get_acupoints_by_symptom(symptom, db)

    return {
        "code": 0,
        "message": "success",
        "data": {
            "symptom": symptom,
            "items": [
                {
                    "id": item["acupoint"].id,
                    "name": item["acupoint"].name,
                    "code": item["acupoint"].code,
                    "meridian": item["acupoint"].meridian,
                    "body_part": item["acupoint"].body_part,
                    "simple_location": item["acupoint"].simple_location,
                    "efficacy": item["acupoint"].efficacy,
                    "image_url": item["acupoint"].image_url,
                    "priority": item["priority"]
                }
                for item in result
            ]
        }
    }


@router.get("/meridian/{meridian}", response_model=AcupointListResponse)
async def get_acupoints_by_meridian(
    meridian: str,
    db: Session = Depends(get_db_optional)
) -> Dict[str, Any]:
    """
    根据经络获取穴位列表

    返回某条经络上的所有穴位
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    acupoints = acupoint_service.get_acupoints_by_meridian(meridian, db)

    return {
        "code": 0,
        "message": "success",
        "data": {
            "meridian": meridian,
            "items": [
                {
                    "id": a.id,
                    "name": a.name,
                    "code": a.code,
                    "location": a.simple_location,
                    "efficacy": a.efficacy
                }
                for a in acupoints
            ]
        }
    }


@router.get("/body-parts/list")
async def get_body_parts() -> Dict[str, Any]:
    """
    获取部位列表
    """
    body_parts = acupoint_service.get_body_parts()

    return {
        "code": 0,
        "message": "success",
        "data": body_parts
    }


@router.get("/meridians/list")
async def get_meridians(db: Session = Depends(get_db_optional)) -> Dict[str, Any]:
    """
    获取经络列表
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    meridians = acupoint_service.get_meridians(db)

    return {
        "code": 0,
        "message": "success",
        "data": [{"value": m, "label": m} for m in meridians]
    }
