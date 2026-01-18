# 第一期开发计划文档 v2.0（基于现有体质辨识系统）

> **项目名称：** 中医养生平台（第一期）
> **版本：** v2.0
> **更新时间：** 2026-01-18
> **更新说明：** 基于已实现的体质辨识系统进行完善

---

## 一、已有系统概览

### 1.1 已实现功能

| 功能模块 | 状态 | 说明 |
|---------|-----|------|
| **体质测试** | ✅ 已完成 | 30题精简测试，基于CCMQ标准 |
| **体质判定算法** | ✅ 已完成 | 支持主要体质+次要体质判定 |
| **九种体质数据** | ✅ 已完成 | 体质特征、调理原则、禁忌等 |
| **测试结果展示** | ✅ 已完成 | 分数展示、体质分析、调理建议预览 |
| **后端API** | ✅ 已完成 | 提交测试、获取结果接口 |
| **前端页面** | ✅ 已完成 | 测试页、结果页、详情页 |

### 1.2 体质类型映射

| 代码 | 名称 | 图标 | 颜色 | 题目范围 |
|-----|-----|-----|-----|---------|
| `peace` | 平和质 | ☯ | #52c41a | 1-4 |
| `qi_deficiency` | 气虚质 | 气 | #faad14 | 5-8 |
| `yang_deficiency` | 阳虚质 | 阳 | #1890ff | 9-12 |
| `yin_deficiency` | 阴虚质 | 阴 | #eb2f96 | 13-16 |
| `phlegm_damp` | 痰湿质 | 痰 | #722ed1 | 17-19 |
| `damp_heat` | 湿热质 | 湿 | #fa541c | 20-22 |
| `blood_stasis` | 血瘀质 | 瘀 | #f5222d | 23-25 |
| `qi_depression` | 气郁质 | 郁 | #13c2c2 | 26-28 |
| `special` | 特禀质 | 特 | #52c41a | 29-30 |

### 1.3 现有API接口

```yaml
# 获取测试题目
GET /api/v1/questions
Response:
  code: 0
  data:
    total: 30
    questions: [...]

# 提交测试答案
POST /api/v1/test/submit
Body:
  answers: [1, 2, 3, ..., 30]  # 30个答案
Response:
  code: 0
  data:
    result_id: "xxx"
    primary_constitution: "qi_deficiency"
    primary_constitution_name: "气虚质"
    secondary_constitutions: [...]
    scores: {...}

# 获取测试结果
GET /api/v1/result/{result_id}
Response:
  code: 0
  data:
    result_id: "xxx"
    primary_constitution: "qi_deficiency"
    primary_constitution_name: "气虚质"
    characteristics: {...}
    regulation_principles: {...}
```

---

## 二、第一期新增产品

### 2.1 产品清单

| 序号 | 产品名称 | 优先级 | 工期 | 依赖 |
|-----|---------|-------|-----|-----|
| 1 | **食材库 + 食谱库** | P0 | 3周 | 体质数据 |
| 2 | **穴位查找** | P0 | 2周 | 症状数据 |
| 3 | **AI舌诊** | P0 | 2周 | 体质判定 |
| 4 | **免费养生课程** | P1 | 2周 | 体质数据 |

### 2.2 核心设计原则

**与现有系统的集成：**
1. **食材/食谱** → 按体质推荐（利用已有9种体质数据）
2. **穴位查找** → 按症状推荐（与体质调理建议关联）
3. **AI舌诊** → 作为体质测试的补充验证
4. **养生课程** → 按体质分类内容

**用户体验流程：**
```
体质测试 → 知道自己是什么体质
    ↓
食材库 → 查看适合自己体质的食材
食谱库 → 获取适合自己体质的食谱
穴位查找 → 找到调理穴位
AI舌诊 → 验证体质判断
养生课程 → 学习养生知识
```

---

## 三、食材库 + 食谱库

### 3.1 功能概述

基于用户已测定的体质类型，推荐适合的食材和食谱。

### 3.2 核心功能

#### 3.2.1 食材库

**功能列表：**
- 食材列表展示（分类浏览）
- 食材详情页
- **按体质筛选食材**（与现有体质系统集成）
- 按功效筛选食材
- 食材搜索
- 食材收藏

