<template>
  <view class="recipes-list-page">
    <!-- 顶部导航 -->
    <view class="nav-bar">
      <view class="nav-back" @click="goBack">
        <text class="back-icon">←</text>
        <text class="nav-title">食谱库</text>
      </view>
    </view>

    <!-- 整体滚动区域：包含筛选器和列表 -->
    <scroll-view class="main-scroll" scroll-y @scrolltolower="loadMore" refresher-enabled @refresherrefresh="onRefresh" :refresher-triggered="refreshing">
      <!-- 筛选器区域 -->
      <view class="filter-section">
        <scroll-view scroll-x class="filter-scroll">
          <view class="filter-label">体质:</view>
          <view class="filter-item" :class="{ active: !selectedConstitution }" @click="selectConstitution('')">
            全部
          </view>
          <view
            v-for="item in constitutions"
            :key="item.value"
            class="filter-item"
            :class="{ active: selectedConstitution === item.value }"
            @click="selectConstitution(item.value)"
          >
            {{ item.label }}
          </view>
        </scroll-view>

        <scroll-view scroll-x class="filter-scroll">
          <view class="filter-label">功效:</view>
          <view class="filter-item" :class="{ active: !selectedEfficacy }" @click="selectEfficacy('')">
            全部
          </view>
          <view
            v-for="item in commonEfficacyTags"
            :key="item"
            class="filter-item"
            :class="{ active: selectedEfficacy === item }"
            @click="selectEfficacy(item)"
          >
            {{ item }}
          </view>
        </scroll-view>

        <scroll-view scroll-x class="filter-scroll">
          <view class="filter-label">季节:</view>
          <view class="filter-item" :class="{ active: !selectedSeason }" @click="selectSeason('')">
            全部
          </view>
          <view
            v-for="item in seasons"
            :key="item.value"
            class="filter-item"
            :class="{ active: selectedSeason === item.value }"
            @click="selectSeason(item.value)"
          >
            {{ item.label }}
          </view>
        </scroll-view>

        <scroll-view scroll-x class="filter-scroll">
          <view class="filter-label">难度:</view>
          <view class="filter-item" :class="{ active: !selectedDifficulty }" @click="selectDifficulty('')">
            全部
          </view>
          <view
            v-for="item in difficulties"
            :key="item.value"
            class="filter-item"
            :class="{ active: selectedDifficulty === item.value }"
            @click="selectDifficulty(item.value)"
          >
            {{ item.label }}
          </view>
        </scroll-view>
      </view>

      <!-- 总数提示 -->
      <view v-if="total > 0" class="total-hint">
        <text>共 {{ total }} 道美食，已加载 {{ recipes.length }} 道</text>
      </view>

      <view class="recipes-list">
        <!-- 加载状态 -->
        <view v-if="loading && recipes.length === 0" class="loading-state">
          <text>加载中...</text>
        </view>

        <!-- 空状态 -->
        <view v-else-if="recipes.length === 0 && !loading" class="empty-state">
          <text class="empty-icon">🍲</text>
          <text class="empty-text">暂无食谱</text>
        </view>

        <!-- 食谱卡片 -->
        <view
          v-for="item in recipes"
          :key="item.id"
          class="recipe-card"
          @click="goToDetail(item.id)"
        >
          <image v-if="item.image_url" :src="item.image_url" class="recipe-cover" mode="aspectFill" />
          <view v-else class="recipe-cover placeholder">
            <text class="placeholder-icon">🍲</text>
          </view>
          <view class="recipe-content">
            <view class="recipe-header">
              <text class="recipe-name">{{ item.name }}</text>
              <view class="difficulty-badge" :class="item.difficulty">
                {{ getDifficultyName(item.difficulty) }}
              </view>
            </view>
            <view v-if="item.desc" class="recipe-desc">{{ item.desc }}</view>
            <view class="recipe-meta">
              <text v-if="item.cooking_time" class="meta-item">⏱ {{ item.cooking_time }}分钟</text>
              <text v-if="item.servings" class="meta-item">👤 {{ item.servings }}人份</text>
            </view>
            <view v-if="item.efficacy_tags && item.efficacy_tags.length" class="efficacy-tags">
              <text v-for="(tag, idx) in item.efficacy_tags.slice(0, 3)" :key="idx" class="efficacy-tag">
                {{ tag }}
              </text>
              <text v-if="item.efficacy_tags.length > 3" class="more-tags">+{{ item.efficacy_tags.length - 3 }}</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 加载更多 -->
      <view class="load-more">
        <text v-if="loading && recipes.length > 0">加载中...</text>
        <text v-else-if="!hasMore">已加载全部 {{ total }} 道美食</text>
        <text v-else>下拉加载更多 ({{ recipes.length }}/{{ total }})</text>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getRecipesList, CONSTITUTIONS, SEASONS, DIFFICULTIES, getConstitutionName, getDifficultyName } from '@/api/recipes.js'

// 数据
const recipes = ref([])
const constitutions = ref(CONSTITUTIONS)
const seasons = ref(SEASONS)
const difficulties = ref(DIFFICULTIES)
// 常用功效标签（从后端数据中选取的常见标签）
const commonEfficacyTags = ref([
  '补气', '补血', '滋阴', '助阳', '健脾', '养胃',
  '润肺', '补肾', '疏肝', '安神', '祛湿', '清热',
  '消食', '止咳', '化痰', '美容', '瘦身'
])
const selectedConstitution = ref('')
const selectedSeason = ref('')
const selectedDifficulty = ref('')
const selectedEfficacy = ref('')
const loading = ref(false)
const refreshing = ref(false)
const hasMore = ref(true)
const currentPage = ref(1)
const pageSize = 100  // 每页显示100条
const total = ref(0)

