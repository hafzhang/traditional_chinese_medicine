#!/bin/bash
# Token Guard - Token使用量监控与熔断
# 防止成本失控，设置24小时使用上限

set -e

LOG_DIR=".claude/hooks"
TOKEN_LOG="$LOG_DIR/token_usage.json"
ALERT_LOG="$LOG_DIR/token_alerts.log"

# 配置
DAILY_LIMIT=1000000        # 100万token ≈ $2-3 USD
WARN_THRESHOLD=800000      # 80万token时发出警告
CRITICAL_THRESHOLD=950000  # 95万token时严格限制

mkdir -p "$(dirname "$TOKEN_LOG")"

# 获取当前时间戳
NOW=$(date +%s)
TODAY_START=$(date -d "$(date +%Y-%m-%d)" +%s 2>/dev/null || date -j "$(date +%Y-%m-%d)" +%s)

# 初始化token使用记录
if [ ! -f "$TOKEN_LOG" ]; then
    cat > "$TOKEN_LOG" << EOF
{
  "last_24h_tokens": 0,
  "today_tokens": 0,
  "last_reset": $NOW,
  "session_tokens": 0,
  "daily_records": []
}
EOF
fi

# 从环境变量获取本次使用的token数
SESSION_TOKENS="${CLAUDE_TOKENS_USED:-0}"

# 读取当前记录
CURRENT_24H=$(jq -r '.last_24h_tokens' "$TOKEN_LOG" 2>/dev/null || echo "0")
CURRENT_TODAY=$(jq -r '.today_tokens' "$TOKEN_LOG" 2>/dev/null || echo "0")
LAST_RESET=$(jq -r '.last_reset' "$TOKEN_LOG" 2>/dev/null || echo "$NOW")

# 检查是否需要重置
if [ "$((NOW - LAST_RESET))" -gt 86400 ]; then
    # 超过24小时，重置计数
    jq --argjson now "$NOW" \
       --argjson today "$SESSION_TOKENS" \
       '.last_reset = $now | .today_tokens = $today | .last_24h_tokens = $today' \
       "$TOKEN_LOG" > "$TOKEN_LOG.tmp"
    mv "$TOKEN_LOG.tmp" "$TOKEN_LOG"

    CURRENT_24H=$SESSION_TOKENS
    CURRENT_TODAY=$SESSION_TOKENS
else
    # 累加本次使用量
    NEW_24H=$((CURRENT_24H + SESSION_TOKENS))
    NEW_TODAY=$((CURRENT_TODAY + SESSION_TOKENS))

    jq --argjson tokens_24h "$NEW_24H" \
       --argjson tokens_today "$NEW_TODAY" \
       '.last_24h_tokens = $tokens_24h | .today_tokens = $tokens_today | .session_tokens = $tokens_today' \
       "$TOKEN_LOG" > "$TOKEN_LOG.tmp"
    mv "$TOKEN_LOG.tmp" "$TOKEN_LOG"

    CURRENT_24H=$NEW_24H
    CURRENT_TODAY=$NEW_TODAY
fi

# 估算成本（按 $3/100万token 计算）
COST_PER_1M=3
ESTIMATED_COST=$(awk "BEGIN {printf \"%.2f\", ($CURRENT_24H / 1000000) * $COST_PER_1M}")

# 判断是否需要熔断
if [ "$CURRENT_24H" -ge "$DAILY_LIMIT" ]; then
    echo ""
    echo "=========================================="
    echo "🚨 TOKEN 熔断触发"
    echo "=========================================="
    echo ""
    echo "24小时Token使用量: $CURRENT_24H / $DAILY_LIMIT"
    echo "预估成本: \$$ESTIMATED_COST"
    echo ""
    echo "为防止成本失控，系统已自动停机"
    echo ""
    echo "请检查:"
    echo "  1. 是否有异常高频请求"
    echo "  2. 是否有循环错误导致的重复请求"
    echo "  3. 是否需要调整 DAILY_LIMIT"
    echo ""
    echo "恢复方法:"
    echo "  编辑 $TOKEN_LOG，将 last_24h_tokens 设为 0"
    echo ""
    echo "=========================================="
    echo ""

    # 记录熔断事件
    cat >> "$ALERT_LOG" << EOF
[$(date -Iseconds)] TOKEN CIRCUIT BREAKER TRIGGERED
Usage: $CURRENT_24H / $DAILY_LIMIT
Estimated Cost: \$$ESTIMATED_COST
---

EOF

    # 可选：发送webhook通知
    # WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
    # curl -X POST "$WEBHOOK_URL" \
    #   -H "Content-Type: application/json" \
    #   -d "{\"msg_type\":\"text\",\"content\":{\"text\":\"Claude Token熔断: ${CURRENT_24H}/${DAILY_LIMIT}\"}}" \
    #   2>/dev/null || true

    exit 1  # 阻止继续执行

elif [ "$CURRENT_24H" -ge "$CRITICAL_THRESHOLD" ]; then
    echo ""
    echo "⚠️  TOKEN 使用量接近上限"
    echo "   已使用: $CURRENT_24H / $DAILY_LIMIT ($((CURRENT_24H * 100 / DAILY_LIMIT))%)"
    echo "   预估成本: \$$ESTIMATED_COST"
    echo ""
    echo "   建议停止新任务，或手动确认继续"

    exit 1  # 需要确认

elif [ "$CURRENT_24H" -ge "$WARN_THRESHOLD" ]; then
    echo ""
    echo "📊 Token 使用量提醒"
    echo "   已使用: $CURRENT_24H / $DAILY_LIMIT ($((CURRENT_24H * 100 / DAILY_LIMIT))%)"
    echo "   预估成本: \$$ESTIMATED_COST"
    echo ""

    exit 0  # 仅警告，不阻止

else
    # 正常状态，仅记录
    echo "📊 Token: $CURRENT_24H / $DAILY_LIMIT (\$$ESTIMATED_COST)"
    exit 0
fi
