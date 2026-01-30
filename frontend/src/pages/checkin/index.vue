<template>
  <view class="checkin-page">
    <!-- 周选择器 -->
    <view class="week-selector">
      <scroll-view scroll-x class="week-scroll">
        <view
          v-for="week in availableWeeks"
          :key="week"
          class="week-item"
          :class="{ active: currentWeek === week }"
          @click="selectWeek(week)"
        >
          第{{ week }}周
        </view>
      </scroll-view>
    </view>

    <!-- 本周汇总 -->
    <view v-if="weekSummary" class="summary-card">
      <view class="summary-title">本周汇总</view>
      <view class="summary-stats">
        <view class="stat-item">
          <text class="stat-value">{{ weekSummary.completed_days || 0 }}/7</text>
          <text class="stat-label">完成天数</text>
        </view>
        <view class="stat-item">
          <text class="stat-value">{{ weekSummary.exercise_completion_rate?.toFixed(0) || 0 }}%</text>
          <text class="stat-label">运动完成率</text>
        </view>
        <view class="stat-item">
          <text class="stat-value">{{ weekSummary.routine_adherence_rate?.toFixed(0) || 0 }}%</text>
          <text class="stat-label">作息遵守率</text>
        </view>
        <view class="stat-item">
          <text class="stat-value">{{ weekSummary.avg_mood_score?.toFixed(1) || '-' }}</text>
          <text class="stat-label">平均情绪</text>
        </view>
      </view>
    </view>

    <!-- 打卡日历 -->
    <view v-if="currentCheckin" class="checkin-calendar">
      <view class="calendar-header">
        <text>本周打卡</text>
        <text class="streak-info">连续 {{ currentStreak }} 天</text>
      </view>
      <view class="calendar-grid">
        <view
          v-for="(day, index) in currentCheckin.daily_entries"
          :key="index"
          class="day-card"
          :class="{ completed: day.completed, today: isToday(day.date) }"
          @click="openDayModal(day, index)"
        >
          <view class="day-header">
            <text class="day-name">{{ day.weekday }}</text>
            <text v-if="day.completed" class="completed-icon">✓</text>
          </view>
          <view class="day-content">
            <text class="day-number">{{ day.day }}</text>
            <view v-if="day.exercises_completed && day.exercises_completed.length" class="exercise-count">
              <text>{{ day.exercises_completed.length }}项运动</text>
            </view>
            <view v-if="day.mood_score" class="mood-score">
              情绪: {{ day.mood_score }}/10
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- AI反馈 -->
    <view v-if="aiFeedback && (aiFeedback.trends || aiFeedback.recommendations)" class="ai-feedback-card">
      <view class="feedback-title">🤖 AI分析</view>
      <view v-if="aiFeedback.trends && aiFeedback.trends.length" class="feedback-section">
        <text class="feedback-label">趋势分析：</text>
        <text v-for="(trend, index) in aiFeedback.trends" :key="index" class="feedback-item">
          • {{ trend }}
        </text>
      </view>
      <view v-if="aiFeedback.recommendations && aiFeedback.recommendations.length" class="feedback-section">
        <text class="feedback-label">建议：</text>
        <text v-for="(rec, index) in aiFeedback.recommendations" :key="index" class="feedback-item">
          {{ index + 1 }}. {{ rec }}
        </text>
      </view>
      <view v-if="aiFeedback.motivational_message" class="motivational-message">
        {{ aiFeedback.motivational_message }}
      </view>
    </view>

    <!-- 鼓励信息 -->
    <view v-if="motivationalMessage" class="motivational-card">
      <text class="motivational-text">{{ motivationalMessage }}</text>
    </view>

    <!-- 打卡弹窗 -->
    <uni-popup ref="dayModal" type="bottom">
      <view class="day-modal" v-if="selectedDay">
        <view class="modal-header">
          <text class="modal-title">{{ selectedDay.weekday }} 打卡</text>
          <text class="modal-date">{{ selectedDay.date }}</text>
        </view>

        <scroll-view class="modal-content" scroll-y>
          <!-- 运动打卡 -->
          <view class="form-section">
            <view class="form-label">运动记录</view>
            <view class="form-item">
              <text class="field-label">运动时长（分钟）</text>
              <input
                v-model.number="formData.exercise_minutes"
                type="number"
                class="form-input"
                placeholder="请输入运动时长"
              />
            </view>
            <view class="form-item">
              <text class="field-label">是否完成运动</text>
              <switch
                :checked="formData.exercises_done"
                @change="onExerciseSwitchChange"
                color="#4CAF50"
              />
            </view>
          </view>

          <!-- 作息打卡 -->
          <view class="form-section">
            <view class="form-label">作息记录</view>
            <view class="form-item">
              <text class="field-label">是否按作息</text>
              <switch
                :checked="formData.routine_followed"
                @change="onRoutineSwitchChange"
                color="#4CAF50"
              />
            </view>
            <view class="form-item">
              <text class="field-label">睡眠时长（小时）</text>
              <input
                v-model.number="formData.sleep_hours"
                type="digit"
                class="form-input"
                placeholder="请输入睡眠时长"
              />
            </view>
          </view>

          <!-- 状态打卡 -->
          <view class="form-section">
            <view class="form-label">状态记录</view>
            <view class="form-item">
              <text class="field-label">情绪分数 (1-10)</text>
              <slider
                :value="formData.mood_score"
                @change="onMoodScoreChange"
                min="1"
                max="10"
                step="1"
                show-value
                active-color="#4CAF50"
              />
            </view>
            <view class="form-item">
              <text class="field-label">精力水平 (1-10)</text>
              <slider
                :value="formData.energy_level"
                @change="onEnergyLevelChange"
                min="1"
                max="10"
                step="1"
                show-value
                active-color="#4CAF50"
              />
            </view>
          </view>

          <!-- 备注 -->
          <view class="form-section">
            <view class="form-label">备注</view>
            <textarea
              v-model="formData.notes"
              class="form-textarea"
              placeholder="记录今天的感受..."
              maxlength="200"
            />
          </view>
        </scroll-view>

        <view class="modal-footer">
          <button class="btn-secondary" @click="closeModal">取消</button>
          <button class="btn-primary" @click="saveDayEntry">保存</button>
        </view>
      </view>
    </uni-popup>
  </view>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import {
  getCurrentWeekCheckin,
  updateDailyEntry,
  getWeekSummary,
  getProgressStreak,
  getWeeklyRecommendations,
  getMotivationalMessage
} from '@/api/checkin.js'

