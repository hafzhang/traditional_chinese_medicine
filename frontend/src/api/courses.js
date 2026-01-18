/**
 * 养生课程相关 API - Phase 1
 */
import { get } from '@/utils/request.js'

/**
 * 获取课程列表
 * @param {Object} params - 查询参数
 * @param {number} params.skip - 跳过数量
 * @param {number} params.limit - 限制数量
 * @param {string} params.category - 分类筛选
 * @param {string} params.content_type - 内容类型筛选
 * @param {string} params.constitution - 体质筛选
 * @param {string} params.search - 搜索关键词
 * @returns {Promise}
 */
export function getCoursesList(params = {}) {
  return get('/api/v1/courses', params)
}

/**
 * 获取课程详情
 * @param {string} courseId - 课程ID
 * @returns {Promise}
 */
export function getCourseDetail(courseId) {
  return get(`/api/v1/courses/${courseId}`)
}

/**
 * 根据体质获取推荐课程
 * @param {string} constitution - 体质代码
 * @returns {Promise}
 */
export function getCourseRecommendation(constitution) {
  return get(`/api/v1/courses/recommend/${constitution}`)
}

/**
 * 根据季节获取养生课程
 * @param {string} season - 季节 (spring, summer, autumn, winter)
 * @returns {Promise}
 */
export function getSeasonCourses(season) {
  return get(`/api/v1/courses/season/${season}`)
}

/**
 * 获取课程分类列表
 * @returns {Promise}
 */
export function getCourseCategories() {
  return get('/api/v1/courses/categories/list')
}

/**
 * 获取季节列表
 * @returns {Promise}
 */
export function getSeasons() {
  return get('/api/v1/courses/seasons/list')
}

export default {
  getCoursesList,
  getCourseDetail,
  getCourseRecommendation,
  getSeasonCourses,
  getCourseCategories,
  getSeasons
}
