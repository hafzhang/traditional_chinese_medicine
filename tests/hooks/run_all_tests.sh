#!/bin/bash
# Claude Code Hooks Test Suite
# 运行所有 hooks 测试案例

set -e

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 测试计数器
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
SKIPPED_TESTS=0

# 打印标题
print_header() {
    echo ""
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}======================================${NC}"
    echo ""
}

# 运行单个测试
run_test() {
    local test_name=$1
    local test_command=$2
    local should_fail=$3  # true if test expects failure

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "  Running: $test_name ... "

    # 执行测试命令
    if eval "$test_command" >/dev/null 2>&1; then
        if [ "$should_fail" = "true" ]; then
            echo -e "${RED}FAILED${NC} (expected failure but passed)"
            FAILED_TESTS=$((FAILED_TESTS + 1))
            return 1
        else
            echo -e "${GREEN}PASSED${NC}"
            PASSED_TESTS=$((PASSED_TESTS + 1))
            return 0
        fi
    else
        if [ "$should_fail" = "true" ]; then
            echo -e "${GREEN}PASSED${NC} (expected failure)"
            PASSED_TESTS=$((PASSED_TESTS + 1))
            return 0
        else
            echo -e "${RED}FAILED${NC}"
            FAILED_TESTS=$((FAILED_TESTS + 1))
            return 1
        fi
    fi
}

# 打印测试组开始
print_group() {
    echo ""
    echo -e "${YELLOW}=== $1 ===${NC}"
}

