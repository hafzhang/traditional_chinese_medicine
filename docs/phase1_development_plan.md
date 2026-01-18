# 第一期开发计划文档

> **项目名称：** 中医养生平台（第一期）
> **版本：** v1.0
> **更新时间：** 2026-01-18

---

## 一、第一期产品范围

### 1.1 产品清单

| 序号 | 产品名称 | 产品类型 | 优先级 | 状态 |
|-----|---------|---------|-------|------|
| 1 | 食材库 + 食谱库 | 工具类 | P0 | 待开发 |
| 2 | 穴位查找 | 工具类 | P0 | 待开发 |
| 3 | AI舌诊 | AI工具 | P0 | 待开发 |
| 4 | 免费养生课程 | 内容类 | P1 | 待开发 |

### 1.2 不包含内容

- ❌ 支付系统
- ❌ 电商购物车
- ❌ 会员订阅
- ❌ 实体商品

---

## 二、食材库 + 食谱库

### 2.1 功能概述

为用户提供基于中医体质和症状的食疗方案，包括食材查询、食谱推荐、搭配禁忌等功能。

### 2.2 核心功能

#### 2.2.1 食材库

**功能列表：**
- 食材列表展示（分类浏览）
- 食材详情页
- 按体质筛选食材
- 按功效筛选食材
- 食材搜索
- 食材收藏

**食材详情包含：**
```yaml
食材基本信息:
  - 名称: 如"山药"
  - 别名: 如"怀山药、淮山"
  - 性味: "甘、平"
  - 归经: "脾、肺、肾经"
  - 功效: "健脾养胃、补肺益肾"
  - 适用体质: ["气虚质", "阴虚质"]
  - 禁忌体质: ["痰湿质"]
  - 营养成分: "蛋白质、维生素、黏液质等"
  - 适宜人群: "脾胃虚弱者"
  - 不宜人群: "便秘者"
  - 食用方法: "蒸、煮、炖"
  - 搭配宜忌:
      宜配: ["莲子", "枸杞"]
      忌配: ["碱性食物"]

食用建议:
  - 每日用量: "50-100g"
  - 最佳食用时间: "早晚餐"
  - 注意事项: "生用健脾，炒用止泻"
```

#### 2.2.2 食谱库

**功能列表：**
- 食谱列表展示
- 食谱详情页
- 按体质推荐食谱
- 按症状推荐食谱
- 按季节推荐食谱
- 食谱搜索
- 食谱收藏

**食谱详情包含：**
```yaml
食谱基本信息:
  - 名称: "山药莲子粥"
  - 类型: "粥类"
  - 难度: "简单"
  - 用时: "30分钟"
  - 份量: "2人份"

适用信息:
  - 适用体质: ["气虚质", "阴虚质"]
  - 主治症状: ["食欲不振", "疲劳乏力"]
  - 适宜季节: ["春", "秋", "冬"]

食材清单:
  - 主料:
      - 山药: 100g
      - 糯米: 50g
  - 辅料:
      - 莲子: 20g
      - 枸杞: 10g
  - 调料:
      - 冰糖: 适量

制作步骤:
  - 步骤1: "山药去皮切小块，糯米提前浸泡2小时"
  - 步骤2: "锅中加水，放入糯米大火煮开"
  - 步骤3: "加入山药、莲子转小火煮30分钟"
  - 步骤4: "最后加入枸杞、冰糖煮5分钟即可"

功效说明:
  - 健脾养胃
  - 补肺益气
  - 适合脾胃虚弱、食欲不振者

注意事项:
  - 糖尿病患者慎用或少放冰糖
  - 孕妇不宜过量食用
```

### 2.3 数据库设计

#### 2.3.1 食材表 (ingredients)

```sql
CREATE TABLE ingredients (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) NOT NULL COMMENT '食材名称',
    aliases TEXT COMMENT '别名，JSON数组',
    nature VARCHAR(20) COMMENT '性：寒、凉、平、温、热',
    flavor VARCHAR(50) COMMENT '味：甘、酸、苦、辛、咸',
    meridians TEXT COMMENT '归经，JSON数组',
    efficacy TEXT COMMENT '功效描述',
    nutrition TEXT COMMENT '营养成分',

    -- 体质相关
    suitable_constitutions JSON COMMENT '适用体质，JSON数组',
    avoid_constitutions JSON COMMENT '禁忌体质，JSON数组',

    -- 人群相关
    suitable_people TEXT COMMENT '适宜人群',
    avoid_people TEXT COMMENT '不宜人群',

    -- 食用指导
    cooking_methods JSON COMMENT '食用方法，JSON数组',
    daily_dosage VARCHAR(50) COMMENT '每日用量',
    best_time VARCHAR(50) COMMENT '最佳食用时间',
    precautions TEXT COMMENT '注意事项',

    -- 搭配宜忌
    compatible_with JSON COMMENT '宜配食材，JSON数组',
    incompatible_with JSON COMMENT '忌配食材，JSON数组',

    -- 分类
    category VARCHAR(50) COMMENT '分类：谷物、蔬菜、水果、肉类、药材等',
    subcategory VARCHAR(50) COMMENT '子分类',

    -- 展示
    image_url VARCHAR(255) COMMENT '图片URL',
    description TEXT COMMENT '详细描述',

    -- 元数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_ingredients_name ON ingredients(name);
CREATE INDEX idx_ingredients_category ON ingredients(category);
CREATE INDEX idx_ingredients_constitution ON ingredients((CAST(suitable_constitutions AS CHAR(255))));
```

#### 2.3.2 食谱表 (recipes)

```sql
CREATE TABLE recipes (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '食谱名称',
    type VARCHAR(50) COMMENT '类型：粥类、汤类、茶饮、菜肴、点心',
    difficulty VARCHAR(20) COMMENT '难度：简单、中等、困难',
    cook_time INT COMMENT '用时（分钟）',
    servings INT COMMENT '份量',

    -- 适用信息
    suitable_constitutions JSON COMMENT '适用体质，JSON数组',
    symptoms JSON COMMENT '主治症状，JSON数组',
    suitable_seasons JSON COMMENT '适宜季节，JSON数组',

    -- 食材清单
    ingredients JSON COMMENT '食材清单，JSON结构',
    -- 格式: {"main": [{"name": "山药", "amount": "100g"}], "auxiliary": [], "seasoning": []}

    -- 制作步骤
    steps JSON COMMENT '制作步骤，JSON数组',
    -- 格式: ["步骤1", "步骤2", ...]

    -- 功效说明
    efficacy TEXT COMMENT '功效说明',
    health_benefits TEXT COMMENT '健康益处',

    -- 注意事项
    precautions TEXT COMMENT '注意事项',
    taboos TEXT COMMENT '禁忌人群',

    -- 分类标签
    tags JSON COMMENT '标签，JSON数组',
    -- 如：["健脾养胃", "补气", "早餐"]

    -- 展示
    image_url VARCHAR(255) COMMENT '图片URL',
    description TEXT COMMENT '简介',

    -- 统计
    view_count INT DEFAULT 0 COMMENT '浏览次数',
    favorite_count INT DEFAULT 0 COMMENT '收藏次数',

    -- 元数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_recipes_name ON recipes(name);
CREATE INDEX idx_recipes_type ON recipes(type);
CREATE INDEX idx_recipes_constitution ON recipes((CAST(suitable_constitutions AS CHAR(255))));
CREATE INDEX idx_recipes_symptoms ON recipes((CAST(symptoms AS CHAR(255))));
```

