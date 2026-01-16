# Claude Code Hooks 测试案例文档

## 中医体质识别 MVP 项目

---

## 目录

1. [测试概述](#测试概述)
2. [测试环境准备](#测试环境准备)
3. [Pre-Command Hooks 测试](#pre-command-hooks-测试)
4. [User-Prompt-Submit Hooks 测试](#user-prompt-submit-hooks-测试)
5. [Tool-Use Hooks 测试](#tool-use-hooks-测试)
6. [Pre-Response Hooks 测试](#pre-response-hooks-测试)
7. [Post-Response Hooks 测试](#post-response-hooks-测试)
8. [Error Hooks 测试](#error-hooks-测试)
9. [集成测试案例](#集成测试案例)
10. [性能测试案例](#性能测试案例)

---

## 测试概述

### 测试目标

验证所有 Claude Code hooks 在不同场景下能够正确执行，并达到预期效果。

### 测试覆盖范围

| Hook 类型 | Hook 数量 | 测试案例数 |
|----------|----------|-----------|
| pre-command | 1 | 3 |
| user-prompt-submit | 3 | 9 |
| tool-use | 6 | 22 |
| pre-response | 2 | 6 |
| post-response | 2 | 4 |
| error | 3 | 11 |
| **总计** | **17** | **55** |

### 新增自动修复 Hooks

| Hook 名称 | 触发条件 | 功能 |
|-----------|---------|-----|
| `auto_fix_sql` | SQL 验证失败 | 自动修复常见 SQL 问题 |
| `auto_fix_python` | Python 验证失败 | 自动修复常见 Python 问题 |
| `run_relevant_tests` | Write/Edit 后 | 运行测试并自动修复失败 |
| `auto_fix_on_error` | 错误发生 | 根据错误类型自动修复 |

### 测试通过标准

- ✅ Hook 脚本可正常执行（退出码 0）
- ✅ 输出符合预期格式
- ✅ 日志文件正确生成
- ✅ 异常场景能够正确处理

---

## 测试环境准备

### 1. 目录结构创建

```bash
# 创建 hooks 日志目录
mkdir -p .claude/hooks

# 创建测试目录
mkdir -p tests/hooks
mkdir -p tests/fixtures
mkdir -p tests/temp
```

### 2. 设置测试环境变量

```bash
# 创建测试环境文件
cat > tests/.test_env << 'EOF'
# 测试环境变量
export CLAUDE_SESSION_ID="test-session-001"
export CLAUDE_MODEL="claude-opus-4-5"
export CLAUDE_USER="test-user"
export TEST_MODE=true
EOF

source tests/.test_env
```

### 3. 安装测试依赖

```bash
# 安装必要的测试工具
pip install pytest pytest-cov pytest-mock
pip install pyflakes pylint black

# 安装项目依赖
pip install -r requirements.txt
```

### 4. 准备测试数据

```bash
# 创建测试用的 Python 文件
cat > tests/fixtures/sample_valid.py << 'EOF'
"""Sample valid Python file for testing."""
from typing import List


def calculate_constitution_score(answers: List[int]) -> dict:
    """Calculate constitution scores from answers."""
    scores = {"qi_deficiency": 0, "yang_deficiency": 0}
    return scores


class ConstitutionAnalyzer:
    """Analyzes user constitution type."""

    def __init__(self):
        self.version = "1.0.0"
EOF

# 创建测试用的无效 Python 文件
cat > tests/fixtures/sample_invalid.py << 'EOF'
"""Sample invalid Python file for testing."""
def broken_function(
    # Missing closing parenthesis - syntax error
    return "error"
EOF

# 创建测试用的 SQL 文件
cat > tests/fixtures/sample_migration.sql << 'EOF'
-- Migration: Create constitution_results table
CREATE TABLE constitution_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    primary_constitution VARCHAR(50) NOT NULL,
    scores JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_constitution_results_user_id ON constitution_results(user_id);
EOF

# 创建测试用的 API 文件
cat > tests/fixtures/sample_api.py << 'EOF'
"""API endpoints for constitution testing."""
from fastapi import APIRouter


router = APIRouter(prefix="/api/v1")


@router.post("/test/submit")
async def submit_test():
    """Submit constitution test answers."""
    return {"result_id": "test-123"}


@router.get("/result/{result_id}")
async def get_result(result_id: str):
    """Get test result by ID."""
    return {"result_id": result_id}
EOF
```

---

## Pre-Command Hooks 测试

### Hook: check_environment

**触发时机**: 执行任何命令前
**脚本路径**: `scripts/hooks/check_env.sh`

#### 测试案例 TC-ENV-001: 正常环境检查

**测试描述**: 验证在正常环境下环境检查通过

**前置条件**:
- Python 3.11+ 已安装
- requirements.txt 存在
- pyproject.toml 存在
- .env.example 存在
- .env 文件存在且包含必需变量

**测试步骤**:
```bash
# 1. 设置测试环境
export PYTHON_VERSION="3.11.0"
touch requirements.txt pyproject.toml .env.example
cat > .env << 'EOF'
DATABASE_URL=postgresql://localhost:5432/test
SECRET_KEY=test-secret-key
EOF

# 2. 执行 hook
bash scripts/hooks/check_env.sh

# 3. 检查退出码
echo "Exit code: $?"
```

**预期结果**:
```
=== Environment Check ===
Timestamp: 2025-01-13T10:00:00+00:00
Python version: 3.11.0
✅ Python version OK
✅ Found: requirements.txt
✅ Found: pyproject.toml
✅ Found: .env.example
✅ Env var set: DATABASE_URL
✅ Env var set: SECRET_KEY
=== Environment Check Complete ===
Exit code: 0
```

**验证点**:
- [ ] Exit code 为 0
- [ ] 所有检查项显示 ✅
- [ ] 日志文件已创建

---

#### 测试案例 TC-ENV-002: Python 版本不满足要求

**测试描述**: 验证当 Python 版本低于 3.11 时能够正确检测并报错

**前置条件**:
- 系统有 Python 3.9 或 3.10

**测试步骤**:
```bash
# 1. 模拟低版本 Python
export PATH="/path/to/python3.9:$PATH"

# 2. 执行 hook
bash scripts/hooks/check_env.sh 2>&1 | tee test_output.log

# 3. 检查退出码（应该非0）
```

**预期结果**:
```
=== Environment Check ===
Python version: 3.9.7
❌ ERROR: Python 3.11+ required, found 3.9.7
```

**验证点**:
- [ ] Exit code 为 1（非0）
- [ ] 显示错误信息
- [ ] 日志记录错误

---

#### 测试案例 TC-ENV-003: 缺少必需文件

**测试描述**: 验证当缺少必需文件时能够正确检测

**测试步骤**:
```bash
# 1. 清理必需文件
rm -f requirements.txt pyproject.toml

# 2. 执行 hook
bash scripts/hooks/check_env.sh 2>&1
```

**预期结果**:
```
=== Environment Check ===
✅ Python version OK
⚠️  Missing: requirements.txt
⚠️  Missing: pyproject.toml
⚠️  WARNING: .env file not found. Copy from .env.example
```

**验证点**:
- [ ] 显示警告而非错误（退出码0）
- [ ] 列出所有缺失文件

---

## User-Prompt-Submit Hooks 测试

### Hook: log_user_request

**触发时机**: 用户提交提示词时
**脚本路径**: `scripts/hooks/log_request.sh`

#### 测试案例 TC-REQ-001: 正常请求日志

**测试描述**: 验证用户请求能够正确记录

**测试步骤**:
```bash
# 1. 设置环境变量
export CLAUDE_USER_PROMPT="实现体质测试问卷功能"
export CLAUDE_SESSION_ID="test-session-001"
export CLAUDE_MODEL="claude-opus-4-5"

# 2. 执行 hook
bash scripts/hooks/log_request.sh

# 3. 检查日志文件
cat .claude/hooks/requests.log | tail -1
```

**预期结果**:
```json
{
  "timestamp": "2025-01-13T10:00:00+00:00",
  "prompt": "实现体质测试问卷功能",
  "session_id": "test-session-001",
  "model": "claude-opus-4-5"
}
```

**验证点**:
- [ ] 日志格式为 JSON
- [ ] 包含所有必需字段
- [ ] 时间戳格式正确

---

#### 测试案例 TC-REQ-002: 特殊字符处理

**测试描述**: 验证包含特殊字符的请求能够正确转义

**测试步骤**:
```bash
export CLAUDE_USER_PROMPT='创建 "POST /api/v1/test" 接口，返回 {"code": 0}'
bash scripts/hooks/log_request.sh
cat .claude/hooks/requests.log | tail -1 | jq .
```

**预期结果**: JSON 有效，特殊字符正确转义

**验证点**:
- [ ] jq 能够解析 JSON
- [ ] 引号和特殊符号正确转义

---

#### 测试案例 TC-REQ-003: 日志文件大小限制

**测试描述**: 验证日志文件只保留最近1000条记录

**测试步骤**:
```bash
# 1. 创建超过1000条记录
for i in {1..1100}; do
    export CLAUDE_USER_PROMPT="测试请求 $i"
    bash scripts/hooks/log_request.sh
done

# 2. 统计行数
wc -l .claude/hooks/requests.log
```

**预期结果**: 行数 <= 1000

**验证点**:
- [ ] 日志文件不超过1000行
- [ ] 保留的是最新的记录

---

### Hook: detect_feature

**触发时机**: 用户提交提示词时
**脚本路径**: `scripts/hooks/detect_feature.sh`

#### 测试案例 TC-FEATURE-001: 检测新功能请求

**测试步骤**:
```bash
export CLAUDE_USER_PROMPT="添加用户登录功能"
bash scripts/hooks/detect_feature.sh 2>&1
```

**预期结果**:
```
📋 Feature detected: new_feature
```

**验证点**:
- [ ] 正确识别为 new_feature
- [ ] 写入 feature_requests.log

---

#### 测试案例 TC-FEATURE-002: 检测 API 开发请求

**测试步骤**:
```bash
export CLAUDE_USER_PROMPT="实现 POST /api/v1/constitute/analyze 接口"
bash scripts/hooks/detect_feature.sh 2>&1
```

**预期结果**:
```
📋 Feature detected: api_development
```

---

#### 测试案例 TC-FEATURE-003: 检测 UI 开发请求

**测试步骤**:
```bash
export CLAUDE_USER_PROMPT="创建体质报告页面，包含雷达图"
bash scripts/hooks/detect_feature.sh 2>&1
```

**预期结果**:
```
📋 Feature detected: ui_development
```

---

### Hook: check_mvp_scope

**触发时机**: 用户提交提示词时
**脚本路径**: `scripts/hooks/check_mvp_scope.sh`

#### 测试案例 TC-SCOPE-001: MVP 范围内功能（不触发警告）

**测试步骤**:
```bash
export CLAUDE_USER_PROMPT="实现体质测试问卷功能"
bash scripts/hooks/check_mvp_scope.sh 2>&1
echo "Exit code: $?"
```

**预期结果**:
```
Exit code: 0
（无警告输出）
```

**验证点**:
- [ ] 退出码为 0
- [ ] 无警告输出
- [ ] scope_warnings.log 无新增内容

---

#### 测试案例 TC-SCOPE-002: 超出 MVP 范围 - 社交功能

**测试步骤**:
```bash
export CLAUDE_USER_PROMPT="添加好友PK和积分商城功能"
bash scripts/hooks/check_mvp_scope.sh 2>&1
```

**预期结果**:
```
⚠️  WARNING: This feature may be outside MVP scope. Consider deferring to post-MVP.
```

**验证点**:
- [ ] 显示警告
- [ ] scope_warnings.log 记录警告

---

#### 测试案例 TC-SCOPE-003: 超出 MVP 范围 - AI 舌诊

**测试步骤**:
```bash
export CLAUDE_USER_PROMPT="实现 AI 舌诊功能辅助体质识别"
bash scripts/hooks/check_mvp_scope.sh 2>&1
```

**预期结果**:
```
⚠️  WARNING: This feature may be outside MVP scope. Consider deferring to post-MVP.
```

---

#### 测试案例 TC-SCOPE-004: 超出 MVP 范围 - 健康追踪

**测试步骤**:
```bash
export CLAUDE_USER_PROMPT="添加每日打卡和健康追踪功能"
bash scripts/hooks/check_mvp_scope.sh 2>&1
```

**预期结果**:
```
⚠️  WARNING: This feature may be outside MVP scope. Consider deferring to post-MVP.
```

---

## Tool-Use Hooks 测试

### Hook: validate_python_code

**触发时机**: Write 操作写入 *.py 文件时
**脚本路径**: `scripts/hooks/validate_python.sh`

#### 测试案例 TC-PY-001: 验证有效的 Python 代码

**测试步骤**:
```bash
export CLAUDE_TOOL_INPUT_FILE_PATH="tests/fixtures/sample_valid.py"
bash scripts/hooks/validate_python.sh 2>&1
echo "Exit code: $?"
```

**预期结果**:
```
✅ Python syntax OK: tests/fixtures/sample_valid.py
Exit code: 0
```

**验证点**:
- [ ] 验证通过
- [ ] 退出码为 0

---

#### 测试案例 TC-PY-002: 验证无效的 Python 代码

**测试步骤**:
```bash
export CLAUDE_TOOL_INPUT_FILE_PATH="tests/fixtures/sample_invalid.py"
bash scripts/hooks/validate_python.sh 2>&1
echo "Exit code: $?"
```

**预期结果**:
```
❌ Python syntax error in tests/fixtures/sample_invalid.py
Error: <具体语法错误信息>
Exit code: 1
```

**验证点**:
- [ ] 检测到语法错误
- [ ] 退出码为 1（阻止写入）
- [ ] 记录到 validation.log

---

#### 测试案例 TC-PY-003: 非 Python 文件不触发验证

**测试步骤**:
```bash
export CLAUDE_TOOL_INPUT_FILE_PATH="README.md"
bash scripts/hooks/validate_python.sh 2>&1
echo "Exit code: $?"
```

**预期结果**:
```
（无输出）
Exit code: 0
```

**验证点**:
- [ ] 非 .py 文件不触发验证
- [ ] 退出码为 0

---

#### 测试案例 TC-PY-004: API 文件额外验证

**测试步骤**:
```bash
export CLAUDE_TOOL_INPUT_FILE_PATH="backend/api/constitution.py"
export CLAUDE_TOOL_NAME="Write"

# 创建一个不符合规范的 API 文件
cat > tests/temp/bad_api.py << 'EOF'
from fastapi import APIRouter

router = APIRouter()

@router.post("/submitTest")  # 应该是 /api/v1/test/submit
def submitTest():  # 应该是 snake_case
    return {}
EOF

export CLAUDE_TOOL_INPUT_FILE_PATH="tests/temp/bad_api.py"
bash scripts/hooks/check_api_naming.sh 2>&1
```

**预期结果**:
```
⚠️  API Warnings for tests/temp/bad_api.py:
  - Route '/submitTest' should follow /api/v{N} convention
  - Use snake_case for function names, found: submitTest
  - API endpoint should have docstring
```

---

### Hook: validate_sql_schema

**触发时机**: Write 操作写入 *migration*.sql 文件时
**脚本路径**: `scripts/hooks/validate_sql.sh`

#### 测试案例 TC-SQL-001: 验证符合规范的 SQL

**测试步骤**:
```bash
export CLAUDE_TOOL_INPUT_FILE_PATH="tests/fixtures/sample_migration.sql"
bash scripts/hooks/validate_sql.sh 2>&1
echo "Exit code: $?"
```

**预期结果**:
```
✅ SQL validation passed: tests/fixtures/sample_migration.sql
Exit code: 0
```

---

#### 测试案例 TC-SQL-002: 警告 - DROP TABLE 无备份

**测试步骤**:
```bash
cat > tests/temp/dangerous.sql << 'EOF'
DROP TABLE users;
CREATE TABLE users_new (...);
EOF

export CLAUDE_TOOL_INPUT_FILE_PATH="tests/temp/dangerous.sql"
bash scripts/hooks/validate_sql.sh 2>&1
```

**预期结果**:
```
⚠️  SQL Warnings for tests/temp/dangerous.sql:
  - DROP TABLE detected without backup statement
```

---

#### 测试案例 TC-SQL-003: 警告 - 外键无索引

**测试步骤**:
```bash
cat > tests/temp/no_index.sql << 'EOF'
CREATE TABLE test_results (
    user_id UUID REFERENCES users(id),
    score INT
);
EOF

export CLAUDE_TOOL_INPUT_FILE_PATH="tests/temp/no_index.sql"
bash scripts/hooks/validate_sql.sh 2>&1
```

**预期结果**:
```
⚠️  SQL Warnings for tests/temp/no_index.sql:
  - Foreign key detected without index
```

---

#### 测试案例 TC-SQL-004: 警告 - 缺少 created_at

**测试步骤**:
```bash
cat > tests/temp/no_timestamp.sql << 'EOF'
CREATE TABLE test_table (
    id UUID PRIMARY KEY
);
EOF

export CLAUDE_TOOL_INPUT_FILE_PATH="tests/temp/no_timestamp.sql"
bash scripts/hooks/validate_sql.sh 2>&1
```

**预期结果**:
```
⚠️  SQL Warnings for tests/temp/no_timestamp.sql:
  - New table missing created_at column
```

---

### Hook: track_file_changes

**触发时机**: Write 或 Edit 操作时
**脚本路径**: `scripts/hooks/track_changes.sh`

#### 测试案例 TC-TRACK-001: 跟踪 Write 操作

**测试步骤**:
```bash
export CLAUDE_TOOL_NAME="Write"
export CLAUDE_TOOL_INPUT_FILE_PATH="backend/services/constitution.py"
export CLAUDE_USER="developer"

bash scripts/hooks/track_changes.sh

cat .claude/hooks/file_changes.log | tail -1
```

**预期结果**:
```
[2025-01-13T10:00:00+00:00] Write
File: backend/services/constitution.py
User: developer
---
```

---

#### 测试案例 TC-TRACK-002: 跟踪 Edit 操作

**测试步骤**:
```bash
export CLAUDE_TOOL_NAME="Edit"
export CLAUDE_TOOL_INPUT_FILE_PATH="docs/constitution_recognition_mvp.md"

bash scripts/hooks/track_changes.sh
cat .claude/hooks/file_changes.log | tail -2
```

**预期结果**: 记录了 Edit 操作

---

#### 测试案例 TC-TRACK-003: 日志文件大小限制

**测试步骤**:
```bash
# 创建超过500条记录
for i in {1..600}; do
    export CLAUDE_TOOL_NAME="Write"
    export CLAUDE_TOOL_INPUT_FILE_PATH="test_file_$i.py"
    bash scripts/hooks/track_changes.sh
done

wc -l .claude/hooks/file_changes.log
```

**预期结果**: 行数 <= 500

---

### Hook: check_api_endpoint

**触发时机**: Write 操作写入 api/* 目录下的文件时
**脚本路径**: `scripts/hooks/check_api_naming.sh`

#### 测试案例 TC-API-001: 符合规范的 API 文件

**测试步骤**:
```bash
export CLAUDE_TOOL_INPUT_FILE_PATH="tests/fixtures/sample_api.py"
bash scripts/hooks/check_api_naming.sh 2>&1
echo "Exit code: $?"
```

**预期结果**:
```
Exit code: 0
（无警告或错误）
```

---

#### 测试案例 TC-API-002: 路由不符合 /api/vN 规范

**测试步骤**:
```bash
cat > tests/temp/bad_route.py << 'EOF'
from fastapi import APIRouter

router = APIRouter()

@router.post("/submit")  # 应该是 /api/v1/submit
def submit():
    return {}
EOF

export CLAUDE_TOOL_INPUT_FILE_PATH="tests/temp/bad_route.py"
bash scripts/hooks/check_api_naming.sh 2>&1
```

**预期结果**:
```
⚠️  API Warnings for tests/temp/bad_route.py:
  - Route '/submit' should follow /api/v{N} convention
```

---

#### 测试案例 TC-API-003: 函数名使用 camelCase

**测试步骤**:
```bash
cat > tests/temp/camel_case.py << 'EOF'
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

@router.post("/test")
def submitTest():  # 应该是 submit_test
    """Submit test."""
    return {}
EOF

export CLAUDE_TOOL_INPUT_FILE_PATH="tests/temp/camel_case.py"
bash scripts/hooks/check_api_naming.sh 2>&1
```

**预期结果**:
```
⚠️  API Warnings for tests/temp/camel_case.py:
  - Use snake_case for function names, found: submitTest
```

---

#### 测试案例 TC-API-004: 缺少 docstring

**测试步骤**:
```bash
cat > tests/temp/no_docstring.py << 'EOF'
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

@router.post("/test")
def submit():
    return {}
EOF

export CLAUDE_TOOL_INPUT_FILE_PATH="tests/temp/no_docstring.py"
bash scripts/hooks/check_api_naming.sh 2>&1
```

**预期结果**:
```
⚠️  API Warnings for tests/temp/no_docstring.py:
  - API endpoint should have docstring
```

---

#### 测试案例 TC-API-005: 非 API 目录文件不触发

**测试步骤**:
```bash
export CLAUDE_TOOL_INPUT_FILE_PATH="backend/services/validator.py"
bash scripts/hooks/check_api_naming.sh 2>&1
echo "Exit code: $?"
```

**预期结果**:
```
（无输出）
Exit code: 0
```

---

### Hook: auto_fix_sql

**触发时机**: SQL 验证失败时
**脚本路径**: `scripts/hooks/auto_fix_sql.sh`

#### 测试案例 TC-AUTO-SQL-001: 修复缺失的 created_at

**测试步骤**:
```bash
cat > tests/temp/missing_timestamp.sql << 'EOF'
CREATE TABLE test_table (
    id UUID PRIMARY KEY
);
EOF

export CLAUDE_TOOL_INPUT_FILE_PATH="tests/temp/missing_timestamp.sql"
bash scripts/hooks/auto_fix_sql.sh 2>&1

cat tests/temp/missing_timestamp.sql
```

**预期结果**:
```
🔧 Attempting to auto-fix SQL issues in: tests/temp/missing_timestamp.sql
✅ Applied 1 auto-fixes:
  - Added created_at column
   Backup saved to: tests/temp/missing_timestamp.sql.bak
```

**验证点**:
- [ ] 文件已备份
- [ ] created_at 列已添加
- [ ] .bak 文件存在

---

#### 测试案例 TC-AUTO-SQL-002: 修复缺失的外键索引

**测试步骤**:
```bash
cat > tests/temp/no_fk_index.sql << 'EOF'
CREATE TABLE orders (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id)
);
EOF

export CLAUDE_TOOL_INPUT_FILE_PATH="tests/temp/no_fk_index.sql"
bash scripts/hooks/auto_fix_sql.sh 2>&1

cat tests/temp/no_fk_index.sql
```

**预期结果**:
```
✅ Applied 1 auto-fixes:
  - Added index idx_orders_user_id
```

---

#### 测试案例 TC-AUTO-SQL-003: 无法修复的复杂问题

**测试步骤**:
```bash
cat > tests/temp/complex_issue.sql << 'EOF'
-- Complex SQL issue that auto-fix cannot handle
CREATE OR REPLACE FUNCTION broken_function()
RETURNS void AS $$
BEGIN
    -- Complex logic error
    -- This cannot be auto-fixed
END;
$$ LANGUAGE plpgsql;
EOF

export CLAUDE_TOOL_INPUT_FILE_PATH="tests/temp/complex_issue.sql"
bash scripts/hooks/auto_fix_sql.sh 2>&1
echo "Exit code: $?"
```

**预期结果**:
```
ℹ️  No auto-fixes available for this SQL file
Exit code: 1
```

---

### Hook: auto_fix_python

**触发时机**: Python 验证失败时
**脚本路径**: `scripts/hooks/auto_fix_python.sh`

#### 测试案例 TC-AUTO-PY-001: 修复 camelCase 函数名

**测试步骤**:
```bash
cat > tests/temp/camel_case_func.py << 'EOF'
def calculateScore():
    return 100

result = calculateScore()
EOF

export CLAUDE_TOOL_INPUT_FILE_PATH="tests/temp/camel_case_func.py"
bash scripts/hooks/auto_fix_python.sh 2>&1

cat tests/temp/camel_case_func.py
```

**预期结果**:
```
🔧 Attempting to auto-fix Python issues in: tests/temp/camel_case_func.py
✅ Applied 1 auto-fixes:
  - Renamed function: calculateScore → calculate_score
   Backup saved to: tests/temp/camel_case_func.py.bak
✅ Fixed code passes syntax validation!
```

---

#### 测试案例 TC-AUTO-PY-002: 添加缺失的类型提示

**测试步骤**:
```bash
cat > tests/temp/no_type_hints.py << 'EOF'
def add_numbers(a, b):
    return a + b
EOF

export CLAUDE_TOOL_INPUT_FILE_PATH="tests/temp/no_type_hints.py"
bash scripts/hooks/auto_fix_python.sh 2>&1
```

**预期结果**:
```
✅ Applied auto-fixes:
  - Added type hint: add_numbers() -> None
```

---

#### 测试案例 TC-AUTO-PY-003: 添加 typing 导入

**测试步骤**:
```bash
cat > tests/temp/missing_typing.py << 'EOF'
from fastapi import APIRouter

def process_items(items: List[str]) -> Dict:
    return {"result": items}
EOF

export CLAUDE_TOOL_INPUT_FILE_PATH="tests/temp/missing_typing.py"
bash scripts/hooks/auto_fix_python.sh 2>&1
```

**预期结果**:
```
✅ Applied auto-fixes:
  - Added typing imports
```

---

### Hook: run_relevant_tests

**触发时机**: Write/Edit 操作后
**脚本路径**: `scripts/hooks/run_relevant_tests.sh`

#### 测试案例 TC-TEST-001: Python 文件测试通过

**测试步骤**:
```bash
export CLAUDE_TOOL_INPUT_FILE_PATH="tests/fixtures/sample_valid.py"
bash scripts/hooks/run_relevant_tests.sh 2>&1
```

**预期结果**:
```
🧪 Running tests for: sample_valid.py
  Running: Python syntax check...
  ✅ Python syntax check: PASSED

✅ All tests passed (1/1)
```

---

#### 测试案例 TC-TEST-002: Python 文件测试失败后自动修复

**测试步骤**:
```bash
cat > tests/temp/broken_syntax.py << 'EOF'
def broken_function(
    return "error"
EOF

export CLAUDE_TOOL_INPUT_FILE_PATH="tests/temp/broken_syntax.py"
bash scripts/hooks/run_relevant_tests.sh 2>&1
```

**预期结果**:
```
🧪 Running tests for: broken_syntax.py
  Running: Python syntax check...
  ❌ Python syntax check: FAILED
  🔧 Attempting auto-fix...
  🔧 Attempting to auto-fix Python issues in: tests/temp/broken_syntax.py
  ✅ Applied auto-fixes:
    - Removed trailing whitespace
    - Added final newline
  🔧 Attempting to auto-fix...
  ⚠️  Auto-fix applied but test still fails

⚠️  Some tests failed (0/1 passed, 1 failed)
```

---

#### 测试案例 TC-TEST-003: SQL 文件测试通过

**测试步骤**:
```bash
export CLAUDE_TOOL_INPUT_FILE_PATH="tests/fixtures/sample_migration.sql"
bash scripts/hooks/run_relevant_tests.sh 2>&1
```

**预期结果**:
```
🧪 Running tests for: sample_migration.sql
  Running: SQL schema validation...
  ✅ SQL schema validation: PASSED

✅ All tests passed (1/1)
```

---

#### 测试案例 TC-TEST-004: 不支持的文件类型

**测试步骤**:
```bash
export CLAUDE_TOOL_INPUT_FILE_PATH="README.md"
bash scripts/hooks/run_relevant_tests.sh 2>&1
```

**预期结果**:
```
🧪 Running tests for: README.md
  ℹ️  No tests configured for .md files

ℹ️  No tests run for this file
```

---

### Hook: auto_fix_on_error

**触发时机**: 错误发生时
**脚本路径**: `scripts/hooks/auto_fix_on_error.sh`

#### 测试案例 TC-AUTO-ERR-001: Python 语法错误自动修复

**测试步骤**:
```bash
cat > tests/temp/syntax_error.py << 'EOF'
def broken(
    return "missing paren"
EOF

export CLAUDE_TOOL_INPUT_FILE_PATH="tests/temp/syntax_error.py"
export CLAUDE_ERROR_MESSAGE="SyntaxError: unexpected EOF while parsing"
bash scripts/hooks/auto_fix_on_error.sh 2>&1
```

**预期结果**:
```
🔧 Auto-fix triggered by error: SyntaxError: unexpected EOF while parsing
   File: tests/temp/syntax_error.py
  🔧 Running auto-fix script: auto_fix_python.sh
  🔧 Attempting to auto-fix Python issues...
  ✅ Applied auto-fixes:
    - Added final newline
```

---

#### 测试案例 TC-AUTO-ERR-002: SQL 验证错误自动修复

**测试步骤**:
```bash
cat > tests/temp/invalid_table.sql << 'EOF'
CREATE TABLE test (
    id INT
    -- Missing created_at
);
EOF

export CLAUDE_TOOL_INPUT_FILE_PATH="tests/temp/invalid_table.sql"
export CLAUDE_ERROR_MESSAGE="ValidationError: Missing created_at column"
bash scripts/hooks/auto_fix_on_error.sh 2>&1
```

**预期结果**:
```
🔧 Auto-fix triggered by error: ValidationError: Missing created_at column
   File: tests/temp/invalid_table.sql
  🔧 Running auto-fix script: auto_fix_sql.sh
  ✅ Applied auto-fixes:
    - Added created_at column
```

---

#### 测试案例 TC-AUTO-ERR-003: 无法识别的错误类型

**测试步骤**:
```bash
export CLAUDE_ERROR_MESSAGE="UnknownError: Something unexpected happened"
bash scripts/hooks/auto_fix_on_error.sh 2>&1
echo "Exit code: $?"
```

**预期结果**:
```
ℹ️  No auto-fix available for file type: .unknown
Exit code: 0
```

---

## Pre-Response Hooks 测试

### Hook: check_response_length

**触发时机**: 生成响应前
**脚本路径**: `scripts/hooks/check_response.sh`

#### 测试案例 TC-RESP-001: 正常长度响应

**测试步骤**:
```bash
# 创建一个约1000字符的响应
export CLAUDE_RESPONSE=$(python3 << 'EOF'
print("A" * 1000)
EOF
)

bash scripts/hooks/check_response.sh 2>&1
echo "Exit code: $?"
```

**预期结果**:
```
Exit code: 0
（无警告）
```

---

#### 测试案例 TC-RESP-002: 长响应警告

**测试步骤**:
```bash
# 创建一个约60000字符的响应
export CLAUDE_RESPONSE=$(python3 << 'EOF'
print("A" * 60000)
EOF
)

bash scripts/hooks/check_response.sh 2>&1
echo "Exit code: $?"
```

**预期结果**:
```
⚠️  WARNING: Long response (60000 chars, ~15000 tokens)
Exit code: 0
```

---

#### 测试案例 TC-RESP-003: 超长响应严重警告

**测试步骤**:
```bash
# 创建一个约120000字符的响应
export CLAUDE_RESPONSE=$(python3 << 'EOF'
print("A" * 120000)
EOF
)

bash scripts/hooks/check_response.sh 2>&1
echo "Exit code: $?"
```

**预期结果**:
```
⚠️  CRITICAL: Response is very long (120000 chars, ~30000 tokens)
   Consider breaking into smaller responses.
```

---

### Hook: verify_task_completion

**触发时机**: 生成响应前
**脚本路径**: `scripts/hooks/verify_completion.sh`

#### 测试案例 TC-COMP-001: 无进度文件时初始化

**测试步骤**:
```bash
rm -f .claude/mvp_checklist.json
bash scripts/hooks/verify_completion.sh 2>&1
```

**预期结果**:
```
📊 MVP Progress: 0/21 tasks completed (0%)
```

**验证点**:
- [ ] 创建了 mvp_checklist.json
- [ ] 显示初始进度

---

#### 测试案例 TC-COMP-002: 部分完成状态

**测试步骤**:
```bash
cat > .claude/mvp_checklist.json << 'EOF'
{
  "week_0": {
    "tasks": [
      {"id": "w0_1", "task": "确认30题问卷", "status": "completed"},
      {"id": "w0_2", "task": "确认首发平台", "status": "completed"},
      {"id": "w0_3", "task": "接口规范评审", "status": "pending"}
    ]
  }
}
EOF

bash scripts/hooks/verify_completion.sh 2>&1
```

**预期结果**:
```
📊 MVP Progress: 2/21 tasks completed (9%)
```

---

#### 测试案例 TC-COMP-003: 全部完成状态

**测试步骤**:
```bash
# 修改所有任务为 completed
jq '(.[][].tasks[] | select(.status == "pending")).status = "completed"' \
    .claude/mvp_checklist.json > /tmp/checklist.json && \
    mv /tmp/checklist.json .claude/mvp_checklist.json

bash scripts/hooks/verify_completion.sh 2>&1
```

**预期结果**:
```
📊 MVP Progress: 21/21 tasks completed (100%)
🎉 All MVP tasks completed!
```

---

## Post-Response Hooks 测试

### Hook: log_session_summary

**触发时机**: 响应完成后
**脚本路径**: `scripts/hooks/log_session.sh`

#### 测试案例 TC-SESS-001: 记录会话摘要

**测试步骤**:
```bash
export CLAUDE_SESSION_ID="test-session-001"
export CLAUDE_TOKENS_USED=5432
export CLAUDE_MODEL="claude-opus-4-5"
export CLAUDE_USER="developer"

bash scripts/hooks/log_session.sh

cat .claude/hooks/sessions.log | tail -1 | jq .
```

**预期结果**:
```json
{
  "timestamp": "2025-01-13T10:00:00+00:00",
  "session_id": "test-session-001",
  "tokens_used": 5432,
  "model": "claude-opus-4-5",
  "user": "developer"
}
```

---

#### 测试案例 TC-SESS-002: 日志文件大小限制

**测试步骤**:
```bash
# 创建超过1000条记录
for i in {1..1100}; do
    export CLAUDE_SESSION_ID="session-$i"
    export CLAUDE_TOKENS_USED=1000
    bash scripts/hooks/log_session.sh
done

wc -l .claude/hooks/sessions.log
```

**预期结果**: 行数 <= 1000

---

### Hook: update_progress

**触发时机**: 响应完成后
**脚本路径**: `scripts/hooks/update_progress.sh`

#### 测试案例 TC-PROG-001: 初始化进度文件

**测试步骤**:
```bash
rm -f .claude/progress.json
bash scripts/hooks/update_progress.sh

cat .claude/progress.json | jq .
```

**预期结果**:
```json
{
  "mvp_deadline_days": 21,
  "days_elapsed": 0,
  "current_week": 0,
  "tasks_completed": 0,
  "tasks_total": 21,
  "last_updated": "2025-01-13T10:00:00+00:00"
}
```

---

#### 测试案例 TC-PROG-002: 更新时间戳

**测试步骤**:
```bash
# 第一次执行
bash scripts/hooks/update_progress.sh
FIRST_TIMESTAMP=$(jq -r '.last_updated' .claude/progress.json)

# 等待后再次执行
sleep 2
bash scripts/hooks/update_progress.sh
SECOND_TIMESTAMP=$(jq -r '.last_updated' .claude/progress.json)

echo "First: $FIRST_TIMESTAMP"
echo "Second: $SECOND_TIMESTAMP"
```

**预期结果**: 时间戳不同（已更新）

---

## Error Hooks 测试

### Hook: log_error

**触发时机**: 发生错误时
**脚本路径**: `scripts/hooks/log_error.sh`

#### 测试案例 TC-ERR-001: 记录模块导入错误

**测试步骤**:
```bash
export CLAUDE_ERROR_MESSAGE="ModuleNotFoundError: No module named 'fastapi'"
export CLAUDE_USER_PROMPT="启动 FastAPI 服务器"
export CLAUDE_TOOL_NAME="Bash"
export CLAUDE_SESSION_ID="test-session-001"

bash scripts/hooks/log_error.sh 2>&1

cat .claude/hooks/error_log.log | tail -1 | jq .
```

**预期结果**:
```json
{
  "timestamp": "2025-01-13T10:00:00+00:00",
  "error": "ModuleNotFoundError: No module named 'fastapi'",
  "user_prompt": "启动 FastAPI 服务器",
  "tool_name": "Bash",
  "session_id": "test-session-001"
}
```

---

#### 测试案例 TC-ERR-002: 记录权限错误

**测试步骤**:
```bash
export CLAUDE_ERROR_MESSAGE="PermissionError: [Errno 13] Permission denied: '/var/log/app.log'"
export CLAUDE_USER_PROMPT="写入日志文件"
export CLAUDE_TOOL_NAME="Write"

bash scripts/hooks/log_error.sh
```

**预期结果**: 错误被记录到日志

---

#### 测试案例 TC-ERR-003: 记录语法错误

**测试步骤**:
```bash
export CLAUDE_ERROR_MESSAGE="SyntaxError: invalid syntax (constitution.py, line 42)"
export CLAUDE_USER_PROMPT="运行体质分析脚本"
export CLAUDE_TOOL_NAME="Bash"

bash scripts/hooks/log_error.sh
```

**预期结果**: 错误被记录

---

#### 测试案例 TC-ERR-004: 记录数据库连接错误

**测试步骤**:
```bash
export CLAUDE_ERROR_MESSAGE="psycopg2.OperationalError: could not connect to server: Connection refused"
export CLAUDE_USER_PROMPT="连接数据库"
export CLAUDE_TOOL_NAME="Bash"

bash scripts/hooks/log_error.sh
```

**预期结果**: 错误被记录

---

### Hook: suggest_fix

**触发时机**: 发生错误时
**脚本路径**: `scripts/hooks/suggest_fix.sh`

#### 测试案例 TC-FIX-001: 模块缺失建议

**测试步骤**:
```bash
export CLAUDE_ERROR_MESSAGE="ModuleNotFoundError: No module named 'sqlalchemy'"
bash scripts/hooks/suggest_fix.sh 2>&1
```

**预期结果**:
```
❌ Error logged to .claude/hooks/error_log.log
💡 Suggestion: Install missing module with 'pip install <module_name>'
```

---

#### 测试案例 TC-FIX-002: 权限错误建议

**测试步骤**:
```bash
export CLAUDE_ERROR_MESSAGE="PermissionError: [Errno 13] Permission denied"
bash scripts/hooks/suggest_fix.sh 2>&1
```

**预期结果**:
```
💡 Suggestion: Check file permissions or run with appropriate access rights
```

---

#### 测试案例 TC-FIX-003: 语法错误建议

**测试步骤**:
```bash
export CLAUDE_ERROR_MESSAGE="SyntaxError: invalid syntax"
bash scripts/hooks/suggest_fix.sh 2>&1
```

**预期结果**:
```
💡 Suggestion: Validate syntax using linter/formatter (e.g., pylint, black)
```

---

#### 测试案例 TC-FIX-004: 数据库连接错误建议

**测试步骤**:
```bash
export CLAUDE_ERROR_MESSAGE="Connection refused at localhost:5432"
bash scripts/hooks/suggest_fix.sh 2>&1
```

**预期结果**:
```
💡 Suggestion: Verify database/server is running and accessible
```

---

## 集成测试案例

### TC-INT-001: 完整开发流程

**测试描述**: 模拟完整的 MVP 开发流程，验证所有 hooks 协同工作

**测试场景**: 实现"体质测试问卷提交"功能

**测试步骤**:

1. **用户提交请求**
```bash
export CLAUDE_USER_PROMPT="实现 POST /api/v1/test/submit 接口，接收30题问卷答案并返回体质结果"
export CLAUDE_SESSION_ID="integration-test-001"

# 触发 user-prompt-submit hooks
bash scripts/hooks/log_request.sh
bash scripts/hooks/detect_feature.sh
bash scripts/hooks/check_mvp_scope.sh
```

2. **验证通过后，创建 Python 文件**
```bash
export CLAUDE_TOOL_NAME="Write"
export CLAUDE_TOOL_INPUT_FILE_PATH="backend/api/test.py"

# 先创建一个有效的 Python 文件
cat > backend/api/test.py << 'EOF'
"""API endpoints for constitution test."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter(prefix="/api/v1")


class TestSubmitRequest(BaseModel):
    """Request model for test submission."""
    answers: list[int]
    user_id: str | None = None


@router.post("/test/submit")
async def submit_test(request: TestSubmitRequest):
    """Submit constitution test and get results."""
    # Validate answers
    if len(request.answers) != 30:
        raise HTTPException(status_code=400, detail="Expected 30 answers")

    # Calculate scores (simplified)
    scores = {
        "qi_deficiency": 85,
        "yang_deficiency": 35,
        "yin_deficiency": 20
    }

    return {
        "result_id": "test-123",
        "primary_constitution": "qi_deficiency",
        "scores": scores
    }
EOF

# 触发 tool-use hooks
bash scripts/hooks/validate_python.sh
bash scripts/hooks/check_api_naming.sh
bash scripts/hooks/track_changes.sh
```

3. **生成响应后**
```bash
export CLAUDE_TOKENS_USED=8500
bash scripts/hooks/log_session.sh
bash scripts/hooks/update_progress.sh
bash scripts/hooks/verify_completion.sh
```

**预期结果**:
```
# Step 1 输出
📋 Feature detected: api_development

# Step 2 输出
✅ Python syntax OK: backend/api/test.py
[2025-01-13T10:00:00+00:00] Write
File: backend/api/test.py

# Step 3 输出
📊 MVP Progress: 1/21 tasks completed (5%)
```

**验证点**:
- [ ] 所有 hooks 正常执行
- [ ] 日志文件正确记录
- [ ] 进度正确更新
- [ ] 无阻塞错误

---

### TC-INT-002: 错误处理流程

**测试描述**: 验证当发生错误时的 hooks 行为

**测试步骤**:

1. **模拟错误场景**
```bash
# 尝试写入有语法错误的 Python 文件
cat > tests/temp/error_test.py << 'EOF'
def broken_function(
    # Missing closing parenthesis
    return "error"
EOF

export CLAUDE_TOOL_NAME="Write"
export CLAUDE_TOOL_INPUT_FILE_PATH="tests/temp/error_test.py"

# 执行验证（应该失败）
bash scripts/hooks/validate_python.sh 2>&1
EXIT_CODE=$?

echo "Exit code: $EXIT_CODE"
```

2. **记录错误**
```bash
export CLAUDE_ERROR_MESSAGE="SyntaxError: unexpected EOF while parsing"
export CLAUDE_USER_PROMPT="创建体质分析函数"
export CLAUDE_TOOL_NAME="Write"
export CLAUDE_SESSION_ID="error-test-001"

bash scripts/hooks/log_error.sh
bash scripts/hooks/suggest_fix.sh
```

**预期结果**:
```
# Step 1 输出
❌ Python syntax error in tests/temp/error_test.py
Error: <具体错误信息>
Exit code: 1

# Step 2 输出
❌ Error logged to .claude/hooks/error_log.log
💡 Suggestion: Validate syntax using linter/formatter (e.g., pylint, black)
```

---

### TC-INT-003: MVP 范围警告流程

**测试描述**: 验证请求超出 MVP 功能时的警告机制

**测试步骤**:
```bash
# 测试各种超出 MVP 范围的请求

test_requests=(
    "添加积分商城功能"
    "实现 AI 舌诊辅助"
    "创建好友 PK 功能"
    "添加每日健康打卡"
)

for request in "${test_requests[@]}"; do
    echo "Testing: $request"
    export CLAUDE_USER_PROMPT="$request"
    bash scripts/hooks/check_mvp_scope.sh 2>&1
    echo "---"
done
```

**预期结果**: 所有请求都触发警告

---

## 性能测试案例

### TC-PERF-001: Hook 执行时间

**测试描述**: 验证每个 hook 的执行时间在可接受范围内

**测试步骤**:
```bash
#!/bin/bash
# tests/hooks/performance_test.sh

declare -A hooks=(
    ["check_environment"]="scripts/hooks/check_env.sh"
    ["log_request"]="scripts/hooks/log_request.sh"
    ["detect_feature"]="scripts/hooks/detect_feature.sh"
    ["check_mvp_scope"]="scripts/hooks/check_mvp_scope.sh"
    ["validate_python"]="scripts/hooks/validate_python.sh"
    ["track_changes"]="scripts/hooks/track_changes.sh"
    ["check_response"]="scripts/hooks/check_response.sh"
    ["verify_completion"]="scripts/hooks/verify_completion.sh"
    ["log_session"]="scripts/hooks/log_session.sh"
    ["log_error"]="scripts/hooks/log_error.sh"
)

echo "Hook Performance Test"
echo "===================="

for hook_name in "${!hooks[@]}"; do
    hook_script="${hooks[$hook_name]}"

    # 设置必要的环境变量
    export CLAUDE_USER_PROMPT="test prompt"
    export CLAUDE_SESSION_ID="perf-test"
    export CLAUDE_TOOL_NAME="Write"
    export CLAUDE_TOOL_INPUT_FILE_PATH="test.py"
    export CLAUDE_RESPONSE="test response"
    export CLAUDE_ERROR_MESSAGE="test error"

    # 测量执行时间
    start_time=$(date +%s%N)
    bash "$hook_script" >/dev/null 2>&1
    end_time=$(date +%s%N)

    duration=$(( (end_time - start_time) / 1000000 ))  # 转换为毫秒

    printf "%-25s %5d ms\n" "$hook_name:" "$duration"

    # 判断是否超时（阈值：100ms）
    if [ $duration -gt 100 ]; then
        echo "  ⚠️  WARNING: Hook execution exceeds 100ms threshold"
    fi
done
```

**预期结果**: 所有 hooks 执行时间 < 100ms

---

### TC-PERF-002: 并发执行测试

**测试描述**: 验证多个 hooks 并发执行时的性能

**测试步骤**:
```bash
#!/bin/bash
# tests/hooks/concurrent_test.sh

echo "Concurrent Hook Execution Test"
echo "=============================="

# 模拟并发执行
for i in {1..10}; do
    (
        export CLAUDE_SESSION_ID="concurrent-$i"
        export CLAUDE_USER_PROMPT="Concurrent test $i"
        bash scripts/hooks/log_request.sh
        bash scripts/hooks/detect_feature.sh
    ) &
done

wait

echo "All concurrent hooks completed"

# 检查日志完整性
REQUEST_COUNT=$(wc -l < .claude/hooks/requests.log)
echo "Total requests logged: $REQUEST_COUNT"
```

**预期结果**:
- 所有并发执行完成
- 日志完整记录（10条）

---

### TC-PERF-003: 日志文件大小测试

**测试描述**: 验证日志文件大小控制机制

**测试步骤**:
```bash
#!/bin/bash
# tests/hooks/log_size_test.sh

echo "Log Size Control Test"
echo "===================="

# 生成大量日志记录
echo "Generating 2000 log entries..."

for i in {1..2000}; do
    export CLAUDE_SESSION_ID="size-test-$i"
    export CLAUDE_TOKENS_USED=1000
    bash scripts/hooks/log_session.sh
done

# 检查文件大小
FILE_SIZE=$(wc -c < .claude/hooks/sessions.log)
LINE_COUNT=$(wc -l < .claude/hooks/sessions.log)

echo "Session log file size: $FILE_SIZE bytes"
echo "Session log line count: $LINE_COUNT"

# 验证行数限制
if [ $LINE_COUNT -le 1000 ]; then
    echo "✅ Log size control working correctly (max 1000 lines)"
else
    echo "❌ Log size exceeds limit!"
fi
```

**预期结果**: 日志文件行数 <= 1000

---

## 测试执行脚本

### 完整测试套件

```bash
#!/bin/bash
# tests/hooks/run_all_tests.sh

set -e

echo "======================================"
echo "Claude Code Hooks Test Suite"
echo "======================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

run_test() {
    local test_name=$1
    local test_command=$2

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "Running: $test_name ... "

    if eval "$test_command" >/dev/null 2>&1; then
        echo -e "${GREEN}PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}FAILED${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# 环境准备
echo "Setting up test environment..."
mkdir -p .claude/hooks tests/temp
touch requirements.txt pyproject.toml .env.example
echo "✅ Environment ready"
echo ""

# Pre-Command Hooks 测试
echo "=== Pre-Command Hooks ==="
run_test "TC-ENV-001: Normal environment check" \
    "bash scripts/hooks/check_env.sh"
run_test "TC-ENV-003: Missing required files" \
    "bash scripts/hooks/check_env.sh"
echo ""

# User-Prompt-Submit Hooks 测试
echo "=== User-Prompt-Submit Hooks ==="
export CLAUDE_USER_PROMPT="实现体质测试问卷功能"
export CLAUDE_SESSION_ID="test-session-001"
run_test "TC-REQ-001: Normal request logging" \
    "bash scripts/hooks/log_request.sh"
run_test "TC-FEATURE-001: Feature detection" \
    "bash scripts/hooks/detect_feature.sh"
run_test "TC-SCOPE-001: MVP scope check (in scope)" \
    "bash scripts/hooks/check_mvp_scope.sh"
echo ""

# Tool-Use Hooks 测试
echo "=== Tool-Use Hooks ==="
export CLAUDE_TOOL_NAME="Write"
export CLAUDE_TOOL_INPUT_FILE_PATH="tests/fixtures/sample_valid.py"
run_test "TC-PY-001: Valid Python code" \
    "bash scripts/hooks/validate_python.sh"
run_test "TC-TRACK-001: Track file changes" \
    "bash scripts/hooks/track_changes.sh"
echo ""

# Pre-Response Hooks 测试
echo "=== Pre-Response Hooks ==="
export CLAUDE_RESPONSE="test response"
run_test "TC-RESP-001: Normal response length" \
    "bash scripts/hooks/check_response.sh"
run_test "TC-COMP-001: Initialize progress" \
    "bash scripts/hooks/verify_completion.sh"
echo ""

# Post-Response Hooks 测试
echo "=== Post-Response Hooks ==="
export CLAUDE_TOKENS_USED=5000
run_test "TC-SESS-001: Log session summary" \
    "bash scripts/hooks/log_session.sh"
run_test "TC-PROG-001: Initialize progress file" \
    "bash scripts/hooks/update_progress.sh"
echo ""

# Error Hooks 测试
echo "=== Error Hooks ==="
export CLAUDE_ERROR_MESSAGE="Test error message"
run_test "TC-ERR-001: Log error" \
    "bash scripts/hooks/log_error.sh"
run_test "TC-FIX-001: Suggest fix for module error" \
    "CLAUDE_ERROR_MESSAGE='ModuleNotFoundError: test' bash scripts/hooks/suggest_fix.sh"
echo ""

# 性能测试
echo "=== Performance Tests ==="
echo "Skipping detailed performance tests (use performance_test.sh)"
echo ""

# 汇总结果
echo "======================================"
echo "Test Summary"
echo "======================================"
echo -e "Total Tests:  $TOTAL_TESTS"
echo -e "${GREEN}Passed:       $PASSED_TESTS${NC}"
echo -e "${RED}Failed:       $FAILED_TESTS${NC}"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed!${NC}"
    exit 1
fi
```

---

## 测试报告模板

```markdown
# Claude Code Hooks 测试报告

## 测试信息

- **测试日期**: 2025-01-13
- **测试人员**: [测试人员姓名]
- **测试环境**: Python 3.11, Ubuntu 22.04
- **测试版本**: MVP v1.0

## 测试结果汇总

| Hook 类型 | 总数 | 通过 | 失败 | 通过率 |
|----------|-----|-----|-----|--------|
| pre-command | 3 | 3 | 0 | 100% |
| user-prompt-submit | 9 | 9 | 0 | 100% |
| tool-use | 16 | 15 | 1 | 93.75% |
| pre-response | 6 | 6 | 0 | 100% |
| post-response | 4 | 4 | 0 | 100% |
| error | 8 | 8 | 0 | 100% |
| **总计** | **46** | **45** | **1** | **97.8%** |

## 失败测试详情

### TC-API-003: 函数名使用 camelCase

**失败原因**: 正则表达式未正确匹配 camelCase
**修复方案**: 更新正则表达式为 `[a-z]+[A-Z]`
**状态**: 已修复

## 性能测试结果

| Hook | 平均执行时间 | 最大执行时间 | 状态 |
|------|-------------|-------------|------|
| check_environment | 45ms | 120ms | ⚠️ |
| log_request | 5ms | 8ms | ✅ |
| validate_python | 120ms | 250ms | ⚠️ |
| track_changes | 3ms | 5ms | ✅ |

## 建议与改进

1. **性能优化**: `validate_python` hook 执行时间较长，建议增加缓存机制
2. **错误处理**: 增强异常处理，避免 hook 执行失败影响主流程
3. **日志管理**: 考虑使用日志轮转，避免单个日志文件过大

## 结论

本次测试覆盖了所有 14 个 hooks 共 46 个测试案例，整体通过率 97.8%。
核心功能验证通过，可以投入使用。
```

---

*文档版本: v1.0*
*最后更新: 2025-01-13*
