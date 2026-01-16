#!/bin/bash
# Hook: load_small_template
# Trigger: user-prompt-submit (当检测到大型任务时)
# Description: 检测大型任务并建议/自动拆分为小型子任务

USER_PROMPT="${CLAUDE_USER_PROMPT:-unknown}"
LOG_FILE=".claude/hooks/task_breakdown.log"
RETRY_FILE=".claude/retry_counter.json"
TASK_TEMPLATES_DIR="task_templates"

mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$TASK_TEMPLATES_DIR"

# 检测任务复杂度的关键词
COMPLEXITY_PATTERNS=(
    "实现.*完整.*功能"           # 完整功能实现
    "搭建.*整个.*系统"           # 整个系统
    "开发.*所有.*接口"           # 所有接口
    "完成.*全.*流程"             # 全流程
    "从.*到.*完整.*实现"         # 端到端
    "集成.*多个.*模块"           # 多模块集成
    "重构.*全部.*代码"           # 全部重构
)

# 评估任务复杂度
estimate_complexity() {
    local prompt="$1"
    local complexity_score=0
    local reasons=()

    # 检查复杂模式
    for pattern in "${COMPLEXITY_PATTERNS[@]}"; do
        if echo "$prompt" | grep -qiE "$pattern"; then
            complexity_score=$((complexity_score + 3))
            reasons+=("检测到复杂模式: $pattern")
        fi
    done

    # 检查任务长度
    word_count=$(echo "$prompt" | wc -w)
    if [ $word_count -gt 50 ]; then
        complexity_score=$((complexity_score + 2))
        reasons+=("任务描述过长: ${word_count} 词")
    fi

    # 检查是否包含多个步骤
    and_count=$(echo "$prompt" | grep -oi "和\|以及\|并" | wc -l)
    if [ $and_count -ge 2 ]; then
        complexity_score=$((complexity_score + 2))
        reasons+=("包含多个子任务: ${and_count} 个连接词")
    fi

    # 检查是否包含时间限制相关词汇
    if echo "$prompt" | grep -qi "尽快\|立即\|现在\|今天.*完成"; then
        complexity_score=$((complexity_score + 1))
        reasons+=("有紧急时间要求")
    fi

    echo "$complexity_score"
}

# 检查重试次数
check_retry_count() {
    local task_hash=$(echo "$1" | md5sum | cut -d' ' -f1)

    if [ -f "$RETRY_FILE" ]; then
        local retry_count=$(jq -r --arg hash "$task_hash" '.[$hash] // 0' "$RETRY_FILE" 2>/dev/null || echo "0")
        echo "$retry_count"
    else
        echo "0"
    fi
}

# 增加重试计数
increment_retry() {
    local task_hash=$(echo "$1" | md5sum | cut -d' ' -f1)

    if [ ! -f "$RETRY_FILE" ]; then
        echo "{}" > "$RETRY_FILE"
    fi

    local current_count=$(check_retry_count "$1")
    local new_count=$((current_count + 1))

    jq --arg hash "$task_hash" --argjson count "$new_count" '. + {($hash): $count}' "$RETRY_FILE" > "$RETRY_FILE.tmp"
    mv "$RETRY_FILE.tmp" "$RETRY_FILE"

    echo "$new_count"
}

# 主逻辑
COMPLEXITY=$(estimate_complexity "$USER_PROMPT")
TASK_HASH=$(echo "$USER_PROMPT" | md5sum | cut -d' ' -f1)
RETRY_COUNT=$(check_retry_count "$USER_PROMPT")

# 复杂度阈值
COMPLEXITY_THRESHOLD=5
RETRY_THRESHOLD=3

# 记录日志
cat >> "$LOG_FILE" << EOF
[$(date -Iseconds)] Task Analysis
Prompt: $USER_PROMPT
Complexity: $COMPLEXITY
Retry Count: $RETRY_COUNT
---

EOF

# 判断是否需要干预
if [ $COMPLEXITY -ge $COMPLEXITY_THRESHOLD ]; then
    echo ""
    echo "⚠️  检测到复杂任务！"
    echo ""
    echo "任务: $USER_PROMPT"
    echo "复杂度评分: $COMPLEXITY (阈值: $COMPLEXITY_THRESHOLD)"
    echo ""
    echo "建议: 将任务拆分为更小的子任务"
    echo ""

    # 建议的拆分模板
    cat << 'EOF'
推荐拆分方式:

1. 按功能模块拆分
   - 先实现核心功能
   - 再实现辅助功能

2. 按开发阶段拆分
   - 数据结构设计
   - 接口定义
   - 核心逻辑
   - 测试验证

3. 按文件/组件拆分
   - 每次只修改 1-2 个文件
   - 每个文件专注单一职责

建议操作:
1. 使用 TodoWrite 工具创建子任务列表
2. 按优先级逐个完成
3. 每完成一个子任务后更新 todo.md

EOF

    # 增加重试计数
    NEW_RETRY=$(increment_retry "$USER_PROMPT")

    if [ $NEW_RETRY -ge $RETRY_THRESHOLD ]; then
        echo ""
        echo "🚨 任务重试次数过多 ($NEW_RETRY/$RETRY_THRESHOLD)"
        echo ""
        echo "可能存在以下问题:"
        echo "  - 任务定义不清晰"
        echo "  - 缺少必要的前置条件"
        echo "  - 技术难度被低估"
        echo ""
        echo "建议: 人工介入重新评估任务"
        echo ""
        exit 1  # 强制停机
    fi

    exit 1  # 阻止当前任务，要求拆分
fi

# 检查是否陷入死循环（同一任务反复重试）
if [ $RETRY_COUNT -ge $RETRY_THRESHOLD ]; then
    echo ""
    echo "🚨 检测到可能的死循环！"
    echo ""
    echo "任务已被重试 $RETRY_COUNT 次"
    echo "建议: 人工介入检查"
    echo ""
    echo "可能的原因:"
    echo "  - 代码中的 bug 导致持续失败"
    echo "  - 环境配置问题"
    echo "  - 依赖项缺失"
    echo "  - 需求理解偏差"
    echo ""
    exit 1  # 强制停机
fi

# 任务复杂度适中，允许继续
exit 0
