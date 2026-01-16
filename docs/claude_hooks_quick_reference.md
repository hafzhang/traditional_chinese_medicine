# Claude Code Hooks 快速参考指南

## 中医体质识别 MVP 项目

---

## 概述

本文档提供了 Claude Code hooks 的快速参考信息，包括每个 hook 的用途、触发时机和快速测试命令。

---

## Hooks 一览

### 1. Pre-Command Hooks

| Hook 名称 | 触发时机 | 用途 |
|-----------|---------|-----|
| `check_environment` | 执行任何命令前 | 验证 Python 版本和必需文件 |

**快速测试**:
```bash
bash scripts/hooks/check_env.sh
```

---

### 2. User-Prompt-Submit Hooks

| Hook 名称 | 触发时机 | 用途 |
|-----------|---------|-----|
| `log_user_request` | 用户提交提示词 | 记录所有用户请求 |
| `detect_feature` | 用户提交提示词 | 检测并分类功能请求 |
| `check_mvp_scope` | 用户提交提示词 | 警告超出 MVP 范围的请求 |

**快速测试**:
```bash
# 测试日志记录
export CLAUDE_USER_PROMPT="实现体质测试问卷"
bash scripts/hooks/log_request.sh

# 测试功能检测
export CLAUDE_USER_PROMPT="添加用户登录功能"
bash scripts/hooks/detect_feature.sh

# 测试 MVP 范围检查（在范围内）
export CLAUDE_USER_PROMPT="实现问卷提交接口"
bash scripts/hooks/check_mvp_scope.sh

# 测试 MVP 范围检查（超出范围）
export CLAUDE_USER_PROMPT="添加积分商城功能"
bash scripts/hooks/check_mvp_scope.sh
```

---

### 3. Tool-Use Hooks

