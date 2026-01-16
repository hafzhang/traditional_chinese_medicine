# 结果页面设计文档

## 页面概述

| 项目 | 说明 |
|------|------|
| 页面路径 | `/pages/result/result` |
| 页面名称 | 测试结果 - 体质分析 |
| 主要功能 | 展示用户的体质测试结果和分析报告 |
| 数据来源 | API: `getResult()`, 本地: `@/data/constitution.js` |

---

## 页面结构

```
结果页面 (result)
├── 加载状态
│   └── 加载动画
│
└── 结果内容
    ├── 结果头部（动态颜色）
    │   ├── 体质图标（100rpx）
    │   ├── 标题：您的体质是
    │   ├── 体质名称（56rpx）
    │   └── 体质描述
    │
    ├── 体质特征卡片
    │   ├── 标题：📋 主要特征
    │   └── 特征列表（4条）
    │       ├── ✓ 图标
    │       └── 特征文本
    │
    ├── 体质分数卡片
    │   ├── 标题：📊 体质分数分析
    │   └── 分数条列表（9种，按分数排序）
    │       ├── 体质图标 + 名称
    │       ├── 分数值
    │       └── 进度条
    │
    ├── 次要体质卡片（条件显示）
    │   ├── 标题：🔄 次要体质
    │   └── 次要体质列表
    │       ├── 图标 + 名称
    │       └── 分数
    │
    ├── 调理建议卡片
    │   ├── 标题：💡 调理建议
    │   ├── 饮食建议
    │   │   ├── 图标：🍎
    │   │   └── 建议文本（第一条）
    │   └── 运动建议
    │       ├── 图标：🏃
    │       └── 建议文本（第一条）
    │
    └── 操作按钮
        ├── 📋 查看详细分析（主按钮）
        ├── 🥗 饮食推荐（轮廓按钮）
        └── 重新测试（文字按钮）
```

---

## 组件设计

### 1. 结果头部 (`.result-header`)

动态颜色系统，头部背景色根据主要体质类型动态设置。

**样式规格**
```scss
.result-header {
  text-align: center;
  padding: 60rpx 30rpx;
  border-radius: 0 0 40rpx 40rpx;
  color: #fff;
  /* background: 通过 :style 动态设置体质颜色 */
}

.result-icon {
  font-size: 100rpx;
  margin-bottom: 20rpx;
}

.result-title {
  font-size: 28rpx;
  opacity: 0.9;
  margin-bottom: 16rpx;
}

.constitution-name {
  font-size: 56rpx;
  font-weight: 700;
  margin-bottom: 12rpx;
}

.result-desc {
  font-size: 26rpx;
  opacity: 0.9;
  line-height: 1.5;
}
```

**数据绑定**
```vue
<view class="result-header" :style="{ background: constitutionInfo?.color || '#667eea' }">
```

### 2. 特征预览 (`.features-preview`)

显示主要体质的前4条特征。

**样式规格**
```scss
.features-preview {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 12rpx;
  font-size: 28rpx;
  color: #333;
  line-height: 1.5;
}

.feature-bullet {
  color: #52c41a;
  font-weight: 600;
  flex-shrink: 0;
}
```

**数据来源**
```javascript
constitutionInfo?.characteristics.overall?.slice(0, 4)
```

### 3. 分数图表 (`.score-chart`)

展示所有九种体质的分数，主要体质高亮显示。

**样式规格**
```scss
.score-chart {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.score-item {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.score-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.score-header {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.score-icon {
  font-size: 24rpx;
}

.score-name {
  font-size: 28rpx;
  color: #333;
  font-weight: 500;
}

.score-value {
  font-size: 26rpx;
  color: #666;
}

.score-value.primary {
  color: #667eea;
  font-weight: 600;
}

.score-bar {
  height: 16rpx;
  background: #f5f5f5;
  border-radius: 8rpx;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  border-radius: 8rpx;
  transition: width 0.5s;
}

.score-fill.primary {
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
}
```

**数据结构**
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
    .sort((a, b) => b.value - a.value)  // 按分数降序排列
})
```

### 4. 次要体质 (`.secondary-list`)

条件显示：当存在次要体质时显示。

**显示条件**
```vue
<view v-if="result.secondary_constitutions?.length" class="card">
```

**样式规格**
```scss
.secondary-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.secondary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24rpx;
  background: #f8f9ff;
  border-radius: 12rpx;
}