#### 2.3.3 食材-食谱关联表 (recipe_ingredients)

```sql
CREATE TABLE recipe_ingredients (
    id VARCHAR(36) PRIMARY KEY,
    recipe_id VARCHAR(36) NOT NULL,
    ingredient_id VARCHAR(36) NOT NULL,
    amount VARCHAR(50) COMMENT '用量',
    role VARCHAR(20) COMMENT '角色：main(主料)、auxiliary(辅料)、seasoning(调料)',
    sort_order INT DEFAULT 0,

    FOREIGN KEY (recipe_id) REFERENCES recipes(id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
    UNIQUE KEY unique_recipe_ingredient (recipe_id, ingredient_id, role)
);

CREATE INDEX idx_recipe_ingredients_recipe ON recipe_ingredients(recipe_id);
CREATE INDEX idx_recipe_ingredients_ingredient ON recipe_ingredients(ingredient_id);
```

#### 2.3.4 症状表 (symptoms)

```sql
CREATE TABLE symptoms (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) NOT NULL COMMENT '症状名称',
    category VARCHAR(50) COMMENT '分类：消化、睡眠、呼吸等',
    description TEXT COMMENT '症状描述',
    related_constitutions JSON COMMENT '相关体质，JSON数组',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_symptoms_name ON symptoms(name);
CREATE INDEX idx_symptoms_category ON symptoms(category);
```

#### 2.3.5 用户收藏表 (user_favorites)

```sql
CREATE TABLE user_favorites (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) COMMENT '用户ID（可选，用于跨端同步）',
    session_id VARCHAR(100) COMMENT '会话ID（未登录用户）',
    favorite_type VARCHAR(20) NOT NULL COMMENT '收藏类型：ingredient、recipe',
    favorite_id VARCHAR(36) NOT NULL COMMENT '收藏对象ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY unique_favorite (user_id, session_id, favorite_type, favorite_id)
);

CREATE INDEX idx_user_favorites_user ON user_favorites(user_id);
CREATE INDEX idx_user_favorites_type ON user_favorites(favorite_type, favorite_id);
```

### 2.4 API接口设计

#### 2.4.1 食材相关接口

```yaml
# 获取食材列表
GET /api/v1/ingredients
Query Parameters:
  - page: 页码
  - page_size: 每页数量
  - category: 分类筛选
  - constitution: 体质筛选
  - keyword: 搜索关键词
Response:
  code: 0
  data:
    total: 100
    items:
      - id: "xxx"
        name: "山药"
        nature: "平"
        flavor: "甘"
        image_url: "https://..."
        category: "蔬菜"

# 获取食材详情
GET /api/v1/ingredients/{id}
Response:
  code: 0
  data:
    id: "xxx"
    name: "山药"
    aliases: ["怀山药", "淮山"]
    nature: "平"
    flavor: "甘"
    meridians: ["脾", "肺", "肾"]
    efficacy: "健脾养胃、补肺益肾"
    suitable_constitutions: ["气虚质", "阴虚质"]
    avoid_constitutions: ["痰湿质"]
    compatible_with: ["莲子", "枸杞"]
    incompatible_with: ["碱性食物"]

# 根据体质推荐食材
GET /api/v1/ingredients/recommend
Query Parameters:
  - constitution: 体质类型
Response:
  code: 0
  data:
    recommended: [...]  # 推荐食材
    avoided: [...]     # 禁忌食材
```

#### 2.4.2 食谱相关接口

```yaml
# 获取食谱列表
GET /api/v1/recipes
Query Parameters:
  - page: 页码
  - page_size: 每页数量
  - type: 类型筛选
  - constitution: 体质筛选
  - symptom: 症状筛选
  - season: 季节筛选
  - keyword: 搜索关键词
Response:
  code: 0
  data:
    total: 100
    items:
      - id: "xxx"
        name: "山药莲子粥"
        type: "粥类"
        difficulty: "简单"
        cook_time: 30
        image_url: "https://..."
        suitable_constitutions: ["气虚质"]

# 获取食谱详情
GET /api/v1/recipes/{id}
Response:
  code: 0
  data:
    id: "xxx"
    name: "山药莲子粥"
    type: "粥类"
    difficulty: "简单"
    cook_time: 30
    servings: 2
    suitable_constitutions: ["气虚质", "阴虚质"]
    symptoms: ["食欲不振", "疲劳乏力"]
    suitable_seasons: ["春", "秋", "冬"]
    ingredients:
      main:
        - name: "山药"
          amount: "100g"
      auxiliary:
        - name: "莲子"
          amount: "20g"
    steps:
      - "山药去皮切小块，糯米提前浸泡2小时"
      - "锅中加水，放入糯米大火煮开"
      - "加入山药、莲子转小火煮30分钟"
      - "最后加入枸杞、冰糖煮5分钟即可"
    efficacy: "健脾养胃、补肺益气"
    precautions: "糖尿病患者慎用或少放冰糖"

# 根据体质推荐食谱
GET /api/v1/recipes/recommend
Query Parameters:
  - constitution: 体质类型
Response:
  code: 0
  data:
    breakfast: [...]   # 早餐推荐
    lunch: [...]       # 午餐推荐
    dinner: [...]      # 晚餐推荐
    snack: [...]       # 加餐推荐
```

#### 2.4.3 收藏相关接口

```yaml
# 添加收藏
POST /api/v1/favorites
Body:
  type: "recipe"  # 或 "ingredient"
  id: "xxx"
Response:
  code: 0
  data:
    id: "xxx"

# 获取收藏列表
GET /api/v1/favorites
Query Parameters:
  - type: 类型筛选（可选）
Response:
  code: 0
  data:
    ingredients: [...]
    recipes: [...]

# 取消收藏
DELETE /api/v1/favorites/{id}
Response:
  code: 0
```

### 2.5 前端页面设计

#### 2.5.1 食材库页面

```
┌─────────────────────────────────────────┐
│  食材库                    🔍 搜索      │
├─────────────────────────────────────────┤
│  分类: [全部][谷物][蔬菜][水果][药材]   │
├─────────────────────────────────────────┤
│  体质筛选:                              │
│  [气虚][阴虚][阳虚][痰湿][湿热]...     │
├─────────────────────────────────────────┤
│  ┌──────┐ ┌──────┐ ┌──────┐           │
│  │山药  │ │枸杞  │ │莲子  │           │
│  │ 甘平 │ │ 甘平 │ │ 甘平 │           │
│  │健脾  │ │滋补  │ │养心  │           │
│  └──────┘ └──────┘ └──────┘           │
│  ┌──────┐ ┌──────┐ ┌──────┐           │
│  │...   │ │...   │ │...   │           │
│  └──────┘ └──────┘ └──────┘           │
└─────────────────────────────────────────┘
```

