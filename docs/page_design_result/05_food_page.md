# 饮食推荐页面设计文档

## 页面概述

| 项目 | 说明 |
|------|------|
| 页面路径 | `/pages/food/food` |
| 页面名称 | 饮食推荐 - 体质饮食 |
| 主要功能 | 根据体质类型提供个性化饮食建议 |
| 数据来源 | API: `getFoodRecommendations()` |

---

## 页面结构

```
饮食推荐页面 (food)
├── 加载状态
│   └── 加载动画
│
└── 推荐内容（可滚动 scroll-view）
    ├── 饮食头部
    │   ├── 标题：{体质名称}饮食推荐（40rpx）
    │   └── 副标题：科学搭配，健康调理（26rpx）
    │
    ├── 宜吃食物卡片
    │   ├── 标题：✅ 宜吃食物
    │   └── 食物列表
    │       └── 食物项
    │           ├── 食物名称（30rpx）
    │           ├── 标签组
    │           │   ├── 性质标签（如：温）
    │           │   └── 味道标签（如：甘）
    │           └── 功效标签
    │
    ├── 不宜食物卡片（条件显示）
    │   ├── 标题：❌ 不宜食物
    │   └── 食物列表
    │       └── 食物项
    │           ├── 食物名称
    │           └── 不宜原因
    │
    ├── 推荐食谱卡片（条件显示）
    │   ├── 标题：🍳 推荐食谱
    │   └── 食谱列表
    │       └── 食谱项
    │           ├── 食谱名称（30rpx）
    │           └── 食谱描述（26rpx）
    │
    ├── 饮食原则卡片
    │   ├── 标题：💡 饮食原则
    │   └── 原则列表（4条）
    │       ├── 序号图标（圆形渐变）
    │       └── 原则文本
    │
    └── 免责声明
        └── 免责文本
```

---

## 组件设计

### 1. 饮食头部 (`.food-header`)

**样式规格**
```scss
.food-header {
  text-align: center;
  padding: 60rpx 30rpx 40rpx;
  background: linear-gradient(135deg, #52c41a 0%, #389e0d 100%);
  border-radius: 0 0 40rpx 40rpx;
  color: #fff;
}

.header-title {
  font-size: 40rpx;
  font-weight: 700;
  margin-bottom: 12rpx;
}

.header-subtitle {
  font-size: 26rpx;
  opacity: 0.9;
}
```

### 2. 宜吃食物 (`.food-item.recommended`)

**样式规格**
```scss
.food-item.recommended {
  background: #f6ffed;
  border-color: #d9f7be;
}

.food-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12rpx;
}

.food-name {
  font-size: 30rpx;
  font-weight: 600;
  color: #1a1a1a;
}

.food-tags {
  display: flex;
  gap: 8rpx;
}

.tag {
  padding: 4rpx 12rpx;
  border-radius: 6rpx;
  font-size: 22rpx;
}

.tag-nature {
  background: #e6f7ff;
  color: #1890ff;
}

.tag-flavor {
  background: #fff0f6;
  color: #eb2f96;
}

.food-effects {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.effect-item {
  font-size: 24rpx;
  color: #52c41a;
  background: #f6ffed;
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
}
```

### 3. 不宜食物 (`.food-item.avoid`)

**样式规格**
```scss
.food-item.avoid {
  background: #fff2e8;
  border-color: #ffbb96;
}

.avoid-reason {
  font-size: 26rpx;
  color: #d46b08;
  margin-top: 8rpx;
}
```

### 4. 推荐食谱 (`.recipe-item`)

**样式规格**
```scss
.recipe-item {
  padding: 24rpx;
  background: #fff7e6;
  border-radius: 16rpx;
  border-left: 6rpx solid #faad14;
}

.recipe-name {
  font-size: 30rpx;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 8rpx;
}

.recipe-desc {
  font-size: 26rpx;
  color: #666;
  line-height: 1.5;
}
```

### 5. 饮食原则 (`.tips-card`)

**样式规格**
```scss
.tips-card {
  background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%);
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.tip-icon {
  width: 48rpx;
  height: 48rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  font-weight: 600;
  flex-shrink: 0;
}

.tip-text {
  flex: 1;
  font-size: 28rpx;
  color: #333;
  line-height: 1.5;
}
```

---

## 食物标签系统

### 性质标签 (nature)

| 性质 | 颜色代码 | 背景色 | 文字色 | 说明 |
|------|----------|--------|--------|------|
| 温 | warm | #e6f7ff | #1890ff | 温热，助阳 |
| 热 | hot | #fff1f0 | #f5222d | 热烈，燥热 |
| 平 | neutral | #f5f5f5 | #666666 | 平和，不偏 |
| 凉 | cool | #e6f7ff | #1890ff | 凉润，清热 |
| 寒 | cold | #fff1f0 | #f5222d | 寒凉，泻火 |

