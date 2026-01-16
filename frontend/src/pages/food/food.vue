<template>
  <view class="page-container">
    <view v-if="loading" class="loading">
      <view class="loading-spinner"></view>
      <view class="loading-text">加载中...</view>
    </view>

    <view v-else-if="error" class="error-state">
      <view class="error-icon">⚠️</view>
      <view class="error-text">{{ error }}</view>
      <button class="btn btn-primary" @click="goBack">返回</button>
    </view>

    <scroll-view v-else-if="foodData" scroll-y class="content-scroll">
      <!-- 头部 -->
      <view class="food-header">
        <view class="header-title">{{ foodData.constitution_name }}饮食推荐</view>
        <view class="header-subtitle">科学搭配，健康调理</view>
      </view>

      <!-- 体质概述 -->
      <view v-if="foodData.overview" class="card overview-card">
        <view class="card-title">
          <text class="title-icon">📖</text>
          体质概述
        </view>
        <view class="overview-text">{{ foodData.overview }}</view>
      </view>

      <!-- 推荐食物 -->
      <view class="card">
        <view class="card-title">
          <text class="title-icon">✅</text>
          宜吃食物
        </view>
        <view class="food-list">
          <view
            v-for="(item, index) in foodData.recommended_foods"
            :key="index"
            class="food-item recommended"
          >
            <view class="food-header-row">
              <view class="food-name">{{ item.name }}</view>
              <view class="food-tags">
                <text v-if="item.nature" class="tag tag-nature">{{ item.nature }}</text>
                <text v-if="item.flavor" class="tag tag-flavor">{{ item.flavor }}</text>
              </view>
            </view>
            <view v-if="item.effects?.length" class="food-effects">
              <text v-for="(effect, i) in item.effects" :key="i" class="effect-item">
                {{ effect }}
              </text>
            </view>
          </view>
        </view>
      </view>

      <!-- 不宜食物 -->
      <view v-if="foodData.avoid_foods?.length" class="card">
        <view class="card-title">
          <text class="title-icon">❌</text>
          不宜食物
        </view>
        <view class="food-list">
          <view
            v-for="(item, index) in foodData.avoid_foods"
            :key="index"
            class="food-item avoid"
          >
            <view class="food-name">{{ item.name }}</view>
            <view v-if="item.reason" class="avoid-reason">原因：{{ item.reason }}</view>
          </view>
        </view>
      </view>

      <!-- 推荐食谱 -->
      <view v-if="foodData.recipes?.length" class="card">
        <view class="card-title">
          <text class="title-icon">🍳</text>
          推荐食谱
        </view>
        <view class="recipe-list">
          <view
            v-for="(item, index) in foodData.recipes"
            :key="index"
            class="recipe-item-full"
          >
            <view class="recipe-name">{{ item.name }}</view>
            <view v-if="item.description" class="recipe-desc">{{ item.description }}</view>
            <view v-if="item.ingredients?.length" class="recipe-ingredients">
              <view class="recipe-subtitle">📝 配料：</view>
              <view class="ingredient-list">
                <text v-for="(ing, i) in item.ingredients" :key="i" class="ingredient-tag">{{ ing }}</text>
              </view>
            </view>
            <view v-if="item.steps?.length" class="recipe-steps">
              <view class="recipe-subtitle">👨‍🍳 做法：</view>
              <view class="step-list">
                <view v-for="(step, i) in item.steps" :key="i" class="step-item">{{ i + 1 }}. {{ step }}</view>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 饮食原则 -->
      <view v-if="foodData.principles?.length" class="card tips-card">
        <view class="card-title">
          <text class="title-icon">💡</text>
          饮食原则
        </view>
        <view class="tips-list">
          <view class="tip-item" v-for="(principle, index) in foodData.principles" :key="index">
            <text class="tip-icon">{{ index + 1 }}</text>
            <text class="tip-text">{{ principle }}</text>
          </view>
        </view>
      </view>

      <!-- 茶饮推荐 -->
      <view v-if="foodData.tea_recommendations?.length" class="card">
        <view class="card-title">
          <text class="title-icon">🍵</text>
          茶饮推荐
        </view>
        <view class="tea-list">
          <view
            v-for="(tea, index) in foodData.tea_recommendations"
            :key="index"
            class="tea-item"
          >
            <view class="tea-name">{{ tea.name }}</view>
            <view class="tea-ingredients">配料：{{ tea.ingredients }}</view>
            <view class="tea-effect">功效：{{ tea.effect }}</view>
          </view>
        </view>
      </view>

      <!-- 注意事项 -->
      <view v-if="foodData.precautions?.length" class="card caution-card">
        <view class="card-title">
          <text class="title-icon">⚠️</text>
          注意事项
        </view>
        <view class="caution-list">
          <view class="caution-item" v-for="(item, index) in foodData.precautions" :key="index">
            <text class="caution-bullet">•</text>
            <text class="caution-text">{{ item }}</text>
          </view>
        </view>
      </view>

      <!-- 运动建议 -->
      <view v-if="foodData.exercise_tips?.length" class="card">
        <view class="card-title">
          <text class="title-icon">🏃</text>
          运动建议
        </view>
        <view class="exercise-list">
          <view class="exercise-item" v-for="(tip, index) in foodData.exercise_tips" :key="index">
            <view class="exercise-title">{{ tip.title }}</view>
            <view class="exercise-content">{{ tip.content }}</view>
          </view>
        </view>
      </view>

      <!-- 四季调养 -->
      <view v-if="foodData.seasonal_tips" class="card seasonal-card">
        <view class="card-title">
          <text class="title-icon">🌡️</text>
          四季调养
        </view>
        <view class="seasonal-grid">
          <view class="seasonal-item" v-if="foodData.seasonal_tips.spring">
            <view class="seasonal-label">🌸 春季</view>
            <view class="seasonal-text">{{ foodData.seasonal_tips.spring }}</view>
          </view>
          <view class="seasonal-item" v-if="foodData.seasonal_tips.summer">
            <view class="seasonal-label">☀️ 夏季</view>
            <view class="seasonal-text">{{ foodData.seasonal_tips.summer }}</view>
          </view>
          <view class="seasonal-item" v-if="foodData.seasonal_tips.autumn">
            <view class="seasonal-label">🍂 秋季</view>
            <view class="seasonal-text">{{ foodData.seasonal_tips.autumn }}</view>
          </view>
          <view class="seasonal-item" v-if="foodData.seasonal_tips.winter">
            <view class="seasonal-label">❄️ 冬季</view>
            <view class="seasonal-text">{{ foodData.seasonal_tips.winter }}</view>
          </view>
        </view>
      </view>

      <!-- 养生建议 -->
      <view v-if="foodData.wellness_tips?.length" class="card wellness-card">
        <view class="card-title">
          <text class="title-icon">🥗</text>
          养生建议
        </view>
        <view class="wellness-list">
          <view class="wellness-item" v-for="(tip, index) in foodData.wellness_tips" :key="index">
            <view class="wellness-category">{{ tip.category }}</view>
            <view class="wellness-content-list">
              <view class="wellness-content-item" v-for="(content, i) in tip.items" :key="i">
                - {{ content }}
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 免责声明 -->
      <view class="disclaimer">
        <view class="disclaimer-text">
          以上建议仅供参考，具体饮食请根据个人情况调整。如有特殊疾病或过敏史，请咨询专业营养师或医生。
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getFoodRecommendations } from '@/api/constitution.js'
import { getLocalFoodRecommendations } from '@/data/foods.js'
import { CONSTITUTION_INFO } from '@/data/constitution.js'

