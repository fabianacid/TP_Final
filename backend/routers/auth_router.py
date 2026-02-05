"""
Router de Autenticación

Este módulo implementa los endpoints de autenticación:
- POST /auth/register: Registro de nuevos usuarios
- POST /auth/login: Inicio de sesión (obtener token JWT)
- GET /auth/me: Obtener información del usuario actual
- POST /auth/forgot-password: Solicitar recuperación de contraseña
- POST /auth/reset-password: Resetear contraseña con token
- PUT /auth/change-password: Cambiar contraseña (autenticado)

Cumple con las recomendaciones de OWASP para autenticación segura.
"""
import logging
import secrets
from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db, Usuario, PasswordResetToken
from ..schemas import (
    UserCreate, UserResponse, Token,
    ForgotPasswordRequest, ResetPasswordRequest, ChangePasswordRequest,
    MessageResponse
)
from ..auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    verify_password
)
from ..config import settings
from ..email_service import EmailService

# Configuración de logging
logger = logging.getLogger(__name__)

# Crear router con prefijo y tags
router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Crea una nueva cuenta de usuario con credenciales seguras."
)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Registra un nuevo usuario en el sistema.

    El proceso incluye:
    1. Validación de datos de entrada
    2. Verificación de username único
    3. Hash seguro de contraseña con bcrypt
    4. Persistencia en base de datos

    Args:
        user_data: Datos del nuevo usuario
        db: Sesión de base de datos

    Returns:
        UserResponse: Datos del usuario creado

    Raises:
        HTTPException 400: Si el username ya existe
    """
    # Verificar si el usuario ya existe
    existing_user = db.query(Usuario).filter(
        Usuario.username == user_data.username
    ).first()

    if existing_user:
        logger.warning(f"Intento de registro con username existente: {user_data.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado"
        )

    # Verificar email único si se proporciona
    if user_data.email:
        existing_email = db.query(Usuario).filter(
            Usuario.email == user_data.email
        ).first()

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )

    # Crear hash de contraseña
    hashed_password = get_password_hash(user_data.password)

    # Crear usuario
    new_user = Usuario(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"Usuario registrado exitosamente: {user_data.username}")

        return UserResponse(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            rol=new_user.rol,
            fecha_creacion=new_user.fecha_creacion
        )

    except Exception as e:
        db.rollback()
        logger.error(f"Error al registrar usuario: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al crear usuario"
        )


@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
    description="Autentica usuario y retorna token JWT."
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Autentica un usuario y genera token de acceso.

    El proceso incluye:
    1. Verificación de credenciales
    2. Generación de token JWT firmado
    3. Configuración de tiempo de expiración

    Args:
        form_data: Credenciales de usuario (OAuth2 form)
        db: Sesión de base de datos

    Returns:
        Token: Token JWT de acceso

    Raises:
        HTTPException 401: Si las credenciales son inválidas
    """
    # Autenticar usuario
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        logger.warning(f"Intento de login fallido para: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Crear token de acceso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "user_id": user.id
        },
        expires_delta=access_token_expires
    )

    logger.info(f"Login exitoso para usuario: {user.username}")

    return Token(
        access_token=access_token,
        token_type="bearer"
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Obtener usuario actual",
    description="Retorna información del usuario autenticado."
)
async def get_current_user_info(
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtiene información del usuario autenticado.

    Endpoint protegido que requiere token JWT válido.

    Args:
        current_user: Usuario obtenido del token

    Returns:
        UserResponse: Información del usuario
    """
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        rol=current_user.rol,
        fecha_creacion=current_user.fecha_creacion
    )


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refrescar token",
    description="Genera un nuevo token JWT para el usuario autenticado."
)
async def refresh_token(
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Refresca el token de acceso del usuario.

    Permite obtener un nuevo token sin necesidad de
    enviar credenciales nuevamente.

    Args:
        current_user: Usuario obtenido del token actual

    Returns:
        Token: Nuevo token JWT
    """
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": current_user.username,
            "user_id": current_user.id
        },
        expires_delta=access_token_expires
    )

    logger.info(f"Token refrescado para usuario: {current_user.username}")

    return Token(
        access_token=access_token,
        token_type="bearer"
    )


