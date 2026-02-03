"""
Database Configuration and Session Management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from api.config import settings


# Create database engine (SQLite doesn't support connection pooling)
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        echo=settings.DEBUG
    )

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency

    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_optional() -> Generator[Session | None, None, None]:
    """
    Optional database session dependency - returns None if DB unavailable

    Yields:
        Session | None: Database session or None
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    # Import all models so they're registered with Base.metadata
    from api.models import (
        User, ConstitutionResult, Question, Food, Recipe,
        Ingredient, Acupoint, SymptomAcupoint, TongueDiagnosisRecord, Course,
        RecipeIngredient, RecipeStep, ConstitutionInfo
    )
    Base.metadata.create_all(bind=engine)
    print("[OK] Database tables initialized")