// 状态
const constitution = ref('')
const foodData = ref(null)
const loading = ref(false)
const error = ref('')

// 从 URL 获取参数的辅助函数
function getQueryParams() {
  if (typeof window !== 'undefined' && window.location) {
    let params = {}

    // 尝试从 search 获取 (?constitution=xxx)
    if (window.location.search) {
      const urlParams = new URLSearchParams(window.location.search)
      for (const [key, value] of urlParams) {
        params[key] = value
      }
    }

    // 尝试从 hash 获取 (#/pages/food/food?constitution=xxx)
    if (window.location.hash && window.location.hash.includes('?')) {
      const hashQuery = window.location.hash.split('?')[1]
      const urlParams = new URLSearchParams(hashQuery)
      for (const [key, value] of urlParams) {
        params[key] = value
      }
    }

    console.log('[Food] Parsed params from URL:', params)
    return params
  }
  return {}
}

// 初始化页面参数
function initPageParams() {
  const params = getQueryParams()
  console.log('[Food] URL params:', params)

  if (params.constitution) {
    constitution.value = params.constitution
    loadRecommendations()
  } else {
    error.value = '参数错误，无法加载饮食推荐'
  }
}

// uni-app 生命周期（小程序环境）
onLoad((options) => {
  console.log('[Food] onLoad called:', options)
  if (options && options.constitution) {
    constitution.value = options.constitution
    loadRecommendations()
  } else if (!options) {
    // H5 环境手动获取
    initPageParams()
  }
})

