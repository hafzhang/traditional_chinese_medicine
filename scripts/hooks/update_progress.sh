#!/bin/bash
# Hook: update_progress
# Trigger: post-response
# Description: Update MVP development progress tracker

PROGRESS_FILE=".claude/progress.json"
LOG_FILE=".claude/hooks/progress_updates.log"
mkdir -p "$(dirname "$LOG_FILE")"

TIMESTAMP=$(date -Iseconds)

# Initialize progress file if not exists
if [ ! -f "$PROGRESS_FILE" ]; then
    cat > "$PROGRESS_FILE" << EOF
{
  "mvp_deadline_days": 21,
  "days_elapsed": 0,
  "current_week": 0,
  "tasks_completed": 0,
  "tasks_total": 21,
  "last_updated": "$TIMESTAMP"
}
EOF
fi

# Update progress
CURRENT_WEEK=$(jq -r '.current_week' "$PROGRESS_FILE")
TASKS_COMPLETED=$(jq -r '.tasks_completed' "$PROGRESS_FILE")

# Calculate days since last update
LAST_UPDATED=$(jq -r '.last_updated' "$PROGRESS_FILE")
if [ "$LAST_UPDATED" != "$TIMESTAMP" ]; then
    DAYS_SINCE_UPDATE=$(( ($(date +%s) - $(date -d "$LAST_UPDATED" +%s 2>/dev/null || echo "0")) / 86400 ))
    if [ "$DAYS_SINCE_UPDATE" -gt 0 ]; then
        NEW_DAYS_ELAPSED=$(jq -r ".days_elapsed + $DAYS_SINCE_UPDATE" "$PROGRESS_FILE")
        jq --arg new_days "$NEW_DAYS_ELAPSED" '.days_elapsed = ($new_days | tonumber)' "$PROGRESS_FILE" > "$PROGRESS_FILE.tmp" && mv "$PROGRESS_FILE.tmp" "$PROGRESS_FILE"
    fi
fi

# Update timestamp
jq --arg ts "$TIMESTAMP" '.last_updated = $ts' "$PROGRESS_FILE" > "$PROGRESS_FILE.tmp" && mv "$PROGRESS_FILE.tmp" "$PROGRESS_FILE"

# Log update
cat >> "$LOG_FILE" << EOF
[$TIMESTAMP] Progress updated
Week: $CURRENT_WEEK
Tasks: $TASKS_COMPLETED completed
---
EOF

exit 0