### 味道标签 (flavor)

| 味道 | 颜色代码 | 背景色 | 文字色 | 说明 |
|------|----------|--------|--------|------|
| 酸 | sour | #fff0f6 | #eb2f96 | 收敛，固涩 |
| 苦 | bitter | #fff7e6 | #faad14 | 泻火，燥湿 |
| 甘 | sweet | #f6ffed | #52c41a | 补益，和中 |
| 辛 | spicy | #fff2e8 | #fa541c | 散寒，行气 |
| 咸 | salty | #f0f9ff | #13c2c2 | 软坚，润下 |

---

## 数据流

### 状态管理

```javascript
// 页面参数
const constitution = ref('')    // 体质类型标识

// 数据
const foodData = ref(null)      // API 返回的饮食数据
const loading = ref(false)
```

### 页面参数获取

```javascript
onLoad((options) => {
  if (options.constitution) {
    constitution.value = options.constitution
    loadRecommendations()
  } else {
    uni.showToast({ title: '参数错误', icon: 'none' })
    setTimeout(() => uni.navigateBack(), 1500)
  }
})
```

---

## API 调用

**端点**: `GET /api/v1/food/recommendations?constitution={type}`

**响应格式**:
```json
{
  "code": 200,
  "data": {
    "constitution": "yang_deficiency",
    "constitution_name": "阳虚质",
    "recommended_foods": [
      {
        "name": "羊肉",
        "nature": "温",
        "flavor": "甘",
        "effects": ["补肾阳", "温中暖下", "益气补虚"]
      },
      {
        "name": "韭菜",
        "nature": "温",
        "flavor": "辛",
        "effects": ["温补肾阳", "行气活血"]
      }
    ],
    "avoid_foods": [
      {
        "name": "西瓜",
        "reason": "性寒凉，易伤阳气"
      },
      {
        "name": "苦瓜",
        "reason": "性寒，损伤阳气"
      }
    ],
    "recipes": [
      {
        "name": "当归生姜羊肉汤",
        "description": "温中补虚，祛寒止痛，适用于阳虚体质冬季进补"
      },
      {
        "name": "韭菜炒虾仁",
        "description": "补肾壮阳，益气养血"
      }
    ]
  }
}
```

**调用代码**:
```javascript
async function loadRecommendations() {
  loading.value = true
  try {
    const res = await getFoodRecommendations(constitution.value)
    foodData.value = res.data
  } catch (error) {
    uni.showToast({ title: '加载失败', icon: 'none' })
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

---

## 样式变量

```scss
// 头部颜色
$food-header-gradient: linear-gradient(135deg, #52c41a 0%, #389e0d 100%);

// 食物状态
$food-recommended-bg: #f6ffed;
$food-recommended-border: #d9f7be;
$food-avoid-bg: #fff2e8;
$food-avoid-border: #ffbb96;

// 标签颜色
$tag-nature-bg: #e6f7ff;
$tag-nature-text: #1890ff;
$tag-flavor-bg: #fff0f6;
$tag-flavor-text: #eb2f96;
$effect-bg: #f6ffed;
$effect-text: #52c41a;

// 食谱样式
$recipe-bg: #fff7e6;
$recipe-border: #faad14;

// 原则卡片
$tips-card-gradient: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%);
```

---

## 可访问性

- 食物卡片使用绿色/橙色背景区分宜吃/不宜
- 所有标签具有足够的对比度
- 食物功效使用绿色标签突出显示
- 免责声明使用醒目的黄色背景

---

## 滚动优化

```scss
.content-scroll {
  height: 100vh;
}
```

---

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| constitution 参数缺失 | 提示"参数错误"并返回 |
| API 加载失败 | 显示 Toast 提示 |
| 数据为空 | 显示空状态提示 |

---

## 免责声明

```vue
<view class="disclaimer">
  <view class="disclaimer-text">
    以上建议仅供参考，具体饮食请根据个人情况调整。如有特殊疾病或过敏史，请咨询专业营养师或医生。
  </view>
</view>
```

**样式**:
```scss
.disclaimer {
  background: #fffbe6;
  border-radius: 16rpx;
  padding: 24rpx;
  margin: 0 30rpx 30rpx;
  border: 2rpx solid #ffe58f;
}

.disclaimer-text {
  font-size: 24rpx;
  color: #8c6800;
  line-height: 1.6;
}
```
