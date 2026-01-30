"""
Database Models
数据库模型定义 - SQLite 兼容版本
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON, UniqueConstraint
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
    """食材库表 - Phase 1 更新版 + 营养增强版"""
    __tablename__ = "ingredients"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    aliases = Column(JSON)  # 别名列表，如 ["怀山药", "淮山"]
    category = Column(String(50))  # 类别：谷物、蔬菜、水果、肉类、药材、调味品、海鲜、坚果、菌藻、豆类

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

    # 营养数据 (每100g)
    calories = Column(Float, default=0)  # 热量 (kcal)
    protein = Column(Float, default=0)  # 蛋白质 (g)
    fat = Column(Float, default=0)  # 脂肪 (g)
    carbohydrates = Column(Float, default=0)  # 碳水化合物 (g)
    dietary_fiber = Column(Float, default=0)  # 膳食纤维 (g)

    # 维生素含量 (每100g)
    vitamin_a = Column(Float)  # 维生素A (μgRAE)
    vitamin_b1 = Column(Float)  # 维生素B1 (mg)
    vitamin_b2 = Column(Float)  # 维生素B2 (mg)
    vitamin_c = Column(Float)  # 维生素C (mg)
    vitamin_e = Column(Float)  # 维生素E (mg)

    # 矿物质含量 (每100g)
    calcium = Column(Float)  # 钙 (mg)
    iron = Column(Float)  # 铁 (mg)
    zinc = Column(Float)  # 锌 (mg)
    potassium = Column(Float)  # 钾 (mg)
    sodium = Column(Float)  # 钠 (mg)
    iodine = Column(Float)  # 碘 (μg)
    selenium = Column(Float)  # 硒 (μg)

    # 食用指导
    cooking_methods = Column(JSON)  # 食用方法列表，如 ["蒸", "煮", "炖"]
    daily_dosage = Column(String(50))  # 每日用量，如 "50-100g"
    best_time = Column(String(50))  # 最佳食用时间，如 "早晚餐"
    precautions = Column(Text)  # 注意事项

    # 增强搭配信息 (带原因说明)
    compatible_foods = Column(JSON)  # 宜配食材列表 [{"name": "莲子", "reason": "健脾益气", "benefit": "适合气血两虚"}]
    incompatible_foods = Column(JSON)  # 忌配食材列表 [{"name": "碱性食物", "reason": "破坏黏液蛋白", "effect": "降低营养价值"}]
    classic_combinations = Column(JSON)  # 经典搭配 [{"name": "山药+红枣", "benefit": "健脾益气", "target": "气血两虚"}]

    # 储存与安全
    storage_method = Column(String(50))  # 储存方法：常温、冷藏、冷冻
    storage_temperature = Column(String(30))  # 储存温度，如 "10-15℃"
    storage_humidity = Column(String(30))  # 储存湿度，如 "85-90%"
    shelf_life = Column(String(30))  # 保质期，如 "1-2个月"
    preservation_tips = Column(Text)  # 保鲜技巧

    # 食材安全
    pesticide_risk = Column(String(20))  # 农药残留风险：高、中、低
    heavy_metal_risk = Column(String(20))  # 重金属风险：高、中、低
    microbe_risk = Column(String(20))  # 微生物风险：高、中、低
    safety_precautions = Column(Text)  # 安全注意事项

    # 烹饪方法详情
    cooking_details = Column(JSON)  # 烹饪详情 [{"method": "煮", "time": "30分钟", "temperature": "100℃", "tips": "小火慢煮"}]

    # 季节推荐
    best_seasons = Column(JSON)  # 最佳季节，如 ["春", "秋", "冬"]
    seasonal_benefits = Column(JSON)  # 季节功效 [{"season": "夏", "benefit": "清热解暑"}]

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
    """食谱库表 - Phase 1 更新版 + 营养分析版 + Excel导入增强版"""
    __tablename__ = "recipes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False, index=True)
    type = Column(String(50))  # 类型：粥类、汤类、茶饮、菜肴、主食、甜品小吃
    difficulty = Column(String(20))  # 难度：简单、中等、困难 -> easy/medium/hard
    cook_time = Column(Integer)  # 烹饪时间（分钟）
    cooking_time = Column(Integer)  # 烹饪时间（分钟）- Excel导入字段（分钟）
    servings = Column(Integer)  # 份量

    # 描述字段
    description = Column(Text)  # 基本描述
    desc = Column(Text)  # 个人体验描述 - Excel导入字段
    tip = Column(Text)  # 烹饪贴士 - Excel导入字段

    # 体质关联（与现有系统对接）
    suitable_constitutions = Column(JSON)  # 适用体质，如 ["qi_deficiency"]
    avoid_constitutions = Column(JSON)  # 禁忌体质 - Excel导入字段
    symptoms = Column(JSON)  # 主治症状，如 ["食欲不振", "疲劳乏力"]
    suitable_seasons = Column(JSON)  # 适用季节，如 ["春", "秋", "冬"]

    # 功效和节气标签 - Excel导入字段
    efficacy_tags = Column(JSON)  # 功效标签，如 ["健脾", "养胃", "补气"]
    solar_terms = Column(JSON)  # 节气标签，如 ["立春", "雨水"]

    # 食材和步骤
    ingredients = Column(JSON)  # {main: [...], auxiliary: [...], seasoning: [...]}
    steps = Column(JSON)  # 制作步骤列表

    # 功效说明
    efficacy = Column(Text)  # 功效，如 "健脾养胃、补肺益气"
    health_benefits = Column(Text)  # 健康益处
    precautions = Column(Text)  # 注意事项

    # 营养分析 (每份)
    calories = Column(Integer, default=0)  # 热量 (kcal/份) - Excel导入要求Integer
    protein = Column(Float, default=0)  # 蛋白质 (g/份)
    fat = Column(Float, default=0)  # 脂肪 (g/份)
    carbohydrates = Column(Float, default=0)  # 碳水化合物 (g/份) -> 映射到carbs
    carbs = Column(Float, default=0)  # 碳水化合物 (g/份) - Excel导入字段
    dietary_fiber = Column(Float, default=0)  # 膳食纤维 (g/份)

    # 营养素含量详情
    nutrition_summary = Column(JSON)  # 营养摘要 {"calories": 150, "protein": 8, "fat": 1, "carbs": 25}
    key_nutrients = Column(JSON)  # 关键营养素 [{"name": "维生素A", "amount": 1200, "unit": "μgRAE"}]

    # 烹饪方法详情
    cooking_method = Column(String(30))  # 主要烹饪方法：煮、蒸、炒、炖、炸、烤
    cooking_temperature = Column(String(30))  # 烹饪温度，如 "100-150℃"
    nutrition_tips = Column(Text)  # 营养提示

    # 中医食疗信息
    tcm_efficacy = Column(Text)  # 中医功效
    tcm_target = Column(JSON)  # 中医适用人群 [{"constitution": "qi_deficiency", "symptoms": ["乏力", "气短"]}]
    contraindications = Column(JSON)  # 禁忌人群 [{"type": "实热证", "reason": "本品温补"}]

    # 标签
    tags = Column(JSON)  # 标签列表，如 ["健脾养胃", "补气", "安神"]
    meal_type = Column(String(20))  # 餐次类型：早餐、午餐、晚餐、加餐、夜宵

    # 展示
    image_url = Column(String(255))
    cover_image = Column(String(500))  # 封面图 - Excel导入字段
    source = Column(String(100))  # 来源，如 "《本草纲目》"

    # 统计
    view_count = Column(Integer, default=0)
    favorite_count = Column(Integer, default=0)
    rating = Column(Float, default=0)  # 评分
    review_count = Column(Integer, default=0)  # 评论数

    # 发布状态 - Excel导入字段
    is_published = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

    # Relationships (ingredient_relations added in US-002, step_relations pending US-003)
    ingredient_relations = relationship("RecipeIngredient", back_populates="recipe")
    # step_relations = relationship("RecipeStep", back_populates="recipe")


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
    pinyin = Column(String(100))  # 拼音
    aliases = Column(JSON, nullable=False, default=list)  # 别名数组，如 ["头冲", "颈冲"]
    meridian = Column(String(50))  # 所属经络，如 "足阳明胃经"
    five_element = Column(String(20))  # 经络五行，如 "金", "木", "水", "火", "土"

    # 位置
    body_part = Column(String(50))  # 部位，如 "下肢"
    location = Column(Text)  # 定位，如 "犊鼻下3寸，胫骨前缘外一横指"
    simple_location = Column(Text)  # 简易取穴，如 "膝盖骨外侧下方凹陷往下四横指"

    # 释义与功效
    explanation = Column(Text)  # 穴位释义
    functions = Column(Text)  # 穴位功能描述
    efficacy = Column(JSON, nullable=False, default=list)  # 主要功效列表，如 ["健脾和胃", "扶正培元", "调理气血"]
    indications = Column(JSON, nullable=False, default=list)  # 主治病症列表，如 ["胃痛", "消化不良", "失眠", "疲劳"]

    # 操作方法
    massage_method = Column(Text)  # 按摩手法
    moxibustion_method = Column(Text)  # 灸法
    massage_duration = Column(String(50))  # 按摩时间，如 "3-5分钟"
    massage_frequency = Column(String(50))  # 按摩频率，如 "每日1-2次"
    precautions = Column(Text)  # 注意事项

    # 解剖与配伍
    anatomical_structure = Column(Text)  # 解剖位置和结构
    combinations = Column(Text)  # 主要配伍

    # 体质关联（与现有系统对接）
    suitable_constitutions = Column(JSON, nullable=False, default=list)  # 适用体质，如 ["qi_deficiency", "yang_deficiency"]
    constitution_benefit = Column(Text)  # 体质调理说明，如 "健脾和胃，增强体质"

    # 展示
    image_url = Column(String(255))
    anatomical_image_url = Column(String(255)) # 解剖图
    model_3d_url = Column(String(255)) # 3D模型

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


class RecipeIngredient(Base):
    """菜谱-食材关联表 - Excel导入新增"""
    __tablename__ = "recipe_ingredients"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    recipe_id = Column(String(36), ForeignKey("recipes.id"), nullable=False)
    ingredient_id = Column(String(36), ForeignKey("ingredients.id"), nullable=False)
    amount = Column(String(50))  # 用量，如 "100g"
    is_main = Column(Boolean, default=False)  # 是否主料
    display_order = Column(Integer, default=0)  # 显示顺序

    created_at = Column(DateTime, server_default=func.now())

    # Unique constraint: each ingredient can only appear once per recipe
    __table_args__ = (
        UniqueConstraint('recipe_id', 'ingredient_id', name='uq_recipe_ingredient'),
    )

    # Relationships
    recipe = relationship("Recipe", back_populates="ingredient_relations")
    ingredient = relationship("Ingredient")
