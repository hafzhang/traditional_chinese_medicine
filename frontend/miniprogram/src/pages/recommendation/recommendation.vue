<template>
  <view class="container">
    <view v-if="recommendation">
      <!-- 饮食推荐 -->
      <view class="card">
        <view class="card-header">
          <text class="card-icon">🍲</text>
          <text class="card-title">饮食推荐</text>
        </view>
        <view class="rec-section">
          <view class="rec-title">宜吃食物</view>
          <view class="food-list">
            <text class="food-item" v-for="(item, index) in recommendation.diet.suitable" :key="index">
              {{ item }}
            </text>
          </view>
        </view>
        <view class="rec-section">
          <view class="rec-title">忌吃食物</view>
          <view class="food-list">
            <text class="food-item food-avoid" v-for="(item, index) in recommendation.diet.avoid" :key="index">
              {{ item }}
            </text>
          </view>
        </view>
        <view class="rec-section" v-if="recommendation.diet.recipes">
          <view class="rec-title">推荐食谱</view>
          <view class="recipe-list">
            <view class="recipe-item" v-for="(item, index) in recommendation.diet.recipes" :key="index">
              <text class="recipe-icon">👩‍🍳</text>
              <text>{{ item }}</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 运动推荐 -->
      <view class="card">
        <view class="card-header">
          <text class="card-icon">🏃</text>
          <text class="card-title">运动推荐</text>
        </view>
        <view class="rec-section">
          <view class="rec-title">推荐运动</view>
          <view class="exercise-list">
            <text class="exercise-item" v-for="(item, index) in recommendation.exercise.recommended" :key="index">
              {{ item }}
            </text>
          </view>
        </view>
        <view class="rec-section" v-if="recommendation.exercise.avoid && recommendation.exercise.avoid.length">
          <view class="rec-title">避免运动</view>
          <view class="exercise-list">
            <text class="exercise-item exercise-avoid" v-for="(item, index) in recommendation.exercise.avoid" :key="index">
              {{ item }}
            </text>
          </view>
        </view>
        <view class="rec-section">
          <view class="rec-title">运动建议</view>
          <view class="advice-text">{{ recommendation.exercise.advice }}</view>
        </view>
      </view>

      <!-- 作息建议 -->
      <view class="card">
        <view class="card-header">
          <text class="card-icon">🌙</text>
          <text class="card-title">作息建议</text>
        </view>
        <view class="sleep-info">
          <view class="sleep-item">
            <text class="sleep-label">入睡时间：</text>
            <text class="sleep-value">{{ recommendation.lifestyle.sleep_time }}</text>
          </view>
          <view class="sleep-item">
            <text class="sleep-label">睡眠时长：</text>
            <text class="sleep-value">{{ recommendation.lifestyle.sleep_duration }}</text>
          </view>
          <view class="sleep-item">
            <text class="sleep-label">健康建议：</text>
            <text class="sleep-value">{{ recommendation.lifestyle.advice }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API_BASE = 'http://localhost:8000/api/v1'

const recommendation = ref(null)

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  const options = currentPage.options

  loadRecommendation(options.type)
})

const loadRecommendation = async (type) => {
  if (!type) {
    const result = uni.getStorageSync('quizResult')
    if (result) {
      type = result.primary
    }
  }

  if (!type) {
    uni.showToast({
      title: '请先完成测试',
      icon: 'none'
    })
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
    return
  }

  try {
    const res = await uni.request({
      url: `${API_BASE}/recommendation/${type}`,
      method: 'GET'
    })

    if (res.data.code === 0) {
      recommendation.value = res.data.data
    }
  } catch (e) {
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  }
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background: #f8f8f8;
  padding: 30rpx;
}

.card {
  background: #fff;
  border-radius: 24rpx;
  padding: 40rpx;
  margin-bottom: 30rpx;
}

.card-header {
  display: flex;
  align-items: center;
  margin-bottom: 30rpx;
}

.card-icon {
  font-size: 48rpx;
  margin-right: 20rpx;
}

.card-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.rec-section {
  margin-bottom: 30rpx;
}

.rec-section:last-child {
  margin-bottom: 0;
}

.rec-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #666;
  margin-bottom: 15rpx;
}

.food-list,
.exercise-list {
  display: flex;
  flex-wrap: wrap;
  gap: 15rpx;
}

.food-item,
.exercise-item {
  padding: 12rpx 24rpx;
  background: #f0f0f0;
  border-radius: 20rpx;
  font-size: 26rpx;
  color: #333;
}

.food-avoid,
.exercise-avoid {
  background: #ffebee;
  color: #f44336;
}

.recipe-list {
  display: flex;
  flex-direction: column;
  gap: 15rpx;
}

.recipe-item {
  display: flex;
  align-items: center;
  font-size: 28rpx;
  color: #333;
}

.recipe-icon {
  font-size: 32rpx;
  margin-right: 15rpx;
}

.advice-text {
  font-size: 28rpx;
  color: #666;
  line-height: 1.8;
  padding: 20rpx;
  background: #f9f9f9;
  border-radius: 12rpx;
}

.sleep-info {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.sleep-item {
  display: flex;
  font-size: 28rpx;
}

.sleep-label {
  color: #666;
  min-width: 160rpx;
}

.sleep-value {
  color: #333;
  font-weight: bold;
}
</style>