**食材详情包含：**
```yaml
基本信息:
  - 名称: "山药"
  - 别名: ["怀山药", "淮山"]
  - 类别: "蔬菜"

性味归经:
  - 性: "平"
  - 味: "甘"
  - 归经: ["脾", "肺", "肾"]

体质关联:  # 与现有体质系统关联
  - 适用体质: ["气虚质", "阴虚质", "平和质"]
  - 禁忌体质: ["痰湿质"]

功效:
  - "健脾养胃"
  - "补肺益肾"

食用指导:
  - 食用方法: ["蒸", "煮", "炖"]
  - 每日用量: "50-100g"
  - 注意事项: "生用健脾，炒用止泻"

搭配宜忌:
  - 宜配: ["莲子", "枸杞"]
  - 忌配: ["碱性食物"]

相关食谱:  # 链接到食谱库
  - ["山药莲子粥", "山药炖鸡汤"]
```

#### 3.2.2 食谱库

**功能列表：**
- 食谱列表展示
- 食谱详情页
- **按体质推荐食谱**（与现有体质系统集成）
- 按症状推荐食谱
- 按季节推荐食谱
- 食谱搜索
- 食谱收藏

**食谱详情包含：**
```yaml
基本信息:
  - 名称: "山药莲子粥"
  - 类型: "粥类"
  - 难度: "简单"
  - 用时: "30分钟"
  - 份量: "2人份"

体质关联:  # 与现有体质系统关联
  - 适用体质: ["气虚质", "阴虚质"]
  - 主治症状: ["食欲不振", "疲劳乏力"]

食材清单:
  主料:
    - {name: "山药", amount: "100g", 体质关联: "气虚质宜食"}
    - {name: "糯米", amount: "50g"}
  辅料:
    - {name: "莲子", amount: "20g"}
    - {name: "枸杞", amount: "10g"}

制作步骤:
  - "山药去皮切小块，糯米提前浸泡2小时"
  - "锅中加水，放入糯米大火煮开"
  - "加入山药、莲子转小火煮30分钟"
  - "最后加入枸杞、冰糖煮5分钟即可"

功效说明:
  - "健脾养胃、补肺益气"
  - "适合脾胃虚弱、食欲不振者"
```

### 3.3 与现有系统集成

#### 3.3.1 从体质结果页跳转

在现有结果页添加"推荐食材"和"推荐食谱"入口：

```javascript
// frontend/src/pages/result/result.vue
// 添加跳转按钮
<view class="action-buttons">
  <button @click="viewRecommendedIngredients">推荐食材</button>
  <button @click="viewRecommendedRecipes">推荐食谱</button>
</view>

viewRecommendedIngredients() {
  uni.navigateTo({
    url: `/pages/ingredients/list?constitution=${this.result.primary_constitution}`
  })
}

viewRecommendedRecipes() {
  uni.navigateTo({
    url: `/pages/recipes/list?constitution=${this.result.primary_constitution}`
  })
}
```

#### 3.3.2 按体质筛选API

```yaml
# 根据体质获取推荐食材
GET /api/v1/ingredients/recommend/{constitution}
Response:
  code: 0
  data:
    constitution: "qi_deficiency"
    constitution_name: "气虚质"
    recommended:  # 推荐食材
      - id: "xxx"
        name: "山药"
        reason: "健脾养胃"
    avoided:  # 禁忌食材
      - id: "yyy"
        name: "山楂"
        reason: "破气耗气"

# 根据体质获取推荐食谱
GET /api/v1/recipes/recommend/{constitution}
Response:
  code: 0
  data:
    constitution: "qi_deficiency"
    recipes:
      breakfast:
        - id: "xxx"
          name: "山药小米粥"
          reason: "健脾养胃，适合早餐"
      lunch:
        - id: "yyy"
          name: "黄芪炖鸡汤"
          reason: "补气养血"
      dinner:
        - id: "zzz"
          name: "莲子百合粥"
          reason: "养心安神"
```

### 3.4 数据库设计

#### 3.4.1 食材表 (ingredients)

