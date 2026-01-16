#!/bin/bash
# Hook: detect_feature_request
# Trigger: user-prompt-submit
# Description: Detect and categorize feature requests from user prompts

USER_PROMPT="${CLAUDE_USER_PROMPT:-unknown}"
LOG_FILE=".claude/hooks/feature_requests.log"
mkdir -p "$(dirname "$LOG_FILE")"

# Feature keywords detection
FEATURE_PATTERNS=(
    "add.*feature|implement.*function|create.*module"
    "build.*api|develop.*endpoint"
    "design.*page|create.*ui|build.*interface"
    "integrate.*service|connect.*api"
    "optimize.*performance|improve.*speed"
    "fix.*bug|resolve.*error"
)

CATEGORIES=(
    "new_feature"
    "api_development"
    "ui_development"
    "integration"
    "optimization"
    "bug_fix"
)

TIMESTAMP=$(date -Iseconds)

# Detect category
DETECTED_CATEGORY="general"
for i in "${!FEATURE_PATTERNS[@]}"; do
    if echo "$USER_PROMPT" | grep -qiE "${FEATURE_PATTERNS[$i]}"; then
        DETECTED_CATEGORY="${CATEGORIES[$i]}"
        break
    fi
done

# Log if it's a feature request
if [ "$DETECTED_CATEGORY" != "general" ]; then
    cat >> "$LOG_FILE" << EOF
[$TIMESTAMP] Category: $DETECTED_CATEGORY
Prompt: $USER_PROMPT
---
EOF
    echo "📋 Feature detected: $DETECTED_CATEGORY"
fi

exit 0
