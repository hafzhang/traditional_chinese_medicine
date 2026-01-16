#!/bin/bash
# Hook: check_api_endpoint
# Trigger: tool-use (Write operation in api/* directories)
# Description: Validate API endpoint naming conventions

LOG_FILE=".claude/hooks/api_validation.log"
mkdir -p "$(dirname "$LOG_FILE")"

TIMESTAMP=$(date -Iseconds)
FILE_PATH="${CLAUDE_TOOL_INPUT_FILE_PATH:-unknown}"

# Only process files in api/* directories
if [[ "$FILE_PATH" != */api/* ]]; then
    exit 0
fi

# Read file content
FILE_CONTENT=$(cat "$FILE_PATH" 2>/dev/null || echo "")

# Validation rules
ERRORS=()
WARNINGS=()

# Rule 1: API routes should follow RESTful conventions
if echo "$FILE_CONTENT" | grep -E '@(app\.router|APIRouter)\.(get|post|put|delete|patch)'; then
    # Check if route starts with /api/v1/
    ROUTES=$(echo "$FILE_CONTENT" | grep -oP '(?<=get|post|put|delete|patch)\(["\x27]/[^"\x27]+["\x27]' || true)

    while IFS= read -r route; do
        route=$(echo "$route" | sed 's/["\x27]//g' | sed 's/^[^/]*//')
        if [[ ! "$route" =~ ^/api/v[0-9]+/ ]]; then
            if [[ "$route" =~ ^/ ]]; then
                WARNINGS+=("Route '$route' should follow /api/v{N} convention")
            fi
        fi
    done <<< "$ROUTES"
fi

# Rule 2: Check for snake_case function names in Python
if [[ "$FILE_PATH" == *.py ]]; then
    # Check for camelCase function definitions (should be snake_case)
    CAMEL_CASE_FUNCS=$(echo "$FILE_CONTENT" | grep -oP 'def\s+[a-z]+[A-Z]' || true)
    if [ -n "$CAMEL_CASE_FUNCS" ]; then
        WARNINGS+=("Use snake_case for function names, found: $CAMEL_CASE_FUNCS")
    fi
fi

# Rule 3: Endpoints should have docstrings
if echo "$FILE_CONTENT" | grep -E '@(app\.router|APIRouter)\.(get|post)'; then
    NEXT_LINE_COUNT=$(echo "$FILE_CONTENT" | grep -A1 '@(app\.router|APIRouter)\.(get|post)' | grep -c '"""' || true)
    if [ "$NEXT_LINE_COUNT" -lt 2 ]; then
        WARNINGS+=("API endpoint should have docstring")
    fi
fi

# Log results
if [ ${#ERRORS[@]} -gt 0 ] || [ ${#WARNINGS[@]} -gt 0 ]; then
    cat >> "$LOG_FILE" << EOF
[$TIMESTAMP] API Validation: $FILE_PATH
WARNINGS:
$(printf '  - %s\n' "${WARNINGS[@]}")
ERRORS:
$(printf '  - %s\n' "${ERRORS[@]}")
---
EOF

    if [ ${#WARNINGS[@]} -gt 0 ]; then
        echo "⚠️  API Warnings for $FILE_PATH:"
        printf '  - %s\n' "${WARNINGS[@]}"
    fi

    if [ ${#ERRORS[@]} -gt 0 ]; then
        echo "❌ API Errors in $FILE_PATH:"
        printf '  - %s\n' "${ERRORS[@]}"
        exit 1
    fi
fi

exit 0
