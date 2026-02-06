#!/usr/bin/env python3
"""
Script Helper para Resetear Contraseña Manualmente
===================================================

Este script te ayuda a resetear tu contraseña cuando SMTP no está configurado.

Uso:
    python reset_password_helper.py
"""
import requests
import json

# Configuración
API_URL = "http://localhost:8000"

def solicitar_token(email):
    """Paso 1: Solicitar token de reseteo."""
    print(f"\n🔄 Solicitando token para: {email}")

    response = requests.post(
        f"{API_URL}/auth/forgot-password",
        json={"email": email}
    )

    if response.status_code == 200:
        print("✅ Solicitud exitosa!")
        print("📋 Ahora busca el token en los logs del backend.")
        print("\nEjecuta este comando en otra terminal:")
        print('tail -n 100 "C:\\Users\\mfabi\\AppData\\Local\\Temp\\claude\\C--Users-mfabi-OneDrive-Escritorio-Posgrado-IA-Taller-A-proyecto-final\\tasks\\b757d89.output" | grep "Token de reseteo"')
        print("\nVerás algo como:")
        print('INFO - Token de reseteo para tu_usuario: AbCdEf123...XyZ456')
        print("\nCopia el token completo.")
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False

def resetear_password(token, new_password):
    """Paso 2: Resetear contraseña con el token."""
    print(f"\n🔐 Reseteando contraseña...")

    response = requests.post(
        f"{API_URL}/auth/reset-password",
        json={
            "token": token,
            "new_password": new_password
        }
    )

    if response.status_code == 200:
        print("✅ ¡Contraseña reseteada exitosamente!")
        print("🎉 Ya puedes iniciar sesión con tu nueva contraseña.")
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())
        return False

def main():
    """Función principal."""
    print("=" * 60)
    print("  🔐 RESETEAR CONTRASEÑA - MODO MANUAL")
    print("=" * 60)

    print("\n¿Qué deseas hacer?")
    print("1. Solicitar token de reseteo")
    print("2. Resetear contraseña (ya tengo el token)")
    print("3. Proceso completo (solicitar + resetear)")

    opcion = input("\nElige una opción (1/2/3): ").strip()

    if opcion == "1":
        email = input("\nIngresa tu email: ").strip()
        solicitar_token(email)

    elif opcion == "2":
        token = input("\nIngresa el token completo: ").strip()
        new_password = input("Ingresa tu nueva contraseña: ").strip()
        confirm_password = input("Confirma tu nueva contraseña: ").strip()

        if new_password != confirm_password:
            print("❌ Las contraseñas no coinciden!")
            return

        if len(new_password) < 8:
            print("❌ La contraseña debe tener al menos 8 caracteres!")
            return

        resetear_password(token, new_password)

    elif opcion == "3":
        email = input("\nIngresa tu email: ").strip()

        if solicitar_token(email):
            print("\n" + "=" * 60)
            input("\n⏸️  Presiona ENTER cuando tengas el token copiado...")

            token = input("\nPega el token aquí: ").strip()
            new_password = input("Ingresa tu nueva contraseña: ").strip()
            confirm_password = input("Confirma tu nueva contraseña: ").strip()

            if new_password != confirm_password:
                print("❌ Las contraseñas no coinciden!")
                return

            if len(new_password) < 8:
                print("❌ La contraseña debe tener al menos 8 caracteres!")
                return

            resetear_password(token, new_password)
    else:
        print("❌ Opción inválida!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Operación cancelada.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
