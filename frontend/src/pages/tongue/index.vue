<template>
  <view class="tongue-page">
    <!-- 顶部说明 -->
    <view class="header-section">
      <view class="title">AI 舌诊分析</view>
      <view class="subtitle">拍摄舌象照片，选择特征，AI 分析您的体质倾向</view>
    </view>

    <!-- 拍照区域 -->
    <view class="photo-section">
      <view class="photo-area" @click="takePhoto">
        <image v-if="imageUrl" :src="imageUrl" class="preview-image" mode="aspectFill" />
        <view v-else class="photo-placeholder">
          <text class="placeholder-icon">📷</text>
          <text class="placeholder-text">点击拍摄舌象照片</text>
        </view>
      </view>
    </view>

    <!-- 特征选择区域 -->
    <view class="features-section">
      <view class="section-title">请选择舌象特征</view>

      <!-- 舌质颜色 -->
      <view class="feature-group">
        <view class="feature-label">舌质颜色</view>
        <view class="feature-options">
          <view
            v-for="option in tongueColors"
            :key="option.value"
            class="feature-option"
            :class="{ active: formData.tongue_color === option.value }"
            @click="selectFeature('tongue_color', option.value)"
          >
            {{ option.label }}
          </view>
        </view>
      </view>

      <!-- 舌质形态 -->
      <view class="feature-group">
        <view class="feature-label">舌质形态</view>
        <view class="feature-options">
          <view
            v-for="option in tongueShapes"
            :key="option.value"
            class="feature-option"
            :class="{ active: formData.tongue_shape === option.value }"
            @click="selectFeature('tongue_shape', option.value)"
          >
            {{ option.label }}
          </view>
        </view>
      </view>

      <!-- 苔色 -->
      <view class="feature-group">
        <view class="feature-label">苔色</view>
        <view class="feature-options">
          <view
            v-for="option in coatingColors"
            :key="option.value"
            class="feature-option"
            :class="{ active: formData.coating_color === option.value }"
            @click="selectFeature('coating_color', option.value)"
          >
            {{ option.label }}
          </view>
        </view>
      </view>

      <!-- 苔质 -->
      <view class="feature-group">
        <view class="feature-label">苔质</view>
        <view class="feature-options">
          <view
            v-for="option in coatingThickness"
            :key="option.value"
            class="feature-option"
            :class="{ active: formData.coating_thickness === option.value }"
            @click="selectFeature('coating_thickness', option.value)"
          >
            {{ option.label }}
          </view>
        </view>
      </view>
    </view>

    <!-- 分析按钮 -->
    <view class="action-section">
      <button class="analyze-btn" :disabled="!canAnalyze" @click="handleAnalyze">
        {{ analyzing ? '分析中...' : '开始分析' }}
      </button>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { analyzeTongue, getTongueOptions } from '@/api/tongue.js'

// 表单数据
const formData = ref({
  tongue_color: '',
  tongue_shape: '',
  coating_color: '',
  coating_thickness: ''
})

// 图片
const imageUrl = ref('')

// 选项数据
const tongueColors = ref([])
const tongueShapes = ref([])
const coatingColors = ref([])
const coatingThickness = ref([])

// 分析状态
const analyzing = ref(false)

// 测试结果ID（从URL获取）
const resultId = ref('')

// 是否可以分析
const canAnalyze = computed(() => {
  return formData.value.tongue_color &&
         formData.value.tongue_shape &&
         formData.value.coating_color &&
         formData.value.coating_thickness
})

onLoad((options) => {
  if (options.resultId) {
    resultId.value = options.resultId
  }
  loadOptions()
})

async function loadOptions() {
  try {
    const res = await getTongueOptions()
    if (res.code === 0) {
      tongueColors.value = res.data.tongue_colors
      tongueShapes.value = res.data.tongue_shapes
      coatingColors.value = res.data.coating_colors
      coatingThickness.value = res.data.coating_thickness
    }
  } catch (e) {
    console.error('加载选项失败', e)
  }
}

function selectFeature(key, value) {
  formData.value[key] = value
}

function takePhoto() {
  uni.chooseImage({
    count: 1,
    sizeType: ['compressed'],
    sourceType: ['camera', 'album'],
    success: (res) => {
      imageUrl.value = res.tempFilePaths[0]
    }
  })
}

async function handleAnalyze() {
  if (!canAnalyze.value) return

  analyzing.value = true

  try {
    // TODO: 实际应该先上传图片获取URL
    const data = {
      ...formData.value,
      result_id: resultId.value
    }

    const res = await analyzeTongue(data)

    if (res.code === 0) {
      // 跳转到结果页
      uni.navigateTo({
        url: `/pages/tongue/result?data=${encodeURIComponent(JSON.stringify(res.data))}`
      })
    }
  } catch (e) {
    console.error('分析失败', e)
    uni.showToast({
      title: '分析失败',
      icon: 'none'
    })
  } finally {
    analyzing.value = false
  }
}
</script>

<style lang="scss" scoped>
.tongue-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 40rpx;
}

.header-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 50rpx 30rpx;
  color: #fff;
  text-align: center;
}

.title {
  font-size: 40rpx;
  font-weight: bold;
  margin-bottom: 15rpx;
}

.subtitle {
  font-size: 26rpx;
  opacity: 0.9;
}

.photo-section {
  padding: 30rpx;
}

.photo-area {
  width: 100%;
  height: 400rpx;
  background: #fff;
  border-radius: 20rpx;
  overflow: hidden;
}

.preview-image {
  width: 100%;
  height: 100%;
}

.photo-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f8f9ff;
}

.placeholder-icon {
  font-size: 100rpx;
  margin-bottom: 20rpx;
}

.placeholder-text {
  font-size: 28rpx;
  color: #999;
}

.features-section {
  padding: 0 30rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 30rpx;
}

.feature-group {
  background: #fff;
  border-radius: 16rpx;
  padding: 25rpx;
  margin-bottom: 20rpx;
}

.feature-label {
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 20rpx;
}

.feature-options {
  display: flex;
  gap: 15rpx;
  flex-wrap: wrap;
}

.feature-option {
  padding: 12rpx 24rpx;
  background: #f5f5f5;
  border-radius: 30rpx;
  font-size: 26rpx;
  color: #666;
  transition: all 0.3s;

  &.active {
    background: #667eea;
    color: #fff;
  }
}

.action-section {
  padding: 30rpx;
}

.analyze-btn {
  width: 100%;
  height: 90rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 32rpx;
  font-weight: bold;
  border-radius: 45rpx;
  border: none;

  &:disabled {
    background: #ccc;
  }
}
</style>
