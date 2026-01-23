<template>
  <view class="page-container">
    <!-- 进度条 -->
    <view class="progress-bar">
      <view class="progress-fill" :style="{ width: progress + '%' }"></view>
    </view>
    <view class="progress-text">{{ currentQuestionIndex + 1 }} / 30</view>

    <!-- 问题卡片 -->
    <view class="question-card" v-if="currentQuestion">
      <view class="question-number">问题 {{ currentQuestionIndex + 1 }}</view>
      <view class="question-content">{{ currentQuestion.content }}</view>

      <!-- 选项 -->
      <view class="options">
        <view
          v-for="option in options"
          :key="option.value"
          class="option-item"
          :class="{ active: answers[currentQuestionIndex] === option.value }"
          @click="selectOption(option.value)"
        >
          <view class="option-radio">
            <view v-if="answers[currentQuestionIndex] === option.value" class="radio-dot"></view>
          </view>
          <view class="option-label">{{ option.label }}</view>
        </view>
      </view>

      <!-- 导航按钮 -->
      <view class="nav-buttons">
        <button
          v-if="currentQuestionIndex > 0"
          class="btn btn-outline"
          @click="prevQuestion"
        >
          上一题
        </button>
        <button
          v-if="currentQuestionIndex < 29"
          class="btn btn-primary"
          :disabled="!answers[currentQuestionIndex]"
          @click="nextQuestion"
        >
          下一题
        </button>
        <button
          v-else
          class="btn btn-primary btn-large"
          :disabled="!allAnswered"
          @click="submitTest"
        >
          提交测试
        </button>
      </view>
    </view>

    <!-- 加载状态 -->
    <view v-if="loading" class="loading">
      <view class="loading-spinner"></view>
      <view class="loading-text">加载中...</view>
    </view>

    <!-- 快速跳转 - 按体质类型分组 -->
    <view class="quick-nav">
      <view class="quick-nav-title">快速跳转</view>
      <view class="question-groups">
        <view
          v-for="(group, type) in QUESTION_GROUPS"
          :key="type"
          class="question-group"
        >
          <view class="question-grid-group">
            <view
              v-for="idx in Array.from({ length: group.end - group.start + 1 }, (_, i) => group.start + i - 1)"
              :key="idx"
              class="question-dot"
              :class="{
                'current': idx === currentQuestionIndex,
                'answered': answers[idx]
              }"
              @click="jumpToQuestion(idx)"
            >
              {{ idx + 1 }}
            </view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getQuestions, submitTest as submitTestApi } from '@/api/constitution.js'
import { QUESTION_GROUPS, CONSTITUTION_INFO } from '@/data/constitution.js'

// 状态
const questions = ref([])
const answers = ref(new Array(30).fill(null))
const currentQuestionIndex = ref(0)
const loading = ref(false)
const submitting = ref(false)

// 获取当前题目所属体质
const currentConstitutionType = computed(() => {
  const questionNum = currentQuestionIndex.value + 1
  for (const [type, info] of Object.entries(QUESTION_GROUPS)) {
    if (questionNum >= info.start && questionNum <= info.end) {
      return { type, name: info.name, color: CONSTITUTION_INFO[type]?.color || '#667eea' }
    }
  }
  return null
})

// 选项定义
const options = [
  { value: 1, label: '没有' },
  { value: 2, label: '很少' },
  { value: 3, label: '有时' },
  { value: 4, label: '经常' },
  { value: 5, label: '总是' }
]

// 计算属性
const progress = computed(() => ((currentQuestionIndex.value + 1) / 30) * 100)

const currentQuestion = computed(() => {
  return questions.value[currentQuestionIndex.value]
})

const allAnswered = computed(() => {
  return answers.value.every(a => a !== null)
})

// 生命周期
onMounted(() => {
  loadQuestions()
})

/**
 * 加载问题
 */
