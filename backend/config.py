"""
Configuración del Sistema de Seguimiento Financiero

Este módulo gestiona la configuración del sistema mediante
variables de entorno, siguiendo las mejores prácticas de
seguridad recomendadas por OWASP.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Clase de configuración basada en Pydantic Settings.

    Carga automáticamente los valores desde variables de entorno
    o desde un archivo .env, sin exponer información sensible
    en el código fuente.
    """

    # Configuración de seguridad JWT
    SECRET_KEY: str = "clave_secreta_desarrollo_cambiar_en_produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Base de datos
    DATABASE_URL: str = "sqlite:///./financial_tracker.db"

    # Configuración de correo electrónico (opcional)
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None

    # Umbrales de alertas (en porcentaje)
    ALERT_THRESHOLD_WARNING: float = 3.0
    ALERT_THRESHOLD_CRITICAL: float = 7.0

    # Configuración de la aplicación
    APP_NAME: str = "Sistema de Seguimiento Financiero"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # CORS - Orígenes permitidos
    CORS_ORIGINS: list = ["http://localhost:8501", "http://localhost:3000", "http://127.0.0.1:8501"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()
