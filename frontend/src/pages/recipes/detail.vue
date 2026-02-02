<template>
  <view class="recipe-detail-page">
    <!-- 顶部导航 -->
    <view class="nav-bar">
      <view class="nav-back" @click="goBack">
        <text class="back-icon">←</text>
        <text class="nav-title">食谱详情</text>
      </view>
      <view class="nav-share" @click="shareRecipe">
        <text class="share-icon">Share</text>
      </view>
    </view>

    <scroll-view class="detail-scroll" scroll-y>
      <!-- 图片区域 -->
      <view class="image-section">
        <image
          v-if="recipe.cover_image"
          :src="recipe.cover_image"
          class="recipe-image"
          mode="aspectFill"
        />
        <view v-else class="recipe-image placeholder">
          <text class="placeholder-icon">🍲</text>
        </view>
      </view>

      <!-- 基本信息 -->
      <view class="info-card">
        <view class="recipe-name">{{ recipe.name }}</view>
        <view class="recipe-meta">
          <view class="difficulty-badge" :class="recipe.difficulty">
            {{ getDifficultyName(recipe.difficulty) }}
          </view>
          <text v-if="recipe.cooking_time" class="time">⏱ {{ recipe.cooking_time }}分钟</text>
          <text v-if="recipe.servings" class="servings">👤 {{ recipe.servings }}人份</text>
        </view>
      </view>

      <!-- 描述区域 (蓝色背景) -->
      <view v-if="recipe.desc" class="info-card desc-section">
        <view class="card-title">简介</view>
        <view class="card-content">{{ recipe.desc }}</view>
      </view>

      <!-- 贴士区域 (黄色背景) -->
      <view v-if="recipe.tip" class="info-card tip-section">
        <view class="card-title">💡 小贴士</view>
        <view class="card-content">{{ recipe.tip }}</view>
      </view>

      <!-- 体质信息 (适合 + 禁忌) -->
      <view class="info-card">
        <view class="card-title">适用体质</view>
        <view class="constitutions">
          <view
            v-for="code in recipe.suitable_constitutions"
            :key="'suit-' + code"
            class="constitution-tag suitable"
          >
            ✓ {{ getConstitutionName(code) }}
          </view>
        </view>
      </view>

      <view v-if="recipe.avoid_constitutions && recipe.avoid_constitutions.length" class="info-card avoid-section">
        <view class="card-title">禁忌体质</view>
        <view class="constitutions">
          <view
            v-for="code in recipe.avoid_constitutions"
            :key="'avoid-' + code"
            class="constitution-tag avoid"
          >
            ✗ {{ getConstitutionName(code) }}
          </view>
        </view>
      </view>

      <!-- 功效标签 -->
      <view v-if="recipe.efficacy_tags && recipe.efficacy_tags.length" class="info-card">
        <view class="card-title">功效标签</view>
        <view class="tags">
          <text
            v-for="tag in recipe.efficacy_tags"
            :key="tag"
            class="efficacy-tag"
          >
            {{ tag }}
          </text>
        </view>
      </view>

      <!-- 节气 -->
      <view v-if="recipe.solar_terms && recipe.solar_terms.length" class="info-card">
        <view class="card-title">适用节气</view>
        <view class="tags">
          <text
            v-for="term in recipe.solar_terms"
            :key="term"
            class="solar-term-tag"
          >
            {{ term }}
          </text>
        </view>
      </view>

      <!-- 食材清单 -->
      <view v-if="recipe.ingredients && recipe.ingredients.length" class="info-card">
        <view class="card-title">食材清单</view>
        <view class="ingredients-list">
          <view
            v-for="(item, index) in recipe.ingredients"
            :key="index"
            class="ingredient-row"
          >
            <view class="ingredient-header">
              <text class="ingredient-name">{{ item.name }}</text>
              <text v-if="item.amount" class="ingredient-amount">{{ item.amount }}</text>
            </view>
            <text v-if="item.is_primary" class="primary-badge">主料</text>
          </view>
        </view>
      </view>

      <!-- 制作步骤 -->
      <view v-if="recipe.steps && recipe.steps.length" class="info-card">
        <view class="card-title">制作步骤</view>
        <view class="steps-list">
          <view class="step-item" v-for="(step, index) in recipe.steps" :key="index">
            <view class="step-number">{{ index + 1 }}</view>
            <view class="step-content">
              <text class="step-text">{{ step.description }}</text>
              <text v-if="step.duration" class="step-duration">⏱ {{ step.duration }}</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 浏览次数 -->
      <view v-if="recipe.view_count" class="info-card view-count">
        <text class="view-text">👁 {{ recipe.view_count }} 次浏览</text>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getRecipeDetail, getConstitutionName, getDifficultyName } from '@/api/recipes.js'

