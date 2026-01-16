#!/bin/bash
# Hook: check_priority
# Trigger: user-prompt-submit
# Description: 检查任务优先级，防止偏离主线

USER_PROMPT="${CLAUDE_USER_PROMPT:-unknown}"
LOG_FILE=".claude/hooks/priority_checks.log"
RULES_FILE="priority.rules"

mkdir -p "$(dirname "$LOG_FILE")"

# 加载优先级规则
load_rules() {
    if [ ! -f "$RULES_FILE" ]; then
        return
    fi

    source "$RULES_FILE"
}

# 检查是否偏离 MVP 范围
check_mvp_scope() {
    local prompt="$1"

    # 非核心功能的关键词
    local non_mvp_patterns=(
        "社交.*功能"
        "积分.*商城"
        "AI.*舌诊"
        "企业.*服务"
        "会员.*体系"
        "积分.*系统"
        "好友.*PK"
        "话题.*挑战"
        "社区.*讨论"
        "消息.*推送"
        "实时.*通讯"
        "支付.*功能"
        "订单.*系统"
    )

    for pattern in "${non_mvp_patterns[@]}"; do
        if echo "$prompt" | grep -qiE "$pattern"; then
            echo "WARNING:NonMVP:$pattern"
            return 1
        fi
    done

    return 0
}

# 检查是否有未阻塞的高优先级任务
check_blocking_tasks() {
    local todo_file=".claude/todo.md"

    if [ ! -f "$todo_file" ]; then
        return 0
    fi

    # 查找标记为阻塞的任务
    local blocking_tasks=$(grep -E '\[!\]' "$todo_file" | wc -l)

    if [ $blocking_tasks -gt 0 ]; then
        echo "WARNING:BlockingTasks:$blocking_tasks"
        return 1
    fi

    return 0
}

# 评估任务优先级
assess_priority() {
    local prompt="$1"
    local priority=5  # 默认中等优先级

    # 高优先级关键词
    local high_priority_patterns=(
        "修复.*bug"
        "解决.*错误"
        "核心.*功能"
        "阻塞.*问题"
        "紧急.*修复"
        "无法.*继续"
    )

    # 低优先级关键词
    local low_priority_patterns=(
        "优化.*性能"
        "重构.*代码"
        "改进.*体验"
        "美化.*界面"
        "添加.*注释"
        "优化.*样式"
    )

    for pattern in "${high_priority_patterns[@]}"; do
        if echo "$prompt" | grep -qiE "$pattern"; then
            priority=1  # 最高优先级
            break
        fi
    done

    if [ $priority -eq 5 ]; then
        for pattern in "${low_priority_patterns[@]}"; do
            if echo "$prompt" | grep -qiE "$pattern"; then
                priority=9  # 最低优先级
                break
            fi
        done
    fi

    echo "$priority"
}

# 检查当前是否有更高优先级的任务
check_higher_priority_exists() {
    local current_priority=$1
    local todo_file=".claude/todo.md"

    if [ ! -f "$todo_file" ]; then
        return 0
    fi

    # 查找未完成的高优先级任务
    # 这里简化处理，实际可以更精细
    local urgent_tasks=$(grep -E '^\s*-.*\[.*\]' "$todo_file" | head -5 | wc -l)

    if [ $urgent_tasks -gt 5 ]; then
        echo "WARNING:TooManyPendingTasks:$urgent_tasks"
        return 1
    fi

    return 0
}

# 主逻辑
load_rules

# 记录日志
cat >> "$LOG_FILE" << EOF
[$(date -Iseconds)] Priority Check
Prompt: $USER_PROMPT
---

EOF

# 执行检查
MVP_CHECK=$(check_mvp_scope "$USER_PROMPT")
BLOCKING_CHECK=$(check_blocking_tasks)
PRIORITY=$(assess_priority "$USER_PROMPT")
HIGHER_PRIORITY_CHECK=$(check_higher_priority_exists "$PRIORITY")

# 处理警告
WARNINGS=0

if echo "$MVP_CHECK" | grep -q "WARNING"; then
    echo ""
    echo "⚠️  优先级警告: 任务可能超出 MVP 范围"
    echo ""
    reason=$(echo "$MVP_CHECK" | cut -d':' -f2)
    echo "检测到: $reason"
    echo ""
    echo "MVP 核心功能:"
    echo "  - 体质测试问卷"
    echo "  - 判定服务"
    echo "  - 基础报告生成"
    echo "  - 饮食推荐"
    echo "  - 结果可视化"
    echo "  - 分享卡片"
    echo ""
    echo "建议: 确认此任务是否为 MVP 必需功能"
    echo ""
    WARNINGS=$((WARNINGS + 1))
fi

if echo "$BLOCKING_CHECK" | grep -q "WARNING"; then
    count=$(echo "$BLOCKING_CHECK" | cut -d':' -f2)
    echo ""
    echo "⚠️  优先级警告: 存在 $count 个阻塞任务"
    echo ""
    echo "建议先处理标记为 [!] 的阻塞任务"
    echo ""
    WARNINGS=$((WARNINGS + 1))
fi

if echo "$HIGHER_PRIORITY_CHECK" | grep -q "WARNING"; then
    echo ""
    echo "⚠️  优先级警告: 待处理任务过多"
    echo ""
    echo "建议: 先完成当前正在进行的主线任务"
    echo ""
    WARNINGS=$((WARNINGS + 1))
fi

# 优先级显示
if [ $WARNINGS -eq 0 ]; then
    case $PRIORITY in
        1)
            echo "🔴 高优先级任务 - 立即处理"
            ;;
        2|3)
            echo "🟠 中高优先级任务"
            ;;
        4|5)
            echo "🟡 中等优先级任务"
            ;;
        6|7|8)
            echo "🟢 中低优先级任务"
            ;;
        9)
            echo "🔵 低优先级任务 - 可延后"
            ;;
    esac
    echo ""
fi

# 如果有警告，询问是否继续
if [ $WARNINGS -gt 0 ]; then
    echo "是否继续当前任务？"
    echo "  - 如继续，请在回复中明确说明 '继续' 或 '确认'"
    echo "  - 如需调整，请说明 '改为 [新任务]'"
    echo ""
    exit 1  # 需要确认
fi

exit 0
