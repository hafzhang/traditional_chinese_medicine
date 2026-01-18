/**
 * 舌诊相关 API - Phase 1
 */
import { post, get } from '@/utils/request.js'

/**
 * 分析舌象
 * @param {Object} data - 舌象数据
 * @param {string} data.tongue_color - 舌质颜色
 * @param {string} data.tongue_shape - 舌质形态
 * @param {string} data.coating_color - 苔色
 * @param {string} data.coating_thickness - 苔质
 * @param {string} data.result_id - 测试结果ID（可选）
 * @returns {Promise}
 */
export function analyzeTongue(data) {
  return post('/api/v1/tongue/analyze', data)
}

/**
 * 获取用户舌诊记录
 * @param {string} userId - 用户ID
 * @returns {Promise}
 */
export function getTongueRecords(userId) {
  return get(`/api/v1/tongue/records/${userId}`)
}

/**
 * 获取舌诊选项列表
 * @returns {Promise}
 */
export function getTongueOptions() {
  return get('/api/v1/tongue/options')
}

export default {
  analyzeTongue,
  getTongueRecords,
  getTongueOptions
}
