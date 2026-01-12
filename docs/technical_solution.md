# 中医养生产品矩阵技术方案

> 本方案支持产品矩阵化开发，通过统一技术架构实现多个小程序的快速迭代

## 一、技术栈选型

### 1.1 推荐方案：uni-app + Python FastAPI + Serverless

```
┌─────────────────────────────────────────────────────────────────────┐
│                        前端层（多产品复用）                           │
├─────────────────────────────────────────────────────────────────────┤
│  uni-app (Vue 3 + TypeScript + Pinia)                               │
│  ├─ 抖音小程序：体质测试、AI舌诊、穴位地图、养生课堂...               │
│  ├─ 微信小程序：产品矩阵扩展                                         │
│  └─ H5营销页：视频引流落地页                                        │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        后端层（Python + FastAPI）                     │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                      共享服务层（复用）                          │ │
│  │  • 用户中心 (统一认证、用户档案、会员体系)                        │ │
│  │  • 数据中心 (健康数据、行为数据、跨产品数据)                      │ │
│  │  • 推荐引擎 (个性化推荐、跨产品推荐)                              │ │
│  │  • 支付中心 (统一支付、对账、退款)                                │ │
│  │  • 消息中心 (推送、站内信、模板消息)                              │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                              ↓                                       │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                    业务服务层（按产品拆分）                      │ │
│  │ 体质服务 | 舌诊服务 | 打卡服务 | 商城服务 | 预约服务 | 课程服务  │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        数据层                                       │
├─────────────────────────────────────────────────────────────────────┤
│  • PostgreSQL（主数据库，JSONB支持）                                │
│  • Redis（缓存、排行榜、限流、Session）                             │
│  • 云存储 COS（图片、视频、分享海报）                               │
│  • ElasticSearch（全文搜索，可选）                                  │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        部署层                                       │
├─────────────────────────────────────────────────────────────────────┤
│  • 字节云（抖音小程序首选）                                         │
│  • 腾讯云（微信小程序首选）                                         │
│  • 云函数 Serverless（MVP阶段）                                     │
│  • 云托管 CloudRun（成长期）                                        │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 为什么选择 Python + FastAPI？

| 考虑因素 | 选型 | 理由 |
|---------|-----|-----|
| **团队熟悉度** | Python | 你已熟悉Python，学习成本最低 |
| **开发效率** | FastAPI | 代码简洁、自动文档、类型验证 |
| **性能表现** | FastAPI | 异步支持，性能媲美Node.js |
| **AI/ML扩展** | Python | 完美支持后期AI舌诊、推荐算法 |
| **云函数支持** | Python | 字节云/腾讯云都支持Python 3.10+ |
| **2025趋势** | FastAPI | 使用率38%，已成为Python Web首选 |

---

## 二、前端技术方案

### 2.1 框架选择：uni-app (Vue 3)

**核心优势：**
- ✅ 一套代码同时发布抖音、微信、H5
- ✅ Vue 3 Composition API，代码组织更优雅
- ✅ TypeScript 支持，类型安全
- ✅ 成熟的组件市场和UI框架
- ✅ 抖音小程序官方支持良好

**项目结构：**
```
tcm-constitution-miniapp/
├── src/
│   ├── pages/              # 页面
│   │   ├── index/          # 首页
│   │   ├── quiz/           # 问卷测试
│   │   ├── result/         # 结果报告
│   │   └── profile/        # 个人中心
│   ├── components/         # 组件
│   │   ├── quiz-card/      # 问卷卡片
│   │   ├── constitution-chart/  # 体质图表
│   │   └── recommendation-list/  # 推荐列表
│   ├── api/                # API接口
│   ├── store/              # 状态管理
│   ├── utils/              # 工具函数
│   ├── styles/             # 样式
│   └── static/             # 静态资源
├── uni_modules/            # uni-app插件
├── cloudfunctions/         # 云函数
├── manifest.json           # 配置文件
├── pages.json              # 页面配置
└── package.json
```

### 2.2 UI框架选择

**推荐：uView UI 2.0**

| 框架 | 优势 | 劣势 |
|-----|-----|-----|
| **uView UI** | 组件丰富、文档完善、更新及时 | 部分组件样式需调整 |
| uni-ui | 官方出品、稳定 | 组件较少 |
| NutUI | 京东出品、质量高 | 主要面向Vue3 |
| 自研 | 完全可控 | 开发成本高 |

### 2.3 状态管理

**推荐：Pinia（Vue 3官方推荐）**

```typescript
// stores/constitution.ts
import { defineStore } from 'pinia'