```sql
CREATE TABLE ingredients (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    aliases JSON,  -- ["怀山药", "淮山"]
    category VARCHAR(50),  -- 谷物、蔬菜、水果、肉类、药材

    -- 性味归经
    nature VARCHAR(20),  -- 寒、凉、平、温、热
    flavor VARCHAR(50),  -- 甘、酸、苦、辛、咸
    meridians JSON,  -- ["脾", "肺", "肾"]

    -- 体质关联（与现有系统对接）
    suitable_constitutions JSON,  -- ["qi_deficiency", "yin_deficiency"]
    avoid_constitutions JSON,  -- ["phlegm_damp"]

    -- 功效
    efficacy TEXT,  -- "健脾养胃、补肺益肾"
    nutrition TEXT,  -- 营养成分说明

    -- 食用指导
    cooking_methods JSON,  -- ["蒸", "煮", "炖"]
    daily_dosage VARCHAR(50),  -- "50-100g"
    best_time VARCHAR(50),  -- "早晚餐"
    precautions TEXT,  -- 注意事项

    -- 搭配
    compatible_with JSON,  -- ["莲子", "枸杞"]
    incompatible_with JSON,  -- ["碱性食物"]

    -- 展示
    image_url VARCHAR(255),
    description TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_ingredients_suitable ON ingredients((CAST(suitable_constitutions AS CHAR(255))));
CREATE INDEX idx_ingredients_avoid ON ingredients((CAST(avoid_constitutions AS CHAR(255))));
```

#### 3.4.2 食谱表 (recipes)

```sql
CREATE TABLE recipes (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50),  -- 粥类、汤类、茶饮、菜肴
    difficulty VARCHAR(20),  -- 简单、中等、困难
    cook_time INT,  -- 分钟
    servings INT,

    -- 体质关联（与现有系统对接）
    suitable_constitutions JSON,  -- ["qi_deficiency"]
    symptoms JSON,  -- ["食欲不振", "疲劳乏力"]
    suitable_seasons JSON,  -- ["春", "秋", "冬"]

    -- 食材
    ingredients JSON,  -- {main: [...], auxiliary: [...], seasoning: [...]}
    steps JSON,  -- ["步骤1", "步骤2"]

    -- 功效
    efficacy TEXT,
    health_benefits TEXT,
    precautions TEXT,

    -- 标签
    tags JSON,  -- ["健脾养胃", "补气"]

    -- 展示
    image_url VARCHAR(255),
    description TEXT,

    -- 统计
    view_count INT DEFAULT 0,
    favorite_count INT DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_recipes_suitable ON recipes((CAST(suitable_constitutions AS CHAR(255))));
```

### 3.5 前端页面

#### 3.5.1 新增页面

```
frontend/src/pages/
├── ingredients/
│   ├── list.vue        # 食材列表页（支持按体质筛选）
│   └── detail.vue      # 食材详情页
└── recipes/
    ├── list.vue        # 食谱列表页（支持按体质筛选）
    └── detail.vue      # 食谱详情页
```

#### 3.5.2 修改现有页面

```vue
<!-- frontend/src/pages/result/result.vue -->
<!-- 添加推荐食材和食谱的快捷入口 -->

<template>
  <view class="page-container">
    <!-- 现有结果展示 -->

    <!-- 新增：推荐内容区 -->
    <view class="recommendation-section">
      <view class="section-title">
        <text>为您推荐</text>
      </view>

      <!-- 推荐食材 -->
      <view class="recommend-card" @click="goToIngredients">
        <view class="card-icon">🥗</view>
        <view class="card-content">
          <view class="card-title">适合您的食材</view>
          <view class="card-desc">
            {{ constitutionInfo?.regulation?.diet?.[0] || '' }}
          </view>
        </view>
        <view class="card-arrow">→</view>
      </view>

      <!-- 推荐食谱 -->
      <view class="recommend-card" @click="goToRecipes">
        <view class="card-icon">🍲</view>
        <view class="card-content">
          <view class="card-title">推荐食谱</view>
          <view class="card-desc">根据您的体质定制</view>
        </view>
        <view class="card-arrow">→</view>
      </view>
    </view>
  </view>
</template>

<script setup>
// ... 现有代码

const goToIngredients = () => {
  uni.navigateTo({
    url: `/pages/ingredients/list?constitution=${result.value.primary_constitution}`
  })
}

const goToRecipes = () => {
  uni.navigateTo({
    url: `/pages/recipes/list?constitution=${result.value.primary_constitution}`
  })
}
</script>
```

---

## 四、穴位查找

### 4.1 功能概述

提供人体穴位查询功能，支持按症状查找穴位，展示穴位位置、功效、按摩方法。

**与体质系统关联：**
- 在体质调理建议中推荐对应穴位
- 点击穴位名称跳转到穴位详情

### 4.2 核心功能

#### 4.2.1 穴位列表

- 按部位分类（头面部、颈部、胸腹部、背部、上肢、下肢）
- 按经络分类
- 搜索功能

#### 4.2.2 穴位详情

