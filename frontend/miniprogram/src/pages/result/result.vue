<template>
  <view class="container">
    <view v-if="result">
      <!-- 体质标签 -->
      <view class="header-card">
        <view class="tag-large tag-primary">{{ result.primary_name }}</view>
        <view class="score">得分: {{ result.report.score }}分</view>
      </view>

      <!-- 体质特征 -->
      <view class="card">
        <view class="card-title">体质特征</view>
        <view class="card-content">
          <view class="desc">{{ result.report.description }}</view>
          <view class="characteristics">
            <view class="char-item" v-for="(item, index) in result.report.characteristics" :key="index">
              <text class="char-icon">✓</text>
              <text>{{ item }}</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 得分雷达 -->
      <view class="card">
        <view class="card-title">九种体质得分</view>
        <view class="scores-list">
          <view
            class="score-item"
            v-for="(score, key) in result.scores"
            :key="key"
          >
            <view class="score-name">{{ getConstitutionName(key) }}</view>
            <view class="score-bar">
              <view class="score-fill" :style="{ width: score + '%' }"></view>
            </view>
            <view class="score-value">{{ score }}</view>
          </view>
        </view>
      </view>

      <!-- 调理要点 -->
      <view class="card">
        <view class="card-title">调理要点</view>
        <view class="advice">
          <view class="advice-item">
            <text class="advice-label">饮食原则：</text>
            <text>{{ result.report.diet_principle }}</text>
          </view>
          <view class="advice-item">
            <text class="advice-label">运动原则：</text>
            <text>{{ result.report.exercise_principle }}</text>
          </view>
          <view class="advice-item">
            <text class="advice-label">总体建议：</text>
            <text>{{ result.report.advice }}</text>
          </view>
        </view>
      </view>

      <!-- 次要体质 -->
      <view class="card" v-if="result.secondary && result.secondary.length > 0">
        <view class="card-title">兼夹体质</view>
        <view class="secondary-tags">
          <view
            class="tag tag-secondary"
            v-for="(item, index) in result.secondary"
            :key="index"
          >
            {{ item.name }} ({{ item.score }}分)
          </view>
        </view>
      </view>

      <!-- 操作按钮 -->
      <view class="actions">
        <button class="btn btn-primary" @tap="viewRecommendation">查看养生方案</button>
        <button class="btn btn-outline" @tap="shareResult">分享报告</button>
        <button class="btn btn-outline" @tap="retest">重新测试</button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const result = ref(null)

const CONSTITUTION_NAMES = {
  peace: '平和质',
  qi_deficiency: '气虚质',
  yang_deficiency: '阳虚质',
  yin_deficiency: '阴虚质',
  phlegm_damp: '痰湿质',
  damp_heat: '湿热质',
  blood_stasis: '血瘀质',
  qi_depression: '气郁质',
  special: '特禀质'
}

onMounted(() => {
  const data = uni.getStorageSync('quizResult')
  if (data) {
    result.value = data
  } else {
    uni.showToast({
      title: '请先完成测试',
      icon: 'none'
    })
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
  }
})

const getConstitutionName = (key) => {
  return CONSTITUTION_NAMES[key] || key
}

const viewRecommendation = () => {
  uni.navigateTo({
    url: `/pages/recommendation/recommendation?type=${result.value.primary}`
  })
}

const shareResult = () => {
  uni.showShareMenu({
    withShareTicket: true
  })
}

const retest = () => {
  uni.showModal({
    title: '确认重新测试',
    content: '重新测试将覆盖当前结果',
    success: (res) => {
      if (res.confirm) {
        uni.redirectTo({
          url: '/pages/quiz/quiz'
        })
      }
    }
  })
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background: #f8f8f8;
  padding: 30rpx;
}

.header-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 24rpx;
  padding: 60rpx 40rpx;
  text-align: center;
  margin-bottom: 30rpx;
}

.tag-large {
  display: inline-block;
  font-size: 48rpx;
  font-weight: bold;
  color: #fff;
  padding: 20rpx 60rpx;
  border-radius: 50rpx;
  margin-bottom: 20rpx;
}

.score {
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.9);
}

.card {
  background: #fff;
  border-radius: 24rpx;
  padding: 40rpx;
  margin-bottom: 30rpx;
}

.card-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 30rpx;
}

.card-content {
  font-size: 28rpx;
  color: #666;
  line-height: 1.8;
}

.desc {
  margin-bottom: 30rpx;
}

.characteristics {
  display: flex;
  flex-wrap: wrap;
  gap: 15rpx;
}

.char-item {
  display: flex;
  align-items: center;
  font-size: 26rpx;
  color: #333;
}

.char-icon {
  width: 40rpx;
  height: 40rpx;
  border-radius: 50%;
  background: #4CAF50;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10rpx;
  font-size: 22rpx;
}

.scores-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.score-item {
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.score-name {
  width: 120rpx;
  font-size: 26rpx;
  color: #666;
}

.score-bar {
  flex: 1;
  height: 16rpx;
  background: #e0e0e0;
  border-radius: 8rpx;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 8rpx;
  transition: width 0.5s;
}

.score-value {
  width: 60rpx;
  text-align: right;
  font-size: 24rpx;
  color: #999;
}

.advice {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.advice-item {
  font-size: 28rpx;
  color: #333;
  line-height: 1.8;
}

.advice-label {
  color: #667eea;
  font-weight: bold;
}

.secondary-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 15rpx;
}

.tag {
  display: inline-block;
  padding: 15rpx 30rpx;
  border-radius: 30rpx;
  font-size: 26rpx;
}

.tag-secondary {
  background: #FFC107;
  color: #fff;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.btn {
  height: 88rpx;
  border-radius: 44rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
  border: none;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.btn-outline {
  background: transparent;
  border: 2rpx solid #667eea;
  color: #667eea;
}
</style>