async function loadQuestions() {
  loading.value = true
  try {
    const res = await getQuestions()
    questions.value = res.data.questions
  } catch (error) {
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

/**
 * 选择选项
 */
function selectOption(value) {
  answers.value[currentQuestionIndex.value] = value
  // 自动跳转到下一题，提升体验
  if (currentQuestionIndex.value < 29) {
    setTimeout(() => {
      nextQuestion()
    }, 300)
  }
}

/**
 * 上一题
 */
function prevQuestion() {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
  }
}

/**
 * 下一题
 */
function nextQuestion() {
  if (currentQuestionIndex.value < 29 && answers.value[currentQuestionIndex.value]) {
    currentQuestionIndex.value++
  }
}

/**
 * 跳转到指定题目
 */
function jumpToQuestion(index) {
  currentQuestionIndex.value = index
}

/**
 * 提交测试
 */
async function submitTest() {
  if (!allAnswered.value) {
    uni.showToast({
      title: '请完成所有题目',
      icon: 'none'
    })
    return
  }

  submitting.value = true
  try {
    const res = await submitTestApi(answers.value)

    uni.setStorageSync('latestResult', res.data)
    uni.setStorageSync('resultId', res.data.result_id)

    // 跳转到结果页
    uni.redirectTo({
      url: `/pages/result/result?resultId=${res.data.result_id}`
    })
  } catch (error) {
    uni.showToast({
      title: '提交失败',
      icon: 'none'
    })
  } finally {
    submitting.value = false
  }
}
</script>

<style lang="scss" scoped>
.progress-bar {
  width: 100%;
  height: 8rpx;
  background: #e8e8e8;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s;
}

.progress-text {
  text-align: center;
  padding: 30rpx;
  font-size: 26rpx;
  color: #666;
}

.question-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 40rpx;
  margin: 20rpx 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
}

.question-number {
  font-size: 24rpx;
  color: #999;
  margin-bottom: 16rpx;
}

.question-content {
  font-size: 36rpx;
  font-weight: 600;
  line-height: 1.6;
  margin-bottom: 40rpx;
  color: #1a1a1a;
}

.options {
  margin-bottom: 40rpx;
}

.option-item {
  display: flex;
  align-items: center;
  padding: 28rpx 24rpx;
  border: 2rpx solid #e8e8e8;
  border-radius: 16rpx;
  margin-bottom: 20rpx;
  transition: all 0.3s;
}

.option-item.active {
  border-color: #667eea;
  background: #f8f9ff;
}

.option-radio {
  width: 40rpx;
  height: 40rpx;
  border: 3rpx solid #d9d9d9;
  border-radius: 50%;
  margin-right: 24rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.option-item.active .option-radio {
  border-color: #667eea;
}

.radio-dot {
  width: 20rpx;
  height: 20rpx;
  background: #667eea;
  border-radius: 50%;
}

.option-label {
  flex: 1;
  font-size: 30rpx;
}

.nav-buttons {
  display: flex;
  gap: 20rpx;
}

.nav-buttons .btn {
  flex: 1;
}

.quick-nav {
  background: #fff;
  border-radius: 24rpx;
  padding: 30rpx;
  margin: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
}

.quick-nav-title {
  font-size: 28rpx;
  font-weight: 600;
  margin-bottom: 20rpx;
  color: #333;
}

.question-groups {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.question-grid-group {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12rpx;
}

.question-grid {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 12rpx;
}

.question-dot {
  width: 60rpx;
  height: 60rpx;
  border-radius: 12rpx;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  color: #999;
  transition: all 0.3s;
}

.question-dot.answered {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.question-dot.current {
  border: 3rpx solid #667eea;
}

.loading {
  padding: 100rpx 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.loading-text {
  font-size: 28rpx;
  color: #999;
  margin-top: 20rpx;
}

.loading-spinner {
  width: 60rpx;
  height: 60rpx;
  border: 4rpx solid #f3f3f3;
  border-top: 4rpx solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.btn:disabled {
  opacity: 0.5;
}

/* 体质类型标签 */
.constitution-tag {
  display: inline-flex;
  align-items: center;
  gap: 8rpx;
  padding: 10rpx 20rpx;
  border-radius: 20rpx;
  margin-bottom: 20rpx;
  color: #fff;
}

.tag-icon {
  font-size: 24rpx;
}

.tag-name {
  font-size: 24rpx;
  font-weight: 500;
}

/* 快速跳转分组 */
.question-group {
  margin-bottom: 20rpx;
}

.question-group-label {
  font-size: 24rpx;
  color: #999;
  margin-bottom: 12rpx;
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.question-group-label .group-icon {
  font-size: 22rpx;
}
</style>
