<template>
  <view class="ingredient-detail-page">
    <scroll-view class="detail-scroll" scroll-y>
      <!-- 图片区域 -->
      <view class="image-section">
        <image
          v-if="ingredient.image_url"
          :src="ingredient.image_url"
          class="ingredient-image"
          mode="aspectFill"
        />
        <view v-else class="ingredient-image placeholder">🥗</view>
      </view>

      <!-- 基本信息 -->
      <view class="info-card">
        <view class="ingredient-name">{{ ingredient.name }}</view>
        <view class="aliases" v-if="ingredient.aliases && ingredient.aliases.length">
          别名：{{ ingredient.aliases.join('、') }}
        </view>

        <view class="tags">
          <text class="tag category">{{ ingredient.category }}</text>
          <text class="tag nature">{{ ingredient.nature }}</text>
          <text class="tag flavor">{{ ingredient.flavor }}</text>
        </view>
      </view>

      <!-- 性味归经 -->
      <view class="info-card" v-if="ingredient.meridians && ingredient.meridians.length">
        <view class="card-title">性味归经</view>
        <view class="meridians">
          <text v-for="meridian in ingredient.meridians" :key="meridian" class="meridian-tag">
            {{ meridian }}经
          </text>
        </view>
      </view>

      <!-- 功效 -->
      <view class="info-card" v-if="ingredient.efficacy">
        <view class="card-title">功效</view>
        <view class="card-content">{{ ingredient.efficacy }}</view>
      </view>

      <!-- 营养成分 -->
      <view class="info-card" v-if="ingredient.nutrition">
        <view class="card-title">营养成分</view>
        <view class="card-content">{{ ingredient.nutrition }}</view>
      </view>

      <!-- 食用指导 -->
      <view class="info-card">
        <view class="card-title">食用指导</view>
        <view class="guide-list">
          <view class="guide-item" v-if="ingredient.cooking_methods && ingredient.cooking_methods.length">
            <text class="guide-label">食用方法：</text>
            <text>{{ ingredient.cooking_methods.join('、') }}</text>
          </view>
          <view class="guide-item" v-if="ingredient.daily_dosage">
            <text class="guide-label">每日用量：</text>
            <text>{{ ingredient.daily_dosage }}</text>
          </view>
          <view class="guide-item" v-if="ingredient.best_time">
            <text class="guide-label">最佳时间：</text>
            <text>{{ ingredient.best_time }}</text>
          </view>
        </view>
      </view>

      <!-- 注意事项 -->
      <view class="info-card warning" v-if="ingredient.precautions">
        <view class="card-title">⚠️ 注意事项</view>
        <view class="card-content">{{ ingredient.precautions }}</view>
      </view>

      <!-- 搭配宜忌 -->
      <view class="info-card">
        <view class="card-title">搭配宜忌</view>
        <view class="compatible-list">
          <view class="compatible-item good" v-if="ingredient.compatible_with && ingredient.compatible_with.length">
            <text class="compatible-label">✅ 宜配：</text>
            <text>{{ ingredient.compatible_with.join('、') }}</text>
          </view>
          <view class="compatible-item bad" v-if="ingredient.incompatible_with && ingredient.incompatible_with.length">
            <text class="compatible-label">❌ 忌配：</text>
            <text>{{ ingredient.incompatible_with.join('、') }}</text>
          </view>
        </view>
      </view>

      <!-- 体质关联 -->
      <view class="info-card">
        <view class="card-title">体质关联</view>
        <view class="constitution-list">
          <view class="constitution-item" v-if="ingredient.suitable_constitutions && ingredient.suitable_constitutions.length">
            <text class="constitution-label">✅ 适用体质：</text>
            <text>{{ getConstitutionNames(ingredient.suitable_constitutions) }}</text>
          </view>
          <view class="constitution-item" v-if="ingredient.avoid_constitutions && ingredient.avoid_constitutions.length">
            <text class="constitution-label">⚠️ 禁忌体质：</text>
            <text>{{ getConstitutionNames(ingredient.avoid_constitutions) }}</text>
          </view>
        </view>
      </view>

      <!-- 描述 -->
      <view class="info-card" v-if="ingredient.description">
        <view class="card-title">简介</view>
        <view class="card-content">{{ ingredient.description }}</view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getIngredientDetail } from '@/api/ingredients.js'

// 数据
const ingredient = ref({})

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
    const res = await getIngredientDetail(id)
    if (res.code === 0) {
      ingredient.value = res.data
    }
  } catch (e) {
    console.error('加载食材详情失败', e)
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  } finally {
    uni.hideLoading()
  }
}

function getConstitutionNames(codes) {
  if (!codes || !codes.length) return ''
  return codes.map(code => constitutionNames[code] || code).join('、')
}
</script>

<style lang="scss" scoped>
.ingredient-detail-page {
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

.ingredient-image {
  width: 400rpx;
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

.ingredient-name {
  font-size: 40rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 10rpx;
}

.aliases {
  font-size: 26rpx;
  color: #999;
  margin-bottom: 20rpx;
}

.tags {
  display: flex;
  gap: 10rpx;
  flex-wrap: wrap;
}

.tag {
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
  font-size: 24rpx;

  &.category {
    background: #e6f7ff;
    color: #1890ff;
  }

  &.nature {
    background: #f6ffed;
    color: #52c41a;
  }

  &.flavor {
    background: #fff7e6;
    color: #fa8c16;
  }
}

.meridians {
  display: flex;
  gap: 10rpx;
  flex-wrap: wrap;
}

.meridian-tag {
  padding: 8rpx 20rpx;
  background: #f0f5ff;
  color: #597ef7;
  border-radius: 20rpx;
  font-size: 26rpx;
}

.guide-list {
  display: flex;
  flex-direction: column;
  gap: 15rpx;
}

.guide-item {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
}

.guide-label {
  color: #333;
  font-weight: 500;
}

.compatible-list {
  display: flex;
  flex-direction: column;
  gap: 15rpx;
}

.compatible-item {
  font-size: 28rpx;
  line-height: 1.6;

  &.good {
    color: #52c41a;
  }

  &.bad {
    color: #ff4d4f;
  }
}

.compatible-label {
  font-weight: 500;
}

.constitution-list {
  display: flex;
  flex-direction: column;
  gap: 15rpx;
}

.constitution-item {
  font-size: 28rpx;
  line-height: 1.6;
}

.constitution-label {
  font-weight: 500;
}
</style>
