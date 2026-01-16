# 无人值守自主开发系统使用指南

## 中医体质识别 MVP 项目

---

## 系统概述

本系统使 Claude 能够自主完成整个 MVP 开发，无需人工持续干预。

### 核心组件

| 组件 | 功能 | 文件 |
|-----|-----|-----|
| 任务队列 | 存储所有待办任务 | `.claude/todo.md` |
| 优先级检查 | 防止偏离 MVP 主线 | `scripts/hooks/check_priority.sh` |
| 任务拆分 | 大任务自动分解 | `scripts/hooks/load_small_template.sh` |
| 自动规划 | 自动选择下一个任务 | `scripts/hooks/auto_plan_next.sh` |
| 死循环防护 | 检测并阻止重复失败 | `.claude/retry_counter.json` |
| 任务模板 | 提供拆分参考 | `task_templates/` |

---

## 快速开始

### 1. 确认文件权限

```bash
chmod +x scripts/hooks/*.sh
```

### 2. 测试自动规划

```bash
# 查看下一个任务
bash scripts/hooks/auto_plan_next.sh

# 应该输出:
# ⏭️  接口规范评审与确认
# 📊 今日进度: 2/5 完成 (40%)
```

### 3. 测试优先级检查

```bash
# 测试 MVP 范围内的任务
export CLAUDE_USER_PROMPT="实现体质测试问卷功能"
bash scripts/hooks/check_priority.sh
# 输出: 🟠 中高优先级任务

# 测试超出 MVP 范围的任务
export CLAUDE_USER_PROMPT="添加积分商城和好友PK功能"
bash scripts/hooks/check_priority.sh
# 输出: ⚠️  优先级警告: 任务可能超出 MVP 范围
```

### 4. 测试任务拆分检测

```bash
# 测试大型任务
export CLAUDE_USER_PROMPT="实现完整的体质测试API系统，包括所有接口、数据库、前端页面和测试"
bash scripts/hooks/load_small_template.sh
# 输出: ⚠️  检测到复杂任务！建议: 将任务拆分为更小的子任务
```

---

## 工作流程

```
┌─────────────────────────────────────────────────────────────────┐
│                    无人值守开发流程                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣  用户请求 → priority_check → 拦截非MVP任务                    │
│       ↓                                                         │
│  2️⃣  load_small_template → 大任务拆分                           │
│       ↓                                                         │
│  3️⃣  Claude 执行任务 → validate/auto_fix                        │
│       ↓                                                         │
│  4️⃣  run_relevant_tests → 测试验证                              │
│       ↓                                                         │
│  5️⃣  更新 todo.md → 标记 [x] 完成                               │
│       ↓                                                         │
│  6️⃣  auto_plan_next → 显示下一个任务                            │
│       ↓                                                         │
│  7️⃣  循环直到今日目标全部完成                                   │
│       ↓                                                         │
│  8️⃣  达成提示 → "今日目标达成"                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 任务队列格式

### todo.md 结构

```markdown
## 今日目标 (2025-01-13)

### Week 0: 准备阶段
- [ ] 任务1 - 待完成
- [x] 任务2 - 已完成
- [!] 任务3 - 阻塞中
- [-] 任务4 - 已跳过
```

### 任务标记说明

| 标记 | 含义 | 用途 |
|-----|-----|-----|
| `[ ]` | 待完成 | 默认状态 |
| `[x]` | 已完成 | 任务完成 |
| `[!]` | 阻塞 | 需要人工介入 |
| `[-]` | 跳过 | 非关键任务 |

---

## 优先级规则

### 优先级定义

| 级别 | 说明 | 示例 |
|-----|-----|-----|
| 1️⃣ 最高 | 阻塞问题、核心 bug | "修复无法启动的bug" |
| 2️⃣ 高 | 核心功能 | "实现体质判定" |
| 3️⃣ 中高 | 重要功能 | "实现报告生成" |
| 4️⃣ 中等 | 正常任务 | "优化UI样式" |
| 5️⃣ 中低 | 改进任务 | "添加注释" |

### 拦截规则

以下任务会被**强制拦截**：
- 社交功能（积分商城、好友PK）
- AI 舌诊
- 企业服务
- 会员体系

---

## 死循环防护

### 检测机制

1. **重试计数**: 同一任务失败 3 次
2. **语法错误**: 连续 5 次语法错误
3. **相同文件修改**: 同一文件修改 3 次
4. **连续失败**: 连续 3 个任务失败

### 防护措施

```bash
# 查看重试计数
cat .claude/retry_counter.json | jq .

