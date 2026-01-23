/**
 * 养生课程 API 单元测试
 * Unit Tests for Courses API
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import * as coursesApi from '@/api/courses.js'

// Mock request module
vi.mock('@/utils/request.js', () => ({
  get: vi.fn(),
  post: vi.fn()
}))

import { get } from '@/utils/request.js'

describe('Courses API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('getCoursesList', () => {
    it('应该获取课程列表', async () => {
      const mockResponse = {
        code: 0,
        data: {
          items: [
            {
              id: 'course-001',
              title: '气虚体质调理指南',
              category: '体质调理',
              content_type: '视频',
              duration: 1200,
              is_free: true
            }
          ],
          total: 1
        }
      }
      get.mockResolvedValue(mockResponse)

      const result = await coursesApi.getCoursesList({ skip: 0, limit: 10 })

      expect(get).toHaveBeenCalledWith('/api/v1/courses', { skip: 0, limit: 10 })
      expect(result).toEqual(mockResponse)
    })

    it('应该支持按分类筛选', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await coursesApi.getCoursesList({ category: '体质调理' })

      expect(get).toHaveBeenCalledWith('/api/v1/courses', { category: '体质调理' })
    })

    it('应该支持按内容类型筛选', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await coursesApi.getCoursesList({ content_type: '视频' })

      expect(get).toHaveBeenCalledWith('/api/v1/courses', { content_type: '视频' })
    })

    it('应该支持按体质筛选', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await coursesApi.getCoursesList({ constitution: 'qi_deficiency' })

      expect(get).toHaveBeenCalledWith('/api/v1/courses', { constitution: 'qi_deficiency' })
    })

    it('应该支持搜索功能', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await coursesApi.getCoursesList({ search: '八段锦' })

      expect(get).toHaveBeenCalledWith('/api/v1/courses', { search: '八段锦' })
    })

    it('应该支持分页参数', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await coursesApi.getCoursesList({ skip: 20, limit: 20 })

      expect(get).toHaveBeenCalledWith('/api/v1/courses', { skip: 20, limit: 20 })
    })

    it('应该支持组合筛选条件', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await coursesApi.getCoursesList({
        category: '运动养生',
        content_type: '视频',
        constitution: 'qi_deficiency',
        search: '气功'
      })

      expect(get).toHaveBeenCalledWith('/api/v1/courses', {
        category: '运动养生',
        content_type: '视频',
        constitution: 'qi_deficiency',
        search: '气功'
      })
    })

    it('默认参数应该为空对象', async () => {
      const mockResponse = { code: 0, data: { items: [], total: 0 } }
      get.mockResolvedValue(mockResponse)

      await coursesApi.getCoursesList()

      expect(get).toHaveBeenCalledWith('/api/v1/courses', {})
    })
  })

  describe('getCourseDetail', () => {
    it('应该获取课程详情', async () => {
      const mockResponse = {
        code: 0,
        data: {
          id: 'course-001',
          title: '八段锦教学',
          description: '传统养生功法',
          category: '运动养生',
          content_type: '视频',
          duration: 1800,
          video_url: 'https://example.com/video.mp4',
          is_free: true,
          suitable_constitutions: ['qi_deficiency', 'peace'],
          instructor: '张医生',
          created_at: '2026-01-20T10:00:00'
        }
      }
      get.mockResolvedValue(mockResponse)

      const result = await coursesApi.getCourseDetail('course-001')

      expect(get).toHaveBeenCalledWith('/api/v1/courses/course-001')
      expect(result).toEqual(mockResponse)
    })
  })

  describe('getCourseRecommendation', () => {
    it('应该根据体质获取推荐课程', async () => {
      const mockResponse = {
        code: 0,
        data: {
          constitution: 'qi_deficiency',
          constitution_name: '气虚质',
          recommended: [
            {
              id: 'course-001',
              title: '气虚体质调理指南',
              category: '体质调理',
              reason: '专门针对气虚体质设计的养生课程'
            },
            {
              id: 'course-002',
              title: '八段锦教学',
              category: '运动养生',
              reason: '温和运动，适合气虚体质练习'
            }
          ]
        }
      }
      get.mockResolvedValue(mockResponse)

      const result = await coursesApi.getCourseRecommendation('qi_deficiency')

      expect(get).toHaveBeenCalledWith('/api/v1/courses/recommend/qi_deficiency')
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

      await coursesApi.getCourseRecommendation('peace')

      expect(get).toHaveBeenCalledWith('/api/v1/courses/recommend/peace')
    })

    it('应该为不同体质返回不同推荐', async () => {
      const constitutions = [
        'qi_deficiency',
        'yang_deficiency',
        'yin_deficiency',
        'phlegm_damp',
        'damp_heat'
      ]

      for (const constitution of constitutions) {
        get.mockResolvedValue({
          code: 0,
          data: { constitution, recommended: [] }
        })

        await coursesApi.getCourseRecommendation(constitution)

        expect(get).toHaveBeenCalledWith(`/api/v1/courses/recommend/${constitution}`)
      }
    })
  })

  describe('getSeasonCourses', () => {
    it('应该根据季节获取养生课程', async () => {
      const mockResponse = {
        code: 0,
        data: [
          {
            id: 'course-001',
            title: '春季养生指南',
            category: '季节养生',
            season: 'spring',
            description: '春季养肝护肝'
          }
        ]
      }
      get.mockResolvedValue(mockResponse)

      const result = await coursesApi.getSeasonCourses('spring')

      expect(get).toHaveBeenCalledWith('/api/v1/courses/season/spring')
      expect(result).toEqual(mockResponse)
    })

    it('应该支持所有四季', async () => {
      const seasons = ['spring', 'summer', 'autumn', 'winter']

      for (const season of seasons) {
        get.mockResolvedValue({ code: 0, data: [] })

        await coursesApi.getSeasonCourses(season)

        expect(get).toHaveBeenCalledWith(`/api/v1/courses/season/${season}`)
      }
    })

    it('春季应该推荐养肝课程', async () => {
      const mockResponse = {
        code: 0,
        data: [
          { title: '春季养肝指南', season: 'spring' },
          { title: '春季食疗', season: 'spring' }
        ]
      }
      get.mockResolvedValue(mockResponse)

      const result = await coursesApi.getSeasonCourses('spring')

      expect(result.data.every(course => course.season === 'spring')).toBe(true)
    })

    it('夏季应该推荐养心课程', async () => {
      const mockResponse = {
        code: 0,
        data: [
          { title: '夏季养心指南', season: 'summer' }
        ]
      }
      get.mockResolvedValue(mockResponse)

      const result = await coursesApi.getSeasonCourses('summer')

      expect(result.data.every(course => course.season === 'summer')).toBe(true)
    })
  })

  describe('getCourseCategories', () => {
    it('应该获取课程分类列表', async () => {
      const mockResponse = {
        code: 0,
        data: [
          '体质调理',
          '运动养生',
          '饮食养生',
          '情志养生',
          '季节养生',
          '经络养生',
          '起居养生'
        ]
      }
      get.mockResolvedValue(mockResponse)

      const result = await coursesApi.getCourseCategories()

      expect(get).toHaveBeenCalledWith('/api/v1/courses/categories/list')
      expect(result).toEqual(mockResponse)
      expect(result.data).toContain('体质调理')
      expect(result.data).toContain('运动养生')
    })
  })

  describe('getSeasons', () => {
    it('应该获取季节列表', async () => {
      const mockResponse = {
        code: 0,
        data: [
          { value: 'spring', label: '春季' },
          { value: 'summer', label: '夏季' },
          { value: 'autumn', label: '秋季' },
          { value: 'winter', label: '冬季' }
        ]
      }
      get.mockResolvedValue(mockResponse)

      const result = await coursesApi.getSeasons()

      expect(get).toHaveBeenCalledWith('/api/v1/courses/seasons/list')
      expect(result).toEqual(mockResponse)
      expect(result.data).toHaveLength(4)
    })
  })

  describe('免费课程', () => {
    it('应该标记免费课程', async () => {
      const mockResponse = {
        code: 0,
        data: {
          items: [
            { id: 'course-001', title: '免费课程', is_free: true },
            { id: 'course-002', title: '付费课程', is_free: false }
          ],
          total: 2
        }
      }
      get.mockResolvedValue(mockResponse)

      const result = await coursesApi.getCoursesList()

      expect(result.data.items.filter(c => c.is_free)).toHaveLength(1)
      expect(result.data.items.filter(c => c.is_free)[0].title).toBe('免费课程')
    })
  })

  describe('内容类型', () => {
    it('应该支持不同内容类型', async () => {
      const mockResponse = {
        code: 0,
        data: {
          items: [
            { id: 'course-001', content_type: '视频' },
            { id: 'course-002', content_type: '音频' },
            { id: 'course-003', content_type: '图文' }
          ],
          total: 3
        }
      }
      get.mockResolvedValue(mockResponse)

      const result = await coursesApi.getCoursesList()

      expect(result.data.items).toHaveLength(3)
      expect(result.data.items[0].content_type).toBe('视频')
      expect(result.data.items[1].content_type).toBe('音频')
      expect(result.data.items[2].content_type).toBe('图文')
    })
  })

  describe('错误处理', () => {
    it('应该处理网络错误', async () => {
      get.mockRejectedValue(new Error('Network error'))

      await expect(coursesApi.getCoursesList()).rejects.toThrow('Network error')
    })

    it('应该处理 API 错误响应', async () => {
      get.mockRejectedValue({
        code: -1,
        message: '参数错误'
      })

      await expect(coursesApi.getCoursesList()).rejects.toEqual({
        code: -1,
        message: '参数错误'
      })
    })

    it('应该处理无效的季节参数', async () => {
      get.mockRejectedValue({
        code: -1,
        message: '无效的季节参数'
      })

      await expect(coursesApi.getSeasonCourses('invalid_season')).rejects.toEqual({
        code: -1,
        message: '无效的季节参数'
      })
    })

    it('应该处理不存在的课程ID', async () => {
      get.mockRejectedValue({
        code: -1,
        message: '课程不存在'
      })

      await expect(coursesApi.getCourseDetail('non-existent-id')).rejects.toEqual({
        code: -1,
        message: '课程不存在'
      })
    })
  })
})
