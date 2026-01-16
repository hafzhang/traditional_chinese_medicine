#!/bin/bash
# Hook: auto_fix_python
# Trigger: After Python validation fails
# Description: Automatically fix common Python code issues

FILE_PATH="${CLAUDE_TOOL_INPUT_FILE_PATH:-unknown}"
LOG_FILE=".claude/hooks/auto_fix_python.log"
FIX_LOG=".claude/hooks/python_fixes_applied.log"

mkdir -p "$(dirname "$LOG_FILE")"

TIMESTAMP=$(date -Iseconds)

# Only process Python files
if [[ "$FILE_PATH" != *.py ]]; then
    exit 0
fi

# Check if file exists
if [ ! -f "$FILE_PATH" ]; then
    echo "⚠️  File not found: $FILE_PATH"
    exit 1
fi

echo "🔧 Attempting to auto-fix Python issues in: $FILE_PATH"

# Read original content
ORIGINAL_CONTENT=$(cat "$FILE_PATH")
FIXED_CONTENT="$ORIGINAL_CONTENT"
FIXES_APPLIED=()

# Fix 1: Add missing docstring to functions
if echo "$FIXED_CONTENT" | grep -E "def\s+\w+\([^)]*\):\s*$" > /dev/null; then
    FIXED_CONTENT=$(echo "$FIXED_CONTENT" | sed '/def \w\+([^)]*):/a\    """TODO: Add docstring."""')
    FIXES_APPLIED+=("Added placeholder docstrings to functions")
fi

# Fix 2: Convert camelCase to snake_case for function names
# This is a simple heuristic - detect common patterns
CAMEL_FUNCS=$(echo "$FIXED_CONTENT" | grep -oP "def\s+[a-z]+[A-Z][a-zA-Z]*" | cut -d' ' -f2)

for camel_func in $CAMEL_FUNCS; do
    # Convert camelCase to snake_case
    snake_func=$(echo "$camel_func" | sed 's/\([A-Z]\)/_\L\1/g' | sed 's/^_//')

    if [ "$camel_func" != "$snake_func" ]; then
        FIXED_CONTENT=$(echo "$FIXED_CONTENT" | sed "s/def $camel_func(/def $snake_func(/g")
        # Also update calls to this function
        FIXED_CONTENT=$(echo "$FIXED_CONTENT" | sed "s/$camel_func(/$snake_func(/g")
        FIXES_APPLIED+=("Renamed function: $camel_func → $snake_func")
    fi
done

# Fix 3: Add type hints to function definitions (basic)
if echo "$FIXED_CONTENT" | grep -E "def\s+\w+\([^)]*\):" > /dev/null; then
    # Functions without return type annotation
    NO_RETURN=$(echo "$FIXED_CONTENT" | grep -E "def\s+\w+\([^)]*\):" | grep -v " -> " | cut -d':' -f1 | cut -d' ' -f2)

    for func in $NO_RETURN; do
        # Add -> None for functions without return type (heuristic)
        FIXED_CONTENT=$(echo "$FIXED_CONTENT" | sed "s/def $func(/def $func(/g; s/\(def $func([^)]*)\):/\1 -> None:/g")
        FIXES_APPLIED+=("Added type hint: $func() -> None")
    done
fi

# Fix 4: Add import typing if type hints are used
if echo "$FIXED_CONTENT" | grep -qE "List|Dict|Optional|Tuple"; then
    if ! echo "$FIXED_CONTENT" | grep -q "from typing import"; then
        # Find the first import line and add typing import
        FIXED_CONTENT=$(echo "$FIXED_CONTENT" | sed '0,/import/s//from typing import List, Dict, Optional, Tuple\n\nimport/')
        FIXES_APPLIED+=("Added typing imports")
    fi
fi

# Fix 5: Fix trailing whitespace
if echo "$FIXED_CONTENT" | grep "[[:space:]]$" > /dev/null; then
    FIXED_CONTENT=$(echo "$FIXED_CONTENT" | sed 's/[[:space:]]*$//')
    FIXES_APPLIED+=("Removed trailing whitespace")
fi

# Fix 6: Ensure file ends with newline
if [ -n "$FIXED_CONTENT" ] && [ "$(tail -c 1 <<< "$FIXED_CONTENT" | wc -l)" -eq 0 ]; then
    FIXED_CONTENT="$FIXED_CONTENT"$'\n'
    FIXES_APPLIED+=("Added final newline")
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

    # Re-validate to see if fixes worked
    if python3 -m py_compile "$FILE_PATH" 2>/dev/null; then
        echo "✅ Fixed code passes syntax validation!"
        exit 0
    else
        echo "⚠️  Syntax issues remain, manual review needed"
        exit 1
    fi
else
    echo "ℹ️  No auto-fixes available for this Python file"

    cat >> "$LOG_FILE" << EOF
[$TIMESTAMP] No auto-fixes available: $FILE_PATH
EOF

    exit 1
fi
