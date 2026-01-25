<template>
  <view class="acupoint-list">
    <!-- 搜索框 -->
    <view class="search-bar">
      <view class="search-input-wrapper">
        <text class="search-icon">🔍</text>
        <input
          v-model="keyword"
          class="search-input"
          placeholder="搜索穴位名称/拼音"
          @confirm="handleSearch"
        />
        <text v-if="keyword" class="clear-icon" @click="clearSearch">✕</text>
      </view>
    </view>

    <!-- Tab 切换 -->
    <view class="tabs">
      <view
        :class="['tab', { active: activeTab === 'meridian' }]"
        @click="switchTab('meridian')"
      >按经络</view>
      <view
        :class="['tab', { active: activeTab === 'part' }]"
        @click="switchTab('part')"
      >按部位</view>
    </view>

    <!-- 主内容区：左右分栏 -->
    <view class="content-area">
      <!-- 左侧分类菜单 -->
      <scroll-view class="side-menu" scroll-y>
        <view
          v-for="item in sideMenuItems"
          :key="item.value"
          class="menu-item"
          :class="{ active: selectedSideMenu === item.value }"
          @click="selectMenu(item.value)"
        >
          {{ item.label }}
        </view>
      </scroll-view>

      <!-- 右侧穴位列表 -->
      <scroll-view class="main-list" scroll-y @scrolltolower="loadMore">
        <view class="section-header">
          <text class="section-title">{{ selectedMenuLabel }}</text>
        </view>

        <view class="acupoint-grid">
          <view
            v-for="point in acupoints"
            :key="point.id"
            class="acupoint-card"
            @click="goDetail(point.id)"
          >
            <text class="name">{{ point.name }}</text>
            <text class="pinyin">{{ point.pinyin || point.code }}</text>
          </view>
        </view>

        <!-- 加载状态 -->
        <view class="load-more">
          <text v-if="loading">加载中...</text>
          <text v-else-if="!hasMore && acupoints.length > 0">没有更多了</text>
          <text v-else-if="acupoints.length === 0 && !loading" class="empty-text">暂无数据</text>
        </view>
      </scroll-view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import {
  getAcupointsList,
  getBodyParts,
  getMeridians,
  searchAcupoints
} from '@/api/acupoints.js'

// 状态
const activeTab = ref('meridian') // 'meridian' | 'part'
const keyword = ref('')
const sideMenuItems = ref([])
const selectedSideMenu = ref('')
const acupoints = ref([])
const loading = ref(false)
const hasMore = ref(true)
const currentPage = ref(0)
const pageSize = 20

// 计算属性：当前选中的菜单标签
const selectedMenuLabel = computed(() => {
  const item = sideMenuItems.value.find(i => i.value === selectedSideMenu.value)
  return item ? item.label : ''
})

// 生命周期
onLoad(() => {
  initData()
})

// 初始化
async function initData() {
  await loadSideMenuData()
}

// 切换 Tab
async function switchTab(tab) {
  if (activeTab.value === tab) return
  activeTab.value = tab
  selectedSideMenu.value = '' // 重置选中项
  acupoints.value = [] // 清空列表
  keyword.value = '' // 清空搜索
  await loadSideMenuData()
}

// 加载侧边栏数据
async function loadSideMenuData() {
  try {
    let res
    if (activeTab.value === 'part') {
      res = await getBodyParts()
    } else if (activeTab.value === 'meridian') {
      res = await getMeridians()
    }

    if (res.code === 0) {
      sideMenuItems.value = res.data
      // 默认选中第一个
      if (sideMenuItems.value.length > 0 && !keyword.value) {
        selectMenu(sideMenuItems.value[0].value)
      }
    }
  } catch (error) {
    console.error('Failed to load menu data:', error)
  }
}

// 选择菜单项
function selectMenu(value) {
  if (selectedSideMenu.value === value) return
  selectedSideMenu.value = value
  // 重置分页并加载数据
  currentPage.value = 0
  acupoints.value = []
  hasMore.value = true
  loadAcupoints()
}

// 搜索处理
function handleSearch() {
  currentPage.value = 0
  acupoints.value = []
  hasMore.value = true
  loadAcupoints()
}

// 清除搜索
function clearSearch() {
  keyword.value = ''
  handleSearch()
}

