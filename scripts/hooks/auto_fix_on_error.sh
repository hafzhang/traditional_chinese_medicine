#!/bin/bash
# Hook: auto_fix_on_error
# Trigger: When specific error types occur
# Description: Automatically attempt to fix errors based on file type and error pattern

ERROR_MESSAGE="${CLAUDE_ERROR_MESSAGE:-unknown}"
FILE_PATH="${CLAUDE_TOOL_INPUT_FILE_PATH:-unknown}"
LOG_FILE=".claude/hooks/auto_fix_errors.log"

mkdir -p "$(dirname "$LOG_FILE")"

TIMESTAMP=$(date -Iseconds)

# Exit if no file context
if [ "$FILE_PATH" = "unknown" ]; then
    exit 0
fi

# Exit if file doesn't exist
if [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

echo "🔧 Auto-fix triggered by error: $ERROR_MESSAGE"
echo "   File: $FILE_PATH"

# Get file extension
FILE_EXT="${FILE_PATH##*.}"

# Determine error type and fix strategy
ERROR_TYPE="unknown"
AUTO_FIX_SCRIPT=""

# Classify error type
if echo "$ERROR_MESSAGE" | grep -qi "SyntaxError\|syntax error\|parse error"; then
    ERROR_TYPE="syntax"
elif echo "$ERROR_MESSAGE" | grep -qi "ValidationError\|validation\|invalid"; then
    ERROR_TYPE="validation"
elif echo "$ERROR_MESSAGE" | grep -qi "TypeError\|type error"; then
    ERROR_TYPE="type"
elif echo "$ERROR_MESSAGE" | grep -qi "ImportError\|ModuleNotFoundError"; then
    ERROR_TYPE="import"
fi

# Select auto-fix script based on file type and error
case "$FILE_EXT" in
    py)
        case "$ERROR_TYPE" in
            syntax|validation)
                AUTO_FIX_SCRIPT="auto_fix_python.sh"
                ;;
            import)
                # Try to fix import errors
                echo "  🔧 Attempting to fix import error..."

                MISSING_MODULE=$(echo "$ERROR_MESSAGE" | grep -oP "No module named '\K[^']*" || echo "")
                if [ -n "$MISSING_MODULE" ]; then
                    echo "  ℹ️  Missing module: $MISSING_MODULE"
                    echo "  💡 Run: pip install $MISSING_MODULE"
                fi

                # Try to add missing import statement
                if [ "$MISSING_MODULE" = "fastapi" ]; then
                    if ! grep -q "from fastapi import" "$FILE_PATH"; then
                        # This is a simple heuristic - would need more sophisticated handling
                        echo "  💡 Consider adding: from fastapi import APIRouter"
                    fi
                fi

                AUTO_FIX_SCRIPT="auto_fix_python.sh"
                ;;
            *)
                AUTO_FIX_SCRIPT="auto_fix_python.sh"
                ;;
        esac
        ;;

    sql)
        AUTO_FIX_SCRIPT="auto_fix_sql.sh"
        ;;

    *)
        echo "  ℹ️  No auto-fix available for file type: .$FILE_EXT"
        exit 0
        ;;
esac

# Attempt auto-fix
if [ -n "$AUTO_FIX_SCRIPT" ] && [ -f "scripts/hooks/$AUTO_FIX_SCRIPT" ]; then
    echo "  🔧 Running auto-fix script: $AUTO_FIX_SCRIPT"

    export CLAUDE_TOOL_INPUT_FILE_PATH="$FILE_PATH"
    export CLAUDE_ERROR_MESSAGE="$ERROR_MESSAGE"

    if bash "scripts/hooks/$AUTO_FIX_SCRIPT" 2>&1; then
        echo "  ✅ Auto-fix applied successfully"

        # Log successful fix
        cat >> "$LOG_FILE" << EOF
[$TIMESTAMP] Auto-fix SUCCESS
File: $FILE_PATH
Error type: $ERROR_TYPE
Script: $AUTO_FIX_SCRIPT
---
EOF

        exit 0
    else
        echo "  ⚠️  Auto-fix failed or no changes needed"

        # Log failed fix
        cat >> "$LOG_FILE" << EOF
[$TIMESTAMP] Auto-fix FAILED
File: $FILE_PATH
Error type: $ERROR_TYPE
Script: $AUTO_FIX_SCRIPT
---
EOF

        exit 1
    fi
else
    echo "  ℹ️  No auto-fix script available"

    cat >> "$LOG_FILE" << EOF
[$TIMESTAMP] No auto-fix available
File: $FILE_PATH
Error type: $ERROR_TYPE
File extension: $FILE_EXT
---
EOF

    exit 1
fi
