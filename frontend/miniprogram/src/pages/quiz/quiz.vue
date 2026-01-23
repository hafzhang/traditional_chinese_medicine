<template>
  <view class="container">
    <!-- 进度条 -->
    <view class="progress-bar">
      <view class="progress" :style="{ width: progress + '%' }"></view>
    </view>
    <view class="progress-text">{{ currentIndex + 1 }} / {{ questions.length }}</view>

    <!-- 问题卡片 -->
    <view class="question-card" v-if="currentQuestion">
      <view class="question-text">{{ currentQuestion.question_text }}</view>

      <!-- 选项 -->
      <view class="options">
        <view
          class="option"
          v-for="(option, index) in options"
          :key="index"
          :class="{ active: answers[currentIndex] === option.value }"
          @tap="selectAnswer(option.value)"
        >
          <view class="option-label">{{ option.label }}</view>
          <view class="option-text">{{ option.text }}</view>
        </view>
      </view>
    </view>

    <!-- 导航按钮 -->
    <view class="nav-buttons">
      <button class="btn btn-outline" @tap="prevQuestion" :disabled="currentIndex === 0">上一题</button>
      <button class="btn btn-primary" @tap="nextQuestion">
        {{ currentIndex === questions.length - 1 ? '提交' : '下一题' }}
      </button>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const API_BASE = 'http://localhost:8000/api/v1'

const questions = ref([])
const answers = ref([])
const currentIndex = ref(0)

const options = [
  { label: '①', text: '没有', value: 1 },
  { label: '②', text: '很少', value: 2 },
  { label: '③', text: '有时', value: 3 },
  { label: '④', text: '经常', value: 4 },
  { label: '⑤', text: '总是', value: 5 }
]

const progress = computed(() => {
  return ((currentIndex.value + 1) / questions.value.length) * 100
})

const currentQuestion = computed(() => {
  return questions.value[currentIndex.value]
})

// 获取问卷题目
const loadQuestions = async () => {
  try {
    const res = await uni.request({
      url: `${API_BASE}/constitution/quiz/questions`,
      method: 'GET'
    })
    if (res.data.code === 0) {
      questions.value = res.data.data.questions
      // 初始化答案数组
      answers.value = new Array(questions.value.length).fill(0)
    }
  } catch (e) {
    uni.showToast({
      title: '加载题目失败',
      icon: 'none'
    })
  }
}

const selectAnswer = (value) => {
  answers.value[currentIndex.value] = value
  // 自动跳转到下一题
  if (currentIndex.value < questions.value.length - 1) {
    setTimeout(() => {
      nextQuestion()
    }, 300)
  }
}

const prevQuestion = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}

const nextQuestion = () => {
  // 检查是否已选择答案
  if (answers.value[currentIndex.value] === 0) {
    uni.showToast({
      title: '请选择一个答案',
      icon: 'none'
    })
    return
  }

  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
  } else {
    submitQuiz()
  }
}

const submitQuiz = async () => {
  try {
    uni.showLoading({ title: '分析中...' })

    const res = await uni.request({
      url: `${API_BASE}/constitution/quiz/submit`,
      method: 'POST',
      data: {
        answers: answers.value
      }
    })

    uni.hideLoading()

    if (res.data.code === 0) {
      // 保存结果到本地
      uni.setStorageSync('quizResult', res.data.data)
      // 跳转到结果页
      uni.redirectTo({
        url: '/pages/result/result'
      })
    }
  } catch (e) {
    uni.hideLoading()
    uni.showToast({
      title: '提交失败',
      icon: 'none'
    })
  }
}

onMounted(() => {
  loadQuestions()
})
</script>

<style scoped>
.container {
  min-height: 100vh;
  background: #f8f8f8;
  padding: 30rpx;
}

.progress-bar {
  height: 8rpx;
  background: #e0e0e0;
  border-radius: 4rpx;
  overflow: hidden;
  margin-bottom: 20rpx;
}

.progress {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s;
}

.progress-text {
  text-align: center;
  font-size: 26rpx;
  color: #999;
  margin-bottom: 30rpx;
}

.question-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 40rpx;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.1);
}

.question-text {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  line-height: 1.6;
  margin-bottom: 40rpx;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.option {
  display: flex;
  align-items: center;
  padding: 30rpx;
  border: 2rpx solid #e0e0e0;
  border-radius: 16rpx;
  transition: all 0.3s;
}

.option.active {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.1);
}

.option-label {
  width: 60rpx;
  height: 60rpx;
  border-radius: 50%;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26rpx;
  color: #666;
  margin-right: 20rpx;
}

.option.active .option-label {
  background: #667eea;
  color: #fff;
}

.option-text {
  font-size: 28rpx;
  color: #333;
}

.nav-buttons {
  display: flex;
  gap: 20rpx;
  margin-top: 40rpx;
}

.btn {
  flex: 1;
  height: 88rpx;
  border-radius: 44rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
  border: none;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.btn-outline {
  background: transparent;
  border: 2rpx solid #667eea;
  color: #667eea;
}

.btn[disabled] {
  opacity: 0.5;
}
</style>