// Vue 生命周期（H5 环境）
onMounted(() => {
  console.log('[Food] onMounted called')
  if (!constitution.value && !error.value) {
    initPageParams()
  }
})

async function loadRecommendations() {
  loading.value = true
  try {
    const res = await getFoodRecommendations(constitution.value)
    const apiData = res && res.data ? res.data : null
    const localData = getLocalFoodRecommendations(constitution.value)

    const hasApiContent =
      apiData &&
      (
        (Array.isArray(apiData.recommended_foods) && apiData.recommended_foods.length > 0) ||
        (Array.isArray(apiData.avoid_foods) && apiData.avoid_foods.length > 0) ||
        (Array.isArray(apiData.recipes) && apiData.recipes.length > 0) ||
        (Array.isArray(apiData.principles) && apiData.principles.length > 0) ||
        (Array.isArray(apiData.precautions) && apiData.precautions.length > 0) ||
        (Array.isArray(apiData.exercise_tips) && apiData.exercise_tips.length > 0) ||
        (Array.isArray(apiData.wellness_tips) && apiData.wellness_tips.length > 0) ||
        (Array.isArray(apiData.tea_recommendations) && apiData.tea_recommendations.length > 0) ||
        (apiData.seasonal_tips && Object.keys(apiData.seasonal_tips).length > 0)
      )

    if (hasApiContent) {
      foodData.value = apiData
    } else if (localData) {
      foodData.value = localData
      uni.showToast({
        title: '使用本地饮食推荐',
        icon: 'none'
      })
    } else {
      foodData.value = {
        constitution: constitution.value,
        constitution_name: CONSTITUTION_INFO[constitution.value]?.name || '未知体质',
        overview: CONSTITUTION_INFO[constitution.value]?.description || '',
        recommended_foods: [],
        avoid_foods: [],
        recipes: [],
        principles: [],
        precautions: [],
        exercise_tips: [],
        wellness_tips: []
      }
    }
  } catch (err) {
    console.error('API 加载失败，使用本地数据:', err)
    const localData = getLocalFoodRecommendations(constitution.value)
    if (localData) {
      foodData.value = localData
      uni.showToast({
        title: '使用本地饮食推荐',
        icon: 'none'
      })
    } else {
      foodData.value = {
        constitution: constitution.value,
        constitution_name: CONSTITUTION_INFO[constitution.value]?.name || '未知体质',
        overview: CONSTITUTION_INFO[constitution.value]?.description || '',
        recommended_foods: [],
        avoid_foods: [],
        recipes: [],
        principles: [],
        precautions: [],
        exercise_tips: [],
        wellness_tips: []
      }
    }
  } finally {
    loading.value = false
  }
}

