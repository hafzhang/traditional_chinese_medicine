<template>
  <view class="acupoint-detail">
    <!-- 导航栏 -->
    <view class="navbar">
      <view class="back" @click="goBack">←</view>
      <text class="title">穴位详情</text>
    </view>

    <!-- 穴位图片 -->
    <view class="image-section">
      <image
        :src="acupoint.image_url || '/static/acupoints/default.png'"
        mode="aspectFit"
        class="acupoint-image"
        @click="previewImage"
      />
    </view>

    <!-- 基本信息 -->
    <view class="info-section">
      <view class="name-row">
        <text class="name">{{ acupoint.name }}</text>
        <text class="code" v-if="acupoint.code">({{ acupoint.code }})</text>
      </view>
      <view class="meta-row">
        <text class="meridian">{{ acupoint.meridian }}</text>
        <text class="five-element" v-if="acupoint.five_element">· {{ acupoint.five_element }}</text>
      </view>
      <view class="aliases" v-if="acupoint.aliases && acupoint.aliases.length">
        <text class="alias-label">别名：</text>
        <text class="alias-text">{{ acupoint.aliases.join('、') }}</text>
      </view>
    </view>

    <!-- 穴位释义 -->
    <view class="detail-section" v-if="acupoint.explanation">
      <view class="section-title">【穴位释义】</view>
      <view class="content-text">{{ acupoint.explanation }}</view>
    </view>

    <!-- 定位描述 -->
    <view class="detail-section" v-if="acupoint.location">
      <view class="section-title">【定位取穴】</view>
      <view class="content-text">{{ acupoint.location }}</view>
      <view class="simple-location" v-if="acupoint.simple_location">
        <text class="label">简易取穴：</text>
        <text>{{ acupoint.simple_location }}</text>
      </view>
    </view>

    <!-- 功效与功能 -->
    <view class="detail-section" v-if="acupoint.functions">
      <view class="section-title">【功效功能】</view>
      <view class="content-text">{{ acupoint.functions }}</view>
    </view>

    <!-- 主治病症 -->
    <view class="detail-section" v-if="acupoint.indications && acupoint.indications.length">
      <view class="section-title">【主治病症】</view>
      <view class="tags-list">
        <text class="tag" v-for="(item, index) in acupoint.indications" :key="index">{{ item }}</text>
      </view>
    </view>

    <!-- 操作方法 -->
    <view class="detail-section">
      <view class="section-title">【操作方法】</view>

      <!-- 按摩方法 -->
      <view class="method-item" v-if="acupoint.massage_method">
        <view class="method-label">💆 按摩：</view>
        <view class="method-content">{{ acupoint.massage_method }}</view>
      </view>

      <!-- 灸法 -->
      <view class="method-item" v-if="acupoint.moxibustion_method">
        <view class="method-label">🔥 灸法：</view>
        <view class="method-content">{{ acupoint.moxibustion_method }}</view>
      </view>
    </view>

    <!-- 解剖结构 -->
    <view class="detail-section" v-if="acupoint.anatomical_structure">
      <view class="section-title">【解剖结构】</view>
      <view class="content-text">{{ acupoint.anatomical_structure }}</view>
    </view>

    <!-- 主要配伍 -->
    <view class="detail-section" v-if="acupoint.combinations">
      <view class="section-title">【主要配伍】</view>
      <view class="content-text combinations-text">{{ acupoint.combinations }}</view>
    </view>

    <!-- 经络 GIF 动画 -->
    <view class="meridian-section" v-if="meridianGifUrl">
      <view class="section-title">【经络循行】</view>
      <image
        :src="meridianGifUrl"
        mode="aspectFit"
        class="meridian-gif"
      />
      <view class="meridian-desc">{{ meridianDescription }}</view>
    </view>

    <!-- 体质关联 -->
    <view class="detail-section" v-if="acupoint.suitable_constitutions && acupoint.suitable_constitutions.length">
      <view class="section-title">【适用体质】</view>
      <view class="tags-list">
        <text class="tag constitution" v-for="code in acupoint.suitable_constitutions" :key="code">
          {{ getConstitutionName(code) }}
        </text>
      </view>
    </view>

    <!-- 按摩计时器 -->
    <view class="timer-section">
      <view class="timer-btn" @click="openTimer">
        <text class="timer-icon">⏱️</text>
        <text>按摩计时器</text>
      </view>
    </view>
  </view>

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
</template>

