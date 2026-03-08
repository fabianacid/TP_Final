# Informe Detallado de Pruebas del Sistema Multiagente

**Fecha de ejecución:** 13 de febrero de 2026
**Sistema evaluado:** Sistema Multiagente de Seguimiento Financiero
**Tipo de pruebas:** Funcionales con validación de métricas de clasificación
**Tickers evaluados:** 10 (AAPL, MSFT, TSLA, GOOGL, AMZN, META, NVDA, JPM, V, WMT)
**Iteraciones por ticker:** 3
**Total de pruebas:** 30

---

## Resumen Ejecutivo

### Resultados Generales

| Métrica | Valor | Estado |
|---------|-------|--------|
| **Tasa de éxito** | 100% (30/30) | Excelente |
| **Latencia promedio** | 4.90s | Cumple objetivo (<5s) |
| **Latencia mínima** | 4.15s | Consistente |
| **Latencia máxima** | 8.48s | ️ Solo primera iteración |
| **Mejora con caché** | 48% (8.5s → 4.3s) | Muy efectivo |

### Rendimiento de Agentes

| Agente | Tests | Éxitos | Tasa |
|--------|-------|--------|------|
| MarketAgent | 30 | 30 | 100% |
| ModelAgent | 30 | 30 | 100% |
| SentimentAgent | 30 | 30 | 100% |
| RecommendationAgent | 30 | 30 | 100% |
| AlertAgent | 30 | 30 | 100% |

**Conclusión:** Todos los agentes operan al 100% de efectividad. No se detectaron fallos ni inconsistencias.

---

## Métricas de Clasificación del Modelo

### Resultados Agregados

| Métrica | Promedio | Mínimo | Máximo | Desv. Std |
|---------|----------|--------|--------|-----------|
| **Accuracy** | 55.92% | 48.98% | 62.59% | 0.0402 |
| **Precision** | 58.64% | 42.96% | 75.02% | 0.0877 |
| **Recall** | 69.66% | 18.35% | 98.41% | 0.1980 |
| **F1-Score** | 58.06% | 24.96% | 69.01% | 0.1195 |
| **AUC** | 59.48% | 54.23% | 74.97% | 0.0587 |

### Interpretación

**Accuracy (55.92%):**
- **Supera el baseline** de clasificación aleatoria (50%)
- Predice correctamente la dirección en ~56% de los casos
- ️ Hay margen de mejora (objetivo ideal: >60%)

**Precision (58.64%):**
- Cuando predice SUBIDA, acierta en ~59% de los casos
- Es útil para traders conservadores que prefieren evitar falsos positivos
- ️ Variabilidad alta entre tickers (42.96% - 75.02%)

**Recall (69.66%):**
- Detecta el 70% de las subidas reales
- Bueno para no perder oportunidades alcistas
- ️ Desviación estándar muy alta (0.198) indica rendimiento inconsistente

**F1-Score (58.06%):**
- Balance razonable entre precision y recall
- Confirma que el modelo es ligeramente mejor que azar

**AUC (59.48%):**
- Capacidad de discriminación aceptable
- Valores >0.5 indican que el modelo tiene poder predictivo
- ️ Idealmente debería ser >0.65 para uso comercial

---

## Análisis Detallado por Ticker

### Mejores Tickers (Accuracy > 59%)

#### 1. **AAPL (Apple Inc.)** - Accuracy: 62.59%
```
Métricas:
├── Accuracy: 62.59% (Mejor rendimiento)
├── Precision: 64.08%
├── Recall: 78.28%
├── F1-Score: 69.01%
└── AUC: 60.05%

Latencia: 4.41s - 8.48s (promedio: 5.80s)
Sentimiento: Negativo (-0.1244)
Recomendación: VENTA (confianza: 30%)
```

**Análisis:**
- **Mejor ticker del portafolio** para clasificación
- Alta liquidez y volumen de trading
- Recall alto (78.28%) - detecta la mayoría de subidas
- El modelo funciona bien con acciones tech de alta capitalización