export const useConstitutionStore = defineStore('constitution', {
  state: () => ({
    quizAnswers: [] as QuizAnswer[],
    constitutionResult: null as ConstitutionResult | null,
    userProfile: null as UserProfile | null
  }),
  actions: {
    saveAnswer(questionId: string, answer: number) {
      // 保存答案
    },
    async submitQuiz() {
      // 提交问卷
    },
    async getRecommendations() {
      // 获取推荐
    }
  }
})
```

### 2.4 网络请求

**推荐封装：**

```typescript
// utils/request.ts
interface RequestOptions {
  url: string
  method?: 'GET' | 'POST'
  data?: any
  showLoading?: boolean
}

export const request = <T = any>(options: RequestOptions): Promise<T> => {
  const { url, method = 'GET', data, showLoading = true } = options

  if (showLoading) {
    uni.showLoading({ title: '加载中...' })
  }

  return new Promise((resolve, reject) => {
    uni.request({
      url: `${BASE_URL}${url}`,
      method,
      data,
      header: {
        'Authorization': `Bearer ${getToken()}`
      },
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data)
        } else {
          reject(res)
        }
      },
      fail: reject,
      complete: () => {
        if (showLoading) uni.hideLoading()
      }
    })
  })
}
```

---

## 三、后端技术方案（Python + FastAPI）

### 3.1 方案对比

| 方案 | 适用阶段 | 优势 | 劣势 | 月成本 |
|-----|---------|-----|-----|-------|
| **云函数 Serverless** | MVP | 免运维、按量付费、自动扩展 | 冷启动、调试复杂 | ¥50-200 |
| **云托管 CloudRun** | 成长期 | 性能好、灵活度高 | 需运维 | ¥200-1000 |
| **自建服务器** | 成熟期 | 完全控制 | 运维成本高 | ¥500+ |

### 3.2 FastAPI 核心优势

```
FastAPI 特点：
├── 高性能（异步支持，性能媲美 Node.js 和 Go）
├── 自动生成 API 文档（Swagger/UI）
├── 类型验证（Pydantic 自动处理）
├── 开发速度快（代码简洁，易维护）
├── AI/ML 友好（Python 生态完善）
└── 2025年使用率 38%（Python Web 框架榜首）
```

### 3.3 项目结构（支持产品矩阵）

```
tcm-backend/
├── app/
│   ├── api/                    # API路由层
│   │   ├── v1/                 # API版本管理
│   │   │   ├── constitution.py   # 体质测试接口
│   │   │   ├── tongue.py         # 舌诊接口
│   │   │   ├── acupoint.py       # 穴位接口
│   │   │   ├── course.py         # 课程接口
│   │   │   ├── checkin.py        # 打卡接口
│   │   │   ├── mall.py           # 商城接口
│   │   │   └── user.py           # 用户接口
│   │   └── deps.py              # 依赖注入
│   ├── core/                   # 核心配置
│   │   ├── config.py           # 配置管理
│   │   ├── security.py         # 安全认证
│   │   └── database.py         # 数据库连接
│   ├── models/                 # 数据模型
│   │   ├── constitution.py     # 体质模型
│   │   ├── user.py             # 用户模型
│   │   ├── course.py           # 课程模型
│   │   └── product.py          # 商品模型
│   ├── schemas/                # Pydantic模型（API数据验证）
│   │   ├── constitution.py
│   │   ├── user.py
│   │   └── common.py
│   ├── services/               # 业务逻辑层
│   │   ├── constitution_service.py    # 体质分析服务
│   │   ├── tongue_service.py          # 舌诊AI服务
│   │   ├── recommendation_service.py  # 推荐引擎
│   │   └── shared_service.py          # 共享服务
│   ├── shared/                 # 共享服务层
│   │   ├── user_center.py      # 用户中心
│   │   ├── payment_center.py   # 支付中心
│   │   ├── message_center.py   # 消息中心
│   │   └── data_center.py      # 数据中心
│   └── main.py                 # FastAPI应用入口
├── tests/                      # 测试
├── requirements.txt            # Python依赖
├── Dockerfile                  # Docker配置
└── README.md
```

### 3.4 FastAPI 应用入口

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import constitution, tongue, acupoint, course, checkin, mall, user
from app.core.config import settings

app = FastAPI(
    title="中医养生产品矩阵API",
    description="支持体质测试、AI舌诊、穴位地图、养生课堂等多个产品",
    version="1.0.0"
)

# CORS配置（支持小程序跨域）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境需限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(constitution.router, prefix="/api/v1/constitution", tags=["体质测试"])
app.include_router(tongue.router, prefix="/api/v1/tongue", tags=["AI舌诊"])
app.include_router(acupoint.router, prefix="/api/v1/acupoint", tags=["穴位地图"])
app.include_router(course.router, prefix="/api/v1/course", tags=["养生课堂"])
app.include_router(checkin.router, prefix="/api/v1/checkin", tags=["打卡助手"])
app.include_router(mall.router, prefix="/api/v1/mall", tags=["食疗商城"])
app.include_router(user.router, prefix="/api/v1/user", tags=["用户中心"])

@app.get("/")
async def root():
    return {
        "message": "中医养生产品矩阵API",
        "products": [
            "体质测试助手",
            "AI舌诊自测",
            "中医穴位地图",
            "养生课堂",
            "打卡助手",
            "食疗商城"
        ],
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### 3.5 体质分析服务示例

```python
# app/services/constitution_service.py
from typing import List, Dict
from app.models.constitution import ConstitutionType

