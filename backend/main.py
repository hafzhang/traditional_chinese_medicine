#!/usr/bin/env python3
"""
FastAPI Application Entry Point
中医体质识别 MVP 后端服务
"""

import uvicorn
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from api.config import settings
from api.database import engine, Base
from api.routers import constitution, health, ingredients, recipes, acupoints, tongue, courses, wellness


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("[INFO] Starting Constitution Recognition API...")
    print(f"   Environment: {settings.ENVIRONMENT}")
    print(f"   Database: {settings.DATABASE_URL[:20] if settings.DATABASE_URL else 'N/A'}...")
    print(f"   Redis: {settings.REDIS_URL[:20] if settings.REDIS_URL else 'N/A'}...")

    yield

    # Shutdown
    print("[INFO] Shutting down Constitution Recognition API...")
    try:
        if engine is not None:
            await engine.dispose()
    except Exception as e:
        print(f"[WARNING] Error during engine disposal: {e}")


# Create FastAPI application
app = FastAPI(
    title="Constitution Recognition API",
    description="中医体质识别 MVP 服务 - 基于王琦院士CCMQ标准量表",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    lifespan=lifespan
)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(constitution.router, prefix="/api/v1", tags=["Constitution"])
app.include_router(ingredients.router, prefix="/api/v1", tags=["Ingredients"])
app.include_router(recipes.router, prefix="/api/v1", tags=["Recipes"])
app.include_router(acupoints.router, prefix="/api/v1", tags=["Acupoints"])
app.include_router(tongue.router, prefix="/api/v1", tags=["Tongue"])
app.include_router(courses.router, prefix="/api/v1", tags=["Courses"])
app.include_router(wellness.router, prefix="/api/v1", tags=["Wellness"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Constitution Recognition API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    import logging
    logging.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "code": -1,
            "message": "Internal server error",
            "detail": str(exc) if settings.ENVIRONMENT != "production" else "An error occurred"
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level="info"
    )
