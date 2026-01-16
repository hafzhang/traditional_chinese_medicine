# 无人值守自主开发系统 - 最后 5 分钟 Checklist

## 快速设置步骤

### ✅ 已完成

- [x] 创建 todo.md 并初始化任务
- [x] 新增 3 个钩子（auto_plan_next / load_small_template / check_priority）
- [x] 放 task_templates/ 模板 & priority.rules
- [x] 给 retry_counter.json 加死循环保护
- [x] 更新 hooks.json 至 v2.0.0（添加 autonomous_mode 配置）

---

### 📋 待确认（5 分钟内）

#### 1. 文件权限（30 秒）

```bash
chmod +x scripts/hooks/*.sh
```

#### 2. 测试自动规划（30 秒）

```bash
bash scripts/hooks/auto_plan_next.sh
```

**预期输出**:
```
═══════════════════════════════════════════════════════════════
                    📋 下一个任务
═══════════════════════════════════════════════════════════════

  ⏭️  接口规范评审与确认

  📊 今日进度: 2/5 完成 (40%)

  💡 提示: 完成后请在 todo.md 中将 [ ] 改为 [x]

  📝 文件位置: .claude/todo.md

═══════════════════════════════════════════════════════════════
```

#### 3. 测试优先级检查（30 秒）

```bash
# 测试 MVP 范围内的任务（应该通过）
export CLAUDE_USER_PROMPT="实现体质测试问卷功能"
bash scripts/hooks/check_priority.sh
echo "Exit code: $?"

# 测试超出 MVP 范围的任务（应该警告）
export CLAUDE_USER_PROMPT="添加积分商城功能"
bash scripts/hooks/check_priority.sh
```

#### 4. 测试任务拆分检测（30 秒）

```bash
# 测试大型任务（应该警告）
export CLAUDE_USER_PROMPT="实现完整的体质测试API系统，包括所有接口、数据库、前端页面和测试"
bash scripts/hooks/load_small_template.sh
```

#### 5. 确认 hooks.json 配置（30 秒）

```bash
# 检查 autonomous_mode 是否启用
grep -A 5 "autonomous_mode" .claude/hooks.json
```

**预期输出**:
```json
{
  "autonomous_mode": {
    "enabled": true,
    "max_continuous_hours": 8,
    ...
  }
}
```

#### 6. 验证 todo.md 格式（30 秒）

```bash
# 检查今日目标
grep -A 10 "今日目标" .claude/todo.md

# 统计任务数量
echo "总任务数: $(grep -c '^\s*-\s*\[[x ]\]' .claude/todo.md)"
echo "已完成: $(grep -c '^\s*-\s*\[x\]' .claude/todo.md)"
```

#### 7. 确认文件结构（30 秒）

```bash
# 检查关键文件是否存在
ls -la .claude/todo.md
ls -la .claude/retry_counter.json
ls -la priority.rules
ls -la task_templates/
ls -la scripts/hooks/auto_plan_next.sh
ls -la scripts/hooks/check_priority.sh
ls -la scripts/hooks/load_small_template.sh
```

#### 8. 测试完整流程（2 分钟）

```bash
# 启动自动规划
bash scripts/hooks/auto_plan_next.sh

# 记录下一个任务
NEXT_TASK=$(cat .claude/next_task.txt 2>/dev/null || echo "")
echo "下一个任务: $NEXT_TASK"

# 模拟完成任务
echo "请确认: 是否开始执行 '$NEXT_TASK'？"
```

#### 9. 查看日志目录（30 秒）

```bash
# 确认日志目录存在
ls -la .claude/hooks/

# 查看现有日志
cat .claude/hooks/session.log 2>/dev/null || echo "会话日志尚未创建"
```

#### 10. 阅读快速指南（1 分钟）

```bash
# 打开使用指南
less docs/autonomous_development_guide.md
```

---

## ✅ 完成确认

全部通过后，系统已准备就绪！

### 启动命令

```bash
# 开始自主开发
echo "请开始自主开发，从 todo.md 中的第一个任务开始"

# 或者指定具体任务
echo "请从'搭建 FastAPI 项目脚手架'开始"
```

### 监控命令

```bash
# 实时查看下一个任务（每30秒刷新）
watch -n 30 'bash scripts/hooks/auto_plan_next.sh'

# 查看所有日志
tail -f .claude/hooks/*.log
```

---

## 🎯 第一天目标

### Week 0: 准备阶段（5 个任务）

- [x] 确认 30 题问卷最终版本与题目映射
- [x] 确认首发平台（抖音小程序 / H5）
- [ ] **接口规范评审与确认** ← 下一个任务
- [ ] 食物库样例数据准备（每体质至少 10 条食物数据）
- [ ] 设计稿评审（问卷页、报告页、分享卡片）

### 预计完成时间

- 当前进度: 40%
- 预计剩余时间: 3-4 小时
- 预计达成时间: 今日 18:00

---

## 📞 紧急停止

如需立即停止自主开发：

```bash
# 方法1: 禁用自主模式
# 编辑 .claude/hooks.json
# 将 "autonomous_mode" 的 "enabled" 改为 false

# 方法2: 清空任务队列
echo "" > .claude/todo.md

# 方法3: 添加人工干预标记
# 在 todo.md 中添加: - [!] 人工介入暂停
```

---

## 📚 相关文档

| 文档 | 路径 | 用途 |
|-----|-----|-----|
| 使用指南 | `docs/autonomous_development_guide.md` | 完整使用说明 |
| 任务队列 | `.claude/todo.md` | 所有待办任务 |
| Hooks 配置 | `.claude/hooks.json` | 钩子配置 |
| 优先级规则 | `priority.rules` | 优先级定义 |
| 任务模板 | `task_templates/` | 拆分参考 |

---

*Checklist 版本: v1.0*
*预计设置时间: 5 分钟*
*最后更新: 2025-01-13*
