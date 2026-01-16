/**
 * 体质相关 API
 */
import { get, post } from '@/utils/request.js'

/**
 * 获取测试问题列表
 * @returns {Promise}
 */
export function getQuestions() {
  return get('/api/v1/questions')
}

/**
 * 提交测试答案
 * @param {Array} answers - 30个答案的数组，每个为1-5
 * @param {Object} userInfo - 用户信息（可选）
 * @returns {Promise}
 */
export function submitTest(answers, userInfo = {}) {
  return post('/api/v1/test/submit', {
    answers,
    ...userInfo
  })
}

/**
 * 获取测试结果详情
 * @param {string} resultId - 结果ID
 * @returns {Promise}
 */
export function getResult(resultId) {
  return get(`/api/v1/result/${resultId}`)
}

/**
 * 获取饮食推荐
 * @param {string} constitution - 体质类型
 * @returns {Promise}
 */
export function getFoodRecommendations(constitution) {
  return get('/api/v1/recommend/food', { constitution })
}

/**
 * 健康检查
 * @returns {Promise}
 */
export function healthCheck() {
  return get('/health')
}

export default {
  getQuestions,
  submitTest,
  getResult,
  getFoodRecommendations,
  healthCheck
}
