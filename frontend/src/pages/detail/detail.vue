<template>
  <view class="page-container">
    <!-- 加载状态 -->
    <view v-if="loading" class="loading">
      <view class="loading-spinner"></view>
      <view class="loading-text">加载中...</view>
    </view>

    <!-- 错误状态 -->
    <view v-else-if="error" class="error-state">
      <view class="error-icon">⚠️</view>
      <view class="error-text">{{ error }}</view>
      <button class="btn btn-primary" @click="goBack">返回</button>
    </view>

    <!-- 内容区域 -->
    <scroll-view v-else-if="currentConstitution" scroll-y class="content-scroll">
      <!-- 头部 -->
      <view class="detail-header" :style="{ background: currentConstitution.color }">
        <view class="constitution-icon">{{ currentConstitution.icon }}</view>
        <view class="constitution-name">{{ currentConstitution.name }}</view>
        <view class="constitution-desc">{{ currentConstitution.description }}</view>
      </view>

      <!-- 体质特征 -->
      <view class="card">
        <view class="card-title">
          <text class="title-icon">📋</text>
          体质特征
        </view>
        <view class="characteristics">
          <!-- 总体特征 -->
          <view class="character-group">
            <view class="character-title">
              <text class="category-icon">👤</text>
              总体特征
            </view>
            <view class="character-list">
              <view v-for="(item, index) in currentConstitution.characteristics.overall" :key="index" class="character-item">
                <text class="bullet">✓</text>
                <text>{{ item }}</text>
              </view>
            </view>
          </view>

          <!-- 心理特征 -->
          <view v-if="currentConstitution.characteristics.mental" class="character-group">
            <view class="character-title">
              <text class="category-icon">💭</text>
              心理特征
            </view>
            <view class="character-list">
              <view v-for="(item, index) in currentConstitution.characteristics.mental" :key="index" class="character-item">
                <text class="bullet">✓</text>
                <text>{{ item }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 调理原则 -->
      <view class="card">
        <view class="card-title">
          <text class="title-icon">🎯</text>
          调理原则
        </view>
        <view class="regulation-sections">
          <!-- 饮食建议 -->
          <view v-if="currentConstitution.regulation.diet" class="regulation-item">
            <view class="regulation-category">
              <text class="category-icon">🍎</text>
              <text>饮食建议</text>
            </view>
            <view class="regulation-list">
              <view v-for="(item, index) in currentConstitution.regulation.diet" :key="index" class="regulation-text">
                • {{ item }}
              </view>
            </view>
          </view>

          <!-- 运动建议 -->
          <view v-if="currentConstitution.regulation.exercise" class="regulation-item">
            <view class="regulation-category">
              <text class="category-icon">🏃</text>
              <text>运动建议</text>
            </view>
            <view class="regulation-list">
              <view v-for="(item, index) in currentConstitution.regulation.exercise" :key="index" class="regulation-text">
                • {{ item }}
              </view>
            </view>
          </view>

          <!-- 起居建议 -->
          <view v-if="currentConstitution.regulation.lifestyle" class="regulation-item">
            <view class="regulation-category">
              <text class="category-icon">🌙</text>
              <text>起居建议</text>
            </view>
            <view class="regulation-list">
              <view v-for="(item, index) in currentConstitution.regulation.lifestyle" :key="index" class="regulation-text">
                • {{ item }}
              </view>
            </view>
          </view>

          <!-- 情志调节 -->
          <view v-if="currentConstitution.regulation.emotion" class="regulation-item">
            <view class="regulation-category">
              <text class="category-icon">😊</text>
              <text>情志调节</text>
            </view>
            <view class="regulation-list">
              <view v-for="(item, index) in currentConstitution.regulation.emotion" :key="index" class="regulation-text">
                • {{ item }}
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 禁忌事项 -->
      <view v-if="currentConstitution.taboos" class="card">
        <view class="card-title">
          <text class="title-icon">⚠️</text>
          禁忌事项
        </view>
        <view class="taboos-grid">
          <view v-for="(taboo, index) in currentConstitution.taboos" :key="index" class="taboo-item">
            <text class="taboo-icon">🚫</text>
            <text class="taboo-text">{{ taboo }}</text>
          </view>
        </view>
      </view>

      <!-- 科学依据 -->
      <view class="card science-card">
        <view class="card-title">
          <text class="title-icon">📚</text>
          科学依据
        </view>
        <view class="science-content">
          <view class="science-item">
            <view class="science-icon">🎓</view>
            <view class="science-info">
              <view class="science-title">王琦院士 CCMQ 标准</view>
              <view class="science-text">基于中国中医科学院王琦院士团队研发的《中医体质分类与判定》标准量表</view>
            </view>
          </view>
          <view class="science-item">
            <view class="science-icon">📊</view>
            <view class="science-info">
              <view class="science-title">大样本验证</view>
              <view class="science-text">经过全国大样本流行病学调查，信度和效度检验</view>
            </view>
          </view>
        </view>
      </view>

      <!-- 免责声明 -->
      <view class="disclaimer">
        <view class="disclaimer-title">⚠️ 重要提示</view>
        <view class="disclaimer-text">
          本产品提供的体质识别和养生建议仅供参考，不构成医疗诊断和治疗方案。如有疾病或严重健康问题，请及时就医。
        </view>
      </view>

      <!-- 操作按钮 -->
      <view class="action-buttons">
        <button class="btn btn-primary btn-large btn-block" @click="viewFood">
          <text class="btn-icon">🥗</text>
          <text>查看饮食推荐</text>
        </button>
        <button class="btn btn-outline btn-block" @click="goBack">
          返回结果页
        </button>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { CONSTITUTION_INFO } from '@/data/constitution.js'

const resultId = ref('')
const constitution = ref('')
const loading = ref(false)
const error = ref('')

const currentConstitution = computed(() => {
  if (!constitution.value) return null
  return CONSTITUTION_INFO[constitution.value] || null
})

function initFromStorage() {
  const cached = uni.getStorageSync('latestResult')
  if (cached) {
    if (!constitution.value && cached.primary_constitution) {
      constitution.value = cached.primary_constitution
    }
    if (!resultId.value && cached.result_id) {
      resultId.value = cached.result_id
    }
  }
}

onLoad((options) => {
  if (options) {
    if (options.constitution) {
      constitution.value = options.constitution
    }
    if (options.resultId) {
      resultId.value = options.resultId
    }
  }

  if (!constitution.value) {
    initFromStorage()
  }

  if (!constitution.value) {
    error.value = '缺少参数，无法查看体质详情'
  }
})

/**
 * 查看饮食推荐
 */
function viewFood() {
  uni.navigateTo({
    url: `/pages/food/food?constitution=${constitution.value}`
  })
}

/**
 * 返回
 */
function goBack() {
  if (resultId.value) {
    uni.navigateTo({
      url: `/pages/result/result?resultId=${resultId.value}`
    })
  } else {
    uni.navigateBack()
  }
}
</script>

<style lang="scss" scoped>
.loading {
  padding: 100rpx 0;
  display: flex;
  justify-content: center;
  align-items: center;
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

/* 头部 */
.detail-header {
  text-align: center;
  padding: 60rpx 30rpx 40rpx;
  border-radius: 0 0 40rpx 40rpx;
  color: #fff;
}

.constitution-icon {
  font-size: 100rpx;
  margin-bottom: 20rpx;
}

.constitution-name {
  font-size: 48rpx;
  font-weight: 700;
  margin-bottom: 12rpx;
}

.constitution-desc {
  font-size: 26rpx;
  opacity: 0.9;
  line-height: 1.5;
}

/* 卡片通用 */
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

/* 特征 */
.characteristics {
  display: flex;
  flex-direction: column;
  gap: 30rpx;
}

.character-group {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.character-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #667eea;
  margin-bottom: 8rpx;
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.category-icon {
  font-size: 24rpx;
}

.character-list {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.character-item {
  display: flex;
  align-items: flex-start;
  gap: 12rpx;
  font-size: 28rpx;
  color: #333;
  line-height: 1.6;
}

.bullet {
  color: #52c41a;
  font-weight: 600;
  flex-shrink: 0;
}

/* 调理原则 */
.regulation-sections {
  display: flex;
  flex-direction: column;
  gap: 30rpx;
}

.regulation-item {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.regulation-category {
  display: flex;
  align-items: center;
  gap: 12rpx;
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
  padding-bottom: 12rpx;
  border-bottom: 2rpx solid #f0f0f0;
}

.regulation-list {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.regulation-text {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
  padding-left: 12rpx;
}

/* 禁忌 */
.taboos-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16rpx;
}

.taboo-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 16rpx;
  background: #fff1f0;
  border-radius: 12rpx;
  border: 1rpx solid #ffccc7;
}

.taboo-icon {
  font-size: 24rpx;
  flex-shrink: 0;
}

.taboo-text {
  font-size: 26rpx;
  color: #cf1322;
  line-height: 1.4;
}

/* 科学依据 */
.science-card {
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
}

.science-content {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.science-item {
  display: flex;
  gap: 16rpx;
  padding: 20rpx;
  background: #fff;
  border-radius: 16rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.04);
}

.science-icon {
  width: 60rpx;
  height: 60rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28rpx;
  flex-shrink: 0;
}

.science-info {
  flex: 1;
}

.science-title {
  font-size: 26rpx;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 6rpx;
}

.science-text {
  font-size: 24rpx;
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

.disclaimer-title {
  font-size: 26rpx;
  font-weight: 600;
  color: #d46b08;
  margin-bottom: 12rpx;
}

.disclaimer-text {
  font-size: 24rpx;
  color: #8c6800;
  line-height: 1.6;
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
</style>
