# 设计系统总览

## 系统概述

本设计系统为中医体质识别应用提供统一的设计规范。

## 设计原则

| 原则 | 说明 |
|------|------|
| **科学性** | 基于王琦院士 CCMQ 标准量表 |
| **易用性** | 清晰的信息层次，简洁的操作流程 |
| **一致性** | 统一的色彩、组件、交互模式 |
| **可访问性** | 符合 WCAG AA 标准 |

---

## 色彩系统

### 主色调

```scss
// 品牌主色（紫色渐变）
$primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
$primary-solid: #667eea;
```

### 体质颜色系统

九种体质各有专属颜色，用于视觉区分：

| 体质类型 | 英文标识 | 颜色值 | RGB | 图标 |
|----------|----------|--------|-----|------|
| 平和质 | peace | #52c41a | rgb(82, 196, 26) | ☯ |
| 气虚质 | qi_deficiency | #faad14 | rgb(250, 173, 20) | 气 |
| 阳虚质 | yang_deficiency | #1890ff | rgb(24, 144, 255) | 阳 |
| 阴虚质 | yin_deficiency | #eb2f96 | rgb(235, 47, 150) | 阴 |
| 痰湿质 | phlegm_damp | #722ed1 | rgb(114, 46, 209) | 痰 |
| 湿热质 | damp_heat | #fa541c | rgb(250, 84, 28) | 湿 |
| 血瘀质 | blood_stasis | #f5222d | rgb(245, 34, 45) | 瘀 |
| 气郁质 | qi_depression | #13c2c2 | rgb(19, 194, 194) | 郁 |
| 特禀质 | special | #52c41a | rgb(82, 196, 26) | 特 |

### 功能色彩

```scss
// 状态色
$color-success: #52c41a;   // 成功、宜吃
$color-warning: #faad14;   // 警告、注意
$color-danger: #f5222d;    // 危险、禁忌
$color-info: #1890ff;      // 信息、提示

// 中性色
$bg-page: #f5f5f5;         // 页面背景
$bg-card: #ffffff;         // 卡片背景
$bg-light: #f8f9ff;        // 浅色背景
$border-color: #e8e8e8;    // 边框颜色

// 文本色
$text-primary: #1a1a1a;    // 主要文字
$text-secondary: #666666;  // 次要文字
$text-tertiary: #999999;   // 辅助文字
$text-disabled: #cccccc;   // 禁用文字
```

### 渐变色系统

```scss
// 功能图标渐变
$gradient-purple: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
$gradient-pink: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
$gradient-blue: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
$gradient-green: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
$gradient-orange: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
$gradient-cyan: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
```

---

## 排版系统

### 字体大小

```scss
$font-size-xl: 56rpx;   // 大标题（结果页体质名称）
$font-size-lg: 48rpx;   // 标题（详情页体质名称）
$font-size-md: 40rpx;   // 副标题
$font-size-base: 32rpx; // 正文标题
$font-size-sm: 28rpx;   // 正文
$font-size-xs: 26rpx;   // 小字
$font-size-xxs: 24rpx;  // 辅助文字
```

### 字重

```scss
$font-weight-normal: 400;
$font-weight-medium: 500;
$font-weight-semibold: 600;
$font-weight-bold: 700;
```

### 行高

```scss
$line-height-tight: 1.4;
$line-height-normal: 1.5;
$line-height-loose: 1.6;
```

---

## 间距系统

```scss
$spacing-xs: 8rpx;    // 超小间距
$spacing-sm: 12rpx;   // 小间距
$spacing-md: 20rpx;   // 中等间距
$spacing-lg: 30rpx;   // 大间距
$spacing-xl: 40rpx;   // 超大间距
$spacing-xxl: 60rpx;  // 特大间距
```

---

## 圆角系统

