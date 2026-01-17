<template>
  <view class="container">
    <!-- 头部 -->
    <view class="header">
      <image class="header-bg" src="/static/header-bg.png" mode="aspectFill"></image>
      <view class="header-content">
        <text class="title">中医体质养生助手</text>
        <text class="subtitle">了解你的体质，养出健康的生活</text>
      </view>
    </view>

    <!-- 测试入口 -->
    <view class="card" @tap="startQuiz">
      <view class="quiz-icon">🧘</view>
      <view class="quiz-title">开始体质测试</view>
      <view class="quiz-desc">30题精简问卷，5-8分钟完成</view>
      <view class="quiz-btn">立即测试</view>
    </view>

    <!-- 体质类型介绍 -->
    <view class="section">
      <view class="section-title">九种体质类型</view>
      <view class="constitution-list">
        <view
          class="constitution-item"
          v-for="item in constitutions"
          :key="item.type"
          @tap="viewConstitution(item)"
        >
          <view class="item-icon">{{ item.icon }}</view>
          <view class="item-info">
            <view class="item-name">{{ item.name }}</view>
            <view class="item-desc">{{ item.desc }}</view>
          </view>
        </view>
      </view>
    </view>

    <!-- 产品特点 -->
    <view class="section">
      <view class="section-title">为什么选择我们</view>
      <view class="feature-list">
        <view class="feature-item">
          <view class="feature-icon">📚</view>
          <view class="feature-text">专业可靠</view>
          <view class="feature-desc">基于王琦院士CCMQ标准量表</view>
        </view>
        <view class="feature-item">
          <view class="feature-icon">⚡</view>
          <view class="feature-text">快速便捷</view>
          <view class="feature-desc">5-8分钟完成测试</view>
        </view>
        <view class="feature-item">
          <view class="feature-icon">🎯</view>
          <view class="feature-text">个性精准</view>
          <view class="feature-desc">一人一方定制方案</view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

const constitutions = ref([
  { type: 'peace', name: '平和质', icon: '😊', desc: '健康体质，阴阳调和' },
  { type: 'qi_deficiency', name: '气虚质', icon: '😌', desc: '元气不足，容易疲乏' },
  { type: 'yang_deficiency', name: '阳虚质', icon: '🥶', desc: '阳气不足，畏寒怕冷' },
  { type: 'yin_deficiency', name: '阴虚质', icon: '🔥', desc: '阴液亏虚，口干咽燥' },
  { type: 'phlegm_damp', name: '痰湿质', icon: '😐', desc: '水湿内停，体形肥胖' },
  { type: 'damp_heat', name: '湿热质', icon: '😓', desc: '湿热内蕴，面垢油光' },
  { type: 'blood_stasis', name: '血瘀质', icon: '😶', desc: '血行不畅，面色晦暗' },
  { type: 'qi_depression', name: '气郁质', icon: '😔', desc: '气机郁滞，情绪抑郁' },
  { type: 'special', name: '特禀质', icon: '🤧', desc: '先天失常，容易过敏' }
])

const startQuiz = () => {
  uni.navigateTo({
    url: '/pages/quiz/quiz'
  })
}

const viewConstitution = (item) => {
  uni.showModal({
    title: item.name,
    content: item.desc,
    showCancel: false
  })
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background: linear-gradient(180deg, #f5f7fa 0%, #c3cfe2 100%);
}

.header {
  position: relative;
  height: 400rpx;
  overflow: hidden;
}

.header-bg {
  width: 100%;
  height: 100%;
}

.header-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  width: 100%;
}

.title {
  display: block;
  font-size: 48rpx;
  font-weight: bold;
  color: #fff;
  margin-bottom: 20rpx;
}

.subtitle {
  display: block;
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.9);
}

.card {
  background: #fff;
  border-radius: 24rpx;
  padding: 40rpx;
  margin: 30rpx;
  text-align: center;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.1);
}

.quiz-icon {
  font-size: 120rpx;
  margin-bottom: 20rpx;
}

.quiz-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 10rpx;
}

.quiz-desc {
  font-size: 26rpx;
  color: #999;
  margin-bottom: 30rpx;
}

.quiz-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  padding: 24rpx 60rpx;
  border-radius: 50rpx;
  display: inline-block;
  font-size: 28rpx;
}

.section {
  padding: 30rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 30rpx;
}

.constitution-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
}

.constitution-item {
  background: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  width: calc(50% - 10rpx);
  display: flex;
  align-items: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
}

.item-icon {
  font-size: 60rpx;
  margin-right: 20rpx;
}

.item-info {
  flex: 1;
}

.item-name {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
}

.item-desc {
  font-size: 22rpx;
  color: #999;
}

.feature-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.feature-item {
  background: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  display: flex;
  align-items: center;
}

.feature-icon {
  font-size: 60rpx;
  margin-right: 20rpx;
}

.feature-text {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
}

.feature-desc {
  font-size: 22rpx;
  color: #999;
  margin-left: auto;
}
</style>
