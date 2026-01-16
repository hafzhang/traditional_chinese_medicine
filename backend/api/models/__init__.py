"""
Database Models
数据库模型定义 - SQLite 兼容版本
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from api.database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    douyin_openid = Column(String(128), unique=True, nullable=True, index=True)
    wechat_openid = Column(String(128), unique=True, nullable=True, index=True)
    anonymous_id = Column(String(128), unique=True, nullable=True, index=True)
    nickname = Column(String(100))
    avatar_url = Column(String(500))
    member_level = Column(String(20), default="free")  # free, silver, gold, diamond
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    constitution_results = relationship("ConstitutionResult", back_populates="user")


class Question(Base):
    """问卷题目表"""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    question_number = Column(Integer, nullable=False, unique=True)
    content = Column(Text, nullable=False)
    constitution_type = Column(String(50), nullable=False)  # 对应体质类型
    options = Column(JSON, nullable=True)  # 选项配置
    created_at = Column(DateTime, server_default=func.now())

    # Constitution types mapping
    # peace: 平和质 (4题)
    # qi_deficiency: 气虚质 (4题)
    # yang_deficiency: 阳虚质 (4题)
    # yin_deficiency: 阴虚质 (4题)
    # phlegm_damp: 痰湿质 (3题)
    # damp_heat: 湿热质 (3题)
    # blood_stasis: 血瘀质 (3题)
    # qi_depression: 气郁质 (3题)
    # special: 特禀质 (2题)


class ConstitutionResult(Base):
    """体质结果表"""
    __tablename__ = "constitution_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    primary_constitution = Column(String(50), nullable=False)
    secondary_constitutions = Column(JSON)  # 次要体质列表
    scores = Column(JSON, nullable=False)  # 九种体质分数
    answers = Column(JSON)  # 用户原始答案
    ip_address = Column(String(50))  # INET -> String
    user_agent = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="constitution_results")


class Food(Base):
    """食物库表"""
    __tablename__ = "foods"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    name_en = Column(String(100))
    nature = Column(String(20))  # 寒、凉、平、温、热
    flavor = Column(String(50))  # 酸、苦、甘、辛、咸、涩
    meridians = Column(JSON)  # ARRAY -> JSON 存储列表
    suitable_constitutions = Column(JSON)  # ARRAY -> JSON 存储列表
    avoid_constitutions = Column(JSON)  # ARRAY -> JSON 存储列表
    nutrition_info = Column(JSON)  # 营养信息
    effects = Column(JSON)  # ARRAY -> JSON 存储列表
    recipes = Column(JSON)  # ARRAY -> JSON 存储列表
    image_url = Column(String(500))
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


class Recipe(Base):
    """推荐菜谱表"""
    __tablename__ = "recipes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    name_en = Column(String(200))
    suitable_constitutions = Column(JSON, nullable=False)  # ARRAY -> JSON
    ingredients = Column(JSON, nullable=False)  # 食材列表
    steps = Column(JSON, nullable=False)  # 制作步骤
    images = Column(JSON)  # ARRAY -> JSON 存储列表
    description = Column(Text)
    tips = Column(Text)  # 制作贴士
    preparation_time = Column(Integer)  # 制作时间（分钟）
    servings = Column(Integer)  # 份数
    difficulty = Column(String(20))  # 简单、中等、困难
    created_at = Column(DateTime, server_default=func.now())


class ConstitutionInfo(Base):
    """体质信息表（静态数据）"""
    __tablename__ = "constitution_info"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    constitution_type = Column(String(50), unique=True, nullable=False)  # 英文标识
    constitution_name = Column(String(50), nullable=False)  # 中文名称
    description = Column(Text)  # 体质描述
    characteristics = Column(JSON)  # 典型表现
    regulation_principles = Column(JSON)  # 调理原则
    diet_principles = Column(JSON)  # 饮食原则
    exercise_recommendations = Column(JSON)  # 运动建议
    lifestyle_recommendations = Column(JSON)  # 作息建议
    emotion_recommendations = Column(JSON)  # 情志调节
    taboos = Column(JSON)  # 禁忌
    created_at = Column(DateTime, server_default=func.now())
