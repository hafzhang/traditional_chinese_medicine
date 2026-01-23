<template>
  <view class="acupoint-detail-page">
    <scroll-view class="detail-scroll" scroll-y>
      <!-- 头部大图 -->
      <view class="hero-image-wrapper">
        <image 
          :src="acupoint.image_url || '/static/acupoints/default_detail.png'" 
          mode="aspectFill" 
          class="hero-image"
          @click="previewImage"
        />
        <view class="image-overlay"></view>
        <view class="header-content">
          <view class="acupoint-name-large">{{ acupoint.name }}</view>
          <view class="acupoint-meta">
            <text class="meta-tag">{{ acupoint.code }}</text>
            <text class="meta-tag">{{ acupoint.meridian }}</text>
          </view>
        </view>
      </view>

      <!-- 功能入口栏 -->
      <view class="feature-bar">
        <view class="feature-item" @click="show3DModel">
          <view class="feature-icon-box blue">
            <text class="feature-icon">🧊</text>
          </view>
          <text class="feature-label">3D图解</text>
        </view>
        <view class="feature-item" @click="showARMode">
          <view class="feature-icon-box purple">
            <text class="feature-icon">📷</text>
          </view>
          <text class="feature-label">AR取穴</text>
        </view>
        <view class="feature-item" @click="openTimer">
          <view class="feature-icon-box green">
            <text class="feature-icon">⏱️</text>
          </view>
          <text class="feature-label">按摩计时</text>
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
            <text class="location-text highlight">{{ acupoint.simple_location }}</text>
          </view>
          <view class="detail-location" v-if="acupoint.location">
            <text class="location-label">标准定位：</text>
            <text class="location-text">{{ acupoint.location }}</text>
          </view>
          <view class="detail-location" v-if="acupoint.body_part">
             <text class="location-label">所属部位：</text>
             <text class="location-text">{{ acupoint.body_part }}</text>
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
          <!-- 默认建议 -->
          <view class="massage-tips">
            <text class="tip-icon">💡</text>
            <text>建议每次按摩3-5分钟，力度以产生酸胀感为宜。</text>
          </view>
        </view>
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
        </view>
      </view>
      
      <!-- 底部留白 -->
      <view style="height: 100rpx;"></view>
    </scroll-view>

    <!-- 计时器弹窗 -->
    <view class="timer-modal" v-if="showTimerModal">
      <view class="timer-mask" @click="closeTimer"></view>
      <view class="timer-content">
        <view class="timer-header">
          <text>按摩计时</text>
          <view class="close-btn" @click="closeTimer">×</view>
        </view>
        <view class="timer-display">
          <text class="time-text">{{ formatTime(timeLeft) }}</text>
        </view>
        <view class="timer-controls">
          <button class="timer-btn reset" @click="resetTimer">重置</button>
          <button class="timer-btn toggle" :class="{ active: timerRunning }" @click="toggleTimer">
            {{ timerRunning ? '暂停' : '开始' }}
          </button>
        </view>
        <view class="timer-presets">
          <view class="preset-chip" @click="setTimer(60)">1分钟</view>
          <view class="preset-chip" @click="setTimer(180)">3分钟</view>
          <view class="preset-chip" @click="setTimer(300)">5分钟</view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getAcupointDetail } from '@/api/acupoints.js'

const acupoint = ref({})
const showTimerModal = ref(false)
const timerRunning = ref(false)
const timeLeft = ref(180) // 默认3分钟
let timerInterval = null

// 映射字典
const constitutionMap = {
  'yang_deficiency': '阳虚质',
  'yin_deficiency': '阴虚质',
  'qi_deficiency': '气虚质',
  'phlegm_dampness': '痰湿质',
  'damp_heat': '湿热质',
  'blood_stasis': '血瘀质',
  'qi_stagnation': '气郁质',
  'special': '特禀质',
  'peace': '平和质'
}

onLoad((options) => {
  if (options.id) {
    loadDetail(options.id)
  }
})

onUnmounted(() => {
  stopTimer()
})

async function loadDetail(id) {
  try {
    const res = await getAcupointDetail(id)
    if (res.code === 0) {
      acupoint.value = res.data
    }
  } catch (error) {
    console.error('Failed to load detail:', error)
    uni.showToast({ title: '加载失败', icon: 'none' })
  }
}

function getConstitutionName(code) {
  return constitutionMap[code] || code
}

function previewImage() {
  if (acupoint.value.image_url) {
    uni.previewImage({
      urls: [acupoint.value.image_url]
    })
  }
}

// 功能入口
function show3DModel() {
  uni.showToast({
    title: '3D模型加载中...\n(演示功能)',
    icon: 'none',
    duration: 2000
  })
}

function showARMode() {
  uni.showToast({
    title: 'AR功能开发中\n请期待后续版本',
    icon: 'none',
    duration: 2000
  })
}

// 计时器逻辑
function openTimer() {
  showTimerModal.value = true
}

function closeTimer() {
  showTimerModal.value = false
  stopTimer()
}

function toggleTimer() {
  if (timerRunning.value) {
    stopTimer()
  } else {
    startTimer()
  }
}

function startTimer() {
  if (timeLeft.value <= 0) return
  
  timerRunning.value = true
  timerInterval = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
    } else {
      stopTimer()
      uni.vibrateLong() // 震动提醒
      uni.showToast({ title: '按摩完成', icon: 'success' })
    }
  }, 1000)
}

function stopTimer() {
  timerRunning.value = false
  if (timerInterval) {
    clearInterval(timerInterval)
    timerInterval = null
  }
}

function resetTimer() {
  stopTimer()
  timeLeft.value = 180
}

