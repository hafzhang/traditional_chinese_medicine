#!/bin/bash
# Hook: log_session_summary
# Trigger: post-response
# Description: Log session summary and token usage

LOG_FILE=".claude/hooks/sessions.log"
mkdir -p "$(dirname "$LOG_FILE")"

TIMESTAMP=$(date -Iseconds)
SESSION_ID="${CLAUDE_SESSION_ID:-unknown}"
TOKENS_USED="${CLAUDE_TOKENS_USED:-0}"
MODEL="${CLAUDE_MODEL:-unknown}"

cat >> "$LOG_FILE" << EOF
{
  "timestamp": "$TIMESTAMP",
  "session_id": "$SESSION_ID",
  "tokens_used": $TOKENS_USED,
  "model": "$MODEL",
  "user": "${CLAUDE_USER:-unknown}"
}
EOF

# Keep log manageable
tail -n 1000 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"

exit 0