<script setup>
import { ref, onUnmounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getAcupointDetail } from '@/api/acupoints.js'

const acupoint = ref({})
const meridianGifUrl = ref('')
const meridianDescription = ref('')
const showTimerModal = ref(false)
const timerRunning = ref(false)
const timeLeft = ref(180)
let timerInterval = null

// 体质映射
const constitutionMap = {
  'yang_deficiency': '阳虚质',
  'yin_deficiency': '阴虚质',
  'qi_deficiency': '气虚质',
  'phlegm_damp': '痰湿质',
  'damp_heat': '湿热质',
  'blood_stasis': '血瘀质',
  'qi_depression': '气郁质',
  'special': '特禀质',
  'peace': '平和质'
}

// 经络描述映射
const meridianDescriptions = {
  '手太阴肺经': '起于中焦，下络大肠，还循胃口，上膈属肺。从肺系横出腋下，沿上臂内侧下行，止于拇指桡侧端。',
  '手阳明大肠经': '起于食指桡侧端，沿食指内间、第1掌骨之间上行，沿上臂外侧前缘，上肩，至颈部，入下齿中。',
  '足阳明胃经': '起于鼻翼两侧，上行至鼻根部，沿鼻外侧下行，入上齿中，环绕口唇，交会承浆，沿发际上行至额前。',
  '足太阴脾经': '起于足大趾内侧端，沿足内侧、小腿内侧、大腿内侧前缘上行，入腹，属脾，络胃，上膈，挟咽，连舌本，散舌下。',
  '手少阴心经': '起于心中，下络小肠，上挟咽，系目系。从心系上肺，横出腋下，沿上臂内侧后缘下行，止于小指桡侧端。',
  '手太阳小肠经': '起于小指尺侧端，沿手背、上臂外侧后缘上行，绕肩胛，交肩上，入缺盆，络心，抵胃，属小肠。',
  '足太阳膀胱经': '起于内眼角，上行额部，交会于头顶。从头顶下行，沿后头部、后背、腰部、下肢后外侧，止于小趾外侧端。',
  '足少阴肾经': '起于足小趾下，斜向足心，沿足内侧、下肢内侧后缘上行，属肾，络膀胱，上达肝，入肺，沿喉咙，挟舌本。',
  '手厥阴心包经': '起于胸中，属心包，下膈，络三焦。从胸出胁部，沿上臂内侧中线下行，止于中指指尖。',
  '手少阳三焦经': '起于无名指尺侧端，沿手背、上臂外侧中线上行，绕肩颈部，耳后，止于眉梢凹陷处。',
  '足少阳胆经': '起于外眼角，上行至额角，下行至耳后，沿颈部、肩部、胁肋部、下肢外侧中线，止于第4趾外侧端。',
  '足厥阴肝经': '起于足大趾丛毛之际，沿足背、下肢内侧前缘上行，绕阴器，属肝，络胆，上贯膈，布胁肋，上达头顶。',
  '督脉': '起于胞中，下出会阴，沿脊柱上行，至项后风府穴，进入脑内，上行巅顶，沿前额下行鼻柱。',
  '任脉': '起于胞中，下出会阴，经阴阜，沿腹部和胸部正中线上行，至颏部，上行至眼眶。'
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
      // 设置经络 GIF
      setMeridianInfo(res.data.meridian)
    }
  } catch (error) {
    console.error('Failed to load detail:', error)
    uni.showToast({ title: '加载失败', icon: 'none' })
  }
}

function setMeridianInfo(meridian) {
  if (!meridian) return

  // 设置 GIF URL
  meridianGifUrl.value = `/static/acupoints/meridians/${meridian}.gif`
  // 设置经络描述
  meridianDescription.value = meridianDescriptions[meridian] || ''
}

function getConstitutionName(code) {
  return constitutionMap[code] || code
}

function goBack() {
  uni.navigateBack()
}

