"""
API Routers Package
"""

from api.routers.constitution import router as constitution_router
from api.routers.health import router as health_router


__all__ = ["constitution_router", "health_router"]

