<template>
  <view class="routine-page">
    <view v-if="routineData" class="routine-container">
      <!-- 季节信息 -->
      <view v-if="routineData.current_season" class="season-banner">
        <text class="season-icon">{{ getSeasonIcon(routineData.current_season.code) }}</text>
        <view class="season-info">
          <text class="season-name">{{ routineData.current_season.name }}</text>
          <text class="season-tip">当前季节，注意调整作息</text>
        </view>
      </view>

      <!-- 作息方案 -->
      <view v-if="routineData.routine" class="routine-content">
        <!-- 基本信息 -->
        <view class="routine-header">
          <view class="routine-name">{{ routineData.routine.name }}</view>
          <view class="routine-time">
            <text>起床 {{ routineData.routine.wake_time }}</text>
            <text>睡眠 {{ routineData.routine.sleep_time }}</text>
          </view>
        </view>

        <!-- 餐饮时间 -->
        <view v-if="routineData.routine.meal_timings" class="meal-times">
          <view class="section-title">用餐时间</view>
          <view class="meal-list">
            <view class="meal-item" v-for="(time, meal) in routineData.routine.meal_timings" :key="meal">
              <text class="meal-name">{{ getMealName(meal) }}</text>
              <text class="meal-time">{{ time }}</text>
            </view>
          </view>
        </view>

        <!-- 晨间安排 -->
        <view v-if="routineData.routine.morning_routine && routineData.routine.morning_routine.length" class="routine-section morning">
          <view class="section-title with-icon">
            <text class="section-icon">🌅</text>
            <text>晨间安排</text>
          </view>
          <view class="routine-list">
            <view
              v-for="(item, index) in routineData.routine.morning_routine"
              :key="index"
              class="routine-item"
            >
              <text class="routine-time">{{ item.time || '' }}</text>
              <view class="routine-content">
                <text class="routine-activity">{{ item.activity || item }}</text>
                <text v-if="item.duration" class="routine-duration">{{ item.duration }}</text>
                <text v-if="item.note" class="routine-note">{{ item.note }}</text>
              </view>
            </view>
          </view>
        </view>

        <!-- 午间安排 -->
        <view v-if="routineData.routine.afternoon_routine && routineData.routine.afternoon_routine.length" class="routine-section afternoon">
          <view class="section-title with-icon">
            <text class="section-icon">☀️</text>
            <text>午间安排</text>
          </view>
          <view class="routine-list">
            <view
              v-for="(item, index) in routineData.routine.afternoon_routine"
              :key="index"
              class="routine-item"
            >
              <text class="routine-time">{{ item.time || '' }}</text>
              <view class="routine-content">
                <text class="routine-activity">{{ item.activity || item }}</text>
                <text v-if="item.duration" class="routine-duration">{{ item.duration }}</text>
                <text v-if="item.note" class="routine-note">{{ item.note }}</text>
              </view>
            </view>
          </view>
        </view>

        <!-- 晚间安排 -->
        <view v-if="routineData.routine.evening_routine && routineData.routine.evening_routine.length" class="routine-section evening">
          <view class="section-title with-icon">
            <text class="section-icon">🌙</text>
            <text>晚间安排</text>
          </view>
          <view class="routine-list">
            <view
              v-for="(item, index) in routineData.routine.evening_routine"
              :key="index"
              class="routine-item"
            >
              <text class="routine-time">{{ item.time || '' }}</text>
              <view class="routine-content">
                <text class="routine-activity">{{ item.activity || item }}</text>
                <text v-if="item.duration" class="routine-duration">{{ item.duration }}</text>
                <text v-if="item.note" class="routine-note">{{ item.note }}</text>
              </view>
            </view>
          </view>
        </view>

        <!-- 温馨提示 -->
        <view v-if="routineData.routine.tips && routineData.routine.tips.length" class="tips-section">
          <view class="section-title">💡 温馨提示</view>
          <view class="tips-list">
            <text v-for="(tip, index) in routineData.routine.tips" :key="index" class="tip-item">
              • {{ tip }}
            </text>
          </view>
        </view>

        <!-- 季节调整 -->
        <view v-if="routineData.current_season && routineData.current_season.adjustment" class="seasonal-adjustment">
          <view class="section-title seasonal-title">🍂 季节调整建议</view>
          <view class="adjustment-content">
            <text v-if="routineData.current_season.adjustment.tips" class="adjustment-tip">
              {{ routineData.current_season.adjustment.tips }}
            </text>
            <view v-if="routineData.current_season.adjustment.modified_activities" class="modified-activities">
              <text
                v-for="(value, key) in routineData.current_season.adjustment.modified_activities"
                :key="key"
                class="modified-item"
              >
                • {{ key }}: {{ value }}
              </text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 加载状态 -->
    <view v-else class="loading-state">
      <text>加载中...</text>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getRoutineWithSeasonalInfo } from '@/api/routines.js'

