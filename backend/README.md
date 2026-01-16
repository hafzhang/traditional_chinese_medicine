# Constitution Recognition Backend

中医体质识别 MVP 后端服务

## 技术栈

- **Python 3.10+**
- **FastAPI** - Web 框架
- **SQLAlchemy** - ORM
- **PostgreSQL** - 数据库
- **Pydantic** - 数据验证

## 项目结构

```
backend/
├── main.py                 # 应用入口
├── requirements.txt        # Python 依赖
├── .env.example           # 环境变量示例
├── api/
│   ├── config.py          # 配置管理
│   ├── database.py        # 数据库连接
│   ├── models/            # 数据库模型
│   │   └── __init__.py    # User, Question, ConstitutionResult, Food, Recipe, ConstitutionInfo
│   ├── schemas/           # Pydantic 模型
│   │   └── constitution.py
│   ├── services/          # 业务逻辑
│   │   └── constitution.py
│   ├── routers/           # API 路由
│   │   ├── constitution.py
│   │   └── health.py
│   └── data/              # 静态数据
│       ├── questions.py   # 30个问题
│       ├── foods.py       # 食物库
│       └── constitution_info.py  # 体质信息
└── scripts/
    └── seed_db.py         # 数据库初始化脚本
```

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库连接等
```

### 3. 启动 PostgreSQL 数据库

确保 PostgreSQL 已安装并运行，创建数据库：

```bash
createdb constitution_db
```

### 4. 初始化数据库

```bash
python scripts/seed_db.py
```

这将创建所有表并种子初始数据：
- 30个测试问题
- 90+条食物数据
- 示例食谱
- 9种体质信息

### 5. 启动服务

```bash
python main.py
```

或使用 uvicorn：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

服务将在 http://localhost:8000 启动

API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 接口

### 健康检查

- `GET /health` - 健康检查
- `GET /ping` - 简单 ping

### 体质测试

- `POST /api/v1/test/submit` - 提交测试
- `GET /api/v1/result/{result_id}` - 获取结果
- `GET /api/v1/recommend/food?constitution=xxx` - 饮食推荐
- `GET /api/v1/questions` - 获取问题列表

## 体质评分算法

### 评分规则

1. **原始分计算**：将各体质对应问题的答案分数相加
2. **百分制转换**：原始分 × 2.5 = 百分制分数
3. **体质判定**：
   - 平和质：≥60分 且 其他8种体质均<40分
   - 主要体质：分数最高的体质
   - 次要体质：≥30分的其他体质

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

## 开发说明

### 数据库模型

- **User**: 用户表（支持抖音、微信、匿名用户）
- **Question**: 测试题目（30题）
- **ConstitutionResult**: 测试结果
- **Food**: 食物库
- **Recipe**: 食谱库
- **ConstitutionInfo**: 体质信息（静态数据）

### 配置说明

在 `.env` 文件中可以调整以下参数：

- `SCORE_CONVERT_FACTOR`: 分数转换系数（默认 2.5）
- `THRESHOLD_PRIMARY`: 主要体质阈值（默认 40）
- `THRESHOLD_SECONDARY`: 次要体质阈值（默认 30）
- `THRESHOLD_PEACE`: 平和质阈值（默认 60）

## 测试

```bash
# 运行测试（需要先安装 pytest）
pip install pytest pytest-asyncio
pytest
```

## 部署

### 使用 Docker

```bash
docker build -t constitution-api .
docker run -p 8000:8000 constitution-api
```

### 使用 systemd

创建 `/etc/systemd/system/constitution-api.service`:

```ini
[Unit]
Description=Constitution Recognition API
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

## License

MIT
