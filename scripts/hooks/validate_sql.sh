#!/bin/bash
# Hook: validate_sql_schema
# Trigger: tool-use (Write operation on migration SQL files)
# Description: Validate SQL schema changes for MVP compliance

LOG_FILE=".claude/hooks/sql_validation.log"
mkdir -p "$(dirname "$LOG_FILE")"

TIMESTAMP=$(date -Iseconds)
FILE_PATH="${CLAUDE_TOOL_INPUT_FILE_PATH:-unknown}"

# Only process SQL migration files
if [[ "$FILE_PATH" != *migration*.sql ]]; then
    exit 0
fi

# Read SQL content
SQL_CONTENT=$(cat "$FILE_PATH" 2>/dev/null || echo "")

# Validation checks
ERRORS=()
WARNINGS=()

# Check 1: DROP TABLE without backup
if echo "$SQL_CONTENT" | grep -qi "DROP TABLE"; then
    if ! echo "$SQL_CONTENT" | grep -qi "BACKUP\|COPY\|dump"; then
        WARNINGS+=("DROP TABLE detected without backup statement")
    fi
fi

# Check 2: Missing indexes on foreign keys
if echo "$SQL_CONTENT" | grep -qi "FOREIGN KEY"; then
    if ! echo "$SQL_CONTENT" | grep -qi "CREATE INDEX\|ADD INDEX"; then
        WARNINGS+=("Foreign key detected without index")
    fi
fi

# Check 3: Missing created_at timestamp
if echo "$SQL_CONTENT" | grep -qi "CREATE TABLE"; then
    if ! echo "$SQL_CONTENT" | grep -qi "created_at"; then
        WARNINGS+=("New table missing created_at column")
    fi
fi

# Log results
if [ ${#ERRORS[@]} -gt 0 ] || [ ${#WARNINGS[@]} -gt 0 ]; then
    cat >> "$LOG_FILE" << EOF
[$TIMESTAMP] SQL Validation: $FILE_PATH
WARNINGS:
$(printf '  - %s\n' "${WARNINGS[@]}")
ERRORS:
$(printf '  - %s\n' "${ERRORS[@]}")
---
EOF

    if [ ${#WARNINGS[@]} -gt 0 ]; then
        echo "⚠️  SQL Warnings for $FILE_PATH:"
        printf '  - %s\n' "${WARNINGS[@]}"
    fi

    if [ ${#ERRORS[@]} -gt 0 ]; then
        echo "❌ SQL Errors in $FILE_PATH:"
        printf '  - %s\n' "${ERRORS[@]}"
        exit 1
    fi
fi

echo "✅ SQL validation passed: $FILE_PATH"
exit 0
