<template>
  <view class="api-test-page">
    <view class="header">
      <text class="title">API 连接测试</text>
    </view>

    <view class="section">
      <text class="section-title">基础信息</text>
      <view class="info-item">
        <text class="label">环境:</text>
        <text class="value">{{ isDev ? '开发环境' : '生产环境' }}</text>
      </view>
      <view class="info-item">
        <text class="label">平台:</text>
        <text class="value">{{ platform }}</text>
      </view>
      <view class="info-item">
        <text class="label">BASE_URL:</text>
        <text class="value">{{ baseUrl }}</text>
      </view>
    </view>

    <view class="section">
      <text class="section-title">最近请求</text>
      <view class="info-box" v-if="lastRequest">
        <text class="info-text">{{ lastRequest.method }} {{ lastRequest.url }}</text>
        <text class="info-time">{{ lastRequest.time }}</text>
      </view>
      <text class="empty-text" v-else>暂无请求记录</text>
    </view>

    <view class="section">
      <text class="section-title">最近响应</text>
      <view class="info-box" v-if="lastResponse">
        <text class="info-text">Status: {{ lastResponse.status }}</text>
        <text class="info-text">{{ JSON.stringify(lastResponse.data).substring(0, 200) }}...</text>
        <text class="info-time">{{ lastResponse.time }}</text>
      </view>
      <text class="empty-text" v-else>暂无响应记录</text>
    </view>

    <view class="section">
      <text class="section-title">最近错误</text>
      <view class="error-box" v-if="lastError">
        <text class="error-text">{{ lastError.msg || '未知错误' }}</text>
        <text class="info-time">{{ lastError.time }}</text>
      </view>
      <text class="empty-text" v-else>暂无错误记录</text>
    </view>

    <view class="section">
      <text class="section-title">测试操作</text>
      <view class="button-group">
        <button class="test-btn" @click="testMeridians">测试经络列表</button>
        <button class="test-btn" @click="testAcupoints">测试穴位列表</button>
        <button class="test-btn" @click="testBodyParts">测试部位列表</button>
      </view>
    </view>

    <view class="section" v-if="testResults.length > 0">
      <text class="section-title">测试结果</text>
      <view class="result-item" v-for="(result, index) in testResults" :key="index" :class="result.success ? 'success' : 'error'">
        <text class="result-name">{{ result.name }}</text>
        <text class="result-status">{{ result.success ? '✓ 成功' : '✗ 失败' }}</text>
        <text class="result-detail" v-if="result.data">数据: {{ JSON.stringify(result.data).substring(0, 100) }}...</text>
        <text class="result-error" v-if="result.error">错误: {{ result.error }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { getMeridians, getAcupointsList, getBodyParts } from '@/api/acupoints.js'

const isDev = ref(import.meta.env.DEV)
const platform = ref('')
const baseUrl = ref('')
const lastRequest = ref(null)
const lastResponse = ref(null)
const lastError = ref(null)
const testResults = ref([])

onMounted(() => {
  // @ts-ignore
  platform.value = uni.getSystemInfoSync().platform

  // Get BASE_URL from request module
  if (typeof window !== 'undefined') {
    baseUrl.value = window.location.origin
  } else {
    baseUrl.value = 'http://localhost:8000 (小程序环境)'
  }

  // Check for debug info
  checkDebugInfo()

  // Set up interval to check debug info
  debugInterval.value = setInterval(checkDebugInfo, 1000)
})

const debugInterval = ref(null)

onUnmounted(() => {
  if (debugInterval.value) {
    clearInterval(debugInterval.value)
  }
})

function checkDebugInfo() {
  // @ts-ignore
  if (typeof window !== 'undefined') {
    // @ts-ignore
    if (window.__LAST_REQUEST__) {
      // @ts-ignore
      lastRequest.value = window.__LAST_REQUEST__
    }
    // @ts-ignore
    if (window.__LAST_RESPONSE__) {
      // @ts-ignore
      lastResponse.value = window.__LAST_RESPONSE__
    }
    // @ts-ignore
    if (window.__LAST_ERROR__) {
      // @ts-ignore
      lastError.value = window.__LAST_ERROR__
    }
  }
}

async function testMeridians() {
  try {
    console.log('[Test] Calling getMeridians()...')
    const res = await getMeridians()
    console.log('[Test] Response:', res)

    testResults.value.unshift({
      name: '经络列表',
      success: true,
      data: res.data
    })

    // Keep only last 5 results
    if (testResults.value.length > 5) {
      testResults.value = testResults.value.slice(0, 5)
    }
  } catch (error) {
    console.error('[Test] Error:', error)
    testResults.value.unshift({
      name: '经络列表',
      success: false,
      error: error.message || String(error)
    })
  }
}

async function testAcupoints() {
  try {
    console.log('[Test] Calling getAcupointsList()...')
    const res = await getAcupointsList({ limit: 5 })
    console.log('[Test] Response:', res)

    testResults.value.unshift({
      name: '穴位列表',
      success: true,
      data: res.data
    })

    if (testResults.value.length > 5) {
      testResults.value = testResults.value.slice(0, 5)
    }
  } catch (error) {
    console.error('[Test] Error:', error)
    testResults.value.unshift({
      name: '穴位列表',
      success: false,
      error: error.message || String(error)
    })
  }
}

async function testBodyParts() {
  try {
    console.log('[Test] Calling getBodyParts()...')
    const res = await getBodyParts()
    console.log('[Test] Response:', res)

    testResults.value.unshift({
      name: '部位列表',
      success: true,
      data: res.data
    })

    if (testResults.value.length > 5) {
      testResults.value = testResults.value.slice(0, 5)
    }
  } catch (error) {
    console.error('[Test] Error:', error)
    testResults.value.unshift({
      name: '部位列表',
      success: false,
      error: error.message || String(error)
    })
  }
}
</script>

<style lang="scss" scoped>
.api-test-page {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20rpx;
}

.header {
  padding: 30rpx 0;
  text-align: center;

  .title {
    font-size: 40rpx;
    font-weight: bold;
    color: #333;
  }
}

.section {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;

  .section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 20rpx;
    display: block;
  }
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 15rpx 0;
  border-bottom: 1rpx solid #f0f0f0;

  .label {
    color: #666;
    font-size: 28rpx;
  }

  .value {
    color: #333;
    font-size: 28rpx;
    font-weight: 500;
  }
}

