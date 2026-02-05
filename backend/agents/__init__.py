"""
Sistema Multiagente para Análisis Financiero

Este módulo contiene los agentes especializados que componen
el sistema multiagente:

- MarketAgent: Obtención y preprocesamiento de datos de mercado
- ModelAgent: Predicción mediante modelos de ML
- SentimentAgent: Análisis de sentimiento de noticias
- RecommendationAgent: Generación de recomendaciones
- AlertAgent: Evaluación y registro de alertas
"""
from .market_agent import MarketAgent, MarketData
from .model_agent import ModelAgent, PredictionResult
from .sentiment_agent import SentimentAgent, SentimentResult
from .recommendation_agent import RecommendationAgent, RecommendationResult
from .alert_agent import AlertAgent, AlertResult, NivelAlerta

__all__ = [
    # Agentes
    "MarketAgent",
    "ModelAgent",
    "SentimentAgent",
    "RecommendationAgent",
    "AlertAgent",
    # Estructuras de datos
    "MarketData",
    "PredictionResult",
    "SentimentResult",
    "RecommendationResult",
    "AlertResult",
    "NivelAlerta"
]