/**
 * 返回上一页
 */
function goBack() {
  uni.navigateBack()
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
  border-top: 4rpx solid #52c41a;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100rpx 30rpx;
  text-align: center;
}

.error-icon {
  font-size: 100rpx;
  margin-bottom: 30rpx;
}

.error-text {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 40rpx;
}

.content-scroll {
  height: 100vh;
}

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

/* 体质概述 */
.overview-card {
  background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%);
}

.overview-text {
  font-size: 28rpx;
  color: #333;
  line-height: 1.8;
  text-indent: 2em;
}

.food-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.food-item {
  padding: 24rpx;
  border-radius: 16rpx;
  border: 2rpx solid #f0f0f0;
}

.food-item.recommended {
  background: #f6ffed;
  border-color: #d9f7be;
}

.food-item.avoid {
  background: #fff2e8;
  border-color: #ffbb96;
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

.avoid-reason {
  font-size: 26rpx;
  color: #d46b08;
  margin-top: 8rpx;
}

/* 食谱详细样式 */
.recipe-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.recipe-item-full {
  padding: 24rpx;
  background: #fff7e6;
  border-radius: 16rpx;
  border-left: 6rpx solid #faad14;
  margin-bottom: 16rpx;
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
  margin-bottom: 12rpx;
}

.recipe-subtitle {
  font-size: 26rpx;
  font-weight: 600;
  color: #faad14;
  margin-top: 16rpx;
  margin-bottom: 8rpx;
}

.ingredient-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.ingredient-tag {
  font-size: 24rpx;
  color: #fff;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
}

.step-list {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.step-item {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
  padding-left: 12rpx;
}

/* 饮食原则 */
.tips-card {
  background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%);
}

.tips-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
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

/* 茶饮推荐样式 */
.tea-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.tea-item {
  padding: 24rpx;
  background: #f0f5ff;
  border-radius: 16rpx;
  border-left: 6rpx solid #597ef7;
}

.tea-name {
  font-size: 30rpx;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 8rpx;
}

.tea-ingredients {
  font-size: 26rpx;
  color: #666;
  margin-bottom: 6rpx;
}

.tea-effect {
  font-size: 26rpx;
  color: #52c41a;
}

/* 注意事项 */
.caution-card {
  background: linear-gradient(135deg, #fff7e6 0%, #ffe7ba 100%);
}

.caution-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.caution-item {
  display: flex;
  align-items: flex-start;
  gap: 12rpx;
}

.caution-bullet {
  color: #faad14;
  font-size: 28rpx;
  font-weight: 600;
  flex-shrink: 0;
}

.caution-text {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
}

/* 运动建议 */
.exercise-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.exercise-item {
  padding: 20rpx;
  background: #f6ffed;
  border-radius: 16rpx;
}

.exercise-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #52c41a;
  margin-bottom: 8rpx;
}

.exercise-content {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
}

/* 四季调养 */
.seasonal-card {
  background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%);
}

.seasonal-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16rpx;
}

.seasonal-item {
  padding: 20rpx;
  background: #fff;
  border-radius: 16rpx;
  text-align: center;
}

.seasonal-label {
  font-size: 28rpx;
  font-weight: 600;
  color: #1890ff;
  margin-bottom: 8rpx;
}

.seasonal-text {
  font-size: 24rpx;
  color: #666;
  line-height: 1.4;
}

/* 养生建议 */
.wellness-card {
  background: linear-gradient(135deg, #f9f0ff 0%, #efdbff 100%);
}

.wellness-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.wellness-item {
  background: #fff;
  padding: 20rpx;
  border-radius: 16rpx;
}

.wellness-category {
  font-size: 28rpx;
  font-weight: 600;
  color: #722ed1;
  margin-bottom: 12rpx;
}

.wellness-content-list {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.wellness-content-item {
  font-size: 26rpx;
  color: #666;
  line-height: 1.5;
}

/* 免责声明 */
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
</style>
