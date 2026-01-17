# 中医体质养生助手 - MVP 开发文档

> 最小可行产品(MVP)开发指南，帮助开发者快速搭建项目

## 目录

- [一、MVP 范围](#一mvp-范围)
- [二、后端开发](#二后端开发)
- [三、前端开发](#三前端开发)
- [四、数据库部署](#四数据库部署)
- [五、联调测试](#五联调测试)
- [六、部署上线](#六部署上线)

---

## 一、MVP 范围

### 1.1 MVP 功能列表

| 模块 | 功能 | 优先级 |
|------|------|--------|
| 体质测试 | 30题精简问卷 | P0 |
| 体质测试 | 智能分析判定 | P0 |
| 结果报告 | 体质特征展示 | P0 |
| 结果报告 | 雷达图可视化 | P0 |
| 饮食推荐 | 宜吃/忌吃食物 | P0 |
| 饮食推荐 | 推荐食谱 | P1 |
| 运动推荐 | 推荐运动类型 | P1 |
| 作息建议 | 睡眠时间和建议 | P1 |

### 1.2 非功能需求

| 需求 | 指标 |
|------|------|
| 响应时间 | API < 500ms |
| 并发用户 | 100+ |
| 可用性 | 99% |
| 测试完成率 | > 70% |

---

## 二、后端开发

### 2.1 环境准备

```bash
# 检查 Python 版本
python --version  # 需要 3.10+

# 创建虚拟环境
cd backend
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2.2 配置环境变量

```bash
# 复制配置文件
cp .env.example .env

# 编辑 .env 文件
vim .env
```

```env
# .env 文件内容
APP_NAME=中医体质养生助手
DEBUG=True

# 数据库配置
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/tcm_db

# Redis 配置
REDIS_URL=redis://localhost:6379/0

# JWT 配置
SECRET_KEY=your-secret-key-here
```

### 2.3 启动开发服务器

```bash
# 方式一：直接启动
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 方式二：使用启动脚本
python -m uvicorn app.main:app --reload
```

访问 http://localhost:8000/docs 查看 API 文档

### 2.4 API 测试

```bash
# 获取问卷题目
curl http://localhost:8000/api/v1/constitution/quiz/questions

# 提交问卷
curl -X POST http://localhost:8000/api/v1/constitution/quiz/submit \
  -H "Content-Type: application/json" \
  -d '{"answers": [1,2,3,4,5,3,2,1,4,3,2,1,5,4,3,2,1,4,3,2,1,5,4,3,2,1,4,3,2,1,5]}'

# 获取推荐
curl http://localhost:8000/api/v1/recommendation/qi_deficiency
```

---

## 三、前端开发

### 3.1 环境准备

```bash
# 检查 Node.js 版本
node --version  # 需要 16+
npm --version

# 安装 HBuilderX（推荐）
# 下载地址：https://www.dcloud.io/hbuilderx.html

# 或使用命令行
cd frontend/miniprogram
npm install
```

### 3.2 配置 API 地址

```javascript
// frontend/miniprogram/src/utils/config.js
export const CONFIG = {
  API_BASE: 'http://localhost:8000/api/v1',  // 开发环境
  // API_BASE: 'https://api.example.com/api/v1',  // 生产环境
}
```

### 3.3 运行小程序

**使用 HBuilderX：**
1. 打开 HBuilderX
2. 文件 → 打开目录 → 选择 `frontend/miniprogram`
3. 运行 → 运行到小程序模拟器 → 微信开发者工具
4. 运行 → 运行到小程序模拟器 → 抖音开发者工具

**使用命令行：**
```bash
# 微信小程序
npm run dev:mp-weixin

# 抖音小程序
npm run dev:mp-toutiao
```

### 3.4 页面结构

```
pages/
├── index/          # 首页
│   └── index.vue   # 介绍、入口、体质介绍
├── quiz/           # 测试页
│   └── quiz.vue    # 问卷答题
├── result/         # 结果页
│   └── result.vue  # 体质报告
└── recommendation/ # 推荐页
    └── recommendation.vue  # 养生方案
```

---

## 四、数据库部署

### 4.1 Docker 部署（推荐）

```bash
# 启动 PostgreSQL 和 Redis
docker-compose up -d
```

`docker-compose.yml`:
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: tcm_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### 4.2 本地安装

**macOS:**
```bash
brew install postgresql@15 redis
brew services start postgresql@15
brew services start redis
```

**Ubuntu:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib redis-server
sudo systemctl start postgresql
sudo systemctl start redis
```

**Windows:**
下载安装包：
- PostgreSQL: https://www.postgresql.org/download/windows/
- Redis: https://github.com/microsoftarchive/redis/releases

### 4.3 初始化数据库

```bash
# 创建数据库
createdb tcm_db -U postgres

# 初始化表结构
psql -U postgres -d tcm_db -f database/init.sql

# 或使用 Python 脚本
python -c "from app.core.database import init_db; init_db()"
```

---

## 五、联调测试

### 5.1 测试流程

```
1. 启动后端服务
   ↓
2. 启动数据库
   ↓
3. 启动小程序
   ↓
4. 完整流程测试
```

### 5.2 测试用例

| 用例 | 步骤 | 预期结果 |
|------|------|----------|
| 完整测试流程 | 1. 打开小程序<br>2. 点击开始测试<br>3. 完成30题<br>4. 查看结果<br>5. 查看推荐 | 正常完成，结果准确 |
| 网络异常 | 断网后提交问卷 | 显示错误提示 |
| 答案不完整 | 未完成所有题目 | 提示完成剩余题目 |
| 重新测试 | 再次完成测试 | 覆盖旧结果 |

### 5.3 常见问题

**问题1：API 请求失败**
```
检查项：
1. 后端服务是否启动
2. API 地址是否正确
3. 小程序域名是否白名单
```

**问题2：数据库连接失败**
```
检查项：
1. PostgreSQL 是否启动
2. 连接字符串是否正确
3. 防火墙是否阻止
```

---

## 六、部署上线

### 6.1 后端部署

**字节云 Serverless:**
```bash
# 安装字节云 CLI
npm install -g @bytedance/serverless-cli

# 部署
serverless deploy
```

**云托管 CloudRun:**
```bash
# 构建 Docker 镜像
docker build -t tcm-backend .

# 推送到镜像仓库
docker tag tcm-backend registry.cn-hangzhou.cr.aliyuncs.com/tcm/backend
docker push registry.cn-hangzhou.cr.aliyuncs.com/tcm/backend

# 部署到云托管
```

### 6.2 前端部署

**抖音小程序:**
1. 登录 [抖音开放平台](https://developer.open-douyin.com/)
2. 创建小程序，获取 AppID
3. 配置服务器域名白名单
4. 上传代码
5. 提交审核

**微信小程序:**
1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 配置 AppID
3. 上传代码
4. 提交审核

### 6.3 环境变量配置

生产环境 `.env`:
```env
APP_NAME=中医体质养生助手
DEBUG=False
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/tcm_db
REDIS_URL=redis://host:6379/0
SECRET_KEY=production-secret-key
```

### 6.4 监控和日志

```python
# 日志监控
from loguru import logger

logger.add("logs/app.log", rotation="500 MB", compression="zip")

# 性能监控
from prometheus_client import Counter, Histogram

request_count = Counter('http_requests_total', 'Total requests')
request_duration = Histogram('http_request_duration_seconds', 'Request duration')
```

---

## 七、开发规范

### 7.1 代码规范

**Python:**
- 遵循 PEP 8
- 使用类型注解
- 编写 docstring

```python
async def analyze_constitution(answers: List[int]) -> Dict:
    """
    分析体质类型

    Args:
        answers: 用户答案列表

    Returns:
        体质分析结果
    """
    pass
```

**Vue:**
- 使用 Composition API
- 组件命名使用 PascalCase
- 样式使用 scoped

```vue
<script setup>
import { ref } from 'vue'

const count = ref(0)
</script>

<style scoped>
.container {
  padding: 30rpx;
}
</style>
```

### 7.2 Git 工作流

```bash
# 功能开发
git checkout -b feature/quiz-page

# 提交代码
git add .
git commit -m "feat: 添加问卷页面"

# 推送分支
git push origin feature/quiz-page

# 创建 Pull Request
```

**提交消息规范:**
```
feat: 新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试
chore: 构建/工具
```

---

## 八、项目时间表

| 阶段 | 任务 | 时间 |
|------|------|------|
| Week 1 | 后端 API 开发 | 3-4 天 |
| Week 2 | 前端页面开发 | 3-4 天 |
| Week 3 | 联调测试 | 2-3 天 |
| Week 4 | 部署上线 | 1-2 天 |

---

## 九、联系与支持

- **文档**: https://github.com/hafzhang/traditional_chinese_medicine
- **Issues**: https://github.com/hafzhang/traditional_chinese_medicine/issues
- **技术支持**: hafzhang@example.com

---

*文档版本: v1.0*
*最后更新: 2025年*
