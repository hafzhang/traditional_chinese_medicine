#!/bin/bash
# Hook: run_relevant_tests
# Trigger: After Write/Edit operation
# Description: Run relevant test suite and auto-fix on failure

FILE_PATH="${CLAUDE_TOOL_INPUT_FILE_PATH:-unknown}"
LOG_FILE=".claude/hooks/test_execution.log"

mkdir -p "$(dirname "$LOG_FILE")"

TIMESTAMP=$(date -Iseconds)

# Get file extension and type
FILE_EXT="${FILE_PATH##*.}"
FILE_NAME=$(basename "$FILE_PATH")

# Skip if file doesn't exist
if [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

echo ""
echo "🧪 Running tests for: $FILE_NAME"

# Test result tracking
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0
AUTO_FIX_ATTEMPTED=false

# Function to run test and handle failure
run_test() {
    local test_name=$1
    local test_command=$2
    local auto_fix_script=$3

    TESTS_RUN=$((TESTS_RUN + 1))

    echo "  Running: $test_name..."

    if eval "$test_command" >/dev/null 2>&1; then
        echo "  ✅ $test_name: PASSED"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo "  ❌ $test_name: FAILED"
        TESTS_FAILED=$((TESTS_FAILED + 1))

        # Attempt auto-fix if script provided
        if [ -n "$auto_fix_script" ] && [ -f "scripts/hooks/$auto_fix_script" ]; then
            echo "  🔧 Attempting auto-fix..."
            AUTO_FIX_ATTEMPTED=true

            export CLAUDE_TOOL_INPUT_FILE_PATH="$FILE_PATH"

            if bash "scripts/hooks/$auto_fix_script" 2>&1; then
                echo "  ✅ Auto-fix applied, re-running test..."

                # Re-run the test after fix
                if eval "$test_command" >/dev/null 2>&1; then
                    echo "  ✅ $test_name: PASSED after auto-fix"
                    TESTS_PASSED=$((TESTS_PASSED + 1))
                    TESTS_FAILED=$((TESTS_FAILED - 1))
                    return 0
                else
                    echo "  ⚠️  Auto-fix applied but test still fails"
                    return 1
                fi
            else
                echo "  ⚠️  Auto-fix failed or not available"
                return 1
            fi
        else
            return 1
        fi
    fi
}

# Determine file type and run appropriate tests
case "$FILE_EXT" in
    py)
        # Python file tests

        # Test 1: Syntax validation
        run_test "Python syntax check" \
            "python3 -m py_compile '$FILE_PATH'" \
            "auto_fix_python.sh"

        # Test 2: Type checking (if mypy available)
        if command -v mypy >/dev/null 2>&1; then
            run_test "Type check (mypy)" \
                "mypy --no-error-summary '$FILE_PATH'" \
                ""
        fi

        # Test 3: Linting (if pylint available)
        if command -v pylint >/dev/null 2>&1; then
            run_test "Lint (pylint)" \
                "pylint --errors-only '$FILE_PATH'" \
                ""
        fi

        # Test 4: API naming convention (if in api/ directory)
        if [[ "$FILE_PATH" == */api/* ]]; then
            run_test "API naming convention" \
                "bash scripts/hooks/check_api_naming.sh" \
                ""
        fi

        # Test 5: Run pytest if tests exist
        if [ -d "tests" ] && [ -f "tests/${FILE_PATH%.py}_test.py" ] || [ -f "tests/test_${FILE_PATH##*/}" ]; then
            run_test "Unit tests (pytest)" \
                "python -m pytest tests/ -k '${FILE_NAME%.py}' -q" \
                ""
        fi
        ;;

    sql)
        # SQL file tests

        # Test 1: SQL validation
        run_test "SQL schema validation" \
            "bash scripts/hooks/validate_sql.sh" \
            "auto_fix_sql.sh"

        # Test 2: Check for common SQL issues
        if [ -f "$FILE_PATH" ]; then
            SQL_CONTENT=$(cat "$FILE_PATH")

            # Check for DROP without backup
            if echo "$SQL_CONTENT" | grep -qi "DROP TABLE" && ! echo "$SQL_CONTENT" | grep -qi "BACKUP\|COPY"; then
                echo "  ⚠️  Warning: DROP TABLE without backup"
            fi

            # Check for missing indexes on foreign keys
            if echo "$SQL_CONTENT" | grep -qi "FOREIGN KEY" && ! echo "$SQL_CONTENT" | grep -qi "CREATE INDEX"; then
                echo "  ⚠️  Warning: Foreign key without index"
            fi
        fi
        ;;

    js|ts|jsx|tsx)
        # JavaScript/TypeScript file tests

        # Test 1: ESLint (if available)
        if command -v eslint >/dev/null 2>&1; then
            run_test "Lint (eslint)" \
                "eslint '$FILE_PATH'" \
                ""
        fi

        # Test 2: Type check for TypeScript
        if [ "$FILE_EXT" = "ts" ] && command -v tsc >/dev/null 2>&1; then
            run_test "Type check (tsc)" \
                "tsc --noEmit '$FILE_PATH'" \
                ""
        fi
        ;;

    md)
        # Markdown file tests

        # Test 1: Check for markdown lint errors (if markdownlint available)
        if command -v markdownlint >/dev/null 2>&1; then
            run_test "Markdown lint" \
                "markdownlint '$FILE_PATH'" \
                ""
        fi
        ;;

    *)
        # Unknown file type - skip tests
        echo "  ℹ️  No tests configured for .$FILE_EXT files"
        ;;
esac

# Log test execution
cat >> "$LOG_FILE" << EOF
[$TIMESTAMP] Test execution for: $FILE_PATH
Tests run: $TESTS_RUN
Passed: $TESTS_PASSED
Failed: $TESTS_FAILED
Auto-fix attempted: $AUTO_FIX_ATTEMPTED
EOF

# Summary
echo ""
if [ $TESTS_RUN -eq 0 ]; then
    echo "ℹ️  No tests run for this file"
    exit 0
elif [ $TESTS_FAILED -eq 0 ]; then
    echo "✅ All tests passed ($TESTS_PASSED/$TESTS_RUN)"
    exit 0
else
    echo "⚠️  Some tests failed ($TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed)"
    exit 1
fi
