# 测试页面设计文档

## 页面概述

| 项目 | 说明 |
|------|------|
| 页面路径 | `/pages/test/test` |
| 页面名称 | 体质测试 - 30道问题 |
| 主要功能 | 引导用户完成30道体质问题测试 |
| 数据来源 | API: `getQuestions()`, 本地: `@/data/constitution.js` |

---

## 页面结构

```
测试页面 (test)
├── 进度条（顶部固定）
│   ├── 进度填充条（紫色渐变）
│   └── 进度文本：X / 30
│
├── 问题卡片
│   ├── 体质类型标签（彩色徽章）
│   │   ├── 体质图标
│   │   └── 体质名称
│   ├── 问题编号：问题 X
│   ├── 问题内容
│   ├── 选项列表（5个单选项）
│   │   ├── 没有任何 (1分)
│   │   ├── 很少 (2分)
│   │   ├── 有时 (3分)
│   │   ├── 经常 (4分)
│   │   └── 总是 (5分)
│   └── 导航按钮
│       ├── 上一题（非第一题显示）
│       ├── 下一题（非最后一题显示）
│       └── 提交测试（最后一题显示）
│
└── 快速跳转面板
    └── 按体质类型分组（9组）
        ├── 组标签：[图标] 名称 (题目范围)
        └── 题目按钮网格（4列）
            ├── 已答题：紫色渐变背景
            ├── 当前题：紫色边框
            └── 未答题：灰色背景
```

---

## 题目分组结构

| 体质类型 | 题目范围 | 数量 | 标签颜色 |
|----------|----------|------|----------|
| 平和质 | 1-4 | 4题 | #52c41a |
| 气虚质 | 5-8 | 4题 | #faad14 |
| 阳虚质 | 9-12 | 4题 | #1890ff |
| 阴虚质 | 13-16 | 4题 | #eb2f96 |
| 痰湿质 | 17-19 | 3题 | #722ed1 |
| 湿热质 | 20-22 | 3题 | #fa541c |
| 血瘀质 | 23-25 | 3题 | #f5222d |
| 气郁质 | 26-28 | 3题 | #13c2c2 |
| 特禀质 | 29-30 | 2题 | #52c41a |

---

## 组件设计

### 1. 进度条 (`.progress-bar`)

**样式规格**
```scss
.progress-bar {
  width: 100%;
  height: 8rpx;
  background: #e8e8e8;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s;
}

.progress-text {
  text-align: center;
  padding: 30rpx;
  font-size: 26rpx;
  color: #666;
}
```

### 2. 体质类型标签 (`.constitution-tag`)

显示当前问题所属的体质类型。

**样式规格**
```scss
.constitution-tag {
  display: inline-flex;
  align-items: center;
  gap: 8rpx;
  padding: 10rpx 20rpx;
  border-radius: 20rpx;
  margin-bottom: 20rpx;
  color: #fff;
}

.tag-icon {
  font-size: 24rpx;
}

.tag-name {
  font-size: 24rpx;
  font-weight: 500;
}
```

### 3. 问题卡片 (`.question-card`)

**样式规格**
```scss
.question-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 40rpx;
  margin: 20rpx 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
}

.question-number {
  font-size: 24rpx;
  color: #999;
  margin-bottom: 16rpx;
}

.question-content {
  font-size: 36rpx;
  font-weight: 600;
  line-height: 1.6;
  margin-bottom: 40rpx;
  color: #1a1a1a;
}
```

### 4. 选项列表 (`.options`)

**选项定义**
```javascript
const options = [
  { value: 1, label: '没有' },
  { value: 2, label: '很少' },
  { value: 3, label: '有时' },
  { value: 4, label: '经常' },
  { value: 5, label: '总是' }
]
```

**样式规格**
```scss
.option-item {
  display: flex;
  align-items: center;
  padding: 28rpx 24rpx;
  border: 2rpx solid #e8e8e8;
  border-radius: 16rpx;
  margin-bottom: 20rpx;
  transition: all 0.3s;
}

.option-item.active {
  border-color: #667eea;
  background: #f8f9ff;
}

.option-radio {
  width: 40rpx;
  height: 40rpx;
  border: 3rpx solid #d9d9d9;
  border-radius: 50%;
  margin-right: 24rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.option-item.active .option-radio {
  border-color: #667eea;
}

.radio-dot {
  width: 20rpx;
  height: 20rpx;
  background: #667eea;
  border-radius: 50%;
}
```

### 5. 快速跳转面板 (`.quick-nav`)

**样式规格**
```scss
.question-groups {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.question-group-label {
  font-size: 24rpx;
  color: #999;
  margin-bottom: 12rpx;
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.question-grid-group {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12rpx;
}

.question-dot {
  width: 60rpx;
  height: 60rpx;
  border-radius: 12rpx;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  color: #999;
  transition: all 0.3s;
}

.question-dot.answered {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.question-dot.current {
  border: 3rpx solid #667eea;
}
```

---

## 数据流

### 状态管理