```yaml
基本信息:
  - 名称: "足三里"
  - 代号: "ST36"
  - 所属经络: "足阳明胃经"

位置:
  - 部位: "小腿前外侧"
  - 定位: "犊鼻下3寸，胫骨前缘外一横指"
  - 简易取穴: "膝盖骨外侧下方凹陷往下四横指"

功效:
  - 主要功效: ["健脾和胃", "扶正培元", "调理气血"]
  - 主治病症: ["胃痛", "消化不良", "失眠", "疲劳"]

按摩方法:
  - 手法: "用拇指指腹按压"
  - 时间: "3-5分钟"
  - 频率: "每日1-2次"

体质关联:  # 新增
  - 适用体质: ["气虚质", "阳虚质", "痰湿质"]
  - 相关调理: "健脾和胃，增强体质"
```

#### 4.2.3 按症状查找

用户输入症状，系统推荐相关穴位。

### 4.3 与现有系统集成

#### 4.3.1 在体质详情页添加穴位推荐

```vue
<!-- frontend/src/pages/detail/detail.vue -->
<template>
  <view class="page-container">
    <!-- 现有调理建议 -->

    <!-- 新增：推荐穴位 -->
    <view class="section">
      <view class="section-title">
        <text class="title-icon">📍</text>
        <text>推荐穴位</text>
      </view>

      <view class="acupoint-list">
        <view
          v-for="point in recommendedAcupoints"
          :key="point.id"
          class="acupoint-item"
          @click="goToAcupoint(point.id)"
        >
          <view class="acupoint-name">{{ point.name }}</view>
          <view class="acupoint-benefit">{{ point.benefit }}</view>
          <view class="acupoint-arrow">→</view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getAcupointsByConstitution } from '@/api/acupoint.js'

const constitution = ref('')
const recommendedAcupoints = ref([])

onLoad((options) => {
  constitution.value = options.constitution
  loadRecommendedAcupoints()
})

const loadRecommendedAcupoints = async () => {
  const res = await getAcupointsByConstitution(constitution.value)
  recommendedAcupoints.value = res.data
}

const goToAcupoint = (id) => {
  uni.navigateTo({
    url: `/pages/acupoints/detail?id=${id}`
  })
}
</script>
```

### 4.4 数据库设计

```sql
CREATE TABLE acupoints (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    code VARCHAR(20),  -- ST36
    meridian VARCHAR(50),  -- 足阳明胃经

    -- 位置
    body_part VARCHAR(50),  -- 下肢
    location TEXT,
    simple_location TEXT,

    -- 功效
    efficacy JSON,  -- ["健脾和胃", "扶正培元"]
    indications JSON,  -- ["胃痛", "消化不良"]

    -- 按摩
    massage_method TEXT,
    massage_duration VARCHAR(50),
    massage_frequency VARCHAR(50),
    precautions TEXT,

    -- 体质关联（新增）
    suitable_constitutions JSON,  -- ["qi_deficiency"]
    constitution_benefit TEXT,  -- "健脾和胃，增强体质"

    -- 展示
    image_url VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE symptom_acupoints (
    id VARCHAR(36) PRIMARY KEY,
    symptom_name VARCHAR(100) NOT NULL,
    acupoint_id VARCHAR(36) NOT NULL,
    priority INT DEFAULT 0
);
```

---

## 五、AI舌诊

### 5.1 功能概述

用户拍摄舌象照片，通过AI分析舌质、舌苔、舌形，给出体质倾向和健康建议。

**与现有系统关联：**
- 作为体质测试的补充验证
- 分析结果与体质类型对应
- 可与30题测试结果对比

### 5.2 核心功能

#### 5.2.1 拍照上传

- 调用相机拍照
- 从相册选择
- 拍照引导（光线、角度、位置）

#### 5.2.2 AI分析

```yaml
舌质分析:
  - 颜色: 淡白/淡红/红/绛/紫
  - 形态: 胖大/瘦薄/齿痕/裂纹

舌苔分析:
  - 苔色: 白苔/黄苔/灰黑苔
  - 苔质: 厚苔/薄苔/腻苔

综合判断:
  - 体质倾向: 对应现有9种体质
  - 健康状态: 描述性说明
  - 调理建议: 关联体质调理方案
```

#### 5.2.3 分析报告