@router.post(
    "/forgot-password",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Solicitar recuperación de contraseña",
    description="Envía un email con link para resetear contraseña."
)
async def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Solicita recuperación de contraseña mediante email.

    Proceso:
    1. Verifica que el email esté registrado
    2. Genera token único y seguro
    3. Guarda token en BD con expiración
    4. Envía email con link de reseteo

    Args:
        request: Email del usuario
        db: Sesión de base de datos

    Returns:
        MessageResponse: Confirmación (siempre éxito por seguridad)
    """
    # Buscar usuario por email
    user = db.query(Usuario).filter(Usuario.email == request.email).first()

    # IMPORTANTE: Por seguridad, siempre devolver éxito aunque el email no exista
    # Esto evita que atacantes enumeren emails registrados
    if not user:
        logger.warning(f"Solicitud de reseteo para email no registrado: {request.email}")
        return MessageResponse(
            message="Si el email está registrado, recibirás instrucciones para resetear tu contraseña.",
            detail="Por seguridad, no indicamos si el email existe o no."
        )

    try:
        # Generar token seguro (64 caracteres hexadecimales)
        reset_token = secrets.token_urlsafe(48)

        # Calcular fecha de expiración
        expiration = datetime.utcnow() + timedelta(hours=settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS)

        # Invalidar tokens anteriores del usuario
        db.query(PasswordResetToken).filter(
            PasswordResetToken.usuario_id == user.id,
            PasswordResetToken.usado == 0
        ).update({"usado": 1})

        # Crear nuevo token
        new_token = PasswordResetToken(
            usuario_id=user.id,
            token=reset_token,
            expiracion=expiration
        )

        db.add(new_token)
        db.commit()

        # Enviar email
        email_sent = EmailService.send_password_reset_email(
            to_email=request.email,
            username=user.username,
            reset_token=reset_token
        )

        if email_sent:
            logger.info(f"Token de reseteo creado y email enviado para: {user.username}")
        else:
            logger.warning(f"Token de reseteo creado pero email no enviado para: {user.username}")

        return MessageResponse(
            message="Si el email está registrado, recibirás instrucciones para resetear tu contraseña.",
            detail="Revisa tu bandeja de entrada y spam. El link expira en 1 hora."
        )

    except Exception as e:
        db.rollback()
        logger.error(f"Error en forgot_password: {str(e)}")
        # Por seguridad, no revelar el error específico
        return MessageResponse(
            message="Si el email está registrado, recibirás instrucciones para resetear tu contraseña."
        )


@router.post(
    "/reset-password",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Resetear contraseña con token",
    description="Resetea la contraseña usando el token recibido por email."
)
async def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Resetea la contraseña usando token de recuperación.

    Proceso:
    1. Valida token (existencia, expiración, uso previo)
    2. Actualiza contraseña del usuario
    3. Marca token como usado
    4. Envía email de confirmación

    Args:
        request: Token y nueva contraseña
        db: Sesión de base de datos

    Returns:
        MessageResponse: Confirmación de cambio

    Raises:
        HTTPException 400: Si el token es inválido o expirado
    """
    # Buscar token
    token_record = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == request.token
    ).first()

    # Validar token existe
    if not token_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido o expirado"
        )

    # Validar token no usado
    if token_record.usado == 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este token ya fue utilizado"
        )

    # Validar token no expirado
    if datetime.utcnow() > token_record.expiracion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token expirado. Solicita uno nuevo."
        )

    try:
        # Obtener usuario
        user = db.query(Usuario).filter(Usuario.id == token_record.usuario_id).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        # Actualizar contraseña
        user.password_hash = get_password_hash(request.new_password)

        # Marcar token como usado
        token_record.usado = 1

        db.commit()

        logger.info(f"Contraseña reseteada exitosamente para: {user.username}")

        # Enviar email de confirmación
        EmailService.send_password_changed_confirmation(
            to_email=user.email,
            username=user.username
        )

        return MessageResponse(
            message="Contraseña actualizada exitosamente",
            detail="Ya puedes iniciar sesión con tu nueva contraseña"
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error en reset_password: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar contraseña"
        )


@router.put(
    "/change-password",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Cambiar contraseña (autenticado)",
    description="Permite al usuario cambiar su contraseña estando autenticado."
)
async def change_password(
    request: ChangePasswordRequest,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Cambia la contraseña del usuario autenticado.

    Requiere que el usuario proporcione su contraseña actual
    por seguridad.

    Args:
        request: Contraseña actual y nueva
        current_user: Usuario autenticado
        db: Sesión de base de datos

    Returns:
        MessageResponse: Confirmación de cambio

    Raises:
        HTTPException 401: Si la contraseña actual es incorrecta
    """
    # Verificar contraseña actual
    if not verify_password(request.current_password, current_user.password_hash):
        logger.warning(f"Intento de cambio de contraseña fallido para: {current_user.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña actual incorrecta"
        )

    try:
        # Actualizar contraseña
        current_user.password_hash = get_password_hash(request.new_password)
        db.commit()

        logger.info(f"Contraseña cambiada exitosamente para: {current_user.username}")

        # Enviar email de confirmación
        if current_user.email:
            EmailService.send_password_changed_confirmation(
                to_email=current_user.email,
                username=current_user.username
            )

        return MessageResponse(
            message="Contraseña actualizada exitosamente",
            detail="Tu contraseña ha sido cambiada de forma segura"
        )

    except Exception as e:
        db.rollback()
        logger.error(f"Error en change_password: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar contraseña"
        )