const currentWeek = ref(1)
const availableWeeks = ref([1, 2, 3, 4])
const currentCheckin = ref(null)
const weekSummary = ref(null)
const currentStreak = ref(0)
const aiFeedback = ref(null)
const motivationalMessage = ref('')

// 选中的日期
const selectedDay = ref(null)
const selectedDayIndex = ref(0)

// 表单数据
const formData = ref({
  exercise_minutes: 0,
  exercises_done: false,
  routine_followed: false,
  sleep_hours: 0,
  mood_score: 5,
  energy_level: 5,
  notes: ''
})

const dayModal = ref(null)

onMounted(() => {
  loadCurrentWeekCheckin()
})

async function loadCurrentWeekCheckin() {
  try {
    // 使用模拟用户ID
    const userId = 'mock_user_id'
    currentCheckin.value = await getCurrentWeekCheckin(userId)

    // 加载周汇总
    if (currentCheckin.value) {
      await loadWeekSummary(currentCheckin.value.id)
      await loadAIRecommendations(currentCheckin.value.id)
    }

    // 加载连续天数
    const streakData = await getProgressStreak(userId)
    currentStreak.value = streakData.current_streak

    // 加载鼓励信息
    const motivationalData = await getMotivationalMessage(userId, currentStreak.value)
    motivationalMessage.value = motivationalData.motivational_message
  } catch (e) {
    console.error('加载打卡数据失败:', e)
    // 如果本周没有打卡记录，创建一个
    try {
      const userId = 'mock_user_id'
      // 这里应该调用创建打卡的API
      // currentCheckin.value = await createWeeklyCheckin({ user_id: userId, week_number: currentWeek.value })
    } catch (createError) {
      console.error('创建打卡记录失败:', createError)
    }
  }
}