```
┌─────────────────────────────────────────┐
│  AI舌诊报告                             │
├─────────────────────────────────────────┤
│  【舌象分析】                           │
│  舌质：淡白，有齿痕                     │
│  舌苔：薄白苔                           │
│  舌形：胖大有齿痕                       │
├─────────────────────────────────────────┤
│  【体质判断】                           │
│  体质倾向：气虚质                       │
│  与30题测试结果：一致 ✓                 │
├─────────────────────────────────────────┤
│  【调理建议】                           │
│  1. 饮食：多食山药、莲子、大枣         │
│  2. 起居：避免过度劳累                 │
│  3. 运动：散步、太极                   │
│  4. 情志：保持心情舒畅                 │
├─────────────────────────────────────────┤
│  【推荐】                               │
│  → 查看气虚质详情                       │
│  → 推荐食材                             │
│  → 推荐食谱                             │
│  → 推荐穴位                             │
└─────────────────────────────────────────┘
```

### 5.3 与现有系统集成

#### 5.3.1 舌诊结果与体质结果对比

```yaml
场景1: 用户已完成30题测试
  - 显示舌诊结果
  - 显示与30题测试结果对比
  - 一致性提示

场景2: 用户未完成测试
  - 显示舌诊结果
  - 提示"完成30题测试获取更准确判断"
  - 引导到体质测试页

场景3: 从舌诊跳转到其他功能
  - 查看体质详情
  - 推荐食材
  - 推荐食谱
  - 推荐穴位
```

#### 5.3.2 API设计

```yaml
# 上传舌象照片进行分析
POST /api/v1/tongue-diagnosis/analyze
Body:
  image: base64图片
  user_result_id: 可选，如果有30题测试结果ID
Response:
  code: 0
  data:
    id: "xxx"
    image_url: "https://..."
    analysis:
      tongue_color: "淡白"
      tongue_shape: "胖大有齿痕"
      coating_color: "白"
      coating_thickness: "薄"
    conclusion:
      constitution_tendency: "qi_deficiency"
      constitution_name: "气虚质"
      confidence: 0.85
      comparison:  # 与30题测试对比（如果有）
        test_result_constitution: "qi_deficiency"
        is_consistent: true
    advice:
      diet: "多食山药、莲子、大枣"
      lifestyle: "..."
    recommendations:
      acupoints: [...]
      recipes: [...]
```

### 5.4 技术实现

#### 5.4.1 简化方案（第一期）

使用规则引擎而非AI模型：

```python
# backend/api/services/tongue_diagnosis.py

class TongueDiagnosisService:
    # 舌象-体质映射规则（简化版）
    TONGUE_CONSTITUTION_RULES = {
        'qi_deficiency': {
            'tongue_color': ['淡白', '淡红'],
            'tongue_shape': ['胖大', '齿痕'],
            'coating_color': ['白'],
            'coating_thickness': ['薄'],
        },
        'yin_deficiency': {
            'tongue_color': ['红', '绛'],
            'tongue_shape': ['瘦薄'],
            'coating_color': ['黄', '少'],
            'coating_thickness': ['薄', '剥落'],
        },
        # ... 其他体质
    }

    def analyze(self, image_data, user_result_id=None):
        # 第一版：手动标记或简单图像处理
        # 后期：接入AI API

        # 简化实现：返回预设结果用于演示
        result = self.get_diagnosis_result(image_data)

        # 如果有用户测试结果，进行对比
        if user_result_id:
            user_result = self.get_user_result(user_result_id)
            result['comparison'] = {
                'test_result_constitution': user_result['primary_constitution'],
                'is_consistent': result['constitution_tendency'] == user_result['primary_constitution']
            }

        return result
```

#### 5.4.2 后期AI方案

```python
# 接入腾讯云/百度AI图像识别
from tencentcloud.ai import TencentCloudAI

class TongueDiagnosisAI:
    def __init__(self):
        self.client = TencentCloudAI(api_key=...)

    def analyze(self, image_url):
        # 调用AI API分析舌象
        result = self.client.detect_tongue(image_url)

        # 提取特征
        features = self.extract_features(result)

        # 匹配体质
        constitution = self.match_constitution(features)

        return constitution
```

---

## 六、免费养生课程

### 6.1 功能概述

提供免费的中医养生知识内容，包括短视频、图文文章。

**与体质系统关联：**
- 按体质分类内容
- 在体质详情页推荐相关课程

### 6.2 核心功能

#### 6.2.1 内容分类

```yaml
按体质分类:  # 新增
  - 气虚质养生
  - 阴虚质养生
  - 阳虚质养生
  - ...（9种体质）

按主题分类:
  - 四季养生
  - 食疗养生
  - 经络养生
  - 情志养生

按形式分类:
  - 短视频 (1-3分钟)
  - 图文文章
```

