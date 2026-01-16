#!/bin/bash
# Hook: verify_task_completion
# Trigger: pre-response
# Description: Verify all MVP checklist items are addressed

MVP_CHECKLIST_FILE=".claude/mvp_checklist.json"
LOG_FILE=".claude/hooks/completion_verification.log"
mkdir -p "$(dirname "$LOG_FILE")"

TIMESTAMP=$(date -Iseconds)

# Create checklist if not exists
if [ ! -f "$MVP_CHECKLIST_FILE" ]; then
    cat > "$MVP_CHECKLIST_FILE" << EOF
{
  "week_0": {
    "tasks": [
      {"id": "w0_1", "task": "确认30题问卷最终版本", "status": "pending"},
      {"id": "w0_2", "task": "确认首发平台", "status": "pending"},
      {"id": "w0_3", "task": "接口规范评审", "status": "pending"},
      {"id": "w0_4", "task": "食物库样例数据准备", "status": "pending"},
      {"id": "w0_5", "task": "设计稿评审", "status": "pending"}
    ]
  },
  "week_1": {
    "tasks": [
      {"id": "w1_backend_1", "task": "搭建 FastAPI 项目脚手架", "status": "pending"},
      {"id": "w1_backend_2", "task": "数据库表设计与迁移脚本", "status": "pending"},
      {"id": "w1_backend_3", "task": "实现 POST /api/v1/test/submit 接口", "status": "pending"},
      {"id": "w1_backend_4", "task": "实现体质判定算法", "status": "pending"},
      {"id": "w1_frontend_1", "task": "uni-app 项目初始化", "status": "pending"},
      {"id": "w1_frontend_2", "task": "问卷页面 UI 实现", "status": "pending"},
      {"id": "w1_frontend_3", "task": "答题流程与进度保存", "status": "pending"}
    ]
  }
}
EOF
fi

# Count completed vs pending tasks
COMPLETED=$(jq -r '[.[][].tasks[] | select(.status == "completed")] | length' "$MVP_CHECKLIST_FILE" 2>/dev/null || echo "0")
TOTAL=$(jq -r '[.[][].tasks[]] | length' "$MVP_CHECKLIST_FILE" 2>/dev/null || echo "0")

if [ "$TOTAL" -gt 0 ]; then
    PERCENT=$((COMPLETED * 100 / TOTAL))
    echo "📊 MVP Progress: $COMPLETED/$TOTAL tasks completed ($PERCENT%)"

    if [ $PERCENT -eq 100 ]; then
        echo "🎉 All MVP tasks completed!"
    elif [ $PERCENT -ge 75 ]; then
        echo "🚀 MVP is nearly complete!"
    fi
fi

exit 0
