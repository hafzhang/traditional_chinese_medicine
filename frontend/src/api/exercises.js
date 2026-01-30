/**
 * 运动/功法相关 API - MVP
 */
import { get, post, put } from '@/utils/request.js'

/**
 * 获取运动列表
 * @param {Object} params - 查询参数
 * @param {number} params.skip - 跳过数量
 * @param {number} params.limit - 限制数量
 * @param {string} params.exercise_type - 运动类型筛选
 * @param {string} params.difficulty_level - 难度级别筛选
 * @param {string} params.search - 搜索关键词
 * @returns {Promise<Object>} 返回 {total, items}
 */
export function getExercises(params = {}) {
  return get('/api/v1/exercises', params).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取运动列表失败')
  })
}

/**
 * 获取运动类型列表
 * @returns {Promise<Array>} 返回类型列表
 */
export function getExerciseTypes() {
  return get('/api/v1/exercises/types').then(res => {
    if (res.code === 0) return res.data.types
    throw new Error(res.message || '获取运动类型失败')
  })
}

/**
 * 根据体质获取推荐运动
 * @param {string} constitutionCode - 体质代码
 * @param {Object} params - 查询参数
 * @param {number} params.limit - 限制数量
 * @returns {Promise<Object>} 返回 {constitution, total, items}
 */
export function getExercisesByConstitution(constitutionCode, params = {}) {
  return get(`/api/v1/exercises/constitution/${constitutionCode}`, params).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取推荐运动失败')
  })
}

/**
 * 获取个性化运动方案（早中晚）
 * @param {string} constitutionCode - 体质代码
 * @returns {Promise<Object>} 返回 {constitution, routine: {morning, afternoon, evening}}
 */
export function getPersonalizedRoutine(constitutionCode) {
  return get(`/api/v1/exercises/routine/${constitutionCode}`).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取运动方案失败')
  })
}

/**
 * 获取周运动计划
 * @param {string} constitutionCode - 体质代码
 * @param {number} week - 第几周
 * @returns {Promise<Object>} 返回 {week, constitution, daily_plan}
 */
export function getExercisePlanWeek(constitutionCode, week) {
  return get(`/api/v1/exercises/plan/${constitutionCode}/${week}`).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取周计划失败')
  })
}

/**
 * 获取运动详情
 * @param {string} exerciseId - 运动ID
 * @returns {Promise<Object>} 返回运动详情
 */
export function getExerciseDetail(exerciseId) {
  return get(`/api/v1/exercises/${exerciseId}`).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取运动详情失败')
  })
}

/**
 * 增加运动浏览次数
 * @param {string} exerciseId - 运动ID
 * @returns {Promise<Object>}
 */
export function incrementViewCount(exerciseId) {
  return post(`/api/v1/exercises/${exerciseId}/view`).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '操作失败')
  })
}

export default {
  getExercises,
  getExerciseTypes,
  getExercisesByConstitution,
  getPersonalizedRoutine,
  getExercisePlanWeek,
  getExerciseDetail,
  incrementViewCount
}