#### 2.5.2 食材详情页

```
┌─────────────────────────────────────────┐
│  ← 返回            ⭐ 收藏   分享      │
├─────────────────────────────────────────┤
│            [山药图片]                   │
├─────────────────────────────────────────┤
│  山药 (怀山药、淮山)                    │
│                                         │
│  【性味归经】                           │
│  性：平  味：甘                         │
│  归经：脾、肺、肾经                     │
│                                         │
│  【功效】                               │
│  健脾养胃、补肺益肾                     │
│                                         │
│  【适用体质】                           │
│  ✓ 气虚质  ✓ 阴虚质                    │
│                                         │
│  【禁忌体质】                           │
│  ✗ 痰湿质                              │
│                                         │
│  【搭配宜忌】                           │
│  宜配：莲子、枸杞                       │
│  忌配：碱性食物                         │
│                                         │
│  【食用方法】                           │
│  蒸、煮、炖                             │
│  每日用量：50-100g                      │
│                                         │
│  【相关食谱】                           │
│  → 山药莲子粥  → 山药炖鸡汤            │
├─────────────────────────────────────────┤
│         [查看含有山药的食谱]            │
└─────────────────────────────────────────┘
```

#### 2.5.3 食谱库页面

```
┌─────────────────────────────────────────┐
│  食疗食谱                🔍 搜索      │
├─────────────────────────────────────────┤
│  分类: [全部][粥类][汤类][茶饮][菜肴]   │
├─────────────────────────────────────────┤
│  筛选:                                  │
│  体质 [气虚质 ▼]  症状 [食欲不振 ▼]    │
├─────────────────────────────────────────┤
│  ┌────────────────┐ ┌────────────────┐ │
│  │ [山药莲子粥图] │ │ [红枣桂圆汤图] │ │
│  │ 山药莲子粥     │ │ 红枣桂圆汤     │ │
│  │ 简单 | 30分钟  │ │ 简单 | 45分钟  │ │
│  │ 健脾养胃       │ │ 补血养颜       │ │
│  │ ⭐ 1.2k        │ │ ⭐ 856         │ │
│  └────────────────┘ └────────────────┘ │
│  ┌────────────────┐ ┌────────────────┐ │
│  │ ...            │ │ ...            │ │
│  └────────────────┘ └────────────────┘ │
└─────────────────────────────────────────┘
```

#### 2.5.4 食谱详情页

```
┌─────────────────────────────────────────┐
│  ← 返回         ⭐ 收藏   分享   推荐  │
├─────────────────────────────────────────┤
│         [食谱大图]                       │
│                                         │
│  山药莲子粥                             │
│  简单 | 30分钟 | 2人份                  │
│                                         │
│  【适合体质】                           │
│  ✓ 气虚质  ✓ 阴虚质                    │
│                                         │
│  【功效】                               │
│  健脾养胃、补肺益气                     │
│  适合脾胃虚弱、食欲不振者               │
├─────────────────────────────────────────┤
│  【食材】                               │
│  主料：                                 │
│  • 山药 100g                            │
│  • 糯米 50g                             │
│  辅料：                                 │
│  • 莲子 20g                             │
│  • 枸杞 10g                             │
│  调料：                                 │
│  • 冰糖 适量                            │
├─────────────────────────────────────────┤
│  【制作步骤】                           │
│  1. 山药去皮切小块，糯米提前浸泡2小时  │
│  2. 锅中加水，放入糯米大火煮开         │
│  3. 加入山药、莲子转小火煮30分钟       │
│  4. 最后加入枸杞、冰糖煮5分钟即可      │
├─────────────────────────────────────────┤
│  【注意事项】                           │
│  • 糖尿病患者慎用或少放冰糖            │
│  • 孕妇不宜过量食用                    │
├─────────────────────────────────────────┤
│  【推荐搭配】                           │
│  → 红枣桂圆汤  → 枸杞茶                │
└─────────────────────────────────────────┘
```

### 2.6 初始数据

需要准备的食材和食谱数据：

#### 食材分类
```yaml
谷物类: ["大米", "小米", "糯米", "红豆", "绿豆", "黑豆", "黄豆"]
蔬菜类: ["山药", "莲藕", "百合", "白萝卜", "胡萝卜", "冬瓜"]
水果类: ["苹果", "梨", "红枣", "桂圆", "枸杞", "山楂"]
肉类: ["鸡肉", "排骨", "羊肉", "牛肉"]
药材类: ["黄芪", "当归", "党参", "茯苓", "陈皮", "甘草"]
```

#### 基础食谱（10-20个）
```yaml
粥类:
  - 山药莲子粥
  - 红枣小米粥
  - 百合银耳粥
  - 绿豆百合粥

汤类:
  - 红枣桂圆汤
  - 当归黄芪鸡汤
  - 莲子百合汤
  - 冬瓜排骨汤

茶饮:
  - 枸杞菊花茶
  - 红枣姜茶
  - 山楂陈皮茶
  - 玫瑰花茶
```

---

## 三、穴位查找

### 3.1 功能概述

提供人体穴位查询功能，支持按症状查找穴位、按部位查找穴位，展示穴位位置、功效、按摩方法。

### 3.2 核心功能

#### 3.2.1 穴位列表

- 按部位分类（头面部、颈部、胸腹部、背部、上肢、下肢）
- 按经络分类（十二经脉、任督二脉）
- 搜索功能

#### 3.2.2 穴位详情

```yaml
穴位基本信息:
  - 名称: "足三里"
  - 拼音: "zusanli"
  - 代号: "ST36"
  - 所属经络: "足阳明胃经"

位置信息:
  - 部位: "小腿前外侧"
  - 定位: "犊鼻下3寸，胫骨前缘外一横指"
  - 简易取穴: "膝盖骨外侧下方凹陷往下四横指"

功效主治:
  - 主要功效: ["健脾和胃", "扶正培元", "调理气血"]
  - 主治病症: ["胃痛", "消化不良", "失眠", "疲劳"]

按摩方法:
  - 按摩手法: "用拇指指腹按压"
  - 按摩时间: "3-5分钟"
  - 按摩频率: "每日1-2次"
  - 注意事项: "孕妇慎用"

3D展示:
  - 人体模型上的位置标注
  - 多角度展示
  - 取穴动画演示

相关穴位:
  - 配伍: ["中脘", "内关"]
  - 邻近: ["上巨虚", "下巨虚"]
```

#### 3.2.3 按症状查找

用户输入症状（如"失眠"、"头痛"），系统推荐相关穴位。

