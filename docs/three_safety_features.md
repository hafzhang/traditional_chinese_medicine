# 无人值守自主开发 - 三个保险丝完整说明

## 中医体质识别 MVP 项目

---

## 🛡️ 三保险丝架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    无人值守自主开发系统                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │              │    │              │    │              │      │
│  │  日志管理    │    │  Token熔断   │    │  进程保活    │      │
│  │              │    │              │    │              │      │
│  │ 防磁盘满     │    │  防成本失控   │    │  防意外退出   │      │
│  │              │    │              │    │              │      │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘      │
│         │                   │                   │              │
│         └───────────────────┼───────────────────┘              │
│                             ↓                                  │
│                    ┌───────────────┐                          │
│                    │               │                          │
│                    │  Claude 自主   │                          │
│                    │    开发引擎    │                          │
│                    │               │                          │
│                    └───────────────┘                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1️⃣ 日志管理 (house_keeping.sh)

### 功能
防止日志文件占满磁盘，确保长期稳定运行。

### 触发时机
- 每小时自动检查
- 每天凌晨0点全面清理

### 清理规则

| 规则 | 阈值 | 动作 |
|-----|-----|-----|
| 过期日志 | 7天以上 | 删除 |
| 大文件轮转 | >100MB | 归档并创建新文件 |
| 归档压缩 | 3天以上 | gzip 压缩 |
| 旧归档清理 | 30天以上 | 删除 |
| 总大小限制 | >500MB | 紧急清理 |
| 会话日志 | >1000行 | 裁剪到1000行 |

### 磁盘空间检查
```
使用率 >90% → 紧急清理
使用率 >80% → 警告
使用率 <80% → 正常
```

### 使用方法

```bash
# 手动执行
bash scripts/hooks/house_keeping.sh

# 查看清理日志
cat .claude/hooks/house_keeping.log
```

---

## 2️⃣ Token 熔断 (token_guard.sh)

### 功能
防止 API 调用成本失控，设置 24 小时使用上限。

### 阈值设置

| 阈值类型 | Token数 | 预估成本 | 动作 |
|---------|--------|---------|-----|
| 正常 | < 80万 | < $2.40 | 继续执行 |
| 警告 | 80-95万 | $2.40-2.85 | 显示警告 |
| 临界 | 95-100万 | $2.85-3.00 | 需要确认 |
| 熔断 | > 100万 | > $3.00 | 停止执行 |

### Token 记录

```json
{
  "last_24h_tokens": 50000,
  "today_tokens": 50000,
  "last_reset": 1736745600,
  "session_tokens": 50000
}
```

### 熔断触发后的操作

1. 自动停止执行
2. 记录熔断事件
3. 显示统计信息
4. （可选）发送 webhook 通知

### 恢复方法

```bash
# 方法1: 重置计数
echo '{"last_24h_tokens":0}' > .claude/hooks/token_usage.json

# 方法2: 调整上限
# 编辑 scripts/hooks/token_guard.sh
# 修改 DAILY_LIMIT=1000000
```

### 使用方法

```bash
# 查看当前使用
cat .claude/hooks/token_usage.json | jq '.'

# 手动检查
bash scripts/hooks/token_guard.sh
```

---

## 3️⃣ 进程保活 (supervisor)

### 功能
防止 Claude 进程意外退出，自动重启。

### 安装

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y supervisor

# CentOS/RHEL
sudo yum install -y supervisor

# macOS
brew install supervisor
```

### 配置文件位置

```
/etc/supervisor/conf.d/claude.conf
```

### 常用命令

```bash
# 启动
sudo supervisorctl start claude

# 停止
sudo supervisorctl stop claude

# 重启
sudo supervisorctl restart claude

# 查看状态
sudo supervisorctl status

# 查看日志
sudo tail -f /var/log/supervisor/claude.stdout.log
```

### 自动重启配置

```
autostart=true      # 自动启动
autorestart=true    # 自动重启
startretries=3      # 重启尝试次数
```

---

## 📋 Crontab 定时任务

### 配置内容

```bash
# 每6小时检查 token
0 */6 * * * bash /path/to/token_guard.sh

