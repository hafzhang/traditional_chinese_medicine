"""
Health Check Router
健康检查 API 路由
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Any

from api.database import get_db
from api.config import settings


router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    健康检查接口

    Args:
        db: 数据库会话

    Returns:
        系统健康状态
    """
    # 检查数据库连接
    db_status = "healthy"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "unhealthy"

    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "database": db_status,
        "services": {
            "api": "healthy",
            "database": db_status
        }
    }


@router.get("/ping")
async def ping() -> Dict[str, str]:
    """
    简单的 ping 接口，用于快速检查服务是否运行

    Returns:
        pong 响应
    """
    return {"ping": "pong"}
