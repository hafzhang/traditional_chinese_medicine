<template>
  <view class="recipe-detail-page">
    <scroll-view class="detail-scroll" scroll-y>
      <!-- 图片区域 -->
      <view class="image-section">
        <image
          v-if="recipe.image_url"
          :src="recipe.image_url"
          class="recipe-image"
          mode="aspectFill"
        />
        <view v-else class="recipe-image placeholder">🍲</view>
      </view>

      <!-- 基本信息 -->
      <view class="info-card">
        <view class="recipe-name">{{ recipe.name }}</view>
        <view class="recipe-meta">
          <text class="tag type">{{ recipe.type }}</text>
          <text class="tag difficulty" :class="recipe.difficulty">{{ recipe.difficulty }}</text>
          <text class="time">⏱ {{ recipe.cook_time }}分钟</text>
          <text class="servings">👤 {{ recipe.servings }}人份</text>
        </view>
      </view>

      <!-- 功效说明 -->
      <view class="info-card" v-if="recipe.efficacy">
        <view class="card-title">功效</view>
        <view class="card-content">{{ recipe.efficacy }}</view>
        <view class="card-sub" v-if="recipe.health_benefits">{{ recipe.health_benefits }}</view>
      </view>

      <!-- 食材清单 -->
      <view class="info-card" v-if="recipe.ingredients">
        <view class="card-title">食材清单</view>
        <view class="ingredients-section">
          <view class="ingredient-group" v-if="recipe.ingredients.main">
            <view class="group-title">主料</view>
            <view class="ingredient-list">
              <view class="ingredient-row" v-for="(item, index) in recipe.ingredients.main" :key="index">
                <text class="ingredient-name">{{ item.name }}</text>
                <text class="ingredient-amount">{{ item.amount }}</text>
              </view>
            </view>
          </view>
          <view class="ingredient-group" v-if="recipe.ingredients.auxiliary">
            <view class="group-title">辅料</view>
            <view class="ingredient-list">
              <view class="ingredient-row" v-for="(item, index) in recipe.ingredients.auxiliary" :key="index">
                <text class="ingredient-name">{{ item.name }}</text>
                <text class="ingredient-amount">{{ item.amount }}</text>
              </view>
            </view>
          </view>
          <view class="ingredient-group" v-if="recipe.ingredients.seasoning">
            <view class="group-title">调味</view>
            <view class="ingredient-list">
              <view class="ingredient-row" v-for="(item, index) in recipe.ingredients.seasoning" :key="index">
                <text class="ingredient-name">{{ item.name }}</text>
                <text class="ingredient-amount">{{ item.amount }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 制作步骤 -->
      <view class="info-card" v-if="recipe.steps && recipe.steps.length">
        <view class="card-title">制作步骤</view>
        <view class="steps-list">
          <view class="step-item" v-for="(step, index) in recipe.steps" :key="index">
            <view class="step-number">{{ index + 1 }}</view>
            <view class="step-content">{{ step }}</view>
          </view>
        </view>
      </view>

      <!-- 注意事项 -->
      <view class="info-card warning" v-if="recipe.precautions">
        <view class="card-title">⚠️ 注意事项</view>
        <view class="card-content">{{ recipe.precautions }}</view>
      </view>

      <!-- 适用体质 -->
      <view class="info-card" v-if="recipe.suitable_constitutions && recipe.suitable_constitutions.length">
        <view class="card-title">适用体质</view>
        <view class="constitutions">
          <text
            v-for="code in recipe.suitable_constitutions"
            :key="code"
            class="constitution-tag"
          >
            {{ getConstitutionName(code) }}
          </text>
        </view>
      </view>

      <!-- 主治症状 -->
      <view class="info-card" v-if="recipe.symptoms && recipe.symptoms.length">
        <view class="card-title">主治症状</view>
        <view class="symptoms">
          <text v-for="symptom in recipe.symptoms" :key="symptom" class="symptom-tag">
            {{ symptom }}
          </text>
        </view>
      </view>

      <!-- 适用季节 -->
      <view class="info-card" v-if="recipe.suitable_seasons && recipe.suitable_seasons.length">
        <view class="card-title">适用季节</view>
        <view class="seasons">
          <text v-for="season in recipe.suitable_seasons" :key="season" class="season-tag">
            {{ season }}季
          </text>
        </view>
      </view>

      <!-- 标签 -->
      <view class="info-card" v-if="recipe.tags && recipe.tags.length">
        <view class="card-title">标签</view>
        <view class="tags">
          <text v-for="tag in recipe.tags" :key="tag" class="tag-item">
            {{ tag }}
          </text>
        </view>
      </view>

      <!-- 描述 -->
      <view class="info-card" v-if="recipe.description">
        <view class="card-title">简介</view>
        <view class="card-content">{{ recipe.description }}</view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getRecipeDetail } from '@/api/recipes.js'

// 数据
const recipe = ref({})

// 体质名称映射
const constitutionNames = {
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

function getConstitutionName(code) {
  return constitutionNames[code] || code
}
</script>

<style lang="scss" scoped>
.recipe-detail-page {
  height: 100vh;
  background: #f5f5f5;
}

.detail-scroll {
  height: 100%;
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
    background: #f0f0f0;
    font-size: 150rpx;
  }
}

.info-card {
  background: #fff;
  margin: 20rpx;
  padding: 30rpx;
  border-radius: 16rpx;

  &.warning {
    background: #fffbe6;
    border: 1px solid #ffe58f;
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

.card-sub {
  font-size: 26rpx;
  color: #999;
  margin-top: 10rpx;
  line-height: 1.5;
}

.recipe-name {
  font-size: 40rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.recipe-meta {
  display: flex;
  gap: 10rpx;
  align-items: center;
  flex-wrap: wrap;
}

.tag {
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
  font-size: 24rpx;

  &.type {
    background: #e6f7ff;
    color: #1890ff;
  }

  &.difficulty {
    &.简单 {
      background: #f6ffed;
      color: #52c41a;
    }
    &.中等 {
      background: #fff7e6;
      color: #fa8c16;
    }
    &.困难 {
      background: #fff1f0;
      color: #ff4d4f;
    }
  }
}

.time, .servings {
  font-size: 26rpx;
  color: #999;
}

.ingredients-section {
  display: flex;
  flex-direction: column;
  gap: 30rpx;
}

.ingredient-group {
  .group-title {
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 15rpx;
  }
}

.ingredient-list {
  display: flex;
  flex-direction: column;
  gap: 10rpx;
}

.ingredient-row {
  display: flex;
  justify-content: space-between;
  padding: 15rpx 0;
  border-bottom: 1px solid #f0f0f0;
}

.ingredient-name {
  font-size: 28rpx;
  color: #333;
}

.ingredient-amount {
  font-size: 26rpx;
  color: #999;
}

.steps-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
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
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
  padding-top: 5rpx;
}

.constitutions, .symptoms, .seasons, .tags {
  display: flex;
  gap: 10rpx;
  flex-wrap: wrap;
}

.constitution-tag, .symptom-tag, .season-tag, .tag-item {
  padding: 8rpx 20rpx;
  border-radius: 20rpx;
  font-size: 26rpx;
}

.constitution-tag {
  background: #f0f5ff;
  color: #597ef7;
}

.symptom-tag {
  background: #fff7e6;
  color: #fa8c16;
}

.season-tag {
  background: #f6ffed;
  color: #52c41a;
}

.tag-item {
  background: #f5f5f5;
  color: #666;
}
</style>
