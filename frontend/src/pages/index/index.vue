<template>
  <view class="page-container">
    <!-- 头部 Hero 区域 -->
    <view class="hero-section">
      <view class="hero-bg"></view>
      <view class="hero-content">
        <view class="hero-icon">🩺</view>
        <view class="hero-title">中医体质识别</view>
        <view class="hero-subtitle">基于王琦院士 CCMQ 标准量表</view>

        <view class="hero-actions">
          <button class="btn btn-primary btn-large btn-block" @click="startTest">
            <text class="btn-icon">🎯</text>
            <text>开始体质测试</text>
          </button>
        </view>
      </view>
    </view>

    <!-- 快速开始卡片 -->
    <view class="section-card">
      <view class="section-header">
        <text class="section-icon">📋</text>
        <text class="section-title">测试说明</text>
      </view>
      <view class="intro-content">
        <view class="intro-item">
          <text class="intro-icon">✦</text>
          <text class="intro-text">通过30个问题，科学识别您的中医体质类型</text>
        </view>
        <view class="intro-item">
          <text class="intro-icon">✦</text>
          <text class="intro-text">基于国家中医药管理局发布的CCMQ标准量表</text>
        </view>
        <view class="intro-item">
          <text class="intro-icon">✦</text>
          <text class="intro-text">获得个性化体质分析和养生建议</text>
        </view>
      </view>
    </view>

    <!-- 九种体质类型 -->
    <view class="section-card">
      <view class="section-header">
        <text class="section-icon">☯</text>
        <text class="section-title">九种体质类型</text>
      </view>

      <view class="constitution-grid">
        <view
          v-for="item in constitutionTypes"
          :key="item.type"
          class="constitution-card"
          @click="viewConstitution(item)"
          :class="'border-' + item.type"
        >
          <view class="constitution-header" :style="{ background: item.color }">
            <text class="constitution-icon">{{ item.icon }}</text>
            <text class="constitution-mini-name">{{ item.name }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 功能特点 -->
    <view class="section-card">
      <view class="section-header">
        <text class="section-icon">⭐</text>
        <text class="section-title">功能特点</text>
      </view>

      <view class="feature-list">
        <view class="feature-card" v-for="(item, index) in features" :key="index" @click="handleFeatureClick(item)">
          <view class="feature-icon" :style="{ background: item.bgColor }">
            <text class="feature-emoji">{{ item.icon }}</text>
          </view>
          <view class="feature-content">
            <view class="feature-title">{{ item.title }}</view>
            <view class="feature-desc">{{ item.desc }}</view>
          </view>
        </view>
      </view>
    </view>

    <!-- 科学依据 -->
    <view class="section-card science-section">
      <view class="section-header">
        <text class="section-icon">📚</text>
        <text class="section-title">科学依据</text>
      </view>

      <view class="science-content">
        <view class="science-item">
          <view class="science-icon">🎓</view>
          <view class="science-info">
            <view class="science-title">王琦院士 CCMQ 标准</view>
            <view class="science-text">中国中医科学院王琦院士团队研发，国家中医药管理局推广标准</view>
          </view>
        </view>
        <view class="science-item">
          <view class="science-icon">📊</view>
          <view class="science-info">
            <view class="science-title">大样本验证</view>
            <view class="science-text">基于全国大样本流行病学调查，经过信度效度检验</view>
          </view>
        </view>
        <view class="science-item">
          <view class="science-icon">🔬</view>
          <view class="science-info">
            <view class="science-title">中医理论指导</view>
            <view class="science-text">融合《黄帝内经》《金匮要略》等经典中医体质理论</view>
          </view>
        </view>
      </view>
    </view>

    <!-- 底部行动按钮 -->
    <view class="bottom-action">
      <button class="btn btn-primary btn-large btn-block" @click="startTest">
        立即开始测试
      </button>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { CONSTITUTION_INFO } from '@/data/constitution.js'

// 九种体质数据
const constitutionTypes = ref(Object.values(CONSTITUTION_INFO).map(info => ({
  type: info.type,
  name: info.name,
  icon: info.icon,
  color: info.color,
  shortDesc: info.description,
  features: info.characteristics.overall.slice(0, 2)
})))

// 功能特点
const features = ref([
  {
    icon: '📋',
    title: '科学量表',
    desc: '采用国家中医药管理局发布的CCMQ标准量表',
    bgColor: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  {
    icon: '🎯',
    title: '精准识别',
    desc: '通过算法精确计算，识别主要体质和次要体质',
    bgColor: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
  },
  {
    icon: '🥗',
    title: '饮食推荐',
    desc: '根据体质类型提供个性化的饮食建议',
    bgColor: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
  }
])

/**
 * 开始测试
 */
function startTest() {
  console.log('startTest clicked')
  uni.switchTab({
    url: '/pages/test/test'
  })
}

/**
 * 查看体质详情
 */
function viewConstitution(item) {
  // 跳转到体质详情页，直接传递体质类型参数
  uni.navigateTo({
    url: `/pages/detail/detail?constitution=${item.type}`
  })
}

/**
 * 处理功能卡片点击
 */
function handleFeatureClick(item) {
  // 如果点击的是饮食推荐卡片，跳转到饮食列表页
  if (item.icon === '🥗') {
    uni.navigateTo({
      url: '/pages/food/list'
    })
  }
}
</script>

<style lang="scss" scoped>
.page-container {
  background: #f5f5f5;
  min-height: 100vh;
  padding-bottom: 40rpx;
}

/* Hero 区域 */
.hero-section {
  position: relative;
  padding: 60rpx 30rpx 40rpx;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  z-index: 0;
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: #fff;
}

.hero-icon {
  font-size: 120rpx;
  margin-bottom: 20rpx;
  opacity: 0.9;
}

.hero-title {
  font-size: 52rpx;
  font-weight: 700;
  margin-bottom: 16rpx;
  letter-spacing: 2rpx;
}

.hero-subtitle {
  font-size: 28rpx;
  opacity: 0.9;
  margin-bottom: 30rpx;
}

.hero-actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20rpx;
}

.hero-note {
  font-size: 24rpx;
  opacity: 0.8;
}

/* 卡片通用样式 */
.section-card {
  background: #fff;
  margin: 30rpx;
  border-radius: 24rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12rpx;
  margin-bottom: 30rpx;
}

.section-icon {
  font-size: 36rpx;
}

.section-title {
  font-size: 36rpx;
  font-weight: 700;
  color: #1a1a1a;
  flex: 1;
}

.section-desc {
  font-size: 24rpx;
  color: #999;
}

/* 测试说明 */
.intro-content {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.intro-item {
  display: flex;
  align-items: flex-start;
  gap: 12rpx;
}

.intro-icon {
  color: #667eea;
  font-size: 28rpx;
  flex-shrink: 0;
}

.intro-text {
  font-size: 28rpx;
  color: #555;
  line-height: 1.6;
}

/* 体质网格 */
.constitution-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20rpx;
}

.constitution-card {
  background: #fff;
  border-radius: 16rpx;
  overflow: hidden;
  border: 2rpx solid #f0f0f0;
  transition: all 0.3s;
}

.constitution-card:active {
  transform: scale(0.95);
}

.constitution-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12rpx;
  padding: 30rpx 20rpx;
  color: #fff;
}

