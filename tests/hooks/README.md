# Claude Code Hooks 测试套件

## 中医体质识别 MVP 项目

---

## 目录

- [概述](#概述)
- [快速开始](#快速开始)
- [测试说明](#测试说明)
- [测试脚本](#测试脚本)
- [测试数据](#测试数据)
- [故障排除](#故障排除)

---

## 概述

本测试套件用于验证 Claude Code hooks 的功能、性能和可靠性。

### 测试覆盖

| 测试类型 | 脚本 | 描述 |
|---------|-----|-----|
| 功能测试 | `run_all_tests.sh` | 验证所有 hooks 的基本功能 |
| 性能测试 | `performance_test.sh` | 测试每个 hook 的执行时间 |
| 并发测试 | `concurrent_test.sh` | 测试并发执行场景 |
| 日志测试 | `log_size_test.sh` | 测试日志文件大小控制 |

---

## 快速开始

### 1. 准备环境

```bash
# 确保在项目根目录
cd /path/to/traditional_chinese_medicine

# 确保脚本有执行权限
chmod +x scripts/hooks/*.sh
chmod +x tests/hooks/*.sh

# 安装必要工具
sudo apt-get install bc jq  # Linux
brew install bc jq           # macOS
```

### 2. 运行所有测试

```bash
# 运行完整测试套件
./tests/hooks/run_all_tests.sh

# 预期输出
# ======================================
# Claude Code Hooks Test Suite
# ======================================
#
# === Pre-Command Hooks (3 tests) ===
#   Running: TC-ENV-001: Normal environment check ... PASSED
# ...
#
# ======================================
# Test Summary
# ======================================
# Total Tests:  30
# Passed:       30
# Failed:       0
#
# ✅ All tests passed!
```

### 3. 运行单独测试

```bash
# 性能测试
./tests/hooks/performance_test.sh

# 并发测试
./tests/hooks/concurrent_test.sh

# 日志大小测试
./tests/hooks/log_size_test.sh
```

---

## 测试说明

### 功能测试 (run_all_tests.sh)

运行所有 hooks 的功能验证测试，确保每个 hook 按预期工作。

**测试内容**:
- 环境检查
- 请求日志记录
- 功能检测
- MVP 范围检查
- 代码验证
- API 命名检查
- 错误处理

**预期时间**: ~10 秒

---

### 性能测试 (performance_test.sh)

测量每个 hook 的执行时间，识别性能瓶颈。

**性能阈值**:
- ✅ OK: < 100ms
- ⚠️ WARNING: ≥ 100ms
- ⚠️⚠️ CRITICAL: ≥ 500ms

**预期输出**:
```
Hook Name                            Time (ms) Status
----------------------------------- ---------- ----------
check_environment                         45 OK
log_user_request                          5 OK
detect_feature                            8 OK
...
```

---

### 并发测试 (concurrent_test.sh)

测试多个 hooks 并发执行时的行为。

**配置**:
- 并发任务数: 20
- 总请求数: 100

**验证点**:
- 数据完整性（无重复）
- 日志格式正确
- 高成功率（≥95%）

---

### 日志测试 (log_size_test.sh)

验证日志文件大小限制机制。

**测试**:
- 生成 1500 条日志（超过限制）
- 验证日志被正确裁剪

---

## 测试数据

### Fixtures 目录

```
tests/fixtures/
├── sample_valid.py      # 有效的 Python 文件
├── sample_invalid.py    # 无效的 Python 文件
├── sample_migration.sql # 有效的 SQL 迁移文件
└── sample_api.py        # 符合规范的 API 文件
```

### Temp 目录

```
tests/temp/
└── (临时测试文件，运行时生成)
```

---

## 故障排除

### 问题: 测试失败 - "command not found: jq"

**解决方案**:
```bash
# Ubuntu/Debian
sudo apt-get install jq

# macOS
brew install jq
```

### 问题: 权限拒绝

**解决方案**:
```bash
# 给脚本添加执行权限
chmod +x scripts/hooks/*.sh
chmod +x tests/hooks/*.sh
```

### 问题: 日志文件不存在

**解决方案**:
```bash
# 创建日志目录
mkdir -p .claude/hooks
```

### 问题: Hook 执行超时

**解决方案**:
```bash
# 检查系统负载
top

# 单独运行性能测试，找出慢的 hook
./tests/hooks/performance_test.sh

# 优化或禁用慢的 hook
```

---

## 清理测试数据

```bash
# 清理日志文件
rm -f .claude/hooks/*.log

# 清理临时文件
rm -rf tests/temp/*

# 清理测试生成的文件
rm -f .claude/mvp_checklist.json .claude/progress.json
```

---

## 持续集成

### GitHub Actions 示例

```yaml
name: Hooks Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y bc jq
      - name: Run hooks tests
        run: ./tests/hooks/run_all_tests.sh
      - name: Run performance tests
        run: ./tests/hooks/performance_test.sh
```

---

## 开发指南

### 添加新测试

1. 在 `run_all_tests.sh` 中添加测试函数
2. 使用 `run_test` 辅助函数
3. 更新测试计数

```bash
run_test "TC-NEW-001: New test case" \
    "bash scripts/hooks/new_hook.sh"
```

### 调试单个 Hook

```bash
# 设置环境变量
export CLAUDE_USER_PROMPT="test"
export CLAUDE_SESSION_ID="debug-test"

# 直接运行 hook 脚本
bash -x scripts/hooks/log_request.sh

# 查看日志
cat .claude/hooks/requests.log | tail -1
```

---

## 联系

如有问题或建议，请联系开发团队。

---

*测试套件版本: v1.0*
*最后更新: 2025-01-13*
