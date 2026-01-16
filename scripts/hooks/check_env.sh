#!/bin/bash
# Hook: check_environment
# Trigger: pre-command
# Description: Verify required environment variables and dependencies

set -e

LOG_FILE=".claude/hooks/check_env.log"
mkdir -p "$(dirname "$LOG_FILE")"

echo "=== Environment Check ===" | tee -a "$LOG_FILE"
echo "Timestamp: $(date -Iseconds)" | tee -a "$LOG_FILE"

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

echo "Python version: $PYTHON_VERSION" | tee -a "$LOG_FILE"

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
    echo "❌ ERROR: Python 3.11+ required, found $PYTHON_VERSION" | tee -a "$LOG_FILE"
    exit 1
fi
echo "✅ Python version OK" | tee -a "$LOG_FILE"

# Check required files
REQUIRED_FILES=("requirements.txt" "pyproject.toml" ".env.example")
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ Found: $file" | tee -a "$LOG_FILE"
    else
        echo "⚠️  Missing: $file" | tee -a "$LOG_FILE"
    fi
done

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  WARNING: .env file not found. Copy from .env.example" | tee -a "$LOG_FILE"
fi

# Check critical environment variables if .env exists
if [ -f ".env" ]; then
    REQUIRED_VARS=("DATABASE_URL" "SECRET_KEY")
    for var in "${REQUIRED_VARS[@]}"; do
        if grep -q "^$var=" .env; then
            echo "✅ Env var set: $var" | tee -a "$LOG_FILE"
        else
            echo "⚠️  Env var missing: $var" | tee -a "$LOG_FILE"
        fi
    done
fi

echo "=== Environment Check Complete ===" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

exit 0
