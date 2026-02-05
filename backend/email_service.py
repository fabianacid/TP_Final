"""
Servicio de Envío de Emails

Este módulo maneja el envío de emails para recuperación de contraseña
y otras notificaciones del sistema.
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from .config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Servicio para envío de emails vía SMTP."""

    @staticmethod
    def send_password_reset_email(
        to_email: str,
        username: str,
        reset_token: str,
        frontend_url: str = "http://localhost:8501"
    ) -> bool:
        """
        Envía email con link de recuperación de contraseña.

        Args:
            to_email: Email del destinatario
            username: Nombre de usuario
            reset_token: Token único de reseteo
            frontend_url: URL del frontend (dashboard)

        Returns:
            bool: True si el email se envió correctamente, False en caso contrario
        """
        try:
            # Verificar que SMTP esté configurado
            if not hasattr(settings, 'SMTP_SERVER') or not settings.SMTP_SERVER:
                logger.warning("SMTP no configurado. Email no enviado.")
                logger.info(f"Token de reseteo para {username}: {reset_token}")
                logger.info("Configura SMTP_SERVER, SMTP_PORT, SMTP_USER y SMTP_PASSWORD en .env")
                return False

            # Crear mensaje
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Recuperación de Contraseña - Sistema Financiero"
            msg['From'] = settings.SMTP_USER
            msg['To'] = to_email

            # Crear link de reseteo
            reset_link = f"{frontend_url}/reset-password?token={reset_token}"

            # Texto plano (fallback)
            text_body = f"""
Hola {username},

Recibimos una solicitud para restablecer tu contraseña.

Para crear una nueva contraseña, haz clic en el siguiente enlace:
{reset_link}

Este enlace expirará en 1 hora por seguridad.

Si no solicitaste restablecer tu contraseña, ignora este email.

Saludos,
Sistema Multiagente de Seguimiento Financiero
"""

            # HTML (versión mejorada)
            html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .header {{
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px 5px 0 0;
        }}
        .content {{
            background-color: white;
            padding: 30px;
            border-radius: 0 0 5px 5px;
        }}
        .button {{
            display: inline-block;
            padding: 12px 30px;
            background-color: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .button:hover {{
            background-color: #2980b9;
        }}
        .warning {{
            background-color: #fff3cd;
            border: 1px solid #ffc107;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .footer {{
            text-align: center;
            color: #7f8c8d;
            font-size: 12px;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 Recuperación de Contraseña</h1>
        </div>
        <div class="content">
            <p>Hola <strong>{username}</strong>,</p>

            <p>Recibimos una solicitud para restablecer tu contraseña en el Sistema Multiagente de Seguimiento Financiero.</p>

            <p>Para crear una nueva contraseña, haz clic en el siguiente botón:</p>

            <center>
                <a href="{reset_link}" class="button">Restablecer Contraseña</a>
            </center>

            <div class="warning">
                <strong>⏰ Importante:</strong> Este enlace expirará en <strong>1 hora</strong> por seguridad.
            </div>

            <p>Si no puedes hacer clic en el botón, copia y pega este enlace en tu navegador:</p>
            <p style="word-break: break-all; background-color: #ecf0f1; padding: 10px; border-radius: 3px;">
                {reset_link}
            </p>

            <hr style="border: none; border-top: 1px solid #ecf0f1; margin: 30px 0;">

            <p><strong>¿No solicitaste restablecer tu contraseña?</strong></p>
            <p>Si no realizaste esta solicitud, puedes ignorar este email de forma segura. Tu contraseña no será modificada.</p>
        </div>
        <div class="footer">
            <p>Sistema Multiagente de Seguimiento Financiero</p>
            <p>Este es un email automático, por favor no respondas a este mensaje.</p>
        </div>
    </div>
</body>
</html>
"""

            # Adjuntar ambas versiones
            part1 = MIMEText(text_body, 'plain')
            part2 = MIMEText(html_body, 'html')
            msg.attach(part1)
            msg.attach(part2)

            # Enviar email
            with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)

            logger.info(f"Email de recuperación enviado a {to_email}")
            return True

        except Exception as e:
            logger.error(f"Error enviando email de recuperación: {str(e)}")
            logger.info(f"Token de reseteo para {username} (usar manualmente): {reset_token}")
            return False

    @staticmethod
    def send_password_changed_confirmation(
        to_email: str,
        username: str
    ) -> bool:
        """
        Envía email de confirmación de cambio de contraseña.

        Args:
            to_email: Email del destinatario
            username: Nombre de usuario

        Returns:
            bool: True si el email se envió correctamente
        """
        try:
            if not hasattr(settings, 'SMTP_SERVER') or not settings.SMTP_SERVER:
                logger.info(f"Contraseña cambiada para {username} (SMTP no configurado)")
                return False

            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Contraseña Modificada - Sistema Financiero"
            msg['From'] = settings.SMTP_USER
            msg['To'] = to_email

            text_body = f"""
Hola {username},

Tu contraseña ha sido modificada exitosamente.

Si no realizaste este cambio, por favor contacta al soporte inmediatamente.

Fecha y hora del cambio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Saludos,
Sistema Multiagente de Seguimiento Financiero
"""

            html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; }}
        .header {{ background-color: #27ae60; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
        .content {{ background-color: white; padding: 30px; border-radius: 0 0 5px 5px; }}
        .success {{ background-color: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .warning {{ background-color: #fff3cd; border: 1px solid #ffc107; padding: 15px; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✅ Contraseña Modificada</h1>
        </div>
        <div class="content">
            <p>Hola <strong>{username}</strong>,</p>

            <div class="success">
                <strong>✓ Tu contraseña ha sido modificada exitosamente.</strong>
            </div>

            <p>Tu cuenta está ahora protegida con la nueva contraseña.</p>

            <div class="warning">
                <strong>⚠️ ¿No fuiste tú?</strong><br>
                Si no realizaste este cambio, tu cuenta podría estar comprometida.
                Contacta al soporte inmediatamente.
            </div>

            <p><strong>Detalles del cambio:</strong></p>
            <ul>
                <li>Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
                <li>Usuario: {username}</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

            part1 = MIMEText(text_body, 'plain')
            part2 = MIMEText(html_body, 'html')
            msg.attach(part1)
            msg.attach(part2)

            with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)

            logger.info(f"Email de confirmación enviado a {to_email}")
            return True

        except Exception as e:
            logger.error(f"Error enviando email de confirmación: {str(e)}")
            return False


# Import datetime for email timestamps
from datetime import datetime
