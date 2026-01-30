<template>
  <view class="recipes-search-page">
    <!-- 搜索框 -->
    <view class="search-bar">
      <view class="search-input-wrapper">
        <text class="search-icon">🔍</text>
        <input
          v-model="keyword"
          class="search-input"
          placeholder="搜索菜谱名称、食材、功效"
          :confirm-type="'search'"
          @confirm="onSearch"
        />
        <text v-if="keyword" class="clear-icon" @click="clearKeyword">✕</text>
      </view>
      <button class="search-btn" @click="onSearch">搜索</button>
    </view>

    <!-- 筛选区域 -->
    <view class="filter-section">
      <!-- 体质筛选 -->
      <scroll-view scroll-x class="filter-scroll">
        <view class="filter-item" :class="{ active: !filters.constitution }" @click="selectConstitution('')">
          全部体质
        </view>
        <view
          v-for="constitution in constitutions"
          :key="constitution.value"
          class="filter-item"
          :class="{ active: filters.constitution === constitution.value }"
          @click="selectConstitution(constitution.value)"
        >
          {{ constitution.label }}
        </view>
      </scroll-view>

      <!-- 功效筛选 -->
      <scroll-view scroll-x class="filter-scroll">
        <view class="filter-item" :class="{ active: !filters.efficacy }" @click="selectEfficacy('')">
          全部功效
        </view>
        <view
          v-for="efficacy in efficacies"
          :key="efficacy"
          class="filter-item"
          :class="{ active: filters.efficacy === efficacy }"
          @click="selectEfficacy(efficacy)"
        >
          {{ efficacy }}
        </view>
      </scroll-view>

      <!-- 节气筛选 -->
      <scroll-view scroll-x class="filter-scroll">
        <view class="filter-item" :class="{ active: !filters.solar_term }" @click="selectSolarTerm('')">
          全部节气
        </view>
        <view
          v-for="term in solarTerms"
          :key="term"
          class="filter-item"
          :class="{ active: filters.solar_term === term }"
          @click="selectSolarTerm(term)"
        >
          {{ term }}
        </view>
      </scroll-view>

      <!-- 难度筛选 -->
      <scroll-view scroll-x class="filter-scroll">
        <view class="filter-item" :class="{ active: !filters.difficulty }" @click="selectDifficulty('')">
          全部难度
        </view>
        <view
          v-for="diff in difficulties"
          :key="diff.value"
          class="filter-item"
          :class="{ active: filters.difficulty === diff.value }"
          @click="selectDifficulty(diff.value)"
        >
          {{ diff.label }}
        </view>
      </scroll-view>

      <!-- 烹饪时间筛选 -->
      <scroll-view scroll-x class="filter-scroll">
        <view class="filter-item" :class="{ active: !filters.max_cooking_time }" @click="selectCookingTime(null)">
          全部时间
        </view>
        <view
          v-for="time in cookingTimes"
          :key="time.value"
          class="filter-item"
          :class="{ active: filters.max_cooking_time === time.value }"
          @click="selectCookingTime(time.value)"
        >
          {{ time.label }}
        </view>
      </scroll-view>
    </view>

    <!-- 操作栏 -->
    <view v-if="hasFilters" class="action-bar">
      <view class="filter-summary">
        <text class="summary-text">{{ getFilterSummary() }}</text>
      </view>
      <button class="clear-btn" @click="clearAllFilters">清除筛选</button>
    </view>

    <!-- 搜索结果 -->
    <scroll-view
      class="results-scroll"
      scroll-y
      @scrolltolower="onScrollToLower"
    >
      <!-- 空状态 -->
      <view v-if="!loading && recipes.length === 0" class="empty-state">
        <text class="empty-icon">{{ keyword ? '🔍' : '🍳' }}</text>
        <text class="empty-text">{{ keyword ? '没有找到相关菜谱' : '请输入关键词搜索' }}</text>
        <text v-if="hasFilters" class="empty-hint">尝试调整筛选条件</text>
      </view>

      <!-- 结果列表 -->
      <view v-else class="results-list">
        <view
          v-for="item in recipes"
          :key="item.id"
          class="recipe-item"
          @click="goToDetail(item.id)"
        >
          <!-- 封面图 -->
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
              <text v-if="item.difficulty" class="tag difficulty" :class="getDifficultyClass(item.difficulty)">
                {{ getDifficultyLabel(item.difficulty) }}
              </text>
              <text v-if="item.cooking_time" class="time">⏱ {{ item.cooking_time }}分钟</text>
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
        <text v-if="loading">加载中...</text>
        <text v-else-if="!hasMore && recipes.length > 0">没有更多了</text>
        <text v-else-if="recipes.length > 0">上拉加载更多</text>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRecipesStore } from '@/stores/recipes.js'
import { getRecipeDifficulties } from '@/api/recipes.js'

// Store
const store = useRecipesStore()

// 数据
const keyword = ref('')
const recipes = ref([])
const loading = ref(false)
const hasMore = ref(false)
const pagination = ref({
  total: 0,
  page: 1,
  page_size: 20
})

// 筛选条件
const filters = ref({
  constitution: '',
  efficacy: '',
  solar_term: '',
  difficulty: '',
  max_cooking_time: null
})

// 筛选选项
const difficulties = ref([])

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

// 节气选项
const solarTerms = ref(['春季', '夏季', '秋季', '冬季', '立春', '雨水', '惊蛰', '春分', '清明', '谷雨', '立夏', '小满', '芒种', '夏至', '小暑', '大暑', '立秋', '处暑', '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪', '冬至', '小寒', '大寒'])

