<template>
  <view class="recipe-detail-page">
    <scroll-view class="detail-scroll" scroll-y>
      <!-- 加载状态 -->
      <view v-if="loading" class="loading-state">
        <text>加载中...</text>
      </view>

      <!-- 内容区域 -->
      <template v-else-if="recipe">
        <!-- 图片区域 -->
        <view class="image-section">
          <image
            v-if="recipe.cover_image"
            :src="recipe.cover_image"
            class="recipe-image"
            mode="aspectFill"
            @tap="previewImage"
            @error="onImageError"
          />
          <view v-else class="recipe-image placeholder">
            <text class="placeholder-icon">🍲</text>
          </view>
        </view>

        <!-- 基本信息 -->
        <view class="info-card">
          <view class="recipe-name">{{ recipe.name }}</view>
          <view class="recipe-meta">
            <text v-if="recipe.difficulty" class="tag difficulty" :class="getDifficultyClass(recipe.difficulty)">
              {{ getDifficultyLabel(recipe.difficulty) }}
            </text>
            <text v-if="recipe.cooking_time" class="time">⏱ {{ recipe.cooking_time }}分钟</text>
            <text v-if="recipe.calories" class="calories">🔥 {{ recipe.calories }}kcal</text>
          </view>
          <view v-if="recipe.description" class="recipe-description">
            {{ recipe.description }}
          </view>
        </view>

        <!-- 功效标签 -->
        <view v-if="recipe.efficacy_tags && recipe.efficacy_tags.length" class="info-card">
          <view class="card-title">功效标签</view>
          <view class="tags">
            <text v-for="tag in recipe.efficacy_tags" :key="tag" class="tag-item efficacy">
              {{ tag }}
            </text>
          </view>
        </view>

        <!-- 适合体质 -->
        <view v-if="recipe.suitable_constitutions && recipe.suitable_constitutions.length" class="info-card">
          <view class="card-title">适合体质</view>
          <view class="constitutions">
            <text
              v-for="code in recipe.suitable_constitutions"
              :key="code"
              class="constitution-tag suitable"
            >
              {{ getConstitutionName(code) }}
            </text>
          </view>
        </view>

        <!-- 禁忌体质 -->
        <view v-if="recipe.avoid_constitutions && recipe.avoid_constitutions.length" class="info-card avoid">
          <view class="card-title">禁忌体质</view>
          <view class="constitutions">
            <text
              v-for="code in recipe.avoid_constitutions"
              :key="code"
              class="constitution-tag avoid"
            >
              {{ getConstitutionName(code) }}
            </text>
          </view>
        </view>

        <!-- 个人体验区域 (蓝色背景) -->
        <view v-if="recipe.desc" class="info-card desc-section">
          <view class="card-title">💭 个人体验</view>
          <view class="card-content">{{ recipe.desc }}</view>
        </view>

        <!-- 营养信息 -->
        <view v-if="hasNutritionInfo" class="info-card">
          <view class="card-title">营养信息 (每100g)</view>
          <view class="nutrition-info">
            <view v-if="recipe.protein" class="nutrition-item">
              <text class="nutrition-label">蛋白质</text>
              <text class="nutrition-value">{{ recipe.protein }}g</text>
            </view>
            <view v-if="recipe.fat" class="nutrition-item">
              <text class="nutrition-label">脂肪</text>
              <text class="nutrition-value">{{ recipe.fat }}g</text>
            </view>
            <view v-if="recipe.carbs" class="nutrition-item">
              <text class="nutrition-label">碳水</text>
              <text class="nutrition-value">{{ recipe.carbs }}g</text>
            </view>
          </view>
        </view>

        <!-- 食材清单 -->
        <view v-if="recipe.ingredients && recipe.ingredients.length" class="info-card">
          <view class="card-title">食材清单</view>
          <view class="ingredients-list">
            <view
              v-for="(item, index) in recipe.ingredients"
              :key="index"
              class="ingredient-row"
              :class="{ main: item.is_main }"
            >
              <view class="ingredient-info">
                <text v-if="item.is_main" class="main-badge">主料</text>
                <text class="ingredient-name">{{ item.name }}</text>
                <text v-if="item.nature" class="ingredient-nature">{{ item.nature }}</text>
                <text v-if="item.taste" class="ingredient-taste">{{ item.taste }}</text>
              </view>
              <text v-if="item.amount" class="ingredient-amount">{{ item.amount }}</text>
            </view>
          </view>
        </view>

        <!-- 制作步骤 -->
        <view v-if="recipe.steps && recipe.steps.length" class="info-card">
          <view class="card-title">制作步骤</view>
          <view class="steps-list">
            <view
              v-for="(step, index) in recipe.steps"
              :key="index"
              class="step-item"
            >
              <view class="step-number">{{ step.step_number || index + 1 }}</view>
              <view class="step-content">
                <text class="step-description">{{ step.description }}</text>
                <text v-if="step.duration" class="step-duration">⏱ {{ step.duration }}分钟</text>
              </view>
              <image
                v-if="step.image_url"
                :src="step.image_url"
                class="step-image"
                mode="aspectFill"
                @tap="previewStepImage(step.image_url)"
              />
            </view>
          </view>
        </view>

        <!-- 烹饪贴士区域 (黄色背景) -->
        <view v-if="recipe.tip" class="info-card tip-section">
          <view class="card-title">💡 烹饪贴士</view>
          <view class="card-content">{{ recipe.tip }}</view>
        </view>

        <!-- 适用节气 -->
        <view v-if="recipe.solar_terms && recipe.solar_terms.length" class="info-card">
          <view class="card-title">适用节气</view>
          <view class="tags">
            <text v-for="term in recipe.solar_terms" :key="term" class="tag-item season">
              {{ term }}
            </text>
          </view>
        </view>
      </template>

      <!-- 错误状态 -->
      <view v-else class="error-state">
        <text class="error-icon">😕</text>
        <text class="error-text">菜谱不存在</text>
      </view>

      <!-- 相关菜谱推荐 -->
      <view v-if="relatedRecipes.length > 0" class="info-card">
        <view class="card-title">相关菜谱</view>
        <view class="related-recipes">
          <view
            v-for="item in relatedRecipes"
            :key="item.id"
            class="related-item"
            @tap="goToDetail(item.id)"
          >
            <image
              v-if="item.cover_image"
              :src="item.cover_image"
              class="related-image"
              mode="aspectFill"
            />
            <view v-else class="related-image placeholder">
              <text>🍲</text>
            </view>
            <view class="related-info">
              <view class="related-name">{{ item.name }}</view>
              <text class="related-meta">{{ getDifficultyLabel(item.difficulty) }} · {{ item.cooking_time }}分钟</text>
            </view>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useRecipesStore } from '@/stores/recipes.js'

