/**
 * 食谱组件单元测试
 * Unit Tests for Recipes Component
 */

import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import RecipesList from '@/pages/recipes/list.vue'

describe('RecipesList', () => {
  it('组件应该正确渲染', () => {
    const wrapper = mount(RecipesList, {
      global: {
        mocks: {
          uni: {
            request: vi.fn()
          }
        }
      }
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('应该显示食谱列表', async () => {
    const wrapper = mount(RecipesList, {
      data() {
        return {
          recipes: [
            { id: '1', name: '山药莲子粥', type: '粥类' }
          ]
        }
      }
    })
    expect(wrapper.vm.recipes.length).toBe(1)
  })

  it('应该支持按体质筛选', () => {
    const wrapper = mount(RecipesList)
    wrapper.vm.filterByConstitution('qi_deficiency')
    expect(wrapper.vm.selectedConstitution).toBe('qi_deficiency')
  })
})