async function loadWeekSummary(checkinId) {
  try {
    weekSummary.value = await getWeekSummary(checkinId)
  } catch (e) {
    console.error('加载周汇总失败:', e)
  }
}

async function loadAIRecommendations(checkinId) {
  try {
    aiFeedback.value = await getWeeklyRecommendations(checkinId)
  } catch (e) {
    console.error('加载AI建议失败:', e)
  }
}

function selectWeek(week) {
  currentWeek.value = week
  // 重新加载该周的打卡数据
}

function openDayModal(day, index) {
  selectedDay.value = day
  selectedDayIndex.value = index

  // 填充表单数据
  formData.value = {
    exercise_minutes: day.exercise_minutes || 0,
    exercises_done: (day.exercises_completed && day.exercises_completed.length > 0) || false,
    routine_followed: day.routine_followed || false,
    sleep_hours: day.sleep_hours || 0,
    mood_score: day.mood_score || 5,
    energy_level: day.energy_level || 5,
    notes: day.notes || ''
  }

  dayModal.value?.open()
}

function closeModal() {
  dayModal.value?.close()
}

function onExerciseSwitchChange(e) {
  formData.value.exercises_done = e.detail.value
}

function onRoutineSwitchChange(e) {
  formData.value.routine_followed = e.detail.value
}

function onMoodScoreChange(e) {
  formData.value.mood_score = e.detail.value
}

function onEnergyLevelChange(e) {
  formData.value.energy_level = e.detail.value
}

async function saveDayEntry() {
  try {
    const day = selectedDayIndex.value + 1
    const data = {
      exercise_minutes: formData.value.exercise_minutes,
      exercises_completed: formData.value.exercises_done ? ['exercise_1'] : [],
      routine_followed: formData.value.routine_followed,
      sleep_hours: formData.value.sleep_hours,
      mood_score: formData.value.mood_score,
      energy_level: formData.value.energy_level,
      notes: formData.value.notes,
      completed: formData.value.exercises_done || formData.value.routine_followed
    }

    await updateDailyEntry(currentCheckin.value.id, day, data)

    // 更新本地数据
    currentCheckin.value.daily_entries[selectedDayIndex.value] = {
      ...currentCheckin.value.daily_entries[selectedDayIndex.value],
      ...data
    }

    // 重新加载汇总
    await loadWeekSummary(currentCheckin.value.id)

    uni.showToast({ title: '保存成功', icon: 'success' })
    closeModal()
  } catch (e) {
    console.error('保存打卡失败:', e)
    uni.showToast({ title: '保存失败', icon: 'none' })
  }
}

function isToday(dateStr) {
  const today = new Date()
  const date = new Date(dateStr)
  return today.toDateString() === date.toDateString()
}
</script>

<style scoped>
.checkin-page {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 40rpx;
}

.week-selector {
  background-color: #fff;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #e5e5e5;
}

.week-scroll {
  white-space: nowrap;
  padding: 0 20rpx;
}

.week-item {
  display: inline-block;
  padding: 12rpx 32rpx;
  margin-right: 16rpx;
  background-color: #f5f5f5;
  border-radius: 40rpx;
  font-size: 28rpx;
  color: #666;
}

.week-item.active {
  background-color: #4CAF50;
  color: #fff;
}

.summary-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  margin: 20rpx;
  padding: 30rpx;
  border-radius: 16rpx;
  color: #fff;
}