### 3.3 数据库设计

#### 3.3.1 穴位表 (acupoints)

```sql
CREATE TABLE acupoints (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) NOT NULL COMMENT '穴位名称',
    pinyin VARCHAR(100) COMMENT '拼音',
    code VARCHAR(20) COMMENT '国际代号',
    meridian VARCHAR(50) COMMENT '所属经络',

    -- 位置信息
    body_part VARCHAR(50) COMMENT '部位：头面、颈、胸腹、背、上肢、下肢',
    location TEXT COMMENT '定位描述',
    simple_location TEXT COMMENT '简易取穴法',
    anatomic_guide TEXT COMMENT '解剖层次',

    -- 功效主治
    efficacy JSON COMMENT '功效，JSON数组',
    indications JSON COMMENT '主治病症，JSON数组',

    -- 按摩方法
    massage_method TEXT COMMENT '按摩手法',
    massage_duration VARCHAR(50) COMMENT '按摩时长',
    massage_frequency VARCHAR(50) COMMENT '按摩频率',
    precautions TEXT COMMENT '注意事项',

    -- 多媒体
    image_url VARCHAR(255) COMMENT '图片URL',
    model_coordinates JSON COMMENT '3D模型坐标',
    video_url VARCHAR(255) COMMENT '演示视频URL',

    -- 关联
    related_acupoints JSON COMMENT '配伍穴位，JSON数组',
    neighboring_acupoints JSON COMMENT '邻近穴位，JSON数组',

    -- 统计
    view_count INT DEFAULT 0,
    favorite_count INT DEFAULT 0,

    -- 元数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_acupoints_name ON acupoints(name);
CREATE INDEX idx_acupoints_meridian ON acupoints(meridian);
CREATE INDEX idx_acupoints_body_part ON acupoints(body_part);
CREATE INDEX idx_acupoints_indications ON acupoints((CAST(indications AS CHAR(255))));
```

#### 3.3.2 症状-穴位关联表 (symptom_acupoints)

```sql
CREATE TABLE symptom_acupoints (
    id VARCHAR(36) PRIMARY KEY,
    symptom_name VARCHAR(100) NOT NULL COMMENT '症状名称',
    acupoint_id VARCHAR(36) NOT NULL COMMENT '穴位ID',
    priority INT DEFAULT 0 COMMENT '优先级，数字越小越优先',

    FOREIGN KEY (acupoint_id) REFERENCES acupoints(id)
);

CREATE INDEX idx_symptom_acupoints_symptom ON symptom_acupoints(symptom_name);
CREATE INDEX idx_symptom_acupoints_acupoint ON symptom_acupoints(acupoint_id);
```

### 3.4 API接口设计

```yaml
# 获取穴位列表
GET /api/v1/acupoints
Query Parameters:
  - page: 页码
  - page_size: 每页数量
  - meridian: 经络筛选
  - body_part: 部位筛选
  - keyword: 搜索关键词
Response:
  code: 0
  data:
    total: 100
    items:
      - id: "xxx"
        name: "足三里"
        code: "ST36"
        meridian: "足阳明胃经"
        body_part: "下肢"

# 获取穴位详情
GET /api/v1/acupoints/{id}
Response:
  code: 0
  data:
    id: "xxx"
    name: "足三里"
    pinyin: "zusanli"
    code: "ST36"
    meridian: "足阳明胃经"
    body_part: "下肢"
    location: "犊鼻下3寸，胫骨前缘外一横指"
    simple_location: "膝盖骨外侧下方凹陷往下四横指"
    efficacy: ["健脾和胃", "扶正培元", "调理气血"]
    indications: ["胃痛", "消化不良", "失眠", "疲劳"]
    massage_method: "用拇指指腹按压"
    massage_duration: "3-5分钟"
    massage_frequency: "每日1-2次"
    image_url: "https://..."
    related_acupoints: ["中脘", "内关"]

# 按症状查找穴位
GET /api/v1/acupoints/by-symptom
Query Parameters:
  - symptom: 症状名称
Response:
  code: 0
  data:
    symptom: "失眠"
    acupoints:
      - id: "xxx"
        name: "神门"
        priority: 1
      - id: "yyy"
        name: "内关"
        priority: 2
```

### 3.5 前端页面设计

#### 3.5.1 穴位查找首页

```
┌─────────────────────────────────────────┐
│  穴位查找                🔍 搜索穴位    │
├─────────────────────────────────────────┤
│  按部位查找：                           │
│  [头面][颈部][胸腹][背部][上肢][下肢]   │
├─────────────────────────────────────────┤
│  按经络查找：                           │
│  [胃经][脾经][心经][肺经]...            │
├─────────────────────────────────────────┤
│  热门穴位：                             │
│  ┌──────────┐ ┌──────────┐             │
│  │ 足三里   │ │ 三阴交   │             │
│  │ ST36     │ │ SP6      │             │
│  │ 健脾和胃 │ │ 调理气血 │             │
│  └──────────┘ └──────────┘             │
│  ┌──────────┐ ┌──────────┐             │
│  │ 合谷     │ │ 内关     │             │
│  │ LI4      │ │ PC6      │             │
│  │ 镇静止痛 │ │ 宁心安神 │             │
│  └──────────┘ └──────────┘             │
├─────────────────────────────────────────┤
│  按症状查找：                           │
│  [失眠] [头痛] [胃痛] [便秘] ...       │
└─────────────────────────────────────────┘
```

#### 3.5.2 穴位详情页

```
┌─────────────────────────────────────────┐
│  ← 返回        ⭐ 收藏    分享         │
├─────────────────────────────────────────┤
│                                         │
│       [穴位位置图示]                    │
│                                         │
│  足三里 (Zusanli)                       │
│  ST36  |  足阳明胃经                    │
├─────────────────────────────────────────┤
│  【位置】                               │
│  小腿前外侧                             │
│  犊鼻下3寸，胫骨前缘外一横指           │
│                                         │
│  【简易取穴】                           │
│  膝盖骨外侧下方凹陷往下四横指           │
│  [查看取穴演示视频]                     │
├─────────────────────────────────────────┤
│  【功效】                               │
│  • 健脾和胃                             │
│  • 扶正培元                             │
│  • 调理气血                             │
├─────────────────────────────────────────┤
│  【主治】                               │
│  胃痛、消化不良、失眠、疲劳、膝痛       │
├─────────────────────────────────────────┤
│  【按摩方法】                           │
│  手法：用拇指指腹按压                   │
│  时间：3-5分钟                          │
│  频率：每日1-2次                        │
│  [查看按摩演示]                         │
├─────────────────────────────────────────┤
│  【注意事项】                           │
│  • 孕妇慎用                             │
│  • 按压力度适中，有酸胀感为宜           │
├─────────────────────────────────────────┤
│  【配伍穴位】                           │
│  • 中脘 + 足三里：健脾和胃              │
│  • 内关 + 足三里：调理肠胃              │
└─────────────────────────────────────────┘
```

