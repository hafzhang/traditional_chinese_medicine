#!/bin/bash
# Claude Code Hooks Concurrent Execution Test
# 测试多个 hooks 并发执行时的性能和正确性

set -e

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
CONCURRENT_JOBS=20
TOTAL_REQUESTS=100

print_header() {
    echo ""
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}======================================${NC}"
    echo ""
}

main() {
    print_header "Concurrent Hook Execution Test"

    # 确保日志目录存在
    mkdir -p .claude/hooks

    echo "Configuration:"
    echo "  Concurrent jobs: $CONCURRENT_JOBS"
    echo "  Total requests:   $TOTAL_REQUESTS"
    echo ""

    # 清空现有日志
    > .claude/hooks/requests.log
    > .claude/hooks/sessions.log

    echo -e "${YELLOW}Running concurrent tests...${NC}"
    echo ""

    # 记录开始时间
    start_time=$(date +%s)

    # 并发执行多个 hook 调用
    for i in $(seq 1 $TOTAL_REQUESTS); do
        (
            export CLAUDE_SESSION_ID="concurrent-test-$i"
            export CLAUDE_USER_PROMPT="Concurrent test request $i"
            export CLAUDE_MODEL="claude-opus-4-5"
            export CLAUDE_TOKENS_USED=$((1000 + RANDOM % 5000))

            # 执行多个 hooks
            bash scripts/hooks/log_request.sh 2>/dev/null
            bash scripts/hooks/detect_feature.sh 2>/dev/null
            bash scripts/hooks/log_session.sh 2>/dev/null
        ) &

        # 控制并发数
        if [ $((i % CONCURRENT_JOBS)) -eq 0 ]; then
            wait
            echo -n "."
        fi
    done

    wait
    echo ""

    # 记录结束时间
    end_time=$(date +%s)
    duration=$((end_time - start_time))

    echo ""
    echo -e "${BLUE}Results:${NC}"
    echo ""

    # 统计日志行数
    request_lines=$(wc -l < .claude/hooks/requests.log 2>/dev/null || echo "0")
    session_lines=$(wc -l < .claude/hooks/sessions.log 2>/dev/null || echo "0")

    expected_lines=$((TOTAL_REQUESTS * 3))  # 每个请求执行3个hooks

    echo "Log file statistics:"
    echo "  Requests logged:  $request_lines (expected: ~$TOTAL_REQUESTS)"
    echo "  Sessions logged:  $session_lines (expected: ~$TOTAL_REQUESTS)"
    echo "  Total duration:   ${duration}s"
    echo ""

    # 计算成功率
    request_success=0
    if [ $TOTAL_REQUESTS -gt 0 ]; then
        request_success=$((request_lines * 100 / TOTAL_REQUESTS))
    fi

    session_success=0
    if [ $TOTAL_REQUESTS -gt 0 ]; then
        session_success=$((session_lines * 100 / TOTAL_REQUESTS))
    fi

    echo "Success rate:"
    echo "  Request logging: ${request_success}%"
    echo "  Session logging: ${session_success}%"
    echo ""

    # 检查数据完整性
    echo -e "${YELLOW}Data integrity check:${NC}"

    # 检查是否有重复的 session_id
    duplicates=$(grep -o 'concurrent-test-[0-9]*' .claude/hooks/requests.log 2>/dev/null | sort | uniq -d | wc -l)

    if [ $duplicates -eq 0 ]; then
        echo -e "  ${GREEN}✅ No duplicate session IDs${NC}"
    else
        echo -e "  ${RED}❌ Found $duplicates duplicate session IDs${NC}"
    fi

    # 检查日志格式
    invalid_json=0
    if [ -f .claude/hooks/requests.log ]; then
        while IFS= read -r line; do
            if ! echo "$line" | jq . >/dev/null 2>&1; then
                invalid_json=$((invalid_json + 1))
            fi
        done < .claude/hooks/requests.log
    fi

    if [ $invalid_json -eq 0 ]; then
        echo -e "  ${GREEN}✅ All log entries are valid JSON${NC}"
    else
        echo -e "  ${RED}❌ Found $invalid_json invalid JSON entries${NC}"
    fi

    # 性能评估
    echo ""
    echo -e "${YELLOW}Performance metrics:${NC}"

    if [ $duration -gt 0 ]; then
        rps=$((TOTAL_REQUESTS / duration))
        echo "  Requests per second: $rps"
    fi

    # 最终评估
    echo ""
    if [ $request_success -ge 95 ] && [ $session_success -ge 95 ] && [ $duplicates -eq 0 ]; then
        echo -e "${GREEN}======================================${NC}"
        echo -e "${GREEN}✅ Concurrent test PASSED${NC}"
        echo -e "${GREEN}======================================${NC}"
        exit 0
    else
        echo -e "${RED}======================================${NC}"
        echo -e "${RED}❌ Concurrent test FAILED${NC}"
        echo -e "${RED}======================================${NC}"
        exit 1
    fi
}

main "$@"
