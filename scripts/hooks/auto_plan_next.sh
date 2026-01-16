#!/bin/bash
# Hook: auto_plan_next
# Trigger: post-response
# Description: 自动规划下一个任务，从 todo.md 中提取并展示

TODO_FILE=".claude/todo.md"
NEXT_TASK_FILE=".claude/next_task.txt"
SESSION_LOG=".claude/hooks/session.log"

mkdir -p "$(dirname "$NEXT_TASK_FILE")"

# 获取当前时间
CURRENT_DATE=$(date +%Y-%m-%d)
CURRENT_TIME=$(date +%H:%M)

# 检查 todo.md 是否存在
if [ ! -f "$TODO_FILE" ]; then
    echo "⚠️  TODO 文件不存在: $TODO_FILE"
    exit 0
fi

# 查找当前未完成的第一个任务
find_next_task() {
    local in_current_section=false
    local current_task=""
    local task_number=0
    local found=false

    while IFS= read -r line; do
        # 跳过空行和注释
        [[ "$line" =~ ^[[:space:]]*$ ]] && continue
        [[ "$line" =~ ^[[:space:]]*# ]] && continue

        # 检测是否在当前日期目标中
        if [[ "$line" =~ ##[[:space:]]今日目标[[:space:]]*\(([0-9]{4}-[0-9]{2}-[0-9]{2})\) ]]; then
            local task_date="${BASH_REMATCH[1]}"
            if [ "$task_date" = "$CURRENT_DATE" ]; then
                in_current_section=true
            else
                in_current_section=false
            fi
            continue
        fi

        # 如果离开了今日目标部分
        if [[ "$line" =~ ^## ]] && [ "$in_current_section" = true ]; then
            break
        fi

        # 只处理今日目标中的任务
        if [ "$in_current_section" = true ]; then
            # 查找未完成的任务
            if [[ "$line" =~ ^[[:space:]]*-[[:space:]]\[[[:space:]]*\] ]]; then
                task_number=$((task_number + 1))
                current_task="$line"

                # 跳过已跳过的任务
                if [[ "$line" =~ \[-\] ]]; then
                    continue
                fi

                # 找到第一个未完成的任务
                found=true
                break
            fi
        fi
    done < "$TODO_FILE"

    if [ "$found" = true ]; then
        echo "$current_task"
    else
        echo ""
    fi
}

# 主逻辑
NEXT_TASK=$(find_next_task)

if [ -n "$NEXT_TASK" ]; then
    # 清理任务文本，提取纯任务描述
    TASK_DESC=$(echo "$NEXT_TASK" | sed 's/^[[:space:]]*-[[:space:]]*\[[[:space:]]*[x!-]\?[[:space:]]*\][[:space:]]*//')

    # 保存到文件
    echo "$TASK_DESC" > "$NEXT_TASK_FILE"

    # 统计今日进度
    TOTAL_TASKS=$(grep -E '^\s*-\s*\[[ x\-!]\]' "$TODO_FILE" | wc -l)
    COMPLETED_TASKS=$(grep -E '^\s*-\s*\[x\]' "$TODO_FILE" | wc -l)
    PROGRESS=$((COMPLETED_TASKS * 100 / TOTAL_TASKS))

    # 检查是否全部完成
    if [ $COMPLETED_TASKS -eq $TOTAL_TASKS ]; then
        echo ""
        echo "=========================================="
        echo "🎉 今日目标达成！"
        echo "=========================================="
        echo ""
        echo "✅ 所有 $TOTAL_TASKS 个任务已完成"
        echo "📊 完成率: 100%"
        echo "🕐 完成时间: $CURRENT_TIME"
        echo ""
        echo "🌟 出色的工作！休息一下吧~"
        echo ""
        echo "=========================================="
        echo ""
        exit 0
    fi

    # 输出下一个任务提示
    cat << 'EOF'

═══════════════════════════════════════════════════════════════
                    📋 下一个任务
═══════════════════════════════════════════════════════════════

EOF

    # 使用颜色和格式化输出
    printf "  ⏭️  %s\n" "$TASK_DESC"
    echo ""
    printf "  📊 今日进度: %d/%d 完成 (%d%%)\n" "$COMPLETED_TASKS" "$TOTAL_TASKS" "$PROGRESS"
    echo ""
    printf "  💡 提示: 完成后请在 todo.md 中将 [ ] 改为 [x]\n"
    echo ""
    printf "  📝 文件位置: %s\n" "$TODO_FILE"
    echo ""

    cat << 'EOF'
═══════════════════════════════════════════════════════════════

EOF

    # 记录到会话日志
    echo "[$CURRENT_DATE $CURRENT_TIME] Next task: $TASK_DESC" >> "$SESSION_LOG"

    exit 0
else
    echo ""
    echo "🎉 恭喜！今日所有任务已完成！"
    echo ""
    echo "现在可以:"
    echo "  1. 查看整体进度: cat .claude/todo.md"
    echo "  2. 开始明天的任务: 编辑 todo.md 中的日期"
    echo "  3. 添加新任务到 todo.md"
    echo ""
    exit 0
fi
