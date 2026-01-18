<template>
  <view class="acupoints-list-page">
    <!-- 搜索栏 -->
    <view class="search-section">
      <view class="search-bar">
        <text class="search-icon">🔍</text>
        <input
          class="search-input"
          placeholder="搜索穴位名称或症状"
          v-model="searchKeyword"
          @confirm="handleSearch"
        />
      </view>
    </view>

    <!-- 顶部筛选区 -->
    <view class="filter-section">
      <scroll-view scroll-x class="filter-scroll">
        <view class="filter-item" :class="{ active: !selectedBodyPart }" @click="selectBodyPart('')">
          全部部位
        </view>
        <view
          v-for="part in bodyParts"
          :key="part.value"
          class="filter-item"
          :class="{ active: selectedBodyPart === part.value }"
          @click="selectBodyPart(part.value)"
        >
          {{ part.label }}
        </view>
      </scroll-view>
    </view>

    <!-- 穴位列表 -->
    <scroll-view class="acupoints-scroll" scroll-y @scrolltolower="loadMore">
      <view class="acupoints-list">
        <view
          v-for="item in acupoints"
          :key="item.id"
          class="acupoint-item"
          @click="goToDetail(item.id)"
        >
          <view class="acupoint-header">
            <view class="acupoint-name">{{ item.name }}</view>
            <view class="acupoint-code">{{ item.code }}</view>
          </view>
          <view class="acupoint-meridian">{{ item.meridian }}</view>
          <view class="acupoint-location">{{ item.location }}</view>
          <view class="acupoint-efficacy" v-if="item.efficacy && item.efficacy.length">
            <text class="efficacy-tag" v-for="(efficacy, index) in item.efficacy.slice(0, 3)" :key="index">
              {{ efficacy }}
            </text>
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
import {
  getAcupointsList,
  getBodyParts,
  getAcupointsBySymptom
} from '@/api/acupoints.js'

// 数据
const acupoints = ref([])
const bodyParts = ref([])
const selectedBodyPart = ref('')
const searchKeyword = ref('')
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
    const res = await getBodyParts()
    if (res.code === 0) {
      bodyParts.value = res.data
    }
  } catch (e) {
    console.error('加载筛选选项失败', e)
  }
}

// 加载穴位列表
async function loadData(reset = true) {
  if (loading.value) return

  loading.value = true

  try {
    const params = {
      skip: reset ? 0 : currentPage.value * pageSize,
      limit: pageSize
    }

    if (selectedBodyPart.value) {
      params.body_part = selectedBodyPart.value
    }
    if (constitutionFilter.value) {
      params.constitution = constitutionFilter.value
    }

    const res = await getAcupointsList(params)

    if (res.code === 0) {
      if (reset) {
        acupoints.value = res.data.items
      } else {
        acupoints.value.push(...res.data.items)
      }
      hasMore.value = acupoints.value.length < res.data.total
    }
  } catch (e) {
    console.error('加载穴位列表失败', e)
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

// 搜索穴位/症状
async function handleSearch() {
  if (!searchKeyword.value.trim()) {
    loadData(true)
    return
  }

  loading.value = true

  try {
    // 先搜索症状
    const symptomRes = await getAcupointsBySymptom(searchKeyword.value)

    if (symptomRes.code === 0 && symptomRes.data.items.length > 0) {
      acupoints.value = symptomRes.data.items
      hasMore.value = false
      return
    }

    // 症状无结果，搜索穴位名称
    const res = await getAcupointsList({
      skip: 0,
      limit: 50,
      search: searchKeyword.value
    })

    if (res.code === 0) {
      acupoints.value = res.data.items
      hasMore.value = acupoints.value.length < res.data.total
    }
  } catch (e) {
    console.error('搜索失败', e)
    uni.showToast({
      title: '搜索失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

// 选择部位
function selectBodyPart(value) {
  selectedBodyPart.value = value
  currentPage.value = 0
  loadData(true)
}

// 加载更多
function loadMore() {
  if (!hasMore.value || loading.value) return
  currentPage.value++
  loadData(false)
}

// 跳转详情
function goToDetail(id) {
  uni.navigateTo({
    url: `/pages/acupoints/detail?id=${id}`
  })
}
</script>

<style lang="scss" scoped>
.acupoints-list-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.search-section {
  background: #fff;
  padding: 20rpx;
  border-bottom: 1px solid #eee;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 15rpx;
  padding: 15rpx 25rpx;
  background: #f5f5f5;
  border-radius: 30rpx;
}

.search-icon {
  font-size: 32rpx;
}

.search-input {
  flex: 1;
  font-size: 28rpx;
  color: #333;
}

.filter-section {
  background: #fff;
  border-bottom: 1px solid #eee;
}

.filter-scroll {
  white-space: nowrap;
  padding: 15rpx 0;
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

.acupoints-scroll {
  flex: 1;
  padding: 20rpx;
}

.acupoints-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.acupoint-item {
  background: #fff;
  border-radius: 16rpx;
  padding: 25rpx;
}

.acupoint-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15rpx;
}

.acupoint-name {
  font-size: 34rpx;
  font-weight: bold;
  color: #333;
}

.acupoint-code {
  font-size: 24rpx;
  color: #999;
  padding: 5rpx 12rpx;
  background: #f5f5f5;
  border-radius: 8rpx;
}

.acupoint-meridian {
  font-size: 26rpx;
  color: #1890ff;
  margin-bottom: 10rpx;
}

.acupoint-location {
  font-size: 26rpx;
  color: #666;
  margin-bottom: 15rpx;
  line-height: 1.5;
}

.acupoint-efficacy {
  display: flex;
  gap: 10rpx;
  flex-wrap: wrap;
}

.efficacy-tag {
  font-size: 24rpx;
  padding: 5rpx 12rpx;
  background: #f6ffed;
  color: #52c41a;
  border-radius: 8rpx;
}

.load-more {
  padding: 30rpx;
  text-align: center;
  color: #999;
  font-size: 28rpx;
}
</style>
