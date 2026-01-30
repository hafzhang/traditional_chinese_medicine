/**
 * 健康打卡相关 API - MVP
 */
import { get, post, put } from '@/utils/request.js'

/**
 * 创建新的周打卡记录
 * @param {Object} data - 打卡数据
 * @param {string} data.user_id - 用户ID
 * @param {number} data.week_number - 第几周
 * @returns {Promise<Object>} 返回创建的打卡记录
 */
export function createWeeklyCheckin(data) {
  return post('/api/v1/checkins', data).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '创建打卡记录失败')
  })
}

/**
 * 获取用户的打卡记录列表
 * @param {string} userId - 用户ID
 * @param {Object} params - 查询参数
 * @param {number} params.skip - 跳过数量
 * @param {number} params.limit - 限制数量
 * @returns {Promise<Object>} 返回 {total, items}
 */
export function getUserCheckins(userId, params = {}) {
  return get('/api/v1/checkins', { user_id: userId, ...params }).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取打卡记录失败')
  })
}

/**
 * 获取用户本周的打卡记录
 * @param {string} userId - 用户ID
 * @returns {Promise<Object>} 返回本周打卡记录
 */
export function getCurrentWeekCheckin(userId) {
  return get(`/api/v1/checkins/current/${userId}`).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取本周打卡记录失败')
  })
}

/**
 * 获取打卡记录详情
 * @param {string} checkinId - 打卡记录ID
 * @returns {Promise<Object>} 返回详情
 */
export function getCheckinDetail(checkinId) {
  return get(`/api/v1/checkins/${checkinId}`).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取打卡详情失败')
  })
}

/**
 * 更新某日的打卡数据
 * @param {string} checkinId - 打卡记录ID
 * @param {number} day - 第几天 (1-7)
 * @param {Object} data - 打卡数据
 * @returns {Promise<Object>} 返回更新后的打卡记录
 */
export function updateDailyEntry(checkinId, day, data) {
  return put(`/api/v1/checkins/${checkinId}/day/${day}`, data).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '更新打卡数据失败')
  })
}

/**
 * 获取周打卡汇总
 * @param {string} checkinId - 打卡记录ID
 * @returns {Promise<Object>} 返回汇总数据
 */
export function getWeekSummary(checkinId) {
  return get(`/api/v1/checkins/${checkinId}/summary`).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取周汇总失败')
  })
}

/**
 * 生成周报数据
 * @param {string} checkinId - 打卡记录ID
 * @returns {Promise<Object>} 返回周报数据
 */
export function getWeeklyReport(checkinId) {
  return get(`/api/v1/checkins/${checkinId}/report`).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '生成周报失败')
  })
}

/**
 * 计算用户连续打卡天数
 * @param {string} userId - 用户ID
 * @returns {Promise<Object>} 返回 {user_id, current_streak}
 */
export function getProgressStreak(userId) {
  return get(`/api/v1/checkins/streak/${userId}`).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取连续打卡天数失败')
  })
}

/**
 * 获取用户整体进度概览
 * @param {string} userId - 用户ID
 * @returns {Promise<Object>} 返回进度概览
 */
export function getUserProgressOverview(userId) {
  return get(`/api/v1/checkins/progress/${userId}/overview`).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取进度概览失败')
  })
}

/**
 * 获取AI周建议
 * @param {string} checkinId - 打卡记录ID
 * @returns {Promise<Object>} 返回AI建议
 */
export function getWeeklyRecommendations(checkinId) {
  return get(`/api/v1/checkins/${checkinId}/recommendations`).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取AI建议失败')
  })
}

/**
 * 生成鼓励信息
 * @param {string} userId - 用户ID
 * @param {number} streak - 连续打卡天数
 * @returns {Promise<Object>} 返回鼓励信息
 */
export function getMotivationalMessage(userId, streak = 0) {
  return get(`/api/v1/checkins/motivational/${userId}`, { streak }).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '获取鼓励信息失败')
  })
}

/**
 * 识别风险因素
 * @param {string} userId - 用户ID
 * @returns {Promise<Object>} 返回风险因素列表
 */
export function identifyRiskFactors(userId) {
  return get(`/api/v1/checkins/risks/${userId}`).then(res => {
    if (res.code === 0) return res.data
    throw new Error(res.message || '识别风险因素失败')
  })
}

export default {
  createWeeklyCheckin,
  getUserCheckins,
  getCurrentWeekCheckin,
  getCheckinDetail,
  updateDailyEntry,
  getWeekSummary,
  getWeeklyReport,
  getProgressStreak,
  getUserProgressOverview,
  getWeeklyRecommendations,
  getMotivationalMessage,
  identifyRiskFactors
}
