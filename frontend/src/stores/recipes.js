/**
 * 菜谱状态管理 - Pinia Store
 */
import { defineStore } from 'pinia'
import * as recipesApi from '@/api/recipes.js'

export const useRecipesStore = defineStore('recipes', {
  state: () => ({
    // 菜谱列表
    recipes: [],
    // 当前菜谱详情
    currentRecipe: null,
    // 筛选条件
    filters: {
      constitution: '',
      efficacy: '',
      solar_term: '',
      difficulty: '',
      max_cooking_time: null
    },
    // 分页信息
    pagination: {
      total: 0,
      page: 1,
      page_size: 20
    },
    // 加载状态
    loading: false,
    // 错误信息
    error: null
  }),

  getters: {
    /**
     * 是否还有更多数据
     */
    hasMore(state) {
      return state.pagination.page * state.pagination.page_size < state.pagination.total
    },

    /**
     * 是否有筛选条件
     */
    hasFilters(state) {
      return !!(
        state.filters.constitution ||
        state.filters.efficacy ||
        state.filters.solar_term ||
        state.filters.difficulty ||
        state.filters.max_cooking_time
      )
    }
  },

  actions: {
    /**
     * 加载菜谱列表（重置分页）
     * @param {Object} params - 查询参数
     * @param {number} params.page - 页码，默认1
     * @param {number} params.page_size - 每页数量，默认20
     * @param {boolean} params.reset - 是否重置列表，默认true
     */
    async loadRecipes(params = {}) {
      const { page = 1, page_size = 20, reset = true } = params

      this.loading = true
      this.error = null

      try {
        // 构建查询参数
        const queryParams = {
          page,
          page_size,
          ...this.filters
        }

        // 移除空值
        Object.keys(queryParams).forEach(key => {
          if (queryParams[key] === '' || queryParams[key] === null || queryParams[key] === undefined) {
            delete queryParams[key]
          }
        })

        const result = await recipesApi.getRecipes(queryParams)

        if (reset) {
          this.recipes = result.items
        } else {
          this.recipes = [...this.recipes, ...result.items]
        }

        this.pagination = {
          total: result.total,
          page: result.page,
          page_size: result.page_size
        }
      } catch (err) {
        console.error('加载菜谱列表失败:', err)
        this.error = err.message || '加载菜谱列表失败'
        throw err
      } finally {
        this.loading = false
      }
    },

    /**
     * 加载更多菜谱
     */
    async loadMoreRecipes() {
      if (!this.hasMore || this.loading) {
        return
      }

      const nextPage = this.pagination.page + 1
      await this.loadRecipes({ page: nextPage, page_size: this.pagination.page_size, reset: false })
    },

    /**
     * 加载菜谱详情
     * @param {string} id - 菜谱ID
     */
    async loadRecipeDetail(id) {
      this.loading = true
      this.error = null

      try {
        const recipe = await recipesApi.getRecipeDetail(id)
        this.currentRecipe = recipe
        return recipe
      } catch (err) {
        console.error('加载菜谱详情失败:', err)
        this.error = err.message || '加载菜谱详情失败'
        throw err
      } finally {
        this.loading = false
      }
    },

    /**
     * 搜索菜谱
     * @param {string} keyword - 搜索关键词
     * @param {Object} params - 查询参数
     */
    async searchRecipes(keyword, params = {}) {
      this.loading = true
      this.error = null

      try {
        const result = await recipesApi.searchRecipes(keyword, params)
        this.recipes = result.items
        this.pagination = {
          total: result.total,
          page: result.page,
          page_size: result.page_size
        }
        return result
      } catch (err) {
        console.error('搜索菜谱失败:', err)
        this.error = err.message || '搜索菜谱失败'
        throw err
      } finally {
        this.loading = false
      }
    },

    /**
     * 加载推荐菜谱
     * @param {string} type - 推荐类型 ('constitution', 'solar_term', 'efficacy')
     * @param {Object} params - 推荐参数
     */
    async loadRecommendations(type, params = {}) {
      this.loading = true
      this.error = null

      try {
        const result = await recipesApi.getRecommendations(type, params)
        this.recipes = result.items
        return result
      } catch (err) {
        console.error('加载推荐菜谱失败:', err)
        this.error = err.message || '加载推荐菜谱失败'
        throw err
      } finally {
        this.loading = false
      }
    },

    /**
     * 设置筛选条件
     * @param {string} key - 筛选键
     * @param {string|number} value - 筛选值
     */
    setFilter(key, value) {
      if (key in this.filters) {
        this.filters[key] = value
      }
    },

    /**
     * 重置筛选条件
     */
    resetFilters() {
      this.filters = {
        constitution: '',
        efficacy: '',
        solar_term: '',
        difficulty: '',
        max_cooking_time: null
      }
    },

    /**
     * 重置分页到第一页
     */
    resetPagination() {
      this.pagination = {
        total: 0,
        page: 1,
        page_size: 20
      }
    },

    /**
     * 清空当前菜谱
     */
    clearCurrentRecipe() {
      this.currentRecipe = null
    }
  }
})
