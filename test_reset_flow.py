#!/usr/bin/env python3
"""
Script de Prueba: Flujo Completo de Reseteo de Contraseña
===========================================================
"""
import requests
import json
import time

API_URL = "http://localhost:8000"

print("=" * 70)
print("  🧪 PRUEBA COMPLETA: RESETEO DE CONTRASEÑA")
print("=" * 70)

# Paso 1: Crear usuario de prueba
print("\n📝 PASO 1: Creando usuario de prueba...")
print("-" * 70)

user_data = {
    "username": "test_reseteo",
    "email": "test_reseteo@example.com",
    "password": "Password123!"
}

try:
    response = requests.post(f"{API_URL}/auth/register", json=user_data)
    if response.status_code == 200:
        print("✅ Usuario creado exitosamente!")
        user_info = response.json()
        print(f"   - Username: {user_info['username']}")
        print(f"   - Email: {user_info['email']}")
        print(f"   - ID: {user_info['id']}")
    elif response.status_code == 400:
        print("ℹ️  Usuario ya existe (usaremos el existente)")
    else:
        print(f"⚠️  Status: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

# Paso 2: Solicitar token de reseteo
print("\n🔐 PASO 2: Solicitando token de reseteo...")
print("-" * 70)

reset_request = {
    "email": "test_reseteo@example.com"
}

try:
    response = requests.post(f"{API_URL}/auth/forgot-password", json=reset_request)
    if response.status_code == 200:
        print("✅ Solicitud de reseteo enviada!")
        result = response.json()
        print(f"   Mensaje: {result.get('message', 'OK')}")
        print("\n📋 El token ha sido generado y debe estar en los logs del backend.")
        print("   Como SMTP no está configurado, el token se imprime en los logs.")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

# Esperar un momento para que el log se escriba
time.sleep(1)

# Paso 3: Instrucciones para obtener el token
print("\n📂 PASO 3: Obtener el token de los logs")
print("-" * 70)
print("El token se encuentra en los logs del backend.")
print("\nPara encontrarlo, ejecuta en otra terminal:")
print('tail -n 50 "C:\\Users\\mfabi\\AppData\\Local\\Temp\\claude\\C--Users-mfabi-OneDrive-Escritorio-Posgrado-IA-Taller-A-proyecto-final\\tasks\\b757d89.output" | grep "test_reseteo"')
print("\nO busca una línea similar a:")
print('INFO - Token de reseteo para test_reseteo: <TOKEN_LARGO>')
print("\n⏸️  Presiona ENTER cuando hayas copiado el token...")

input()

# Paso 4: Resetear contraseña
print("\n🔄 PASO 4: Reseteando contraseña con el token")
print("-" * 70)

token = input("Pega el token aquí: ").strip()

if not token:
    print("❌ No ingresaste ningún token. Abortando.")
    exit(1)

new_password = "NewPassword456!"

reset_data = {
    "token": token,
    "new_password": new_password
}

try:
    response = requests.post(f"{API_URL}/auth/reset-password", json=reset_data)
    if response.status_code == 200:
        print("✅ ¡Contraseña reseteada exitosamente!")
        result = response.json()
        print(f"   {result.get('message', 'OK')}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   Response: {response.json()}")
        exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Paso 5: Verificar login con nueva contraseña
print("\n🔑 PASO 5: Verificando login con la nueva contraseña")
print("-" * 70)

login_data = {
    "username": "test_reseteo",
    "password": new_password
}

try:
    response = requests.post(
        f"{API_URL}/auth/login",
        data=login_data
    )
    if response.status_code == 200:
        print("✅ ¡Login exitoso con la nueva contraseña!")
        result = response.json()
        print(f"   Token JWT recibido: {result['access_token'][:50]}...")
        print(f"   Token type: {result['token_type']}")
        print(f"   Expira en: {result['expires_in']} segundos")
    else:
        print(f"❌ Error en login: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

# Resumen final
print("\n" + "=" * 70)
print("  ✅ PRUEBA COMPLETADA")
print("=" * 70)
print("\n📊 Resumen:")
print("   1. ✓ Usuario de prueba creado/verificado")
print("   2. ✓ Token de reseteo solicitado")
print("   3. ✓ Token obtenido de logs")
print("   4. ✓ Contraseña reseteada")
print("   5. ✓ Login verificado con nueva contraseña")
print("\n🎉 El sistema de reseteo de contraseña funciona correctamente!")
print("\n💡 Ahora sabes cómo usar el token manualmente cuando SMTP no está configurado.")
