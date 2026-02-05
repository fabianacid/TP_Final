#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación de instalación y configuración
Sistema Multiagente de Seguimiento Financiero

Ejecutar: python check_setup.py
"""

import sys
import os
from pathlib import Path

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_check(item, status, message=""):
    """Imprime el resultado de una verificación"""
    try:
        icon = "✅" if status else "❌"
    except:
        icon = "[OK]" if status else "[X]"

    try:
        print(f"{icon} {item}", end="")
        if message:
            print(f": {message}")
        else:
            print()
    except UnicodeEncodeError:
        icon = "[OK]" if status else "[X]"
        print(f"{icon} {item}", end="")
        if message:
            print(f": {message}")
        else:
            print()

def check_python_version():
    """Verifica la versión de Python"""
    print_header("Verificando Python")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    is_valid = version.major == 3 and version.minor >= 8
    print_check(
        "Versión de Python",
        is_valid,
        f"{version_str} {'(OK)' if is_valid else '(Se requiere 3.8+)'}"
    )
    return is_valid

def check_dependencies():
    """Verifica que las dependencias principales estén instaladas"""
    print_header("Verificando Dependencias Principales")

    dependencies = {
        "fastapi": "FastAPI",
        "uvicorn": "Uvicorn",
        "sqlalchemy": "SQLAlchemy",
        "pydantic": "Pydantic",
        "pandas": "Pandas",
        "numpy": "NumPy",
        "sklearn": "scikit-learn",
        "yfinance": "yfinance",
        "streamlit": "Streamlit",
    }

    all_ok = True
    for module, name in dependencies.items():
        try:
            __import__(module.replace("-", "_"))
            print_check(name, True, "Instalado")
        except ImportError:
            print_check(name, False, "NO instalado")
            all_ok = False

    return all_ok

def check_optional_dependencies():
    """Verifica dependencias opcionales"""
    print_header("Verificando Dependencias Opcionales")

    optional_deps = {
        "torch": "PyTorch (para LSTM)",
        "transformers": "Transformers (para FinBERT)",
        "xgboost": "XGBoost",
        "lightgbm": "LightGBM",
    }

    for module, name in optional_deps.items():
        try:
            __import__(module)
            print_check(name, True, "Instalado")
        except ImportError:
            print_check(name, False, "No instalado (opcional)")

def check_project_structure():
    """Verifica la estructura del proyecto"""
    print_header("Verificando Estructura del Proyecto")

    required_paths = [
        ("backend/", "Directorio backend"),
        ("backend/main.py", "Archivo main.py"),
        ("backend/agents/", "Directorio de agentes"),
        ("backend/routers/", "Directorio de routers"),
        ("dashboard/app.py", "Dashboard de Streamlit"),
        ("requirements.txt", "Archivo de dependencias"),
        (".env.example", "Ejemplo de configuración"),
    ]

    all_ok = True
    for path, description in required_paths:
        exists = Path(path).exists()
        print_check(description, exists, path if exists else "NO ENCONTRADO")
        if not exists:
            all_ok = False

    return all_ok

def check_env_file():
    """Verifica el archivo .env"""
    print_header("Verificando Configuración (.env)")

    env_exists = Path(".env").exists()
    print_check("Archivo .env existe", env_exists)

    if not env_exists:
        print("\n[!] ADVERTENCIA: Archivo .env no encontrado")
        print("    Ejecuta: cp .env.example .env")
        print("    Y configura SECRET_KEY con una clave segura")
        return False

    # Verificar contenido básico
    try:
        with open(".env", "r") as f:
            content = f.read()

        has_secret = "SECRET_KEY=" in content
        has_default = "tu_clave_secreta" in content or "cambiar_en_produccion" in content

        print_check("SECRET_KEY configurado", has_secret)

        if has_default:
            print("[!] ADVERTENCIA: SECRET_KEY parece usar el valor por defecto")
            print("    Genera una clave segura con:")
            print("    python -c \"import secrets; print(secrets.token_urlsafe(32))\"")

        return has_secret
    except Exception as e:
        print_check("Lectura de .env", False, str(e))
        return False

def check_database():
    """Verifica la base de datos"""
    print_header("Verificando Base de Datos")

    db_exists = Path("financial_tracker.db").exists()
    print_check(
        "Base de datos SQLite",
        True,
        "Existente" if db_exists else "Se creará al iniciar el backend"
    )

    return True

def check_ports():
    """Verifica que los puertos necesarios estén disponibles"""
    print_header("Verificando Puertos")

    import socket

    ports = {
        8000: "Backend (FastAPI)",
        8501: "Dashboard (Streamlit)",
    }

    all_ok = True
    for port, service in ports.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()

        is_available = result != 0
        status = "Disponible" if is_available else "En uso"
        print_check(f"Puerto {port} ({service})", is_available, status)

        if not is_available:
            all_ok = False

    return all_ok

def provide_recommendations():
    """Proporciona recomendaciones basadas en los checks"""
    print_header("Recomendaciones")

    print("""
Para instalar dependencias faltantes:
    pip install -r requirements.txt

Para instalar dependencias opcionales (recomendado):
    pip install torch transformers xgboost lightgbm

Para configurar el sistema:
    1. cp .env.example .env
    2. Editar .env y configurar SECRET_KEY
    3. python -c "import secrets; print(secrets.token_urlsafe(32))"

Para iniciar el sistema:
    Terminal 1: uvicorn backend.main:app --reload
    Terminal 2: streamlit run dashboard/app.py

Documentación completa: README.md
    """)

def main():
    """Función principal"""
    try:
        separator = "🔍 " * 20
    except:
        separator = "=" * 60

    print("\n" + separator)
    print("   VERIFICACIÓN DE INSTALACIÓN")
    print("   Sistema Multiagente de Seguimiento Financiero")
    print(separator)

    results = []

    # Ejecutar todas las verificaciones
    results.append(("Python", check_python_version()))
    results.append(("Dependencias", check_dependencies()))
    check_optional_dependencies()  # Solo informativo
    results.append(("Estructura", check_project_structure()))
    results.append(("Configuración", check_env_file()))
    results.append(("Base de datos", check_database()))
    results.append(("Puertos", check_ports()))

    # Resumen final
    print_header("Resumen")

    all_passed = all(result[1] for result in results)
    critical_passed = results[0][1] and results[1][1] and results[3][1]  # Python, deps, env

    if all_passed:
        print("[OK] ¡Todo está configurado correctamente!")
        print("     El sistema está listo para ejecutarse.")
    elif critical_passed:
        print("[!]  Configuración parcial detectada")
        print("     El sistema puede ejecutarse, pero revisa las advertencias arriba.")
    else:
        print("[X]  Se encontraron problemas críticos")
        print("     Corrige los errores marcados antes de ejecutar.")

    # Mostrar recomendaciones si hay problemas
    if not all_passed:
        provide_recommendations()

    print("\n" + "=" * 60)

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
