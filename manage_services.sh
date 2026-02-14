#!/bin/bash
# Script de gestión de servicios del proyecto

PROJECT_DIR="C:/Users/mfabi/OneDrive/Escritorio/Posgrado IA/Taller A/proyecto_final"

case "$1" in
  start)
    echo "Iniciando servicios..."
    cd "$PROJECT_DIR"
    source venv/Scripts/activate

    # Iniciar backend en background
    uvicorn backend.main:app --reload --port 8000 &
    echo "Backend iniciado (PID: $!)"

    # Esperar un poco
    sleep 3

    # Iniciar dashboard en background
    streamlit run dashboard/app.py &
    echo "Dashboard iniciado (PID: $!)"

    echo ""
    echo "✓ Servicios iniciados:"
    echo "  - Backend: http://localhost:8000"
    echo "  - Dashboard: http://localhost:8501"
    ;;

  stop)
    echo "Deteniendo servicios..."
    pkill -f uvicorn && echo "✓ Backend detenido"
    pkill -f streamlit && echo "✓ Dashboard detenido"
    ;;

  restart)
    echo "Reiniciando servicios..."
    $0 stop
    sleep 2
    $0 start
    ;;

  status)
    echo "Estado de servicios:"
    echo ""
    echo "Backend (uvicorn):"
    pgrep -a uvicorn || echo "  No está corriendo"
    echo ""
    echo "Dashboard (streamlit):"
    pgrep -a streamlit || echo "  No está corriendo"
    echo ""
    echo "Puertos:"
    netstat -ano | findstr :8000 || echo "  Puerto 8000: libre"
    netstat -ano | findstr :8501 || echo "  Puerto 8501: libre"
    ;;

  *)
    echo "Uso: $0 {start|stop|restart|status}"
    echo ""
    echo "Comandos:"
    echo "  start   - Inicia backend y dashboard"
    echo "  stop    - Detiene todos los servicios"
    echo "  restart - Reinicia los servicios"
    echo "  status  - Muestra el estado actual"
    exit 1
    ;;
esac
