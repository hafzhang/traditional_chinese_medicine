<template>
  <view class="tongue-result-page">
    <!-- 分析结果头部 -->
    <view class="result-header">
      <view class="constitution-icon">👅</view>
      <view class="result-title">舌诊分析结果</view>
      <view class="constitution-name">{{ analysis.constitution_name }}</view>
      <view class="confidence">
        置信度：{{ analysis.confidence }}%
      </view>
    </view>

    <!-- 舌象特征 -->
    <view class="info-card">
      <view class="card-title">
        <text class="title-icon">🔍</text>
        舌象特征
      </view>
      <view class="feature-list">
        <view class="feature-row">
          <text class="feature-label">舌质颜色：</text>
          <text class="feature-value">{{ features.tongue_color }}</text>
        </view>
        <view class="feature-row">
          <text class="feature-label">舌质形态：</text>
          <text class="feature-value">{{ features.tongue_shape }}</text>
        </view>
        <view class="feature-row">
          <text class="feature-label">苔色：</text>
          <text class="feature-value">{{ features.coating_color }}</text>
        </view>
        <view class="feature-row">
          <text class="feature-label">苔质：</text>
          <text class="feature-value">{{ features.coating_thickness }}</text>
        </view>
      </view>
    </view>

    <!-- 对比结果 -->
    <view class="info-card" v-if="comparison">
      <view class="card-title">
        <text class="title-icon">⚖️</text>
        与测试结果对比
      </view>
      <view class="comparison-content">
        <view class="comparison-status" :class="{ consistent: comparison.is_consistent }">
          <text class="status-icon">{{ comparison.is_consistent ? '✓' : '⚠' }}</text>
          <text class="status-text">{{ comparison.is_consistent ? '结果一致' : '存在差异' }}</text>
        </view>
        <view class="comparison-detail">
          <text class="detail-label">舌诊体质：</text>
          <text class="detail-value">{{ comparison.tongue_constitution_name }}</text>
        </view>
        <view class="comparison-detail">
          <text class="detail-label">测试体质：</text>
          <text class="detail-value">{{ comparison.test_constitution_name }}</text>
        </view>
        <view class="comparison-message">{{ comparison.message }}</view>
      </view>
    </view>

    <!-- 调理建议 -->
    <view class="info-card">
      <view class="card-title">
        <text class="title-icon">💡</text>
        调理建议
      </view>
      <view class="advice-content">
        <view class="advice-item">
          <view class="advice-label">
            <text class="label-icon">🍎</text>
            <text>饮食建议</text>
          </view>
          <view class="advice-text">{{ getAdviceText('diet') }}</view>
        </view>
        <view class="advice-item">
          <view class="advice-label">
            <text class="label-icon">🏃</text>
            <text>生活建议</text>
          </view>
          <view class="advice-text">{{ getAdviceText('lifestyle') }}</view>
        </view>
      </view>
    </view>

    <!-- 操作按钮 -->
    <view class="action-buttons">
      <button class="btn btn-outline btn-block" @click="goToCourses">
        <text class="btn-icon">📚</text>
        <text>查看养生课程</text>
      </button>
      <button class="btn btn-text btn-block" @click="retest">
        重新舌诊
      </button>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

// 数据
const analysis = ref({})
const features = ref({})
const comparison = ref(null)
const advice = ref({})

const constitution = ref('')

onLoad((options) => {
  if (options.data) {
    const data = JSON.parse(decodeURIComponent(options.data))
    if (data.analysis) {
      analysis.value = data.analysis
      features.value = data.analysis.tongue_features || {}
      constitution.value = data.analysis.constitution_tendency
    }
    comparison.value = data.comparison || null
    loadAdvice()
  }
})

