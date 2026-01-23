<template>
  <view class="acupoints-list-page">
    <!-- 顶部 Tabs -->
    <view class="tabs-header">
      <view 
        class="tab-item" 
        :class="{ active: currentTab === 'meridian' }"
        @click="switchTab('meridian')"
      >
        经脉
      </view>
      <view 
        class="tab-item" 
        :class="{ active: currentTab === 'part' }"
        @click="switchTab('part')"
      >
        部位
      </view>
      <!-- 暂时隐藏首字母功能，待后续完善 -->
      <!-- <view 
        class="tab-item" 
        :class="{ active: currentTab === 'pinyin' }"
        @click="switchTab('pinyin')"
      >
        首字母
      </view> -->
    </view>

    <!-- 主内容区：左右分栏 -->
    <view class="content-area">
      <!-- 左侧侧边栏 -->
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

      <!-- 右侧内容区 -->
      <scroll-view class="main-list" scroll-y @scrolltolower="loadMore">
        <view class="section-header">
          <text class="section-title">{{ selectedMenuLabel }}</text>
        </view>

        <view class="acupoint-grid">
          <view 
            v-for="item in acupoints" 
            :key="item.id" 
            class="acupoint-card"
            @click="goToDetail(item.id)"
          >
            <view class="card-image-wrapper">
              <!-- 占位图，实际项目中应替换为真实图片 -->
              <image 
                :src="item.image_url || '/static/acupoints/default.png'" 
                mode="aspectFill" 
                class="acupoint-image"
              />
              <view class="acupoint-code-badge" v-if="item.code">{{ item.code }}</view>
            </view>
            <view class="card-info">
              <text class="acupoint-name">{{ item.name }}</text>
              <text class="acupoint-brief" v-if="item.location">{{ item.location }}</text>
            </view>
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
import { ref, computed, watch, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import {
  getAcupointsList,
  getBodyParts,
  getMeridians
} from '@/api/acupoints.js'

// 状态
const currentTab = ref('meridian') // 'meridian' | 'part'
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
  if (currentTab.value === tab) return
  currentTab.value = tab
  selectedSideMenu.value = '' // 重置选中项
  acupoints.value = [] // 清空列表
  await loadSideMenuData()
}

// 加载侧边栏数据
async function loadSideMenuData() {
  try {
    let res
    if (currentTab.value === 'part') {
      res = await getBodyParts()
    } else if (currentTab.value === 'meridian') {
      res = await getMeridians()
    }
    
    if (res.code === 0) {
      sideMenuItems.value = res.data
      // 默认选中第一个
      if (sideMenuItems.value.length > 0) {
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

// 加载穴位数据
async function loadAcupoints() {
  if (loading.value || !selectedSideMenu.value) return
  
  loading.value = true
  try {
    const params = {
      skip: currentPage.value * pageSize,
      limit: pageSize
    }
    
    // 根据当前 Tab 添加筛选参数
    if (currentTab.value === 'part') {
      params.body_part = selectedSideMenu.value
    } else if (currentTab.value === 'meridian') {
      params.meridian = selectedSideMenu.value
    }
    
    const res = await getAcupointsList(params)
    if (res.code === 0) {
      const newItems = res.data.items
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
function goToDetail(id) {
  uni.navigateTo({
    url: `/pages/acupoints/detail?id=${id}`
  })
}
</script>

<style lang="scss">
.acupoints-list-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
}

/* 顶部 Tabs */
.tabs-header {
  display: flex;
  background-color: #fff;
  border-bottom: 1rpx solid #eee;
  height: 88rpx;
  flex-shrink: 0;
  
  .tab-item {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30rpx;
    color: #666;
    position: relative;
    
    &.active {
      color: #2b9939; // 主题色
      font-weight: bold;
      
      &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 40rpx;
        height: 4rpx;
        background-color: #2b9939;
        border-radius: 2rpx;
      }
    }
  }
}

/* 内容区 */
.content-area {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* 左侧菜单 */
.side-menu {
  width: 200rpx;
  background-color: #f0f2f5;
  height: 100%;
  
  .menu-item {
    height: 100rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28rpx;
    color: #666;
    border-bottom: 1rpx solid #e8e8e8;
    position: relative;
    
    &.active {
      background-color: #fff;
      color: #2b9939;
      font-weight: 500;
      
      &::before {
        content: '';
        position: absolute;
        left: 0;
        top: 30rpx;
        bottom: 30rpx;
        width: 6rpx;
        background-color: #2b9939;
        border-radius: 0 4rpx 4rpx 0;
      }
    }
  }
}

/* 右侧列表 */
.main-list {
  flex: 1;
  background-color: #fff;
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
      width: 8rpx;
      height: 24rpx;
      background-color: #2b9939;
      border-radius: 4rpx;
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
  background-color: #fff;
  border-radius: 12rpx;
  overflow: hidden;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
  border: 1rpx solid #f0f0f0;
  
  .card-image-wrapper {
    width: 100%;
    height: 200rpx;
    position: relative;
    background-color: #f8f8f8;
    
    .acupoint-image {
      width: 100%;
      height: 100%;
    }
    
    .acupoint-code-badge {
      position: absolute;
      top: 10rpx;
      right: 10rpx;
      background-color: rgba(0, 0, 0, 0.5);
      color: #fff;
      font-size: 20rpx;
      padding: 4rpx 10rpx;
      border-radius: 20rpx;
    }
  }
  
  .card-info {
    padding: 16rpx;
    
    .acupoint-name {
      display: block;
      font-size: 28rpx;
      font-weight: bold;
      color: #333;
      margin-bottom: 8rpx;
      text-align: center;
    }
    
    .acupoint-brief {
      display: block;
      font-size: 22rpx;
      color: #999;
      text-align: center;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }
}

.load-more {
  text-align: center;
  padding: 30rpx 0;
  color: #999;
  font-size: 24rpx;
  
  .empty-text {
    padding-top: 100rpx;
    display: block;
  }
}
</style>