// 加载穴位数据
async function loadAcupoints() {
  if (loading.value) return

  loading.value = true
  try {
    const params = {
      skip: currentPage.value * pageSize,
      limit: pageSize
    }

    // 搜索关键词优先
    if (keyword.value) {
      params.search = keyword.value
    } else if (selectedSideMenu.value) {
      // 根据当前 Tab 添加筛选参数
      if (activeTab.value === 'part') {
        params.body_part = selectedSideMenu.value
      } else if (activeTab.value === 'meridian') {
        params.meridian = selectedSideMenu.value
      }
    }

    const res = await getAcupointsList(params)
    if (res.code === 0) {
      const newItems = res.data.items || res.data || []
      if (newItems.length < pageSize) {
        hasMore.value = false
      }
      acupoints.value = [...acupoints.value, ...newItems]
      currentPage.value++
    }
  } catch (error) {
    console.error('Failed to load acupoints:', error)
  } finally {
    loading.value = false
  }
}

// 加载更多
function loadMore() {
  if (hasMore.value && !loading.value) {
    loadAcupoints()
  }
}

// 跳转详情
function goDetail(id) {
  uni.navigateTo({
    url: `/pages/acupoints/detail?id=${id}`
  })
}
</script>

<style lang="scss">
.acupoint-list {
  background: #f5f5f5;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 搜索框 */
.search-bar {
  padding: 20rpx;
  background: #fff;

  .search-input-wrapper {
    display: flex;
    align-items: center;
    height: 70rpx;
    background: #f5f5f5;
    border-radius: 35rpx;
    padding: 0 30rpx;

    .search-icon {
      font-size: 32rpx;
      margin-right: 15rpx;
    }

    .search-input {
      flex: 1;
      height: 100%;
      font-size: 28rpx;
      color: #333;
    }

    .clear-icon {
      font-size: 28rpx;
      color: #999;
      padding: 10rpx;
    }
  }
}

/* Tab 切换 */
.tabs {
  display: flex;
  background: #fff;
  border-bottom: 1rpx solid #eee;

  .tab {
    flex: 1;
    text-align: center;
    padding: 30rpx 0;
    font-size: 32rpx;
    color: #666;
    position: relative;

    &.active {
      color: #1acc76;
      font-weight: bold;

      &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 60rpx;
        height: 4rpx;
        background-color: #1acc76;
        border-radius: 2rpx;
      }
    }
  }
}

/* 内容区：左右分栏 */
.content-area {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* 左侧分类菜单 */
.side-menu {
  width: 200rpx;
  background: #f0f2f5;
  height: 100%;

  .menu-item {
    height: 100rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26rpx;
    color: #666;
    border-bottom: 1rpx solid #e8e8e8;
    position: relative;

    &.active {
      background: #fff;
      color: #1acc76;
      font-weight: 500;

      &::before {
        content: '';
        position: absolute;
        left: 0;
        top: 30rpx;
        bottom: 30rpx;
        width: 6rpx;
        background-color: #1acc76;
        border-radius: 0 4rpx 4rpx 0;
      }
    }
  }
}

/* 右侧穴位列表 */
.main-list {
  flex: 1;
  background: #fff;
  height: 100%;
  padding: 20rpx;
  box-sizing: border-box;
}

.section-header {
  padding: 10rpx 0 20rpx;

  .section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    position: relative;
    padding-left: 20rpx;

    &::before {
      content: '';
      position: absolute;
      left: 0;
      top: 50%;
      transform: translateY(-50%);
      width: 6rpx;
      height: 24rpx;
      background-color: #1acc76;
      border-radius: 3rpx;
    }
  }
}

/* 穴位网格 */
.acupoint-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20rpx;
}

.acupoint-card {
  background: #fff;
  border-radius: 16rpx;
  padding: 30rpx 20rpx;
  text-align: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
  border: 1rpx solid #f0f0f0;
  transition: all 0.3s;

  &:active {
    transform: scale(0.98);
    box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
  }

  .name {
    display: block;
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 10rpx;
  }

  .pinyin {
    display: block;
    font-size: 24rpx;
    color: #999;
  }
}

/* 加载状态 */
.load-more {
  text-align: center;
  padding: 30rpx 0;
  color: #999;
  font-size: 24rpx;

  .empty-text {
    padding-top: 100rpx;
    display: block;
    color: #ccc;
  }
}
</style>
