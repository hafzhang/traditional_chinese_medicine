#!/bin/bash
# Hook: track_file_changes
# Trigger: tool-use (Write or Edit operations)
# Description: Track all file write operations for change tracking

LOG_FILE=".claude/hooks/file_changes.log"
mkdir -p "$(dirname "$LOG_FILE")"

TIMESTAMP=$(date -Iseconds)
TOOL_NAME="${CLAUDE_TOOL_NAME:-unknown}"
FILE_PATH="${CLAUDE_TOOL_INPUT_FILE_PATH:-unknown}"

# Log the change
cat >> "$LOG_FILE" << EOF
[$TIMESTAMP] $TOOL_NAME
File: $FILE_PATH
User: ${CLAUDE_USER:-unknown}
---
EOF

# Keep log manageable
tail -n 500 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"

exit 0