function loadAdvice() {
  // 简化的建议数据
  const adviceMap = {
    peace: {
      diet: '保持均衡饮食，不偏食挑食，五谷杂粮搭配',
      lifestyle: '作息规律，适度运动，保持心情舒畅'
    },
    qi_deficiency: {
      diet: '多吃补气健脾食物，如山药、黄芪、红枣、人参',
      lifestyle: '避免过度劳累，保证充足睡眠，适度运动'
    },
    yang_deficiency: {
      diet: '多吃温补食物，如羊肉、韭菜、生姜、肉桂',
      lifestyle: '注意保暖，避免受凉，适当晒太阳'
    },
    yin_deficiency: {
      diet: '多吃滋阴润燥食物，如百合、银耳、梨、枸杞',
      lifestyle: '避免熬夜，保持心情舒畅，避免辛辣'
    },
    phlegm_damp: {
      diet: '多吃健脾利湿食物，如薏米、赤小豆、冬瓜、陈皮',
      lifestyle: '加强运动，保持居住环境干燥，避免油腻'
    },
    damp_heat: {
      diet: '多吃清热利湿食物，如绿豆、苦瓜、芹菜、黄瓜',
      lifestyle: '避免辛辣油腻，保持皮肤清洁，多饮水'
    },
    blood_stasis: {
      diet: '多吃活血化瘀食物，如山楂、红花、桃仁、黑木耳',
      lifestyle: '适度运动，避免久坐，注意保暖'
    },
    qi_depression: {
      diet: '多吃疏肝理气食物，如玫瑰花、陈皮、佛手、薄荷',
      lifestyle: '保持心情舒畅，适当户外活动，学会释放压力'
    },
    special: {
      diet: '避免过敏原，多吃抗过敏食物，如蜂蜜、红枣、胡萝卜',
      lifestyle: '保持室内清洁，避免接触过敏源，增强体质'
    }
  }

  advice.value = adviceMap[constitution.value] || adviceMap.peace
}

function getAdviceText(type) {
  return advice.value[type] || ''
}

function goToCourses() {
  uni.navigateTo({
    url: `/pages/courses/list?constitution=${constitution.value}`
  })
}

function retest() {
  uni.navigateBack()
}
</script>

<style lang="scss" scoped>
.tongue-result-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 40rpx;
}

.result-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60rpx 30rpx;
  text-align: center;
  color: #fff;
}

.constitution-icon {
  font-size: 100rpx;
  margin-bottom: 20rpx;
}

.result-title {
  font-size: 32rpx;
  opacity: 0.9;
  margin-bottom: 15rpx;
}

.constitution-name {
  font-size: 48rpx;
  font-weight: bold;
  margin-bottom: 15rpx;
}

.confidence {
  font-size: 26rpx;
  opacity: 0.9;
}

.info-card {
  background: #fff;
  margin: 20rpx;
  padding: 30rpx;
  border-radius: 16rpx;
}

.card-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 25rpx;
  display: flex;
  align-items: center;
  gap: 10rpx;
}

.title-icon {
  font-size: 36rpx;
}

.feature-list {
  display: flex;
  flex-direction: column;
  gap: 15rpx;
}

.feature-row {
  display: flex;
  padding: 15rpx 0;
  border-bottom: 1px solid #f0f0f0;

  &:last-child {
    border-bottom: none;
  }
}

.feature-label {
  font-size: 28rpx;
  color: #666;
  width: 180rpx;
  flex-shrink: 0;
}

.feature-value {
  font-size: 28rpx;
  color: #333;
  font-weight: 500;
}

.comparison-content {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.comparison-status {
  display: flex;
  align-items: center;
  gap: 15rpx;
  padding: 20rpx;
  border-radius: 12rpx;
  background: #fff7e6;

  &.consistent {
    background: #f6ffed;
  }
}

.status-icon {
  font-size: 40rpx;
}

.status-text {
  font-size: 28rpx;
  font-weight: 600;
}

.comparison-detail {
  display: flex;
  font-size: 26rpx;
  line-height: 1.6;
}

.detail-label {
  color: #666;
  flex-shrink: 0;
}

.detail-value {
  color: #333;
  font-weight: 500;
}

.comparison-message {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
  padding: 15rpx;
  background: #f8f9ff;
  border-radius: 12rpx;
}

.advice-content {
  display: flex;
  flex-direction: column;
  gap: 25rpx;
}

.advice-item {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.advice-label {
  display: flex;
  align-items: center;
  gap: 10rpx;
  font-size: 26rpx;
  font-weight: 600;
  color: #333;
}

.label-icon {
  font-size: 28rpx;
}

.advice-text {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
  padding-left: 40rpx;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
  padding: 0 30rpx;
}

.btn-icon {
  margin-right: 8rpx;
}
</style>