// Store
const store = useRecipesStore()

// 数据
const recipe = ref(null)
const relatedRecipes = ref([])
const loading = ref(true)
const recipeId = ref('')

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

// 计算属性：是否有营养信息
const hasNutritionInfo = computed(() => {
  return recipe.value && (recipe.value.protein || recipe.value.fat || recipe.value.carbs)
})

// 生命周期
onLoad((options) => {
  if (options.id) {
    recipeId.value = options.id
    loadDetail(options.id)
  }
})

// 加载详情
async function loadDetail(id) {
  loading.value = true
  uni.showLoading({ title: '加载中...' })

  try {
    const data = await store.loadRecipeDetail(id)
    recipe.value = data

    // 加载相关推荐（基于体质）
    if (data.suitable_constitutions && data.suitable_constitutions.length > 0) {
      loadRelatedRecipes(data.suitable_constitutions[0], id)
    }
  } catch (e) {
    console.error('加载菜谱详情失败', e)
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
    uni.hideLoading()
  }
}

// 加载相关菜谱
async function loadRelatedRecipes(constitution, excludeId) {
  try {
    const result = await store.loadRecommendations('constitution', {
      constitution,
      limit: 4
    })

    // 过滤掉当前菜谱
    relatedRecipes.value = result.items.filter(item => item.id !== excludeId).slice(0, 3)
  } catch (e) {
    console.error('加载相关菜谱失败', e)
  }
}

// 预览图片
function previewImage() {
  if (recipe.value?.cover_image) {
    uni.previewImage({
      urls: [recipe.value.cover_image],
      current: 0
    })
  }
}

// 预览步骤图片
function previewStepImage(imageUrl) {
  uni.previewImage({
    urls: [imageUrl],
    current: 0
  })
}

// 图片加载错误
function onImageError() {
  console.log('图片加载失败')
  recipe.value.cover_image = ''
}

// 跳转到其他详情
function goToDetail(id) {
  uni.redirectTo({
    url: `/pages/recipes/detail?id=${id}`
  })
}

// 获取体质名称
function getConstitutionName(code) {
  return constitutionNames[code] || code
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
</script>

<style lang="scss" scoped>
.recipe-detail-page {
  height: 100vh;
  background: #f5f5f5;
}

.detail-scroll {
  height: 100%;
}

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  font-size: 32rpx;
  color: #999;
}

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;

  .error-icon {
    font-size: 120rpx;
    margin-bottom: 20rpx;
  }

  .error-text {
    font-size: 32rpx;
    color: #999;
  }
}

.image-section {
  background: #fff;
  padding: 40rpx;
  text-align: center;
}