| Hook 名称 | 触发条件 | 用途 |
|-----------|---------|-----|
| `validate_python_code` | 写入 *.py 文件 | 验证 Python 语法 |
| `validate_sql_schema` | 写入 *migration*.sql | 验证 SQL schema |
| `auto_fix_sql` | SQL 验证失败 | 自动修复 SQL 问题 |
| `track_file_changes` | Write/Edit 操作 | 跟踪文件变更 |
| `check_api_endpoint` | 写入 api/* 文件 | 验证 API 命名规范 |
| `run_relevant_tests` | Write/Edit 后 | 运行测试并自动修复 |

**快速测试**:
```bash
# 测试 Python 验证（有效文件）
export CLAUDE_TOOL_INPUT_FILE_PATH="tests/fixtures/sample_valid.py"
bash scripts/hooks/validate_python.sh

# 测试文件变更跟踪
export CLAUDE_TOOL_NAME="Write"
export CLAUDE_TOOL_INPUT_FILE_PATH="backend/test.py"
bash scripts/hooks/track_changes.sh

# 测试 API 命名检查
export CLAUDE_TOOL_INPUT_FILE_PATH="backend/api/test.py"
bash scripts/hooks/check_api_naming.sh

# 测试 SQL 自动修复
cat > tests/temp/test.sql << 'EOF'
CREATE TABLE test (id INT);
EOF
export CLAUDE_TOOL_INPUT_FILE_PATH="tests/temp/test.sql"
bash scripts/hooks/auto_fix_sql.sh

# 测试集成测试+自动修复
export CLAUDE_TOOL_INPUT_FILE_PATH="tests/fixtures/sample_valid.py"
bash scripts/hooks/run_relevant_tests.sh
```

---

### 4. Pre-Response Hooks

| Hook 名称 | 触发时机 | 用途 |
|-----------|---------|-----|
| `check_response_length` | 生成响应前 | 警告过长响应 |
| `verify_task_completion` | 生成响应前 | 显示 MVP 进度 |

**快速测试**:
```bash
# 测试响应长度检查
export CLAUDE_RESPONSE="A short response"
bash scripts/hooks/check_response.sh

# 测试任务完成验证
bash scripts/hooks/verify_completion.sh
```

---

### 5. Post-Response Hooks

| Hook 名称 | 触发时机 | 用途 |
|-----------|---------|-----|
| `log_session_summary` | 响应完成后 | 记录会话摘要和 token 使用 |
| `update_progress` | 响应完成后 | 更新 MVP 进度 |

**快速测试**:
```bash
# 测试会话日志
export CLAUDE_SESSION_ID="test-001"
export CLAUDE_TOKENS_USED=5000
bash scripts/hooks/log_session.sh

# 测试进度更新
bash scripts/hooks/update_progress.sh
```

---

### 6. Error Hooks

| Hook 名称 | 触发时机 | 用途 |
|-----------|---------|-----|
| `log_error` | 发生错误时 | 记录错误详情 |
| `suggest_fix` | 发生错误时 | 建议修复方案 |
| `auto_fix_on_error` | 特定错误类型 | 自动修复错误 |

**快速测试**:
```bash
# 测试错误日志
export CLAUDE_ERROR_MESSAGE="ModuleNotFoundError: No module named 'fastapi'"
export CLAUDE_USER_PROMPT="启动服务器"
export CLAUDE_TOOL_NAME="Bash"
export CLAUDE_SESSION_ID="error-test"
bash scripts/hooks/log_error.sh

# 测试修复建议
bash scripts/hooks/suggest_fix.sh

# 测试错误自动修复
cat > tests/temp/broken.py << 'EOF'
def broken_function(
    return "error"
EOF

export CLAUDE_TOOL_INPUT_FILE_PATH="tests/temp/broken.py"
export CLAUDE_ERROR_MESSAGE="SyntaxError: unexpected EOF while parsing"
bash scripts/hooks/auto_fix_on_error.sh
```

---

## MVP 范围规则

### 包含的功能（MVP）
- 体质测试问卷
- 判定服务
- 基础报告生成
- 饮食推荐
- 结果可视化
- 分享卡片

### 排除的功能（Post-MVP）
- 社交长链（好友PK、积分商城）
- AI 舌诊
- 企业服务
- 季节养生
- 运动推荐
- 健康追踪
- 复杂推荐引擎

---

## 日志文件位置

| 日志文件 | 内容 |
|---------|-----|
| `.claude/hooks/check_env.log` | 环境检查记录 |
| `.claude/hooks/requests.log` | 用户请求日志（最新1000条） |
| `.claude/hooks/feature_requests.log` | 功能请求检测记录 |
| `.claude/hooks/scope_warnings.log` | MVP 范围警告记录 |
| `.claude/hooks/validation.log` | 代码验证记录 |
| `.claude/hooks/file_changes.log` | 文件变更记录（最新500条） |
| `.claude/hooks/api_validation.log` | API 规范验证记录 |
| `.claude/hooks/response_analysis.log` | 响应分析记录 |
| `.claude/hooks/sessions.log` | 会话日志（最新1000条） |
| `.claude/hooks/error_log.log` | 错误日志 |
| `.claude/hooks/progress_updates.log` | 进度更新记录 |
| `.claude/hooks/sql_validation.log` | SQL 验证记录 |
| `.claude/hooks/fix_suggestions.log` | 修复建议记录 |
| `.claude/hooks/auto_fix_sql.log` | SQL 自动修复记录 |
| `.claude/hooks/auto_fix_python.log` | Python 自动修复记录 |
| `.claude/hooks/sql_fixes_applied.log` | SQL 修复应用记录 |
| `.claude/hooks/python_fixes_applied.log` | Python 修复应用记录 |
| `.claude/hooks/auto_fix_errors.log` | 错误自动修复记录 |
| `.claude/hooks/test_execution.log` | 测试执行记录 |

---

## 常见问题

### Q1: Hook 执行失败怎么办？
A: 检查 `.claude/hooks/` 目录下的日志文件，查看具体错误信息。

### Q2: 如何禁用某个 hook？
A: 编辑 `.claude/hooks.json`，将对应 hook 的 `"enabled"` 设为 `false`。

### Q3: 日志文件太大怎么办？
A: 大多数日志已自动限制行数（500-1000行）。手动清理：
```bash
rm -f .claude/hooks/*.log
```

### Q4: 如何添加自定义 hook？
A: 在 `scripts/hooks/` 创建新脚本，然后在 `.claude/hooks.json` 中注册。

---

## 测试命令速查

```bash
# 运行所有测试
bash tests/hooks/run_all_tests.sh

# 运行性能测试
bash tests/hooks/performance_test.sh

# 运行并发测试
bash tests/hooks/concurrent_test.sh

# 清理测试数据
rm -rf tests/temp .claude/hooks/*.log
```

---

## 文件结构

```
traditional_chinese_medicine/
├── .claude/
│   ├── hooks.json                 # Hooks 配置文件
│   ├── mvp_checklist.json         # MVP 任务清单
│   ├── progress.json              # MVP 进度跟踪
│   └── hooks/                     # Hooks 日志目录
├── scripts/
│   └── hooks/                     # Hooks 脚本目录
│       ├── check_env.sh
│       ├── log_request.sh
│       ├── detect_feature.sh
│       ├── check_mvp_scope.sh
│       ├── validate_python.sh
│       ├── validate_sql.sh
│       ├── auto_fix_sql.sh         # SQL 自动修复
│       ├── auto_fix_python.sh      # Python 自动修复
│       ├── track_changes.sh
│       ├── check_api_naming.sh
│       ├── run_relevant_tests.sh   # 测试+自动修复
│       ├── check_response.sh
│       ├── verify_completion.sh
│       ├── log_session.sh
│       ├── update_progress.sh
│       ├── log_error.sh
│       ├── suggest_fix.sh
│       └── auto_fix_on_error.sh    # 错误自动修复
├── tests/
│   ├── hooks/                     # 测试脚本
│   │   ├── README.md
│   │   ├── run_all_tests.sh
│   │   ├── performance_test.sh
│   │   ├── concurrent_test.sh
│   │   └── log_size_test.sh
│   ├── fixtures/                  # 测试数据
│   │   ├── sample_valid.py
│   │   ├── sample_invalid.py
│   │   ├── sample_migration.sql
│   │   └── sample_api.py
│   └── temp/                      # 临时文件
└── docs/
    ├── claude_hooks_test_cases.md     # 完整测试案例
    └── claude_hooks_quick_reference.md # 快速参考
```

---

*快速参考版本: v1.1*
*最后更新: 2025-01-13*
