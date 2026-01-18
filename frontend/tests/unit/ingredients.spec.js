/**
 * 食材列表组件单元测试
 * Unit Tests for Ingredients List Component
 */

import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import IngredientsList from '@/pages/ingredients/ingredients.vue'

describe('IngredientsList', () => {
  it('组件应该正确渲染', () => {
    const wrapper = mount(IngredientsList, {
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

  it('应该显示加载状态', () => {
    const wrapper = mount(IngredientsList, {
      data() {
        return {
          loading: true
        }
      }
    })
    expect(wrapper.vm.loading).toBe(true)
  })

  it('应该正确设置筛选器', () => {
    const wrapper = mount(IngredientsList)
    wrapper.vm.setFilter('nature', '平')
    expect(wrapper.vm.filters.nature).toBe('平')
  })
})