.info-box, .error-box {
  background-color: #f8f8f8;
  padding: 20rpx;
  border-radius: 8rpx;

  .info-text, .error-text {
    display: block;
    font-size: 26rpx;
    color: #333;
    margin-bottom: 10rpx;
    word-break: break-all;
  }

  .info-time {
    display: block;
    font-size: 24rpx;
    color: #999;
  }
}

.error-box {
  background-color: #fee;

  .error-text {
    color: #d32f2f;
  }
}

.empty-text {
  display: block;
  text-align: center;
  color: #999;
  font-size: 28rpx;
  padding: 40rpx 0;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.test-btn {
  background-color: #2b9939;
  color: #fff;
  border: none;
  border-radius: 8rpx;
  padding: 25rpx;
  font-size: 30rpx;
}

.result-item {
  background-color: #f8f8f8;
  padding: 20rpx;
  border-radius: 8rpx;
  margin-bottom: 15rpx;

  &.success {
    background-color: #e8f5e9;
    border-left: 4rpx solid #4caf50;
  }

  &.error {
    background-color: #ffebee;
    border-left: 4rpx solid #f44336;
  }

  .result-name {
    display: block;
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 10rpx;
  }

  .result-status {
    display: block;
    font-size: 26rpx;
    margin-bottom: 10rpx;
  }

  .result-detail {
    display: block;
    font-size: 24rpx;
    color: #666;
    word-break: break-all;
  }

  .result-error {
    display: block;
    font-size: 24rpx;
    color: #d32f2f;
  }
}
</style>