# 每天清理日志
0 0 * * * bash /path/to/house_keeping.sh

# 每30分钟检查进程
*/30 * * * * pgrep -f claude || mail -s "进程告警"
```

### 添加方法

```bash
# 编辑 crontab
crontab -e

# 或导入配置
crontab scripts/crontab/claude_tasks.cron
```

---

## 🔄 完整工作流程

```
开始无人值守
    ↓
[每小时] house_keeping → 清理日志，检查磁盘
    ↓
[每次] token_guard → 检查token使用
    ↓
[每次] check_priority → 检查任务优先级
    ↓
[每次] load_small_template → 检查任务大小
    ↓
Claude 执行任务
    ↓
[每次] validate + auto_fix → 验证并修复
    ↓
[每次] run_relevant_tests → 测试验证
    ↓
更新 todo.md
    ↓
[每次] auto_plan_next → 显示下一任务
    ↓
Supervisor → 进程保活监控
    ↓
[每天00:00] 全面日志清理
    ↓
[每6小时] Token全面检查
    ↓
今日目标全部完成 → 达成提示
    ↓
继续明天...
```

---

## 📊 监控仪表板

```bash
# 创建监控脚本
cat > monitor.sh << 'EOF'
#!/bin/bash
clear
while true; do
    echo "=========================================="
    echo "Claude 无人值守监控 - $(date '+%H:%M:%S')"
    echo "=========================================="
    echo ""

    # 进程状态
    echo "📌 进程状态:"
    pgrep -a claude || echo "  ⚠️  进程未运行"
    echo ""

    # Token 使用
    echo "💰 Token 使用:"
    cat .claude/hooks/token_usage.json 2>/dev/null | \
        jq -r '"  24h: \(.last_24h_tokens/1000000*100 | floor)%\n  今日: \(.today_tokens/1000000*100 | floor)%"' 2>/dev/null || echo "  无数据"
    echo ""

    # 任务进度
    echo "📋 任务进度:"
    TOTAL=$(grep -c '^\s*-\s*\[[x ]\]' .claude/todo.md 2>/dev/null || echo 0)
    DONE=$(grep -c '^\s*-\s*\[x\]' .claude/todo.md 2>/dev/null || echo 0)
    echo "  $DONE / $TOTAL 完成"
    echo ""

    # 磁盘使用
    echo "💾 磁盘使用:"
    df -h . | tail -1 | awk '{print "  " $5 " 已使用"}'
    echo ""

    sleep 60
done
EOF

chmod +x monitor.sh
./monitor.sh
```

---

## ✅ 最终检查

```bash
# 快速检查所有保险丝
echo "=== 保险丝状态检查 ==="

# 1. 日志管理
if [ -f "scripts/hooks/house_keeping.sh" ]; then
    echo "✅ 日志管理: 已安装"
else
    echo "❌ 日志管理: 未安装"
fi

# 2. Token 熔断
if [ -f "scripts/hooks/token_guard.sh" ]; then
    echo "✅ Token 熔断: 已安装"
    # 检查是否触发
    USED=$(jq -r '.last_24h_tokens // 0' .claude/hooks/token_usage.json 2>/dev/null || echo 0)
    echo "   已使用: $USED token"
else
    echo "❌ Token 熔断: 未安装"
fi

# 3. 进程保活
if command -v supervisorctl >/dev/null 2>&1; then
    echo "✅ 进程保活: Supervisor 已安装"
    sudo supervisorctl status claude 2>/dev/null | grep -q running && echo "   状态: 运行中" || echo "   状态: 未运行"
else
    echo "⚠️  进程保活: Supervisor 未安装（可选）"
fi

echo ""
echo "=== 系统就绪 ==="
```

---

*文档版本: v1.0*
*最后更新: 2025-01-13*
