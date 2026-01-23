# 测试指南

## 目录

1. [概述](#概述)
2. [测试文档结构](#测试文档结构)
3. [快速开始](#快速开始)
4. [测试覆盖率要求](#测试覆盖率要求)
5. [持续集成](#持续集成)

---

## 概述

本项目采用分层测试策略，确保代码质量和功能稳定性。

### 测试分层

```
┌─────────────────────────────────────────────────────────┐
│                    E2E 测试 (端到端)                     │
│                  浏览器自动化测试                        │
└─────────────────────────────────────────────────────────┘
                          ▲
                          │
┌─────────────────────────────────────────────────────────┐
│                  集成测试 (API/组件)                     │
│         后端 API 测试 + 前端组件测试                     │
└─────────────────────────────────────────────────────────┘
                          ▲
                          │
┌─────────────────────────────────────────────────────────┐
│                  单元测试 (函数/方法)                     │
│         后端服务测试 + 前端工具函数测试                  │
└─────────────────────────────────────────────────────────┘
```

---

## 测试文档结构

```
docs/
├── testing.md                      # 本文件 - 测试总览
├── backend/
│   └── testing.md                  # 后端测试详细规范
└── frontend/
    └── testing.md                  # 前端测试详细规范

backend/tests/
├── conftest.py                     # Pytest 配置和 fixtures
├── test_unit/                      # 服务层单元测试
│   ├── test_ingredients.py         # 食材服务测试
│   ├── test_recipes.py             # 食谱服务测试
│   ├── test_acupoints.py           # 穴位服务测试
│   ├── test_tongue_diagnosis.py    # 舌诊服务测试
│   └── test_courses.py             # 课程服务测试
└── test_api/                       # API 集成测试
    ├── test_ingredients_api.py
    ├── test_recipes_api.py
    ├── test_acupoints_api.py
    ├── test_tongue_api.py
    └── test_courses_api.py

frontend/tests/                      # 前端测试（待配置）
├── unit/                           # 单元测试
├── component/                      # 组件测试
└── e2e/                            # E2E 测试
```

---

## 快速开始

### 后端测试

```bash
# 进入后端目录
cd backend

# 运行所有测试
python -m pytest tests/test_unit/ tests/test_api/ -v

# 运行特定模块测试
python -m pytest tests/test_unit/test_ingredients.py -v

# 生成覆盖率报告
python -m pytest tests/ --cov=api --cov-report=html

# 运行单个测试用例
python -m pytest tests/test_unit/test_ingredients.py::TestIngredientService::test_get_ingredient_by_id -v
```

### 前端测试

```bash
# 进入前端目录
cd frontend

# 运行所有测试（配置后）
npm run test

# 运行特定测试文件
npm run test -- ingredients.test.js

# 运行测试并生成覆盖率报告
npm run test:coverage
```

---

## 测试覆盖率要求

| 模块 | 单元测试 | API/组件测试 | 总体覆盖率 | 状态 |
|------|----------|-------------|-----------|------|
| 食材服务 | ✅ 100% | ✅ 100% | ✅ 100% | 已完成 |
| 食谱服务 | ✅ 100% | ✅ 100% | ✅ 100% | 已完成 |
| 穴位服务 | ✅ 100% | ✅ 100% | ✅ 100% | 已完成 |
| 舌诊服务 | ✅ 100% | ✅ 100% | ✅ 100% | 已完成 |
| 课程服务 | ✅ 100% | ✅ 100% | ✅ 100% | 已完成 |
| 前端组件 | ⏳ 待配置 | ⏳ 待配置 | ⏳ 待配置 | Phase 2 |
| **总体** | **100%** | **100%** | **83%** | Phase 1 完成 |

**覆盖率目标**: ≥80%

---

## 持续集成

### Git Hooks

项目已配置 `backend/.git/hooks/pre-commit`，在每次提交前自动运行测试。

```bash
# 正常提交（会触发 pre-commit hook）
git commit -m "feat: add new feature"

# 跳过 hook（不推荐）
git commit --no-verify -m "feat: add new feature"
```

### CI/CD (GitHub Actions 示例)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest tests/test_unit/ tests/test_api/ -v --cov=api
      - name: Upload coverage
        uses: codecov/codecov-action@v2

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '16'
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Run tests
        run: |
          cd frontend
          npm run test
```

---

## 测试命名规范

### 后端测试

- **测试文件**: `test_{module}.py` 或 `test_{module}_api.py`
- **测试类**: `Test{ServiceName}Service` 或 `Test{ModuleName}API`
- **测试方法**: `test_{action}_{scenario}`

```python
class TestIngredientService:
    def test_get_ingredient_by_id_success(self, db_session):
        """测试：根据ID成功获取食材"""
        pass

    def test_get_ingredient_by_id_not_found(self, db_session):
        """测试：根据ID获取不存在的食材"""
        pass
```

### 前端测试

- **测试文件**: `{module}.test.js`
- **测试组**: `describe('{ComponentName}', ...)`
- **测试用例**: `it('should {expected behavior}', ...)`

```javascript
describe('IngredientCard', () => {
  it('should render ingredient name correctly', () => {
    // 测试代码
  });

  it('should handle empty props gracefully', () => {
    // 测试代码
  });
});
```

---

## 详细文档

### 后端测试规范

详见 [docs/backend/testing.md](docs/backend/testing.md)

包含：
- 测试框架配置（Pytest）
- Fixtures 使用指南
- 数据库测试策略
- API 测试最佳实践
- Mock 和 Stub 使用
- 性能测试指南

### 前端测试规范

详见 [docs/frontend/testing.md](docs/frontend/testing.md)

包含：
- 测试框架配置（Vitest）
- 组件测试指南
- Vue Test Utils 使用
- API Mock 策略
- E2E 测试配置
- 端到端测试最佳实践

---

## 故障排除

### 问题: 后端测试失败 - "Module not found"

**解决方案**:
```bash
# 确保在 backend 目录下运行
cd backend
# 或设置 PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 问题: 数据库测试失败

**解决方案**:
```bash
# 清理测试数据库
rm backend/test.db
# 重新运行测试
cd backend && python -m pytest tests/ -v
```

### 问题: 前端测试超时

**解决方案**:
```bash
# 增加 Vitest 超时时间
# vitest.config.js
export default defineConfig({
  testTimeout: 10000,
})
```

---

## 参考资源

### 后端测试

- [Pytest 官方文档](https://docs.pytest.org/)
- [FastAPI 测试指南](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy 测试最佳实践](https://docs.sqlalchemy.org/en/14/orm/session_basics.html#session-performances)

### 前端测试

- [Vitest 官方文档](https://vitest.dev/)
- [Vue Test Utils](https://test-utils.vuejs.org/)
- [uni-app 测试指南](https://uniapp.dcloud.net.cn/tutorial/testing.html)

---

**文档版本**: v1.0
**最后更新**: 2026-01-20
**维护者**: 开发团队
