@echo off
echo ╔═══════════════════════════════════════════════╗
echo ║  🧪 EJECUTANDO SUITE COMPLETA DE PRUEBAS     ║
echo ╚═══════════════════════════════════════════════╝
echo.

echo 🔍 Verificando que el backend esté activo...
curl -s http://localhost:8000/ >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Backend no está corriendo
    echo    Inicia el backend con: uvicorn backend.main:app --reload
    pause
    exit /b 1
)
echo ✅ Backend respondiendo en puerto 8000

echo.
echo 📦 Instalando dependencias de testing...
pip install -r requirements-test.txt

echo.
if not exist test_results mkdir test_results

echo.
echo 🧪 [1/2] Ejecutando pruebas funcionales...
python tests\test_functional.py

echo.
echo ⚡ [2/2] Ejecutando pruebas de rendimiento...
python tests\test_performance.py

echo.
echo ✅ ¡Todas las pruebas completadas!
echo 📂 Resultados guardados en: test_results\
pause
