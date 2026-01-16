# 详情页面设计文档

## 页面概述

| 项目 | 说明 |
|------|------|
| 页面路径 | `/pages/detail/detail` |
| 页面名称 | 体质详情 - 完整分析 |
| 主要功能 | 展示特定体质类型的完整信息和调理指南 |
| 数据来源 | 本地: `@/data/constitution.js`, API: `getResult()` (可选) |

---

## 页面结构

```
详情页面 (detail)
├── 加载状态
│   └── 加载动画
│
└── 详情内容（可滚动 scroll-view）
    ├── 体质头部（动态颜色）
    │   ├── 体质图标（100rpx）
    │   ├── 体质名称（48rpx）
    │   └── 体质描述
    │
    ├── 体质特征卡片
    │   ├── 标题：📋 体质特征
    │   ├── 总体特征
    │   │   ├── 图标：👤
    │   │   ├── 标题：总体特征
    │   │   └── 特征列表（所有条目）
    │   │       ├── ✓ 图标
    │   │       └── 特征文本
    │   └── 心理特征（条件显示）
    │       ├── 图标：💭
    │       ├── 标题：心理特征
    │       └── 特征列表
    │
    ├── 调理原则卡片
    │   ├── 标题：🎯 调理原则
    │   ├── 饮食建议
    │   │   ├── 图标：🍎
    │   │   ├── 标题：饮食建议
    │   │   └── 建议列表（所有条目）
    │   ├── 运动建议
    │   │   ├── 图标：🏃
    │   │   ├── 标题：运动建议
    │   │   └── 建议列表
    │   ├── 起居建议
    │   │   ├── 图标：🌙
    │   │   ├── 标题：起居建议
    │   │   └── 建议列表
    │   └── 情志调节（条件显示）
    │       ├── 图标：😊
    │       ├── 标题：情志调节
    │       └── 建议列表
    │
    ├── 禁忌事项卡片（条件显示）
    │   ├── 标题：⚠️ 禁忌事项
    │   └── 禁忌网格（2列）
    │       ├── 🚫 图标
    │       └── 禁忌文本
    │
    ├── 科学依据卡片
    │   ├── 标题：📚 科学依据
    │   ├── 王琦院士 CCMQ 标准
    │   │   ├── 图标：🎓
    │   │   ├── 标题
    │   │   └── 说明
    │   └── 大样本验证
    │       ├── 图标：📊
    │       ├── 标题
    │       └── 说明
    │
    ├── 免责声明
    │   ├── 标题：⚠️ 重要提示
    │   └── 免责文本
    │
    └── 操作按钮
        ├── 🥗 查看饮食推荐（主按钮）
        └── 返回结果页（轮廓按钮）
```

---

## 组件设计

### 1. 体质头部 (`.detail-header`)

动态颜色系统，头部背景色根据体质类型动态设置。

**样式规格**
```scss
.detail-header {
  text-align: center;
  padding: 60rpx 30rpx 40rpx;
  border-radius: 0 0 40rpx 40rpx;
  color: #fff;
  /* background: 通过 :style 动态设置体质颜色 */
}

.constitution-icon {
  font-size: 100rpx;
  margin-bottom: 20rpx;
}

.constitution-name {
  font-size: 48rpx;
  font-weight: 700;
  margin-bottom: 12rpx;
}

.constitution-desc {
  font-size: 26rpx;
  opacity: 0.9;
  line-height: 1.5;
}
```

**数据绑定**
```vue
<view class="detail-header" :style="{ background: currentConstitution?.color }">
```

### 2. 体质特征 (`.characteristics`)

分为总体特征和心理特征两个部分。

**样式规格**
```scss
.characteristics {
  display: flex;
  flex-direction: column;
  gap: 30rpx;
}

.character-group {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.character-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #667eea;
  margin-bottom: 8rpx;
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.category-icon {
  font-size: 24rpx;
}

.character-list {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

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
  flex-shrink: 0;
}
```

**数据结构**
```javascript
{
  characteristics: {
    overall: [
      '体型匀称健壮',
      '面色、肤色润泽',
      '头发稠密有光泽',
      // ... 更多特征
    ],
    mental: ['性格随和开朗']  // 可选，部分体质可能没有
  }
}
```

### 3. 调理原则 (`.regulation-sections`)

包含饮食、运动、起居、情志四个方面的建议。

**样式规格**
```scss
.regulation-sections {
  display: flex;
  flex-direction: column;
  gap: 30rpx;
}

.regulation-item {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.regulation-category {
  display: flex;
  align-items: center;
  gap: 12rpx;
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
  padding-bottom: 12rpx;
  border-bottom: 2rpx solid #f0f0f0;
}

.regulation-list {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.regulation-text {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
  padding-left: 12rpx;
}
```

**分类图标系统**
```javascript
const categoryIcons = {
  diet: '🍎',
  exercise: '🏃',
  lifestyle: '🌙',
  emotion: '😊'
}

const categoryNames = {
  diet: '饮食建议',
  exercise: '运动建议',
  lifestyle: '起居建议',
  emotion: '情志调节'
}
```

**数据结构**
```javascript
{
  regulation: {
    diet: [
      '饮食有节，不要过饥过饱',
      '食物搭配要多样化',
      '清淡饮食，避免过饱'
    ],
    exercise: ['适度运动，劳逸结合'],
    lifestyle: [
      '规律作息，避免熬夜',
      '保持心情舒畅'
    ],
    emotion: ['保持心情愉快']  // 可选
  }
}
```

### 4. 禁忌事项 (`.taboos-grid`)

使用 2 列网格布局展示禁忌事项。