#### 3.5.3 按症状查找页

```
┌─────────────────────────────────────────┐
│  ← 返回         症状：失眠             │
├─────────────────────────────────────────┤
│  推荐穴位：                             │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ 神门 (HT7)                         │ │
│  │ 心包经 • 宁心安神                  │ │
│  │                                    │ │
│  │ [位置图示]                         │ │
│  │ 腕横纹尺侧端，尺侧腕屈肌腱桡侧凹陷处│ │
│  │                                    │ │
│  │ 按摩3-5分钟，每日1-2次             │ │
│  │ [查看详情 →]                      │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ 内关 (PC6)                         │ │
│  │ 心包经 • 宁心安神                  │ │
│  │ ...                               │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ 三阴交 (SP6)                       │ │
│  │ 脾经 • 调理气血                   │ │
│  │ ...                               │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### 3.6 初始数据

需要准备的穴位数据（按优先级）：

#### 常用穴位（30-50个）
```yaml
头面部:
  - 百会: 头顶正中，升阳举陷
  - 太阳: 眉梢与目外眦之间，清肝明目
  - 印堂: 两眉中间，镇静安神
  - 人中: 鼻唇沟上1/3处，醒神开窍

上肢:
  - 合谷: 手背虎口处，镇痛要穴
  - 内关: 腕横纹上2寸，宁心安神
  - 神门: 腕横纹尺侧端，宁心安神
  - 曲池: 屈肘成直角，肘横纹外侧端

下肢:
  - 足三里: 犊鼻下3寸，保健要穴
  - 三阴交: 内踝上3寸，调理气血
  - 太冲: 足背第一二跖骨间，平肝息风
  - 涌泉: 足底前1/3处，补肾固本

胸腹部:
  - 中脘: 脐上4寸，健脾和胃
  - 关元: 脐下3寸，培元固本
  - 气海: 脐下1.5寸，益气固表

背部:
  - 肺俞: 第三胸椎下，调肺气
  - 心俞: 第五胸椎下，安心神
  - 肾俞: 第二腰椎下，补肾气
```

#### 常见症状映射
```yaml
失眠: [神门, 内关, 三阴交, 百会]
头痛: [太阳, 合谷, 太冲, 风池]
胃痛: [中脘, 足三里, 内关, 合谷]
便秘: [天枢, 足三里, 支沟]
痛经: [三阴交, 关元, 气海, 太冲]
```

---

## 四、AI舌诊

### 4.1 功能概述

用户拍摄舌象照片，通过AI分析舌质、舌苔、舌形，给出体质倾向和健康建议。

### 4.2 核心功能

#### 4.2.1 拍照上传

- 调用相机拍照
- 从相册选择
- 拍照引导（光线、角度、位置）

#### 4.2.2 AI分析

```yaml
舌质分析:
  - 颜色: 淡白/淡红/红/绛/紫
  - 形态: 胖大/瘦薄/齿痕/裂纹
  - 动态: 萎软/强硬/歪斜

舌苔分析:
  - 苔色: 白苔/黄苔/灰黑苔
  - 苔质: 厚苔/薄苔/腻苔/剥落苔
  - 润燥: 润苔/燥苔/糙苔

舌形分析:
  - 大小: 正常/胖大/瘦薄
  - 形状: 正常/齿痕/裂纹/点刺

综合判断:
  - 体质倾向
  - 健康状态
  - 调理建议
```

#### 4.2.3 分析报告

```
┌─────────────────────────────────────────┐
│  ← 返回         保存报告   分享         │
├─────────────────────────────────────────┤
│                                         │
│       [用户上传的舌象照片]              │
│                                         │
├─────────────────────────────────────────┤
│  AI分析结果                             │
│                                         │
│  【舌质】淡白，有齿痕                   │
│  → 提示：气血不足，脾虚湿盛             │
│                                         │
│  【舌苔】薄白苔                          │
│  → 提示：正常或轻度寒湿                 │
│                                         │
│  【舌形】胖大有齿痕                     │
│  → 提示：脾虚湿盛                       │
│                                         │
├─────────────────────────────────────────┤
│  【综合判断】                           │
│  体质倾向：气虚质                       │
│  可能表现：疲劳乏力、食欲不振、便溏     │
│                                         │
│  【调理建议】                           │
│  1. 饮食：多食山药、莲子、大枣等健脾食物│
│  2. 起居：避免过度劳累，保证充足睡眠    │
│  3. 运动：适度运动，如散步、太极        │
│  4. 情志：保持心情舒畅，避免思虑过度    │
│                                         │
│  【推荐穴位】                           │
│  • 足三里：健脾和胃                     │
│  • 三阴交：调理气血                     │
│                                         │
│  【推荐食谱】                           │
│  → 山药莲子粥                           │
│  → 黄芪炖鸡汤                           │
│                                         │
│  ⚠️ 本结果仅供参考，如有不适请就医      │
├─────────────────────────────────────────┤
│  [重新拍摄]  [查看详细解读]             │
│  [完成体质测试]  [咨询专家]             │
└─────────────────────────────────────────┘
```

### 4.3 技术实现方案

#### 方案A：调用第三方AI API（推荐第一版）

```python
# 使用百度AI、腾讯云AI等图像识别API
from qcloud_image_sdk import QcloudImage

class TongueDiagnosisService:
    def analyze(self, image_url):
        # 1. 调用AI API分析舌象
        result = ai_api.analyze_image(image_url)

        # 2. 提取舌象特征
        tongue_color = result['color']
        tongue_coating = result['coating']
        tongue_shape = result['shape']

        # 3. 匹配体质
        constitution = self.match_constitution(
            tongue_color, tongue_coating, tongue_shape
        )

        # 4. 生成建议
        recommendations = self.get_recommendations(constitution)

        return {
            'tongue_color': tongue_color,
            'tongue_coating': tongue_coating,
            'tongue_shape': tongue_shape,
            'constitution': constitution,
            'recommendations': recommendations
        }
```

#### 方案B：自建AI模型（后期）

- 收集舌象数据集
- 训练CNN分类模型
- 部署为API服务

### 4.4 数据库设计

#### 4.4.1 舌诊记录表 (tongue_diagnosis_records)

```sql
CREATE TABLE tongue_diagnosis_records (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) COMMENT '用户ID（可选）',
    session_id VARCHAR(100) COMMENT '会话ID（未登录用户）',

    -- 图片
    image_url VARCHAR(255) NOT NULL COMMENT '舌象图片URL',

    -- AI分析结果
    tongue_color VARCHAR(50) COMMENT '舌质颜色',
    tongue_shape VARCHAR(50) COMMENT '舌质形态',
    tongue_coating_color VARCHAR(50) COMMENT '舌苔颜色',
    tongue_coating_thickness VARCHAR(50) COMMENT '舌苔厚薄',
    tongue_coating_quality VARCHAR(50) COMMENT '舌苔质地',

    -- 判断结果
    constitution_tendency VARCHAR(50) COMMENT '体质倾向',
    health_status TEXT COMMENT '健康状况描述',

    -- 建议
    diet_advice TEXT COMMENT '饮食建议',
    lifestyle_advice TEXT COMMENT '生活建议',
    acupoints JSON COMMENT '推荐穴位，JSON数组',
    recipes JSON COMMENT '推荐食谱，JSON数组',

    -- 元数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tongue_records_user ON tongue_diagnosis_records(user_id);