#### 6.2.2 与体质系统集成

在体质详情页添加"相关课程"推荐：

```vue
<!-- frontend/src/pages/detail/detail.vue -->
<template>
  <view class="page-container">
    <!-- 现有内容 -->

    <!-- 新增：相关课程 -->
    <view class="section">
      <view class="section-title">
        <text class="title-icon">📺</text>
        <text>养生课程</text>
      </view>

      <view class="course-list">
        <view
          v-for="course in relatedCourses"
          :key="course.id"
          class="course-item"
          @click="goToCourse(course.id)"
        >
          <image :src="course.cover" class="course-cover" />
          <view class="course-info">
            <view class="course-title">{{ course.title }}</view>
            <view class="course-meta">{{ course.duration }} | {{ course.views }}次观看</view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>
```

### 6.3 数据库设计

```sql
CREATE TABLE courses (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,

    -- 分类
    category VARCHAR(50),  -- constitution, season, diet, meridian
    subcategory VARCHAR(50),

    -- 内容类型
    content_type VARCHAR(20),  -- video, article
    content_url VARCHAR(255),

    -- 体质关联（新增）
    suitable_constitutions JSON,  -- ["qi_deficiency"]

    -- 标签
    tags JSON,

    -- 时长
    duration INT,  -- 秒

    -- 封面
    cover_image VARCHAR(255),

    -- 统计
    view_count INT DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_courses_constitution ON courses((CAST(suitable_constitutions AS CHAR(255))));
```

---

## 七、开发计划

### 7.1 开发周期

| 阶段 | 功能 | 工期 | 依赖 |
|-----|-----|-----|-----|
| **Week 1-2** | 食材库开发（数据录入+API+前端） | 2周 | 体质数据 |
| **Week 3-4** | 食谱库开发（数据录入+API+前端） | 2周 | 食材库 |
| **Week 5-6** | 穴位查找（数据录入+API+前端） | 2周 | - |
| **Week 7-8** | AI舌诊（规则版+API+前端） | 2周 | 体质系统 |
| **Week 9-10** | 养生课程（内容准备+API+前端） | 2周 | 体质数据 |
| **Week 11-12** | 系统集成+测试+优化 | 2周 | 全部功能 |
| **总计** | | **12周** | |

### 7.2 里程碑

| 里程碑 | 时间 | 交付物 |
|--------|-----|--------|
| M1 | Week 2 | 食材库上线，可按体质筛选 |
| M2 | Week 4 | 食谱库上线，可按体质推荐 |
| M3 | Week 6 | 穴位查找上线，支持症状搜索 |
| M4 | Week 8 | AI舌诊上线，规则版分析 |
| M5 | Week 10 | 养生课程上线，按体质分类 |
| M6 | Week 12 | 第一期完整版上线 |

---

## 八、数据准备清单

### 8.1 优先级P0数据（必须准备）

#### 食材数据（50种）

```yaml
气虚质适用 (15种):
  - 山药、莲子、大枣、小米、糯米、鸡肉、牛肉、
    鲫鱼、香菇、胡萝卜、南瓜、土豆、扁豆、豌豆、红豆

阴虚质适用 (10种):
  - 百合、银耳、梨、鸭肉、桑葚、枸杞、菠菜、
    西红柿、黄瓜、冬瓜

阳虚质适用 (10种):
  - 羊肉、韭菜、辣椒、生姜、花椒、桂圆、核桃、
    栗子、荔枝、樱桃

痰湿质适用 (8种):
  - 冬瓜、赤小豆、荷叶、白萝卜、薏米、玉米、
    山楂、陈皮

其他常用 (7种):
  - 红糖、蜂蜜、绿茶、菊花、玫瑰花、茯苓、甘草
```

#### 食谱数据（30个）

```yaml
气虚质食谱 (10个):
  粥类: 山药莲子粥、红枣小米粥、黄芪粥
  汤类: 黄芪炖鸡汤、党参排骨汤
  菜肴: 山药炒肉片、莲子炖猪肚

阴虚质食谱 (6个):
  粥类: 百合银耳粥、百合绿豆粥
  汤类: 百合梨汤、银耳莲子汤

阳虚质食谱 (6个):
  粥类: 羊肉粥、韭菜粥
  汤类: 当归生姜羊肉汤

其他体质食谱 (8个):
  痰湿质: 冬瓜排骨汤、荷叶粥
  湿热质: 绿豆汤、苦瓜炒蛋
```

