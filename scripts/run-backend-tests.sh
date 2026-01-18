#!/bin/bash
# Backend test runner for pre-commit hook
# This script runs fast tests only during commit

set -e

echo "🧪 Running Backend Tests..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if backend directory exists
if [ ! -d "backend" ]; then
    echo -e "${YELLOW}⚠️  Backend directory not found, skipping tests${NC}"
    exit 0
fi

# Change to backend directory
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo -e "${YELLOW}⚠️  No virtual environment found, creating one...${NC}"
    python -m venv venv
    source venv/bin/activate
    pip install -q pytest pytest-cov pytest-asyncio httpx
else
    # Activate virtual environment
    if [ -d "venv" ]; then
        source venv/bin/activate
    elif [ -d ".venv" ]; then
        source .venv/bin/activate
    fi
fi

# Run fast tests only (skip slow and integration tests)
echo "🔍 Running unit tests..."
if pytest tests/test_unit/ -v --tb=short -x -m "not slow" 2>&1; then
    echo -e "${GREEN}✅ Backend tests passed!${NC}"
else
    echo -e "${RED}❌ Backend tests failed!${NC}"
    echo ""
    echo "💡 Tip: Run 'pytest -v' in backend/ to see detailed errors"
    exit 1
fi
