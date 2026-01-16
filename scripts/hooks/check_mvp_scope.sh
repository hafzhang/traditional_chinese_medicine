#!/bin/bash
# Hook: check_mvp_scope
# Trigger: user-prompt-submit
# Description: Warn if requested feature is outside MVP scope

USER_PROMPT="${CLAUDE_USER_PROMPT:-unknown}"
LOG_FILE=".claude/hooks/scope_warnings.log"
mkdir -p "$(dirname "$LOG_FILE")"

# Features OUTSIDE MVP scope (should trigger warning)
OUT_OF_SCOPE_PATTERNS=(
    "social.*share|friend.*pk|community|challenge"
    "points.*mall|积分.*商城|reward.*system"
    "tongue.*diagnosis|ai.*tongue|舌诊"
    "enterprise|employee.*health|company"
    "seasonal.*health|节气|二十四节气"
    "exercise.*recommend|运动.*推荐|fitness.*plan"
    "health.*track|打卡|daily.*check"
)

TIMESTAMP=$(date -Iseconds)
WARNING_TRIGGERED=false

# Check against out-of-scope patterns
for pattern in "${OUT_OF_SCOPE_PATTERNS[@]}"; do
    if echo "$USER_PROMPT" | grep -qiE "$pattern"; then
        cat >> "$LOG_FILE" << EOF
[$TIMESTAMP] ⚠️  MVP Scope Warning
Request may be outside MVP scope: $USER_PROMPT
Pattern matched: $pattern
---
EOF
        echo "⚠️  WARNING: This feature may be outside MVP scope. Consider deferring to post-MVP."
        WARNING_TRIGGERED=true
        break
    fi
done

exit 0