# 重置计数（人工介入后）
echo '{}' > .claude/retry_counter.json
```

---

## 自主模式配置

### hooks.json 设置

```json
{
  "autonomous_mode": {
    "enabled": true,
    "max_continuous_hours": 8,
    "auto_break_minutes": 15,
    "daily_goal_check": true
  }
}
```

### 配置说明

| 参数 | 说明 | 默认值 |
|-----|-----|-------|
| enabled | 是否启用自主模式 | true |
| max_continuous_hours | 最大连续工作时长 | 8 |
| auto_break_minutes | 自动休息时长 | 15 |
| daily_goal_check | 每日目标检查 | true |

---

## 使用示例

### 启动自主开发

```bash
# 方式1: 直接开始
echo "请开始自主开发，从 todo.md 中的第一个任务开始"

# 方式2: 指定开始任务
echo "请从'搭建 FastAPI 项目脚手架'开始"

# 方式3: 继续上次任务
echo "请继续上次的任务"
```

### 查看进度

```bash
# 查看任务队列
cat .claude/todo.md

# 查看重试统计
cat .claude/retry_counter.json | jq '.statistics'

# 查看会话日志
tail -20 .claude/hooks/session.log
```

### 人工干预

```bash
# 标记任务完成
# 编辑 .claude/todo.md，将 [ ] 改为 [x]

# 添加新任务
# 在 .claude/todo.md 中添加新任务

# 跳过任务
# 将 [ ] 改为 [-]

# 标记阻塞
# 将 [ ] 改为 [!]
```

---

## 达成检测

### 今日目标完成

当所有今日目标标记为 `[x]` 后，系统会自动输出：

```
==========================================
🎉 今日目标达成！
==========================================

✅ 所有 X 个任务已完成
📊 完成率: 100%
🕐 完成时间: HH:MM

🌟 出色的工作！休息一下吧~

==========================================
```

### 继续明天

完成今日目标后：

```bash
# 1. 更新 todo.md 中的日期
# ## 今日目标 (2025-01-13)
# 改为
# ## 今日目标 (2025-01-14)

# 2. 添加新任务
# 复制明天的任务列表

# 3. 继续开发
echo "继续明天的任务"
```

---

## 故障排除

### 问题: 任务一直重复

**原因**: 可能遇到死循环

**解决**:
```bash
# 查看重试计数
cat .claude/retry_counter.json

# 重置计数
echo '{}' > .claude/retry_counter.json
```

### 问题: 优先级检查过于严格

**解决**: 临时禁用
```bash
# 编辑 .claude/hooks.json
# 将 "check_priority" 的 "enabled" 改为 false
```

### 问题: 任务拆分太频繁

**解决**: 调整阈值
```bash
# 编辑 scripts/hooks/load_small_template.sh
# 修改 COMPLEXITY_THRESHOLD 的值（默认5）
```

---

## 监控命令

```bash
# 实时监控进度
watch -n 30 'bash scripts/hooks/auto_plan_next.sh'

# 查看所有日志
tail -f .claude/hooks/*.log

# 统计今日完成
grep -c '\[x\]' .claude/todo.md
```

---

## 最佳实践

### 1. 任务粒度控制
- 每个任务预计 30-60 分钟
- 涉及文件不超过 3 个
- 功能单一明确

### 2. 定期检查
- 每完成 5 个任务检查一次
- 确认代码质量
- 更新 todo.md

### 3. 合理休息
- 连续工作 2 小时休息
- 避免疲劳开发
- 保持代码质量

### 4. 及时备份
- 每完成一个阶段提交代码
- 重要节点打标签
- 保留回退选项

---

*文档版本: v1.0*
*最后更新: 2025-01-13*
