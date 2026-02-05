# Sistema Multiagente de Seguimiento y Alerta para Activos Financieros

Prototipo funcional de un sistema inteligente basado en agentes para el seguimiento y generación de alertas sobre activos financieros.

## Descripción

Este proyecto implementa un sistema multiagente que integra:

- **Obtención de datos de mercado** mediante yfinance
- **Predicción de precios** con modelos de aprendizaje automático
- **Análisis de sentimiento** (extensible)
- **Generación de recomendaciones** explicables
- **Sistema de alertas** con umbrales configurables

## Arquitectura

El sistema está compuesto por 5 agentes especializados:

1. **MarketAgent**: Descarga datos de mercado, calcula indicadores técnicos (MA, volatilidad) y genera señales de mercado.

2. **ModelAgent**: Implementa regresión lineal para predicción de precios y calcula métricas de evaluación (RMSE, MAPE, MAE).

3. **SentimentAgent**: Analiza sentimiento del mercado. Actualmente implementado como placeholder, preparado para integración con FinBERT/VADER.

4. **RecommendationAgent**: Integra señales de los agentes anteriores mediante scoring ponderado y genera recomendaciones textuales explicables.

5. **AlertAgent**: Evalúa umbrales de variación (3% warning, 7% critical) y persiste alertas en la base de datos.

## Tecnologías

- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **ML**: scikit-learn, pandas, numpy
- **Datos**: yfinance
- **Frontend**: Streamlit
- **Seguridad**: JWT, bcrypt

## Estructura del Proyecto

```
proyecto_final/
├── backend/
│   ├── __init__.py
│   ├── main.py              # Aplicación FastAPI
│   ├── config.py            # Configuración
│   ├── database.py          # Modelos SQLAlchemy
│   ├── schemas.py           # Schemas Pydantic
│   ├── auth.py              # Autenticación JWT
│   ├── routers/
│   │   ├── auth_router.py   # Endpoints de autenticación
│   │   ├── predict_router.py # Endpoints de predicción
│   │   └── alerts_router.py  # Endpoints de alertas
│   └── agents/
│       ├── market_agent.py
│       ├── model_agent.py
│       ├── sentiment_agent.py
│       ├── recommendation_agent.py
│       └── alert_agent.py
├── dashboard/
│   └── app.py               # Dashboard Streamlit
├── requirements.txt
├── .env.example
└── README.md
```

## Instalación

### 1. Clonar el repositorio

```bash
cd proyecto_final
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con valores apropiados
```

Variables importantes:
- `SECRET_KEY`: Clave secreta para JWT (generar una segura)
- `DATABASE_URL`: URL de la base de datos SQLite
- `ALERT_THRESHOLD_WARNING`: Umbral de alerta warning (default: 3%)
- `ALERT_THRESHOLD_CRITICAL`: Umbral de alerta crítica (default: 7%)

## Ejecución

### Iniciar el Backend

```bash
uvicorn backend.main:app --reload --port 8000
```

El API estará disponible en:
- API: http://localhost:8000
- Documentación Swagger: http://localhost:8000/docs
- Documentación ReDoc: http://localhost:8000/redoc

### Iniciar el Dashboard

En otra terminal:

```bash
streamlit run dashboard/app.py
```

El dashboard estará disponible en:
- http://localhost:8501

## Uso

### 1. Registro de Usuario

Desde el dashboard o via API:

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario", "email": "usuario@email.com", "password": "password123"}'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -d "username=usuario&password=password123"
```

### 3. Análisis de Activo

```bash
curl -X GET http://localhost:8000/predict/AAPL \
  -H "Authorization: Bearer <token>"
```

### 4. Ver Alertas

```bash
curl -X GET http://localhost:8000/alerts \
  -H "Authorization: Bearer <token>"
```

## API Endpoints

### Autenticación
- `POST /auth/register` - Registrar usuario
- `POST /auth/login` - Iniciar sesión
- `GET /auth/me` - Obtener usuario actual
- `POST /auth/refresh` - Refrescar token

### Predicción
- `GET /predict/{ticker}` - Análisis completo
- `GET /predict/{ticker}/market` - Solo datos de mercado
- `GET /predict/{ticker}/sentiment` - Solo sentimiento

### Alertas
- `GET /alerts` - Listar alertas
- `GET /alerts/stats` - Estadísticas
- `GET /alerts/{id}` - Detalle de alerta
- `PUT /alerts/{id}/read` - Marcar como leída
- `DELETE /alerts/{id}` - Eliminar alerta

### Estado
- `GET /` - Información de la API
- `GET /health` - Estado del sistema
- `GET /config` - Configuración pública

## Características de Seguridad

- Autenticación JWT con tokens firmados
- Hash de contraseñas con bcrypt
- Validación de datos con Pydantic
- CORS configurado para frontend
- Sin exposición de secretos en configuración pública

## Extensiones Futuras

1. **Sentimiento Real**: Integrar FinBERT para análisis de noticias financieras
2. **Modelos Avanzados**: Implementar LSTM, Prophet u otros modelos de series temporales
3. **Notificaciones**: Agregar WebSocket para alertas en tiempo real
4. **Múltiples Bases**: Soporte para PostgreSQL/MySQL en producción
5. **Cache Distribuido**: Redis para caché de datos de mercado

## Autor

Fabiana Cid

## Licencia

Proyecto académico - Especialización en Inteligencia Artificial, FIUBA