```scss
$radius-xs: 6rpx;     // 小圆角（标签）
$radius-sm: 12rpx;    // 小圆角（按钮）
$radius-md: 16rpx;    // 中等圆角（卡片项）
$radius-lg: 24rpx;    // 大圆角（卡片）
$radius-xl: 40rpx;    // 超大圆角（头部）
$radius-full: 50%;    // 完全圆角（圆形图标）
```

---

## 阴影系统

```scss
$shadow-sm: 0 2rpx 12rpx rgba(0, 0, 0, 0.04);
$shadow-md: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
$shadow-lg: 0 8rpx 30rpx rgba(0, 0, 0, 0.12);
```

---

## 组件规范

### 卡片 (Card)

```scss
.card {
  background: #fff;
  border-radius: 24rpx;
  padding: 30rpx;
  margin: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
}

.card-title {
  font-size: 32rpx;
  font-weight: 600;
  margin-bottom: 30rpx;
  color: #1a1a1a;
  display: flex;
  align-items: center;
  gap: 12rpx;
}
```

### 按钮 (Button)

**主按钮**
```scss
.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 16rpx;
  padding: 28rpx 48rpx;
}

.btn-primary:active {
  opacity: 0.8;
}
```

**轮廓按钮**
```scss
.btn-outline {
  background: transparent;
  color: #667eea;
  border: 2rpx solid #667eea;
  border-radius: 16rpx;
  padding: 28rpx 48rpx;
}
```

**大按钮**
```scss
.btn-large {
  padding: 32rpx 48rpx;
  font-size: 32rpx;
}
```

**全宽按钮**
```scss
.btn-block {
  width: 100%;
}
```

### 标签 (Tag)

```scss
.tag {
  padding: 4rpx 12rpx;
  border-radius: 6rpx;
  font-size: 22rpx;
}

// 体质类型标签
.constitution-tag {
  display: inline-flex;
  align-items: center;
  gap: 8rpx;
  padding: 10rpx 20rpx;
  border-radius: 20rpx;
  color: #fff;
}
```

### 图标

| 类型 | 规范 | 示例 |
|------|------|------|
| 体质图标 | 大尺寸，80-100rpx | ☯ 气 阳 阴 痰 湿 瘀 郁 特 |
| 功能图标 | 中尺寸，36rpx | 📋 🎯 🥗 📊 💡 🔄 |
| 分类图标 | 小尺寸，24-32rpx | 👤 💭 🍎 🏃 🌙 😊 |
| 状态图标 | 迷你尺寸，20-28rpx | ✓ ✅ ❌ ⚠️ 🚫 |

---

## 响应式设计

### 断点系统

```scss
// 小屏设备（手机竖屏）
$breakpoint-sm: 600rpx;

// 中屏设备（平板、手机横屏）
$breakpoint-md: 900rpx;

// 大屏设备（桌面）
$breakpoint-lg: 1200rpx;
```

### 适配规则

| 屏幕宽度 | 体质网格 | 其他调整 |
|----------|----------|----------|
| < 600rpx | 2列 | 减小间距 |
| >= 600rpx | 3列 | 标准布局 |
| >= 900rpx | 4列 | 增大内容宽度 |

---

## 动画系统

### 过渡时间

```scss
$transition-fast: 0.15s;
$transition-base: 0.3s;
$transition-slow: 0.5s;
```

### 缓动函数

```scss
$ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
$ease-out: cubic-bezier(0, 0, 0.2, 1);
$ease-in: cubic-bezier(0.4, 0, 1, 1);
```

---

## 可访问性标准

### 对比度要求

- **文字对比度**: 至少 4.5:1 (WCAG AA)
- **大文字对比度**: 至少 3:1 (WCAG AA)
- **UI 组件对比度**: 至少 3:1 (WCAG AA)

### 点击区域

- **最小尺寸**: 44x44 pt (约 88x88 rpx)
- **推荐尺寸**: 48x48 pt (约 96x96 rpx)

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

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2024-01-15 | 初始版本，建立基础设计系统 |
