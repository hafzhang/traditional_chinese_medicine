# 中医体质识别 MVP

基于王琦院士 CCMQ 标准量表的中医体质识别应用，支持快速测试、体质分析和个性化饮食推荐。

## 项目概述

本项目是一个完整的中医体质识别解决方案，包含后端 API 服务和跨平台前端应用。用户通过 30 题精简问卷快速识别自身体质类型，并获得详细的体质分析和个性化养生建议。

### 核心功能

- **快速体质测试**: 30 题 CCMQ 标准量表，5-8 分钟完成
- **智能体质判定**: 基于 9 种体质类型的科学判定算法
- **详细体质报告**: 体质特征、调理原则、饮食建议
- **个性化饮食推荐**: 根据体质推荐宜/忌食物和食谱
- **跨平台支持**: 微信小程序、抖音小程序、H5

## 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                        前端层                                │
│  uni-app (Vue 3) - 微信小程序 / 抖音小程序 / H5               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ↓ HTTP API
┌─────────────────────────────────────────────────────────────┐
│                        后端层                                │
│  FastAPI + SQLAlchemy + Pydantic                            │
│  • 体质分析服务  • 饮食推荐  • 用户管理                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        数据层                                │
│  PostgreSQL - 用户 / 问题 / 结果 / 食物 / 食谱               │
└─────────────────────────────────────────────────────────────┘
```

## 项目结构

```
traditional_chinese_medicine/
├── backend/                 # 后端服务
│   ├── main.py             # 应用入口
│   ├── requirements.txt    # Python 依赖
│   ├── .env.example        # 环境变量示例
│   ├── api/                # API 模块
│   │   ├── config.py       # 配置管理
│   │   ├── database.py     # 数据库连接
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic 模型
│   │   ├── services/       # 业务逻辑
│   │   ├── routers/        # API 路由
│   │   └── data/           # 静态数据
│   ├── scripts/            # 脚本
│   │   └── seed_db.py      # 数据库初始化
│   └── README.md
│
├── frontend/               # 前端应用
│   ├── package.json        # Node 依赖
│   ├── vite.config.js      # Vite 配置
│   ├── src/
│   │   ├── pages/          # 页面
│   │   ├── api/            # API 封装
│   │   ├── utils/          # 工具函数
│   │   └── styles/         # 全局样式
│   └── README.md
│
└── docs/                   # 文档
    └── constitution_recognition_mvp.md
```

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 16+
- PostgreSQL 14+
- Redis (可选)

### 1. 数据库设置

```bash
# 创建数据库
createdb constitution_db

# 配置环境变量
cd backend
cp .env.example .env
# 编辑 .env 文件，设置数据库连接
```

### 2. 后端服务

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python scripts/seed_db.py

# 启动服务
python main.py
```

后端服务将运行在 `http://localhost:8000`

API 文档: `http://localhost:8000/docs`

### 3. 前端应用

```bash
cd frontend

# 安装依赖
npm install

# 开发运行 (H5)
npm run dev:h5

# 开发运行 (微信小程序)
npm run dev:mp-weixin
```

## API 接口

### 健康检查
- `GET /health` - 服务健康状态
- `GET /ping` - 快速 ping

### 体质测试
- `GET /api/v1/questions` - 获取测试题目
- `POST /api/v1/test/submit` - 提交测试答案
- `GET /api/v1/result/{result_id}` - 获取测试结果
- `GET /api/v1/recommend/food` - 获取饮食推荐

## 体质评分算法

### 评分规则

1. **原始分计算**: 将各体质对应问题的答案分数相加
2. **百分制转换**: 原始分 × 2.5 = 百分制分数
3. **体质判定**:
   - 平和质: ≥60分 且 其他8种体质均<40分
   - 主要体质: 分数最高的体质
   - 次要体质: ≥30分的其他体质

### 问题与体质对应

| 问题 | 体质类型 | 题数 |
|------|----------|------|
| 1-4 | 平和质 | 4 |
| 5-8 | 气虚质 | 4 |
| 9-12 | 阳虚质 | 4 |
| 13-16 | 阴虚质 | 4 |
| 17-19 | 痰湿质 | 3 |
| 20-22 | 湿热质 | 3 |
| 23-25 | 血瘀质 | 3 |
| 26-28 | 气郁质 | 3 |
| 29-30 | 特禀质 | 2 |

## 九种体质类型

| 英文标识 | 中文名称 | 调理原则 |
|---------|---------|---------|
| peace | 平和质 | 保持健康，协调平衡 |
| qi_deficiency | 气虚质 | 补气健脾 |
| yang_deficiency | 阳虚质 | 温补阳气 |
| yin_deficiency | 阴虚质 | 滋阴清热 |
| phlegm_damp | 痰湿质 | 化痰祛湿 |
| damp_heat | 湿热质 | 清热利湿 |
| blood_stasis | 血瘀质 | 活血化瘀 |
| qi_depression | 气郁质 | 疏肝理气 |
| special | 特禀质 | 益气固表 |

## 开发说明

### 后端开发

```bash
cd backend

# 运行测试
pytest

# 代码格式化
black api/
```

### 前端开发

```bash
cd frontend

# H5 开发
npm run dev:h5

# 微信小程序开发
npm run dev:mp-weixin

# 构建
npm run build:h5
npm run build:mp-weixin
```

## 部署

### Docker 部署

```bash
# 构建后端镜像
docker build -t constitution-api backend

# 运行容器
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  constitution-api
```

### 云平台部署

- **字节云 Serverless**: 适合小程序场景
- **腾讯云/阿里云**: 适合高并发场景
- **Docker + K8s**: 适合企业级部署

## 免责声明

本产品提供的体质识别和养生建议仅供参考，不构成医疗诊断和治疗方案。如有疾病或严重健康问题，请及时就医。

## License

MIT

## 联系方式

如有问题或建议，欢迎提交 Issue。