const routineData = ref(null)

// 获取用户体质（这里简化处理，实际应从用户信息中获取）
const userConstitution = ref('peace') // 默认平和质

onMounted(() => {
  loadRoutine()
})

async function loadRoutine() {
  try {
    routineData.value = await getRoutineWithSeasonalInfo(userConstitution.value)
  } catch (e) {
    console.error('加载作息方案失败:', e)
    uni.showToast({ title: '加载失败', icon: 'none' })
  }
}

function getSeasonIcon(season) {
  const icons = {
    spring: '🌸',
    summer: '☀️',
    autumn: '🍂',
    winter: '❄️'
  }
  return icons[season] || '🌤️'
}

function getMealName(meal) {
  const names = {
    breakfast: '早餐',
    lunch: '午餐',
    dinner: '晚餐'
  }
  return names[meal] || meal
}
</script>

<style scoped>
.routine-page {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.routine-container {
  padding-bottom: 40rpx;
}

.season-banner {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 30rpx;
  display: flex;
  align-items: center;
  color: #fff;
}

.season-icon {
  font-size: 60rpx;
  margin-right: 20rpx;
}

.season-info {
  flex: 1;
}

.season-name {
  display: block;
  font-size: 36rpx;
  font-weight: bold;
  margin-bottom: 8rpx;
}

.season-tip {
  display: block;
  font-size: 24rpx;
  opacity: 0.9;
}

.routine-content {
  padding: 20rpx;
}

.routine-header {
  background-color: #fff;
  padding: 30rpx;
  border-radius: 16rpx;
  margin-bottom: 20rpx;
}

.routine-name {
  font-size: 40rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 16rpx;
}

.routine-time {
  display: flex;
  justify-content: space-between;
  font-size: 28rpx;
  color: #666;
}

.meal-times {
  background-color: #fff;
  padding: 30rpx;
  border-radius: 16rpx;
  margin-bottom: 20rpx;
}

.meal-list {
  display: flex;
  justify-content: space-around;
  margin-top: 20rpx;
}

.meal-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.meal-name {
  font-size: 24rpx;
  color: #999;
  margin-bottom: 8rpx;
}

.meal-time {
  font-size: 32rpx;
  color: #4CAF50;
  font-weight: bold;
}

.routine-section {
  background-color: #fff;
  padding: 30rpx;
  border-radius: 16rpx;
  margin-bottom: 20rpx;
}

.routine-section.morning {
  border-left: 6rpx solid #FFB74D;
}

.routine-section.afternoon {
  border-left: 6rpx solid #4FC3F7;
}

.routine-section.evening {
  border-left: 6rpx solid #7E57C2;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 24rpx;
}

.section-title.with-icon {
  display: flex;
  align-items: center;
}

.section-icon {
  font-size: 36rpx;
  margin-right: 12rpx;
}

.routine-list {
  padding-left: 10rpx;
}

.routine-item {
  display: flex;
  margin-bottom: 20rpx;
  padding-bottom: 20rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.routine-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.routine-time {
  width: 120rpx;
  font-size: 26rpx;
  color: #999;
  flex-shrink: 0;
}

.routine-content {
  flex: 1;
}

.routine-activity {
  display: block;
  font-size: 28rpx;
  color: #333;
  margin-bottom: 6rpx;
}

.routine-duration {
  display: block;
  font-size: 24rpx;
  color: #4CAF50;
}

.routine-note {
  display: block;
  font-size: 24rpx;
  color: #999;
  margin-top: 6rpx;
}

.tips-section {
  background-color: #FFF9E6;
  padding: 30rpx;
  border-radius: 16rpx;
  margin-bottom: 20rpx;
}

.tips-list {
  margin-top: 16rpx;
}

.tip-item {
  display: block;
  font-size: 28rpx;
  color: #666;
  line-height: 1.8;
  margin-bottom: 10rpx;
}

.seasonal-adjustment {
  background-color: #F3E5F5;
  padding: 30rpx;
  border-radius: 16rpx;
}

.seasonal-title {
  color: #7E57C2;
}

.adjustment-content {
  margin-top: 16rpx;
}

.adjustment-tip {
  display: block;
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
  margin-bottom: 16rpx;
}

.modified-activities {
  margin-top: 16rpx;
}

.modified-item {
  display: block;
  font-size: 26rpx;
  color: #7E57C2;
  line-height: 1.8;
}

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  color: #999;
}
</style>