#### 穴位数据（30个）

```yaml
保健要穴 (10个):
  - 足三里 (ST36) - 健脾和胃
  - 三阴交 (SP6) - 调理气血
  - 涌泉 (KI1) - 补肾固本
  - 合谷 (LI4) - 镇静止痛
  - 内关 (PC6) - 宁心安神
  - 神门 (HT7) - 宁心安神
  - 中脘 (CV12) - 健脾和胃
  - 关元 (CV4) - 培元固本
  - 气海 (CV6) - 益气固表
  - 命门 (GV4) - 温肾壮阳

按体质分类 (20个):
  气虚质: 足三里、三阴交、气海、中脘
  阴虚质: 三阴交、太溪、照海、复溜
  阳虚质: 关元、命门、气海、足三里
  痰湿质: 足三里、丰隆、阴陵泉、中脘
  湿热质: 曲池、合谷、足三里、阴陵泉
```

#### 症状-穴位映射（15个症状）

```yaml
消化系统:
  - 食欲不振: 足三里、中脘、内关
  - 胃痛: 足三里、中脘、内关
  - 便秘: 天枢、足三里、支沟

神经系统:
  - 失眠: 神门、内关、三阴交
  - 头痛: 太阳、合谷、太冲

呼吸系统:
  - 咳嗽: 肺俞、列缺、合谷

其他:
  - 疲劳: 足三里、三阴交、气海
  - 便秘: 天枢、足三支、支沟
```

#### 舌诊规则映射

```python
# 复用现有体质系统的数据结构
TONGUE_CONSTITUTION_MAPPING = {
    'qi_deficiency': {
        'tongue_color': ['淡白', '淡红'],
        'tongue_shape': ['胖大', '齿痕'],
        'coating_color': ['白'],
        'coating_thickness': ['薄'],
    },
    # ... 其他8种体质
}
```

#### 课程内容（15个视频/文章）

```yaml
体质养生系列 (9个):
  - 气虚质怎么调理？ (02:00)
  - 阴虚质怎么调理？ (02:00)
  - 阳虚质怎么调理？ (02:00)
  - ...（9种体质）

食疗养生系列 (6个):
  - 山药：健脾养胃高手 (02:00)
  - 红枣：补血安神佳品 (02:00)
  - 四季养生食材推荐 (03:00)
```

### 8.2 优先级P1数据（可后续补充）

- 更多食材（100+）
- 更多食谱（50+）
- 更多穴位（50+）
- 更多课程内容

---

## 九、技术实现要点

### 9.1 复用现有代码

#### 9.1.1 体质数据共享

```python
# backend/api/data/constitution_info.py
# 现有体质信息数据可被所有模块复用

# 食材推荐服务
class IngredientRecommendationService:
    def get_by_constitution(self, constitution_type):
        # 复用体质信息中的调理原则
        constitution_info = CONSTITUTION_INFO_DATA[constitution_type]
        diet_principles = constitution_info['regulation_principles']['diet']

        # 根据调理原则筛选食材
        ingredients = self.filter_ingredients(diet_principles)

        return ingredients
```

#### 9.1.2 前端数据共享

```javascript
// frontend/src/data/constitution.js
// 现有体质信息可被所有页面导入

// 食材列表页
import { CONSTITUTION_INFO } from '@/data/constitution.js'

const constitutionInfo = CONSTITUTION_INFO[constitution]
const dietAdvice = constitutionInfo.regulation.diet
```

### 9.2 API接口规范

#### 9.2.1 体质关联接口

所有需要关联体质的接口都使用统一的体质代码：

```yaml
体质代码规范:
  - peace: 平和质
  - qi_deficiency: 气虚质
  - yang_deficiency: 阳虚质
  - yin_deficiency: 阴虚质
  - phlegm_damp: 痰湿质
  - damp_heat: 湿热质
  - blood_stasis: 血瘀质
  - qi_depression: 气郁质
  - special: 特禀质

接口示例:
  GET /api/v1/ingredients/recommend/qi_deficiency
  GET /api/v1/recipes/recommend/yin_deficiency
  GET /api/v1/acupoints/by-constitution/phlegm_damp
  GET /api/v1/courses/by-constitution/qi_deficiency
```

### 9.3 前端路由规范

