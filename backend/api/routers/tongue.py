"""
Tongue Diagnosis API Router
舌诊 API 路由 - Phase 1
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import uuid

from api.database import get_db_optional
from api.services.tongue_service import get_tongue_service
from pydantic import BaseModel


router = APIRouter(prefix="/tongue", tags=["tongue"])

tongue_service = get_tongue_service()


# Request/Response Models
class TongueAnalysisRequest(BaseModel):
    tongue_color: str
    tongue_shape: str
    coating_color: str
    coating_thickness: str
    result_id: Optional[str] = None


class TongueAnalysisResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


@router.post("/analyze", response_model=TongueAnalysisResponse)
async def analyze_tongue(
    tongue_color: str = Form(...),
    tongue_shape: str = Form(...),
    coating_color: str = Form(...),
    coating_thickness: str = Form(...),
    image: Optional[UploadFile] = None,
    result_id: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None),
    db: Session = Depends(get_db_optional)
) -> Dict[str, Any]:
    """
    分析舌象

    上传舌象图片并选择舌象特征，AI分析体质倾向

    **注意**：当前为简化版本，基于规则匹配。
    完整版需要集成AI图像识别服务。
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    # 参数验证
    if tongue_color not in tongue_service.TONGUE_COLORS:
        raise HTTPException(status_code=400, detail=f"Invalid tongue_color. Must be one of: {tongue_service.TONGUE_COLORS}")
    if tongue_shape not in tongue_service.TONGUE_SHAPES:
        raise HTTPException(status_code=400, detail=f"Invalid tongue_shape. Must be one of: {tongue_service.TONGUE_SHAPES}")
    if coating_color not in tongue_service.COATING_COLORS:
        raise HTTPException(status_code=400, detail=f"Invalid coating_color. Must be one of: {tongue_service.COATING_COLORS}")
    if coating_thickness not in tongue_service.COATING_THICKNESS:
        raise HTTPException(status_code=400, detail=f"Invalid coating_thickness. Must be one of: {tongue_service.COATING_THICKNESS}")

    # 分析舌象
    analysis_result = tongue_service.analyze_tongue(
        tongue_color=tongue_color,
        tongue_shape=tongue_shape,
        coating_color=coating_color,
        coating_thickness=coating_thickness,
        db=db
    )

    # 保存图片（如果上传）
    image_url = None
    if image:
        # TODO: 实现图片上传到云存储
        # 这里简化处理，实际应该上传到OSS或S3
        image_url = f"/uploads/tongue/{uuid.uuid4()}.jpg"

    # 保存诊断记录
    record = tongue_service.save_diagnosis_record(
        user_id=user_id,
        result_id=result_id,
        image_url=image_url or "",
        analysis_result=analysis_result,
        db=db
    )

    # 如果提供了测试结果ID，进行对比
    comparison = None
    if result_id:
        from api.models import ConstitutionResult
        test_result = db.query(ConstitutionResult).filter(
            ConstitutionResult.id == result_id
        ).first()
        if test_result:
            comparison = tongue_service.compare_with_test(
                tongue_constitution=analysis_result["constitution_tendency"],
                test_constitution=test_result.primary_constitution
            )

            # 更新记录
            record.is_consistent_with_test = comparison["is_consistent"]
            record.test_constitution = test_result.primary_constitution
            db.commit()

    response_data = {
        "record_id": str(record.id),
        "analysis": analysis_result,
        "comparison": comparison
    }

    return TongueAnalysisResponse(
        code=0,
        message="success",
        data=response_data
    )


@router.get("/records/{user_id}")
async def get_user_records(
    user_id: str,
    limit: int = 10,
    db: Session = Depends(get_db_optional)
) -> Dict[str, Any]:
    """
    获取用户的舌诊记录
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    records = tongue_service.get_user_records(user_id, db, limit)

    return {
        "code": 0,
        "message": "success",
        "data": {
            "total": len(records),
            "items": [
                {
                    "id": str(r.id),
                    "image_url": r.image_url,
                    "tongue_color": r.tongue_color,
                    "tongue_shape": r.tongue_shape,
                    "coating_color": r.coating_color,
                    "coating_thickness": r.coating_thickness,
                    "constitution_tendency": r.constitution_tendency,
                    "confidence": r.confidence,
                    "created_at": r.created_at.isoformat() if r.created_at else None
                }
                for r in records
            ]
        }
    }


@router.get("/options")
async def get_tongue_options() -> Dict[str, Any]:
    """
    获取舌诊选项列表
    """
    return {
        "code": 0,
        "message": "success",
        "data": {
            "tongue_colors": [{"value": v, "label": v} for v in tongue_service.TONGUE_COLORS],
            "tongue_shapes": [{"value": v, "label": v} for v in tongue_service.TONGUE_SHAPES],
            "coating_colors": [{"value": v, "label": v} for v in tongue_service.COATING_COLORS],
            "coating_thickness": [{"value": v, "label": v} for v in tongue_service.COATING_THICKNESS]
        }
    }
