/**
 * 舌诊 API 单元测试
 * Unit Tests for Tongue Diagnosis API
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import * as tongueApi from '@/api/tongue.js'

// Mock request module
vi.mock('@/utils/request.js', () => ({
  get: vi.fn(),
  post: vi.fn()
}))

import { get, post } from '@/utils/request.js'

describe('Tongue Diagnosis API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('analyzeTongue', () => {
    it('应该分析舌象并返回体质结果', async () => {
      const mockResponse = {
        code: 0,
        data: {
          constitution: 'qi_deficiency',
          constitution_name: '气虚质',
          scores: {
            peace: 15,
            qi_deficiency: 85,
            yang_deficiency: 30,
            yin_deficiency: 20
          },
          analysis: {
            tongue_color: '淡白',
            tongue_shape: '胖大有齿痕',
            coating_color: '白',
            coating_thickness: '薄白'
          },
          advice: {
            diet: ['多吃补气健脾食物', '如山药、红枣、莲子'],
            lifestyle: ['避免过度劳累', '保持充足睡眠']
          }
        }
      }
      post.mockResolvedValue(mockResponse)

      const tongueData = {
        tongue_color: '淡白',
        tongue_shape: '胖大有齿痕',
        coating_color: '白',
        coating_thickness: '薄白'
      }

      const result = await tongueApi.analyzeTongue(tongueData)

      expect(post).toHaveBeenCalledWith('/api/v1/tongue/analyze', tongueData)
      expect(result).toEqual(mockResponse)
    })

    it('应该支持关联问卷结果ID', async () => {
      const mockResponse = {
        code: 0,
        data: {
          constitution: 'qi_deficiency',
          comparison: {
            questionnaire_result: 'yang_deficiency',
            tongue_result: 'qi_deficiency',
            match: false
          }
        }
      }
      post.mockResolvedValue(mockResponse)

      const tongueData = {
        tongue_color: '淡白',
        tongue_shape: '胖大有齿痕',
        coating_color: '白',
        coating_thickness: '薄白',
        result_id: 'result-123'
      }

      await tongueApi.analyzeTongue(tongueData)

      expect(post).toHaveBeenCalledWith('/api/v1/tongue/analyze', tongueData)
      expect(tongueData.result_id).toBe('result-123')
    })

    it('应该处理所有舌质颜色选项', async () => {
      const tongueColors = ['淡白', '淡红', '红', '绛', '青紫']
      post.mockResolvedValue({ code: 0, data: { constitution: 'peace' } })

      for (const color of tongueColors) {
        await tongueApi.analyzeTongue({
          tongue_color: color,
          tongue_shape: '正常',
          coating_color: '白',
          coating_thickness: '薄白'
        })
      }

      expect(post).toHaveBeenCalledTimes(5)
    })

    it('应该处理所有舌质形态选项', async () => {
      const tongueShapes = ['正常', '胖大', '瘦薄', '齿痕', '裂纹', '芒刺']
      post.mockResolvedValue({ code: 0, data: { constitution: 'peace' } })

      for (const shape of tongueShapes) {
        await tongueApi.analyzeTongue({
          tongue_color: '淡红',
          tongue_shape: shape,
          coating_color: '白',
          coating_thickness: '薄白'
        })
      }

      expect(post).toHaveBeenCalledTimes(6)
    })

    it('应该处理所有苔色选项', async () => {
      const coatingColors = ['白', '黄', '灰黑']
      post.mockResolvedValue({ code: 0, data: { constitution: 'peace' } })

      for (const color of coatingColors) {
        await tongueApi.analyzeTongue({
          tongue_color: '淡红',
          tongue_shape: '正常',
          coating_color: color,
          coating_thickness: '薄白'
        })
      }

      expect(post).toHaveBeenCalledTimes(3)
    })

    it('应该处理所有苔质选项', async () => {
      const coatingThickness = ['薄白', '白腻', '黄腻', '厚白', '厚黄', '少苔', '无苔', '剥苔']
      post.mockResolvedValue({ code: 0, data: { constitution: 'peace' } })

      for (const thickness of coatingThickness) {
        await tongueApi.analyzeTongue({
          tongue_color: '淡红',
          tongue_shape: '正常',
          coating_color: '白',
          coating_thickness: thickness
        })
      }

      expect(post).toHaveBeenCalledTimes(8)
    })
  })

  describe('getTongueRecords', () => {
    it('应该获取用户舌诊记录', async () => {
      const mockResponse = {
        code: 0,
        data: [
          {
            id: 'record-001',
            user_id: 'user-123',
            tongue_color: '淡白',
            tongue_shape: '胖大有齿痕',
            coating_color: '白',
            coating_thickness: '薄白',
            constitution: 'qi_deficiency',
            created_at: '2026-01-20T10:00:00'
          },
          {
            id: 'record-002',
            user_id: 'user-123',
            tongue_color: '淡红',
            tongue_shape: '正常',
            coating_color: '白',
            coating_thickness: '薄白',
            constitution: 'peace',
            created_at: '2026-01-19T15:30:00'
          }
        ]
      }
      get.mockResolvedValue(mockResponse)

      const result = await tongueApi.getTongueRecords('user-123')

      expect(get).toHaveBeenCalledWith('/api/v1/tongue/records/user-123')
      expect(result).toEqual(mockResponse)
    })

    it('应该返回空数组当用户没有记录时', async () => {
      const mockResponse = {
        code: 0,
        data: []
      }
      get.mockResolvedValue(mockResponse)

      const result = await tongueApi.getTongueRecords('new-user')

      expect(result.data).toEqual([])
    })
  })

  describe('getTongueOptions', () => {
    it('应该获取舌诊选项列表', async () => {
      const mockResponse = {
        code: 0,
        data: {
          tongue_colors: [
            { value: '淡白', label: '淡白', description: '舌色比正常浅' },
            { value: '淡红', label: '淡红', description: '正常舌色' },
            { value: '红', label: '红', description: '舌色比正常深' },
            { value: '绛', label: '绛', description: '舌色深红' },
            { value: '青紫', label: '青紫', description: '舌色青紫' }
          ],
          tongue_shapes: [
            { value: '正常', label: '正常', description: '舌体大小适中' },
            { value: '胖大', label: '胖大', description: '舌体比正常大' },
            { value: '瘦薄', label: '瘦薄', description: '舌体比正常小' },
            { value: '齿痕', label: '齿痕', description: '舌边有齿印' },
            { value: '裂纹', label: '裂纹', description: '舌面有裂纹' },
            { value: '芒刺', label: '芒刺', description: '舌面有红点' }
          ],
          coating_colors: [
            { value: '白', label: '白苔', description: '苔色白' },
            { value: '黄', label: '黄苔', description: '苔色黄' },
            { value: '灰黑', label: '灰黑苔', description: '苔色灰黑' }
          ],
          coating_thickness: [
            { value: '薄白', label: '薄白苔', description: '苔薄白' },
            { value: '白腻', label: '白腻苔', description: '苔白腻' },
            { value: '黄腻', label: '黄腻苔', description: '苔黄腻' },
            { value: '厚白', label: '厚白苔', description: '苔厚白' },
            { value: '厚黄', label: '厚黄苔', description: '苔厚黄' },
            { value: '少苔', label: '少苔', description: '苔少' },
            { value: '无苔', label: '无苔', description: '无苔' },
            { value: '剥苔', label: '剥苔', description: '舌苔剥落' }
          ]
        }
      }
      get.mockResolvedValue(mockResponse)

      const result = await tongueApi.getTongueOptions()

      expect(get).toHaveBeenCalledWith('/api/v1/tongue/options')
      expect(result).toEqual(mockResponse)
      expect(result.data.tongue_colors).toHaveLength(5)
      expect(result.data.tongue_shapes).toHaveLength(6)
      expect(result.data.coating_colors).toHaveLength(3)
      expect(result.data.coating_thickness).toHaveLength(8)
    })
  })

  describe('体质匹配', () => {
    it('应该正确识别气虚质舌象', async () => {
      const mockResponse = {
        code: 0,
        data: {
          constitution: 'qi_deficiency',
          scores: { qi_deficiency: 85 }
        }
      }
      post.mockResolvedValue(mockResponse)

      const result = await tongueApi.analyzeTongue({
        tongue_color: '淡白',
        tongue_shape: '胖大有齿痕',
        coating_color: '白',
        coating_thickness: '薄白'
      })

      expect(result.data.constitution).toBe('qi_deficiency')
    })

    it('应该正确识别阴虚质舌象', async () => {
      const mockResponse = {
        code: 0,
        data: {
          constitution: 'yin_deficiency',
          scores: { yin_deficiency: 80 }
        }
      }
      post.mockResolvedValue(mockResponse)

      const result = await tongueApi.analyzeTongue({
        tongue_color: '红',
        tongue_shape: '瘦薄',
        coating_color: '黄',
        coating_thickness: '少苔'
      })

      expect(result.data.constitution).toBe('yin_deficiency')
    })

    it('应该正确识别阳虚质舌象', async () => {
      const mockResponse = {
        code: 0,
        data: {
          constitution: 'yang_deficiency',
          scores: { yang_deficiency: 85 }
        }
      }
      post.mockResolvedValue(mockResponse)

      const result = await tongueApi.analyzeTongue({
        tongue_color: '淡白',
        tongue_shape: '胖大',
        coating_color: '白',
        coating_thickness: '白腻'
      })

      expect(result.data.constitution).toBe('yang_deficiency')
    })

    it('应该正确识别平和质舌象', async () => {
      const mockResponse = {
        code: 0,
        data: {
          constitution: 'peace',
          scores: { peace: 75 }
        }
      }
      post.mockResolvedValue(mockResponse)

      const result = await tongueApi.analyzeTongue({
        tongue_color: '淡红',
        tongue_shape: '正常',
        coating_color: '白',
        coating_thickness: '薄白'
      })

      expect(result.data.constitution).toBe('peace')
    })
  })

  describe('错误处理', () => {
    it('应该处理参数缺失', async () => {
      post.mockRejectedValue({
        code: -1,
        message: '缺少必要参数'
      })

      await expect(tongueApi.analyzeTongue({})).rejects.toEqual({
        code: -1,
        message: '缺少必要参数'
      })
    })

    it('应该处理网络错误', async () => {
      post.mockRejectedValue(new Error('Network error'))

      await expect(tongueApi.analyzeTongue({
        tongue_color: '淡白',
        tongue_shape: '胖大',
        coating_color: '白',
        coating_thickness: '薄白'
      })).rejects.toThrow('Network error')
    })

    it('应该处理无效的体质对比', async () => {
      post.mockRejectedValue({
        code: -1,
        message: '未找到对应的问卷结果'
      })

      await expect(tongueApi.analyzeTongue({
        tongue_color: '淡红',
        tongue_shape: '正常',
        coating_color: '白',
        coating_thickness: '薄白',
        result_id: 'invalid-result-id'
      })).rejects.toEqual({
        code: -1,
        message: '未找到对应的问卷结果'
      })
    })
  })
})
