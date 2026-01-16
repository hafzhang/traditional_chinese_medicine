# 测试指南

## 📋 测试概述

本项目包含完整的测试套件，覆盖九种体质识别的核心算法、API 端点和前端功能。

## 🧪 测试类型

### 1. 后端测试 (Python/pytest)

#### 体质评分算法测试
- 文件: `backend/tests/test_constitution_scorer.py`
- 覆盖内容:
  - 原始分数计算
  - 百分制转换
  - 体质类型判定
  - 九种体质的标准测试用例
  - 边界条件处理

#### API 端点测试
- 文件: `backend/tests/test_api_endpoints.py`
- 覆盖内容:
  - 健康检查端点
  - 获取问题列表
  - 提交测试答案
  - 获取测试结果
  - 饮食推荐
  - 完整流程集成测试

### 2. 前端测试 (JavaScript)

#### 浏览器测试
- 文件: `frontend/tests/constitution.test.js`
- 可直接在浏览器控制台运行
- 包含与后端相同的测试用例

## 🚀 运行测试

### 方式1: 使用测试脚本

```bash
# 运行所有测试
./scripts/run_tests.sh --all

# 仅运行后端测试
./scripts/run_tests.sh --backend

# 仅运行评分算法测试
./scripts/run_tests.sh --scoring

# 生成覆盖率报告
./scripts/run_tests.sh --backend --cov
```

### 方式2: 直接使用 pytest

```bash
cd backend

# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_constitution_scorer.py -v

# 运行特定测试类
pytest tests/test_constitution_scorer.py::TestConstitutionScorer -v

# 运行特定测试方法
pytest tests/test_constitution_scorer.py::TestConstitutionScorer::test_calculate_scores_all_ones -v

# 生成覆盖率报告
pytest tests/ --cov=api --cov-report=html
```

### 方式3: 浏览器前端测试

1. 在浏览器中打开前端页面
2. 打开开发者工具控制台 (F12)
3. 加载测试文件:
```javascript
// 方法1: 直接在控制台粘贴测试代码
// 复制 frontend/tests/constitution.test.js 的内容到控制台

// 方法2: 通过 script 标签加载
// 在 index.html 中添加:
// <script src="/tests/constitution.test.js"></script>
```

4. 运行测试:
```javascript
runConstitutionTests()
```

## 🔧 安装 Git Hooks

Git hooks 会在代码提交前自动运行测试，确保代码质量。

```bash
# 安装 hooks
./scripts/install_hooks.sh

# 手动运行 pre-commit 测试
.git/hooks/pre-commit

# 跳过 hooks (临时)
git commit --no-verify -m "message"
```

## 📊 测试覆盖率

目标覆盖率: 80%

查看覆盖率报告:
```bash
# 生成 HTML 报告
pytest tests/ --cov=api --cov-report=html

# 在浏览器中打开
open backend/htmlcov/index.html  # macOS
xdg-open backend/htmlcov/index.html  # Linux
start backend/htmlcov/index.html  # Windows
```

## 📝 测试用例说明

### 标准体质测试用例

基于王琦院士 CCMQ 标准的九种体质判定:

| 用例 | 描述 | 预期结果 |
|------|------|----------|
| 典型平和质 | 精力充沛、面色红润、睡眠良好 | 判定为平和质 |
| 典型气虚质 | 容易疲乏、气短、容易感冒 | 判定为气虚质 |
| 典型阳虚质 | 手脚发凉、怕冷、吃凉东西不舒服 | 判定为阳虚质 |
| 典型阴虚质 | 口干咽燥、手心脚心发热、皮肤干 | 判定为阴虚质 |
| 典型痰湿质 | 胸闷腹胀、身体沉重、腹部肥满 | 判定为痰湿质 |
| 典型湿热质 | 面部油腻、容易生痤疮、口苦 | 判定为湿热质 |
| 典型血瘀质 | 皮肤瘀斑、两颧红丝、疼痛固定 | 判定为血瘀质 |
| 典型气郁质 | 情绪低沉、精神紧张、爱叹气 | 判定为气郁质 |
| 典型特禀质 | 没感冒也打喷嚏、流鼻涕 | 判定为特禀质 |
| 气虚阳虚混合 | 气虚和阳虚症状都明显 | 混合体质 |

### 边界条件测试

- 答案数量不正确 (非30个)
- 答案值超出范围 (非1-5)
- 所有答案相同
- 分数达到最大值
- 无体质达到阈值

## 🐛 调试测试

### 查看详细输出

```bash
pytest tests/ -v -s  # -s 显示 print 输出
pytest tests/ -vv    # -vv 更详细的输出
pytest tests/ --tb=long  # 完整的 tracebacks
```

### 只运行失败的测试

```bash
pytest tests/ --lf  # --last-failed
```

### 运行特定标记的测试

```bash
pytest tests/ -m constitution  # 只运行体质相关测试
pytest tests/ -m "not slow"    # 跳过慢速测试
```

## 📚 测试最佳实践

1. **隔离性**: 每个测试独立运行，不依赖其他测试
2. **幂等性**: 多次运行结果一致
3. **快速**: 单元测试应在秒级完成
4. **清晰**: 测试名称清楚描述测试内容
5. **覆盖**: 覆盖正常路径和异常情况

## 🔗 相关文档

- [CCMQ 标准](https://www.cm.org.cn/) - 中国中医药管理局
- [体质分类标准](https://www.cm.org.cn/attached/file/20170927/20170927164016146.pdf)

## 🤝 贡献测试

添加新测试时:
1. 在对应测试文件中添加测试函数
2. 使用清晰的测试名称
3. 包含正常和异常情况
4. 更新此文档
