<template>
  <view class="recipes-list-page">
    <!-- 顶部筛选区 -->
    <view class="filter-section">
      <!-- 体质筛选 -->
      <scroll-view scroll-x class="filter-scroll">
        <view class="filter-item" :class="{ active: !store.filters.constitution }" @click="selectConstitution('')">
          全部体质
        </view>
        <view
          v-for="constitution in constitutions"
          :key="constitution.value"
          class="filter-item"
          :class="{ active: store.filters.constitution === constitution.value }"
          @click="selectConstitution(constitution.value)"
        >
          {{ constitution.label }}
        </view>
      </scroll-view>

      <!-- 功效筛选 -->
      <scroll-view scroll-x class="filter-scroll">
        <view class="filter-item" :class="{ active: !store.filters.efficacy }" @click="selectEfficacy('')">
          全部功效
        </view>
        <view
          v-for="efficacy in efficacies"
          :key="efficacy"
          class="filter-item"
          :class="{ active: store.filters.efficacy === efficacy }"
          @click="selectEfficacy(efficacy)"
        >
          {{ efficacy }}
        </view>
      </scroll-view>

      <!-- 难度筛选 -->
      <scroll-view scroll-x class="filter-scroll">
        <view class="filter-item" :class="{ active: !store.filters.difficulty }" @click="selectDifficulty('')">
          全部难度
        </view>
        <view
          v-for="diff in difficulties"
          :key="diff.value"
          class="filter-item"
          :class="{ active: store.filters.difficulty === diff.value }"
          @click="selectDifficulty(diff.value)"
        >
          {{ diff.label }}
        </view>
      </scroll-view>
    </view>

    <!-- 下拉刷新容器 -->
    <scroll-view
      class="recipes-scroll"
      scroll-y
      refresher-enabled
      :refresher-triggered="refreshing"
      @refresherrefresh="onRefresh"
      @scrolltolower="onScrollToLower"
    >
      <!-- 空状态 -->
      <view v-if="!store.loading && store.recipes.length === 0" class="empty-state">
        <text class="empty-icon">🍳</text>
        <text class="empty-text">暂无菜谱</text>
      </view>

      <!-- 菜谱列表 -->
      <view v-else class="recipes-list">
        <view
          v-for="item in store.recipes"
          :key="item.id"
          class="recipe-item"
          @click="goToDetail(item.id)"
        >
          <!-- 封面图 (lazy-load) -->
          <image
            v-if="item.cover_image"
            :src="item.cover_image"
            class="recipe-image"
            mode="aspectFill"
            lazy-load
            @error="onImageError($event, item)"
          />
          <view v-else class="recipe-image placeholder">
            <text class="placeholder-icon">🍲</text>
          </view>

          <!-- 菜谱信息 -->
          <view class="recipe-info">
            <view class="recipe-name">{{ item.name }}</view>
            <view v-if="item.description" class="recipe-desc">{{ item.description }}</view>

            <!-- 元信息标签 -->
            <view class="recipe-meta">
              <!-- 难度标签 -->
              <text v-if="item.difficulty" class="tag difficulty" :class="getDifficultyClass(item.difficulty)">
                {{ getDifficultyLabel(item.difficulty) }}
              </text>

              <!-- 烹饪时间 -->
              <text v-if="item.cooking_time" class="time">⏱ {{ item.cooking_time }}分钟</text>

              <!-- 热量 -->
              <text v-if="item.calories" class="calories">🔥 {{ item.calories }}kcal</text>
            </view>

            <!-- 功效标签 -->
            <view v-if="item.efficacy_tags && item.efficacy_tags.length > 0" class="recipe-tags">
              <text
                v-for="tag in item.efficacy_tags.slice(0, 3)"
                :key="tag"
                class="tag efficacy"
              >
                {{ tag }}
              </text>
            </view>

            <!-- 体质标签 -->
            <view v-if="item.suitable_constitutions && item.suitable_constitutions.length > 0" class="recipe-constitutions">
              <text class="constitution-label">适合:</text>
              <text
                v-for="c in item.suitable_constitutions.slice(0, 2)"
                :key="c"
                class="constitution-tag"
              >
                {{ getConstitutionLabel(c) }}
              </text>
            </view>
          </view>
        </view>
      </view>

      <!-- 加载状态 -->
      <view class="load-more">
        <text v-if="store.loading">加载中...</text>
        <text v-else-if="!store.hasMore">没有更多了</text>
        <text v-else>上拉加载更多</text>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useRecipesStore } from '@/stores/recipes.js'
