#!/bin/bash
# Hook: log_user_request
# Trigger: user-prompt-submit
# Description: Log all user requests for tracking and analysis

LOG_FILE=".claude/hooks/requests.log"
mkdir -p "$(dirname "$LOG_FILE")"

# Get user prompt from environment
USER_PROMPT="${CLAUDE_USER_PROMPT:-unknown}"
TIMESTAMP=$(date -Iseconds)

# Log entry
cat >> "$LOG_FILE" << EOF
{
  "timestamp": "$TIMESTAMP",
  "prompt": "$(echo "$USER_PROMPT" | sed 's/"/\\"/g')",
  "session_id": "${CLAUDE_SESSION_ID:-unknown}",
  "model": "${CLAUDE_MODEL:-unknown}"
}
EOF

# Keep only last 1000 entries
tail -n 1000 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
