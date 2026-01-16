#!/bin/bash
# Claude Code Hooks Log Size Control Test
# 测试日志文件大小限制机制

set -e

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033=1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
MAX_LINES=1000  # 与 hooks 脚本中的限制一致
TEST_ENTRIES=1500  # 生成超过限制的条目数

print_header() {
    echo ""
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}======================================${NC}"
    echo ""
}

test_log_limit() {
    local log_file=$1
    local log_name=$2
    local max_lines=$3

    echo -e "${YELLOW}Testing: $log_name${NC}"
    echo "  Log file: $log_file"
    echo "  Max lines: $max_lines"
    echo ""

    # 清空日志
    > "$log_file"

    # 生成测试数据
    echo "  Generating $TEST_ENTRIES entries..."

    for i in $(seq 1 $TEST_ENTRIES); do
        case "$log_name" in
            "requests.log")
                export CLAUDE_USER_PROMPT="Test request $i"
                export CLAUDE_SESSION_ID="test-$i"
                bash scripts/hooks/log_request.sh 2>/dev/null
                ;;
            "sessions.log")
                export CLAUDE_SESSION_ID="test-$i"
                export CLAUDE_TOKENS_USED=1000
                bash scripts/hooks/log_session.sh 2>/dev/null
                ;;
            "file_changes.log")
                export CLAUDE_TOOL_NAME="Write"
                export CLAUDE_TOOL_INPUT_FILE_PATH="test_file_$i.py"
                bash scripts/hooks/track_changes.sh 2>/dev/null
                ;;
        esac

        # 显示进度
        if [ $((i % 500)) -eq 0 ]; then
            echo -n "    $i entries..."
        fi
    done

    echo ""
    echo ""

    # 统计结果
    if [ -f "$log_file" ]; then
        line_count=$(wc -l < "$log_file")
        file_size=$(wc -c < "$log_file")
        file_size_kb=$((file_size / 1024))

        echo "  Results:"
        echo "    Entries generated: $TEST_ENTRIES"
        echo "    Lines in log:      $line_count"
        echo "    File size:         ${file_size_kb}KB"
        echo ""

        # 验证限制
        if [ $line_count -le $max_lines ]; then
            echo -e "    ${GREEN}✅ Log size control working${NC}"
            echo -e "    ${GREEN}   (limited to $max_lines lines)${NC}"
            return 0
        else
            echo -e "    ${RED}❌ Log size exceeds limit!${NC}"
            echo -e "    ${RED}   Expected max: $max_lines, got: $line_count${NC}"
            return 1
        fi
    else
        echo -e "    ${RED}❌ Log file not created${NC}"
        return 1
    fi
}

main() {
    print_header "Log Size Control Test"

    # 确保目录存在
    mkdir -p .claude/hooks tests/temp

    echo "Configuration:"
    echo "  Max lines per log:  $MAX_LINES"
    echo "  Test entries:       $TEST_ENTRIES"
    echo ""

    # 测试结果统计
    total_tests=0
    passed_tests=0
    failed_tests=0

    # 测试 requests.log
    total_tests=$((total_tests + 1))
    if test_log_limit ".claude/hooks/requests.log" "requests.log" 1000; then
        passed_tests=$((passed_tests + 1))
    else
        failed_tests=$((failed_tests + 1))
    fi

    echo ""
    echo "---"
    echo ""

    # 测试 sessions.log
    total_tests=$((total_tests + 1))
    if test_log_limit ".claude/hooks/sessions.log" "sessions.log" 1000; then
        passed_tests=$((passed_tests + 1))
    else
        failed_tests=$((failed_tests + 1))
    fi

    echo ""
    echo "---"
    echo ""

    # 测试 file_changes.log
    total_tests=$((total_tests + 1))
    if test_log_limit ".claude/hooks/file_changes.log" "file_changes.log" 500; then
        passed_tests=$((passed_tests + 1))
    else
        failed_tests=$((failed_tests + 1))
    fi

    # 汇总结果
    echo ""
    print_header "Summary"

    echo "Total tests:  $total_tests"
    echo -e "${GREEN}Passed:       $passed_tests${NC}"
    echo -e "${RED}Failed:       $failed_tests${NC}"
    echo ""

    # 检查日志文件是否存在
    echo "Log files created:"
    for log_file in .claude/hooks/*.log; do
        if [ -f "$log_file" ]; then
            size=$(wc -c < "$log_file")
            size_kb=$((size / 1024))
            lines=$(wc -l < "$log_file")
            echo "  $(basename $log_file): ${lines} lines, ${size_kb}KB"
        fi
    done

    echo ""

    if [ $failed_tests -eq 0 ]; then
        echo -e "${GREEN}======================================${NC}"
        echo -e "${GREEN}✅ All log size control tests PASSED${NC}"
        echo -e "${GREEN}======================================${NC}"
        exit 0
    else
        echo -e "${RED}======================================${NC}"
        echo -e "${RED}❌ Some log size control tests FAILED${NC}"
        echo -e "${RED}======================================${NC}"
        exit 1
    fi
}

main "$@"