CREATE INDEX idx_tongue_records_session ON tongue_diagnosis_records(session_id);
```

#### 4.4.2 舌象特征-体质映射表 (tongue_constitution_mapping)

```sql
CREATE TABLE tongue_constitution_mapping (
    id VARCHAR(36) PRIMARY KEY,
    tongue_color VARCHAR(50),
    tongue_shape VARCHAR(50),
    coating_color VARCHAR(50),
    coating_thickness VARCHAR(50),
    constitution VARCHAR(50) NOT NULL,
    confidence DECIMAL(3,2) DEFAULT 0.80,
    advice TEXT
);
```

### 4.5 API接口设计

```yaml
# 上传舌象照片进行分析
POST /api/v1/tongue-diagnosis/analyze
Body:
  image: base64编码的图片 或 图片URL
Response:
  code: 0
  data:
    id: "xxx"
    image_url: "https://..."
    analysis:
      tongue_color: "淡白"
      tongue_shape: "胖大有齿痕"
      tongue_coating_color: "白"
      tongue_coating_thickness: "薄"
      tongue_coating_quality: "润"
    conclusion:
      constitution_tendency: "气虚质"
      health_status: "气血不足，脾虚湿盛"
      possible_symptoms: ["疲劳乏力", "食欲不振", "便溏"]
    advice:
      diet: "多食山药、莲子、大枣等健脾食物"
      lifestyle: "避免过度劳累，保证充足睡眠"
      exercise: "适度运动，如散步、太极"
      emotion: "保持心情舒畅，避免思虑过度"
    recommendations:
      acupoints:
        - name: "足三里"
          reason: "健脾和胃"
        - name: "三阴交"
          reason: "调理气血"
      recipes:
        - id: "xxx"
          name: "山药莲子粥"
          reason: "健脾养胃"

# 获取舌诊历史
GET /api/v1/tongue-diagnosis/history
Response:
  code: 0
  data:
    total: 5
    items:
      - id: "xxx"
        image_url: "https://..."
        constitution_tendency: "气虚质"
        created_at: "2026-01-18"
```

### 4.6 拍照引导

```yaml
拍照前引导:
  1. 光线要求:
     - 选择自然光或明亮环境
     - 避免强光直射
     - 避免阴影遮挡

  2. 姿势要求:
     - 自然伸出舌头
     - 舌头放松不要用力
     - 保持3-5秒

  3. 拍摄角度:
     - 正对舌头
     - 包含整个舌面
     - 距离10-15cm

  4. 注意事项:
     - 拍照前不要喝有色饮料
     - 不要刷牙后立即拍照
     - 女性避开月经期

拍照中辅助:
  - 实时预览框
  - 光线检测提示
  - 距离提示
  - 自动对焦
```

### 4.7 舌象-体质判断规则（简化版）

```python
TONGUE_CONSTITUTION_RULES = {
    '气虚质': {
        'tongue_color': ['淡白', '淡红'],
        'tongue_shape': ['胖大', '齿痕'],
        'coating_color': ['白'],
        'coating_thickness': ['薄'],
    },
    '阴虚质': {
        'tongue_color': ['红', '绛'],
        'tongue_shape': ['瘦薄'],
        'coating_color': ['黄', '少'],
        'coating_thickness': ['薄', '剥落'],
    },
    '阳虚质': {
        'tongue_color': ['淡白', '青紫'],
        'tongue_shape': ['胖大', '湿润'],
        'coating_color': ['白', '滑'],
        'coating_thickness': ['薄', '白滑'],
    },
    '痰湿质': {
        'tongue_color': ['淡红', '淡白'],
        'tongue_shape': ['胖大', '齿痕'],
        'coating_color': ['白', '黄'],
        'coating_thickness': ['厚腻', '白腻'],
    },
    '湿热质': {
        'tongue_color': ['红'],
        'tongue_shape': ['正常', '红'],
        'coating_color': ['黄'],
        'coating_thickness': ['厚腻', '黄腻'],
    },
}
```

---

## 五、免费养生课程

### 5.1 功能概述

提供免费的中医养生知识内容，包括短视频、图文文章，帮助用户学习养生知识。

### 5.2 核心功能

#### 5.2.1 内容分类

```yaml
按主题分类:
  - 体质养生: 针对不同体质的养生方法
  - 四季养生: 春夏秋冬的养生要点
  - 食疗养生: 食材功效、食谱搭配
  - 经络养生: 穴位按摩、经络疏通
  - 情志养生: 心理调节、情绪管理
  - 起居养生: 作息规律、生活习惯

按形式分类:
  - 短视频: 1-3分钟养生知识
  - 图文: 养生科普文章
  - 音频: 养生知识讲解
```

#### 5.2.2 内容展示

**视频列表页：**
```
┌─────────────────────────────────────────┐
│  养生课堂                                │
├─────────────────────────────────────────┤
│  [体质养生][四季养生][食疗][经络]       │
├─────────────────────────────────────────┤
│  ┌────────────────┐ ┌────────────────┐ │
│  │ [视频缩略图]   │ │ [视频缩略图]   │ │
│  │ 气虚质怎么调理? │ │ 春天养生重点   │ │
│  │ 02:15 | 1.2万  │ │ 03:20 | 8565   │ │
│  └────────────────┘ └────────────────┘ │
│  ┌────────────────┐ ┌────────────────┐ │
│  │ ...            │ │ ...            │ │
│  └────────────────┘ └────────────────┘ │
└─────────────────────────────────────────┘
```

**视频播放页：**
```
┌─────────────────────────────────────────┐
│  ← 返回         分享   收藏             │
├─────────────────────────────────────────┤
│                                         │
│         [视频播放器]                    │
│                                         │
├─────────────────────────────────────────┤
│  气虚质怎么调理？                        │
│                                         │
│  【简介】                               │
│  气虚质的表现、成因、调理方法           │
│                                         │
│  【要点】                               │
│  • 饮食：多食健脾益气食物               │
│  • 运动：适度运动，避免过度劳累          │
│  • 起居：规律作息，保证充足睡眠          │
│  • 情志：避免思虑过度                   │
│                                         │
│  【相关推荐】                           │
│  → 气虚质推荐食谱                       │
│  → 足三里穴位按摩                       │
│  → 春季养阳方法                         │
├─────────────────────────────────────────┤
│  [查看评论]  [更多相关课程]             │
└─────────────────────────────────────────┘
```

**图文列表页：**
```
┌─────────────────────────────────────────┐
│  养生知识                                │
├─────────────────────────────────────────┤
│  [最新][最热][收藏最多]                 │
├─────────────────────────────────────────┤
│  ┌───────────────────────────────────┐ │
│  │ [封面图]                           │ │
│  │ 春天养肝正当时                     │ │
│  │ 春季是养肝的最佳时期，本文详细... │ │
│  │ 2026-01-15 | 👁 1.2万 | ⭐ 356    │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ [封面图]                           │ │
│  │ 九种体质的食疗方法                 │ │
│  │ 不同体质适合不同的食疗方案...     │ │
│  │ 2026-01-12 | 👁 8565 | ⭐ 228    │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