import { getRecipeTypes, getRecipeDifficulties } from '@/api/recipes.js'

// Store
const store = useRecipesStore()

// 筛选选项
const recipeTypes = ref([])
const difficulties = ref([])
const refreshing = ref(false)

// 体质选项
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

// 功效选项
const efficacies = ref(['健脾', '养胃', '补气', '补血', '养阴', '温阳', '化痰', '祛湿', '活血', '疏肝', '安神'])

// 生命周期
onLoad((options) => {
  // 从URL参数获取体质筛选
  if (options.constitution) {
    store.setFilter('constitution', options.constitution)
  }
})

onMounted(() => {
  loadFilters()
  loadData()
})

// 加载筛选选项
async function loadFilters() {
  try {
    const [diffRes] = await Promise.all([
      getRecipeDifficulties()
    ])
    if (diffRes) {
      difficulties.value = diffRes
    }
  } catch (e) {
    console.error('加载筛选选项失败', e)
  }
}

// 加载菜谱列表
async function loadData(reset = true) {
  try {
    await store.loadRecipes({ reset })
  } catch (e) {
    uni.showToast({
      title: store.error || '加载失败',
      icon: 'none'
    })
  }
}

// 下拉刷新
async function onRefresh() {
  refreshing.value = true
  try {
    await loadData(true)
  } finally {
    setTimeout(() => {
      refreshing.value = false
    }, 500)
  }
}

// 滚动到底部
function onScrollToLower() {
  if (!store.loading && store.hasMore) {
    store.loadMoreRecipes()
  }
}

// 选择体质
function selectConstitution(value) {
  store.setFilter('constitution', value)
  loadData(true)
}

// 选择功效
function selectEfficacy(value) {
  store.setFilter('efficacy', value)
  loadData(true)
}

// 选择难度
function selectDifficulty(value) {
  store.setFilter('difficulty', value)
  loadData(true)
}

// 图片加载错误
function onImageError(event, item) {
  console.log('图片加载失败:', item.cover_image)
  item.cover_image = ''
}

// 跳转详情
function goToDetail(id) {
  uni.navigateTo({
    url: `/pages/recipes/detail?id=${id}`
  })
}

// 获取难度标签
function getDifficultyLabel(difficulty) {
  const map = {
    easy: '简单',
    medium: '中等',
    hard: '困难'
  }
  return map[difficulty] || difficulty
}

// 获取难度样式类
function getDifficultyClass(difficulty) {
  return difficulty
}

// 获取体质标签
function getConstitutionLabel(code) {
  const constitution = constitutions.value.find(c => c.value === code)
  return constitution ? constitution.label : code
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

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 200rpx 0;

  .empty-icon {
    font-size: 120rpx;
    margin-bottom: 20rpx;
  }

  .empty-text {
    font-size: 32rpx;
    color: #999;
  }
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
  overflow: hidden;
}

.recipe-image {
  width: 200rpx;
  height: 200rpx;
  border-radius: 12rpx;
  flex-shrink: 0;

  &.placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);

    .placeholder-icon {
      font-size: 80rpx;
      opacity: 0.5;
    }
  }
}

.recipe-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10rpx;
  min-width: 0;
}

.recipe-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recipe-desc {
  font-size: 26rpx;
  color: #666;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
  line-height: 1.5;
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

  &.difficulty {
    &.easy {
      background: #f6ffed;
      color: #52c41a;
    }
    &.medium {
      background: #fff7e6;
      color: #fa8c16;
    }
    &.hard {
      background: #fff1f0;
      color: #ff4d4f;
    }
  }

  &.efficacy {
    background: #f0f5ff;
    color: #1890ff;
  }
}

.time, .calories {
  font-size: 24rpx;
  color: #999;
}

.recipe-tags {
  display: flex;
  gap: 8rpx;
  flex-wrap: wrap;
}

.recipe-constitutions {
  display: flex;
  align-items: center;
  gap: 8rpx;
  flex-wrap: wrap;

  .constitution-label {
    font-size: 24rpx;
    color: #999;
  }

  .constitution-tag {
    padding: 4rpx 12rpx;
    border-radius: 8rpx;
    font-size: 24rpx;
    background: #f0f5ff;
    color: #1890ff;
  }
}

.load-more {
  padding: 30rpx;
  text-align: center;
  color: #999;
  font-size: 28rpx;
}
</style>