class ConstitutionService:
    """体质分析服务"""

    # CCMQ评分规则
    SCORE_CONVERT_FACTOR = 2.5  # 转换为百分制 (100/40)

    # 判定阈值
    THRESHOLD_PRIMARY = 40      # 主要体质阈值
    THRESHOLD_SECONDARY = 30    # 次要体质阈值
    THRESHOLD_PEACE = 60        # 平和质阈值

    async def analyze(self, answers: List[int], questions: List[Dict]) -> Dict:
        """
        分析体质类型

        Args:
            answers: 用户答案列表 (1-5分)
            questions: 问题列表，包含所属体质类型

        Returns:
            体质分析结果
        """
        # 1. 计算各维度得分
        scores = self._calculate_scores(answers, questions)

        # 2. 判定体质类型
        result = self._determine_constitution(scores)

        # 3. 生成报告
        report = self._generate_report(result)

        return {
            "primary": result["primary"],
            "secondary": result["secondary"],
            "scores": scores,
            "report": report
        }

    def _calculate_scores(self, answers: List[int], questions: List[Dict]) -> Dict[str, float]:
        """计算各体质维度得分"""
        scores = {
            "peace": 0.0,          # 平和质
            "qi_deficiency": 0.0,   # 气虚质
            "yang_deficiency": 0.0, # 阳虚质
            "yin_deficiency": 0.0,  # 阴虚质
            "phlegm_damp": 0.0,     # 痰湿质
            "damp_heat": 0.0,       # 湿热质
            "blood_stasis": 0.0,    # 血瘀质
            "qi_depression": 0.0,   # 气郁质
            "special": 0.0          # 特禀质
        }

        # 按问题归属累加得分
        for i, question in enumerate(questions):
            constitution_type = question.get("constitution_type")
            answer = answers[i] if i < len(answers) else 0
            scores[constitution_type] += answer

        # 转换为百分制
        for key in scores:
            scores[key] = min(100, scores[key] * self.SCORE_CONVERT_FACTOR)

        return scores

    def _determine_constitution(self, scores: Dict[str, float]) -> Dict:
        """判定体质类型"""
        result_types = []
        max_score = 0
        primary_type = ""

        # 收集所有符合阈值的体质
        for ctype, score in scores.items():
            if score >= self.THRESHOLD_SECONDARY:
                result_types.append({"type": ctype, "score": score})
                if score > max_score:
                    max_score = score
                    primary_type = ctype

        # 平和质判定
        if scores["peace"] >= self.THRESHOLD_PEACE:
            primary_type = "peace"

        return {
            "primary": primary_type,
            "secondary": [r for r in result_types if r["type"] != primary_type]
        }

    def _generate_report(self, result: Dict) -> Dict:
        """生成体质报告"""
        primary = result["primary"]
        reports = {
            "peace": {
                "name": "平和质",
                "description": "阴阳气血调和，体态适中，面色红润，精力充沛",
                "characteristics": ["精力充沛", "睡眠良好", "胃口正常", "适应力强"],
                "advice": "保持良好生活习惯，维持健康状态"
            },
            "qi_deficiency": {
                "name": "气虚质",
                "description": "元气不足，气息低弱，容易疲乏",
                "characteristics": ["疲乏气短", "易出汗", "容易感冒", "肌肉松软"],
                "advice": "宜食补气食物，如糯米、大枣、山药等"
            },
            "yang_deficiency": {
                "name": "阳虚质",
                "description": "阳气不足，畏寒怕冷",
                "characteristics": ["手足不温", "喜热饮食", "畏寒怕冷"],
                "advice": "宜食温补食物，注意保暖，可适当吃羊肉、桂圆"
            },
            # ... 其他体质类型
        }

        return reports.get(primary, {})
```

### 3.6 API路由示例

```python
# app/api/v1/constitution.py
from fastapi import APIRouter, Depends
from typing import List
from app.schemas.constitution import QuizSubmit, QuizResponse
from app.services.constitution_service import ConstitutionService
from app.shared.user_center import get_current_user

router = APIRouter()
service = ConstitutionService()