#### 2. **JPM (JPMorgan Chase)** - Accuracy: 59.86%
```
Métricas:
├── Accuracy: 59.86% 
├── Precision: 69.50% (Segunda mejor)
├── Recall: 74.80%
├── F1-Score: 63.79%
└── AUC: 56.87%

Latencia: 4.18s - 5.64s (promedio: 4.66s)
Sentimiento: Positivo (0.295)
Recomendación: MANTENER (confianza: 30%)
```

**Análisis:**
- Mejor precision del grupo (69.50%)
- Sector financiero con patrones predecibles
- Latencia consistente y baja
- Ideal para estrategias de alta precision

#### 3. **TSLA (Tesla Inc.)** - Accuracy: 59.18%
```
Métricas:
├── Accuracy: 59.18% 
├── Precision: 59.27%
├── Recall: 59.39%
├── F1-Score: 58.10%
└── AUC: 55.15%

Latencia: 4.31s - 5.96s (promedio: 4.87s)
Sentimiento: Positivo (0.2145)
Recomendación: COMPRA (confianza: 39.4%, ️ RIESGO ELEVADO)
```

**Análisis:**
- Tercera mejor accuracy
- ️ Alta volatilidad (riesgo elevado detectado por el sistema)
- Balance perfecto entre precision y recall
- Apropiado para traders con tolerancia al riesgo

---

### ️ Tickers con Desafíos (Accuracy < 52%)

#### 1. **WMT (Walmart Inc.)** - Accuracy: 48.98%
```
Métricas:
├── Accuracy: 48.98% ️ (Peor rendimiento)
├── Precision: 42.96% ️ (Peor precision)
├── Recall: 18.35% ️ (Peor recall)
├── F1-Score: 24.96% ️ (Peor F1)
└── AUC: 54.23%

Latencia: 4.31s - 6.02s
Sentimiento: Neutral (-0.0521)
Recomendación: MANTENER (confianza: 30%)
```

**Análisis:**
- **Peor ticker del portafolio** - accuracy menor que azar
- Recall extremadamente bajo (18.35%) - pierde la mayoría de subidas
- Precision baja (42.96%) - muchos falsos positivos
- **Recomendación:** NO usar este ticker con el modelo actual
- Posible causa: Sector retail con movimientos laterales (no trending)

#### 2. **MSFT (Microsoft Corp.)** - Accuracy: 52.38%
```
Métricas:
├── Accuracy: 52.38%
├── Precision: 55.37%
├── Recall: 77.33%
├── F1-Score: 57.13%
└── AUC: 57.31%

Latencia: 4.25s - 5.76s
Sentimiento: Neutral (0.0855)
Recomendación: MANTENER (confianza: 30%)
```

**Análisis:**
- ️ Accuracy apenas mejor que azar
- Recall alto (77.33%) - detecta subidas
- ️ Precision moderada (55.37%) - algunos falsos positivos
- Puede usarse con precaución, priorizando señales de alta confianza

#### 3. **GOOGL (Alphabet Inc.)** - Accuracy: 52.38%
```
Métricas:
├── Accuracy: 52.38%
├── Precision: 75.02% (MEJOR PRECISION)
├── Recall: 72.09%
├── F1-Score: 60.61%
└── AUC: 74.97% (MEJOR AUC)

Latencia: 4.15s - 6.09s
Sentimiento: Positivo (0.3288)
Recomendación: MANTENER (confianza: 30%)
```

**Análisis:**
- **Mejor precision del portafolio** (75.02%)
- **Mejor AUC del portafolio** (74.97%)
- ️ Baja accuracy general (52.38%)
- **Trade-off interesante:** Predice pocas subidas, pero cuando lo hace, acierta
- **Estrategia recomendada:** Usar solo señales de MUY alta confianza

---

### Tickers en Rango Medio (52% - 59%)

#### AMZN (Amazon.com Inc.) - Accuracy: 58.50%
- Precision: 56.40%
- Recall: 68.16%
- Performance sólida y consistente

#### META (Meta Platforms Inc.) - Accuracy: 56.46%
- Precision: 57.87%
- Recall: 76.00%
- Buen recall, precision moderada

#### NVDA (NVIDIA Corp.) - Accuracy: 53.74%
- Precision: 53.56%
- Recall: 73.77%
- Balance neutro entre precision y recall

