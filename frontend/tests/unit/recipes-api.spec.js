/**
 * 食谱 API 单元测试
 * Unit Tests for Recipes API
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import * as recipesApi from '@/api/recipes.js'

// Mock request module
vi.mock('@/utils/request.js', () => ({
  get: vi.fn(),
  post: vi.fn()
}))

import { get } from '@/utils/request.js'

describe('Recipes API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('getRecipesList', () => {
    it('应该获取食谱列表', async () => {
      const mockResponse = {
        code: 0,
        data: {
          items: [
            {
              id: 'recipe-001',
              name: '山药莲子粥',
              type: '粥类',
              difficulty: '简单',
              cooking_time: 60
            }
          ],
          total: 1
        }
      }
      get.mockResolvedValue(mockResponse)

      const result = await recipesApi.getRecipesList({ skip: 0, limit: 10 })

      expect(get).toHaveBeenCalledWith('/api/v1/recipes', { skip: 0, limit: 10 })
      expect(result).toEqual(mockResponse)
    })

    it('应该支持按类型筛选', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await recipesApi.getRecipesList({ type: '粥类' })

      expect(get).toHaveBeenCalledWith('/api/v1/recipes', { type: '粥类' })
    })

    it('应该支持按难度筛选', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await recipesApi.getRecipesList({ difficulty: '简单' })

      expect(get).toHaveBeenCalledWith('/api/v1/recipes', { difficulty: '简单' })
    })

    it('应该支持按体质筛选', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await recipesApi.getRecipesList({ constitution: 'qi_deficiency' })

      expect(get).toHaveBeenCalledWith('/api/v1/recipes', { constitution: 'qi_deficiency' })
    })

    it('应该支持搜索功能', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await recipesApi.getRecipesList({ search: '山药' })

      expect(get).toHaveBeenCalledWith('/api/v1/recipes', { search: '山药' })
    })

    it('应该支持分页参数', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await recipesApi.getRecipesList({ skip: 20, limit: 10 })

      expect(get).toHaveBeenCalledWith('/api/v1/recipes', { skip: 20, limit: 10 })
    })

    it('应该支持组合筛选条件', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await recipesApi.getRecipesList({
        type: '粥类',
        difficulty: '简单',
        constitution: 'qi_deficiency'
      })

      expect(get).toHaveBeenCalledWith('/api/v1/recipes', {
        type: '粥类',
        difficulty: '简单',
        constitution: 'qi_deficiency'
      })
    })

    it('默认参数应该为空对象', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await recipesApi.getRecipesList()

      expect(get).toHaveBeenCalledWith('/api/v1/recipes', {})
    })
  })

  describe('getRecipeDetail', () => {
    it('应该获取食谱详情', async () => {
      const mockResponse = {
        code: 0,
        data: {
          id: 'recipe-001',
          name: '山药莲子粥',
          type: '粥类',
          difficulty: '简单',
          cooking_time: 60,
          servings: 2,
          ingredients: [
            { name: '山药', amount: '50g' },
            { name: '莲子', amount: '30g' },
            { name: '大米', amount: '100g' }
          ],
          steps: [
            '将山药去皮切块',
            '莲子提前泡发',
            '大米洗净',
            '所有材料放入锅中煮1小时'
          ],
          nutrition_info: {
            calories: 150,
            protein: 5,
            fat: 2,
            carbohydrate: 30
          },
          suitable_constitutions: ['qi_deficiency'],
          tips: '莲子要提前泡发，煮的时间更长'
        }
      }
      get.mockResolvedValue(mockResponse)

      const result = await recipesApi.getRecipeDetail('recipe-001')

      expect(get).toHaveBeenCalledWith('/api/v1/recipes/recipe-001')
      expect(result).toEqual(mockResponse)
      expect(result.data.ingredients).toHaveLength(3)
      expect(result.data.steps).toHaveLength(4)
    })
  })

  describe('getRecipeRecommendation', () => {
    it('应该根据体质获取推荐食谱', async () => {
      const mockResponse = {
        code: 0,
        data: {
          constitution: 'qi_deficiency',
          constitution_name: '气虚质',
          recommended: [
            {
              id: 'recipe-001',
              name: '山药莲子粥',
              type: '粥类',
              difficulty: '简单',
              reason: '补气健脾，适合气虚体质'
            },
            {
              id: 'recipe-002',
              name: '黄芪炖鸡汤',
              type: '汤类',
              difficulty: '中等',
              reason: '补气养血，增强体质'
            }
          ]
        }
      }
      get.mockResolvedValue(mockResponse)

      const result = await recipesApi.getRecipeRecommendation('qi_deficiency')

      expect(get).toHaveBeenCalledWith('/api/v1/recipes/recommend/qi_deficiency')
      expect(result).toEqual(mockResponse)
      expect(result.data.recommended).toHaveLength(2)
    })

    it('应该支持平和体质', async () => {
      const mockResponse = {
        code: 0,
        data: {
          constitution: 'peace',
          constitution_name: '平和质',
          recommended: []
        }
      }
      get.mockResolvedValue(mockResponse)

      await recipesApi.getRecipeRecommendation('peace')

      expect(get).toHaveBeenCalledWith('/api/v1/recipes/recommend/peace')
    })

    it('应该为不同体质返回不同推荐', async () => {
      const constitutions = [
        'qi_deficiency',
        'yang_deficiency',
        'yin_deficiency',
        'phlegm_damp'
      ]

      for (const constitution of constitutions) {
        get.mockResolvedValue({
          code: 0,
          data: { constitution, recommended: [] }
        })

        await recipesApi.getRecipeRecommendation(constitution)

        expect(get).toHaveBeenCalledWith(`/api/v1/recipes/recommend/${constitution}`)
      }
    })
  })

  describe('getRecipeTypes', () => {
    it('应该获取食谱类型列表', async () => {
      const mockResponse = {
        code: 0,
        data: [
          '粥类',
          '汤类',
          '主食',
          '菜品',
          '茶饮',
          '甜品',
          '小食'
        ]
      }
      get.mockResolvedValue(mockResponse)

      const result = await recipesApi.getRecipeTypes()

      expect(get).toHaveBeenCalledWith('/api/v1/recipes/types/list')
      expect(result).toEqual(mockResponse)
      expect(result.data).toContain('粥类')
      expect(result.data).toContain('汤类')
    })
  })

  describe('getRecipeDifficulties', () => {
    it('应该获取食谱难度列表', async () => {
      const mockResponse = {
        code: 0,
        data: [
          { value: '简单', label: '简单', time_range: '30分钟内' },
          { value: '中等', label: '中等', time_range: '30-60分钟' },
          { value: '困难', label: '困难', time_range: '60分钟以上' }
        ]
      }
      get.mockResolvedValue(mockResponse)

      const result = await recipesApi.getRecipeDifficulties()

      expect(get).toHaveBeenCalledWith('/api/v1/recipes/difficulties/list')
      expect(result).toEqual(mockResponse)
      expect(result.data).toHaveLength(3)
    })
  })

  describe('餐次筛选', () => {
    it('应该支持按早餐筛选', async () => {
      const mockResponse = {
        code: 0,
        data: {
          items: [
            { id: 'recipe-001', name: '小米粥', meal_type: 'breakfast' }
          ],
          total: 1
        }
      }
      get.mockResolvedValue(mockResponse)

      await recipesApi.getRecipesList({ meal_type: 'breakfast' })

      expect(get).toHaveBeenCalledWith('/api/v1/recipes', { meal_type: 'breakfast' })
    })

    it('应该支持按午餐筛选', async () => {
      const mockResponse = {
        code: 0,
        data: {
          items: [
            { id: 'recipe-002', name: '山药排骨汤', meal_type: 'lunch' }
          ],
          total: 1
        }
      }
      get.mockResolvedValue(mockResponse)

      await recipesApi.getRecipesList({ meal_type: 'lunch' })

      expect(get).toHaveBeenCalledWith('/api/v1/recipes', { meal_type: 'lunch' })
    })

    it('应该支持按晚餐筛选', async () => {
      const mockResponse = {
        code: 0,
        data: {
          items: [
            { id: 'recipe-003', name: '养胃粥', meal_type: 'dinner' }
          ],
          total: 1
        }
      }
      get.mockResolvedValue(mockResponse)

      await recipesApi.getRecipesList({ meal_type: 'dinner' })

      expect(get).toHaveBeenCalledWith('/api/v1/recipes', { meal_type: 'dinner' })
    })
  })

  describe('错误处理', () => {
    it('应该处理网络错误', async () => {
      get.mockRejectedValue(new Error('Network error'))

      await expect(recipesApi.getRecipesList()).rejects.toThrow('Network error')
    })

    it('应该处理 API 错误响应', async () => {
      get.mockRejectedValue({
        code: -1,
        message: '参数错误'
      })

      await expect(recipesApi.getRecipesList()).rejects.toEqual({
        code: -1,
        message: '参数错误'
      })
    })

    it('应该处理不存在的食谱ID', async () => {
      get.mockRejectedValue({
        code: -1,
        message: '食谱不存在'
      })

      await expect(recipesApi.getRecipeDetail('non-existent-id')).rejects.toEqual({
        code: -1,
        message: '食谱不存在'
      })
    })

    it('应该处理无效的体质代码', async () => {
      get.mockRejectedValue({
        code: -1,
        message: '无效的体质代码'
      })

      await expect(recipesApi.getRecipeRecommendation('invalid')).rejects.toEqual({
        code: -1,
        message: '无效的体质代码'
      })
    })
  })
})
