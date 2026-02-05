"""
Router de Autenticación

Este módulo implementa los endpoints de autenticación:
- POST /auth/register: Registro de nuevos usuarios
- POST /auth/login: Inicio de sesión (obtener token JWT)
- GET /auth/me: Obtener información del usuario actual

Cumple con las recomendaciones de OWASP para autenticación segura.
"""
import logging
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db, Usuario
from ..schemas import UserCreate, UserResponse, Token
from ..auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_active_user
)
from ..config import settings

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