function previewImage() {
  if (acupoint.value.image_url) {
    uni.previewImage({
      urls: [acupoint.value.image_url]
    })
  }
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
      uni.vibrateLong()
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
.acupoint-detail {
  background: #f5f5f5;
  min-height: 100vh;
  padding-bottom: 40rpx;
}

/* 导航栏 */
.navbar {
  height: 88rpx;
  background: #fff;
  display: flex;
  align-items: center;
  padding: 0 30rpx;
  border-bottom: 1rpx solid #eee;
  position: sticky;
  top: 0;
  z-index: 100;

  .back {
    font-size: 40rpx;
    color: #333;
    width: 60rpx;
  }

  .title {
    flex: 1;
    text-align: center;
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    padding-right: 60rpx;
  }
}

/* 图片区域 */
.image-section {
  background: #fff;
  padding: 40rpx;
  text-align: center;

  .acupoint-image {
    width: 400rpx;
    height: 400rpx;
    border-radius: 16rpx;
    background: #f8f8f8;
  }
}

/* 基本信息 */
.info-section {
  background: #fff;
  padding: 30rpx;
  text-align: center;
  margin-bottom: 20rpx;

  .name-row {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 10rpx;

    .name {
      font-size: 48rpx;
      font-weight: bold;
      color: #333;
    }

    .code {
      font-size: 28rpx;
      color: #999;
      margin-left: 10rpx;
    }
  }

  .meta-row {
    font-size: 28rpx;
    color: #1acc76;
    margin-bottom: 10rpx;

    .meridian {
      font-weight: 500;
    }

    .five-element {
      color: #666;
    }
  }

  .aliases {
    font-size: 24rpx;
    color: #999;

    .alias-label {
      color: #666;
    }

    .alias-text {
      color: #999;
    }
  }
}

/* 详情区块 */
.detail-section {
  background: #fff;
  padding: 30rpx;
  margin-bottom: 20rpx;

  .section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 20rpx;
  }

  .content-text {
    font-size: 28rpx;
    color: #666;
    line-height: 1.8;
  }

  .simple-location {
    margin-top: 15rpx;
    padding: 15rpx;
    background: #f0f9eb;
    border-radius: 8rpx;

    .label {
      color: #1acc76;
      font-weight: 500;
    }
  }

  .tags-list {
    display: flex;
    flex-wrap: wrap;
    gap: 15rpx;

    .tag {
      background: #f0f2f5;
      color: #666;
      font-size: 26rpx;
      padding: 8rpx 20rpx;
      border-radius: 8rpx;

      &.constitution {
        background: #e6f7ff;
        color: #1890ff;
        border: 1rpx solid #91d5ff;
      }
    }
  }

  .method-item {
    margin-bottom: 20rpx;

    &:last-child {
      margin-bottom: 0;
    }

    .method-label {
      font-size: 28rpx;
      font-weight: 500;
      color: #333;
      margin-bottom: 10rpx;
    }

    .method-content {
      font-size: 26rpx;
      color: #666;
      line-height: 1.8;
      padding-left: 20rpx;
    }
  }
}

/* 经络区块 */
.meridian-section {
  background: #fff;
  padding: 30rpx;
  margin-bottom: 20rpx;

  .section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 20rpx;
  }

  .meridian-gif {
    width: 100%;
    height: 300rpx;
    background: #f5f5f5;
    border-radius: 16rpx;
    margin-bottom: 20rpx;
  }

  .meridian-desc {
    font-size: 26rpx;
    color: #666;
    line-height: 1.8;
  }
}

/* 计时器区域 */
.timer-section {
  padding: 0 30rpx;

  .timer-btn {
    background: linear-gradient(135deg, #1acc76 0%, #16a750 100%);
    color: #fff;
    font-size: 32rpx;
    padding: 30rpx;
    border-radius: 50rpx;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15rpx;
    box-shadow: 0 8rpx 24rpx rgba(26, 204, 118, 0.3);

    .timer-icon {
      font-size: 40rpx;
    }
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
    background-color: rgba(0, 0, 0, 0.6);
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

      .time-text {
        color: #1acc76;
      }
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
          background-color: #1acc76;
          color: #fff;

          &.active {
            background-color: #ff4d4f;
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
