# 页面设计文档

## 文档概述

本文档包含中医体质识别应用所有页面的详细设计规范。

**项目**: 中医体质识别
**版本**: 1.0.0
**更新日期**: 2024-01-15

---

## 目录

1. [设计系统总览](#设计系统总览)
2. [首页设计](#首页设计)
3. [测试页面设计](#测试页面设计)
4. [结果页面设计](#结果页面设计)
5. [详情页面设计](#详情页面设计)
6. [饮食推荐页面设计](#饮食推荐页面设计)

---

## 设计系统总览

### 设计原则

| 原则 | 说明 |
|------|------|
| **科学性** | 基于王琦院士 CCMQ 标准量表 |
| **易用性** | 清晰的信息层次，简洁的操作流程 |
| **一致性** | 统一的色彩、组件、交互模式 |
| **可访问性** | 符合 WCAG AA 标准 |

### 色彩系统

#### 体质颜色系统

| 体质类型 | 英文标识 | 颜色值 | 图标 |
|----------|----------|--------|------|
| 平和质 | peace | #52c41a | ☯ |
| 气虚质 | qi_deficiency | #faad14 | 气 |
| 阳虚质 | yang_deficiency | #1890ff | 阳 |
| 阴虚质 | yin_deficiency | #eb2f96 | 阴 |
| 痰湿质 | phlegm_damp | #722ed1 | 痰 |
| 湿热质 | damp_heat | #fa541c | 湿 |
| 血瘀质 | blood_stasis | #f5222d | 瘀 |
| 气郁质 | qi_depression | #13c2c2 | 郁 |
| 特禀质 | special | #52c41a | 特 |

#### 功能色彩

```scss
// 主色调
$primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
$primary-solid: #667eea;

// 状态色
$color-success: #52c41a;   // 成功、宜吃
$color-warning: #faad14;   // 警告
$color-danger: #f5222d;    // 危险、禁忌
$color-info: #1890ff;      // 信息

// 中性色
$bg-page: #f5f5f5;
$bg-card: #ffffff;
$text-primary: #1a1a1a;
$text-secondary: #666666;
$text-tertiary: #999999;
```

### 排版系统

```scss
// 字体大小
$font-size-xl: 56rpx;   // 大标题
$font-size-lg: 48rpx;   // 标题
$font-size-md: 40rpx;   // 副标题
$font-size-base: 32rpx; // 正文标题
$font-size-sm: 28rpx;   // 正文
$font-size-xs: 26rpx;   // 小字
$font-size-xxs: 24rpx;  // 辅助文字
```

### 间距系统

```scss
$spacing-xs: 8rpx;
$spacing-sm: 12rpx;
$spacing-md: 20rpx;
$spacing-lg: 30rpx;
$spacing-xl: 40rpx;
```

### 圆角系统

```scss
$radius-sm: 12rpx;
$radius-md: 16rpx;
$radius-lg: 24rpx;
$radius-xl: 40rpx;
```

### 组件规范

#### 卡片
```scss
.card {
  background: #fff;
  border-radius: 24rpx;
  padding: 30rpx;
  margin: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
}
```

#### 按钮
```scss
// 主按钮
.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

// 轮廓按钮
.btn-outline {
  background: transparent;
  color: #667eea;
  border: 2rpx solid #667eea;
}
```

---

## 首页设计

### 页面概述

| 项目 | 说明 |
|------|------|
| 页面路径 | `/pages/index/index` |
| 主要功能 | 展示产品介绍、九种体质类型、功能特点、科学依据 |
| 数据来源 | `@/data/constitution.js` |

### 页面结构

```
首页 (index)
├── Hero 区域
│   ├── 背景：紫色渐变
│   ├── 图标：🩺 (120rpx)
│   ├── 标题：中医体质识别
│   ├── 副标题：基于王琦院士 CCMQ 标准量表
│   ├── 标签组
│   │   ├── 30道科学问题
│   │   ├── 9种体质类型
│   │   └── AI 智能分析
│   └── CTA 按钮：开始体质测试
│
├── 测试说明卡片
│   └── 说明列表（3条）
│
├── 九种体质类型卡片
│   └── 体质网格 (3x3)
│       └── 体质卡片 x 9
│           ├── 头部（彩色背景）
│           ├── 描述
│           ├── 特征标签（2个）
│           └── 查看详情 →
│
├── 功能特点卡片
│   └── 特点列表（6项）
│
├── 科学依据卡片
│   └── 科学说明列表（3项）
│
└── 底部行动按钮
```

### 核心代码

#### 数据映射
```javascript
import { CONSTITUTION_INFO } from '@/data/constitution.js'

const constitutionTypes = ref(Object.values(CONSTITUTION_INFO).map(info => ({
  type: info.type,
  name: info.name,
  icon: info.icon,
  color: info.color,
  shortDesc: info.description,
  features: info.characteristics.overall.slice(0, 2)
})))
```

#### 用户交互
```javascript
// 开始测试
function startTest() {
  uni.navigateTo({ url: '/pages/test/test' })
}

// 查看体质详情
function viewConstitution(item) {
  uni.navigateTo({
    url: `/pages/detail/detail?constitution=${item.type}`
  })
}
```

### 样式规格

```scss
// Hero 区域
.hero-section {
  padding: 60rpx 30rpx 40rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

// 体质网格
.constitution-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20rpx;
}

.constitution-card {
  border-radius: 16rpx;
  border: 2rpx solid #f0f0f0;
}

.constitution-header {
  padding: 20rpx;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

---

## 测试页面设计

### 页面概述

| 项目 | 说明 |
|------|------|
| 页面路径 | `/pages/test/test` |
| 主要功能 | 引导用户完成30道体质问题测试 |
| 数据来源 | API: `getQuestions()`, 本地: `@/data/constitution.js` |

### 页面结构

```
测试页面 (test)
├── 进度条（顶部固定）
│   ├── 进度填充条
│   └── 进度文本：X / 30
│
├── 问题卡片
│   ├── 体质类型标签（彩色徽章）
│   ├── 问题编号：问题 X
│   ├── 问题内容
│   ├── 选项列表（5个单选项）
│   └── 导航按钮
│       ├── 上一题
│       ├── 下一题
│       └── 提交测试
│
└── 快速跳转面板
    └── 按体质类型分组（9组）
        ├── 组标签：[图标] 名称 (范围)
        └── 题目按钮网格
```

### 题目分组

| 体质类型 | 题目范围 | 数量 |
|----------|----------|------|
| 平和质 | 1-4 | 4题 |
| 气虚质 | 5-8 | 4题 |
| 阳虚质 | 9-12 | 4题 |
| 阴虚质 | 13-16 | 4题 |
| 痰湿质 | 17-19 | 3题 |
| 湿热质 | 20-22 | 3题 |
| 血瘀质 | 23-25 | 3题 |
| 气郁质 | 26-28 | 3题 |
| 特禀质 | 29-30 | 2题 |

### 核心代码

#### 体质标签计算
```javascript
const currentConstitutionType = computed(() => {
  const questionNum = currentQuestionIndex.value + 1
  for (const [type, info] of Object.entries(QUESTION_GROUPS)) {
    if (questionNum >= info.start && questionNum <= info.end) {
      return {
        type,
        name: info.name,
        color: CONSTITUTION_INFO[type]?.color || '#667eea'
      }
    }
  }
  return null
})
```

#### 提交答案
```javascript
async function submitTest() {
  if (!allAnswered.value) {
    uni.showToast({ title: '请完成所有题目', icon: 'none' })
    return
  }

  const res = await submitTestApi(answers.value)
  uni.setStorageSync('resultId', res.data.result_id)
  uni.redirectTo({
    url: `/pages/result/result?resultId=${res.data.result_id}`
  })
}
```

### API 接口

**获取题目**
```
GET /api/v1/questions
Response: { questions: [{ id, content, constitution_type }] }
```

**提交答案**
```
POST /api/v1/test/submit
Request: { answers: [1,2,3,4,5,...] }
Response: { result_id, primary_constitution, scores }
```

---

## 结果页面设计

### 页面概述

| 项目 | 说明 |
|------|------|
| 页面路径 | `/pages/result/result` |
| 主要功能 | 展示用户的体质测试结果和分析报告 |
| 数据来源 | API: `getResult()`, 本地: `@/data/constitution.js` |

### 页面结构

```
结果页面 (result)
├── 结果头部（动态颜色）
│   ├── 体质图标
│   ├── 标题：您的体质是
│   ├── 体质名称
│   └── 体质描述
│
├── 体质特征卡片
│   └── 特征列表（4条）
│
├── 体质分数卡片
│   └── 分数条列表（9种，按分数排序）
│       ├── 体质图标 + 名称
│       ├── 分数值
│       └── 进度条
│
├── 次要体质卡片（条件显示）
│
├── 调理建议卡片
│   ├── 饮食建议
│   └── 运动建议
│
└── 操作按钮
    ├── 查看详细分析
    ├── 饮食推荐
    └── 重新测试
```

### 核心代码

#### 体质信息获取
```javascript
const constitutionInfo = computed(() => {
  if (!result.value?.primary_constitution) return null
  return CONSTITUTION_INFO[result.value.primary_constitution]
})
```

#### 分数数据处理
```javascript
const displayScores = computed(() => {
  if (!result.value?.scores) return []

  const primaryType = result.value.primary_constitution

  return Object.entries(result.value.scores)
    .map(([key, value]) => ({
      type: key,
      name: CONSTITUTION_INFO[key]?.name || key,
      value: Math.round(value),
      isPrimary: key === primaryType
    }))
    .sort((a, b) => b.value - a.value)
})
```

### API 接口

**获取结果**
```
GET /api/v1/test/result/{result_id}
Response: {
  result_id,
  primary_constitution,
  primary_constitution_name,
  scores: { peace: 45, ... },
  secondary_constitutions: [{ type, name, score }],
  test_date
}
```

---

## 详情页面设计

### 页面概述

| 项目 | 说明 |
|------|------|
| 页面路径 | `/pages/detail/detail` |
| 主要功能 | 展示特定体质类型的完整信息和调理指南 |
| 数据来源 | 本地: `@/data/constitution.js` |

### 页面结构

```
详情页面 (detail)
├── 体质头部（动态颜色）
│   ├── 体质图标
│   ├── 体质名称
│   └── 体质描述
│
├── 体质特征卡片
│   ├── 总体特征
│   │   └── 特征列表
│   └── 心理特征（条件显示）
│       └── 特征列表
│
├── 调理原则卡片
│   ├── 饮食建议
│   │   └── 建议列表
│   ├── 运动建议
│   │   └── 建议列表
│   ├── 起居建议
│   │   └── 建议列表
│   └── 情志调节（条件显示）
│       └── 建议列表
│
├── 禁忌事项卡片
│   └── 禁忌网格（2列）
│
├── 科学依据卡片
│   ├── 王琦院士 CCMQ 标准
│   └── 大样本验证
│
├── 免责声明
│
└── 操作按钮
    ├── 查看饮食推荐
    └── 返回结果页
```

### 数据结构

```javascript
CONSTITUTION_INFO[type] = {
  type: string,              // 体质标识
  name: string,              // 体质名称
  icon: string,              // 体质图标
  color: string,             // 体质颜色（十六进制）
  description: string,       // 体质描述

  characteristics: {
    overall: string[],       // 总体特征（至少4条）
    mental?: string[]        // 心理特征（可选）
  },

  regulation: {
    diet: string[],          // 饮食建议
    exercise: string[],      // 运动建议
    lifestyle: string[],     // 起居建议
    emotion?: string[]       // 情志调节（可选）
  },

  taboos: string[]           // 禁忌事项
}
```

### 样式规格

```scss
// 特征项
.character-item {
  display: flex;
  align-items: flex-start;
  gap: 12rpx;
  font-size: 28rpx;
  color: #333;
  line-height: 1.6;
}

.bullet {
  color: #52c41a;
  font-weight: 600;
}

// 禁忌网格
.taboos-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16rpx;
}

.taboo-item {
  background: #fff1f0;
  border: 1rpx solid #ffccc7;
  padding: 16rpx;
  border-radius: 12rpx;
}
```

---

## 饮食推荐页面设计

### 页面概述

| 项目 | 说明 |
|------|------|
| 页面路径 | `/pages/food/food` |
| 主要功能 | 根据体质类型提供个性化饮食建议 |
| 数据来源 | API: `getFoodRecommendations()` |

### 页面结构

```
饮食推荐页面 (food)
├── 饮食头部
│   ├── 标题：{体质名称}饮食推荐
│   └── 副标题：科学搭配，健康调理
│
├── 宜吃食物卡片
│   └── 食物列表
│       └── 食物项
│           ├── 食物名称
│           ├── 标签（性味）
│           └── 功效标签
│
├── 不宜食物卡片（条件显示）
│   └── 食物列表
│       └── 食物项
│           ├── 食物名称
│           └── 不宜原因
│
├── 推荐食谱卡片（条件显示）
│
├── 饮食原则卡片
│   └── 原则列表（4条）
│
└── 免责声明
```

### 食物标签系统

#### 性质标签 (nature)

| 性质 | 背景色 | 文字色 |
|------|--------|--------|
| 温 | #e6f7ff | #1890ff |
| 热 | #fff1f0 | #f5222d |
| 平 | #f5f5f5 | #666666 |
| 凉 | #e6f7ff | #1890ff |
| 寒 | #fff1f0 | #f5222d |

#### 味道标签 (flavor)

| 味道 | 背景色 | 文字色 |
|------|--------|--------|
| 酸 | #fff0f6 | #eb2f96 |
| 苦 | #fff7e6 | #faad14 |
| 甘 | #f6ffed | #52c41a |
| 辛 | #fff2e8 | #fa541c |
| 咸 | #f0f9ff | #13c2c2 |

### API 接口

**获取饮食推荐**
```
GET /api/v1/food/recommendations?constitution={type}
Response: {
  constitution,
  constitution_name,
  recommended_foods: [{ name, nature, flavor, effects }],
  avoid_foods: [{ name, reason }],
  recipes: [{ name, description }]
}
```

### 样式规格

```scss
// 宜吃食物
.food-item.recommended {
  background: #f6ffed;
  border-color: #d9f7be;
}

.effect-item {
  font-size: 24rpx;
  color: #52c41a;
  background: #f6ffed;
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
}

// 不宜食物
.food-item.avoid {
  background: #fff2e8;
  border-color: #ffbb96;
}
```

---

## 页面导航流程

```
首页 (index)
    │
    ├──→ 体质卡片点击 → 详情页 (detail)
    │
    └──→ 开始测试 → 测试页 (test)
                         │
                         └──→ 提交答案 → 结果页 (result)
                                             │
                                             ├──→ 查看详情 → 详情页 (detail)
                                             │
                                             └──→ 饮食推荐 → 饮食页 (food)
```

## 可访问性标准

- **文字对比度**: 至少 4.5:1 (WCAG AA)
- **点击区域**: 最小 44x44 pt (约 88x88 rpx)
- **焦点状态**: 清晰的视觉反馈

## 响应式适配

| 屏幕宽度 | 体质网格 | 其他调整 |
|----------|----------|----------|
| < 600rpx | 2列 | 减小间距 |
| >= 600rpx | 3列 | 标准布局 |
| >= 900rpx | 4列 | 增大内容宽度 |

---

**文档版本**: 1.0.0
**最后更新**: 2024-01-15
**维护者**: 中医体质识别项目组
