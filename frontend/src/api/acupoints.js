/**
 * 穴位相关 API - Phase 1
 */
import { get } from '@/utils/request.js'

/**
 * 获取穴位列表
 * @param {Object} params - 查询参数
 * @param {number} params.skip - 跳过数量
 * @param {number} params.limit - 限制数量
 * @param {string} params.body_part - 部位筛选
 * @param {string} params.constitution - 体质筛选
 * @param {string} params.search - 搜索关键词
 * @returns {Promise}
 */
export function getAcupointsList(params = {}) {
  return get('/api/v1/acupoints', params)
}

/**
 * 获取穴位详情
 * @param {string} acupointId - 穴位ID
 * @returns {Promise}
 */
export function getAcupointDetail(acupointId) {
  return get(`/api/v1/acupoints/${acupointId}`)
}

/**
 * 根据体质获取推荐穴位
 * @param {string} constitution - 体质代码
 * @returns {Promise}
 */
export function getAcupointRecommendation(constitution) {
  return get(`/api/v1/acupoints/recommend/${constitution}`)
}

/**
 * 根据症状查找穴位
 * @param {string} symptom - 症状名称
 * @returns {Promise}
 */
export function getAcupointsBySymptom(symptom) {
  return get(`/api/v1/acupoints/symptom/${symptom}`)
}

/**
 * 根据经络获取穴位
 * @param {string} meridian - 经络名称
 * @returns {Promise}
 */
export function getAcupointsByMeridian(meridian) {
  return get(`/api/v1/acupoints/meridian/${meridian}`)
}

/**
 * 获取部位列表
 * @returns {Promise}
 */
export function getBodyParts() {
  return get('/api/v1/acupoints/body-parts/list')
}

/**
 * 获取经络列表
 * @returns {Promise}
 */
export function getMeridians() {
  return get('/api/v1/acupoints/meridians/list')
}

export default {
  getAcupointsList,
  getAcupointDetail,
  getAcupointRecommendation,
  getAcupointsBySymptom,
  getAcupointsByMeridian,
  getBodyParts,
  getMeridians
}