# 主测试流程
main() {
    print_header "Claude Code Hooks Test Suite"

    # 环境准备
    echo "Setting up test environment..."
    mkdir -p .claude/hooks tests/temp tests/fixtures

    # 创建必需文件
    touch requirements.txt pyproject.toml .env.example

    # 创建测试用的有效 Python 文件
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

    echo -e "${GREEN}✅ Environment ready${NC}"

    # ==================== Pre-Command Hooks ====================
    print_group "Pre-Command Hooks (3 tests)"

    run_test "TC-ENV-001: Normal environment check" \
        "bash scripts/hooks/check_env.sh"

    run_test "TC-ENV-002: Missing required files" \
        "rm -f requirements.txt && bash scripts/hooks/check_env.sh && touch requirements.txt"

    # ==================== User-Prompt-Submit Hooks ====================
    print_group "User-Prompt-Submit Hooks (6 tests)"

    export CLAUDE_USER_PROMPT="实现体质测试问卷功能"
    export CLAUDE_SESSION_ID="test-session-001"
    export CLAUDE_MODEL="claude-opus-4-5"

    run_test "TC-REQ-001: Normal request logging" \
        "bash scripts/hooks/log_request.sh"

    run_test "TC-FEATURE-001: Feature detection (new feature)" \
        "bash scripts/hooks/detect_feature.sh"

    run_test "TC-SCOPE-001: MVP scope check (in scope)" \
        "bash scripts/hooks/check_mvp_scope.sh"

    export CLAUDE_USER_PROMPT="添加积分商城功能"
    run_test "TC-SCOPE-002: MVP scope check (out of scope)" \
        "bash scripts/hooks/check_mvp_scope.sh"

    # ==================== Tool-Use Hooks ====================
    print_group "Tool-Use Hooks (8 tests)"

    export CLAUDE_TOOL_NAME="Write"

    run_test "TC-PY-001: Valid Python code validation" \
        "CLAUDE_TOOL_INPUT_FILE_PATH='tests/fixtures/sample_valid.py' bash scripts/hooks/validate_python.sh"

    run_test "TC-PY-003: Non-Python file skip" \
        "CLAUDE_TOOL_INPUT_FILE_PATH='README.md' bash scripts/hooks/validate_python.sh"

    run_test "TC-TRACK-001: Track file changes (Write)" \
        "CLAUDE_TOOL_INPUT_FILE_PATH='backend/test.py' CLAUDE_USER='developer' bash scripts/hooks/track_changes.sh"

    run_test "TC-TRACK-002: Track file changes (Edit)" \
        "CLAUDE_TOOL_NAME='Edit' CLAUDE_TOOL_INPUT_FILE_PATH='docs/test.md' bash scripts/hooks/track_changes.sh"

    run_test "TC-API-001: Valid API file check" \
        "CLAUDE_TOOL_INPUT_FILE_PATH='tests/fixtures/sample_api.py' bash scripts/hooks/check_api_naming.sh"

    run_test "TC-API-005: Non-API directory skip" \
        "CLAUDE_TOOL_INPUT_FILE_PATH='backend/services/validator.py' bash scripts/hooks/check_api_naming.sh"

    # ==================== Pre-Response Hooks ====================
    print_group "Pre-Response Hooks (3 tests)"

    export CLAUDE_RESPONSE="A short test response"
    run_test "TC-RESP-001: Normal response length" \
        "bash scripts/hooks/check_response.sh"

    rm -f .claude/mvp_checklist.json
    run_test "TC-COMP-001: Initialize progress file" \
        "bash scripts/hooks/verify_completion.sh"

    # ==================== Post-Response Hooks ====================
    print_group "Post-Response Hooks (3 tests)"

    export CLAUDE_SESSION_ID="test-session-002"
    export CLAUDE_TOKENS_USED=5000
    export CLAUDE_MODEL="claude-opus-4-5"
    export CLAUDE_USER="developer"

    run_test "TC-SESS-001: Log session summary" \
        "bash scripts/hooks/log_session.sh"

    run_test "TC-PROG-001: Initialize progress file" \
        "bash scripts/hooks/update_progress.sh"

    # ==================== Error Hooks ====================
    print_group "Error Hooks (4 tests)"

    export CLAUDE_ERROR_MESSAGE="ModuleNotFoundError: No module named 'fastapi'"
    export CLAUDE_USER_PROMPT="启动服务器"
    export CLAUDE_TOOL_NAME="Bash"
    export CLAUDE_SESSION_ID="error-test-001"

    run_test "TC-ERR-001: Log module error" \
        "bash scripts/hooks/log_error.sh"

    run_test "TC-FIX-001: Suggest fix for module error" \
        "bash scripts/hooks/suggest_fix.sh"

    export CLAUDE_ERROR_MESSAGE="PermissionError: [Errno 13] Permission denied"
    run_test "TC-ERR-002: Log permission error" \
        "bash scripts/hooks/log_error.sh"

    run_test "TC-FIX-002: Suggest fix for permission error" \
        "bash scripts/hooks/suggest_fix.sh"

    # ==================== 汇总结果 ====================
    print_header "Test Summary"

    echo -e "Total Tests:  ${BLUE}$TOTAL_TESTS${NC}"
    echo -e "${GREEN}Passed:       $PASSED_TESTS${NC}"
    echo -e "${RED}Failed:       $FAILED_TESTS${NC}"
    echo -e "${YELLOW}Skipped:      $SKIPPED_TESTS${NC}"
    echo ""

    # 计算通过率
    if [ $TOTAL_TESTS -gt 0 ]; then
        PASS_RATE=$((PASSED_TESTS * 100 / TOTAL_TESTS))
        echo -e "Pass Rate:    ${PASS_RATE}%"
        echo ""
    fi

    # 显示日志文件位置
    echo "Log files created in: .claude/hooks/"

    # 返回适当的退出码
    if [ $FAILED_TESTS -eq 0 ]; then
        echo -e "${GREEN}======================================${NC}"
        echo -e "${GREEN}All tests passed!${NC}"
        echo -e "${GREEN}======================================${NC}"
        exit 0
    else
        echo -e "${RED}======================================${NC}"
        echo -e "${RED}Some tests failed!${NC}"
        echo -e "${RED}======================================${NC}"
        exit 1
    fi
}

# 执行主流程
main "$@"