.secondary-header {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.secondary-icon {
  font-size: 32rpx;
}

.secondary-name {
  font-size: 28rpx;
  color: #333;
  font-weight: 500;
}

.secondary-score {
  font-size: 26rpx;
  color: #667eea;
  font-weight: 600;
}
```

### 5. 调理建议预览 (`.regulation-preview`)

显示饮食和运动建议的预览。

**样式规格**
```scss
.regulation-preview {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.regulation-item {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.regulation-label {
  display: flex;
  align-items: center;
  gap: 8rpx;
  font-size: 26rpx;
  font-weight: 600;
  color: #333;
}

.label-icon {
  font-size: 28rpx;
}

.regulation-text {
  font-size: 26rpx;
  color: #666;
  line-height: 1.5;
  padding-left: 36rpx;
}
```

**数据来源**
```javascript
constitutionInfo?.regulation.diet?.[0]      // 第一条饮食建议
constitutionInfo?.regulation.exercise?.[0]  // 第一条运动建议
```

---

## 数据流

### 状态管理

```javascript
// 页面参数
const resultId = ref('')     // 从 URL 参数获取
const result = ref(null)     // API 返回的完整结果

// 计算属性
const constitutionInfo = computed(() => {
  if (!result.value?.primary_constitution) return null
  return CONSTITUTION_INFO[result.value.primary_constitution]
})

const displayScores = computed(() => {
  // 处理并格式化分数数据
})
```

### 页面参数获取

```javascript
onLoad((options) => {
  if (options.resultId) {
    resultId.value = options.resultId
    loadResult()
  } else {
    // 尝试从缓存获取
    const cached = uni.getStorageSync('resultId')
    if (cached) {
      resultId.value = cached
      loadResult()
    } else {
      uni.showToast({ title: '参数错误', icon: 'none' })
      setTimeout(() => uni.navigateBack(), 1500)
    }
  }
})
```

---

## API 调用

**端点**: `GET /api/v1/test/result/{result_id}`

**响应格式**:
```json
{
  "code": 200,
  "data": {
    "result_id": "uuid-string",
    "primary_constitution": "yang_deficiency",
    "primary_constitution_name": "阳虚质",
    "scores": {
      "peace": 45,
      "qi_deficiency": 60,
      "yang_deficiency": 85,
      "yin_deficiency": 35,
      "phlegm_damp": 50,
      "damp_heat": 40,
      "blood_stasis": 30,
      "qi_depression": 45,
      "special": 25
    },
    "secondary_constitutions": [
      { "type": "qi_deficiency", "name": "气虚质", "score": 60 }
    ],
    "test_date": "2024-01-15T10:30:00Z"
  }
}
```

**调用代码**:
```javascript
async function loadResult() {
  loading.value = true
  try {
    const res = await getResult(resultId.value)
    result.value = res.data
  } catch (error) {
    uni.showToast({ title: '加载失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}
```

---

## 用户交互

| 交互元素 | 触发事件 | 目标页面/行为 |
|----------|----------|---------------|
| 查看详细分析 | `@click="viewDetail"` | `/pages/detail/detail?resultId={id}` |
| 饮食推荐 | `@click="viewFood"` | `/pages/food/food?constitution={type}` |
| 重新测试 | `@click="retest"` | 确认对话框 → `/pages/test/test` |

**交互代码**:
```javascript
// 查看详情
function viewDetail() {
  uni.navigateTo({
    url: `/pages/detail/detail?resultId=${resultId.value}`
  })
}

// 查看饮食推荐
function viewFood() {
  uni.navigateTo({
    url: `/pages/food/food?constitution=${result.value.primary_constitution}`
  })
}

// 重新测试
function retest() {
  uni.showModal({
    title: '确认',
    content: '确定要重新测试吗？',
    success: (res) => {
      if (res.confirm) {
        uni.redirectTo({ url: '/pages/test/test' })
      }
    }
  })
}
```

---

## 样式变量

```scss
// 体质颜色（动态）
$header-bg: var(--constitution-color);

// 卡片样式
$card-bg: #ffffff;
$card-radius: 24rpx;
$card-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
$card-padding: 30rpx;
$card-margin: 30rpx;

// 文本颜色
$text-primary: #1a1a1a;
$text-secondary: #666666;
$text-tertiary: #999999;

// 状态颜色
$color-success: #52c41a;
$color-primary: #667eea;
$color-bg-light: #f8f9ff;
```

---

## 视觉层次

1. **结果头部**：最突出，动态颜色吸引注意力
2. **体质分数**：次重要，完整展示所有体质
3. **主要特征**：辅助理解体质特点
4. **调理建议**：预览引导查看详情
5. **次要体质**：条件显示，提供补充信息

---

## 可访问性

- 结果头部使用高对比度文字
- 分数条提供数值和视觉双重反馈
- 按钮具有清晰的视觉状态
- 支持屏幕阅读器

---

## 性能优化

- 使用计算属性缓存数据处理结果
- 分数数据一次处理，多次使用
- 动态样式使用 CSS 变量

---

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| resultId 参数缺失 | 尝试从缓存获取，失败则提示并返回 |
| API 加载失败 | 显示 Toast 提示 |
| 缓存获取失败 | 提示"参数错误"并返回上一页 |