@router.post("/quiz/submit", response_model=QuizResponse)
async def submit_quiz(
    data: QuizSubmit,
    current_user = Depends(get_current_user)
):
    """
    提交体质测试问卷

    - **answers**: 答案列表，每个问题1-5分
    - **questionnaire_id**: 问卷ID（可选，默认使用最新版）
    """
    # 获取问卷题目
    questions = await get_questions(data.questionnaire_id)

    # 分析体质
    result = await service.analyze(data.answers, questions)

    # 保存结果
    await save_result(current_user["id"], result)

    return QuizResponse(
        code=0,
        message="success",
        data=result
    )

@router.get("/quiz/questions")
async def get_questions(questionnaire_id: str = None):
    """获取问卷题目"""
    questions = await load_questions(questionnaire_id)
    return {
        "code": 0,
        "data": questions
    }

@router.get("/result/{result_id}")
async def get_result(result_id: str):
    """获取测试结果"""
    result = await load_result(result_id)
    return {
        "code": 0,
        "data": result
    }
```

---

## 四、数据库设计（支持产品矩阵）

### 4.1 数据库选择

| 数据库 | 用途 | 理由 |
|-------|-----|-----|
| **PostgreSQL** | 主数据库 | 支持JSONB、适合复杂查询、可靠性高 |
| **Redis** | 缓存 | 高性能缓存、排行榜、限流、Session |
| **云存储 COS** | 文件存储 | 图片、视频、分享海报 |
| **ElasticSearch** | 搜索 | 全文搜索（可选，后期） |

### 4.2 核心数据表（产品矩阵）

```sql
-- ============================================
-- 共享服务层（所有产品复用）
-- ============================================

-- 用户表（统一用户中心）
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- 抖音/微信 openid
    douyin_openid VARCHAR(128) UNIQUE,
    wechat_openid VARCHAR(128) UNIQUE,
    unionid VARCHAR(128),
    -- 基础信息
    nickname VARCHAR(100),
    avatar_url VARCHAR(500),
    gender INT CHECK (gender IN (0, 1, 2)),
    age INT,
    region VARCHAR(100),
    phone VARCHAR(20),
    -- 会员信息
    member_level VARCHAR(20) DEFAULT 'free', -- free, silver, gold, diamond
    member_expire_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 统一用户画像（支持跨产品推荐）
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    -- 体质信息
    primary_constitution VARCHAR(50),
    constitution_scores JSONB,
    -- 健康关注标签
    health_concerns TEXT[], -- 睡眠、消化、美容等
    -- 偏好数据
    preferences JSONB, -- 饮食偏好、运动偏好等
    -- 地理信息（用于季节推荐）
    city VARCHAR(100),
    province VARCHAR(100),
    -- 统计数据
    last_test_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);

-- ============================================
-- 体质测试产品
-- ============================================

-- 问卷表
CREATE TABLE questionnaires (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    version VARCHAR(20) DEFAULT '1.0',
    total_questions INT DEFAULT 30,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 问题表
CREATE TABLE questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    questionnaire_id UUID REFERENCES questionnaires(id),
    question_text TEXT NOT NULL,
    constitution_type VARCHAR(50) NOT NULL, -- 所属体质类型
    order_index INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 用户回答记录
CREATE TABLE user_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    questionnaire_id UUID REFERENCES questionnaires(id),
    answers JSONB NOT NULL, -- 答案数组
    duration INT, -- 完成时长（秒）
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 体质结果表
CREATE TABLE constitution_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    response_id UUID REFERENCES user_responses(id),
    primary_constitution VARCHAR(50) NOT NULL,
    secondary_constitutions JSONB,
    scores JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- AI舌诊产品
-- ============================================

CREATE TABLE tongue_diagnoses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    -- 图片信息
    image_url VARCHAR(500),
    -- AI分析结果
    tongue_color VARCHAR(50), -- 舌质颜色
    tongue_coating VARCHAR(50), -- 舌苔
    tongue_shape VARCHAR(50), -- 舌形
    -- 判定结果
    constitution_type VARCHAR(50),
    health_status TEXT,
    -- AI置信度
    confidence DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 养生课堂产品
-- ============================================

CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    cover_url VARCHAR(500),
    teacher VARCHAR(100),
    -- 课程类型
    course_type VARCHAR(50), -- free, paid, vip
    price DECIMAL(10,2) DEFAULT 0,
    -- 标签
    tags TEXT[],
    -- 统计
    view_count INT DEFAULT 0,
    enroll_count INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'published',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 课程章节
CREATE TABLE course_chapters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(200),
    video_url VARCHAR(500),
    audio_url VARCHAR(500),
    duration INT, -- 时长（秒）
    order_index INT,
    is_free BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 学习记录
CREATE TABLE course_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    course_id UUID REFERENCES courses(id) ON DELETE CASCADE,
    chapter_id UUID REFERENCES course_chapters(id),
    completed BOOLEAN DEFAULT FALSE,
    progress_percent INT DEFAULT 0,
    last_position INT, -- 视频播放位置
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, course_id, chapter_id)
);

