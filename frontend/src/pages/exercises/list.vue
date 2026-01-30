<template>
  <view class="exercises-page">
    <!-- 顶部筛选区 -->
    <view class="filter-section">
      <!-- 体质筛选 -->
      <scroll-view scroll-x class="filter-scroll">
        <view class="filter-item" :class="{ active: !selectedConstitution }" @click="selectConstitution('')">
          全部
        </view>
        <view
          v-for="constitution in constitutions"
          :key="constitution.value"
          class="filter-item"
          :class="{ active: selectedConstitution === constitution.value }"
          @click="selectConstitution(constitution.value)"
        >
          {{ constitution.label }}
        </view>
      </scroll-view>

      <!-- 运动类型筛选 -->
      <scroll-view scroll-x class="filter-scroll">
        <view class="filter-item" :class="{ active: !selectedType }" @click="selectType('')">
          全部类型
        </view>
        <view
          v-for="type in exerciseTypes"
          :key="type.code"
          class="filter-item"
          :class="{ active: selectedType === type.code }"
          @click="selectType(type.code)"
        >
          {{ type.name }}
        </view>
      </scroll-view>

      <!-- 难度筛选 -->
      <scroll-view scroll-x class="filter-scroll">
        <view class="filter-item" :class="{ active: !selectedDifficulty }" @click="selectDifficulty('')">
          全部难度
        </view>
        <view
          v-for="diff in difficulties"
          :key="diff.value"
          class="filter-item"
          :class="{ active: selectedDifficulty === diff.value }"
          @click="selectDifficulty(diff.value)"
        >
          {{ diff.label }}
        </view>
      </scroll-view>
    </view>

    <!-- 运动列表 -->
    <scroll-view
      class="exercises-scroll"
      scroll-y
      refresher-enabled
      :refresher-triggered="refreshing"
      @refresherrefresh="onRefresh"
      @scrolltolower="loadMore"
    >
      <!-- 空状态 -->
      <view v-if="!loading && exercises.length === 0" class="empty-state">
        <text class="empty-icon">🏃</text>
        <text class="empty-text">暂无运动功法</text>
      </view>

      <!-- 运动列表 -->
      <view v-else class="exercises-list">
        <view
          v-for="item in exercises"
          :key="item.id"
          class="exercise-item"
          @click="goToDetail(item.id)"
        >
          <!-- 封面图 -->
          <image
            v-if="item.image_url"
            :src="item.image_url"
            class="exercise-cover"
            mode="aspectFill"
            lazy-load
          />
          <view v-else class="exercise-cover placeholder">
            <text class="placeholder-icon">🧘</text>
          </view>

          <!-- 运动信息 -->
          <view class="exercise-info">
            <view class="exercise-name">{{ item.name }}</view>
            <view class="exercise-meta">
              <text class="meta-tag">{{ getTypeName(item.exercise_type) }}</text>
              <text class="meta-tag">{{ getDifficultyName(item.difficulty_level) }}</text>
              <text v-if="item.duration_seconds" class="meta-time">
                {{ formatDuration(item.duration_seconds) }}
              </text>
            </view>
            <view v-if="item.description" class="exercise-desc">
              {{ item.description }}
            </view>
          </view>
        </view>
      </view>

      <!-- 加载状态 -->
      <view v-if="loading" class="loading-state">
        <text>加载中...</text>
      </view>

      <!-- 没有更多 -->
      <view v-if="!hasMore && exercises.length > 0" class="no-more">
        <text>没有更多了</text>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getExercises, getExerciseTypes, getExercisesByConstitution } from '@/api/exercises.js'

// 数据
const exercises = ref([])
const exerciseTypes = ref([])
const loading = ref(false)
const refreshing = ref(false)
const hasMore = ref(true)
const selectedConstitution = ref('')
const selectedType = ref('')
const selectedDifficulty = ref('')

// 体质列表
const constitutions = ref([
  { value: 'peace', label: '平和质' },
  { value: 'qi_deficiency', label: '气虚质' },
  { value: 'yang_deficiency', label: '阳虚质' },
  { value: 'yin_deficiency', label: '阴虚质' },
  { value: 'phlegm_damp', label: '痰湿质' },
  { value: 'damp_heat', label: '湿热质' },
  { value: 'blood_stasis', label: '血瘀质' },
  { value: 'qi_depression', label: '气郁质' },
  { value: 'special', label: '特禀质' }
])

// 难度列表
const difficulties = ref([
  { value: 'beginner', label: '初级' },
  { value: 'intermediate', label: '中级' },
  { value: 'advanced', label: '高级' }
])

