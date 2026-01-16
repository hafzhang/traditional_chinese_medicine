#!/bin/bash
# Hook: check_response_length
# Trigger: pre-response
# Description: Warn if response is too long for optimal user experience

LOG_FILE=".claude/hooks/response_analysis.log"
mkdir -p "$(dirname "$LOG_FILE")"

RESPONSE="${CLAUDE_RESPONSE:-}"
TIMESTAMP=$(date -Iseconds)

# Count characters and estimate tokens
CHAR_COUNT=${#RESPONSE}
TOKEN_ESTIMATE=$((CHAR_COUNT / 4))  # Rough estimate: 1 token ≈ 4 chars

# Thresholds
WARNING_THRESHOLD=50000   # ~12500 tokens
CRITICAL_THRESHOLD=100000 # ~25000 tokens

if [ $CHAR_COUNT -gt $CRITICAL_THRESHOLD ]; then
    cat >> "$LOG_FILE" << EOF
[$TIMESTAMP] ⚠️  CRITICAL: Very Long Response
Characters: $CHAR_COUNT
Est. Tokens: $TOKEN_ESTIMATE
---
EOF
    echo "⚠️  CRITICAL: Response is very long ($CHAR_COUNT chars, ~$TOKEN_ESTIMATE tokens)"
    echo "   Consider breaking into smaller responses."

elif [ $CHAR_COUNT -gt $WARNING_THRESHOLD ]; then
    cat >> "$LOG_FILE" << EOF
[$TIMESTAMP] ⚠️  WARNING: Long Response
Characters: $CHAR_COUNT
Est. Tokens: $TOKEN_ESTIMATE
---
EOF
    echo "⚠️  WARNING: Long response ($CHAR_COUNT chars, ~$TOKEN_ESTIMATE tokens)"
fi

exit 0