-- ============================================
-- 打卡助手产品
-- ============================================

CREATE TABLE checkin_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_type VARCHAR(50) NOT NULL, -- drink_water, soak_feet, exercise等
    title VARCHAR(100),
    description TEXT,
    icon VARCHAR(200),
    -- 目标设置
    target_value INT, -- 如8杯水
    unit VARCHAR(20), -- 杯、分钟、次
    points INT DEFAULT 10, -- 完成获得积分
    -- 适用体质
    suitable_constitutions TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 打卡记录
CREATE TABLE checkin_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    task_id UUID REFERENCES checkin_tasks(id),
    task_date DATE NOT NULL,
    actual_value INT,
    status VARCHAR(20) DEFAULT 'completed', -- completed, skipped
    points_earned INT DEFAULT 10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, task_id, task_date)
);

-- ============================================
-- 食疗商城产品
-- ============================================

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    images TEXT[],
    -- 分类
    category VARCHAR(50), -- tea, snack, spice等
    tags TEXT[],
    -- 价格
    price DECIMAL(10,2) NOT NULL,
    original_price DECIMAL(10,2),
    -- 库存
    stock INT DEFAULT 0,
    -- 适用体质
    suitable_constitutions TEXT[],
    avoid_constitutions TEXT[],
    -- 规格信息
    specs JSONB,
    status VARCHAR(20) DEFAULT 'on_sale',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 订单表
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    order_no VARCHAR(50) UNIQUE NOT NULL,
    -- 金额
    total_amount DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    pay_amount DECIMAL(10,2) NOT NULL,
    -- 状态
    status VARCHAR(20) DEFAULT 'pending', -- pending, paid, shipped, completed
    -- 地址
    receiver_name VARCHAR(50),
    receiver_phone VARCHAR(20),
    receiver_address TEXT,
    -- 时间
    paid_at TIMESTAMP,
    shipped_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 订单明细
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID REFERENCES products(id),
    product_name VARCHAR(200),
    product_spec JSONB,
    price DECIMAL(10,2),
    quantity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 食物库（知识库，跨产品使用）
-- ============================================

CREATE TABLE foods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    -- 中医属性
    nature VARCHAR(20), -- 寒、凉、平、温、热
    flavor VARCHAR(50), -- 酸、苦、甘、辛、咸
    meridian TEXT[], -- 归经
    -- 体质适配
    suitable_constitutions TEXT[],
    avoid_constitutions TEXT[],
    -- 营养信息
    nutrition_info JSONB,
    images TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 穴位库（知识库）
CREATE TABLE acupoints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL,
    pinyin VARCHAR(100),
    -- 归属经络
    meridian VARCHAR(50),
    -- 位置
    location TEXT,
    -- 功效
    functions TEXT[],
    -- 主治
    indications TEXT[],
    -- 按摩方法
    massage_method TEXT,
    -- 图片/视频
    images TEXT[],
    video_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 共享服务：积分系统
-- ============================================

CREATE TABLE points_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    points INT NOT NULL,
    source VARCHAR(50) NOT NULL, -- checkin, purchase, share等
    source_id UUID, -- 关联记录ID
    description TEXT,
    balance INT, -- 余额
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 索引优化
-- ============================================

-- 用户相关索引
CREATE INDEX idx_users_douyin_openid ON users(douyin_openid);
CREATE INDEX idx_users_wechat_openid ON users(wechat_openid);
CREATE INDEX idx_user_profiles_user ON user_profiles(user_id);

-- 体质测试索引
CREATE INDEX idx_responses_user ON user_responses(user_id);
CREATE INDEX idx_results_user ON constitution_results(user_id);
CREATE INDEX idx_results_created ON constitution_results(created_at DESC);

-- 课程索引
CREATE INDEX idx_course_progress_user ON course_progress(user_id);
CREATE INDEX idx_course_progress_course ON course_progress(course_id);

-- 打卡索引
CREATE INDEX idx_checkin_user ON checkin_records(user_id);
CREATE INDEX idx_checkin_date ON checkin_records(task_date);

-- 商城索引
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created ON orders(created_at DESC);

-- ============================================
-- 统一用户视图（支持跨产品数据查询）
-- ============================================