function setTimer(seconds) {
  stopTimer()
  timeLeft.value = seconds
}

function formatTime(seconds) {
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
}
</script>

<style lang="scss">
.acupoint-detail-page {
  height: 100vh;
  background-color: #f5f7fa;
}

.detail-scroll {
  height: 100%;
}

/* 头部大图 */
.hero-image-wrapper {
  height: 500rpx;
  position: relative;
  background-color: #333;
  
  .hero-image {
    width: 100%;
    height: 100%;
    opacity: 0.9;
  }
  
  .image-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(to bottom, rgba(0,0,0,0) 60%, rgba(0,0,0,0.7));
  }
  
  .header-content {
    position: absolute;
    bottom: 40rpx;
    left: 30rpx;
    right: 30rpx;
    color: #fff;
    
    .acupoint-name-large {
      font-size: 56rpx;
      font-weight: bold;
      margin-bottom: 16rpx;
      text-shadow: 0 2rpx 4rpx rgba(0,0,0,0.3);
    }
    
    .acupoint-meta {
      display: flex;
      gap: 20rpx;
      
      .meta-tag {
        background-color: rgba(255,255,255,0.2);
        backdrop-filter: blur(4px);
        padding: 4rpx 16rpx;
        border-radius: 8rpx;
        font-size: 24rpx;
        border: 1rpx solid rgba(255,255,255,0.3);
      }
    }
  }
}

/* 功能栏 */
.feature-bar {
  display: flex;
  justify-content: space-around;
  padding: 30rpx 20rpx;
  background-color: #fff;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 10rpx rgba(0,0,0,0.05);
  
  .feature-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12rpx;
    
    .feature-icon-box {
      width: 90rpx;
      height: 90rpx;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: #f0f2f5;
      
      &.blue { background-color: #e6f7ff; color: #1890ff; }
      &.purple { background-color: #f9f0ff; color: #722ed1; }
      &.green { background-color: #f6ffed; color: #52c41a; }
      
      .feature-icon {
        font-size: 40rpx;
      }
    }
    
    .feature-label {
      font-size: 24rpx;
      color: #666;
    }
  }
}

/* 信息卡片 */
.info-card {
  background-color: #fff;
  margin: 20rpx;
  padding: 30rpx;
  border-radius: 16rpx;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.02);
  
  .card-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 24rpx;
    display: flex;
    align-items: center;
    gap: 12rpx;
    
    .title-icon {
      font-size: 36rpx;
    }
  }
}

.location-content {
  .simple-location, .detail-location {
    margin-bottom: 16rpx;
    line-height: 1.6;
    
    .location-label {
      color: #999;
      font-size: 28rpx;
    }
    
    .location-text {
      color: #333;
      font-size: 28rpx;
      
      &.highlight {
        color: #2b9939;
        font-weight: 500;
      }
    }
  }
}

.efficacy-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
  
  .efficacy-item {
    background-color: #f0f9eb;
    color: #2b9939;
    font-size: 26rpx;
    padding: 8rpx 20rpx;
    border-radius: 30rpx;
  }
}

.indications-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
  
  .indication-tag {
    background-color: #f4f4f5;
    color: #666;
    font-size: 26rpx;
    padding: 8rpx 20rpx;
    border-radius: 8rpx;
  }
}

.massage-info {
  .massage-item {
    margin-bottom: 16rpx;
    font-size: 28rpx;
    
    .massage-label { color: #999; }
    .massage-text { color: #333; }
  }
  
  .massage-tips {
    background-color: #fffbe6;
    border: 1rpx solid #ffe58f;
    padding: 20rpx;
    border-radius: 8rpx;
    font-size: 26rpx;
    color: #d48806;
    display: flex;
    gap: 10rpx;
    margin-top: 20rpx;
  }
}

.constitutions {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
  
  .constitution-tag {
    border: 1rpx solid #2b9939;
    color: #2b9939;
    font-size: 24rpx;
    padding: 4rpx 16rpx;
    border-radius: 4rpx;
  }
}

/* 计时器弹窗 */
.timer-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;
  
  .timer-mask {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0,0,0,0.6);
  }
  
  .timer-content {
    position: relative;
    width: 600rpx;
    background-color: #fff;
    border-radius: 24rpx;
    padding: 40rpx;
    display: flex;
    flex-direction: column;
    align-items: center;
    
    .timer-header {
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 40rpx;
      font-size: 32rpx;
      font-weight: bold;
      
      .close-btn {
        font-size: 40rpx;
        color: #999;
        padding: 10rpx;
      }
    }
    
    .timer-display {
      font-size: 80rpx;
      font-weight: bold;
      color: #333;
      font-family: monospace;
      margin-bottom: 60rpx;
    }
    
    .timer-controls {
      display: flex;
      gap: 30rpx;
      width: 100%;
      margin-bottom: 40rpx;
      
      .timer-btn {
        flex: 1;
        height: 88rpx;
        border-radius: 44rpx;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32rpx;
        
        &.reset {
          background-color: #f5f5f5;
          color: #666;
        }
        
        &.toggle {
          background-color: #2b9939;
          color: #fff;
          
          &.active {
            background-color: #ff4d4f; // 暂停/停止色
          }
        }
      }
    }
    
    .timer-presets {
      display: flex;
      gap: 20rpx;
      
      .preset-chip {
        padding: 10rpx 30rpx;
        background-color: #f0f2f5;
        border-radius: 30rpx;
        font-size: 24rpx;
        color: #666;
        
        &:active {
          background-color: #e6f7ff;
          color: #1890ff;
        }
      }
    }
  }
}
</style>
