/**
 * 体质测试组件单元测试
 * Unit Tests for Constitution Test Component
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import ConstitutionTest from '@/pages/test/test.vue'

// Mock uni API
global.uni = {
  request: vi.fn(),
  showToast: vi.fn(),
  setStorageSync: vi.fn(),
  redirectTo: vi.fn()
}

describe('ConstitutionTest', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(ConstitutionTest, {
      global: {
        mocks: {
          uni
        }
      }
    })
  })

  it('组件应该正确渲染', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('应该初始化问题列表', () => {
    expect(wrapper.vm.currentQuestionIndex).toBe(0)
    expect(wrapper.vm.answers.length).toBe(30)
  })

  it('应该支持选择答案', () => {
    wrapper.vm.selectOption(3)
    expect(wrapper.vm.answers[0]).toBe(3)
  })

  it('应该正确跳转到下一题', () => {
    // 先选择一个答案
    wrapper.vm.selectOption(2)
    expect(wrapper.vm.answers[0]).toBe(2)

    const initialIndex = wrapper.vm.currentQuestionIndex
    wrapper.vm.nextQuestion()
    expect(wrapper.vm.currentQuestionIndex).toBe(initialIndex + 1)
  })

  it('应该支持跳转到上一题', () => {
    // 先选择答案并跳到下一题
    wrapper.vm.selectOption(2)
    wrapper.vm.nextQuestion()
    expect(wrapper.vm.currentQuestionIndex).toBe(1)

    // 跳回上一题
    wrapper.vm.prevQuestion()
    expect(wrapper.vm.currentQuestionIndex).toBe(0)
  })

  it('应该支持跳转到指定题目', () => {
    wrapper.vm.jumpToQuestion(5)
    expect(wrapper.vm.currentQuestionIndex).toBe(5)
  })

  it('进度计算应该正确', () => {
    wrapper.vm.jumpToQuestion(0)
    expect(wrapper.vm.progress).toBeCloseTo(3.33, 1)

    wrapper.vm.jumpToQuestion(14)
    expect(wrapper.vm.progress).toBe(50)

    wrapper.vm.jumpToQuestion(29)
    expect(wrapper.vm.progress).toBe(100)
  })
})
