<template>
  <view class="ingredients-list-page">
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

      <scroll-view scroll-x class="filter-scroll">
        <view class="filter-item" :class="{ active: !selectedNature }" @click="selectNature('')">
          全部性味
        </view>
        <view
          v-for="nature in natures"
          :key="nature.value"
          class="filter-item"
          :class="{ active: selectedNature === nature.value }"
          @click="selectNature(nature.value)"
        >
          {{ nature.label }}
        </view>
      </scroll-view>
    </view>

    <!-- 食材列表 -->
    <scroll-view class="ingredients-scroll" scroll-y @scrolltolower="loadMore">
      <view class="ingredients-list">
        <view
          v-for="item in ingredients"
          :key="item.id"
          class="ingredient-item"
          @click="goToDetail(item.id)"
        >
          <image v-if="item.image_url" :src="item.image_url" class="ingredient-image" mode="aspectFill" />
          <view v-else class="ingredient-image placeholder">🥗</view>
          <view class="ingredient-info">
            <view class="ingredient-name">{{ item.name }}</view>
            <view class="ingredient-meta">
              <text class="tag category">{{ item.category }}</text>
              <text class="tag nature">{{ item.nature }}</text>
            </view>
            <view class="ingredient-efficacy">{{ item.efficacy }}</view>
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
import { getIngredientsList, getIngredientCategories, getIngredientNatures } from '@/api/ingredients.js'

// 数据
const ingredients = ref([])
const categories = ref([])
const natures = ref([])
const selectedCategory = ref('')
const selectedNature = ref('')
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
    const [catRes, natureRes] = await Promise.all([
      getIngredientCategories(),
      getIngredientNatures()
    ])
    if (catRes.code === 0) {
      categories.value = catRes.data
    }
    if (natureRes.code === 0) {
      natures.value = natureRes.data
    }
  } catch (e) {
    console.error('加载筛选选项失败', e)
  }
}

// 加载食材列表
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
    if (selectedNature.value) {
      params.nature = selectedNature.value
    }
    if (constitutionFilter.value) {
      params.constitution = constitutionFilter.value
    }

    const res = await getIngredientsList(params)

    if (res.code === 0) {
      if (reset) {
        ingredients.value = res.data.items
      } else {
        ingredients.value.push(...res.data.items)
      }
      hasMore.value = ingredients.value.length < res.data.total
    }
  } catch (e) {
    console.error('加载食材列表失败', e)
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

// 选择类别
function selectCategory(value) {
  selectedCategory.value = value
  currentPage.value = 0
  loadData(true)
}

// 选择性味
function selectNature(value) {
  selectedNature.value = value
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
    url: `/pages/ingredients/detail?id=${id}`
  })
}
</script>

<style lang="scss" scoped>
.ingredients-list-page {
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

.ingredients-scroll {
  flex: 1;
  padding: 20rpx;
}

.ingredients-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.ingredient-item {
  display: flex;
  background: #fff;
  border-radius: 16rpx;
  padding: 20rpx;
  gap: 20rpx;
}

.ingredient-image {
  width: 140rpx;
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

.ingredient-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10rpx;
}

.ingredient-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.ingredient-meta {
  display: flex;
  gap: 10rpx;
}

.tag {
  padding: 4rpx 12rpx;
  border-radius: 8rpx;
  font-size: 24rpx;

  &.category {
    background: #e6f7ff;
    color: #1890ff;
  }

  &.nature {
    background: #f6ffed;
    color: #52c41a;
  }
}

.ingredient-efficacy {
  font-size: 26rpx;
  color: #999;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

.load-more {
  padding: 30rpx;
  text-align: center;
  color: #999;
  font-size: 28rpx;
}
</style>
