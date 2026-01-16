#!/bin/bash
# 安装 Git Hooks 脚本
# Install Git Hooks for Constitution Recognition Project

set -e

echo "🔧 配置 Git Hooks..."
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# 创建 .git/hooks 目录（如果不存在）
HOOKS_DIR="$PROJECT_ROOT/.git/hooks"
mkdir -p "$HOOKS_DIR"

echo "📁 Hooks 目录: $HOOKS_DIR"
echo ""

# 复制 pre-commit hook
if [ -f "$PROJECT_ROOT/backend/.git/hooks/pre-commit" ]; then
    cp "$PROJECT_ROOT/backend/.git/hooks/pre-commit" "$HOOKS_DIR/pre-commit"
    chmod +x "$HOOKS_DIR/pre-commit"
    echo -e "${GREEN}✅ pre-commit hook 已安装${NC}"
else
    echo -e "${YELLOW}⚠️  未找到 pre-commit hook 文件${NC}"
fi

# 创建 pre-push hook
cat > "$HOOKS_DIR/pre-push" << 'EOF'
#!/bin/bash
# Pre-push Hook: 推送前运行完整测试套件

set -e

echo "🚀 运行 pre-push 测试..."
echo ""

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT/backend"

# 运行完整测试套件
echo "运行完整后端测试套件..."
if pytest tests/ -v --tb=short --cov=api --cov-report=term-missing; then
    echo "✅ 所有测试通过"
else
    echo "❌ 测试失败"
    echo "提示: 使用 --no-verify 跳过 pre-push hook"
    exit 1
fi
EOF

chmod +x "$HOOKS_DIR/pre-push"
echo -e "${GREEN}✅ pre-push hook 已安装${NC}"

# 创建 commit-msg hook（检查提交信息格式）
cat > "$HOOKS_DIR/commit-msg" << 'EOF'
#!/bin/bash
# Commit-msg Hook: 验证提交信息格式

COMMIT_MSG_FILE=$1
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

# 检查提交信息长度（至少5个字符）
if [ ${#COMMIT_MSG} -lt 5 ]; then
    echo "❌ 提交信息太短（至少5个字符）"
    exit 1
fi

# 检查是否遵循约定式提交格式（可选）
if ! echo "$COMMIT_MSG" | grep -qE "^(feat|fix|docs|style|refactor|test|chore|build|ci|perf|revert)(\(.+\))?: "; then
    echo "⚠️  建议使用约定式提交格式："
    echo "   feat: 添加新功能"
    echo "   fix: 修复bug"
    echo "   test: 添加测试"
    echo "   docs: 更新文档"
    # 不阻止提交，只是警告
fi

exit 0
EOF

chmod +x "$HOOKS_DIR/commit-msg"
echo -e "${GREEN}✅ commit-msg hook 已安装${NC}"

echo ""
echo -e "${GREEN}✅ Git Hooks 配置完成！${NC}"
echo ""
echo "已安装的 hooks:"
echo "  • pre-commit  - 提交前运行测试"
echo "  • pre-push    - 推送前运行完整测试"
echo "  • commit-msg  - 验证提交信息格式"
echo ""
echo "跳过 hooks: git commit --no-verify ..."
