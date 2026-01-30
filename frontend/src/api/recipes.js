/**
 * 菜谱相关 API - Excel Import
 */
import { get } from '@/utils/request.js'

/**
 * 获取菜谱列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码，默认1
 * @param {number} params.page_size - 每页数量，默认20
 * @param {string} params.constitution - 体质筛选 (如: 'qi_deficiency')
 * @param {string} params.efficacy - 功效标签筛选 (如: '健脾')
 * @param {string} params.solar_term - 节气筛选 (如: '春季')
 * @param {string} params.difficulty - 难度筛选 ('easy', 'medium', 'hard')
 * @param {number} params.max_cooking_time - 最大烹饪时间(分钟)
 * @param {string} params.sort_by - 排序方式 ('created_at_desc', 'view_count_desc', 'cooking_time_asc')
 * @returns {Promise<Object>} 返回 {total, page, page_size, items}
 */
export function getRecipes(params = {}) {
  return get('/api/v1/recipes', params).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取菜谱列表失败')
  })
}

/**
 * 获取菜谱详情
 * @param {string} id - 菜谱ID
 * @returns {Promise<Object>} 返回菜谱详情对象，包含desc、tip、ingredients(含nature/taste)、steps
 */
export function getRecipeDetail(id) {
  return get(`/api/v1/recipes/${id}`).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取菜谱详情失败')
  })
}

/**
 * 搜索菜谱
 * @param {string} keyword - 搜索关键词
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码，默认1
 * @param {number} params.page_size - 每页数量，默认20
 * @returns {Promise<Object>} 返回 {total, page, page_size, items}
 */
export function searchRecipes(keyword, params = {}) {
  if (!keyword || keyword.trim() === '') {
    return Promise.resolve({ total: 0, page: 1, page_size: 20, items: [] })
  }
  return get('/api/v1/recipes/search', { keyword, ...params }).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '搜索菜谱失败')
  })
}

/**
 * 获取推荐菜谱
 * @param {string} type - 推荐类型 ('constitution', 'solar_term', 'efficacy')
 * @param {Object} params - 推荐参数
 * @param {string} params.constitution - 体质代码 (当type='constitution'时必需)
 * @param {string} params.solar_term - 节气名称 (当type='solar_term'时必需)
 * @param {string} params.efficacy - 功效标签 (当type='efficacy'时必需)
 * @param {number} params.limit - 限制数量，默认10
 * @returns {Promise<Object>} 返回 {type, recommendation_reason, items}
 */
export function getRecommendations(type, params = {}) {
  const queryParams = { type, ...params }
  return get('/api/v1/recipes/recommend', queryParams).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取推荐菜谱失败')
  })
}

/**
 * 获取菜谱类型列表
 * @returns {Promise<Array>} 返回类型列表
 */
export function getRecipeTypes() {
  return get('/api/v1/recipes/types/list').then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取菜谱类型失败')
  })
}

/**
 * 获取菜谱难度列表
 * @returns {Promise<Array>} 返回难度列表
 */
export function getRecipeDifficulties() {
  return get('/api/v1/recipes/difficulties/list').then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取菜谱难度失败')
  })
}

export default {
  getRecipes,
  getRecipeDetail,
  searchRecipes,
  getRecommendations,
  getRecipeTypes,
  getRecipeDifficulties
}