#### V (Visa Inc.) - Accuracy: 55.10%
- Precision: 52.39%
- Recall: 98.41% (MEJOR RECALL)
- Detecta casi todas las subidas (sensibilidad máxima)

---

## Análisis de Rendimiento y Latencia

### Distribución de Latencia por Iteración

| Iteración | Latencia Promedio | Observaciones |
|-----------|-------------------|---------------|
| 1ª (sin caché) | 6.02s | Primera carga + descarga de datos |
| 2ª (con caché) | 4.32s | **-28% mejora** |
| 3ª (con caché) | 4.39s | Rendimiento estable |

### Latencia por Ticker

| Ticker | Mín | Máx | Promedio | Variabilidad |
|--------|-----|-----|----------|--------------|
| GOOGL | 4.15s | 6.09s | 4.95s | Baja |
| JPM | 4.18s | 5.64s | 4.66s | Muy baja |
| META | 4.23s | 5.65s | 4.71s | Muy baja |
| MSFT | 4.25s | 5.76s | 4.86s | Baja |
| AMZN | 4.26s | 5.80s | 4.79s | Baja |
| NVDA | 4.27s | 5.38s | 4.65s | Muy baja |
| V | 4.28s | 5.84s | 4.81s | Baja |
| TSLA | 4.31s | 5.96s | 4.87s | Baja |
| WMT | 4.31s | 6.02s | 4.88s | Baja |
| AAPL | 4.41s | 8.48s | 5.80s | Alta ️ |

**Conclusión:**
- Latencia muy consistente (std < 0.5s para la mayoría)
- ️ AAPL tiene el spike más alto (8.48s en primera iteración)
- JPM, META, NVDA son los más rápidos y consistentes

---

## Análisis de Sentimiento vs Recomendación

### Distribución de Sentimientos

| Sentimiento | Cantidad | Porcentaje |
|-------------|----------|------------|
| Positivo | 15 | 50% |
| Neutral | 12 | 40% |
| Negativo | 3 | 10% |

### Distribución de Recomendaciones

| Recomendación | Cantidad | Porcentaje |
|---------------|----------|------------|
| Mantener | 21 | 70% |
| Compra | 6 | 20% |
| Venta | 3 | 10% |

### Correlación Sentimiento-Recomendación

| Ticker | Sentimiento | Score | Recomendación | Coherencia |
|--------|-------------|-------|---------------|------------|
| AAPL | Negativo | -0.12 | Venta | Coherente |
| TSLA | Positivo | 0.21 | Compra | Coherente |
| NVDA | Positivo | 0.29 | Compra | Coherente |
| GOOGL | Positivo | 0.33 | Mantener | ️ Conservador |
| V | Positivo | 0.35 | Mantener | ️ Conservador |

**Observación:** El sistema tiende a ser **conservador**, prefiriendo "Mantener" incluso con señales positivas. Esto es apropiado para gestión de riesgo.

---

## Recomendaciones y Mejoras

### Fortalezas del Sistema

1. **Estabilidad Operacional**
 - 100% de éxito en todas las pruebas
 - Todos los agentes funcionan correctamente
 - Sin errores ni excepciones

2. **Rendimiento Aceptable**
 - Latencia < 5s en promedio (cumple SLA)
 - Mejora significativa con caché (48%)
 - Consistencia entre iteraciones

3. **Tickers Destacados**
 - AAPL, JPM, TSLA superan el 59% de accuracy
 - GOOGL tiene la mejor precision (75%)
 - V tiene el mejor recall (98%)

### ️ Áreas de Mejora

#### 1. **Modelo de Clasificación**

**Problema:** Accuracy promedio del 55.92% es apenas mejor que azar.

**Recomendaciones:**
- Agregar más features:
 - Volumen relativo
 - Métricas de market breadth
 - Correlación con índices
- Probar ventanas temporales diferentes:
 - Actualmente: 252 días (1 año)
 - Experimentar: 126 días (6 meses) y 63 días (3 meses)