// 数据
const recipe = ref({})

// 生命周期
onLoad((options) => {
  if (options.id) {
    loadDetail(options.id)
  }
})

async function loadDetail(id) {
  uni.showLoading({ title: '加载中...' })

  try {
    const res = await getRecipeDetail(id)
    if (res.code === 0) {
      recipe.value = res.data
    }
  } catch (e) {
    console.error('加载食谱详情失败', e)
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  } finally {
    uni.hideLoading()
  }
}

// 分享功能
function shareRecipe() {
  uni.showShareMenu({
    withShareTicket: true
  })
}

// 返回
function goBack() {
  uni.navigateBack()
}
</script>

<style lang="scss" scoped>
.recipe-detail-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  padding: 20rpx 30rpx;
  border-bottom: 1px solid #eee;
}

.nav-back {
  display: flex;
  align-items: center;
  gap: 10rpx;
}

.back-icon {
  font-size: 40rpx;
  color: #333;
}

.nav-title {
  font-size: 36rpx;
  font-weight: 600;
  color: #333;
}

.nav-share {
  padding: 10rpx 20rpx;
  background: #1890ff;
  border-radius: 40rpx;
  color: #fff;
  font-size: 26rpx;
}

.detail-scroll {
  flex: 1;
}

.image-section {
  background: #fff;
  padding: 40rpx;
  text-align: center;
}

.recipe-image {
  width: 100%;
  height: 400rpx;
  border-radius: 20rpx;

  &.placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }
}

.placeholder-icon {
  font-size: 150rpx;
}

.info-card {
  background: #fff;
  margin: 20rpx;
  padding: 30rpx;
  border-radius: 16rpx;

  &.desc-section {
    background: #e3f2fd;
  }

  &.tip-section {
    background: #fff9c4;
  }

  &.avoid-section {
    background: #fff1f0;
  }

  &.view-count {
    text-align: center;
    background: transparent;
  }
}

.card-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.card-content {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
}

.recipe-name {
  font-size: 40rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.recipe-meta {
  display: flex;
  gap: 15rpx;
  align-items: center;
  flex-wrap: wrap;
}

.difficulty-badge {
  padding: 8rpx 20rpx;
  border-radius: 20rpx;
  font-size: 24rpx;
  font-weight: 500;

  &.easy {
    background: #f6ffed;
    color: #52c41a;
  }

  &.medium {
    background: #fff7e6;
    color: #fa8c16;
  }

  &.harder {
    background: #fff1f0;
    color: #ff4d4f;
  }

  &.hard {
    background: #5c0011;
    color: #fff;
  }
}

.time, .servings {
  font-size: 26rpx;
  color: #999;
}

.constitutions, .tags {
  display: flex;
  gap: 15rpx;
  flex-wrap: wrap;
}

.constitution-tag {
  padding: 10rpx 24rpx;
  border-radius: 20rpx;
  font-size: 28rpx;

  &.suitable {
    background: #f6ffed;
    color: #52c41a;
  }

  &.avoid {
    background: #fff1f0;
    color: #ff4d4f;
  }
}

.efficacy-tag, .solar-term-tag {
  padding: 10rpx 24rpx;
  border-radius: 20rpx;
  font-size: 26rpx;
  background: #f0f5ff;
  color: #597ef7;
}

.solar-term-tag {
  background: #f6ffed;
  color: #52c41a;
}

.ingredients-list {
  display: flex;
  flex-direction: column;
  gap: 15rpx;
}

.ingredient-row {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
  padding: 15rpx 0;
  border-bottom: 1px solid #f0f0f0;

  &:last-child {
    border-bottom: none;
  }
}

.ingredient-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ingredient-name {
  font-size: 30rpx;
  color: #333;
  font-weight: 500;
}

.ingredient-amount {
  font-size: 26rpx;
  color: #999;
}

.primary-badge {
  display: inline-block;
  padding: 4rpx 12rpx;
  border-radius: 8rpx;
  font-size: 22rpx;
  background: #fff7e6;
  color: #fa8c16;
  align-self: flex-start;
}

.steps-list {
  display: flex;
  flex-direction: column;
  gap: 25rpx;
}

.step-item {
  display: flex;
  gap: 15rpx;
}

.step-number {
  width: 50rpx;
  height: 50rpx;
  border-radius: 50%;
  background: #1890ff;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  font-weight: bold;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.step-text {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
}

.step-duration {
  font-size: 24rpx;
  color: #999;
}

.view-text {
  font-size: 26rpx;
  color: #999;
}
</style>