```
页面路由设计:
  /pages/ingredients/list?constitution=qi_deficiency
  /pages/ingredients/detail?id=xxx
  /pages/recipes/list?constitution=yin_deficiency
  /pages/recipes/detail?id=xxx
  /pages/acupoints/list?symptom=失眠
  /pages/acupoints/detail?id=xxx
  /pages/tongue-diagnosis/index
  /pages/courses/list?constitution=qi_deficiency
  /pages/courses/detail?id=xxx
```

---

## 十、验收标准

### 10.1 功能验收

| 功能 | 验收标准 |
|-----|---------|
| **食材库** | 可按体质筛选，与体质结果页联动 |
| **食谱库** | 可按体质推荐，显示相关食材 |
| **穴位查找** | 可按症状查找，与体质调理联动 |
| **AI舌诊** | 可拍照分析，与体质测试对比 |
| **养生课程** | 可按体质分类，与体质详情联动 |

### 10.2 集成验收

| 集成点 | 验收标准 |
|--------|---------|
| 体质结果→食材 | 一键跳转，自动筛选 |
| 体质结果→食谱 | 一键跳转，推荐食谱 |
| 体质结果→穴位 | 在详情页显示推荐穴位 |
| 体质结果→课程 | 在详情页显示相关课程 |
| 舌诊→体质测试 | 结果对比显示一致性 |

---

## 十一、与现有系统的兼容性

### 11.1 数据库兼容

```sql
-- 现有表结构保持不变
-- 新增表通过外键或字段关联

-- 新增食材表，添加体质关联字段
CREATE TABLE ingredients (
    ...
    suitable_constitutions JSON,  -- 对应现有9种体质
    ...
);

-- 新增食谱表，添加体质关联字段
CREATE TABLE recipes (
    ...
    suitable_constitutions JSON,  -- 对应现有9种体质
    ...
);
```

### 11.2 API兼容

```python
# 现有API保持不变
# 新增API遵循现有规范

# 现有
GET /api/v1/questions
POST /api/v1/test/submit
GET /api/v1/result/{result_id}

# 新增（遵循现有规范）
GET /api/v1/ingredients
GET /api/v1/recipes
GET /api/v1/acupoints
POST /api/v1/tongue-diagnosis/analyze
GET /api/v1/courses
```

### 11.3 前端兼容

```javascript
// 现有页面保持不变
// 新增页面可从现有页面跳转

// 现有页面
/pages/index/index
/pages/test/test
/pages/result/result
/pages/detail/detail

// 新增页面（可从现有页面跳转）
/pages/ingredients/list
/pages/recipes/list
/pages/acupoints/list
/pages/tongue-diagnosis/index
/pages/courses/list
```

---

## 十二、总结

### 12.1 第一期完整功能矩阵

| 模块 | 状态 | 体质关联 |
|-----|-----|---------|
| 体质测试 | ✅ 已有 | - |
| 体质结果展示 | ✅ 已有 | - |
| 体质详情页 | ✅ 已有 | - |
| 食材库 | 🆕 新增 | ✅ 按体质筛选 |
| 食谱库 | 🆕 新增 | ✅ 按体质推荐 |
| 穴位查找 | 🆕 新增 | ✅ 按体质推荐穴位 |
| AI舌诊 | 🆕 新增 | ✅ 结果与体质对比 |
| 养生课程 | 🆕 新增 | ✅ 按体质分类 |

### 12.2 用户体验流程

```
┌─────────────────────────────────────────────────────┐
│                    用户旅程                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. 体质测试 ──────────────────────────→ 知道体质   │
│                                                     │
│  2. 查看结果 ──────────────────────────→ 了解详情   │
│                                                     │
│  3. 查看食材 ──────────────────────────→ 饮食调理   │
│                                                     │
│  4. 查看食谱 ──────────────────────────→ 实践方案   │
│                                                     │
│  5. 穴位查找 ──────────────────────────→ 穴位按摩   │
│                                                     │
│  6. AI舌诊 ───────────────────────────→ 验证判断   │
│                                                     │
│  7. 养生课程 ──────────────────────────→ 学习知识   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 12.3 开发优势

1. **复用现有代码** - 体质数据、API、前端组件可直接复用
2. **数据关联简单** - 9种体质代码作为关联键
3. **用户体验连贯** - 所有功能围绕体质展开
4. **开发效率高** - 12周完成全部功能

---

## 文档更新记录

| 版本 | 日期 | 更新内容 | 更新人 |
|-----|-----|---------|--------|
| v1.0 | 2026-01-18 | 第一期开发计划初版 | Claude |
| v2.0 | 2026-01-18 | 基于已有体质辨识系统完善 | Claude |