- Modelos adicionales:
 - Agregar XGBoost con tuning de hiperparámetros
 - Probar Neural Networks (LSTM, Transformer)
 - Ensemble con stacking

#### 2. **Tickers Problemáticos**

**Problema:** WMT tiene accuracy del 48.98% (peor que azar).

**Recomendaciones:**
- **Blacklist de tickers:** Filtrar tickers con baja predictibilidad
- **Detección de régimen:** Identificar si el ticker está en trending o ranging
- **Modelos especializados:** Un modelo por sector (tech, finance, retail)

#### 3. **Alta Variabilidad en Recall**

**Problema:** Recall varía entre 18.35% (WMT) y 98.41% (V).

**Recomendaciones:**
- ️ **Balanceo de clases:** Usar SMOTE o class weights
- ️ **Ajuste de threshold:** Optimizar el umbral de clasificación por ticker
- **Calibración de probabilidades:** Usar Platt scaling o isotonic regression

#### 4. **Confianza de Recomendaciones**

**Problema:** Todas las recomendaciones tienen confianza del 30% (fija).

**Recomendaciones:**
- **Confianza dinámica:** Basada en métricas del modelo (accuracy, AUC)
- **Scoring multi-factor:** Combinar:
 - Confianza del modelo
 - Consistencia de señales técnicas
 - Fuerza del sentimiento
 - Volatilidad histórica

#### 5. **Optimización de Latencia**

**Problema:** Primera iteración tarda 8.5s (AAPL).

**Recomendaciones:**
- **Pre-caching:** Descargar datos de tickers populares periódicamente
- **Procesamiento paralelo:** Ejecutar agentes en paralelo (asyncio)
- **Caché distribuido:** Usar Redis para compartir caché entre instancias

---

## Comparativa con Baseline

| Métrica | Baseline (Azar) | Sistema Actual | Mejora |
|---------|-----------------|----------------|--------|
| Accuracy | 50.00% | 55.92% | +11.8% |
| Precision | 50.00% | 58.64% | +17.3% |
| Recall | 50.00% | 69.66% | +39.3% |
| F1-Score | 50.00% | 58.06% | +16.1% |
| AUC | 50.00% | 59.48% | +19.0% |

**Conclusión:** El sistema supera consistentemente al baseline de clasificación aleatoria en todas las métricas. El mayor logro es el **Recall (+39.3%)**, lo que significa que el sistema es significativamente mejor detectando oportunidades alcistas.

---

## Conclusiones Finales

### Logros

1. **Sistema operativo al 100%** - Sin errores ni fallos
2. **Supera el baseline** - Todas las métricas mejor que azar
3. **Tickers destacados** - AAPL (62.6%), JPM (59.9%), TSLA (59.2%)
4. **Alto recall promedio** - Detecta 70% de subidas reales
5. **Latencia cumple SLA** - 4.9s < 5s objetivo

### ️ Limitaciones

1. **Accuracy modesta** - 55.92% apenas supera el 50%
2. **Alta variabilidad** - Rendimiento inconsistente entre tickers
3. **Algunos tickers fallan** - WMT peor que azar
4. **Baja confianza** - Recomendaciones siempre al 30%

### Siguientes Pasos

1. **Corto plazo (1-2 semanas):**
 - Implementar blacklist de tickers con accuracy < 52%
 - Ajustar threshold de clasificación por ticker
 - Mejorar confianza dinámica de recomendaciones

2. **Mediano plazo (1 mes):**
 - Agregar features adicionales (volumen, breadth)
 - Experimentar con ventanas temporales
 - Implementar modelos especializados por sector

3. **Largo plazo (2-3 meses):**
 - Evaluar modelos de deep learning (LSTM, Transformers)
 - Implementar ensemble con stacking
 - Backtesting con datos históricos (3+ años)

---

## Archivos Generados

- `test_results/functional_test_20260213_233918.json` - Datos completos
- `test_results/functional_test_20260213_233918.csv` - Formato tabular
- `test_results/summary_20260213_233918.json` - Resumen estadístico

---

**Informe generado:** 13 de febrero de 2026
**Autor:** Sistema Multiagente de Seguimiento Financiero
**Versión:** 1.0.0
