<template>
  <view class="acupoint-detail-page">
    <scroll-view class="detail-scroll" scroll-y>
      <!-- 头部信息 -->
      <view class="header-card">
        <view class="acupoint-name">{{ acupoint.name }}</view>
        <view class="acupoint-code">{{ acupoint.code }}</view>
        <view class="acupoint-meridian">{{ acupoint.meridian }}</view>
        <view class="acupoint-body-part">
          <text class="label">部位：</text>
          <text>{{ acupoint.body_part }}</text>
        </view>
      </view>

      <!-- 定位说明 -->
      <view class="info-card">
        <view class="card-title">
          <text class="title-icon">📍</text>
          取穴定位
        </view>
        <view class="location-content">
          <view class="simple-location" v-if="acupoint.simple_location">
            <text class="location-label">简易取穴：</text>
            <text class="location-text">{{ acupoint.simple_location }}</text>
          </view>
          <view class="detail-location" v-if="acupoint.location">
            <text class="location-label">标准定位：</text>
            <text class="location-text">{{ acupoint.location }}</text>
          </view>
        </view>
      </view>

      <!-- 功效作用 -->
      <view class="info-card" v-if="acupoint.efficacy && acupoint.efficacy.length">
        <view class="card-title">
          <text class="title-icon">✨</text>
          功效作用
        </view>
        <view class="efficacy-list">
          <text class="efficacy-item" v-for="(efficacy, index) in acupoint.efficacy" :key="index">
            {{ efficacy }}
          </text>
        </view>
      </view>

      <!-- 主治病症 -->
      <view class="info-card" v-if="acupoint.indications && acupoint.indications.length">
        <view class="card-title">
          <text class="title-icon">🏥</text>
          主治病症
        </view>
        <view class="indications-list">
          <text class="indication-tag" v-for="(indication, index) in acupoint.indications" :key="index">
            {{ indication }}
          </text>
        </view>
      </view>

      <!-- 按摩方法 -->
      <view class="info-card massage">
        <view class="card-title">
          <text class="title-icon">🙌</text>
          按摩方法
        </view>
        <view class="massage-info">
          <view class="massage-item" v-if="acupoint.massage_method">
            <text class="massage-label">手法：</text>
            <text class="massage-text">{{ acupoint.massage_method }}</text>
          </view>
          <view class="massage-item" v-if="acupoint.massage_duration">
            <text class="massage-label">时长：</text>
            <text class="massage-text">{{ acupoint.massage_duration }}</text>
          </view>
          <view class="massage-item" v-if="acupoint.massage_frequency">
            <text class="massage-label">频率：</text>
            <text class="massage-text">{{ acupoint.massage_frequency }}</text>
          </view>
        </view>
      </view>

      <!-- 注意事项 -->
      <view class="info-card warning" v-if="acupoint.precautions">
        <view class="card-title">
          <text class="title-icon">⚠️</text>
          注意事项
        </view>
        <view class="precautions-text">{{ acupoint.precautions }}</view>
      </view>

      <!-- 体质关联 -->
      <view class="info-card" v-if="acupoint.suitable_constitutions && acupoint.suitable_constitutions.length">
        <view class="card-title">
          <text class="title-icon">🎯</text>
          体质调理
        </view>
        <view class="constitution-info">
          <view class="constitutions">
            <text class="constitution-tag" v-for="code in acupoint.suitable_constitutions" :key="code">
              {{ getConstitutionName(code) }}
            </text>
          </view>
          <view class="constitution-benefit" v-if="acupoint.constitution_benefit">
            {{ acupoint.constitution_benefit }}
          </view>
        </view>
      </view>

      <!-- 穴位图片 -->
      <view class="info-card" v-if="acupoint.image_url">
        <view class="card-title">
          <text class="title-icon">🖼️</text>
          穴位图示
        </view>
        <image :src="acupoint.image_url" class="acupoint-image" mode="aspectFill" />
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getAcupointDetail } from '@/api/acupoints.js'

// 数据
const acupoint = ref({})

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
    const res = await getAcupointDetail(id)
    if (res.code === 0) {
      acupoint.value = res.data
    }
  } catch (e) {
    console.error('加载穴位详情失败', e)
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
.acupoint-detail-page {
  height: 100vh;
  background: #f5f5f5;
}

.detail-scroll {
  height: 100%;
}

.header-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 50rpx 30rpx;
  color: #fff;
  text-align: center;
}

.acupoint-name {
  font-size: 44rpx;
  font-weight: bold;
  margin-bottom: 15rpx;
}

.acupoint-code {
  font-size: 26rpx;
  opacity: 0.9;
  margin-bottom: 20rpx;
  padding: 8rpx 20rpx;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20rpx;
  display: inline-block;
}

.acupoint-meridian {
  font-size: 28rpx;
  opacity: 0.9;
  margin-bottom: 15rpx;
}

.acupoint-body-part {
  font-size: 26rpx;
  opacity: 0.8;
}

.info-card {
  background: #fff;
  margin: 20rpx;
  padding: 30rpx;
  border-radius: 16rpx;

  &.massage {
    background: #f0f9ff;
    border: 1px solid #bae7ff;
  }

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
  display: flex;
  align-items: center;
  gap: 10rpx;
}

.title-icon {
  font-size: 36rpx;
}

.location-content {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.simple-location,
.detail-location {
  display: flex;
  gap: 10rpx;
}

.location-label {
  font-size: 26rpx;
  font-weight: 500;
  color: #333;
  flex-shrink: 0;
}

.location-text {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
  flex: 1;
}

.efficacy-list,
.indications-list {
  display: flex;
  gap: 10rpx;
  flex-wrap: wrap;
}

.efficacy-item,
.indication-tag {
  font-size: 26rpx;
  padding: 8rpx 16rpx;
  border-radius: 20rpx;
}

.efficacy-item {
  background: #f6ffed;
  color: #52c41a;
}

.indication-tag {
  background: #fff7e6;
  color: #fa8c16;
}

.massage-info {
  display: flex;
  flex-direction: column;
  gap: 15rpx;
}

.massage-item {
  display: flex;
  gap: 10rpx;
}

.massage-label {
  font-size: 26rpx;
  font-weight: 500;
  color: #333;
  flex-shrink: 0;
}

.massage-text {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
  flex: 1;
}

.precautions-text {
  font-size: 26rpx;
  color: #8c6800;
  line-height: 1.6;
}

.constitution-info {
  display: flex;
  flex-direction: column;
  gap: 15rpx;
}

.constitutions {
  display: flex;
  gap: 10rpx;
  flex-wrap: wrap;
}

.constitution-tag {
  font-size: 26rpx;
  padding: 8rpx 16rpx;
  background: #f0f5ff;
  color: #597ef7;
  border-radius: 20rpx;
}

.constitution-benefit {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
  padding: 15rpx;
  background: #f8f9ff;
  border-radius: 12rpx;
}

.acupoint-image {
  width: 100%;
  height: 400rpx;
  border-radius: 12rpx;
}
</style>