// 分页
const currentPage = ref(0)
const pageSize = 20

// 加载运动类型
onMounted(() => {
  loadExerciseTypes()
  loadExercises()
})

async function loadExerciseTypes() {
  try {
    exerciseTypes.value = await getExerciseTypes()
  } catch (e) {
    console.error('加载运动类型失败:', e)
  }
}

// 加载运动列表
async function loadExercises(isRefresh = false) {
  if (loading.value) return

  loading.value = true

  try {
    const params = {
      skip: isRefresh ? 0 : currentPage.value * pageSize,
      limit: pageSize
    }

    if (selectedType.value) params.exercise_type = selectedType.value
    if (selectedDifficulty.value) params.difficulty_level = selectedDifficulty.value
    if (selectedConstitution.value) {
      // 如果选择了体质，使用专门的接口
      const data = await getExercisesByConstitution(selectedConstitution.value, params)
      exercises.value = isRefresh ? data.items : [...exercises.value, ...data.items]
      hasMore.value = exercises.value.length < data.total
    } else {
      const data = await getExercises(params)
      exercises.value = isRefresh ? data.items : [...exercises.value, ...data.items]
      hasMore.value = exercises.value.length < data.total
    }

    if (isRefresh) {
      currentPage.value = 0
    }
  } catch (e) {
    console.error('加载运动列表失败:', e)
    uni.showToast({ title: '加载失败', icon: 'none' })
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

// 下拉刷新
async function onRefresh() {
  refreshing.value = true
  currentPage.value = 0
  await loadExercises(true)
}

// 加载更多
function loadMore() {
  if (!loading.value && hasMore.value) {
    currentPage.value++
    loadExercises()
  }
}

// 筛选方法
function selectConstitution(value) {
  selectedConstitution.value = value
  currentPage.value = 0
  loadExercises(true)
}

function selectType(value) {
  selectedType.value = value
  currentPage.value = 0
  loadExercises(true)
}

function selectDifficulty(value) {
  selectedDifficulty.value = value
  currentPage.value = 0
  loadExercises(true)
}

// 跳转详情
function goToDetail(id) {
  uni.navigateTo({
    url: `/pages/exercises/detail?id=${id}`
  })
}

// 格式化时长
function formatDuration(seconds) {
  const minutes = Math.floor(seconds / 60)
  return `${minutes}分钟`
}

// 获取类型名称
function getTypeName(type) {
  const typeMap = exerciseTypes.value.find(t => t.code === type)
  return typeMap ? typeMap.name : type
}

// 获取难度名称
function getDifficultyName(level) {
  const diffMap = difficulties.value.find(d => d.value === level)
  return diffMap ? diffMap.label : level
}
</script>

<style scoped>
.exercises-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
}

.filter-section {
  background-color: #fff;
  padding: 10rpx 0;
  border-bottom: 1rpx solid #e5e5e5;
}

.filter-scroll {
  white-space: nowrap;
  padding: 10rpx 20rpx;
}

.filter-item {
  display: inline-block;
  padding: 10rpx 24rpx;
  margin-right: 16rpx;
  background-color: #f5f5f5;
  border-radius: 40rpx;
  font-size: 28rpx;
  color: #666;
}

.filter-item.active {
  background-color: #4CAF50;
  color: #fff;
}

.exercises-scroll {
  flex: 1;
}

.exercises-list {
  padding: 20rpx;
}

.exercise-item {
  display: flex;
  background-color: #fff;
  border-radius: 16rpx;
  margin-bottom: 20rpx;
  overflow: hidden;
}

.exercise-cover {
  width: 200rpx;
  height: 200rpx;
  flex-shrink: 0;
}

.exercise-cover.placeholder {
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-icon {
  font-size: 80rpx;
}

.exercise-info {
  flex: 1;
  padding: 20rpx;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.exercise-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 10rpx;
}

.exercise-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
  margin-bottom: 10rpx;
}

.meta-tag {
  padding: 4rpx 12rpx;
  background-color: #f0f0f0;
  border-radius: 8rpx;
  font-size: 24rpx;
  color: #666;
}

.meta-time {
  font-size: 24rpx;
  color: #999;
}

.exercise-desc {
  font-size: 26rpx;
  color: #999;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.empty-state,
.loading-state,
.no-more {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80rpx 0;
  color: #999;
}

.empty-icon {
  font-size: 120rpx;
  margin-bottom: 20rpx;
}

.empty-text {
  font-size: 28rpx;
}
</style>
