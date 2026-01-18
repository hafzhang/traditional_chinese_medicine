@echo off
REM Frontend test runner for pre-commit hook (Windows)
REM This script runs fast tests only during commit

setlocal enabledelayedexpansion

echo 🧪 Running Frontend Tests...
echo.

REM Check if frontend directory exists
if not exist "frontend\" (
    echo ⚠️  Frontend directory not found, skipping tests
    exit /b 0
)

cd frontend

REM Check if node_modules exists
if not exist "node_modules\" (
    echo ⚠️  No node_modules found, installing dependencies...
    call npm install
)

REM Run unit tests
echo 🔍 Running unit tests...
call npm run test:unit
if errorlevel 1 (
    echo ❌ Frontend tests failed!
    echo.
    echo 💡 Tip: Run 'npm run test:unit -- --reporter=verbose' to see detailed errors
    exit /b 1
)

echo ✅ Frontend tests passed!
