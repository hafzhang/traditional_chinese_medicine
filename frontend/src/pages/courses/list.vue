<template>
  <view class="courses-list-page">
    <!-- 顶部筛选区 -->
    <view class="filter-section">
      <scroll-view scroll-x class="filter-scroll">
        <view class="filter-item" :class="{ active: !selectedCategory }" @click="selectCategory('')">
          全部
        </view>
        <view
          v-for="cat in categories"
          :key="cat.value"
          class="filter-item"
          :class="{ active: selectedCategory === cat.value }"
          @click="selectCategory(cat.value)"
        >
          {{ cat.label }}
        </view>
      </scroll-view>

      <scroll-view scroll-x class="filter-scroll" v-if="selectedCategory === 'season'">
        <view class="filter-item" :class="{ active: !selectedSeason }" @click="selectSeason('')">
          全部季节
        </view>
        <view
          v-for="season in seasons"
          :key="season.value"
          class="filter-item"
          :class="{ active: selectedSeason === season.value }"
          @click="selectSeason(season.value)"
        >
          {{ season.label }}
        </view>
      </scroll-view>
    </view>

    <!-- 课程列表 -->
    <scroll-view class="courses-scroll" scroll-y @scrolltolower="loadMore">
      <view class="courses-list">
        <view
          v-for="item in courses"
          :key="item.id"
          class="course-item"
          @click="goToDetail(item.id)"
        >
          <image v-if="item.cover_image" :src="item.cover_image" class="course-image" mode="aspectFill" />
          <view v-else class="course-image placeholder">
            <text class="placeholder-icon">{{ getContentIcon(item.content_type) }}</text>
          </view>
          <view class="course-info">
            <view class="course-title">{{ item.title }}</view>
            <view class="course-desc">{{ item.description }}</view>
            <view class="course-meta">
              <text class="tag type">{{ getCategoryLabel(item.category) }}</text>
              <text class="duration" v-if="item.duration">{{ formatDuration(item.duration) }}</text>
            </view>
            <view class="course-author" v-if="item.author">
              <text class="author-icon">👨‍🏫</text>
              <text class="author-name">{{ item.author }}</text>
              <text class="author-title" v-if="item.author_title">{{ item.author_title }}</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 加载状态 -->
      <view class="load-more">
        <text v-if="loading">加载中...</text>
        <text v-else-if="!hasMore">没有更多了</text>
        <text v-else @click="loadMore">加载更多</text>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getCoursesList, getCourseCategories, getSeasons } from '@/api/courses.js'

// 数据
const courses = ref([])
const categories = ref([])
const seasons = ref([])
const selectedCategory = ref('')
const selectedSeason = ref('')
const loading = ref(false)
const hasMore = ref(true)
const currentPage = ref(0)
const pageSize = 20

// 体质筛选（从URL参数获取）
const constitutionFilter = ref('')

// 生命周期
onLoad((options) => {
  if (options.constitution) {
    constitutionFilter.value = options.constitution
  }
  loadData()
})

onMounted(() => {
  loadFilters()
})

// 加载筛选选项
async function loadFilters() {
  try {
    const [catRes, seasonRes] = await Promise.all([
      getCourseCategories(),
      getSeasons()
    ])
    if (catRes.code === 0) {
      categories.value = catRes.data
    }
    if (seasonRes.code === 0) {
      seasons.value = seasonRes.data
    }
  } catch (e) {
    console.error('加载筛选选项失败', e)
  }
}

// 加载课程列表
async function loadData(reset = true) {
  if (loading.value) return

  loading.value = true

  try {
    const params = {
      skip: reset ? 0 : currentPage.value * pageSize,
      limit: pageSize
    }

    if (selectedCategory.value) {
      params.category = selectedCategory.value
    }
    if (constitutionFilter.value) {
      params.constitution = constitutionFilter.value
    }
    if (selectedSeason.value) {
      // 使用 subcategory 参数传递季节
      params.subcategory = selectedSeason.value
    }

    const res = await getCoursesList(params)

    if (res.code === 0) {
      if (reset) {
        courses.value = res.data.items
      } else {
        courses.value.push(...res.data.items)
      }
      hasMore.value = courses.value.length < res.data.total
    }
  } catch (e) {
    console.error('加载课程列表失败', e)
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

// 选择分类
function selectCategory(value) {
  selectedCategory.value = value
  currentPage.value = 0
  loadData(true)
}

// 选择季节
function selectSeason(value) {
  selectedSeason.value = value
  currentPage.value = 0
  loadData(true)
}

// 加载更多
function loadMore() {
  if (!hasMore.value || loading.value) return
  currentPage.value++
  loadData(false)
}

// 获取内容类型图标
function getContentIcon(type) {
  const icons = {
    video: '🎥',
    article: '📖'
  }
  return icons[type] || '📚'
}

// 获取分类标签
function getCategoryLabel(category) {
  const cat = categories.value.find(c => c.value === category)
  return cat ? cat.label : category
}

// 格式化时长
function formatDuration(seconds) {
  if (!seconds) return ''
  const minutes = Math.floor(seconds / 60)
  if (minutes < 60) {
    return `${minutes}分钟`
  }
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  return mins > 0 ? `${hours}小时${mins}分` : `${hours}小时`
}

// 跳转详情
function goToDetail(id) {
  uni.navigateTo({
    url: `/pages/courses/detail?id=${id}`
  })
}
</script>

<style lang="scss" scoped>
.courses-list-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.filter-section {
  background: #fff;
  border-bottom: 1px solid #eee;
}

.filter-scroll {
  white-space: nowrap;
  padding: 10rpx 0;
  border-bottom: 1px solid #f5f5f5;
}

.filter-item {
  display: inline-block;
  padding: 10rpx 20rpx;
  margin: 0 10rpx;
  border-radius: 20rpx;
  font-size: 28rpx;
  background: #f5f5f5;
  color: #666;

  &.active {
    background: #1890ff;
    color: #fff;
  }
}

.courses-scroll {
  flex: 1;
  padding: 20rpx;
}

.courses-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.course-item {
  display: flex;
  background: #fff;
  border-radius: 16rpx;
  padding: 20rpx;
  gap: 20rpx;
}

.course-image {
  width: 200rpx;
  height: 150rpx;
  border-radius: 12rpx;
  flex-shrink: 0;

  &.placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f0f0f0;
  }
}

.placeholder-icon {
  font-size: 60rpx;
}

.course-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10rpx;
}

.course-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

.course-desc {
  font-size: 24rpx;
  color: #999;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

.course-meta {
  display: flex;
  gap: 10rpx;
  align-items: center;
}

.tag {
  padding: 4rpx 12rpx;
  border-radius: 8rpx;
  font-size: 24rpx;

  &.type {
    background: #e6f7ff;
    color: #1890ff;
  }
}

.duration {
  font-size: 24rpx;
  color: #999;
}

.course-author {
  display: flex;
  align-items: center;
  gap: 8rpx;
  font-size: 24rpx;
}

.author-icon {
  font-size: 28rpx;
}

.author-name {
  color: #333;
  font-weight: 500;
}

.author-title {
  color: #999;
}

.load-more {
  padding: 30rpx;
  text-align: center;
  color: #999;
  font-size: 28rpx;
}
</style>
