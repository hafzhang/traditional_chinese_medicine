# 无人值守自主开发系统 - 最后 5 分钟 Checklist（最终版）

## 3 个"保险丝"已就位

### ✅ 已创建文件

| 文件 | 功能 | 状态 |
|-----|-----|-----|
| `scripts/hooks/house_keeping.sh` | 日志管理，防磁盘满 | ✅ |
| `scripts/hooks/token_guard.sh` | Token熔断，防成本失控 | ✅ |
| `scripts/supervisor/claude.conf` | 进程保活，防意外退出 | ✅ |

---

## 📋 5 分钟设置步骤

### 步骤 1: 设置文件权限（30 秒）

```bash
chmod +x scripts/hooks/*.sh
chmod +x scripts/hooks/token_guard.sh
chmod +x scripts/hooks/house_keeping.sh
```

### 步骤 2: 测试日志清理（30 秒）

```bash
# 测试日志清理
bash scripts/hooks/house_keeping.sh
```

**预期输出**:
```
🧹 House Keeping - 2025-01-13 XX:XX:XX
==========================================

📋 清理过期日志 (7天以上)...
   删除了 0 个过期日志文件

📋 轮转大日志文件 (>100MB)...
   共轮转 0 个大日志文件

📋 检查总日志大小...
   当前日志总大小: 5MB
   ✅ 日志大小正常

==========================================
✅ House Keeping 完成
```

### 步骤 3: 测试 Token 监控（30 秒）

```bash
# 初始化 token 记录
cat > .claude/hooks/token_usage.json << 'EOF'
{
  "last_24h_tokens": 0,
  "today_tokens": 0,
  "last_reset": $(date +%s),
  "session_tokens": 0
}
EOF

# 测试 token 监控
export CLAUDE_TOKENS_USED=1000
bash scripts/hooks/token_guard.sh
echo "Exit code: $?"
```

**预期输出**:
```
📊 Token: 1000 / 1000000 ($0.00)
Exit code: 0
```

### 步骤 4: 测试 Token 熔断（30 秒）

```bash
# 模拟达到上限
jq '.last_24h_tokens = 1000001' .claude/hooks/token_usage.json > /tmp/token_test.json
mv /tmp/token_test.json .claude/hooks/token_usage.json

bash scripts/hooks/token_guard.sh
echo "Exit code: $?"
```

**预期输出**:
```
==========================================
🚨 TOKEN 熔断触发
==========================================

24小时Token使用量: 1000001 / 1000000
预估成本: $3.00

为防止成本失控，系统已自动停机
...
Exit code: 1
```

恢复:
```bash
echo '{"last_24h_tokens":0}' > .claude/hooks/token_usage.json
```

### 步骤 5: 配置 Supervisor（1 分钟）

#### 5.1 安装 Supervisor

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y supervisor

# CentOS/RHEL
sudo yum install -y supervisor

# macOS
brew install supervisor
```

#### 5.2 复制配置文件

```bash
# 编辑 supervisor 配置，修改路径
PROJECT_PATH=$(pwd)
sed "s|/path/to/traditional_chinese_medicine|$PROJECT_PATH|g" \
    scripts/supervisor/claude.conf > /tmp/claude.conf

# 复制到 supervisor 配置目录
sudo cp /tmp/claude.conf /etc/supervisor/conf.d/claude.conf
```

#### 5.3 启动 Supervisor

```bash
# 重新加载配置
sudo supervisorctl reread
sudo supervisorctl update

# 启动 Claude 进程
sudo supervisorctl start claude

# 查看状态
sudo supervisorctl status
```

### 步骤 6: 配置 Crontab（1 分钟）

```bash
# 编辑 crontab
crontab -e

# 添加以下内容（修改路径）
PROJECT_PATH=$(pwd)

cat >> /tmp/claude_cron << EOF
# Claude Code 定时任务

# 每6小时检查 token
0 */6 * * * bash $PROJECT_PATH/scripts/hooks/token_guard.sh >> $PROJECT_PATH/.claude/hooks/cron_token.log 2>&1

# 每天凌晨清理日志
0 0 * * * bash $PROJECT_PATH/scripts/hooks/house_keeping.sh >> $PROJECT_PATH/.claude/hooks/cron_housekeeping.log 2>&1
EOF

# 导入到 crontab
crontab -l > /tmp/existing_cron
cat /tmp/claude_cron >> /tmp/existing_cron
crontab /tmp/existing_cron

# 验证
crontab -l | grep claude
```

### 步骤 7: 验证所有保险丝（1 分钟）

```bash
# 检查1: 日志清理
echo "=== 检查日志清理 ==="
bash scripts/hooks/house_keeping.sh | grep "✅"

