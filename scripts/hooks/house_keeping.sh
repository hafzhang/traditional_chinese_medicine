#!/bin/bash
# House Keeping Script - 日志管理与清理
# 防止磁盘被日志占满，确保长期稳定运行

set -e

LOG_DIR=".claude/hooks"
ARCHIVE_DIR=".claude/logs/archive"
MAX_LOG_SIZE_MB=100
MAX_LOG_AGE_DAYS=7
MAX_TOTAL_LOG_MB=500

# 创建归档目录
mkdir -p "$ARCHIVE_DIR"

echo "🧹 House Keeping - $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

# 1. 清理过期日志（7天以上）
echo ""
echo "📋 清理过期日志 (${MAX_LOG_AGE_DAYS}天以上)..."
if [ -d "$LOG_DIR" ]; then
    DELETED=$(find "$LOG_DIR" -name "*.log" -mtime +$MAX_LOG_AGE_DAYS -delete -print 2>/dev/null | wc -l)
    echo "   删除了 $DELETED 个过期日志文件"
else
    echo "   日志目录不存在，跳过"
fi

# 2. 轮转大日志文件（>100MB）
echo ""
echo "📋 轮转大日志文件 (>${MAX_LOG_SIZE_MB}MB)..."
if [ -d "$LOG_DIR" ]; then
    ROTATED=0
    for log_file in "$LOG_DIR"/*.log; do
        if [ -f "$log_file" ]; then
            SIZE_MB=$(du -m "$log_file" | cut -f1)
            if [ "$SIZE_MB" -gt "$MAX_LOG_SIZE_MB" ]; then
                # 归档旧日志
                BASENAME=$(basename "$log_file")
                TIMESTAMP=$(date +%Y%m%d_%H%M%S)
                ARCHIVE_NAME="${BASENAME%.log}_${TIMESTAMP}.log"

                # 移动到归档目录
                mv "$log_file" "$ARCHIVE_DIR/$ARCHIVE_NAME"
                # 创建新日志文件
                touch "$log_file"

                ROTATED=$((ROTATED + 1))
                echo "   轮转: $BASENAME (${SIZE_MB}MB → $ARCHIVE_NAME)"
            fi
        fi
    done
    echo "   共轮转 $ROTATED 个大日志文件"
else
    echo "   日志目录不存在，跳过"
fi

# 3. 压缩归档日志（节省空间）
echo ""
echo "📋 压缩归档日志..."
if [ -d "$ARCHIVE_DIR" ]; then
    # 压缩3天前的归档日志
    COMPRESSED=$(find "$ARCHIVE_DIR" -name "*.log" -mtime +3 -exec gzip {} \; 2>/dev/null | wc -l)
    echo "   压缩了 $COMPRESSED 个归档日志文件"
else
    echo "   归档目录不存在，跳过"
fi

# 4. 清理压缩归档（30天以上）
echo ""
echo "📋 清理旧压缩归档 (30天以上)..."
if [ -d "$ARCHIVE_DIR" ]; then
    DELETED=$(find "$ARCHIVE_DIR" -name "*.gz" -mtime +30 -delete -print 2>/dev/null | wc -l)
    echo "   删除了 $DELETED 个旧压缩归档"
fi

# 5. 检查总日志大小
echo ""
echo "📋 检查总日志大小..."
if [ -d "$LOG_DIR" ]; then
    TOTAL_SIZE=$(du -sm "$LOG_DIR" | cut -f1)
    echo "   当前日志总大小: ${TOTAL_SIZE}MB"

    if [ "$TOTAL_SIZE" -gt "$MAX_TOTAL_LOG_MB" ]; then
        echo "   ⚠️  警告: 日志总大小超过 ${MAX_TOTAL_LOG_MB}MB"
        echo "   🔧 执行紧急清理..."

        # 删除最老的日志文件，直到总大小降到阈值以下
        find "$LOG_DIR" -name "*.log" -type f -printf '%T@ %p\n' | \
            sort -n | \
            head -n 10 | \
            cut -d' ' -f2 | \
            while read -r old_log; do
                [ -f "$old_log" ] && rm -f "$old_log" && echo "   删除: $(basename $old_log)"
            done

        NEW_SIZE=$(du -sm "$LOG_DIR" | cut -f1)
        echo "   清理后大小: ${NEW_SIZE}MB"
    else
        echo "   ✅ 日志大小正常"
    fi
fi

# 6. 清理会话日志（保留最新1000行）
echo ""
echo "📋 清理会话日志..."
SESSION_LOG="$LOG_DIR/sessions.log"
if [ -f "$SESSION_LOG" ]; then
    LINES=$(wc -l < "$SESSION_LOG")
    if [ "$LINES" -gt 1000 ]; then
        # 保留最新1000行
        tail -n 1000 "$SESSION_LOG" > "$SESSION_LOG.tmp"
        mv "$SESSION_LOG.tmp" "$SESSION_LOG"
        echo "   会话日志从 $LINES 行裁剪到 1000 行"
    else
        echo "   会话日志大小正常 ($LINES 行)"
    fi
fi

# 7. 记录清理操作
CLEANUP_LOG="$LOG_DIR/house_keeping.log"
echo "[$(date -Iseconds)] House keeping completed" >> "$CLEANUP_LOG"
echo "   Total logs: $(find "$LOG_DIR" -name "*.log" | wc -l)" >> "$CLEANUP_LOG"
echo "   Archive size: $(du -sm "$ARCHIVE_DIR" 2>/dev/null | cut -f1 || echo 0)MB" >> "$CLEANUP_LOG"

# 8. 磁盘空间检查
echo ""
echo "📋 磁盘空间检查..."
DISK_USAGE=$(df -h . | tail -1 | awk '{print $5}' | sed 's/%//')
echo "   当前磁盘使用率: ${DISK_USAGE}%"

if [ "$DISK_USAGE" -gt 90 ]; then
    echo "   🚨 警告: 磁盘空间不足（${DISK_USAGE}%）"
    echo "   🔧 执行紧急清理..."

    # 清理临时文件
    find tests/temp -type f -mtime +1 -delete 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

    # 清理npm缓存（如果有）
    [ -d "node_modules/.cache" ] && rm -rf node_modules/.cache/* 2>/dev/null || true

    NEW_DISK=$(df -h . | tail -1 | awk '{print $5}' | sed 's/%//')
    echo "   清理后磁盘使用率: ${NEW_DISK}%"
elif [ "$DISK_USAGE" -gt 80 ]; then
    echo "   ⚠️  磁盘使用率偏高 (${DISK_USAGE}%)"
else
    echo "   ✅ 磁盘空间充足"
fi

echo ""
echo "=========================================="
echo "✅ House Keeping 完成"
echo ""

exit 0
