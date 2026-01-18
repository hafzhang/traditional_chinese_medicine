#!/usr/bin/env python3
"""
FastAPI Application Entry Point
中医体质识别 MVP 后端服务
"""

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.config import settings
from api.database import engine, Base
from api.routers import constitution, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("[INFO] Starting Constitution Recognition API...")
    print(f"   Environment: {settings.ENVIRONMENT}")
    print(f"   Database: {settings.DATABASE_URL[:20]}...")
    print(f"   Redis: {settings.REDIS_URL[:20]}...")

    yield

    # Shutdown
    print("[INFO] Shutting down Constitution Recognition API...")
    await engine.dispose()


# Create FastAPI application
app = FastAPI(
    title="Constitution Recognition API",
    description="中医体质识别 MVP 服务 - 基于王琦院士CCMQ标准量表",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    lifespan=lifespan
)

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
