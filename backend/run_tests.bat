@echo off
echo ========================================
echo 中医养生平台 - Phase 1 后端测试运行脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.11+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/5] 检测到Python版本:
python --version
echo.

REM 检查虚拟环境
if not exist "venv" (
    echo [2/5] 创建虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo [错误] 虚拟环境创建失败
        pause
        exit /b 1
    )
) else (
    echo [2/5] 虚拟环境已存在
)

echo.
echo [3/5] 激活虚拟环境...
call venv\Scripts\activate.bat

echo.
echo [4/5] 安装/更新依赖包...
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo.
echo [5/5] 运行 Phase 1 测试...
echo ========================================
echo.
echo [Phase 1 单元测试]
echo ------------------------
pytest tests/test_unit/test_ingredients.py ^
       tests/test_unit/test_recipes.py ^
       tests/test_unit/test_acupoints.py ^
       tests/test_unit/test_tongue_diagnosis.py ^
       tests/test_unit/test_courses.py ^
       -v --tb=short

if errorlevel 1 (
    echo.
    echo [错误] Phase 1 单元测试失败
    pause
    exit /b 1
)

echo.
echo [Phase 1 API 测试]
echo ------------------------
pytest tests/test_api/test_ingredients_api.py ^
       tests/test_api/test_recipes_api.py ^
       tests/test_api/test_acupoints_api.py ^
       tests/test_api/test_tongue_diagnosis_api.py ^
       tests/test_api/test_courses_api.py ^
       -v --tb=short

if errorlevel 1 (
    echo.
    echo [错误] Phase 1 API 测试失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo Phase 1 测试全部通过！
echo ========================================
echo.
echo 测试覆盖范围:
echo   - 食材服务 (ingredients)
echo   - 食谱服务 (recipes)
echo   - 穴位服务 (acupoints)
echo   - 舌诊服务 (tongue diagnosis)
echo   - 课程服务 (courses)
echo.
pause