# 检查2: Token 监控
echo ""
echo "=== 检查 Token 监控 ==="
export CLAUDE_TOKENS_USED=0
bash scripts/hooks/token_guard.sh | grep "📊"

# 检查3: Supervisor 状态
echo ""
echo "=== 检查 Supervisor 状态 ==="
sudo supervisorctl status claude 2>/dev/null || echo "Supervisor 未配置（可选）"

# 检查4: Cron 任务
echo ""
echo "=== 检查 Cron 任务 ==="
crontab -l | grep -c "claude"
echo "个 Claude 定时任务已配置"
```

### 步骤 8: 最终确认（30 秒）

```bash
# 检查关键文件
echo "=== 关键文件检查 ==="
ls -la scripts/hooks/house_keeping.sh
ls -la scripts/hooks/token_guard.sh
ls -la .claude/hooks/token_usage.json
ls -la scripts/supervisor/claude.conf

# 检查权限
echo ""
echo "=== 执行权限检查 ==="
ls -l scripts/hooks/*.sh | grep -c "rwxrwxrwx"
echo "个脚本有执行权限"
```

---

## ✅ 完成确认

### 三个保险丝状态

| 保险丝 | 触发条件 | 保护措施 | 状态 |
|-------|---------|---------|-----|
| **日志管理** | 日志>7天 或 >100MB | 自动轮转/清理 | ✅ |
| **Token 熔断** | 24h>100万token | 自动停机 | ✅ |
| **进程保活** | 进程意外退出 | 自动重启 | ✅ |

### 保护阈值

| 阈值 | 值 | 说明 |
|-----|---|-----|
| 日志保留 | 7天 | 超过自动删除 |
| 单文件大小 | 100MB | 超过自动轮转 |
| 总日志大小 | 500MB | 超过紧急清理 |
| Token 日限额 | 100万 | 约$2-3 |
| Token 警告线 | 80万 | 提前警告 |
| Token 临界线 | 95万 | 严格限制 |
| 磁盘使用率 | 90% | 紧急清理 |

---

## 🚀 启动无人值守模式

### 方法1: 使用 Supervisor（推荐）

```bash
# 启动
sudo supervisorctl start claude

# 查看日志
sudo tail -f /var/log/supervisor/claude.stdout.log

# 停止
sudo supervisorctl stop claude

# 重启
sudo supervisorctl restart claude
```

### 方法2: 使用 nohup（简单）

```bash
# 后台运行
nohup bash -c 'while true; do echo "请继续自主开发" | claude; sleep 60; done' &
```

### 方法3: 使用 systemd（Linux）

```bash
# 创建服务文件
sudo tee /etc/systemd/system/claude.service << EOF
[Unit]
Description=Claude Code Autonomous Mode
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/claude-code --autonomous
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 启动服务
sudo systemctl daemon-reload
sudo systemctl start claude
sudo systemctl enable claude
```

---

## 📊 监控命令

```bash
# 实时监控日志
tail -f .claude/hooks/*.log

# 查看 Token 使用
cat .claude/hooks/token_usage.json | jq '.'

# 查看任务进度
bash scripts/hooks/auto_plan_next.sh

# 查看进程状态
sudo supervisorctl status

# 查看磁盘使用
df -h .

# 查看最近的错误
grep -i "error\|failed" .claude/hooks/*.log | tail -20
```

---

## 🆘 紧急停止

```bash
# 方法1: Supervisor 停止
sudo supervisorctl stop claude

# 方法2: 禁用 token 监控
jq '.enabled = false' .claude/hooks.json > /tmp/hooks.json
mv /tmp/hooks.json .claude/hooks.json

# 方法3: 设置极低的 token 限制
echo '{"last_24h_tokens": 999999}' > .claude/hooks/token_usage.json
```

---

## 📞 故障排除

### 问题: Supervisor 无法启动

```bash
# 检查配置
sudo supervisorctl configtest

# 查看错误日志
sudo cat /var/log/supervisor/supervisord.log
```

### 问题: Token 计数不准确

```bash
# 重置计数
echo '{"last_24h_tokens":0,"today_tokens":0}' > .claude/hooks/token_usage.json
```

### 问题: 日志占用空间过大

```bash
# 手动清理
bash scripts/hooks/house_keeping.sh

# 或强制清理
rm -f .claude/hooks/*.log.old
```

---

## ✅ 最终检查清单

- [x] house_keeping.sh 创建并测试
- [x] token_guard.sh 创建并测试
- [x] supervisor 配置文件创建
- [x] crontab 配置文件创建
- [x] hooks.json 更新至 v2.0.0
- [ ] Supervisor 安装并配置
- [ ] Crontab 任务添加
- [ ] 文件权限设置完成
- [ ] 三个保险丝全部测试通过

---

*最后更新: 2025-01-13*
*预计设置时间: 5 分钟*