.summary-title {
  font-size: 32rpx;
  font-weight: bold;
  margin-bottom: 20rpx;
}

.summary-stats {
  display: flex;
  justify-content: space-around;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 36rpx;
  font-weight: bold;
  margin-bottom: 8rpx;
}

.stat-label {
  font-size: 24rpx;
  opacity: 0.9;
}

.checkin-calendar {
  background-color: #fff;
  margin: 0 20rpx 20rpx;
  padding: 30rpx;
  border-radius: 16rpx;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.streak-info {
  font-size: 24rpx;
  color: #4CAF50;
  background-color: #E8F5E9;
  padding: 8rpx 16rpx;
  border-radius: 20rpx;
}

.calendar-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.day-card {
  width: calc((100% - 48rpx) / 7);
  background-color: #f5f5f5;
  border-radius: 12rpx;
  padding: 16rpx 8rpx;
  text-align: center;
}

.day-card.completed {
  background-color: #E8F5E9;
  border: 2rpx solid #4CAF50;
}

.day-card.today {
  border: 2rpx solid #FFB74D;
}

.day-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8rpx;
}

.day-name {
  font-size: 20rpx;
  color: #999;
}

.completed-icon {
  font-size: 20rpx;
  color: #4CAF50;
}

.day-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.day-number {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 4rpx;
}

.exercise-count {
  font-size: 20rpx;
  color: #4CAF50;
}

.mood-score {
  font-size: 20rpx;
  color: #FFB74D;
}

.ai-feedback-card {
  background-color: #fff;
  margin: 0 20rpx 20rpx;
  padding: 30rpx;
  border-radius: 16rpx;
}

.feedback-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.feedback-section {
  margin-bottom: 20rpx;
}

.feedback-label {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 10rpx;
}

.feedback-item {
  font-size: 26rpx;
  color: #666;
  line-height: 1.8;
  display: block;
  margin-bottom: 6rpx;
}

.motivational-message {
  background: linear-gradient(135deg, #FFE082 0%, #FFCA28 100%);
  padding: 20rpx;
  border-radius: 12rpx;
  font-size: 28rpx;
  color: #333;
  line-height: 1.6;
}

.motivational-card {
  background: linear-gradient(135deg, #81D4FA 0%, #4FC3F7 100%);
  margin: 0 20rpx 20rpx;
  padding: 30rpx;
  border-radius: 16rpx;
  text-align: center;
}

.motivational-text {
  font-size: 28rpx;
  color: #fff;
  line-height: 1.6;
}

/* 弹窗样式 */
.day-modal {
  background-color: #fff;
  border-radius: 32rpx 32rpx 0 0;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 30rpx;
  border-bottom: 1rpx solid #e5e5e5;
}

.modal-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 8rpx;
}

.modal-date {
  font-size: 26rpx;
  color: #999;
}

.modal-content {
  flex: 1;
  padding: 30rpx;
}

.form-section {
  margin-bottom: 30rpx;
}

.form-label {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 16rpx;
  display: block;
}

.form-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20rpx;
}

.field-label {
  font-size: 28rpx;
  color: #666;
}

.form-input {
  flex: 1;
  margin-left: 20rpx;
  padding: 16rpx;
  border: 1rpx solid #e5e5e5;
  border-radius: 8rpx;
  font-size: 28rpx;
}

.form-textarea {
  width: 100%;
  min-height: 150rpx;
  padding: 16rpx;
  border: 1rpx solid #e5e5e5;
  border-radius: 8rpx;
  font-size: 28rpx;
}

.modal-footer {
  display: flex;
  gap: 20rpx;
  padding: 30rpx;
  border-top: 1rpx solid #e5e5e5;
}

.btn-primary,
.btn-secondary {
  flex: 1;
  padding: 24rpx;
  border-radius: 12rpx;
  font-size: 28rpx;
  border: none;
}

.btn-primary {
  background-color: #4CAF50;
  color: #fff;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #666;
}
</style>