#### 5.2.3 搜索功能

- 按关键词搜索
- 按体质筛选
- 按季节筛选
- 按症状筛选

### 5.3 数据库设计

#### 5.3.1 课程表 (courses)

```sql
CREATE TABLE courses (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(200) NOT NULL COMMENT '标题',
    description TEXT COMMENT '简介',

    -- 分类
    category VARCHAR(50) COMMENT '分类：体质、四季、食疗、经络、情志、起居',
    subcategory VARCHAR(50) COMMENT '子分类',

    -- 内容类型
    content_type VARCHAR(20) NOT NULL COMMENT '类型：video、article、audio',
    content_url VARCHAR(255) COMMENT '内容URL',

    -- 封面
    cover_image VARCHAR(255) COMMENT '封面图片',

    -- 标签
    tags JSON COMMENT '标签，JSON数组',
    -- 如：["气虚质", "健脾", "食疗"]

    -- 适用信息
    suitable_constitutions JSON COMMENT '适用体质，JSON数组',
    suitable_seasons JSON COMMENT '适用季节，JSON数组',
    related_symptoms JSON COMMENT '相关症状，JSON数组',

    -- 时长
    duration INT COMMENT '时长（秒）',

    -- 难度
    difficulty VARCHAR(20) COMMENT '难度：入门、进阶、高级',

    -- 作者
    author VARCHAR(100) COMMENT '作者/讲师',
    author_title VARCHAR(100) COMMENT '作者职称',

    -- 统计
    view_count INT DEFAULT 0 COMMENT '浏览次数',
    favorite_count INT DEFAULT 0 COMMENT '收藏次数',
    share_count INT DEFAULT 0 COMMENT '分享次数',
    like_count INT DEFAULT 0 COMMENT '点赞次数',

    -- 状态
    is_published BOOLEAN DEFAULT TRUE COMMENT '是否发布',
    is_featured BOOLEAN DEFAULT FALSE COMMENT '是否精选',

    -- 元数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_courses_category ON courses(category);
CREATE INDEX idx_courses_type ON courses(content_type);
CREATE INDEX idx_courses_published ON courses(is_published);
CREATE INDEX idx_courses_featured ON courses(is_featured);
```

#### 5.3.2 课程内容表 (course_content)

```sql
CREATE TABLE course_content (
    id VARCHAR(36) PRIMARY KEY,
    course_id VARCHAR(36) NOT NULL,
    content_type VARCHAR(20) COMMENT '类型：text、video、image',
    content TEXT COMMENT '内容',
    sort_order INT DEFAULT 0,

    FOREIGN KEY (course_id) REFERENCES courses(id)
);
```

### 5.4 API接口设计

```yaml
# 获取课程列表
GET /api/v1/courses
Query Parameters:
  - page: 页码
  - page_size: 每页数量
  - category: 分类筛选
  - content_type: 内容类型筛选
  - constitution: 体质筛选
  - keyword: 搜索关键词
Response:
  code: 0
  data:
    total: 100
    items:
      - id: "xxx"
        title: "气虚质怎么调理？"
        description: "气虚质的表现、成因、调理方法"
        category: "体质养生"
        content_type: "video"
        cover_image: "https://..."
        duration: 135
        view_count: 12000
        author: "张医师"

# 获取课程详情
GET /api/v1/courses/{id}
Response:
  code: 0
  data:
    id: "xxx"
    title: "气虚质怎么调理？"
    description: "..."
    category: "体质养生"
    content_type: "video"
    content_url: "https://..."
    cover_image: "https://..."
    duration: 135
    author: "张医师"
    author_title: "中医执业医师"
    tags: ["气虚质", "健脾", "食疗"]
    suitable_constitutions: ["气虚质"]
    view_count: 12000
    favorite_count: 356
    created_at: "2026-01-15"
    content:
      - type: "video"
        url: "https://..."
      - type: "text"
        content: "气虚质的主要表现..."

# 相关课程推荐
GET /api/v1/courses/{id}/related
Response:
  code: 0
  data:
    items:
      - id: "yyy"
        title: "气虚质推荐食谱"
        category: "食疗养生"
```

### 5.5 初始内容规划

#### 5.5.1 体质养生系列（10个视频）

```yaml
气虚质:
  - 气虚质的表现与判断 (02:00)
  - 气虚质的饮食调理 (02:30)
  - 气虚质的穴位按摩 (02:00)
  - 气虚质的运动建议 (01:30)

阴虚质:
  - 阴虚质的表现与判断 (02:00)
  - 阴虚质的饮食调理 (02:30)

阳虚质:
  - 阳虚质的表现与判断 (02:00)
  - 阳虚质的饮食调理 (02:30)

痰湿质:
  - 痰湿质的表现与判断 (02:00)
  - 痰湿质的饮食调理 (02:30)
```

#### 5.5.2 四季养生系列（4个视频）

```yaml
春季:
  - 春天养肝正当时 (03:00)

夏季:
  - 夏季养心防暑热 (03:00)

秋季:
  - 秋季养肺防干燥 (03:00)

冬季:
  - 冬季养肾藏精要 (03:00)
```

#### 5.5.3 食疗养生系列（10个视频）

```yaml
食材介绍:
  - 山药：健脾养胃高手 (02:00)
  - 红枣：补血安神佳品 (02:00)
  - 枸杞：滋补肝肾明目 (02:00)

食疗方法:
  - 粥类的养生功效 (02:30)
  - 汤类的制作与功效 (02:30)
  - 茶饮的搭配与禁忌 (02:00)
```

#### 5.5.4 图文内容（20篇）

```yaml
体质相关:
  - 九种体质自测与调理建议
  - 气虚质的日常养护指南
  - 阴虚质的饮食禁忌

食疗相关:
  - 四季养生食材推荐
  - 常见食材性味速查
  - 药食同源食材大全

穴位相关:
  - 十大保健穴位介绍
  - 常见症状的穴位按摩
  - 穴位按摩的正确方法

起居相关:
  - 十二时辰养生法
  - 最佳睡眠时间与质量
  - 四季作息调整建议
```

---

## 六、技术架构

