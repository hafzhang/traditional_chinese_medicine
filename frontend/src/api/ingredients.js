/**
 * 食材相关 API - Phase 1
 */
import { get } from '@/utils/request.js'

/**
 * 获取食材列表
 * @param {Object} params - 查询参数
 * @param {number} params.skip - 跳过数量
 * @param {number} params.limit - 限制数量
 * @param {string} params.category - 类别筛选
 * @param {string} params.nature - 性味筛选
 * @param {string} params.search - 搜索关键词
 * @returns {Promise}
 */
export function getIngredientsList(params = {}) {
  return get('/api/v1/ingredients', params)
}

/**
 * 获取食材详情
 * @param {string} ingredientId - 食材ID
 * @returns {Promise}
 */
export function getIngredientDetail(ingredientId) {
  return get(`/api/v1/ingredients/${ingredientId}`)
}

/**
 * 根据体质获取推荐食材
 * @param {string} constitution - 体质代码
 * @returns {Promise}
 */
export function getIngredientRecommendation(constitution) {
  return get(`/api/v1/ingredients/recommend/${constitution}`)
}

/**
 * 获取食材类别列表
 * @returns {Promise}
 */
export function getIngredientCategories() {
  return get('/api/v1/ingredients/categories/list')
}

/**
 * 获取食材性味列表
 * @returns {Promise}
 */
export function getIngredientNatures() {
  return get('/api/v1/ingredients/natures/list')
}

export default {
  getIngredientsList,
  getIngredientDetail,
  getIngredientRecommendation,
  getIngredientCategories,
  getIngredientNatures
}