// 烹饪时间选项
const cookingTimes = ref([
  { value: 15, label: '15分钟内' },
  { value: 30, label: '30分钟内' },
  { value: 60, label: '1小时内' },
  { value: 120, label: '2小时内' }
])

// 计算属性：是否有筛选条件
const hasFilters = computed(() => {
  return !!(
    filters.value.constitution ||
    filters.value.efficacy ||
    filters.value.solar_term ||
    filters.value.difficulty ||
    filters.value.max_cooking_time
  )
})

// 生命周期
onMounted(() => {
  loadFilters()
})

// 加载筛选选项
async function loadFilters() {
  try {
    const diffRes = await getRecipeDifficulties()
    if (diffRes) {
      difficulties.value = diffRes
    }
  } catch (e) {
    console.error('加载筛选选项失败', e)
  }
}

// 搜索
async function onSearch() {
  if (!keyword.value.trim() && !hasFilters.value) {
    return
  }
  await loadData(true)
}

// 加载数据
async function loadData(reset = true) {
  loading.value = true

  try {
    let result

    // 如果有关键词，使用搜索API
    if (keyword.value.trim()) {
      result = await store.searchRecipes(keyword.value.trim(), {
        page: reset ? 1 : pagination.value.page,
        page_size: pagination.value.page_size
      })
    } else {
      // 没有关键词，使用筛选列表
      // 构建查询参数
      const queryParams = {
        page: reset ? 1 : pagination.value.page,
        page_size: pagination.value.page_size,
        ...filters.value
      }

      // 移除空值
      Object.keys(queryParams).forEach(key => {
        if (queryParams[key] === '' || queryParams[key] === null || queryParams[key] === undefined) {
          delete queryParams[key]
        }
      })

      result = await store.loadRecipes(queryParams)
      // 从 store 中获取结果
      result = {
        total: store.pagination.total,
        page: store.pagination.page,
        page_size: store.pagination.page_size,
        items: store.recipes
      }
    }

    if (reset) {
      recipes.value = result.items || []
    } else {
      recipes.value = [...recipes.value, ...(result.items || [])]
    }

    pagination.value = {
      total: result.total || 0,
      page: result.page || 1,
      page_size: result.page_size || 20
    }

    hasMore.value = pagination.value.page * pagination.value.page_size < pagination.value.total
  } catch (e) {
    console.error('加载失败', e)
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

// 滚动到底部
function onScrollToLower() {
  if (!loading.value && hasMore.value) {
    pagination.value.page += 1
    loadData(false)
  }
}

// 选择体质
function selectConstitution(value) {
  filters.value.constitution = value
  if (keyword.value.trim() || hasFilters.value) {
    loadData(true)
  }
}

// 选择功效
function selectEfficacy(value) {
  filters.value.efficacy = value
  if (keyword.value.trim() || hasFilters.value) {
    loadData(true)
  }
}

// 选择节气
function selectSolarTerm(value) {
  filters.value.solar_term = value
  if (keyword.value.trim() || hasFilters.value) {
    loadData(true)
  }
}

// 选择难度
function selectDifficulty(value) {
  filters.value.difficulty = value
  if (keyword.value.trim() || hasFilters.value) {
    loadData(true)
  }
}

// 选择烹饪时间
function selectCookingTime(value) {
  filters.value.max_cooking_time = value
  if (keyword.value.trim() || hasFilters.value) {
    loadData(true)
  }
}

// 清除关键词
function clearKeyword() {
  keyword.value = ''
}

// 清除所有筛选
function clearAllFilters() {
  filters.value = {
    constitution: '',
    efficacy: '',
    solar_term: '',
    difficulty: '',
    max_cooking_time: null
  }
  if (keyword.value.trim()) {
    loadData(true)
  }
}

// 获取筛选条件摘要
function getFilterSummary() {
  const parts = []
  if (filters.value.constitution) {
    parts.push('体质')
  }
  if (filters.value.efficacy) {
    parts.push('功效')
  }
  if (filters.value.solar_term) {
    parts.push('节气')
  }
  if (filters.value.difficulty) {
    parts.push('难度')
  }
  if (filters.value.max_cooking_time) {
    parts.push('时间')
  }
  return `已筛选: ${parts.join('、')}`
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
.recipes-search-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.search-bar {
  display: flex;
  align-items: center;
  padding: 20rpx;
  background: #fff;
  gap: 20rpx;
}

.search-input-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  background: #f5f5f5;
  border-radius: 30rpx;
  padding: 15rpx 30rpx;
  gap: 15rpx;
}

.search-icon {
  font-size: 32rpx;
  color: #999;
}

.search-input {
  flex: 1;
  font-size: 28rpx;
  color: #333;
}

.clear-icon {
  font-size: 32rpx;
  color: #999;
  padding: 0 10rpx;
}

.search-btn {
  padding: 15rpx 30rpx;
  background: #1890ff;
  color: #fff;
  border-radius: 30rpx;
  font-size: 28rpx;
  border: none;
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
  font-size: 26rpx;
  background: #f5f5f5;
  color: #666;

  &.active {
    background: #1890ff;
    color: #fff;
  }
}

.action-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20rpx;
  background: #fff7e6;
  border-bottom: 1px solid #ffd591;
}

.filter-summary {
  flex: 1;
}

.summary-text {
  font-size: 26rpx;
  color: #d46b08;
}

.clear-btn {
  padding: 10rpx 20rpx;
  background: #fff;
  color: #d46b08;
  border: 1px solid #d46b08;
  border-radius: 20rpx;
  font-size: 26rpx;
}

.results-scroll {
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
    margin-bottom: 10rpx;
  }

  .empty-hint {
    font-size: 26rpx;
    color: #bbb;
  }
}

.results-list {
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