.constitution-icon {
  font-size: 40rpx;
}

.constitution-mini-name {
  font-size: 28rpx;
  font-weight: 600;
}

/* 边框颜色 */
.border-peace { border-color: #52c41a; }
.border-qi_deficiency { border-color: #faad14; }
.border-yang_deficiency { border-color: #1890ff; }
.border-yin_deficiency { border-color: #eb2f96; }
.border-phlegm_damp { border-color: #722ed1; }
.border-damp_heat { border-color: #fa541c; }
.border-blood_stasis { border-color: #f5222d; }
.border-qi_depression { border-color: #13c2c2; }
.border-special { border-color: #52c41a; }

/* 功能特点 */
.feature-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.feature-card {
  display: flex;
  align-items: center;
  gap: 20rpx;
  padding: 24rpx;
  background: #f8f9ff;
  border-radius: 16rpx;
  transition: all 0.3s;
}

.feature-card:active {
  transform: scale(0.98);
  opacity: 0.8;
}

.feature-icon {
  width: 80rpx;
  height: 80rpx;
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.feature-emoji {
  font-size: 40rpx;
}

.feature-content {
  flex: 1;
}

.feature-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 8rpx;
}

.feature-desc {
  font-size: 26rpx;
  color: #666;
  line-height: 1.5;
}

/* 科学依据 */
.science-section {
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
}

.science-content {
  display: flex;
  flex-direction: column;
  gap: 30rpx;
}

.science-item {
  display: flex;
  gap: 20rpx;
  padding: 24rpx;
  background: #fff;
  border-radius: 16rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.04);
}

.science-icon {
  width: 70rpx;
  height: 70rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
  flex-shrink: 0;
}

.science-info {
  flex: 1;
}

.science-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 8rpx;
}

.science-text {
  font-size: 24rpx;
  color: #666;
  line-height: 1.5;
}

/* 底部行动按钮 */
.bottom-action {
  padding: 0 30rpx 40rpx;
}

.btn-large {
  padding: 32rpx 48rpx;
  font-size: 32rpx;
}
</style>
