#!/bin/bash
# Hook: validate_python_code
# Trigger: tool-use (Write operation on *.py files)
# Description: Validate Python code syntax before Write operation

LOG_FILE=".claude/hooks/validation.log"
mkdir -p "$(dirname "$LOG_FILE")"

# Get file path from tool input
FILE_PATH="${CLAUDE_TOOL_INPUT_FILE_PATH:-unknown}"

TIMESTAMP=$(date -Iseconds)

if [ "$FILE_PATH" != "unknown" ] && [[ "$FILE_PATH" == *.py ]]; then
    # Syntax check using Python
    if python3 -m py_compile "$FILE_PATH" 2>/dev/null; then
        echo "✅ Python syntax OK: $FILE_PATH"
        exit 0
    else
        ERROR=$(python3 -m py_compile "$FILE_PATH" 2>&1)
        cat >> "$LOG_FILE" << EOF
[$TIMESTAMP] ❌ Python Syntax Error
File: $FILE_PATH
Error: $ERROR
---
EOF
        echo "❌ Python syntax error in $FILE_PATH"
        echo "Error: $ERROR"
        exit 1
    fi
fi

exit 0
