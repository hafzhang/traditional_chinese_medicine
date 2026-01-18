<template>
  <view class="recipes-list-page">
    <!-- 顶部筛选区 -->
    <view class="filter-section">
      <scroll-view scroll-x class="filter-scroll">
        <view class="filter-item" :class="{ active: !selectedType }" @click="selectType('')">
          全部类型
        </view>
        <view
          v-for="type in recipeTypes"
          :key="type.value"
          class="filter-item"
          :class="{ active: selectedType === type.value }"
          @click="selectType(type.value)"
        >
          {{ type.label }}
        </view>
      </scroll-view>

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

    <!-- 食谱列表 -->
    <scroll-view class="recipes-scroll" scroll-y @scrolltolower="loadMore">
      <view class="recipes-list">
        <view
          v-for="item in recipes"
          :key="item.id"
          class="recipe-item"
          @click="goToDetail(item.id)"
        >
          <image v-if="item.image_url" :src="item.image_url" class="recipe-image" mode="aspectFill" />
          <view v-else class="recipe-image placeholder">🍲</view>
          <view class="recipe-info">
            <view class="recipe-name">{{ item.name }}</view>
            <view class="recipe-meta">
              <text class="tag type">{{ item.type }}</text>
              <text class="tag difficulty" :class="item.difficulty">{{ item.difficulty }}</text>
              <text class="time">⏱ {{ item.cook_time }}分钟</text>
            </view>
            <view class="recipe-serving">👤 {{ item.servings }}人份</view>
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
import { getRecipesList, getRecipeTypes, getRecipeDifficulties } from '@/api/recipes.js'

// 数据
const recipes = ref([])
const recipeTypes = ref([])
const difficulties = ref([])
const selectedType = ref('')
const selectedDifficulty = ref('')
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
    const [typeRes, diffRes] = await Promise.all([
      getRecipeTypes(),
      getRecipeDifficulties()
    ])
    if (typeRes.code === 0) {
      recipeTypes.value = typeRes.data
    }
    if (diffRes.code === 0) {
      difficulties.value = diffRes.data
    }
  } catch (e) {
    console.error('加载筛选选项失败', e)
  }
}

// 加载食谱列表
async function loadData(reset = true) {
  if (loading.value) return

  loading.value = true

  try {
    const params = {
      skip: reset ? 0 : currentPage.value * pageSize,
      limit: pageSize
    }

    if (selectedType.value) {
      params.type = selectedType.value
    }
    if (selectedDifficulty.value) {
      params.difficulty = selectedDifficulty.value
    }
    if (constitutionFilter.value) {
      params.constitution = constitutionFilter.value
    }

    const res = await getRecipesList(params)

    if (res.code === 0) {
      if (reset) {
        recipes.value = res.data.items
      } else {
        recipes.value.push(...res.data.items)
      }
      hasMore.value = recipes.value.length < res.data.total
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

// 选择类型
function selectType(value) {
  selectedType.value = value
  currentPage.value = 0
  loadData(true)
}

// 选择难度
function selectDifficulty(value) {
  selectedDifficulty.value = value
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
    url: `/pages/recipes/detail?id=${id}`
  })
}
</script>

<style lang="scss" scoped>
.recipes-list-page {
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

.recipes-scroll {
  flex: 1;
  padding: 20rpx;
}

.recipes-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.recipe-item {
  display: flex;
  background: #fff;
  border-radius: 16rpx;
  padding: 20rpx;
  gap: 20rpx;
}

.recipe-image {
  width: 180rpx;
  height: 140rpx;
  border-radius: 12rpx;
  flex-shrink: 0;

  &.placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f0f0f0;
    font-size: 60rpx;
  }
}

.recipe-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10rpx;
}

.recipe-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.recipe-meta {
  display: flex;
  gap: 10rpx;
  align-items: center;
  flex-wrap: wrap;
}

.tag {
  padding: 4rpx 12rpx;
  border-radius: 8rpx;
  font-size: 24rpx;

  &.type {
    background: #e6f7ff;
    color: #1890ff;
  }

  &.difficulty {
    &.简单 {
      background: #f6ffed;
      color: #52c41a;
    }
    &.中等 {
      background: #fff7e6;
      color: #fa8c16;
    }
    &.困难 {
      background: #fff1f0;
      color: #ff4d4f;
    }
  }
}

.time, .recipe-serving {
  font-size: 24rpx;
  color: #999;
}

.load-more {
  padding: 30rpx;
  text-align: center;
  color: #999;
  font-size: 28rpx;
}
</style>
