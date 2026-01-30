/**
 * 起居作息相关 API - MVP
 */
import { get } from '@/utils/request.js'

/**
 * 获取所有作息方案列表
 * @param {Object} params - 查询参数
 * @param {number} params.skip - 跳过数量
 * @param {number} params.limit - 限制数量
 * @returns {Promise<Object>} 返回 {total, items}
 */
export function getRoutines(params = {}) {
  return get('/api/v1/routines', params).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取作息方案列表失败')
  })
}

/**
 * 根据体质获取作息方案
 * @param {string} constitutionCode - 体质代码
 * @returns {Promise<Object>} 返回作息方案详情
 */
export function getRoutineByConstitution(constitutionCode) {
  return get(`/api/v1/routines/constitution/${constitutionCode}`).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取作息方案失败')
  })
}

/**
 * 获取体质作息方案摘要
 * @param {string} constitutionCode - 体质代码
 * @returns {Promise<Object>} 返回摘要信息
 */
export function getRoutineSummary(constitutionCode) {
  return get(`/api/v1/routines/constitution/${constitutionCode}/summary`).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取作息摘要失败')
  })
}

/**
 * 生成今日作息时间表
 * @param {string} userId - 用户ID
 * @param {string} constitutionCode - 体质代码
 * @returns {Promise<Object>} 返回今日时间表
 */
export function getTodaySchedule(userId, constitutionCode) {
  return get(`/api/v1/routines/today/${userId}/${constitutionCode}`).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取今日时间表失败')
  })
}

/**
 * 获取季节性作息调整
 * @param {string} constitutionCode - 体质代码
 * @param {string} season - 季节 (spring/summer/autumn/winter)
 * @returns {Promise<Object>} 返回季节调整
 */
export function getSeasonalAdjustment(constitutionCode, season) {
  return get(`/api/v1/routines/seasonal/${constitutionCode}/${season}`).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取季节调整失败')
  })
}

/**
 * 获取作息方案及当前季节信息
 * @param {string} constitutionCode - 体质代码
 * @returns {Promise<Object>} 返回完整作息方案和季节信息
 */
export function getRoutineWithSeasonalInfo(constitutionCode) {
  return get(`/api/v1/routines/constitution/${constitutionCode}/full`).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取作息方案失败')
  })
}

/**
 * 获取作息方案详情
 * @param {string} routineId - 作息方案ID
 * @returns {Promise<Object>} 返回详情
 */
export function getRoutineDetail(routineId) {
  return get(`/api/v1/routines/${routineId}`).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取作息详情失败')
  })
}

export default {
  getRoutines,
  getRoutineByConstitution,
  getRoutineSummary,
  getTodaySchedule,
  getSeasonalAdjustment,
  getRoutineWithSeasonalInfo,
  getRoutineDetail
}
