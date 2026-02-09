#!/bin/bash

echo "╔═══════════════════════════════════════════════╗"
echo "║  🧪 EJECUTANDO SUITE COMPLETA DE PRUEBAS     ║"
echo "╚═══════════════════════════════════════════════╝"
echo ""

# Verificar que el backend esté corriendo
echo "🔍 Verificando que el backend esté activo..."
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ Backend respondiendo en puerto 8000"
else
    echo "❌ Backend no está corriendo"
    echo "   Inicia el backend con: uvicorn backend.main:app --reload"
    exit 1
fi

# Instalar dependencias de testing
echo ""
echo "📦 Instalando dependencias de testing..."
pip install -r requirements-test.txt

# Crear directorio de resultados
mkdir -p test_results

# Ejecutar pruebas funcionales
echo ""
echo "🧪 [1/2] Ejecutando pruebas funcionales..."
python tests/test_functional.py

# Ejecutar pruebas de rendimiento
echo ""
echo "⚡ [2/2] Ejecutando pruebas de rendimiento..."
python tests/test_performance.py

echo ""
echo "✅ ¡Todas las pruebas completadas!"
echo "📂 Resultados guardados en: test_results/"
