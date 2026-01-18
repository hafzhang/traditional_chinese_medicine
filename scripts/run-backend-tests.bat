@echo off
REM Backend test runner for pre-commit hook (Windows)
REM This script runs fast tests only during commit

setlocal enabledelayedexpansion

echo 🧪 Running Backend Tests...
echo.

REM Check if backend directory exists
if not exist "backend\" (
    echo ⚠️  Backend directory not found, skipping tests
    exit /b 0
)

cd backend

REM Check if virtual environment exists
if not exist "venv\" (
    if not exist ".venv\" (
        echo ⚠️  No virtual environment found
        exit /b 0
    )
)

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

REM Run fast tests only
echo 🔍 Running unit tests...
pytest tests/test_unit/ -v --tb=short -x -m "not slow"
if errorlevel 1 (
    echo ❌ Backend tests failed!
    echo.
    echo 💡 Tip: Run 'pytest -v' in backend\ to see detailed errors
    exit /b 1
)

echo ✅ Backend tests passed!
