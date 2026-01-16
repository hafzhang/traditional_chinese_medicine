#!/bin/bash
# Hook: suggest_fix
# Trigger: error
# Description: Suggest fixes based on error patterns

ERROR_MESSAGE="${CLAUDE_ERROR_MESSAGE:-unknown}"
LOG_FILE=".claude/hooks/fix_suggestions.log"
mkdir -p "$(dirname "$LOG_FILE")"

TIMESTAMP=$(date -Iseconds)

# Error pattern matching and suggestions
suggest_fix() {
    local error="$1"

    case "$error" in
        *"ModuleNotFound"*)
            echo "💡 Suggestion: Install missing module with 'pip install <module_name>'"
            ;;
        *"Permission denied"*)
            echo "💡 Suggestion: Check file permissions or run with appropriate access rights"
            ;;
        *"syntax error"*)
            echo "💡 Suggestion: Validate syntax using linter/formatter (e.g., pylint, black)"
            ;;
        *"import"*"cannot"*)
            echo "💡 Suggestion: Check Python path and module installation"
            ;;
        *"Connection"*"refused"*)
            echo "💡 Suggestion: Verify database/server is running and accessible"
            ;;
        *"authentication"*)
            echo "💡 Suggestion: Check credentials in .env file"
            ;;
        *"TypeError"*)
            echo "💡 Suggestion: Review data types being passed to functions"
            ;;
        *"KeyError"*)
            echo "💡 Suggestion: Verify dictionary keys exist before access"
            ;;
        *)
            echo "💡 Check logs at $LOG_FILE for details"
            ;;
    esac
}

# Log error and suggestion
cat >> "$LOG_FILE" << EOF
[$TIMESTAMP] Error: $ERROR_MESSAGE
EOF

# Output suggestion
suggest_fix "$ERROR_MESSAGE"

exit 0
