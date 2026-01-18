<template>
  <view class="course-detail-page">
    <!-- 封面区域 -->
    <view class="cover-section">
      <image v-if="course.cover_image" :src="course.cover_image" class="cover-image" mode="aspectFill" />
      <view v-else class="cover-image placeholder">
        <text class="placeholder-icon">{{ getContentIcon(course.content_type) }}</text>
      </view>
      <view class="play-btn" @click="handlePlay" v-if="course.content_type === 'video'">
        <text class="play-icon">▶</text>
      </view>
    </view>

    <!-- 课程信息 -->
    <view class="info-card">
      <view class="course-title">{{ course.title }}</view>
      <view class="course-meta">
        <text class="tag type">{{ getCategoryLabel(course.category) }}</text>
        <text class="duration" v-if="course.duration">{{ formatDuration(course.duration) }}</text>
      </view>
    </view>

    <!-- 课程描述 -->
    <view class="info-card" v-if="course.description">
      <view class="card-title">课程简介</view>
      <view class="course-desc">{{ course.description }}</view>
    </view>

    <!-- 作者信息 -->
    <view class="info-card author" v-if="course.author">
      <view class="card-title">讲师介绍</view>
      <view class="author-info">
        <view class="author-name">{{ course.author }}</view>
        <view class="author-title" v-if="course.author_title">{{ course.author_title }}</view>
      </view>
    </view>

    <!-- 适用体质 -->
    <view class="info-card" v-if="course.suitable_constitutions && course.suitable_constitutions.length">
      <view class="card-title">适用体质</view>
      <view class="constitutions">
        <text
          v-for="code in course.suitable_constitutions"
          :key="code"
          class="constitution-tag"
        >
          {{ getConstitutionName(code) }}
        </text>
      </view>
    </view>

    <!-- 标签 -->
    <view class="info-card" v-if="course.tags && course.tags.length">
      <view class="card-title">课程标签</view>
      <view class="tags">
        <text v-for="tag in course.tags" :key="tag" class="tag-item">
          {{ tag }}
        </text>
      </view>
    </view>

    <!-- 操作按钮 -->
    <view class="action-section">
      <button class="action-btn primary" @click="handlePlay">
        <text v-if="course.content_type === 'video'">播放课程</text>
        <text v-else>阅读课程</text>
      </button>
      <button class="action-btn outline" @click="goBack">
        返回列表
      </button>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getCourseDetail } from '@/api/courses.js'

// 数据
const course = ref({})

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

// 分类映射
const categoryMap = {
  constitution: '体质调理',
  season: '季节养生',
  diet: '饮食养生',
  meridian: '经络养生'
}

onLoad((options) => {
  if (options.id) {
    loadDetail(options.id)
  }
})

async function loadDetail(id) {
  uni.showLoading({ title: '加载中...' })

  try {
    const res = await getCourseDetail(id)
    if (res.code === 0) {
      course.value = res.data
    }
  } catch (e) {
    console.error('加载课程详情失败', e)
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  } finally {
    uni.hideLoading()
  }
}

function getContentIcon(type) {
  const icons = {
    video: '🎥',
    article: '📖'
  }
  return icons[type] || '📚'
}

function getCategoryLabel(category) {
  return categoryMap[category] || category
}

function getConstitutionName(code) {
  return constitutionNames[code] || code
}

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

function handlePlay() {
  if (course.value.content_type === 'video') {
    // 视频播放
    if (course.value.content_url) {
      // TODO: 实现视频播放
      uni.showToast({
        title: '播放功能开发中',
        icon: 'none'
      })
    } else {
      uni.showToast({
        title: '暂无视频资源',
        icon: 'none'
      })
    }
  } else {
    // 文章阅读
    if (course.value.content_url) {
      uni.navigateTo({
        url: `/pages/webview/index?url=${encodeURIComponent(course.value.content_url)}`
      })
    } else {
      uni.showToast({
        title: '暂无文章内容',
        icon: 'none'
      })
    }
  }
}

function goBack() {
  uni.navigateBack()
}
</script>

<style lang="scss" scoped>
.course-detail-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 40rpx;
}

.cover-section {
  position: relative;
  width: 100%;
  height: 400rpx;
  background: #000;
}

.cover-image {
  width: 100%;
  height: 100%;

  &.placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    background: #333;
  }
}

.placeholder-icon {
  font-size: 150rpx;
}

.play-btn {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100rpx;
  height: 100rpx;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.play-icon {
  font-size: 40rpx;
  color: #333;
  margin-left: 5rpx;
}

.info-card {
  background: #fff;
  margin: 20rpx;
  padding: 30rpx;
  border-radius: 16rpx;

  &.author {
    background: #f0f9ff;
    border: 1px solid #bae7ff;
  }
}

.card-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.course-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  line-height: 1.4;
  margin-bottom: 20rpx;
}

.course-meta {
  display: flex;
  gap: 10rpx;
  align-items: center;
}

.tag {
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
  font-size: 24rpx;

  &.type {
    background: #e6f7ff;
    color: #1890ff;
  }
}

.duration {
  font-size: 26rpx;
  color: #999;
}

.course-desc {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
}

.author-info {
  display: flex;
  flex-direction: column;
  gap: 10rpx;
}

.author-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.author-title {
  font-size: 26rpx;
  color: #999;
}

.constitutions,
.tags {
  display: flex;
  gap: 10rpx;
  flex-wrap: wrap;
}

.constitution-tag,
.tag-item {
  font-size: 26rpx;
  padding: 8rpx 16rpx;
  border-radius: 20rpx;
}

.constitution-tag {
  background: #f0f5ff;
  color: #597ef7;
}

.tag-item {
  background: #f5f5f5;
  color: #666;
}

.action-section {
  padding: 30rpx;
  display: flex;
  gap: 20rpx;
}

.action-btn {
  flex: 1;
  height: 90rpx;
  border-radius: 45rpx;
  font-size: 30rpx;
  font-weight: bold;
  border: none;

  &.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
  }

  &.outline {
    background: #fff;
    color: #667eea;
    border: 2rpx solid #667eea;
  }
}
</style>