CREATE VIEW user_unified_view AS
SELECT
    u.id,
    u.nickname,
    u.member_level,
    up.primary_constitution,
    -- 体质测试统计
    COUNT(DISTINCT cr.id) as constitution_test_count,
    MAX(cr.created_at) as last_test_at,
    -- 课程统计
    COUNT(DISTINCT cp.id) as course_views,
    COUNT(DISTINCT CASE WHEN cp.completed THEN cp.id END) as course_completed,
    -- 打卡统计
    COUNT(DISTINCT chr.id) as checkin_count,
    MAX(chr.task_date) as last_checkin_at,
    -- 订单统计
    COUNT(DISTINCT o.id) as order_count,
    SUM(o.pay_amount) as total_spend,
    -- 活跃度
    MAX(GREATEST(
        cr.created_at,
        cp.created_at,
        chr.created_at,
        o.created_at
    )) as last_active_at
FROM users u
LEFT JOIN user_profiles up ON u.id = up.user_id
LEFT JOIN constitution_results cr ON u.id = cr.user_id
LEFT JOIN course_progress cp ON u.id = cp.user_id
LEFT JOIN checkin_records chr ON u.id = chr.user_id
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.nickname, u.member_level, up.primary_constitution;
```

### 4.3 Redis 缓存设计

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Redis 缓存架构                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  用户会话缓存                                                        │
│  ├── session:{user_id}          # 用户会话                           │
│  ├── token:{token}              # Token验证                          │
│                                                                     │
│  热点数据缓存                                                        │
│  ├── questions:latest          # 最新问卷题目                        │
│  ├── constitution:{type}       # 体质知识库                          │
│  ├── foods:hot                # 热门食物                             │
│  └── acupoints:hot            # 热门穴位                             │
│                                                                     │
│  排行榜缓存                                                         │
│  ├── ranking:checkin:daily     # 每日打卡排行榜                      │
│  ├── ranking:checkin:weekly    # 每周打卡排行榜                      │
│  └── ranking:course:views      # 课程浏览排行                        │
│                                                                     │
│  限流防刷                                                          │
│  ├── ratelimit:api:{user_id}   # API调用限流                        │
│  ├── ratelimit:quiz:{user_id}  # 测试次数限制                        │
│  └── spam:ip:{ip}               # IP黑名单                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 五、AI/ML方案（Python 优势）

### 5.1 AI舌诊实现

```python
# app/services/tongue_service.py
import httpx
from typing import Dict
from app.core.config import settings

class TongueDiagnosisService:
    """AI舌诊服务"""

    def __init__(self):
        # 可选择多个AI平台
        self.baidu_api_key = settings.BAIDU_AI_API_KEY
        self.tencent_api_key = settings.TENCENT_AI_API_KEY

    async def analyze_tongue(self, image_url: str) -> Dict:
        """
        分析舌象图片

        Args:
            image_url: 舌象图片URL

        Returns:
            舌诊分析结果
        """
        # 调用AI平台API（以百度为例）
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://aip.baidubce.com/rest/2.0/image-classify/v1/tongue",
                headers={"Content-Type": "application/json"},
                json={"image": image_url, "top_num": 3},
                params={"access_token": self.baidu_api_key}
            )
            result = response.json()

        # 解析AI结果
        return {
            "tongue_color": self._parse_color(result),
            "tongue_coating": self._parse_coating(result),
            "constitution_type": self._map_to_constitution(result),
            "confidence": result.get("score", 0.8)
        }

    def _map_to_constitution(self, ai_result: Dict) -> str:
        """将AI舌诊结果映射到体质类型"""
        # 红舌 → 阴虚质/湿热质
        # 淡白舌 → 气虚质/阳虚质
        # 胖大舌 → 痰湿质
        # 齿痕 → 脾虚/气虚质
        color = ai_result.get("color", "")
        coating = ai_result.get("coating", "")

        if color == "red":
            return "yin_deficiency" if coating == "none" else "damp_heat"
        elif color == "pale":
            return "yang_deficiency"
        elif ai_result.get("swollen", False):
            return "phlegm_damp"
        else:
            return "qi_deficiency"
```

### 5.2 推荐引擎（跨产品）

```python
# app/services/recommendation_service.py
from typing import List, Dict
from sqlalchemy import select
from app.models.user import UserProfile
from app.models.food import Food
from app.models.product import Product

