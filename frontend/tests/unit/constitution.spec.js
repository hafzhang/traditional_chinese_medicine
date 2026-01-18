/**
 * 体质测试组件单元测试
 * Unit Tests for Constitution Test Component
 */

import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import ConstitutionTest from '@/pages/test/test.vue'

describe('ConstitutionTest', () => {
  it('组件应该正确渲染', () => {
    const wrapper = mount(ConstitutionTest, {
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

  it('应该初始化问题列表', () => {
    const wrapper = mount(ConstitutionTest)
    expect(wrapper.vm.currentQuestionIndex).toBe(0)
  })

  it('应该支持选择答案', () => {
    const wrapper = mount(ConstitutionTest)
    wrapper.vm.selectAnswer(1)
    expect(wrapper.vm.answers[wrapper.vm.currentQuestionIndex]).toBe(1)
  })

  it('应该计算正确跳转到下一题', () => {
    const wrapper = mount(ConstitutionTest)
    const initialIndex = wrapper.vm.currentQuestionIndex
    wrapper.vm.nextQuestion()
    expect(wrapper.vm.currentQuestionIndex).toBe(initialIndex + 1)
  })
})
