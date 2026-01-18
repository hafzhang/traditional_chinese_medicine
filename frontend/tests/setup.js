/**
 * Vitest Test Setup
 */

import { vi } from 'vitest'

// Mock uni-app API
global.uni = {
  request: vi.fn(() => Promise.resolve({
    statusCode: 200,
    data: { code: 0, data: {} }
  })),
  navigateTo: vi.fn(),
  redirectTo: vi.fn(),
  switchTab: vi.fn(),
  showToast: vi.fn(),
  hideToast: vi.fn(),
  showLoading: vi.fn(),
  hideLoading: vi.fn(),
  getStorageSync: vi.fn(() => null),
  setStorageSync: vi.fn(),
  removeStorageSync: vi.fn(),
  getSystemInfoSync: vi.fn(() => ({
    platform: 'devtools',
    system: 'Windows 10'
  }))
}

// Mock page lifecycle hooks
global.onLoad = (callback) => {
  callback({})
}

global.onShow = (callback) => {
  callback()
}

global.onReady = (callback) => {
  callback()
}

// Mock console methods to avoid noise
global.console = {
  log: vi.fn(),
  warn: vi.fn(),
  error: vi.fn(),
  info: vi.fn()
}