### 6.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                        前端层                               │
├─────────────────────────────────────────────────────────────┤
│  uni-app (微信小程序 + H5)                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │体质测试  │ │食疗商城  │ │穴位查找  │ │养生课堂  │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        API层                                │
├─────────────────────────────────────────────────────────────┤
│  FastAPI Backend                                            │
│  ┌────────────────┐ ┌────────────────┐                    │
│  │ 食材/食谱API   │ │ 穴位API        │                    │
│  ├────────────────┤ ├────────────────┤                    │
│  │ 舌诊AI API     │ │ 课程内容API    │                    │
│  └────────────────┘ └────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        数据层                               │
├─────────────────────────────────────────────────────────────┤
│  ┌────────────┐ ┌────────────┐ ┌────────────┐             │
│  │ PostgreSQL │ │   Redis    │ │   OSS      │             │
│  │  主数据库  │ │   缓存     │ │  文件存储  │             │
│  └────────────┘ └────────────┘ └────────────┘             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        外部服务                             │
├─────────────────────────────────────────────────────────────┤
│  • AI图像识别API（舌诊）                                    │
│  • OSS对象存储                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 技术栈

#### 前端
```yaml
框架: uni-app
语言: Vue 3 + JavaScript
UI: 自定义样式
状态管理: Pinia
HTTP: uni.request
```

#### 后端
```yaml
框架: FastAPI
语言: Python 3.11+
数据库: PostgreSQL + Redis
ORM: SQLAlchemy
文件存储: 腾讯云 COS / 阿里云 OSS
AI服务: 腾讯云AI / 百度AI
```

### 6.3 部署架构

```
┌─────────────────────────────────────────────────────────────┐
│                        部署方案                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  前端:                                                      │
│  ┌──────────────┐     ┌──────────────┐                    │
│  │ 微信小程序   │     │  H5静态站    │                    │
│  │  (微信云开发) │     │ (Vercel)     │                    │
│  └──────────────┘     └──────────────┘                    │
│                                                             │
│  后端:                                                      │
│  ┌──────────────────────────────────────────────────┐      │
│  │  FastAPI 服务                                     │      │
│  │  (Railway / Render)                              │      │
│  └──────────────────────────────────────────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 七、开发计划

### 7.1 开发周期

| 阶段 | 功能 | 工期 | 负责人 |
|-----|-----|-----|--------|
| **Week 1-2** | 食材库开发 | 2周 | |
| **Week 3-4** | 食谱库开发 | 2周 | |
| **Week 5-6** | 穴位查找开发 | 2周 | |
| **Week 7-8** | AI舌诊开发 | 2周 | |
| **Week 9-10** | 养生课程开发 | 2周 | |
| **Week 11-12** | 联调测试 | 2周 | |
| **总计** | | **12周** | |

### 7.2 里程碑

| 里程碑 | 时间 | 交付物 |
|--------|-----|--------|
| M1 | Week 2 | 食材库上线 |
| M2 | Week 4 | 食材库+食谱库上线 |
| M3 | Week 6 | 加入穴位查找功能 |
| M4 | Week 8 | 加入AI舌诊功能 |
| M5 | Week 10 | 加入养生课程 |
| M6 | Week 12 | 第一期完整版上线 |

---

## 八、数据准备清单

### 8.1 食材数据
- [ ] 准备50-100种常见食材
- [ ] 填写性味归经信息
- [ ] 标注适用/禁忌体质
- [ ] 准备食材图片

### 8.2 食谱数据
- [ ] 准备30-50个食疗食谱
- [ ] 详细食材配比
- [ ] 制作步骤说明
- [ ] 准备成品图片

### 8.3 穴位数据
- [ ] 准备30-50个常用穴位
- [ ] 位置描述和取穴方法
- [ ] 功效主治说明
- [ ] 准备穴位图示

### 8.4 症状-穴位映射
- [ ] 准备20个常见症状
- [ ] 对应穴位推荐

### 8.5 课程内容
- [ ] 录制/准备10-15个短视频
- [ ] 撰写20篇图文内容
- [ ] 准备封面图片

### 8.6 舌诊规则
- [ ] 定义舌象特征判断规则
- [ ] 准备体质-舌象映射表
- [ ] 准备调理建议模板

---

## 九、验收标准

### 9.1 功能验收

| 功能 | 验收标准 |
|-----|---------|
| 食材库 | 可搜索、筛选、查看详情 |
| 食谱库 | 可按体质推荐、查看详情 |
| 穴位查找 | 可按部位/经络/症状查找 |
| AI舌诊 | 可拍照、生成分析报告 |
| 养生课程 | 可浏览、播放视频 |

### 9.2 性能验收

| 指标 | 目标值 |
|-----|--------|
| 页面加载时间 | < 2秒 |
| API响应时间 | < 500ms |
| 图片加载 | 使用CDN，< 1秒 |
| 视频播放 | 流畅无卡顿 |

### 9.3 用户体验验收

| 指标 | 目标值 |
|-----|--------|
| 操作流程 | 简单直观 |
| 错误提示 | 清晰明确 |
| 视觉设计 | 统一美观 |
| 兼容性 | 微信小程序 + H5 |

---

## 十、附录

### 10.1 食材分类参考

```yaml
谷物类:
  - 温性: 糯米、高粱、稷米
  - 平性: 大米、小米、玉米、小麦
  - 凉性: 薏米、荞麦

蔬菜类:
  - 温性: 姜、蒜、韭菜、南瓜
  - 平性: 山药、土豆、胡萝卜
  - 凉性: 冬瓜、黄瓜、苦瓜、芹菜

水果类:
  - 温性: 樱桃、石榴、荔枝
  - 平性: 苹果、葡萄、无花果
  - 凉性: 梨、西瓜、柿子

肉类:
  - 温性: 羊肉、鸡肉、虾
  - 平性: 猪肉、鸭肉
  - 凉性: 兔肉、鸭肉

药材类:
  - 补气: 人参、黄芪、党参
  - 补血: 当归、熟地、白芍
  - 补阴: 枸杞、百合、麦冬
  - 补阳: 鹿茸、肉桂、淫羊藿
```

### 10.2 穴位参考数据

```yaml
保健要穴:
  足三里 ST36:
    - 位置: 小腿前外侧，犊鼻下3寸
    - 功效: 健脾和胃、扶正培元
    - 保健: 每日按摩3-5分钟

  三阴交 SP6:
    - 位置: 小腿内侧，内踝上3寸
    - 功效: 调理气血、健脾益肾
    - 保健: 每日按摩3-5分钟

  涌泉 KI1:
    - 位置: 足底前1/3处
    - 功效: 补肾固本、安神助眠
    - 保健: 睡前按摩5分钟

  合谷 LI4:
    - 位置: 手背虎口处
    - 功效: 镇静止痛、通经活络
    - 保健: 按摩3-5分钟
```

---

## 文档更新记录

| 版本 | 日期 | 更新内容 | 更新人 |
|-----|-----|---------|--------|
| v1.0 | 2026-01-18 | 第一期开发计划初版 | Claude |