.recipe-image {
  width: 100%;
  height: 400rpx;
  border-radius: 20rpx;

  &.placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);

    .placeholder-icon {
      font-size: 150rpx;
      opacity: 0.5;
    }
  }
}

.info-card {
  background: #fff;
  margin: 20rpx;
  padding: 30rpx;
  border-radius: 16rpx;

  &.desc-section {
    background: linear-gradient(135deg, #e6f7ff 0%, #f0f5ff 100%);
    border-left: 4rpx solid #1890ff;
  }

  &.tip-section {
    background: linear-gradient(135deg, #fffbe6 0%, #fff7e6 100%);
    border-left: 4rpx solid #faad14;
  }

  &.avoid {
    border-left: 4rpx solid #ff4d4f;
  }
}

.card-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.card-content {
  font-size: 28rpx;
  color: #666;
  line-height: 1.8;
  white-space: pre-wrap;
}

.recipe-name {
  font-size: 40rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.recipe-description {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
  margin-top: 20rpx;
}

.recipe-meta {
  display: flex;
  gap: 10rpx;
  align-items: center;
  flex-wrap: wrap;
}

.tag {
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
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
}

.time, .calories {
  font-size: 26rpx;
  color: #999;
}

.tags {
  display: flex;
  gap: 10rpx;
  flex-wrap: wrap;
}

.tag-item {
  padding: 8rpx 20rpx;
  border-radius: 20rpx;
  font-size: 26rpx;

  &.efficacy {
    background: #f0f5ff;
    color: #1890ff;
  }

  &.season {
    background: #f6ffed;
    color: #52c41a;
  }
}

.constitutions {
  display: flex;
  gap: 10rpx;
  flex-wrap: wrap;
}

.constitution-tag {
  padding: 8rpx 20rpx;
  border-radius: 20rpx;
  font-size: 26rpx;

  &.suitable {
    background: #f0f5ff;
    color: #1890ff;
  }

  &.avoid {
    background: #fff1f0;
    color: #ff4d4f;
  }
}

.nutrition-info {
  display: flex;
  justify-content: space-around;
  padding: 20rpx 0;
}

.nutrition-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10rpx;
}

.nutrition-label {
  font-size: 24rpx;
  color: #999;
}

.nutrition-value {
  font-size: 32rpx;
  font-weight: bold;
  color: #1890ff;
}

.ingredients-list {
  display: flex;
  flex-direction: column;
  gap: 5rpx;
}

.ingredient-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15rpx;
  border-radius: 10rpx;
  background: #f9f9f9;

  &.main {
    background: #fff7e6;
    border-left: 4rpx solid #faad14;
  }
}

.ingredient-info {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10rpx;
  flex-wrap: wrap;
}

.main-badge {
  padding: 4rpx 10rpx;
  border-radius: 8rpx;
  background: #faad14;
  color: #fff;
  font-size: 20rpx;
}

.ingredient-name {
  font-size: 28rpx;
  color: #333;
  font-weight: 500;
}

.ingredient-nature {
  padding: 4rpx 10rpx;
  border-radius: 8rpx;
  background: #f6ffed;
  color: #52c41a;
  font-size: 22rpx;
}

.ingredient-taste {
  padding: 4rpx 10rpx;
  border-radius: 8rpx;
  background: #f0f5ff;
  color: #1890ff;
  font-size: 22rpx;
}

.ingredient-amount {
  font-size: 26rpx;
  color: #999;
}

.steps-list {
  display: flex;
  flex-direction: column;
  gap: 25rpx;
}

.step-item {
  display: flex;
  gap: 15rpx;
  position: relative;
}

.step-number {
  width: 50rpx;
  height: 50rpx;
  border-radius: 50%;
  background: #1890ff;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  font-weight: bold;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10rpx;
}

.step-description {
  font-size: 28rpx;
  color: #333;
  line-height: 1.6;
}

.step-duration {
  font-size: 24rpx;
  color: #999;
}

.step-image {
  width: 120rpx;
  height: 120rpx;
  border-radius: 10rpx;
  flex-shrink: 0;
}

.related-recipes {
  display: flex;
  flex-direction: column;
  gap: 15rpx;
}

.related-item {
  display: flex;
  gap: 15rpx;
  padding: 15rpx;
  background: #f9f9f9;
  border-radius: 10rpx;
}

.related-image {
  width: 120rpx;
  height: 120rpx;
  border-radius: 10rpx;
  flex-shrink: 0;

  &.placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f0f0f0;
    font-size: 50rpx;
  }
}

.related-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10rpx;
}

.related-name {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.related-meta {
  font-size: 24rpx;
  color: #999;
}
</style>
