#!/bin/bash
# Hook: log_error
# Trigger: error
# Description: Log all errors with context for debugging

LOG_FILE=".claude/hooks/error_log.log"
mkdir -p "$(dirname "$LOG_FILE")"

TIMESTAMP=$(date -Iseconds)
ERROR_MESSAGE="${CLAUDE_ERROR_MESSAGE:-unknown}"
USER_PROMPT="${CLAUDE_USER_PROMPT:-unknown}"
TOOL_NAME="${CLAUDE_TOOL_NAME:-none}"

cat >> "$LOG_FILE" << EOF
{
  "timestamp": "$TIMESTAMP",
  "error": "$(echo "$ERROR_MESSAGE" | sed 's/"/\\"/g')",
  "user_prompt": "$(echo "$USER_PROMPT" | sed 's/"/\\"/g')",
  "tool_name": "$TOOL_NAME",
  "session_id": "${CLAUDE_SESSION_ID:-unknown}"
}
EOF

echo "❌ Error logged to $LOG_FILE"
exit 0
