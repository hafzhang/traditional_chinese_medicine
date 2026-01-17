"""
用户管理 API 路由
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/profile")
async def get_user_profile():
    """获取用户信息"""
    return {
        "code": 0,
        "message": "success",
        "data": {
            "id": "user_001",
            "nickname": "测试用户",
            "constitution": "qi_deficiency"
        }
    }


@router.post("/login")
async def login():
    """用户登录"""
    return {
        "code": 0,
        "message": "success",
        "data": {
            "token": "test_token",
            "user_id": "user_001"
        }
    }
