# 前端测试规范

## 目录

1. [测试框架配置](#测试框架配置)
2. [测试结构](#测试结构)
3. [单元测试](#单元测试)
4. [组件测试](#组件测试)
5. [API Mock](#api-mock)
6. [E2E 测试](#e2e-测试)
7. [Phase 1 测试案例](#phase-1-测试案例)
8. [uni-app 特殊考虑](#uni-app-特殊考虑)
9. [最佳实践](#最佳实践)

---

## 测试框架配置

### 推荐测试框架

| 框架 | 用途 | 说明 |
|------|------|------|
| **Vitest** | 单元测试 | 快速、原生 ESM 支持 |
| **Vue Test Utils** | 组件测试 | Vue 官方测试工具 |
| **MSW** | API Mock | API 请求拦截 |
| **Playwright** | E2E 测试 | 跨浏览器 E2E 测试 |

### 安装依赖

```bash
cd frontend

# Vitest 和 Vue Test Utils
npm install -D vitest @vue/test-utils

# jsdom 环境
npm install -D happy-dom

# 覆盖率
npm install -D @vitest/coverage-v8

# MSW API Mock
npm install -D msw

# Playwright E2E (可选)
npm install -D @playwright/test
```

### Vitest 配置

创建 `frontend/vitest.config.js`:

```javascript
import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'happy-dom',
    setupFiles: ['./tests/setup.js'],
    include: ['src/**/*.{test,spec}.{js,ts}', 'tests/**/*.{test,spec}.{js,ts}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.test.{js,ts}',
        '**/*.spec.{js,ts}',
        'src/main.js',
      ]
    },
    testTimeout: 10000,
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
```

### 测试环境设置

创建 `frontend/tests/setup.js`:

```javascript
import { vi } from 'vitest'

// Mock uni-app API
global.uni = {
  request: vi.fn(),
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
    system: 'iOS 13.0',
    model: 'iPhone 11'
  }))
}

// Mock 响应
global.wx = global.uni
```

---

## 测试结构

```
frontend/
├── src/
│   ├── pages/                    # 页面组件
│   │   ├── index/
│   │   ├── test/
│   │   ├── result/
│   │   ├── ingredients/
│   │   ├── recipes/
│   │   ├── acupoints/
│   │   ├── courses/
│   │   └── tongue/
│   ├── api/                      # API 客户端
│   │   ├── index.js
│   │   ├── ingredients.js
│   │   ├── recipes.js
│   │   ├── acupoints.js
│   │   ├── tongue.js
│   │   └── courses.js
│   └── utils/                    # 工具函数
│       ├── constitution.js
│       └── format.js
├── tests/
│   ├── setup.js                  # 测试环境设置
│   ├── unit/                     # 单元测试
│   │   ├── constitution.test.js
│   │   ├── format.test.js
│   │   └── api/
│   │       ├── ingredients.test.js
│   │       ├── recipes.test.js
│   │       └── acupoints.test.js
│   ├── component/                # 组件测试
│   │   ├── IngredientCard.test.js
│   │   ├── RecipeCard.test.js
│   │   └── ConstitutionBadge.test.js
│   └── e2e/                      # E2E 测试
│       ├── constitution.spec.js
│       └── ingredients.spec.js
└── vitest.config.js              # Vitest 配置
```

---

## 单元测试

### 工具函数测试

```javascript
// tests/unit/constitution.test.js
import { describe, it, expect } from 'vitest'
import { calculateScores, determineConstitution } from '@/utils/constitution'

describe('体质评分工具', () => {
  describe('calculateScores', () => {
    it('应该正确计算各体质原始分数', () => {
      const answers = Array(30).fill(3)
      const scores = calculateScores(answers)

      expect(scores.peace).toBe(12)
      expect(scores.qi_deficiency).toBe(12)
      expect(scores.special).toBe(6)
    })

    it('应该处理答案数量不正确的情况', () => {
      expect(() => {
        calculateScores([1, 2, 3])
      }).toThrow('Expected 30 answers')
    })

    it('应该验证答案范围', () => {
      expect(() => {
        calculateScores([0, ...Array(29).fill(3)])
      }).toThrow('between 1 and 5')
    })
  })

  describe('determineConstitution', () => {
    it('应该正确判定平和质', () => {
      const scores = {
        peace: 70,
        qi_deficiency: 30,
        yang_deficiency: 25,
        yin_deficiency: 20,
        phlegm_damp: 20,
        damp_heat: 20,
        blood_stasis: 20,
        qi_depression: 20,
        special: 15
      }

      const result = determineConstitution(scores)

      expect(result.primary_constitution).toBe('peace')
      expect(result.secondary_constitutions).toHaveLength(0)
    })

    it('应该正确判定气虚质', () => {
      const scores = {
        peace: 30,
        qi_deficiency: 50,
        yang_deficiency: 35,
        yin_deficiency: 25,
        phlegm_damp: 20,
        damp_heat: 20,
        blood_stasis: 20,
        qi_depression: 20,
        special: 15
      }

      const result = determineConstitution(scores)

      expect(result.primary_constitution).toBe('qi_deficiency')
    })

    it('应该正确识别次要体质', () => {
      const scores = {
        peace: 30,
        qi_deficiency: 50,
        yang_deficiency: 40,
        yin_deficiency: 35,
        phlegm_damp: 32,
        damp_heat: 20,
        blood_stasis: 20,
        qi_depression: 20,
        special: 15
      }

      const result = determineConstitution(scores)

      expect(result.secondary_constitutions.length).toBeGreaterThan(0)
      expect(result.secondary_constitutions[0].type).toBe('yang_deficiency')
    })
  })
})
```

### 格式化函数测试

```javascript
// tests/unit/format.test.js
import { describe, it, expect } from 'vitest'
import { formatConstitutionName, formatScore } from '@/utils/format'

describe('格式化工具', () => {
  describe('formatConstitutionName', () => {
    it('应该正确转换体质代码', () => {
      expect(formatConstitutionName('qi_deficiency')).toBe('气虚质')
      expect(formatConstitutionName('yang_deficiency')).toBe('阳虚质')
      expect(formatConstitutionName('peace')).toBe('平和质')
    })

    it('应该处理未知代码', () => {
      expect(formatConstitutionName('unknown')).toBe('unknown')
    })
  })

  describe('formatScore', () => {
    it('应该正确格式化分数', () => {
      expect(formatScore(50.5)).toBe('50.50')
      expect(formatScore(100)).toBe('100.00')
    })

    it('应该处理整数', () => {
      expect(formatScore(50)).toBe('50.00')
    })
  })
})
```

---

## 组件测试

### 基础组件测试

```javascript
// tests/component/IngredientCard.test.js
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import IngredientCard from '@/components/IngredientCard.vue'

describe('IngredientCard 组件', () => {
  const mockIngredient = {
    id: 'test-id',
    name: '山药',
    category: '药材',
    nature: '平',
    flavor: '甘',
    efficacy: '健脾养胃、补肺益肾',
    image_url: 'https://example.com/yam.jpg'
  }

  it('应该渲染食材名称', () => {
    const wrapper = mount(IngredientCard, {
      props: { ingredient: mockIngredient }
    })

    expect(wrapper.text()).toContain('山药')
  })

  it('应该渲染食材类别', () => {
    const wrapper = mount(IngredientCard, {
      props: { ingredient: mockIngredient }
    })

    expect(wrapper.text()).toContain('药材')
  })

  it('应该渲染性味', () => {
    const wrapper = mount(IngredientCard, {
      props: { ingredient: mockIngredient }
    })

    expect(wrapper.text()).toContain('平')
    expect(wrapper.text()).toContain('甘')
  })

  it('应该处理空 props', () => {
    const wrapper = mount(IngredientCard, {
      props: { ingredient: null }
    })

    expect(wrapper.text()).toContain('暂无数据')
  })

  it('应该触发点击事件', async () => {
    const wrapper = mount(IngredientCard, {
      props: { ingredient: mockIngredient }
    })

    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
    expect(wrapper.emitted('click')[0]).toEqual([mockIngredient])
  })
})
```

### 带状态组件测试

```javascript
// tests/component/ConstitutionBadge.test.js
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ConstitutionBadge from '@/components/ConstitutionBadge.vue'

describe('ConstitutionBadge 组件', () => {
  it('应该显示正确的体质颜色', () => {
    const wrapper = mount(ConstitutionBadge, {
      props: { constitution: 'qi_deficiency' }
    })

    const badge = wrapper.find('.badge')
    expect(badge.classes()).toContain('qi-deficiency')
  })

  it('应该显示体质名称', () => {
    const wrapper = mount(ConstitutionBadge, {
      props: { constitution: 'qi_deficiency' }
    })

    expect(wrapper.text()).toBe('气虚质')
  })

  it('应该支持自定义样式', () => {
    const wrapper = mount(ConstitutionBadge, {
      props: {
        constitution: 'qi_deficiency',
        size: 'large'
      }
    })

    const badge = wrapper.find('.badge')
    expect(badge.classes()).toContain('large')
  })
})
```

### 列表组件测试

```javascript
// tests/component/IngredientList.test.js
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import IngredientList from '@/components/IngredientList.vue'

describe('IngredientList 组件', () => {
  const mockIngredients = [
    { id: '1', name: '山药', category: '药材', nature: '平' },
    { id: '2', name: '红枣', category: '药材', nature: '温' }
  ]

  it('应该渲染食材列表', () => {
    const wrapper = mount(IngredientList, {
      props: { items: mockIngredients }
    })

    const items = wrapper.findAll('.ingredient-item')
    expect(items).toHaveLength(2)
  })

  it('应该处理空列表', () => {
    const wrapper = mount(IngredientList, {
      props: { items: [] }
    })

    expect(wrapper.text()).toContain('暂无食材')
  })

  it('应该触发加载更多事件', async () => {
    const onLoadMore = vi.fn()
    const wrapper = mount(IngredientList, {
      props: {
        items: mockIngredients,
        onLoadMore
      }
    })

    await wrapper.find('.load-more').trigger('click')
    expect(onLoadMore).toHaveBeenCalled()
  })

  it('应该支持刷新功能', async () => {
    const onRefresh = vi.fn()
    const wrapper = mount(IngredientList, {
      props: {
        items: mockIngredients,
        onRefresh
      }
    })

    await wrapper.find('.refresh').trigger('click')
    expect(onRefresh).toHaveBeenCalled()
  })
})
```

---

## API Mock

### MSW 配置

创建 `frontend/tests/mocks/handlers.js`:

```javascript
import { http, HttpResponse } from 'msw'

export const handlers = [
  // 食材 API
  http.get('/api/ingredients', () => {
    return HttpResponse.json({
      code: 0,
      message: 'success',
      data: {
        total: 2,
        items: [
          {
            id: '1',
            name: '山药',
            category: '药材',
            nature: '平',
            flavor: '甘'
          },
          {
            id: '2',
            name: '红枣',
            category: '药材',
            nature: '温',
            flavor: '甘'
          }
        ]
      }
    })
  }),

  http.get('/api/ingredients/:id', ({ params }) => {
    if (params.id === 'not-found') {
      return HttpResponse.json(
        { code: -1, message: 'Ingredient not found' },
        { status: 404 }
      )
    }

    return HttpResponse.json({
      code: 0,
      message: 'success',
      data: {
        id: params.id,
        name: '山药',
        category: '药材',
        nature: '平'
      }
    })
  }),

  http.get('/api/ingredients/recommend/:constitution', ({ params }) => {
    return HttpResponse.json({
      code: 0,
      message: 'success',
      data: {
        constitution: params.constitution,
        constitution_name: '气虚质',
        recommended: [
          {
            id: '1',
            name: '黄芪',
            category: '药材',
            nature: '温',
            reason: '补气健脾，增强体质'
          }
        ],
        avoided: []
      }
    })
  }),

  // 食谱 API
  http.get('/api/recipes', () => {
    return HttpResponse.json({
      code: 0,
      message: 'success',
      data: {
        total: 1,
        items: [
          {
            id: '1',
            name: '山药红枣粥',
            type: '粥类',
            difficulty: '简单',
            cook_time: 30
          }
        ]
      }
    })
  }),

  // 穴位 API
  http.get('/api/acupoints/symptom/:symptom', ({ params }) => {
    return HttpResponse.json({
      code: 0,
      message: 'success',
      data: {
        symptom: params.symptom,
        items: [
          {
            id: '1',
            name: '神门',
            code: 'HT7',
            simple_location: '腕横纹尺侧端',
            efficacy: ['宁心安神'],
            priority: 10
          }
        ]
      }
    })
  }),

  // 舌诊 API
  http.post('/api/tongue/analyze', async ({ request }) => {
    const body = await request.json()

    return HttpResponse.json({
      code: 0,
      message: 'success',
      data: {
        record_id: 'test-record-id',
        analysis: {
          constitution_tendency: 'qi_deficiency',
          constitution_name: '气虚质',
          confidence: 85,
          tongue_features: body
        }
      }
    })
  }),

  // 课程 API
  http.get('/api/courses/recommend/:constitution', ({ params }) => {
    return HttpResponse.json({
      code: 0,
      message: 'success',
      data: {
        constitution: params.constitution,
        constitution_name: '气虚质',
        items: [
          {
            id: '1',
            title: '气虚质调理指南',
            content_type: 'video',
            duration: 480
          }
        ]
      }
    })
  })
]
```

### MSW 设置

创建 `frontend/tests/mocks/server.js`:

```javascript
import { setupServer } from 'msw/node'
import { handlers } from './handlers'

export const server = setupServer(...handlers)
```

在 `tests/setup.js` 中集成:

```javascript
import { vi } from 'vitest'
import { server } from './mocks/server'

// Vitest setup
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterAll(() => server.close())
afterEach(() => server.resetHandlers())

// ... 其他设置
```

### API 测试使用 Mock

```javascript
// tests/unit/api/ingredients.test.js
import { describe, it, expect } from 'vitest'
import { getIngredients, getIngredientById, getIngredientRecommendation } from '@/api/ingredients'

describe('食材 API', () => {
  describe('getIngredients', () => {
    it('应该获取食材列表', async () => {
      const result = await getIngredients({ skip: 0, limit: 20 })

      expect(result.code).toBe(0)
      expect(result.data.total).toBe(2)
      expect(result.data.items).toHaveLength(2)
    })

    it('应该支持筛选参数', async () => {
      const result = await getIngredients({ category: '药材' })

      expect(result.code).toBe(0)
      expect(result.data.items.every(item => item.category === '药材')).toBe(true)
    })
  })

  describe('getIngredientById', () => {
    it('应该获取食材详情', async () => {
      const result = await getIngredientById('1')

      expect(result.code).toBe(0)
      expect(result.data.name).toBe('山药')
    })

    it('应该处理 404 错误', async () => {
      await expect(getIngredientById('not-found')).rejects.toThrow()
    })
  })

  describe('getIngredientRecommendation', () => {
    it('应该获取推荐食材', async () => {
      const result = await getIngredientRecommendation('qi_deficiency')

      expect(result.code).toBe(0)
      expect(result.data.constitution).toBe('qi_deficiency')
      expect(result.data.recommended).toBeDefined()
      expect(result.data.avoided).toBeDefined()
    })
  })
})
```

---

## E2E 测试

### Playwright 配置

创建 `frontend/playwright.config.js`:

```javascript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
})
```

### E2E 测试示例

```javascript
// tests/e2e/constitution.spec.js
import { test, expect } from '@playwright/test'

test.describe('体质测试流程', () => {
  test('应该完成完整的体质测试', async ({ page }) => {
    // 导航到测试页面
    await page.goto('/pages/test/test')

    // 填写问卷
    for (let i = 1; i <= 30; i++) {
      const option = page.locator(`.question[data-number="${i}"] .option[value="3"]`)
      await option.click()
    }

    // 提交测试
    await page.click('.submit-button')

    // 等待结果页面
    await page.waitForURL('/pages/result/result')

    // 验证结果显示
    await expect(page.locator('.primary-constitution')).toBeVisible()
    await expect(page.locator('.score-breakdown')).toBeVisible()
  })

  test('应该显示正确的体质结果', async ({ page }) => {
    await page.goto('/pages/test/test')

    // 选择特定答案（气虚质）
    const qiDeficiencyAnswers = [
      3, 3, 3, 3,  // 平和质
      5, 5, 5, 5,  // 气虚质 - 明显症状
      3, 3, 3, 3,  // 阳虚质
      3, 3, 3, 3,  // 阴虚质
      3, 3, 3,     // 痰湿质
      3, 3, 3,     // 湿热质
      3, 3, 3,     // 血瘀质
      3, 3, 3,     // 气郁质
      3, 3         // 特禀质
    ]

    for (let i = 0; i < qiDeficiencyAnswers.length; i++) {
      const option = page.locator(`.question[data-number="${i + 1}"] .option[value="${qiDeficiencyAnswers[i]}"]`)
      await option.click()
    }

    await page.click('.submit-button')
    await page.waitForURL('/pages/result/result')

    // 验证气虚质判定
    await expect(page.locator('.primary-constitution')).toContainText('气虚质')
  })
})
```

### 食材页面 E2E 测试

```javascript
// tests/e2e/ingredients.spec.js
import { test, expect } from '@playwright/test'

test.describe('食材页面', () => {
  test('应该显示食材列表', async ({ page }) => {
    await page.goto('/pages/ingredients/ingredients')

    // 等待列表加载
    await expect(page.locator('.ingredient-list')).toBeVisible()

    // 验证食材显示
    const items = page.locator('.ingredient-item')
    await expect(items.first()).toBeVisible()
  })

  test('应该支持点击查看详情', async ({ page }) => {
    await page.goto('/pages/ingredients/ingredients')

    // 点击第一个食材
    await page.locator('.ingredient-item').first().click()

    // 验证导航到详情页
    await page.waitForURL(/\/pages\/ingredients\/detail\/.+/)

    // 验证详情内容
    await expect(page.locator('.ingredient-name')).toBeVisible()
    await expect(page.locator('.ingredient-nature')).toBeVisible()
    await expect(page.locator('.ingredient-efficacy')).toBeVisible()
  })

  test('应该支持按体质筛选', async ({ page }) => {
    await page.goto('/pages/ingredients/ingredients')

    // 打开筛选器
    await page.click('.filter-button')

    // 选择体质
    await page.click('.constitution-filter[value="qi_deficiency"]')

    // 确认筛选
    await page.click('.confirm-filter')

    // 验证筛选结果
    const items = page.locator('.ingredient-item')
    await expect(items.first()).toBeVisible()
  })
})
```

---

## Phase 1 测试案例

### 食材模块测试

```javascript
// tests/unit/api/ingredients.test.js
describe('食材模块 API', () => {
  describe('获取食材列表', () => {
    it('应该返回分页数据', async () => {
      const result = await getIngredients({ skip: 0, limit: 10 })

      expect(result.data).toHaveProperty('total')
      expect(result.data).toHaveProperty('items')
      expect(result.data.items.length).toBeLessThanOrEqual(10)
    })

    it('应该支持按类别筛选', async () => {
      const result = await getIngredients({ category: '药材' })

      result.data.items.forEach(item => {
        expect(item.category).toBe('药材')
      })
    })

    it('应该支持按性味筛选', async () => {
      const result = await getIngredients({ nature: '温' })

      result.data.items.forEach(item => {
        expect(item.nature).toBe('温')
      })
    })
  })

  describe('获取食材详情', () => {
    it('应该返回完整的食材信息', async () => {
      const result = await getIngredientById('1')

      expect(result.data).toHaveProperty('name')
      expect(result.data).toHaveProperty('category')
      expect(result.data).toHaveProperty('nature')
      expect(result.data).toHaveProperty('flavor')
      expect(result.data).toHaveProperty('meridians')
      expect(result.data).toHaveProperty('efficacy')
    })
  })

  describe('获取推荐食材', () => {
    it('应该返回推荐和禁忌食材', async () => {
      const result = await getIngredientRecommendation('qi_deficiency')

      expect(result.data).toHaveProperty('recommended')
      expect(result.data).toHaveProperty('avoided')
      expect(Array.isArray(result.data.recommended)).toBe(true)
      expect(Array.isArray(result.data.avoided)).toBe(true)
    })

    it('应该包含推荐理由', async () => {
      const result = await getIngredientRecommendation('qi_deficiency')

      result.data.recommended.forEach(item => {
        expect(item).toHaveProperty('reason')
      })
    })
  })
})
```

### 食谱模块测试

```javascript
// tests/unit/api/recipes.test.js
describe('食谱模块 API', () => {
  describe('获取食谱列表', () => {
    it('应该支持按类型筛选', async () => {
      const result = await getRecipes({ type: '粥类' })

      result.data.items.forEach(item => {
        expect(item.type).toBe('粥类')
      })
    })

    it('应该支持按难度筛选', async () => {
      const result = await getRecipes({ difficulty: '简单' })

      result.data.items.forEach(item => {
        expect(item.difficulty).toBe('简单')
      })
    })
  })

  describe('获取三餐推荐', () => {
    it('应该返回早餐、午餐、晚餐推荐', async () => {
      const result = await getRecipeRecommendation('qi_deficiency')

      expect(result.data.recipes).toHaveProperty('breakfast')
      expect(result.data.recipes).toHaveProperty('lunch')
      expect(result.data.recipes).toHaveProperty('dinner')
    })

    it('每餐应该包含推荐理由', async () => {
      const result = await getRecipeRecommendation('qi_deficiency')

      Object.values(result.data.recipes).forEach(meals => {
        meals.forEach(recipe => {
          expect(recipe).toHaveProperty('reason')
        })
      })
    })
  })
})
```

### 穴位模块测试

```javascript
// tests/unit/api/acupoints.test.js
describe('穴位模块 API', () => {
  describe('按症状查找穴位', () => {
    it('应该返回相关穴位', async () => {
      const result = await getAcupointsBySymptom('失眠')

      expect(result.data.items).toBeInstanceOf(Array)
      expect(result.data.items.length).toBeGreaterThan(0)
    })

    it('应该按优先级排序', async () => {
      const result = await getAcupointsBySymptom('失眠')

      for (let i = 0; i < result.data.items.length - 1; i++) {
        const current = result.data.items[i]
        const next = result.data.items[i + 1]
        expect(current.priority).toBeGreaterThanOrEqual(next.priority)
      }
    })
  })

  describe('按体质推荐穴位', () => {
    it('应该返回适合的穴位', async () => {
      const result = await getAcupointsByConstitution('qi_deficiency')

      expect(result.data.items).toBeInstanceOf(Array)
      expect(result.data.items.length).toBeGreaterThan(0)
    })

    it('应该包含体质调理说明', async () => {
      const result = await getAcupointsByConstitution('qi_deficiency')

      result.data.items.forEach(item => {
        expect(item).toHaveProperty('constitution_benefit')
      })
    })
  })
})
```

### 舌诊模块测试

```javascript
// tests/unit/api/tongue.test.js
describe('舌诊模块 API', () => {
  describe('分析舌象', () => {
    it('应该返回体质倾向', async () => {
      const result = await analyzeTongue({
        tongue_color: '淡白',
        tongue_shape: '胖大',
        coating_color: '白苔',
        coating_thickness: '薄苔'
      })

      expect(result.data.analysis).toHaveProperty('constitution_tendency')
      expect(result.data.analysis).toHaveProperty('confidence')
    })

    it('应该返回舌象特征', async () => {
      const result = await analyzeTongue({
        tongue_color: '淡白',
        tongue_shape: '胖大',
        coating_color: '白苔',
        coating_thickness: '薄苔'
      })

      expect(result.data.analysis).toHaveProperty('tongue_features')
      expect(result.data.analysis.tongue_features).toEqual({
        tongue_color: '淡白',
        tongue_shape: '胖大',
        coating_color: '白苔',
        coating_thickness: '薄苔'
      })
    })
  })

  describe('与测试结果对比', () => {
    it('应该返回一致性分析', async () => {
      const result = await analyzeTongue(
        { tongue_color: '淡白', tongue_shape: '胖大', coating_color: '白苔', coating_thickness: '薄苔' },
        { result_id: 'test-result-id' }
      )

      expect(result.data).toHaveProperty('comparison')
      expect(result.data.comparison).toHaveProperty('is_consistent')
    })
  })
})
```

### 课程模块测试

```javascript
// tests/unit/api/courses.test.js
describe('课程模块 API', () => {
  describe('按体质获取课程', () => {
    it('应该返回相关课程', async () => {
      const result = await getCoursesByConstitution('qi_deficiency')

      expect(result.data.items).toBeInstanceOf(Array)
    })

    it('应该只返回该体质的课程', async () => {
      const result = await getCoursesByConstitution('qi_deficiency')

      result.data.items.forEach(course => {
        expect(course.suitable_constitutions).toContain('qi_deficiency')
      })
    })
  })

  describe('按季节获取课程', () => {
    it('应该返回季节课程', async () => {
      const result = await getCoursesBySeason('spring')

      expect(result.data.season).toBe('spring')
      expect(result.data.items).toBeInstanceOf(Array)
    })
  })
})
```

---

## uni-app 特殊考虑

### uni-app API Mock

由于 uni-app 的特殊 API，需要创建专门的 mock:

```javascript
// tests/mocks/uni-api.js
export const mockUniAPI = {
  // 页面导航
  navigateTo: vi.fn(({ url }) => {
    // 模拟导航
    return { errMsg: 'navigateTo:ok' }
  }),

  // 网络请求
  request: vi.fn(({ url, method, data }) => {
    return new Promise((resolve) => {
      resolve({
        data: { success: true },
        statusCode: 200,
        header: {}
      })
    })
  }),

  // 本地存储
  getStorageSync: vi.fn((key) => {
    const storage = JSON.parse(localStorage.getItem('_uni_storage') || '{}')
    return storage[key]
  }),

  setStorageSync: vi.fn((key, data) => {
    let storage = JSON.parse(localStorage.getItem('_uni_storage') || '{}')
    storage[key] = data
    localStorage.setItem('_uni_storage', JSON.stringify(storage))
  }),

  // 提示
  showToast: vi.fn(({ title }) => {
    // 可以在测试中验证
  }),

  // 系统信息
  getSystemInfoSync: vi.fn(() => ({
    brand: 'devtools',
    model: 'iPhone 11',
    system: 'iOS 13.0',
    platform: 'devtools'
  }))
}
```

### 条件编译处理

uni-app 使用条件编译，测试时需要处理:

```javascript
// #ifdef H5
// H5 特定代码
// #endif

// 测试时使用环境变量
if (process.env.UNI_PLATFORM === 'h5') {
  // H5 特定测试
}
```

### 组件测试限制

uni-app 组件测试有限制:

1. **不支持所有组件**: 如 `<camera>`, `<map>` 等原生组件
2. **API 限制**: 某些 API 在浏览器中不可用
3. **样式问题**: rpx 单位在测试中需要转换

解决方案:

```javascript
// 使用 happy-dom 提供 DOM 环境
import { mount } from '@vue/test-utils'

// Mock uni-app 特定组件
vi.stubGlobal('uni', mockUniAPI)
```

---

## 最佳实践

### 1. 测试隔离

每个测试应该独立运行:

```javascript
describe('食材 API', () => {
  beforeEach(() => {
    // 重置 mock
    vi.clearAllMocks()
  })

  it('测试 1', () => {
    // 独立的测试
  })

  it('测试 2', () => {
    // 不依赖测试 1
  })
})
```

### 2. 使用描述性测试名

```javascript
// 好的命名
it('应该返回气虚质的推荐食材')
it('应该处理食材不存在的情况')

// 不好的命名
it('test ingredients')
it('test 1')
```

### 3. 使用测试分组

```javascript
describe.concurrent('食材 API', () => {
  describe.concurrent('获取食材列表', () => {
    // 并行运行测试
  })
})
```

### 4. Mock 外部依赖

```javascript
import { vi } from 'vitest'

// Mock HTTP 请求
vi.mock('@/api/ingredients', () => ({
  getIngredients: vi.fn(() => Promise.resolve(mockData))
}))
```

### 5. 测试边界条件

```javascript
describe('边界条件测试', () => {
  it('应该处理空列表', () => {
    const result = getIngredients({ skip: 0, limit: 0 })
    expect(result.data.items).toHaveLength(0)
  })

  it('应该处理无效体质代码', async () => {
    await expect(
      getIngredientRecommendation('invalid')
    ).rejects.toThrow()
  })
})
```

---

## 运行测试

### 运行所有测试

```bash
cd frontend
npm run test
```

### 运行特定测试

```bash
# 单元测试
npm run test:unit

# 组件测试
npm run test:component

# E2E 测试
npm run test:e2e
```

### 监视模式

```bash
npm run test:watch
```

### 覆盖率报告

```bash
npm run test:coverage
```

### 只运行失败的测试

```bash
npm run test:only-failed
```

---

## package.json 脚本

```json
{
  "scripts": {
    "test": "vitest",
    "test:unit": "vitest run tests/unit/",
    "test:component": "vitest run tests/component/",
    "test:e2e": "playwright test",
    "test:watch": "vitest watch",
    "test:coverage": "vitest run --coverage",
    "test:ui": "vitest --ui"
  }
}
```

---

**文档版本**: v1.0
**最后更新**: 2026-01-20
**相关文档**: [docs/testing.md](../testing.md)
