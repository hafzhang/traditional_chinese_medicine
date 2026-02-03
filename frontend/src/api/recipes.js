/**
 * 食谱相关 API - Phase 2
 */
import { get } from '@/utils/request.js'

/**
 * 获取食谱列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码（从1开始）
 * @param {number} params.page_size - 每页数量
 * @param {string} params.constitution - 体质筛选
 * @param {string} params.efficacy - 功效标签筛选
 * @param {string} params.difficulty - 难度筛选
 * @param {string} params.solar_term - 节气筛选
 * @param {string} params.season - 季节筛选
 * @returns {Promise}
 */
export function getRecipesList(params = {}) {
  // Convert skip/limit to page/page_size for backward compatibility
  const apiParams = { ...params }
  if (params.skip !== undefined) {
    apiParams.page = Math.floor(params.skip / (params.limit || 20)) + 1
    delete apiParams.skip
  }
  if (params.limit !== undefined) {
    apiParams.page_size = params.limit
    delete apiParams.limit
  }
  return get('/api/v1/recipes', apiParams)
}

/**
 * 获取食谱详情
 * @param {string} recipeId - 食谱ID
 * @returns {Promise}
 */
export function getRecipeDetail(recipeId) {
  return get(`/api/v1/recipes/detail/${recipeId}`)
}

/**
 * 搜索食谱
 * @param {Object} params - 查询参数
 * @param {string} params.keyword - 搜索关键词
 * @param {number} params.page - 页码（从1开始）
 * @param {number} params.page_size - 每页数量
 * @param {string} params.constitution - 体质筛选
 * @param {string} params.difficulty - 难度筛选
 * @returns {Promise}
 */
export function searchRecipes(params = {}) {
  return get('/api/v1/recipes/search', params)
}

/**
 * 根据体质获取推荐食谱
 * @param {Object} params - 查询参数
 * @param {string} params.constitution - 体质代码
 * @param {number} params.limit - 限制数量
 * @returns {Promise}
 */
export function getRecipeRecommendations(params = {}) {
  return get('/api/v1/recipes/recommendations', params)
}

/**
 * 体质代码列表
 */
export const CONSTITUTIONS = [
  { value: 'peace', label: '平和质' },
  { value: 'qi_deficiency', label: '气虚质' },
  { value: 'yang_deficiency', label: '阳虚质' },
  { value: 'yin_deficiency', label: '阴虚质' },
  { value: 'phlegm_damp', label: '痰湿质' },
  { value: 'damp_heat', label: '湿热质' },
  { value: 'blood_stasis', label: '血瘀质' },
  { value: 'qi_depression', label: '气郁质' },
  { value: 'special', label: '特禀质' }
]

/**
 * 季节列表
 */
export const SEASONS = [
  { value: 'spring', label: '春季' },
  { value: 'summer', label: '夏季' },
  { value: 'autumn', label: '秋季' },
  { value: 'winter', label: '冬季' }
]

/**
 * 难度级别列表
 */
export const DIFFICULTIES = [
  { value: 'easy', label: '简单', color: 'green' },
  { value: 'medium', label: '中等', color: 'orange' },
  { value: 'harder', label: '较难', color: 'red' },
  { value: 'hard', label: '困难', color: 'darkred' }
]

/**
 * 二十四节气列表
 */
export const SOLAR_TERMS = [
  // 春季节气
  { value: 'lichun', label: '立春', season: 'spring' },
  { value: 'yushui', label: '雨水', season: 'spring' },
  { value: 'jingzhe', label: '惊蛰', season: 'spring' },
  { value: 'chunfen', label: '春分', season: 'spring' },
  { value: 'qingming', label: '清明', season: 'spring' },
  { value: 'guyu', label: '谷雨', season: 'spring' },
  // 夏季节气
  { value: 'lixia', label: '立夏', season: 'summer' },
  { value: 'xiaoman', label: '小满', season: 'summer' },
  { value: 'mangzhong', label: '芒种', season: 'summer' },
  { value: 'xiazhi', label: '夏至', season: 'summer' },
  { value: 'xiaoshu', label: '小暑', season: 'summer' },
  { value: 'dashu', label: '大暑', season: 'summer' },
  // 秋季节气
  { value: 'liqiu', label: '立秋', season: 'autumn' },
  { value: 'chushu', label: '处暑', season: 'autumn' },
  { value: 'bailu', label: '白露', season: 'autumn' },
  { value: 'qiufen', label: '秋分', season: 'autumn' },
  { value: 'hanlu', label: '寒露', season: 'autumn' },
  { value: 'shuangjiang', label: '霜降', season: 'autumn' },
  // 冬季节气
  { value: 'lidong', label: '立冬', season: 'winter' },
  { value: 'xiaoxue', label: '小雪', season: 'winter' },
  { value: 'daxue', label: '大雪', season: 'winter' },
  { value: 'dongzhi', label: '冬至', season: 'winter' },
  { value: 'xiaohan', label: '小寒', season: 'winter' },
  { value: 'dahan', label: '大寒', season: 'winter' }
]

/**
 * 获取体质中文名称
 * @param {string} code - 体质代码
 * @returns {string}
 */
export function getConstitutionName(code) {
  const item = CONSTITUTIONS.find(c => c.value === code)
  return item ? item.label : code
}

/**
 * 获取难度中文名称
 * @param {string} code - 难度代码
 * @returns {string}
 */
export function getDifficultyName(code) {
  const item = DIFFICULTIES.find(d => d.value === code)
  return item ? item.label : code
}

/**
 * 获取难度颜色
 * @param {string} code - 难度代码
 * @returns {string}
 */
export function getDifficultyColor(code) {
  const item = DIFFICULTIES.find(d => d.value === code)
  return item ? item.color : 'gray'
}

export default {
  getRecipesList,
  getRecipeDetail,
  searchRecipes,
  getRecipeRecommendations,
  CONSTITUTIONS,
  SEASONS,
  DIFFICULTIES,
  SOLAR_TERMS,
  getConstitutionName,
  getDifficultyName,
  getDifficultyColor
}