class RecommendationService:
    """跨产品推荐引擎"""

    def __init__(self):
        self.weight = {
            "constitution_match": 0.4,  # 体质匹配度
            "season_bonus": 0.2,         # 季节加成
            "user_preference": 0.2,      # 用户偏好
            "popularity": 0.1,           # 热度
            "feedback_score": 0.1        # 历史反馈
        }

    async def cross_product_recommend(self, user_id: str, product_type: str) -> List[Dict]:
        """
        跨产品推荐

        Args:
            user_id: 用户ID
            product_type: 产品类型 (diet, exercise, course, product等)

        Returns:
            推荐列表
        """
        # 1. 获取用户画像
        profile = await self._get_user_profile(user_id)

        # 2. 根据产品类型获取候选池
        candidates = await self._get_candidates(product_type)

        # 3. 计算推荐分数
        scored_items = []
        for item in candidates:
            score = await self._calculate_score(item, profile)
            scored_items.append({**item, "recommend_score": score})

        # 4. 排序返回Top-N
        scored_items.sort(key=lambda x: x["recommend_score"], reverse=True)
        return scored_items[:20]

    async def _calculate_score(self, item: Dict, profile: Dict) -> float:
        """计算推荐分数"""
        score = 0.0

        # 体质匹配度
        if profile.get("constitution") in item.get("suitable_constitutions", []):
            score += self.weight["constitution_match"] * 100
        if profile.get("constitution") in item.get("avoid_constitutions", []):
            score -= 50  # 扣分

        # 季节加成
        current_season = self._get_current_season()
        if current_season in item.get("seasons", []):
            score += self.weight["season_bonus"] * 20

        # 用户偏好
        if item.get("category") in profile.get("preferences", {}).get("likes", []):
            score += self.weight["user_preference"] * 10

        # 热度
        score += self.weight["popularity"] * item.get("popularity_score", 0)

        return score

    def _get_current_season(self) -> str:
        """获取当前季节"""
        from datetime import datetime
        month = datetime.now().month
        if 3 <= month <= 5:
            return "spring"
        elif 6 <= month <= 8:
            return "summer"
        elif 9 <= month <= 11:
            return "autumn"
        else:
            return "winter"
```

### 5.3 机器学习优化（后期）

```python
# app/services/ml_constitution_service.py
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from typing import List, Tuple

class MLConstitutionService:
    """机器学习体质识别（后期优化）"""

    def __init__(self):
        self.model = None
        self.model_path = "models/constitution_model.pkl"

    def load_model(self):
        """加载训练好的模型"""
        try:
            self.model = joblib.load(self.model_path)
        except FileNotFoundError:
            print("模型文件不存在，使用传统评分法")

    def train(self, X: np.ndarray, y: np.ndarray):
        """
        训练模型

        Args:
            X: 特征矩阵 (样本数 × 特征数)
            y: 标签 (体质类型)
        """
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.model.fit(X, y)
        joblib.dump(self.model, self.model_path)

    def predict(self, answers: List[int]) -> Tuple[str, float]:
        """
        预测体质类型

        Returns:
            (体质类型, 置信度)
        """
        if self.model is None:
            self.load_model()

        prediction = self.model.predict([answers])[0]
        probability = self.model.predict_proba([answers])[0].max()

        return prediction, probability
```

---

## 六、共享服务层设计

### 6.1 统一用户中心

```python
# app/shared/user_center.py
from fastapi import Depends, HTTPException, status
from typing import Optional
from app.models.user import User, UserProfile
from sqlalchemy.ext.asyncio import AsyncSession

class UserCenter:
    """统一用户中心"""

    @staticmethod
    async def get_or_create_user(
        openid: str,
        platform: str,  # douyin, wechat
        db: AsyncSession
    ) -> User:
        """获取或创建用户"""
        # 根据平台查找用户
        if platform == "douyin":
            user = await db.execute(
                select(User).where(User.douyin_openid == openid)
            )
        else:
            user = await db.execute(
                select(User).where(User.wechat_openid == openid)
            )

        user = user.scalar_one_or_none()

        # 不存在则创建
        if not user:
            user = User(
                **{f"{platform}_openid": openid},
                nickname=f"用户{openid[:8]}"
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)

        return user

    @staticmethod
    async def get_user_profile(user_id: str, db: AsyncSession) -> UserProfile:
        """获取用户画像（支持跨产品推荐）"""
        profile = await db.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        return profile.scalar_one_or_none()

    @staticmethod
    async def update_member_level(user_id: str, level: str, db: AsyncSession):
        """更新会员等级（跨产品生效）"""
        # 更新用户表
        await db.execute(
            select(User).where(User.id == user_id)
        )
        # ... 会员逻辑
        await db.commit()
```

### 6.2 支付中心

```python
# app/shared/payment_center.py
from typing import Dict
import httpx

class PaymentCenter:
    """统一支付中心"""

    def __init__(self):
        # 支付宝/微信支付配置
        self.alipay_config = {...}
        self.wechat_pay_config = {...}

    async def create_order(
        self,
        user_id: str,
        amount: float,
        subject: str,
        order_type: str  # membership, course, product
    ) -> Dict:
        """创建支付订单"""
        order_no = self._generate_order_no()
        # 调用支付平台API
        return {
            "order_no": order_no,
            "payment_params": {...}
        }

    async def verify_callback(self, callback_data: Dict) -> bool:
        """验证支付回调"""
        # 验证签名
        # 更新订单状态
        return True
