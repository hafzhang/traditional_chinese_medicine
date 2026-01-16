#!/bin/bash
# 快速运行测试脚本
# Quick Test Runner for Constitution Recognition Project

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 帮助信息
function show_help() {
    echo "🧪 体质识别项目测试运行器"
    echo ""
    echo "用法: ./scripts/run_tests.sh [选项]"
    echo ""
    echo "选项:"
    echo "  -a, --all          运行所有测试（后端+前端）"
    echo "  -b, --backend      仅运行后端测试"
    echo "  -f, --frontend     仅运行前端测试"
    echo "  -s, --scoring      仅运行评分算法测试"
    echo "  --api              仅运行 API 测试"
    echo "  --unit             仅运行单元测试"
    echo "  --cov              生成覆盖率报告"
    echo "  -h, --help         显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  ./scripts/run_tests.sh --all         # 运行所有测试"
    echo "  ./scripts/run_tests.sh --scoring     # 只测试评分算法"
    echo "  ./scripts/run_tests.sh --backend --cov  # 后端测试+覆盖率"
}

# 默认参数
RUN_BACKEND=false
RUN_FRONTEND=false
SCORING_ONLY=false
API_ONLY=false
UNIT_ONLY=false
COVERAGE=false

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -a|--all)
            RUN_BACKEND=true
            RUN_FRONTEND=true
            shift
            ;;
        -b|--backend)
            RUN_BACKEND=true
            shift
            ;;
        -f|--frontend)
            RUN_FRONTEND=true
            shift
            ;;
        -s|--scoring)
            SCORING_ONLY=true
            RUN_BACKEND=true
            shift
            ;;
        --api)
            API_ONLY=true
            RUN_BACKEND=true
            shift
            ;;
        --unit)
            UNIT_ONLY=true
            RUN_BACKEND=true
            shift
            ;;
        --cov)
            COVERAGE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}未知选项: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# 如果没有指定任何选项，运行所有测试
if [ "$RUN_BACKEND" = false ] && [ "$RUN_FRONTEND" = false ]; then
    RUN_BACKEND=true
    RUN_FRONTEND=true
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# ==================== 后端测试 ====================
if [ "$RUN_BACKEND" = true ]; then
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}📦 运行后端测试${NC}"
    echo -e "${BLUE}======================================${NC}"
    echo ""

    cd backend

    # 检查 Python 环境
    if ! command -v python &> /dev/null; then
        echo -e "${RED}❌ 未找到 Python，无法运行后端测试${NC}"
        exit 1
    fi

    # 检查虚拟环境
    if [ -d "venv" ]; then
        source venv/bin/activate
    elif [ -d ".venv" ]; then
        source .venv/bin/activate
    fi

    # 检查 pytest
    if ! command -v pytest &> /dev/null; then
        echo "安装 pytest..."
        pip install pytest pytest-cov pytest-asyncio -q
    fi

    # 构建测试命令
    PYTEST_CMD="pytest tests/ -v --tb=short"

    if [ "$SCORING_ONLY" = true ]; then
        PYTEST_CMD="pytest tests/test_constitution_scorer.py -v -k 'scoring or Scorer'"
        echo "🎯 运行评分算法测试..."
    elif [ "$API_ONLY" = true ]; then
        PYTEST_CMD="pytest tests/test_api_endpoints.py -v"
        echo "🌐 运行 API 端点测试..."
    elif [ "$UNIT_ONLY" = true ]; then
        PYTEST_CMD="pytest tests/ -v -m 'unit'"
        echo "🔬 运行单元测试..."
    fi

    if [ "$COVERAGE" = true ]; then
        PYTEST_CMD="$PYTEST_CMD --cov=api --cov-report=html:htmlcov --cov-report=term"
        echo "📊 生成覆盖率报告..."
    fi

    echo ""
    echo "执行: $PYTEST_CMD"
    echo ""

    if eval $PYTEST_CMD; then
        echo -e "${GREEN}✅ 后端测试通过${NC}"
    else
        echo -e "${RED}❌ 后端测试失败${NC}"
        exit 1
    fi

    cd ..
fi

# ==================== 前端测试 ====================
if [ "$RUN_FRONTEND" = true ]; then
    echo ""
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}🌐 运行前端测试${NC}"
    echo -e "${BLUE}======================================${NC}"
    echo ""

    cd frontend

    # 检查 Node 环境
    if ! command -v node &> /dev/null; then
        echo -e "${YELLOW}⚠️  未找到 Node.js，跳过前端测试${NC}"
        cd ..
        exit 0
    fi

    echo "运行前端测试..."
    if node tests/constitution.test.js; then
        echo -e "${GREEN}✅ 前端测试通过${NC}"
    else
        echo -e "${RED}❌ 前端测试失败${NC}"
        exit 1
    fi

    cd ..
fi

# ==================== 总结 ====================
echo ""
echo -e "${BLUE}======================================${NC}"
echo -e "${GREEN}✅ 所有测试完成！${NC}"
echo -e "${BLUE}======================================${NC}"

if [ "$COVERAGE" = true ] && [ "$RUN_BACKEND" = true ]; then
    echo ""
    echo "📊 覆盖率报告: backend/htmlcov/index.html"
fi
