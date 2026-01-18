#!/bin/bash
# Frontend test runner for pre-commit hook
# This script runs fast tests only during commit

set -e

echo "🧪 Running Frontend Tests..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
    echo -e "${YELLOW}⚠️  Frontend directory not found, skipping tests${NC}"
    exit 0
fi

# Change to frontend directory
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}⚠️  No node_modules found, installing dependencies...${NC}"
    npm install > /dev/null 2>&1
fi

# Check if vitest is available
if ! command -v npx &> /dev/null && [ ! -f "node_modules/.bin/vitest" ]; then
    echo -e "${YELLOW}⚠️  Vitest not found, skipping tests${NC}"
    exit 0
fi

# Run unit tests only (skip E2E and slow tests)
echo "🔍 Running unit tests..."
if npm run test:unit 2>&1; then
    echo -e "${GREEN}✅ Frontend tests passed!${NC}"
else
    echo -e "${RED}❌ Frontend tests failed!${NC}"
    echo ""
    echo "💡 Tip: Run 'npm run test:unit -- --reporter=verbose' to see detailed errors"
    exit 1
fi
