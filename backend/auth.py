"""
Módulo de Autenticación y Seguridad

Este módulo implementa los mecanismos de seguridad del sistema:
- Hash seguro de contraseñas con bcrypt
- Generación y validación de tokens JWT
- Dependencias de autenticación para FastAPI

Cumple con las recomendaciones de OWASP para protección
de credenciales y autenticación segura.
"""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db, Usuario
from .schemas import TokenData

# Configuración del contexto de hash de contraseñas
# bcrypt es resistente a ataques de fuerza bruta
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema OAuth2 para extracción del token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña coincide con su hash.

    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Hash almacenado de la contraseña

    Returns:
        bool: True si coincide, False en caso contrario
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Genera un hash seguro de la contraseña.

    Utiliza bcrypt con salt aleatorio para proteger
    contra ataques de diccionario y rainbow tables.

    Args:
        password: Contraseña en texto plano

    Returns:
        str: Hash seguro de la contraseña
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT firmado.

    El token incluye la información del usuario y una fecha
    de expiración para limitar su validez temporal.

    Args:
        data: Diccionario con datos a incluir en el token
        expires_delta: Tiempo de expiración del token

    Returns:
        str: Token JWT codificado y firmado
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> Optional[TokenData]:
    """
    Decodifica y valida un token JWT.

    Args:
        token: Token JWT a validar

    Returns:
        TokenData: Datos extraídos del token o None si es inválido
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")

        if username is None:
            return None

        return TokenData(username=username, user_id=user_id)
    except JWTError:
        return None


def authenticate_user(db: Session, username: str, password: str) -> Optional[Usuario]:
    """
    Autentica un usuario verificando credenciales.

    Args:
        db: Sesión de base de datos
        username: Nombre de usuario
        password: Contraseña en texto plano

    Returns:
        Usuario: Objeto usuario si la autenticación es exitosa, None en caso contrario
    """
    user = db.query(Usuario).filter(Usuario.username == username).first()

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Dependencia de FastAPI para obtener el usuario actual.

    Valida el token JWT y recupera el usuario de la base de datos.
    Se utiliza como dependencia en endpoints protegidos.

    Args:
        token: Token JWT del encabezado Authorization
        db: Sesión de base de datos

    Returns:
        Usuario: Usuario autenticado

    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = decode_token(token)

    if token_data is None or token_data.username is None:
        raise credentials_exception

    user = db.query(Usuario).filter(Usuario.username == token_data.username).first()

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Dependencia para obtener usuario activo.

    Puede extenderse para verificar si el usuario está
    activo o tiene permisos específicos.

    Args:
        current_user: Usuario obtenido del token

    Returns:
        Usuario: Usuario activo verificado
    """
    # Aquí se pueden agregar validaciones adicionales
    # como verificar si el usuario está activo
    return current_user


def get_optional_current_user(
    authorization: Optional[str] = Header(None, alias="Authorization"),
    db: Session = Depends(get_db)
) -> Optional[Usuario]:
    """
    Dependencia opcional para endpoints que pueden
    funcionar con o sin autenticación.

    Usa Header manual en lugar de OAuth2PasswordBearer para evitar
    que FastAPI agregue requisito de autenticación al OpenAPI spec.

    Args:
        authorization: Header Authorization opcional
        db: Sesión de base de datos

    Returns:
        Usuario o None: Usuario si el token es válido, None en caso contrario
    """
    if authorization is None:
        return None

    # Extraer token del header "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None
    except ValueError:
        return None

    try:
        token_data = decode_token(token)
        if token_data is None or token_data.username is None:
            return None

        user = db.query(Usuario).filter(Usuario.username == token_data.username).first()
        return user
    except Exception:
        return None
