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

    <!-- 功能导航区域 -->
    <view class="features-section">
      <view class="section-header">
        <text class="section-title">功能导航</text>
        <text class="section-desc">核心功能 - 一键直达</text>
      </view>

      <view class="features-grid">
        <view
          v-for="item in features"
          :key="item.id"
          class="feature-card"
          @click="navigateTo(item.path, item.isTabBar)"
        >
          <view class="feature-icon-wrapper" :style="{ background: item.gradient }">
            <text class="feature-icon">{{ item.icon }}</text>
          </view>
          <view class="feature-info">
            <view class="feature-title">{{ item.title }}</view>
            <view class="feature-desc">{{ item.desc }}</view>
          </view>
          <view class="feature-action">
            <text class="action-text">{{ item.actionText }}</text>
            <text class="action-arrow">→</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 底部信息区域 -->
    <view class="footer-section">
      <view class="footer-item">
        <text class="footer-icon">🎓</text>
        <view class="footer-info">
          <view class="footer-title">王琦院士 CCMQ 标准</view>
          <view class="footer-desc">国家中医药管理局推广标准</view>
        </view>
      </view>
      <view class="footer-item">
        <text class="footer-icon">🔬</text>
        <view class="footer-info">
          <view class="footer-title">科学权威</view>
          <view class="footer-desc">基于大样本流行病学调查</view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

// 功能列表
const features = ref([
  {
    id: 1,
    icon: '📋',
    title: '体质测试',
    desc: '30道科学问题，精准识别您的体质类型',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    actionText: '立即测试',
    path: '/pages/test/test',
    isTabBar: true
  },
  {
    id: 2,
    icon: '🥬',
    title: '食材库',
    desc: '基于体质推荐的健康食材，了解性味归经',
    gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    actionText: '查看食材',
    path: '/pages/ingredients/list',
    isTabBar: false
  },
  {
    id: 3,
    icon: '🍲',
    title: '食谱库',
    desc: '根据体质推荐的养生食谱和食疗方案',
    gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    actionText: '查看食谱',
    path: '/pages/recipes/list',
    isTabBar: false
  },
  {
    id: 4,
    icon: '📍',
    title: '穴位查找',
    desc: '按症状/部位/经络查找穴位，按摩调理',
    gradient: 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
    actionText: '开始查找',
    path: '/pages/acupoints/list',
    isTabBar: false
  },
  {
    id: 5,
    icon: '👅',
    title: 'AI舌诊',
    desc: '通过舌象分析体质倾向，智能健康评估',
    gradient: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    actionText: '开始诊断',
    path: '/pages/tongue/index',
    isTabBar: false
  },
  {
    id: 6,
    icon: '📚',
    title: '养生课程',
    desc: '根据体质推荐的健康养生课程',
    gradient: 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
    actionText: '浏览课程',
    path: '/pages/courses/list',
    isTabBar: false
  }
])

/**
 * 开始体质测试
 */
function startTest() {
  uni.switchTab({
    url: '/pages/test/test'
  })
}

/**
 * 页面导航
 */
function navigateTo(path, isTabBar) {
  if (isTabBar) {
    uni.switchTab({
      url: path,
      fail: () => {
        console.log('switchTab failed, trying navigateTo')
        uni.navigateTo({ url: path })
      }
    })
  } else {
    uni.navigateTo({
      url: path,
      fail: (err) => {
        console.error('导航失败:', err)
        uni.showToast({
          title: '页面开发中',
          icon: 'none'
        })
      }
    })
  }
}
</script>

<style lang="scss" scoped>
.page-container {
  min-height: 100vh;
  background: #f5f5f5;
}

/* Hero 区域 */
.hero-section {
  position: relative;
  padding: 60rpx 30rpx 50rpx;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-bottom-left-radius: 40rpx;
  border-bottom-right-radius: 40rpx;
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: #fff;
}

.hero-icon {
  font-size: 100rpx;
  margin-bottom: 20rpx;
  opacity: 0.95;
}

.hero-title {
  font-size: 48rpx;
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
  justify-content: center;
}

/* 功能导航区域 */
.features-section {
  padding: 40rpx 30rpx;
}

.section-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30rpx;
}

.section-title {
  font-size: 36rpx;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 8rpx;
}

.section-desc {
  font-size: 24rpx;
  color: #999;
}

/* 功能网格 */
.features-grid {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.feature-card {
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 20rpx;
  padding: 28rpx 24rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.feature-card:active {
  transform: scale(0.98);
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.12);
}

.feature-icon-wrapper {
  width: 88rpx;
  height: 88rpx;
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-right: 20rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.15);
}

.feature-icon {
  font-size: 44rpx;
}

.feature-info {
  flex: 1;
  min-width: 0;
}

.feature-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 8rpx;
}

.feature-desc {
  font-size: 24rpx;
  color: #666;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.feature-action {
  display: flex;
  align-items: center;
  gap: 8rpx;
  flex-shrink: 0;
  margin-left: 12rpx;
}

.action-text {
  font-size: 24rpx;
  color: #667eea;
  font-weight: 500;
}

.action-arrow {
  font-size: 32rpx;
  color: #667eea;
  font-weight: 300;
}

/* 底部信息区域 */
.footer-section {
  padding: 0 30rpx 40rpx;
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.footer-item {
  display: flex;
  align-items: center;
  gap: 16rpx;
  background: #fff;
  padding: 24rpx;
  border-radius: 16rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.06);
}

.footer-icon {
  font-size: 36rpx;
  flex-shrink: 0;
}

.footer-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6rpx;
}

.footer-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #1a1a1a;
}

.footer-desc {
  font-size: 24rpx;
  color: #999;
}

/* 按钮样式 */
.btn {
  border: none;
  border-radius: 50rpx;
  padding: 28rpx 48rpx;
  font-size: 32rpx;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: #fff;
  color: #667eea;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.15);
}

.btn-primary:active {
  transform: scale(0.95);
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.2);
}

.btn-large {
  padding: 32rpx 64rpx;
  font-size: 32rpx;
}

.btn-block {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12rpx;
  min-width: 400rpx;
}

.btn-icon {
  font-size: 32rpx;
}
</style>