```

### 6.3 消息中心

```python
# app/shared/message_center.py
from typing import List

class MessageCenter:
    """消息中心"""

    async def send_template_message(
        self,
        user_id: str,
        template_id: str,
        data: Dict
    ):
        """发送模板消息"""
        # 调用小程序模板消息API
        pass

    async def send_push(self, user_ids: List[str], content: str):
        """发送推送消息"""
        # 调用推送服务
        pass
```

---

## 七、部署方案（Python + FastAPI）

### 7.1 字节云云函数部署

```python
# scf_handler.py（字节云入口文件）
from app.main import app

def handler(event, context):
    """
    字节云云函数入口

    Args:
        event: 事件对象
            - http: HTTP请求信息
            - userInfo: 用户信息
    """
    # 处理HTTP请求
    if "http" in event:
        from fastapi.responses import JSONResponse
        from fastapi import Request

        # 构造FastAPI请求
        scope = {
            "type": "http",
            "method": event["http"]["method"],
            "headers": event["http"]["headers"],
            "query_string": event["http"].get("queryString", ""),
            "path": event["http"]["path"]
        }

        # 使用Starlette处理请求
        from starlette.datastructures import Headers
        from starlette.requests import Request as StarletteRequest

        request = StarletteRequest(scope)

        async def get_response():
            return await app.router(request)

        return asyncio.run(get_response())
```

### 7.2 Docker 部署（云托管）

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# 构建和部署
docker build -t tcm-backend .
docker run -d -p 8000:8000 tcm-backend
```

### 7.3 Python 依赖

```txt
# requirements.txt
fastapi==0.110.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6
pydantic==2.5.0
pydantic-settings==2.1.0

# 数据库
sqlalchemy==2.0.25
asyncpg==0.29.0
redis==5.0.1

# 认证
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# HTTP客户端
httpx==0.25.2

# AI/ML（后期）
scikit-learn==1.3.2
joblib==1.3.2
numpy==1.26.3
pillow==10.1.0  # 图像处理

# 工具
python-dotenv==1.0.0
loguru==0.7.2
```

---

## 八、开发计划（产品矩阵版）

### 第一阶段：核心流量+变现（3个月）

| 周次 | 产品 | 任务 | 交付物 |
|-----|-----|-----|-------|
| 1-2 | 体质测试 | 后端API、算法、数据库 | 可测试的后端 |
| 3-4 | 体质测试 | 前端页面、联调 | 完整功能上线 |
| 5-6 | AI舌诊 | 图像识别API、前端 | 舌诊功能 |
| 7-10 | 食疗商城 | 商品管理、订单、支付 | 商城上线 |
| 11-14 | 养生课堂 | 课程管理、视频、进度 | 课程功能 |

### 第二阶段：留存+数据（3个月）

| 周次 | 产品 | 任务 | 交付物 |
|-----|-----|-----|-------|
| 15-18 | 打卡助手 | 任务系统、积分、排行榜 | 打卡功能 |
| 19-22 | 健康档案 | 数据记录、图表、报告 | 档案功能 |
| 23-24 | 穴位地图 | 3D模型、搜索、定位 | 穴位工具 |
| 25-26 | 会员中心 | 会员体系、积分商城 | 会员功能 |

### 第三阶段：扩展+深耕（持续）

| 产品 | 工期 | 核心功能 |
|-----|-----|---------|
| 预约平台 | 6周 | 中医馆查找、在线预约 |
| 中医美容 | 4周 | 美容方案、穴位按摩 |
| 睡眠助手 | 4周 | 助眠工具、数据追踪 |

---

## 九、Python 后端优势总结

| 优势 | 说明 |
|-----|-----|
| **熟悉度高** | 你已熟悉Python，学习成本最低 |
| **FastAPI 2025首选** | 使用率38%，已成主流 |
| **自动文档** | 访问/docs即可看API文档 |
| **类型验证** | Pydantic自动验证，减少bug |
| **AI生态完善** | 舌诊、推荐算法后期扩展容易 |
| **代码简洁** | 比Node.js代码量少30%+ |
| **云函数支持** | 字节云/腾讯云都支持Python 3.10+ |

---

## 十、快速开始

### 初始化项目

```bash
# 1. 创建后端项目
mkdir tcm-backend && cd tcm-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 安装依赖
pip install fastapi uvicorn sqlalchemy asyncpg redis

# 3. 创建项目结构
mkdir -p app/{api/v1,core,models,schemas,services,shared}

# 4. 初始化数据库
createdb tcm_db -U postgres
psql tcm_db < schema.sql

# 5. 运行
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 访问文档

```
API文档: http://localhost:8000/docs
ReDoc:   http://localhost:8000/redoc
健康检查: http://localhost:8000/health
```
