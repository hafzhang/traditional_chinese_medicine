<template>
  <view class="page-container">
    <!-- 头部 -->
    <view class="header">
      <view class="header-icon">🥗</view>
      <view class="header-title">饮食推荐</view>
      <view class="header-subtitle">根据体质科学调理，吃出健康好身体</view>
    </view>

    <!-- 体质列表 -->
    <scroll-view scroll-y class="constitution-list">
      <view
        v-for="(item, key) in constitutions"
        :key="key"
        class="constitution-card"
        :style="{ '--card-color': item.color }"
        @click="goToFoodDetail(key)"
      >
        <view class="card-header">
          <view class="constitution-icon" :style="{ backgroundColor: item.color }">
            {{ item.icon }}
          </view>
          <view class="constitution-info">
            <view class="constitution-name">{{ item.name }}</view>
            <view class="constitution-desc">{{ item.description }}</view>
          </view>
          <view class="arrow-icon">›</view>
        </view>

        <view class="food-preview">
          <view class="preview-label">推荐食物</view>
          <view class="food-tags">
            <text
              v-for="(food, idx) in getPreviewFoods(key)"
              :key="idx"
              class="food-tag"
            >
              {{ food }}
            </text>
          </view>
        </view>
      </view>
    </scroll-view>

    <!-- 底部提示 -->
    <view class="footer-tip">
      <text>💡 点击查看该体质的详细饮食推荐</text>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { CONSTITUTION_INFO } from '@/data/constitution.js'
import { getLocalFoodRecommendations } from '@/data/foods.js'

// 所有体质数据
const constitutions = ref(CONSTITUTION_INFO)

/**
 * 获取预览食物列表（取前3个）
 */
function getPreviewFoods(type) {
  const foodData = getLocalFoodRecommendations(type)
  if (foodData && foodData.recommended_foods) {
    return foodData.recommended_foods.slice(0, 3).map(f => f.name)
  }
  return ['暂无数据']
}

/**
 * 跳转到饮食推荐详情页
 */
function goToFoodDetail(type) {
  uni.navigateTo({
    url: `/pages/food/food?constitution=${type}`
  })
}
</script>

<style lang="scss" scoped>
.page-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f9ff 0%, #e6f7ff 100%);
}

.header {
  text-align: center;
  padding: 60rpx 30rpx 40rpx;
  background: linear-gradient(135deg, #52c41a 0%, #389e0d 100%);
  border-radius: 0 0 40rpx 40rpx;
  color: #fff;
}

.header-icon {
  font-size: 80rpx;
  margin-bottom: 20rpx;
}

.header-title {
  font-size: 44rpx;
  font-weight: 700;
  margin-bottom: 12rpx;
}

.header-subtitle {
  font-size: 26rpx;
  opacity: 0.9;
}

.constitution-list {
  padding: 30rpx;
  height: calc(100vh - 300rpx);
}

.constitution-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 30rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
  border-left: 6rpx solid var(--card-color);
}

.constitution-card:active {
  transform: scale(0.98);
  opacity: 0.8;
}

.card-header {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.constitution-icon {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36rpx;
  color: #fff;
  margin-right: 20rpx;
  flex-shrink: 0;
}

.constitution-info {
  flex: 1;
}

.constitution-name {
  font-size: 32rpx;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 6rpx;
}

.constitution-desc {
  font-size: 24rpx;
  color: #666;
  line-height: 1.4;
}

.arrow-icon {
  font-size: 50rpx;
  color: #ccc;
  margin-left: 10rpx;
}

.food-preview {
  background: #f6ffed;
  border-radius: 16rpx;
  padding: 20rpx;
}

.preview-label {
  font-size: 24rpx;
  color: #52c41a;
  margin-bottom: 12rpx;
  font-weight: 600;
}

.food-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.food-tag {
  font-size: 24rpx;
  color: #52c41a;
  background: #fff;
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
  border: 1rpx solid #d9f7be;
}

.footer-tip {
  text-align: center;
  padding: 20rpx;
  font-size: 24rpx;
  color: #999;
}
</style>
