#!/bin/bash
# Claude Code Hooks Performance Test
# 测试每个 hook 的执行时间

set -e

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 性能阈值（毫秒）
WARNING_THRESHOLD=100
CRITICAL_THRESHOLD=500

# 打印标题
print_header() {
    echo ""
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}======================================${NC}"
    echo ""
}

# 主测试流程
main() {
    print_header "Hook Performance Test"

    # 确保日志目录存在
    mkdir -p .claude/hooks tests/temp tests/fixtures

    # 创建测试文件
    cat > tests/fixtures/sample_valid.py << 'EOF'
"""Sample valid Python file."""
def test():
    return "test"
EOF

    cat > tests/fixtures/sample_api.py << 'EOF'
"""API endpoints."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

@router.post("/test")
async def test():
    """Test endpoint."""
    return {}
EOF

    # 准备环境变量
    export CLAUDE_USER_PROMPT="test prompt"
    export CLAUDE_SESSION_ID="perf-test"
    export CLAUDE_MODEL="claude-opus-4-5"
    export CLAUDE_USER="developer"
    export CLAUDE_TOOL_NAME="Write"
    export CLAUDE_TOOL_INPUT_FILE_PATH="tests/fixtures/sample_valid.py"
    export CLAUDE_RESPONSE="test response"
    export CLAUDE_ERROR_MESSAGE="test error"
    export CLAUDE_TOKENS_USED=5000

    # Hook 列表和名称
    declare -a hooks=(
        "scripts/hooks/check_env.sh:check_environment"
        "scripts/hooks/log_request.sh:log_user_request"
        "scripts/hooks/detect_feature.sh:detect_feature"
        "scripts/hooks/check_mvp_scope.sh:check_mvp_scope"
        "scripts/hooks/validate_python.sh:validate_python_code"
        "scripts/hooks/track_changes.sh:track_file_changes"
        "scripts/hooks/check_api_naming.sh:check_api_endpoint"
        "scripts/hooks/check_response.sh:check_response_length"
        "scripts/hooks/verify_completion.sh:verify_task_completion"
        "scripts/hooks/log_session.sh:log_session_summary"
        "scripts/hooks/update_progress.sh:update_progress"
        "scripts/hooks/log_error.sh:log_error"
        "scripts/hooks/suggest_fix.sh:suggest_fix"
    )

    # 测试结果存储
    declare -a durations=()
    declare -a names=()
    declare -a statuses=()

    echo -e "${YELLOW}Testing ${#hooks[@]} hooks...${NC}"
    echo ""

    # 执行每个 hook 并测量时间
    for hook_entry in "${hooks[@]}"; do
        IFS=':' read -r script_path hook_name <<< "$hook_entry"

        # 测量执行时间（纳秒级）
        start_time=$(date +%s%N)
        bash "$script_path" >/dev/null 2>&1 || true
        end_time=$(date +%s%N)

        # 转换为毫秒
        duration=$(( (end_time - start_time) / 1000000 ))

        durations+=("$duration")
        names+=("$hook_name")
    done

    # 显示结果
    echo ""
    echo -e "${BLUE}Results:${NC}"
    echo ""
    printf "%-35s %10s %10s\n" "Hook Name" "Time (ms)" "Status"
    printf "%-35s %10s %10s\n" "-----------------------------------" "----------" "----------"

    slow_hooks=0
    critical_hooks=0
    total_time=0

    for i in "${!names[@]}"; do
        duration=${durations[$i]}
        name=${names[$i]}
        total_time=$((total_time + duration))

        # 判断状态
        if [ $duration -ge $CRITICAL_THRESHOLD ]; then
            status="${RED}CRITICAL${NC}"
            symbol="⚠️⚠️"
            critical_hooks=$((critical_hooks + 1))
        elif [ $duration -ge $WARNING_THRESHOLD ]; then
            status="${YELLOW}WARNING${NC}"
            symbol="⚠️"
            slow_hooks=$((slow_hooks + 1))
        else
            status="${GREEN}OK${NC}"
            symbol="✅"
        fi

        printf "%-35s %10d %s\n" "$name" "$duration" "$status"
    done

    echo ""
    echo -e "${BLUE}Summary:${NC}"
    echo ""

    # 计算平均时间
    if [ ${#names[@]} -gt 0 ]; then
        avg_time=$((total_time / ${#names[@]}))
        echo "  Average execution time: ${avg_time}ms"
        echo "  Total execution time:   ${total_time}ms"
        echo ""

        # 统计结果
        ok_hooks=$((${#names[@]} - slow_hooks - critical_hooks))
        echo "  Performance distribution:"
        echo "    ${GREEN}✅ OK (<${WARNING_THRESHOLD}ms):${NC}     $ok_hooks"
        echo "    ${YELLOW}⚠️  WARNING (>=${WARNING_THRESHOLD}ms):${NC} $slow_hooks"
        echo "    ${RED}⚠️⚠️ CRITICAL (>=${CRITICAL_THRESHOLD}ms):${NC} $critical_hooks"
    fi

    echo ""

    # 建议
    if [ $critical_hooks -gt 0 ]; then
        echo -e "${RED}⚠️⚠️ CRITICAL: Some hooks are very slow!${NC}"
        echo "   Recommendations:"
        echo "   - Consider adding caching mechanisms"
        echo "   - Optimize expensive operations"
        echo "   - Use background processing for non-critical hooks"
    elif [ $slow_hooks -gt 0 ]; then
        echo -e "${YELLOW}⚠️  WARNING: Some hooks are slow.${NC}"
        echo "   Recommendations:"
        echo "   - Review slow hooks for optimization opportunities"
    else
        echo -e "${GREEN}✅ All hooks are performing well!${NC}"
    fi

    echo ""
    echo "Log files created in: .claude/hooks/"
    echo ""
}

# 执行主流程
main "$@"
