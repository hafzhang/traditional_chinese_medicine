#!/bin/bash
# Hook: auto_fix_sql
# Trigger: After SQL validation fails
# Description: Automatically fix common SQL schema issues

FILE_PATH="${CLAUDE_TOOL_INPUT_FILE_PATH:-unknown}"
LOG_FILE=".claude/hooks/auto_fix_sql.log"
FIX_LOG=".claude/hooks/sql_fixes_applied.log"

mkdir -p "$(dirname "$LOG_FILE")"

TIMESTAMP=$(date -Iseconds)

# Only process SQL files
if [[ "$FILE_PATH" != *.sql ]]; then
    exit 0
fi

# Check if file exists
if [ ! -f "$FILE_PATH" ]; then
    echo "⚠️  File not found: $FILE_PATH"
    exit 1
fi

echo "🔧 Attempting to auto-fix SQL issues in: $FILE_PATH"

# Read original content
ORIGINAL_CONTENT=$(cat "$FILE_PATH")
FIXED_CONTENT="$ORIGINAL_CONTENT"
FIXES_APPLIED=()

# Fix 1: Add created_at if missing
if ! echo "$FIXED_CONTENT" | grep -qi "created_at"; then
    FIXED_CONTENT=$(echo "$FIXED_CONTENT" | sed '/CREATE TABLE/a\    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
    FIXES_APPLIED+=("Added created_at column")
fi

# Fix 2: Add updated_at if missing and it's a CREATE TABLE
if echo "$FIXED_CONTENT" | grep -qi "CREATE TABLE"; then
    if ! echo "$FIXED_CONTENT" | grep -qi "updated_at"; then
        # Insert before the closing parenthesis of CREATE TABLE
        FIXED_CONTENT=$(echo "$FIXED_CONTENT" | sed '/^);$/i\    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
        FIXES_APPLIED+=("Added updated_at column")
    fi
fi

# Fix 3: Add index for foreign keys
if echo "$FIXED_CONTENT" | grep -qi "FOREIGN KEY"; then
    FK_REFERENCES=$(echo "$FIXED_CONTENT" | grep -oP 'REFERENCES \w+\(\w+\)' | sort -u)

    while IFS= read -r fk; do
        TABLE=$(echo "$fk" | grep -oP 'REFERENCES \K\w+')
        COLUMN=$(echo "$fk" | grep -oP '\(\K\w+\)')

        CURRENT_TABLE=$(echo "$FIXED_CONTENT" | grep -oP 'CREATE TABLE \K\w+' | head -1)

        if ! echo "$FIXED_CONTENT" | grep -qi "CREATE INDEX.*$CURRENT_TABLE.*$COLUMN"; then
            INDEX_NAME="idx_${CURRENT_TABLE}_${COLUMN}"
            INDEX_LINE="CREATE INDEX $INDEX_NAME ON $CURRENT_TABLE($COLUMN);"

            if ! echo "$FIXED_CONTENT" | grep -qi "$INDEX_NAME"; then
                FIXED_CONTENT="$FIXED_CONTENT"$'\n\n'"-- Add index for foreign key"$'\n'"$INDEX_LINE"
                FIXES_APPLIED+=("Added index $INDEX_NAME")
            fi
        fi
    done <<< "$FK_REFERENCES"
fi

# Fix 4: Add COMMENT for documentation
if echo "$FIXED_CONTENT" | grep -qi "CREATE TABLE"; then
    TABLE_NAME=$(echo "$FIXED_CONTENT" | grep -oP 'CREATE TABLE \K\w+' | head -1)

    if ! echo "$FIXED_CONTENT" | grep -qi "COMMENT ON TABLE"; then
        FIXED_CONTENT="$FIXED_CONTENT"$'\n\n'"-- Add documentation"$'\n'"COMMENT ON TABLE $TABLE_NAME IS 'Stores constitution-related data';"
        FIXES_APPLIED+=("Added table comment")
    fi
fi

# Fix 5: Wrap DROP TABLE in transaction
if echo "$FIXED_CONTENT" | grep -qi "DROP TABLE"; then
    if ! echo "$FIXED_CONTENT" | grep -qi "BEGIN TRANSACTION"; then
        FIXED_CONTENT="BEGIN TRANSACTION;"$'\n'"$FIXED_CONTENT"$'\n'"COMMIT;"
        FIXES_APPLIED+=("Wrapped DROP in transaction")
    fi
fi

# Apply fixes if any
if [ "${#FIXES_APPLIED[@]}" -gt 0 ]; then
    # Backup original
    cp "$FILE_PATH" "${FILE_PATH}.bak"

    # Write fixed content
    echo "$FIXED_CONTENT" > "$FILE_PATH"

    # Log fixes
    cat >> "$FIX_LOG" << EOF
[$TIMESTAMP] Auto-fix applied to: $FILE_PATH
Fixes:
$(printf '  - %s\n' "${FIXES_APPLIED[@]}")
EOF

    cat >> "$LOG_FILE" << EOF
[$TIMESTAMP] Auto-fixed: $FILE_PATH
Fixes applied: ${#FIXES_APPLIED[@]}
EOF

    echo "✅ Applied ${#FIXES_APPLIED[@]} auto-fixes:"
    printf '  - %s\n' "${FIXES_APPLIED[@]}"
    echo "   Backup saved to: ${FILE_PATH}.bak"

    exit 0
else
    echo "ℹ️  No auto-fixes available for this SQL file"

    cat >> "$LOG_FILE" << EOF
[$TIMESTAMP] No auto-fixes available: $FILE_PATH
EOF

    exit 1
fi
