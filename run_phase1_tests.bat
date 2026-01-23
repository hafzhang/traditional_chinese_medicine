@echo off
echo ========================================
echo 中医养生平台 - Phase 1 完整测试脚本
echo ========================================
echo.

echo 此脚本将运行所有 Phase 1 功能的测试
echo.

set BACKEND_PASSED=0
set FRONTEND_PASSED=0

REM ==================== 后端测试 ====================
echo.
echo [后端测试]
echo ========================================
cd backend

echo 运行 Phase 1 后端测试...
python -m pytest tests/test_unit/test_ingredients.py ^
                tests/test_unit/test_recipes.py ^
                tests/test_unit/test_acupoints.py ^
                tests/test_unit/test_tongue_diagnosis.py ^
                tests/test_unit/test_courses.py ^
                tests/test_api/test_ingredients_api.py ^
                tests/test_api/test_recipes_api.py ^
                tests/test_api/test_acupoints_api.py ^
                tests/test_api/test_tongue_diagnosis_api.py ^
                tests/test_api/test_courses_api.py ^
                -v --tb=short

if errorlevel 1 (
    echo [错误] 后端测试失败
    set BACKEND_PASSED=0
) else (
    echo [成功] 后端测试通过
    set BACKEND_PASSED=1
)

cd ..

REM ==================== 前端测试 ====================
echo.
echo [前端测试]
echo ========================================
cd frontend

echo 运行 Phase 1 前端 API 测试...
call npm run test:unit -- tests/unit/ingredients-api.spec.js ^
                           tests/unit/recipes-api.spec.js ^
                           tests/unit/acupoints.spec.js ^
                           tests/unit/tongue.spec.js ^
                           tests/unit/courses.spec.js ^
                           --run

if errorlevel 1 (
    echo [错误] 前端测试失败
    set FRONTEND_PASSED=0
) else (
    echo [成功] 前端测试通过
    set FRONTEND_PASSED=1
)

cd ..

REM ==================== 总结 ====================
echo.
echo ========================================
echo 测试总结
echo ========================================
echo 后端测试: %BACKEND_PASSED%
echo 前端测试: %FRONTEND_PASSED%
echo.

if %BACKEND_PASSED%==1 if %FRONTEND_PASSED%==1 (
    echo [成功] Phase 1 所有测试通过！
    echo.
    echo 测试覆盖范围:
    echo   后端:
    echo     - 食材服务 (ingredients)
    echo     - 食谱服务 (recipes)
    echo     - 穴位服务 (acupoints)
    echo     - 舌诊服务 (tongue diagnosis)
    echo     - 课程服务 (courses)
    echo   前端:
    echo     - 食材 API
    echo     - 食谱 API
    echo     - 穴位 API
    echo     - 舌诊 API
    echo     - 课程 API
    echo.
    pause
    exit /b 0
) else (
    echo [失败] 部分测试未通过，请检查错误信息
    echo.
    pause
    exit /b 1
)