```javascript
// 题目数据
const questions = ref([])           // 从 API 加载的30道题目
const answers = ref(new Array(30).fill(null))  // 用户答案

// 当前状态
const currentQuestionIndex = ref(0)  // 当前题目索引 (0-29)
const loading = ref(false)           // 加载状态
const submitting = ref(false)        // 提交状态

// 计算属性
const progress = computed(() => ((currentQuestionIndex.value + 1) / 30) * 100)

const currentQuestion = computed(() => {
  return questions.value[currentQuestionIndex.value]
})

const allAnswered = computed(() => {
  return answers.value.every(a => a !== null)
})

// 体质标签
const currentConstitutionType = computed(() => {
  const questionNum = currentQuestionIndex.value + 1
  for (const [type, info] of Object.entries(QUESTION_GROUPS)) {
    if (questionNum >= info.start && questionNum <= info.end) {
      return {
        type,
        name: info.name,
        color: CONSTITUTION_INFO[type]?.color || '#667eea'
      }
    }
  }
  return null
})
```

---

## API 调用

### 1. 获取题目

**端点**: `GET /api/v1/questions`

**响应格式**:
```json
{
  "code": 200,
  "data": {
    "questions": [
      {
        "id": 1,
        "content": "您容易疲乏吗？",
        "constitution_type": "qi_deficiency"
      },
      {
        "id": 2,
        "content": "您容易气短（短气，喘不上气）吗？",
        "constitution_type": "qi_deficiency"
      }
    ]
  }
}
```

**调用代码**:
```javascript
async function loadQuestions() {
  loading.value = true
  try {
    const res = await getQuestions()
    questions.value = res.data.questions
  } catch (error) {
    uni.showToast({ title: '加载失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}
```

### 2. 提交答案

**端点**: `POST /api/v1/test/submit`

**请求格式**:
```json
{
  "answers": [1, 2, 3, 4, 5, 3, 2, 1, ...]  // 30个整数，范围1-5
}
```

**响应格式**:
```json
{
  "code": 200,
  "data": {
    "result_id": "uuid-string",
    "primary_constitution": "yang_deficiency",
    "primary_constitution_name": "阳虚质",
    "scores": {
      "peace": 45,
      "qi_deficiency": 60,
      "yang_deficiency": 85
    },
    "secondary_constitutions": [
      { "type": "qi_deficiency", "name": "气虚质", "score": 60 }
    ]
  }
}
```

**调用代码**:
```javascript
async function submitTest() {
  if (!allAnswered.value) {
    uni.showToast({ title: '请完成所有题目', icon: 'none' })
    return
  }

  submitting.value = true
  try {
    const res = await submitTestApi(answers.value)
    uni.setStorageSync('resultId', res.data.result_id)
    uni.redirectTo({
      url: `/pages/result/result?resultId=${res.data.result_id}`
    })
  } catch (error) {
    uni.showToast({ title: '提交失败', icon: 'none' })
  } finally {
    submitting.value = false
  }
}
```

---

## 用户交互流程

```
进入页面
    ↓
加载题目（API）
    ↓
显示第1题
    ↓
用户选择答案 → 点击"下一题"
    ↓
显示第2题
    ↓
...（重复）
    ↓
显示第30题
    ↓
用户选择答案 → 点击"提交测试"
    ↓
提交答案（API）
    ↓
跳转结果页
```

### 导航逻辑

| 条件 | 可用按钮 | 动作 |
|------|----------|------|
| 第1题 | 下一题 | 进入第2题 |
| 第2-29题 | 上一题、下一题 | 前后导航 |
| 第30题 | 上一题、提交测试 | 返回或提交 |

---

## 验证规则

| 验证项 | 规则 | 错误提示 |
|--------|------|----------|
| 答案完整性 | 所有30题必须作答 | "请完成所有题目" |
| 答案范围 | 答案值必须在1-5之间 | 前端限制选项选择 |

---

## 可访问性

- 键盘导航支持（Tab 切换选项）
- 单选框状态清晰可见
- 进度条提供视觉反馈
- 快速跳转支持任意题目访问

---

## 性能优化

- 题目数据一次性加载，避免重复请求
- 答案存储在内存中，减少存储操作
- 使用 `v-for` 的 `:key` 优化列表渲染
- CSS transition 使用 GPU 加速

---

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| 题目加载失败 | 显示 Toast 提示，阻止继续 |
| 提交失败 | 显示 Toast 提示，允许重新提交 |
| 网络超时 | 60秒超时，显示错误提示 |

---

## 样式变量

```scss
// 进度条颜色
$progress-gradient: linear-gradient(90deg, #667eea 0%, #764ba2 100%);

// 选项状态
$option-border: #e8e8e8;
$option-border-active: #667eea;
$option-bg-active: #f8f9ff;

// 按钮状态
$option-radio-border: #d9d9d9;
$option-radio-border-active: #667eea;
$option-radio-dot: #667eea;

// 题目按钮
$question-dot-bg: #f5f5f5;
$question-dot-bg-active: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
$question-dot-border-current: 3rpx solid #667eea;
```
