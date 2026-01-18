/**
 * 食谱相关 API - Phase 1
 */
import { get } from '@/utils/request.js'

/**
 * 获取食谱列表
 * @param {Object} params - 查询参数
 * @param {number} params.skip - 跳过数量
 * @param {number} params.limit - 限制数量
 * @param {string} params.type - 类型筛选
 * @param {string} params.difficulty - 难度筛选
 * @param {string} params.constitution - 体质筛选
 * @param {string} params.search - 搜索关键词
 * @returns {Promise}
 */
export function getRecipesList(params = {}) {
  return get('/api/v1/recipes', params)
}

/**
 * 获取食谱详情
 * @param {string} recipeId - 食谱ID
 * @returns {Promise}
 */
export function getRecipeDetail(recipeId) {
  return get(`/api/v1/recipes/${recipeId}`)
}

/**
 * 根据体质获取推荐食谱
 * @param {string} constitution - 体质代码
 * @returns {Promise}
 */
export function getRecipeRecommendation(constitution) {
  return get(`/api/v1/recipes/recommend/${constitution}`)
}

/**
 * 获取食谱类型列表
 * @returns {Promise}
 */
export function getRecipeTypes() {
  return get('/api/v1/recipes/types/list')
}

/**
 * 获取食谱难度列表
 * @returns {Promise}
 */
export function getRecipeDifficulties() {
  return get('/api/v1/recipes/difficulties/list')
}

export default {
  getRecipesList,
  getRecipeDetail,
  getRecipeRecommendation,
  getRecipeTypes,
  getRecipeDifficulties
}
