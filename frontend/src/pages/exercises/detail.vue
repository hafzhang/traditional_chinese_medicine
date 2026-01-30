<template>
  <view class="exercise-detail-page">
    <view v-if="exercise" class="detail-container">
      <!-- 视频播放区 -->
      <view v-if="exercise.video_url" class="video-section">
        <video
          :src="exercise.video_url"
          class="exercise-video"
          controls
          poster=""
          object-fit="contain"
        />
      </view>

      <!-- 封面图（无视频时显示） -->
      <view v-else-if="exercise.image_url" class="cover-section">
        <image :src="exercise.image_url" class="exercise-cover" mode="aspectFill" />
      </view>

      <!-- 基本信息 -->
      <view class="info-section">
        <view class="exercise-name">{{ exercise.name }}</view>
        <view class="exercise-meta">
          <text class="meta-tag">{{ getTypeName(exercise.exercise_type) }}</text>
          <text class="meta-tag">{{ getDifficultyName(exercise.difficulty_level) }}</text>
          <text v-if="exercise.duration_seconds" class="meta-time">
            时长: {{ formatDuration(exercise.duration_seconds) }}
          </text>
        </view>

        <!-- 目标体质 -->
        <view v-if="exercise.target_constitutions && exercise.target_constitutions.length" class="target-constitutions">
          <text class="label">适合体质：</text>
          <text v-for="c in exercise.target_constitutions" :key="c" class="constitution-tag">
            {{ getConstitutionName(c) }}
          </text>
        </view>

        <!-- 描述 -->
        <view v-if="exercise.description" class="description">
          <text class="label">简介：</text>
          <text>{{ exercise.description }}</text>
        </view>

        <!-- 功效 -->
        <view v-if="exercise.benefits && exercise.benefits.length" class="benefits">
          <text class="label">功效：</text>
          <view class="benefit-list">
            <text v-for="(b, index) in exercise.benefits" :key="index" class="benefit-item">
              • {{ b }}
            </text>
          </view>
        </view>

        <!-- 重复次数 -->
        <view v-if="exercise.repetitions" class="repetitions">
          <text class="label">建议次数：</text>
          <text>{{ exercise.repetitions }}</text>
        </view>

        <!-- 目标部位 -->
        <view v-if="exercise.target_body_areas && exercise.target_body_areas.length" class="target-areas">
          <text class="label">锻炼部位：</text>
          <text>{{ exercise.target_body_areas.join('、') }}</text>
        </view>
      </view>

      <!-- 动作要领 -->
      <view v-if="exercise.instructions && exercise.instructions.length" class="instructions-section">
        <view class="section-title">动作要领</view>
        <view class="instructions-list">
          <view v-for="(step, index) in exercise.instructions" :key="index" class="instruction-item">
            <view class="step-number">{{ index + 1 }}</view>
            <view class="step-content">{{ step }}</view>
          </view>
        </view>
      </view>

      <!-- 步骤图片 -->
      <view v-if="exercise.step_images && exercise.step_images.length" class="step-images-section">
        <view class="section-title">步骤演示</view>
        <scroll-view scroll-x class="step-images-scroll">
          <image
            v-for="(img, index) in exercise.step_images"
            :key="index"
            :src="img"
            class="step-image"
            mode="aspectFill"
          />
        </scroll-view>
      </view>

      <!-- 注意事项 -->
      <view v-if="exercise.contraindications || exercise.caution_notes" class="caution-section">
        <view class="section-title caution-title">注意事项</view>
        <view v-if="exercise.contraindications" class="caution-item">
          <text class="caution-label">禁忌：</text>
          <text>{{ exercise.contraindications }}</text>
        </view>
        <view v-if="exercise.caution_notes" class="caution-item">
          <text class="caution-label">提醒：</text>
          <text>{{ exercise.caution_notes }}</text>
        </view>
      </view>
    </view>

    <!-- 加载状态 -->
    <view v-else class="loading-state">
      <text>加载中...</text>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getExerciseDetail, getExerciseTypes, incrementViewCount } from '@/api/exercises.js'

