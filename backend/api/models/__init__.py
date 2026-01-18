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


class Ingredient(Base):
    """食材库表 - Phase 1 更新版"""
    __tablename__ = "ingredients"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    aliases = Column(JSON)  # 别名列表，如 ["怀山药", "淮山"]
    category = Column(String(50))  # 类别：谷物、蔬菜、水果、肉类、药材

    # 性味归经
    nature = Column(String(20))  # 寒、凉、平、温、热
    flavor = Column(String(50))  # 甘、酸、苦、辛、咸
    meridians = Column(JSON)  # 归经列表，如 ["脾", "肺", "肾"]

    # 体质关联（与现有系统对接）
    suitable_constitutions = Column(JSON)  # 适用体质，如 ["qi_deficiency", "yin_deficiency"]
    avoid_constitutions = Column(JSON)  # 禁忌体质，如 ["phlegm_damp"]

    # 功效
    efficacy = Column(Text)  # 功效描述，如 "健脾养胃、补肺益肾"
    nutrition = Column(Text)  # 营养成分说明

    # 食用指导
    cooking_methods = Column(JSON)  # 食用方法列表，如 ["蒸", "煮", "炖"]
    daily_dosage = Column(String(50))  # 每日用量，如 "50-100g"
    best_time = Column(String(50))  # 最佳食用时间，如 "早晚餐"
    precautions = Column(Text)  # 注意事项

    # 搭配
    compatible_with = Column(JSON)  # 宜配食材，如 ["莲子", "枸杞"]
    incompatible_with = Column(JSON)  # 忌配食材，如 ["碱性食物"]

    # 展示
    image_url = Column(String(255))
    description = Column(Text)

    # 统计
    view_count = Column(Integer, default=0)
    favorite_count = Column(Integer, default=0)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    is_deleted = Column(Boolean, default=False)


class Food(Base):
    """食物库表（旧版，保持兼容）"""
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
    """食谱库表 - Phase 1 更新版"""
    __tablename__ = "recipes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    type = Column(String(50))  # 类型：粥类、汤类、茶饮、菜肴
    difficulty = Column(String(20))  # 难度：简单、中等、困难
    cook_time = Column(Integer)  # 烹饪时间（分钟）
    servings = Column(Integer)  # 份量

    # 体质关联（与现有系统对接）
    suitable_constitutions = Column(JSON)  # 适用体质，如 ["qi_deficiency"]
    symptoms = Column(JSON)  # 主治症状，如 ["食欲不振", "疲劳乏力"]
    suitable_seasons = Column(JSON)  # 适用季节，如 ["春", "秋", "冬"]

    # 食材和步骤
    ingredients = Column(JSON)  # {main: [...], auxiliary: [...], seasoning: [...]}
    steps = Column(JSON)  # 制作步骤列表

    # 功效说明
    efficacy = Column(Text)  # 功效，如 "健脾养胃、补肺益气"
    health_benefits = Column(Text)  # 健康益处
    precautions = Column(Text)  # 注意事项

    # 标签
    tags = Column(JSON)  # 标签列表，如 ["健脾养胃", "补气"]

    # 展示
    image_url = Column(String(255))
    description = Column(Text)

    # 统计
    view_count = Column(Integer, default=0)
    favorite_count = Column(Integer, default=0)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    is_deleted = Column(Boolean, default=False)


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


class Acupoint(Base):
    """穴位表 - Phase 1 新增"""
    __tablename__ = "acupoints"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    code = Column(String(20))  # 穴位代号，如 ST36
    meridian = Column(String(50))  # 所属经络，如 "足阳明胃经"

    # 位置
    body_part = Column(String(50))  # 部位，如 "下肢"
    location = Column(Text)  # 定位，如 "犊鼻下3寸，胫骨前缘外一横指"
    simple_location = Column(Text)  # 简易取穴，如 "膝盖骨外侧下方凹陷往下四横指"

    # 功效
    efficacy = Column(JSON)  # 主要功效列表，如 ["健脾和胃", "扶正培元", "调理气血"]
    indications = Column(JSON)  # 主治病症列表，如 ["胃痛", "消化不良", "失眠", "疲劳"]

    # 按摩
    massage_method = Column(Text)  # 按摩手法
    massage_duration = Column(String(50))  # 按摩时间，如 "3-5分钟"
    massage_frequency = Column(String(50))  # 按摩频率，如 "每日1-2次"
    precautions = Column(Text)  # 注意事项

    # 体质关联（与现有系统对接）
    suitable_constitutions = Column(JSON)  # 适用体质，如 ["qi_deficiency", "yang_deficiency"]
    constitution_benefit = Column(Text)  # 体质调理说明，如 "健脾和胃，增强体质"

    # 展示
    image_url = Column(String(255))

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class SymptomAcupoint(Base):
    """症状-穴位关联表 - Phase 1 新增"""
    __tablename__ = "symptom_acupoints"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    symptom_name = Column(String(100), nullable=False)  # 症状名称
    acupoint_id = Column(String(36), nullable=False)  # 穴位ID
    priority = Column(Integer, default=0)  # 优先级

    created_at = Column(DateTime, server_default=func.now())


class TongueDiagnosisRecord(Base):
    """舌诊记录表 - Phase 1 新增"""
    __tablename__ = "tongue_diagnosis_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    result_id = Column(String(36), ForeignKey("constitution_results.id"), nullable=True)  # 关联30题测试结果

    # 图片
    image_url = Column(String(255))

    # 分析结果
    tongue_color = Column(String(50))  # 舌质颜色：淡白/淡红/红/绛/紫
    tongue_shape = Column(String(50))  # 舌质形态：胖大/瘦薄/齿痕/裂纹
    coating_color = Column(String(50))  # 苔色：白苔/黄苔/灰黑苔
    coating_thickness = Column(String(50))  # 苔质：厚苔/薄苔/腻苔

    # 判断结果
    constitution_tendency = Column(String(50))  # 体质倾向，对应9种体质代码
    confidence = Column(Float)  # 置信度

    # 与30题测试对比
    is_consistent_with_test = Column(Boolean)  # 是否与测试结果一致
    test_constitution = Column(String(50))  # 测试结果体质

    # 调理建议
    advice = Column(JSON)  # {diet: "...", lifestyle: "..."}

    created_at = Column(DateTime, server_default=func.now())


class Course(Base):
    """养生课程表 - Phase 1 新增"""
    __tablename__ = "courses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    description = Column(Text)

    # 分类
    category = Column(String(50))  # constitution, season, diet, meridian
    subcategory = Column(String(50))  # 子分类，如 qi_deficiency, yin_deficiency

    # 内容类型
    content_type = Column(String(20))  # video, article
    content_url = Column(String(255))  # 视频/文章URL

    # 体质关联（与现有系统对接）
    suitable_constitutions = Column(JSON)  # 适用体质，如 ["qi_deficiency"]

    # 标签
    tags = Column(JSON)

    # 时长
    duration = Column(Integer)  # 时长（秒）

    # 封面和作者
    cover_image = Column(String(255))
    author = Column(String(100))
    author_title = Column(String(100))

    # 统计
    view_count = Column(Integer, default=0)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