**样式规格**
```scss
.taboos-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16rpx;
}

.taboo-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 16rpx;
  background: #fff1f0;
  border-radius: 12rpx;
  border: 1rpx solid #ffccc7;
}

.taboo-icon {
  font-size: 24rpx;
  flex-shrink: 0;
}

.taboo-text {
  font-size: 26rpx;
  color: #cf1322;
  line-height: 1.4;
}
```

### 5. 科学依据 (`.science-card`)

展示 CCMQ 标准的科学性。

**样式规格**
```scss
.science-card {
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
}

.science-content {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.science-item {
  display: flex;
  gap: 16rpx;
  padding: 20rpx;
  background: #fff;
  border-radius: 16rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.04);
}

.science-icon {
  width: 60rpx;
  height: 60rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28rpx;
  flex-shrink: 0;
}

.science-info {
  flex: 1;
}

.science-title {
  font-size: 26rpx;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 6rpx;
}

.science-text {
  font-size: 24rpx;
  color: #666;
  line-height: 1.5;
}
```

---

## 数据流

### 状态管理

```javascript
// 页面参数
const resultId = ref('')        // 可选，用于返回
const constitution = ref('')    // 体质类型标识

// 数据
const resultData = ref(null)    // API 结果（可选）
const loading = ref(false)

// 计算属性
const currentConstitution = computed(() => {
  if (!constitution.value) return null
  return CONSTITUTION_INFO[constitution.value]
})
```

### 数据来源

**主要来源**：本地数据文件 `@/data/constitution.js`

**可选来源**：API 调用（当提供 resultId 时）

```javascript
async function loadResult() {
  loading.value = true
  try {
    const res = await getResult(resultId.value)
    resultData.value = res.data
    if (!constitution.value) {
      constitution.value = res.data.primary_constitution
    }
  } catch (error) {
    // 如果加载失败，仍然可以使用 constitution 参数
    if (constitution.value) {
      console.log('Using constitution parameter directly')
    }
  } finally {
    loading.value = false
  }
}
```

---

## 页面参数

| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| constitution | string | 是 | 体质类型标识 |
| resultId | string | 否 | 测试结果 ID（用于返回） |

**获取方式**:
```javascript
onLoad((options) => {
  if (options.resultId) {
    resultId.value = options.resultId
    loadResult()
  }
  if (options.constitution) {
    constitution.value = options.constitution
  }
})
```

---

## 条件渲染

| 内容 | 条件 | 说明 |
|------|------|------|
| 心理特征 | `characteristics.mental` 存在 | 部分体质可能没有 |
| 情志调节 | `regulation.emotion` 存在 | 部分体质可能没有 |
| 禁忌事项 | `taboos` 存在且非空 | 所有体质都有 |

**示例代码**:
```vue
<!-- 心理特征 -->
<view v-if="currentConstitution.characteristics.mental" class="character-group">
  <view class="character-title">
    <text class="category-icon">💭</text>
    心理特征
  </view>
  <view class="character-list">
    <view v-for="(item, index) in currentConstitution.characteristics.mental"
          :key="index" class="character-item">
      <text class="bullet">✓</text>
      <text>{{ item }}</text>
    </view>
  </view>
</view>

<!-- 情志调节 -->
<view v-if="currentConstitution.regulation.emotion" class="regulation-item">
  <view class="regulation-category">
    <text class="category-icon">😊</text>
    <text>情志调节</text>
  </view>
  <view class="regulation-list">
    <view v-for="(item, index) in currentConstitution.regulation.emotion"
          :key="index" class="regulation-text">
      • {{ item }}
    </view>
  </view>
</view>
```

---

## 用户交互

| 交互元素 | 触发事件 | 目标页面/行为 |
|----------|----------|---------------|
| 查看饮食推荐 | `@click="viewFood"` | `/pages/food/food?constitution={type}` |
| 返回结果页 | `@click="goBack"` | 有 resultId：`/pages/result/result?resultId={id}`<br>无 resultId：`uni.navigateBack()` |

**交互代码**:
```javascript
// 查看饮食推荐
function viewFood() {
  uni.navigateTo({
    url: `/pages/food/food?constitution=${constitution.value}`
  })
}

// 返回
function goBack() {
  if (resultId.value) {
    uni.navigateTo({
      url: `/pages/result/result?resultId=${resultId.value}`
    })
  } else {
    uni.navigateBack()
  }
}
```

---

## 样式变量

```scss
// 头部颜色（动态）
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

// 特征颜色
$color-feature-title: #667eea;
$color-bullet: #52c41a;

// 禁忌样式
$taboo-bg: #fff1f0;
$taboo-border: #ffccc7;
$taboo-text: #cf1322;

// 免责声明
$disclaimer-bg: #fffbe6;
$disclaimer-border: #ffe58f;
$disclaimer-title: #d46b08;
$disclaimer-text: #8c6800;
```

---

## 数据完整性

所有九种体质必须包含以下数据结构：

```javascript
{
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
    diet: string[],          // 饮食建议（至少2条）
    exercise: string[],      // 运动建议（至少1条）
    lifestyle: string[],     // 起居建议（至少2条）
    emotion?: string[]       // 情志调节（可选）
  },

  taboos: string[]           // 禁忌事项（至少2条）
}
```

---

## 滚动优化

```scss
.content-scroll {
  height: 100vh;
}
```

使用 `scroll-view` 组件实现平滑滚动，确保长内容页面在移动设备上有良好的体验。

---

## 可访问性

- 所有建议项使用清晰的视觉层次
- 禁忌事项使用警示色突出
- 免责声明使用醒目的警告样式
- 支持屏幕阅读器

---

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| constitution 参数缺失 | 提示错误并返回 |
| API 加载失败 | 使用本地 constitution 参数显示数据 |
| 数据不完整 | 使用 `v-if` 条件渲染避免错误 |