// 生命周期
onLoad((options) => {
  if (options.constitution) {
    selectedConstitution.value = options.constitution
  }
  loadData(true)
})

onMounted(() => {
  // 组件已挂载
})

// 下拉刷新
function onRefresh() {
  refreshing.value = true
  loadData(true).finally(() => {
    refreshing.value = false
  })
}

// 加载食谱列表
async function loadData(reset = true) {
  if (loading.value && !refreshing.value) return

  loading.value = true

  try {
    const params = {
      page: reset ? 1 : currentPage.value + 1,
      page_size: pageSize
    }

    if (selectedConstitution.value) {
      params.constitution = selectedConstitution.value
    }
    if (selectedSeason.value) {
      params.season = selectedSeason.value
    }
    if (selectedDifficulty.value) {
      params.difficulty = selectedDifficulty.value
    }
    if (selectedEfficacy.value) {
      params.efficacy = selectedEfficacy.value
    }

    const res = await getRecipesList(params)

    if (res.code === 0) {
      if (reset) {
        recipes.value = res.data.items || []
        currentPage.value = 1
      } else {
        recipes.value.push(...(res.data.items || []))
        currentPage.value++
      }
      total.value = res.data.total || 0
      hasMore.value = recipes.value.length < total.value
    }
  } catch (e) {
    console.error('加载食谱列表失败', e)
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

// 选择体质
function selectConstitution(value) {
  selectedConstitution.value = value
  loadData(true)
}

// 选择季节
function selectSeason(value) {
  selectedSeason.value = value
  loadData(true)
}

// 选择难度
function selectDifficulty(value) {
  selectedDifficulty.value = value
  loadData(true)
}

// 选择功效
function selectEfficacy(value) {
  selectedEfficacy.value = value
  loadData(true)
}

// 加载更多
function loadMore() {
  if (!hasMore.value || loading.value) return
  loadData(false)
}

// 跳转详情
function goToDetail(id) {
  uni.navigateTo({
    url: `/pages/recipes/detail?id=${id}`
  })
}

// 返回
function goBack() {
  uni.navigateBack()
}
</script>

<style lang="scss" scoped>
.recipes-list-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.nav-bar {
  background: #fff;
  padding: 20rpx 30rpx;
  border-bottom: 1px solid #eee;
}

.nav-back {
  display: flex;
  align-items: center;
  gap: 10rpx;
}

.back-icon {
  font-size: 40rpx;
  color: #333;
}

.nav-title {
  font-size: 36rpx;
  font-weight: 600;
  color: #333;
}

.filter-section {
  background: #fff;
  border-bottom: 1px solid #eee;
}

.filter-scroll {
  display: flex;
  white-space: nowrap;
  padding: 20rpx 0;
  border-bottom: 1px solid #f5f5f5;

  &:last-child {
    border-bottom: none;
  }
}

.filter-label {
  padding: 0 20rpx;
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
  display: flex;
  align-items: center;
}

.filter-item {
  display: inline-flex;
  align-items: center;
  padding: 12rpx 24rpx;
  margin: 0 10rpx;
  border-radius: 40rpx;
  font-size: 26rpx;
  background: #f5f5f5;
  color: #666;
  white-space: nowrap;
  transition: all 0.3s;

  &.active {
    background: #1890ff;
    color: #fff;
  }
}

.main-scroll {
  flex: 1;
  height: 0; /* 确保flex子元素正确计算高度 */
  overflow-y: auto;
}

.total-hint {
  padding: 20rpx 30rpx;
  text-align: center;
  font-size: 26rpx;
  color: #999;
  background: #fff;
  border-bottom: 1px solid #eee;
}

.recipes-list {
  padding: 20rpx;
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.loading-state, .empty-state {
  padding: 100rpx 0;
  text-align: center;
  color: #999;
  font-size: 28rpx;
}

.empty-icon {
  display: block;
  font-size: 100rpx;
  margin-bottom: 20rpx;
}

.empty-text {
  display: block;
  font-size: 28rpx;
  color: #999;
}

.recipe-card {
  display: flex;
  background: #fff;
  border-radius: 16rpx;
  overflow: hidden;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
}

.recipe-cover {
  width: 200rpx;
  height: 200rpx;
  flex-shrink: 0;

  &.placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }
}

.placeholder-icon {
  font-size: 80rpx;
}

.recipe-content {
  flex: 1;
  padding: 20rpx;
  display: flex;
  flex-direction: column;
  gap: 10rpx;
}

.recipe-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10rpx;
}

.recipe-name {
  flex: 1;
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.difficulty-badge {
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
  font-size: 22rpx;
  font-weight: 500;
  flex-shrink: 0;

  &.easy {
    background: #f6ffed;
    color: #52c41a;
  }

  &.medium {
    background: #fff7e6;
    color: #fa8c16;
  }

  &.harder {
    background: #fff1f0;
    color: #ff4d4f;
  }

  &.hard {
    background: #5c0011;
    color: #fff;
  }
}

.recipe-desc {
  font-size: 24rpx;
  color: #999;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.recipe-meta {
  display: flex;
  gap: 20rpx;
  flex-wrap: wrap;
}

.meta-item {
  font-size: 24rpx;
  color: #999;
}

.efficacy-tags {
  display: flex;
  gap: 10rpx;
  flex-wrap: wrap;
}

.efficacy-tag {
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
  font-size: 22rpx;
  background: #f0f5ff;
  color: #597ef7;
}

.more-tags {
  font-size: 22rpx;
  color: #999;
  padding: 6rpx 0;
}

.load-more {
  padding: 30rpx;
  text-align: center;
  color: #999;
  font-size: 26rpx;
}
</style>
