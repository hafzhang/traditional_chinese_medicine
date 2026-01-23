/**
 * 食材 API 单元测试
 * Unit Tests for Ingredients API
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import * as ingredientsApi from '@/api/ingredients.js'

// Mock request module
vi.mock('@/utils/request.js', () => ({
  get: vi.fn(),
  post: vi.fn()
}))

import { get } from '@/utils/request.js'

describe('Ingredients API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('getIngredientsList', () => {
    it('应该获取食材列表', async () => {
      const mockResponse = {
        code: 0,
        data: {
          items: [
            { id: 'ingredient-001', name: '山药', category: '蔬菜', nature: '平' }
          ],
          total: 1
        }
      }
      get.mockResolvedValue(mockResponse)

      const result = await ingredientsApi.getIngredientsList({ skip: 0, limit: 10 })

      expect(get).toHaveBeenCalledWith('/api/v1/ingredients', { skip: 0, limit: 10 })
      expect(result).toEqual(mockResponse)
    })

    it('应该支持按类别筛选', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await ingredientsApi.getIngredientsList({ category: '蔬菜' })

      expect(get).toHaveBeenCalledWith('/api/v1/ingredients', { category: '蔬菜' })
    })

    it('应该支持按性味筛选', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await ingredientsApi.getIngredientsList({ nature: '平' })

      expect(get).toHaveBeenCalledWith('/api/v1/ingredients', { nature: '平' })
    })

    it('应该支持搜索功能', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await ingredientsApi.getIngredientsList({ search: '山药' })

      expect(get).toHaveBeenCalledWith('/api/v1/ingredients', { search: '山药' })
    })

    it('应该支持分页参数', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await ingredientsApi.getIngredientsList({ skip: 20, limit: 10 })

      expect(get).toHaveBeenCalledWith('/api/v1/ingredients', { skip: 20, limit: 10 })
    })

    it('应该支持组合筛选条件', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await ingredientsApi.getIngredientsList({
        category: '蔬菜',
        nature: '平',
        search: '健脾'
      })

      expect(get).toHaveBeenCalledWith('/api/v1/ingredients', {
        category: '蔬菜',
        nature: '平',
        search: '健脾'
      })
    })

    it('默认参数应该为空对象', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await ingredientsApi.getIngredientsList()

      expect(get).toHaveBeenCalledWith('/api/v1/ingredients', {})
    })
  })

  describe('getIngredientDetail', () => {
    it('应该获取食材详情', async () => {
      const mockResponse = {
        code: 0,
        data: {
          id: 'ingredient-001',
          name: '山药',
          aliases: ['怀山药', '淮山'],
          category: '蔬菜',
          nature: '平',
          flavor: '甘',
          efficacy: '健脾养胃、补肺益肾',
          suitable_constitutions: ['qi_deficiency', 'yin_deficiency'],
          avoid_constitutions: ['phlegm_damp']
        }
      }
      get.mockResolvedValue(mockResponse)

      const result = await ingredientsApi.getIngredientDetail('ingredient-001')

      expect(get).toHaveBeenCalledWith('/api/v1/ingredients/ingredient-001')
      expect(result).toEqual(mockResponse)
    })
  })

  describe('getIngredientRecommendation', () => {
    it('应该根据体质获取推荐食材', async () => {
      const mockResponse = {
        code: 0,
        data: {
          constitution: 'qi_deficiency',
          constitution_name: '气虚质',
          recommended: [
            {
              id: 'ingredient-001',
              name: '山药',
              category: '蔬菜',
              nature: '平',
              efficacy: '健脾养胃、补肺益肾',
              reason: '补气健脾，增强体质'
            }
          ],
          avoided: [
            {
              id: 'ingredient-002',
              name: '山楂',
              category: '水果',
              reason: '酸味较重，可能损伤脾胃'
            }
          ]
        }
      }
      get.mockResolvedValue(mockResponse)

      const result = await ingredientsApi.getIngredientRecommendation('qi_deficiency')

      expect(get).toHaveBeenCalledWith('/api/v1/ingredients/recommend/qi_deficiency')
      expect(result).toEqual(mockResponse)
      expect(result.data.recommended).toHaveLength(1)
      expect(result.data.avoided).toHaveLength(1)
    })

    it('应该支持平和体质', async () => {
      const mockResponse = {
        code: 0,
        data: {
          constitution: 'peace',
          constitution_name: '平和质',
          recommended: [],
          avoided: []
        }
      }
      get.mockResolvedValue(mockResponse)

      await ingredientsApi.getIngredientRecommendation('peace')

      expect(get).toHaveBeenCalledWith('/api/v1/ingredients/recommend/peace')
    })

    it('应该为不同体质返回不同推荐', async () => {
      const constitutions = [
        'qi_deficiency',
        'yang_deficiency',
        'yin_deficiency',
        'phlegm_damp',
        'damp_heat',
        'blood_stasis',
        'qi_depression',
        'special'
      ]

      for (const constitution of constitutions) {
        get.mockResolvedValue({
          code: 0,
          data: { constitution, recommended: [], avoided: [] }
        })

        await ingredientsApi.getIngredientRecommendation(constitution)

        expect(get).toHaveBeenCalledWith(`/api/v1/ingredients/recommend/${constitution}`)
      }
    })
  })

  describe('getIngredientCategories', () => {
    it('应该获取食材类别列表', async () => {
      const mockResponse = {
        code: 0,
        data: [
          '蔬菜',
          '水果',
          '谷物',
          '肉类',
          '水产',
          '蛋奶',
          '调料',
          '药材',
          '其他'
        ]
      }
      get.mockResolvedValue(mockResponse)

      const result = await ingredientsApi.getIngredientCategories()

      expect(get).toHaveBeenCalledWith('/api/v1/ingredients/categories/list')
      expect(result).toEqual(mockResponse)
      expect(result.data).toContain('蔬菜')
      expect(result.data).toContain('水果')
    })
  })

  describe('getIngredientNatures', () => {
    it('应该获取食材性味列表', async () => {
      const mockResponse = {
        code: 0,
        data: [
          { value: '寒', label: '寒' },
          { value: '凉', label: '凉' },
          { value: '平', label: '平' },
          { value: '温', label: '温' },
          { value: '热', label: '热' }
        ]
      }
      get.mockResolvedValue(mockResponse)

      const result = await ingredientsApi.getIngredientNatures()

      expect(get).toHaveBeenCalledWith('/api/v1/ingredients/natures/list')
      expect(result).toEqual(mockResponse)
      expect(result.data).toHaveLength(5)
    })
  })

  describe('错误处理', () => {
    it('应该处理网络错误', async () => {
      get.mockRejectedValue(new Error('Network error'))

      await expect(ingredientsApi.getIngredientsList()).rejects.toThrow('Network error')
    })

    it('应该处理 API 错误响应', async () => {
      get.mockRejectedValue({
        code: -1,
        message: '参数错误'
      })

      await expect(ingredientsApi.getIngredientsList()).rejects.toEqual({
        code: -1,
        message: '参数错误'
      })
    })

    it('应该处理不存在的食材ID', async () => {
      get.mockRejectedValue({
        code: -1,
        message: '食材不存在'
      })

      await expect(ingredientsApi.getIngredientDetail('non-existent-id')).rejects.toEqual({
        code: -1,
        message: '食材不存在'
      })
    })

    it('应该处理无效的体质代码', async () => {
      get.mockRejectedValue({
        code: -1,
        message: '无效的体质代码'
      })

      await expect(ingredientsApi.getIngredientRecommendation('invalid')).rejects.toEqual({
        code: -1,
        message: '无效的体质代码'
      })
    })
  })
})