const exercise = ref(null)
const exerciseTypes = ref([])

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

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  const options = currentPage.options
  const exerciseId = options.id

  if (exerciseId) {
    loadExerciseDetail(exerciseId)
    loadExerciseTypes()
  }
})

async function loadExerciseDetail(id) {
  try {
    exercise.value = await getExerciseDetail(id)
    // 增加浏览次数
    incrementViewCount(id)
  } catch (e) {
    console.error('加载运动详情失败:', e)
    uni.showToast({ title: '加载失败', icon: 'none' })
  }
}

async function loadExerciseTypes() {
  try {
    exerciseTypes.value = await getExerciseTypes()
  } catch (e) {
    console.error('加载运动类型失败:', e)
  }
}

function formatDuration(seconds) {
  const minutes = Math.floor(seconds / 60)
  return `${minutes}分钟`
}

function getTypeName(type) {
  const typeMap = exerciseTypes.value.find(t => t.code === type)
  return typeMap ? typeMap.name : type
}

function getDifficultyName(level) {
  const diffMap = {
    beginner: '初级',
    intermediate: '中级',
    advanced: '高级'
  }
  return diffMap[level] || level
}

function getConstitutionName(code) {
  return constitutionNames[code] || code
}
</script>

<style scoped>
.exercise-detail-page {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.detail-container {
  padding-bottom: 40rpx;
}

.video-section {
  width: 100%;
  height: 420rpx;
  background-color: #000;
}

.exercise-video {
  width: 100%;
  height: 100%;
}

.cover-section {
  width: 100%;
  height: 420rpx;
}

.exercise-cover {
  width: 100%;
  height: 100%;
}

.info-section {
  background-color: #fff;
  padding: 30rpx;
  margin-bottom: 20rpx;
}

.exercise-name {
  font-size: 40rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.exercise-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
  margin-bottom: 20rpx;
}

.meta-tag {
  padding: 6rpx 16rpx;
  background-color: #4CAF50;
  color: #fff;
  border-radius: 8rpx;
  font-size: 24rpx;
}

.meta-time {
  padding: 6rpx 16rpx;
  background-color: #f0f0f0;
  color: #666;
  border-radius: 8rpx;
  font-size: 24rpx;
}

.target-constitutions,
.description,
.benefits,
.repetitions,
.target-areas {
  margin-bottom: 20rpx;
  font-size: 28rpx;
  line-height: 1.6;
  color: #666;
}

.label {
  color: #333;
  font-weight: bold;
}

.constitution-tag {
  display: inline-block;
  padding: 4rpx 12rpx;
  background-color: #E8F5E9;
  color: #4CAF50;
  border-radius: 8rpx;
  font-size: 24rpx;
  margin-right: 10rpx;
}

.benefit-list {
  margin-top: 10rpx;
}

.benefit-item {
  display: block;
  margin-bottom: 8rpx;
  padding-left: 10rpx;
}

.instructions-section,
.step-images-section,
.caution-section {
  background-color: #fff;
  padding: 30rpx;
  margin-bottom: 20rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.caution-title {
  color: #F44336;
}

.instructions-list {
  padding-left: 10rpx;
}

.instruction-item {
  display: flex;
  margin-bottom: 20rpx;
}

.step-number {
  width: 50rpx;
  height: 50rpx;
  background-color: #4CAF50;
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  font-weight: bold;
  flex-shrink: 0;
  margin-right: 20rpx;
}

.step-content {
  flex: 1;
  font-size: 28rpx;
  line-height: 1.6;
  color: #666;
  padding-top: 8rpx;
}

.step-images-scroll {
  white-space: nowrap;
}

.step-image {
  width: 300rpx;
  height: 300rpx;
  border-radius: 12rpx;
  margin-right: 20rpx;
  display: inline-block;
}

.caution-item {
  padding: 20rpx;
  background-color: #FFEBEE;
  border-radius: 12rpx;
  margin-bottom: 12rpx;
  font-size: 28rpx;
  line-height: 1.6;
}

.caution-label {
  color: #F44336;
  font-weight: bold;
}

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  color: #999;
}
</style>
