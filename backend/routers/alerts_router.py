"""
Router de Alertas

Este módulo implementa los endpoints de gestión de alertas:
- GET /alerts: Listar alertas del usuario
- GET /alerts/{id}: Obtener alerta específica
- PUT /alerts/{id}/read: Marcar alerta como leída
- GET /alerts/stats: Estadísticas de alertas
- DELETE /alerts/{id}: Eliminar alerta

Todos los endpoints requieren autenticación JWT.
"""
import logging
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..database import get_db, Usuario, Alerta
from ..schemas import AlertResponse, AlertListResponse
from ..auth import get_current_active_user
from ..agents import AlertAgent

# Configuración de logging
logger = logging.getLogger(__name__)

# Crear router con prefijo y tags
router = APIRouter(
    prefix="/alerts",
    tags=["Alertas"]
)

# Instancia del agente de alertas
alert_agent = AlertAgent()


@router.get(
    "",
    response_model=AlertListResponse,
    summary="Listar alertas",
    description="Obtiene la lista de alertas del usuario autenticado."
)
async def list_alerts(
    solo_no_leidas: bool = Query(
        False,
        description="Filtrar solo alertas no leídas"
    ),
    limite: int = Query(
        50,
        ge=1,
        le=200,
        description="Número máximo de alertas a retornar"
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Número de alertas a saltar (paginación)"
    ),
    ticker: Optional[str] = Query(
        None,
        description="Filtrar por ticker específico"
    ),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Lista las alertas del usuario autenticado.

    Permite filtrar por estado de lectura y ticker,
    con soporte para paginación.

    Args:
        solo_no_leidas: Si True, solo retorna no leídas
        limite: Máximo de resultados
        offset: Desplazamiento para paginación
        ticker: Filtro por símbolo de activo
        db: Sesión de base de datos
        current_user: Usuario autenticado

    Returns:
        AlertListResponse: Lista de alertas con metadatos
    """
    try:
        # Construir query base
        query = db.query(Alerta).filter(Alerta.usuario_id == current_user.id)

        # Aplicar filtros
        if solo_no_leidas:
            query = query.filter(Alerta.leida == False)

        if ticker:
            query = query.filter(Alerta.ticker == ticker.upper())

        # Contar total antes de paginar
        total = query.count()

        # Aplicar paginación y ordenamiento
        alertas = query.order_by(
            Alerta.fecha_creacion.desc()
        ).offset(offset).limit(limite).all()

        # Convertir a respuesta (usando from_attributes para mapear directamente)
        alertas_response = [
            AlertResponse(
                id=a.id,
                usuario_id=a.usuario_id,
                ticker=a.ticker,
                tipo=a.tipo,
                mensaje=a.mensaje,
                variacion_pct=a.variacion_pct,
                precio_actual=a.precio_actual,
                precio_predicho=a.precio_predicho,
                leida=bool(a.leida),
                fecha_creacion=a.fecha_creacion
            )
            for a in alertas
        ]

        logger.info(
            f"Usuario {current_user.username} consultó alertas: "
            f"{len(alertas_response)} de {total} total"
        )

        return AlertListResponse(
            alertas=alertas_response,
            total=total,
            pagina_actual=offset // limite + 1 if limite > 0 else 1,
            total_paginas=(total + limite - 1) // limite if limite > 0 else 1
        )

    except Exception as e:
        logger.error(f"Error listando alertas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener alertas"
        )


@router.get(
    "/stats",
    summary="Estadísticas de alertas",
    description="Obtiene estadísticas de alertas del usuario."
)
async def get_alert_stats(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtiene estadísticas de alertas del usuario.

    Incluye:
    - Total de alertas
    - Alertas no leídas
    - Distribución por tipo

    Args:
        db: Sesión de base de datos
        current_user: Usuario autenticado

    Returns:
        Dict con estadísticas
    """
    stats = alert_agent.obtener_estadisticas(db, current_user.id)

    return {
        "usuario": current_user.username,
        "estadisticas": stats
    }


@router.get(
    "/{alerta_id}",
    summary="Obtener alerta específica",
    description="Obtiene los detalles de una alerta por su ID."
)
async def get_alert(
    alerta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtiene una alerta específica por ID.

    Solo retorna alertas pertenecientes al usuario autenticado.

    Args:
        alerta_id: ID de la alerta
        db: Sesión de base de datos
        current_user: Usuario autenticado

    Returns:
        Detalles de la alerta

    Raises:
        HTTPException 404: Si la alerta no existe
    """
    alerta = db.query(Alerta).filter(
        Alerta.id == alerta_id,
        Alerta.usuario_id == current_user.id
    ).first()

    if not alerta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerta no encontrada"
        )

    return {
        "id": alerta.id,
        "ticker": alerta.ticker,
        "tipo": alerta.tipo,
        "mensaje": alerta.mensaje,
        "variacion_pct": alerta.variacion_pct,
        "precio_actual": alerta.precio_actual,
        "precio_predicho": alerta.precio_predicho,
        "leida": alerta.leida,
        "fecha_creacion": alerta.fecha_creacion.isoformat()
    }


@router.put(
    "/{alerta_id}/read",
    summary="Marcar alerta como leída",
    description="Marca una alerta específica como leída."
)
async def mark_alert_as_read(
    alerta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Marca una alerta como leída.

    Args:
        alerta_id: ID de la alerta
        db: Sesión de base de datos
        current_user: Usuario autenticado

    Returns:
        Confirmación de la operación

    Raises:
        HTTPException 404: Si la alerta no existe
    """
    success = alert_agent.marcar_como_leida(db, alerta_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerta no encontrada"
        )

    return {
        "mensaje": "Alerta marcada como leída",
        "alerta_id": alerta_id
    }


@router.put(
    "/read-all",
    summary="Marcar todas como leídas",
    description="Marca todas las alertas del usuario como leídas."
)
async def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Marca todas las alertas del usuario como leídas.

    Args:
        db: Sesión de base de datos
        current_user: Usuario autenticado

    Returns:
        Número de alertas actualizadas
    """
    try:
        result = db.query(Alerta).filter(
            Alerta.usuario_id == current_user.id,
            Alerta.leida == False
        ).update({"leida": True})

        db.commit()

        logger.info(
            f"Usuario {current_user.username} marcó "
            f"{result} alertas como leídas"
        )

        return {
            "mensaje": "Alertas marcadas como leídas",
            "alertas_actualizadas": result
        }

    except Exception as e:
        db.rollback()
        logger.error(f"Error marcando alertas como leídas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar alertas"
        )


@router.delete(
    "/{alerta_id}",
    summary="Eliminar alerta",
    description="Elimina una alerta específica."
)
async def delete_alert(
    alerta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Elimina una alerta específica.

    Solo permite eliminar alertas pertenecientes al usuario.

    Args:
        alerta_id: ID de la alerta
        db: Sesión de base de datos
        current_user: Usuario autenticado

    Returns:
        Confirmación de eliminación

    Raises:
        HTTPException 404: Si la alerta no existe
    """
    alerta = db.query(Alerta).filter(
        Alerta.id == alerta_id,
        Alerta.usuario_id == current_user.id
    ).first()

    if not alerta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerta no encontrada"
        )

    try:
        db.delete(alerta)
        db.commit()

        logger.info(
            f"Usuario {current_user.username} eliminó alerta {alerta_id}"
        )

        return {
            "mensaje": "Alerta eliminada",
            "alerta_id": alerta_id
        }

    except Exception as e:
        db.rollback()
        logger.error(f"Error eliminando alerta: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar alerta"
        )


@router.delete(
    "",
    summary="Eliminar todas las alertas",
    description="Elimina todas las alertas del usuario."
)
async def delete_all_alerts(
    solo_leidas: bool = Query(
        True,
        description="Si True, solo elimina alertas leídas"
    ),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Elimina múltiples alertas del usuario.

    Por defecto solo elimina alertas ya leídas.

    Args:
        solo_leidas: Si True, solo elimina las leídas
        db: Sesión de base de datos
        current_user: Usuario autenticado

    Returns:
        Número de alertas eliminadas
    """
    try:
        query = db.query(Alerta).filter(
            Alerta.usuario_id == current_user.id
        )

        if solo_leidas:
            query = query.filter(Alerta.leida == True)

        count = query.delete()
        db.commit()

        logger.info(
            f"Usuario {current_user.username} eliminó {count} alertas"
        )

        return {
            "mensaje": "Alertas eliminadas",
            "alertas_eliminadas": count
        }

    except Exception as e:
        db.rollback()
        logger.error(f"Error eliminando alertas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar alertas"
        )
