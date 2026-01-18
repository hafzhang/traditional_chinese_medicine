<template>
  <view class="page-container">
    <view v-if="loading" class="loading">
      <view class="loading-spinner"></view>
      <view class="loading-text">加载中...</view>
    </view>

    <view v-else-if="result">
      <!-- 结果头部 -->
      <view class="result-header" :style="{ background: constitutionInfo?.color || '#667eea' }">
        <view class="result-icon">{{ constitutionInfo?.icon }}</view>
        <view class="result-title">您的体质是</view>
        <view class="constitution-name">
          {{ constitutionInfo?.name }}
        </view>
        <view class="result-desc">{{ constitutionInfo?.description }}</view>
      </view>

      <!-- 体质特征预览 -->
      <view class="card">
        <view class="card-title">
          <text class="title-icon">📋</text>
          主要特征
        </view>
        <view class="features-preview">
          <view
            v-for="(feature, idx) in constitutionInfo?.characteristics.overall?.slice(0, 4)"
            :key="idx"
            class="feature-item"
          >
            <text class="feature-bullet">✓</text>
            <text>{{ feature }}</text>
          </view>
        </view>
      </view>

      <!-- 分数展示 -->
      <view class="card">
        <view class="card-title">
          <text class="title-icon">📊</text>
          体质分数分析
        </view>
        <view class="score-chart">
          <view
            v-for="score in displayScores"
            :key="score.type"
            class="score-item"
          >
            <view class="score-info">
              <view class="score-header">
                <text class="score-icon">{{ CONSTITUTION_INFO[score.type]?.icon }}</text>
                <text class="score-name">{{ score.name }}</text>
              </view>
              <view class="score-value" :class="score.isPrimary ? 'primary' : ''">
                {{ score.value }}分
              </view>
            </view>
            <view class="score-bar">
              <view
                class="score-fill"
                :class="score.isPrimary ? 'primary' : ''"
                :style="{ width: score.value + '%', background: score.isPrimary ? constitutionInfo?.color : '#d9d9d9' }"
              ></view>
            </view>
          </view>
        </view>
      </view>

      <!-- 次要体质 -->
      <view v-if="result.secondary_constitutions?.length" class="card">
        <view class="card-title">
          <text class="title-icon">🔄</text>
          次要体质
        </view>
        <view class="secondary-list">
          <view
            v-for="item in result.secondary_constitutions"
            :key="item.type"
            class="secondary-item"
          >
            <view class="secondary-header">
              <text class="secondary-icon">{{ CONSTITUTION_INFO[item.type]?.icon }}</text>
              <text class="secondary-name">{{ item.name }}</text>
            </view>
            <view class="secondary-score">{{ item.score }}分</view>
          </view>
        </view>
      </view>

      <!-- 调理建议预览 -->
      <view class="card">
        <view class="card-title">
          <text class="title-icon">💡</text>
          调理建议
        </view>
        <view class="regulation-preview">
          <view class="regulation-item">
            <view class="regulation-label">
              <text class="label-icon">🍎</text>
              <text>饮食建议</text>
            </view>
            <view class="regulation-text">{{ constitutionInfo?.regulation.diet?.[0] }}</view>
          </view>
          <view class="regulation-item">
            <view class="regulation-label">
              <text class="label-icon">🏃</text>
              <text>运动建议</text>
            </view>
            <view class="regulation-text">{{ constitutionInfo?.regulation.exercise?.[0] }}</view>
          </view>
        </view>
      </view>

      <!-- 操作按钮 -->
      <view class="action-buttons">
        <button class="btn btn-primary btn-large btn-block" @click="viewDetail">
          <text class="btn-icon">📋</text>
          <text>查看详细分析</text>
        </button>
        <button class="btn btn-outline btn-block" @click="viewFood">
          <text class="btn-icon">🥗</text>
          <text>饮食推荐</text>
        </button>
        <button class="btn btn-text btn-block" @click="retest">
          重新测试
        </button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getResult } from '@/api/constitution.js'
import { CONSTITUTION_INFO } from '@/data/constitution.js'

// 状态
const resultId = ref('')
const result = ref(null)
const loading = ref(false)

// 计算属性
const constitutionInfo = computed(() => {
  if (!result.value?.primary_constitution) return null
  return CONSTITUTION_INFO[result.value.primary_constitution]
})

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
    .sort((a, b) => b.value - a.value)
})

// 生命周期
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
      uni.showToast({
        title: '参数错误',
        icon: 'none'
      })
      setTimeout(() => {
        uni.navigateBack()
      }, 1500)
    }
  }
})

/**
 * 加载结果
 */
async function loadResult() {
  loading.value = true
  try {
    const res = await getResult(resultId.value)
    result.value = res.data
  } catch (error) {
    const cached = uni.getStorageSync('latestResult')
    if (cached && (!resultId.value || cached.result_id === resultId.value)) {
      result.value = cached
      if (!resultId.value) {
        resultId.value = cached.result_id
      }
    } else {
      uni.showToast({
        title: '加载失败',
        icon: 'none'
      })
    }
  } finally {
    loading.value = false
  }
}

/**
 * 查看详情
 */
function viewDetail() {
  uni.navigateTo({
    url: `/pages/detail/detail?resultId=${resultId.value}&constitution=${result.value?.primary_constitution || ''}`
  })
}

/**
 * 查看饮食推荐
 */
function viewFood() {
  uni.navigateTo({
    url: `/pages/food/food?constitution=${result.value.primary_constitution}`
  })
}

/**
 * 重新测试
 */
function retest() {
  uni.showModal({
    title: '确认',
    content: '确定要重新测试吗？',
    success: (res) => {
      if (res.confirm) {
        uni.switchTab({
          url: '/pages/test/test'
        })
      }
    }
  })
}
</script>

<style lang="scss" scoped>
.loading {
  padding: 100rpx 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.loading-text {
  font-size: 28rpx;
  color: #999;
  margin-top: 20rpx;
}

.loading-spinner {
  width: 60rpx;
  height: 60rpx;
  border: 4rpx solid #f3f3f3;
  border-top: 4rpx solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.result-header {
  text-align: center;
  padding: 60rpx 30rpx;
  border-radius: 0 0 40rpx 40rpx;
  color: #fff;
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

.title-icon {
  font-size: 36rpx;
}

/* 特征预览 */
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

/* 分数图表 */
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

/* 次要体质 */
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

/* 调理建议预览 */
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

/* 操作按钮 */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
  padding: 0 30rpx 40rpx;
}

.btn-icon {
  margin-right: 8rpx;
}

.btn-text {
  background: transparent;
  border: none;
  color: #999;
}

.btn-text::after {
  border: none;
}
</style>
