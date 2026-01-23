/**
 * 穴位 API 单元测试
 * Unit Tests for Acupoints API
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import * as acupointsApi from '@/api/acupoints.js'

// Mock request module
vi.mock('@/utils/request.js', () => ({
  get: vi.fn(),
  post: vi.fn()
}))

import { get } from '@/utils/request.js'

describe('Acupoints API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('getAcupointsList', () => {
    it('应该获取穴位列表', async () => {
      const mockResponse = {
        code: 0,
        data: {
          items: [
            { id: 'acupoint-001', name: '足三里', location: '小腿前外侧' }
          ],
          total: 1
        }
      }
      get.mockResolvedValue(mockResponse)

      const result = await acupointsApi.getAcupointsList({ skip: 0, limit: 10 })

      expect(get).toHaveBeenCalledWith('/api/v1/acupoints', { skip: 0, limit: 10 })
      expect(result).toEqual(mockResponse)
    })

    it('应该支持按部位筛选', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await acupointsApi.getAcupointsList({ body_part: '下肢' })

      expect(get).toHaveBeenCalledWith('/api/v1/acupoints', { body_part: '下肢' })
    })

    it('应该支持按体质筛选', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await acupointsApi.getAcupointsList({ constitution: 'qi_deficiency' })

      expect(get).toHaveBeenCalledWith('/api/v1/acupoints', { constitution: 'qi_deficiency' })
    })

    it('应该支持搜索功能', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await acupointsApi.getAcupointsList({ search: '足三里' })

      expect(get).toHaveBeenCalledWith('/api/v1/acupoints', { search: '足三里' })
    })

    it('应该支持分页参数', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await acupointsApi.getAcupointsList({ skip: 20, limit: 10 })

      expect(get).toHaveBeenCalledWith('/api/v1/acupoints', { skip: 20, limit: 10 })
    })

    it('默认参数应该为空对象', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await acupointsApi.getAcupointsList()

      expect(get).toHaveBeenCalledWith('/api/v1/acupoints', {})
    })
  })

  describe('getAcupointDetail', () => {
    it('应该获取穴位详情', async () => {
      const mockResponse = {
        code: 0,
        data: {
          id: 'acupoint-001',
          name: '足三里',
          location: '小腿前外侧',
          meridian: '足阳明胃经'
        }
      }
      get.mockResolvedValue(mockResponse)

      const result = await acupointsApi.getAcupointDetail('acupoint-001')

      expect(get).toHaveBeenCalledWith('/api/v1/acupoints/acupoint-001')
      expect(result).toEqual(mockResponse)
    })
  })

  describe('getAcupointRecommendation', () => {
    it('应该根据体质获取推荐穴位', async () => {
      const mockResponse = {
        code: 0,
        data: {
          constitution: 'qi_deficiency',
          constitution_name: '气虚质',
          recommended: [
            {
              id: 'acupoint-001',
              name: '足三里',
              reason: '补气健脾，增强体质'
            }
          ]
        }
      }
      get.mockResolvedValue(mockResponse)

      const result = await acupointsApi.getAcupointRecommendation('qi_deficiency')

      expect(get).toHaveBeenCalledWith('/api/v1/acupoints/recommend/qi_deficiency')
      expect(result).toEqual(mockResponse)
    })

    it('应该支持平和体质', async () => {
      const mockResponse = { code: 0, data: { recommended: [] } }
      get.mockResolvedValue(mockResponse)

      await acupointsApi.getAcupointRecommendation('peace')

      expect(get).toHaveBeenCalledWith('/api/v1/acupoints/recommend/peace')
    })
  })

  describe('getAcupointsBySymptom', () => {
    it('应该根据症状查找穴位', async () => {
      const mockResponse = {
        code: 0,
        data: [
          {
            id: 'acupoint-001',
            name: '足三里',
            symptom: '消化不良',
            priority: 1
          }
        ]
      }
      get.mockResolvedValue(mockResponse)

      const result = await acupointsApi.getAcupointsBySymptom('消化不良')

      expect(get).toHaveBeenCalledWith('/api/v1/acupoints/symptom/消化不良')
      expect(result).toEqual(mockResponse)
    })

    it('应该支持多穴位症状', async () => {
      const mockResponse = {
        code: 0,
        data: [
          { id: 'acupoint-001', name: '内关', symptom: '失眠', priority: 1 },
          { id: 'acupoint-002', name: '神门', symptom: '失眠', priority: 2 }
        ]
      }
      get.mockResolvedValue(mockResponse)

      await acupointsApi.getAcupointsBySymptom('失眠')

      expect(get).toHaveBeenCalledWith('/api/v1/acupoints/symptom/失眠')
    })
  })

  describe('getAcupointsByMeridian', () => {
    it('应该根据经络获取穴位', async () => {
      const mockResponse = {
        code: 0,
        data: [
          {
            id: 'acupoint-001',
            name: '足三里',
            meridian: '足阳明胃经'
          },
          {
            id: 'acupoint-002',
            name: '天枢',
            meridian: '足阳明胃经'
          }
        ]
      }
      get.mockResolvedValue(mockResponse)

      const result = await acupointsApi.getAcupointsByMeridian('足阳明胃经')

      expect(get).toHaveBeenCalledWith('/api/v1/acupoints/meridian/足阳明胃经')
      expect(result).toEqual(mockResponse)
    })

    it('应该支持十二正经', async () => {
      const meridians = [
        '手太阴肺经', '手阳明大肠经', '足阳明胃经', '足太阴脾经',
        '手少阴心经', '手太阳小肠经', '足太阳膀胱经', '足少阴肾经',
        '手厥阴心包经', '手少阳三焦经', '足少阳胆经', '足厥阴肝经'
      ]

      for (const meridian of meridians) {
        get.mockResolvedValue({ code: 0, data: [] })
        await acupointsApi.getAcupointsByMeridian(meridian)
        expect(get).toHaveBeenCalledWith(`/api/v1/acupoints/meridian/${meridian}`)
      }
    })
  })

  describe('getBodyParts', () => {
    it('应该获取部位列表', async () => {
      const mockResponse = {
        code: 0,
        data: ['头面部', '上肢', '下肢', '胸腹部', '腰背部']
      }
      get.mockResolvedValue(mockResponse)

      const result = await acupointsApi.getBodyParts()

      expect(get).toHaveBeenCalledWith('/api/v1/acupoints/body-parts/list')
      expect(result).toEqual(mockResponse)
    })
  })

  describe('getMeridians', () => {
    it('应该获取经络列表', async () => {
      const mockResponse = {
        code: 0,
        data: [
          '手太阴肺经', '手阳明大肠经', '足阳明胃经', '足太阴脾经',
          '手少阴心经', '手太阳小肠经', '足太阳膀胱经', '足少阴肾经',
          '手厥阴心包经', '手少阳三焦经', '足少阳胆经', '足厥阴肝经',
          '督脉', '任脉'
        ]
      }
      get.mockResolvedValue(mockResponse)

      const result = await acupointsApi.getMeridians()

      expect(get).toHaveBeenCalledWith('/api/v1/acupoints/meridians/list')
      expect(result).toEqual(mockResponse)
    })
  })

  describe('错误处理', () => {
    it('应该处理网络错误', async () => {
      get.mockRejectedValue(new Error('Network error'))

      await expect(acupointsApi.getAcupointsList()).rejects.toThrow('Network error')
    })

    it('应该处理 API 错误响应', async () => {
      get.mockRejectedValue({
        code: -1,
        message: '参数错误'
      })

      await expect(acupointsApi.getAcupointsList()).rejects.toEqual({
        code: -1,
        message: '参数错误'
      })
    })
  })
})
