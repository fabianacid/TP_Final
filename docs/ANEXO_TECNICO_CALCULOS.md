# ANEXO TÉCNICO: CÁLCULOS Y FÓRMULAS DEL SISTEMA

**Sistema Multiagente de Seguimiento Financiero**
**Análisis Matemático y Metodológico Completo**

---

## ÍNDICE

1. [Agente de Mercado (MarketAgent)](#1-agente-de-mercado-marketagent)
2. [Agente de Modelo Predictivo (ModelAgent)](#2-agente-de-modelo-predictivo-modelagent)
3. [Agente de Sentimiento (SentimentAgent)](#3-agente-de-sentimiento-sentimentagent)
4. [Agente de Recomendación (RecommendationAgent)](#4-agente-de-recomendación-recommendationagent)
5. [Agente de Alertas (AlertAgent)](#5-agente-de-alertas-alertagent)
6. [Flujo de Integración](#6-flujo-de-integración)

---

## 1. AGENTE DE MERCADO (MarketAgent)

### 1.1 Obtención de Datos

**Fuente**: Yahoo Finance API (yfinance)

**Datos descargados**:
```python
periodo = 6 meses
intervalo = 1 día
datos = {precio_apertura, precio_cierre, precio_máximo, precio_mínimo, volumen}
```

### 1.2 Indicadores Técnicos

#### 1.2.1 RSI (Relative Strength Index)

**Concepto**: Mide la velocidad y magnitud de cambios de precio para identificar condiciones de sobrecompra/sobreventa.

**Fórmula**:
```
RSI = 100 - (100 / (1 + RS))

donde:
RS = Ganancia Promedio / Pérdida Promedio

Ganancia Promedio = Σ(ganancias en período) / n
Pérdida Promedio = Σ(pérdidas en período) / n

período = 14 días (estándar)
```

**Cálculo paso a paso**:
1. Calcular cambios diarios: Δ = Precio_cierre(día_i) - Precio_cierre(día_i-1)
2. Separar ganancias (Δ > 0) y pérdidas (Δ < 0)
3. Calcular promedio móvil exponencial (EMA) de 14 días para ganancias y pérdidas
4. RS = EMA(ganancias) / EMA(pérdidas)
5. RSI = 100 - (100 / (1 + RS))

**Interpretación**:
- RSI > 70: Sobrecompra (posible corrección a la baja)
- RSI < 30: Sobreventa (posible rebote al alza)
- RSI ≈ 50: Neutral

**Ejemplo práctico**:
```
Ganancias últimos 14 días: [0.5, 1.2, 0.8, 0, 0, 0.3, 1.1, 0.9, 0.6, 0, 0.4, 0.7, 0.5, 0.8]
Pérdidas últimos 14 días:  [0, 0, 0, 0.4, 0.6, 0, 0, 0, 0, 0.5, 0, 0, 0, 0]

Ganancia_promedio = (0.5+1.2+0.8+0.3+1.1+0.9+0.6+0.4+0.7+0.5+0.8) / 14 = 0.56
Pérdida_promedio = (0.4+0.6+0.5) / 14 = 0.11

RS = 0.56 / 0.11 = 5.09
RSI = 100 - (100 / (1 + 5.09)) = 100 - 16.4 = 83.6

Resultado: RSI = 83.6 → SOBRECOMPRA
```

#### 1.2.2 MACD (Moving Average Convergence Divergence)

**Concepto**: Indicador de momentum que muestra la relación entre dos medias móviles exponenciales.

**Fórmulas**:
```
MACD_line = EMA(12) - EMA(26)
Signal_line = EMA(9) del MACD_line
MACD_histogram = MACD_line - Signal_line

donde:
EMA(n) = Media Móvil Exponencial de n períodos
```

**Cálculo de EMA**:
```
EMA_hoy = (Precio_hoy × multiplicador) + (EMA_ayer × (1 - multiplicador))

multiplicador = 2 / (n + 1)

Para EMA(12): multiplicador = 2 / 13 = 0.1538
Para EMA(26): multiplicador = 2 / 27 = 0.0741
```

**Señales de trading**:
- MACD_line cruza por encima de Signal_line → Señal ALCISTA
- MACD_line cruza por debajo de Signal_line → Señal BAJISTA
- MACD_histogram > 0 → Momentum positivo
- MACD_histogram < 0 → Momentum negativo

**Ejemplo**:
```
EMA(12) = $150.50
EMA(26) = $148.20
MACD_line = 150.50 - 148.20 = 2.30

EMA(9) del MACD = 1.80
Signal_line = 1.80

MACD_histogram = 2.30 - 1.80 = 0.50

Interpretación: MACD positivo y creciente → MOMENTUM ALCISTA
```

#### 1.2.3 Bandas de Bollinger

**Concepto**: Miden la volatilidad y niveles de sobrecompra/sobreventa basándose en desviación estándar.

**Fórmulas**:
```
Banda_Media = SMA(20)
Banda_Superior = SMA(20) + (2 × σ)
Banda_Inferior = SMA(20) - (2 × σ)

donde:
SMA(20) = Media Móvil Simple de 20 períodos
σ = Desviación Estándar de 20 períodos
```

**Cálculo de SMA**:
```
SMA(20) = (P₁ + P₂ + ... + P₂₀) / 20
```

**Cálculo de Desviación Estándar**:
```
σ = √[Σ(Pᵢ - SMA)² / n]

donde n = 20
```

**Interpretación**:
- Precio cerca de Banda_Superior → Sobrecompra
- Precio cerca de Banda_Inferior → Sobreventa
- Bandas estrechas → Baja volatilidad (posible ruptura próxima)
- Bandas amplias → Alta volatilidad

**Ejemplo**:
```
Precios últimos 20 días: [145, 147, 148, 146, 149, 151, 150, 152, 153, 151,
                          154, 155, 153, 156, 157, 155, 158, 159, 157, 160]

SMA(20) = Σ precios / 20 = 3020 / 20 = 151

Cálculo de σ:
Varianza = [(145-151)² + (147-151)² + ... + (160-151)²] / 20
         = [36 + 16 + 9 + 25 + 4 + 0 + 1 + 1 + 4 + 0 + 9 + 16 + 4 + 25 + 36 + 16 + 49 + 64 + 36 + 81] / 20
         = 432 / 20 = 21.6
σ = √21.6 = 4.65

Banda_Superior = 151 + (2 × 4.65) = 151 + 9.3 = 160.3
Banda_Inferior = 151 - (2 × 4.65) = 151 - 9.3 = 141.7

Precio_actual = 160
Posición = (160 - 141.7) / (160.3 - 141.7) = 18.3 / 18.6 = 0.98

Interpretación: Precio al 98% del rango → SOBRECOMPRA
```

#### 1.2.4 ATR (Average True Range)

**Concepto**: Mide la volatilidad del mercado calculando el rango promedio de movimiento del precio.

**Fórmula**:
```
True_Range = max(
    Alto - Bajo,
    |Alto - Cierre_anterior|,
    |Bajo - Cierre_anterior|
)

ATR = Media móvil del True_Range (14 períodos)
```

**Cálculo paso a paso**:
```
Para cada día i:
TR_i = max(
    Alto_i - Bajo_i,
    |Alto_i - Cierre_(i-1)|,
    |Bajo_i - Cierre_(i-1)|
)

ATR = (TR₁ + TR₂ + ... + TR₁₄) / 14
```

**Ejemplo**:
```
Día actual:
Alto = $152.50
Bajo = $148.20
Cierre_anterior = $150.00

TR = max(
    152.50 - 148.20 = 4.30,
    |152.50 - 150.00| = 2.50,
    |148.20 - 150.00| = 1.80
) = 4.30

Si el ATR de 14 días = $3.75
→ Volatilidad moderada-alta
```

#### 1.2.5 OBV (On-Balance Volume)

**Concepto**: Indicador de momentum que relaciona volumen con cambio de precio.

**Fórmula**:
```
Si Cierre_hoy > Cierre_ayer:
    OBV = OBV_ayer + Volumen_hoy

Si Cierre_hoy < Cierre_ayer:
    OBV = OBV_ayer - Volumen_hoy

Si Cierre_hoy = Cierre_ayer:
    OBV = OBV_ayer
```

**Interpretación**:
- OBV creciente + precio creciente → Tendencia alcista confirmada
- OBV decreciente + precio decreciente → Tendencia bajista confirmada
- Divergencia (OBV ↑ pero precio ↓) → Posible reversión alcista

#### 1.2.6 Ratio de Volumen

**Fórmula**:
```
Ratio_Volumen = Volumen_actual / Volumen_promedio(20_días)

Volumen_promedio = Σ(Volumen_i) / 20
```

**Interpretación**:
- Ratio > 2.0: Volumen muy alto (posible confirmación de tendencia)
- Ratio 1.0-2.0: Volumen normal-alto
- Ratio < 0.5: Volumen bajo (falta de convicción)

#### 1.2.7 ADX (Average Directional Index)

**Concepto**: Mide la fuerza de la tendencia (no su dirección).

**Fórmulas**:
```
+DM = Alto_hoy - Alto_ayer (si > 0, sino 0)
-DM = Bajo_ayer - Bajo_hoy (si > 0, sino 0)

+DI = (EMA(+DM, 14) / ATR) × 100
-DI = (EMA(-DM, 14) / ATR) × 100

DX = (|+DI - -DI| / |+DI + -DI|) × 100
ADX = EMA(DX, 14)
```

**Interpretación**:
- ADX > 25: Tendencia fuerte
- ADX < 20: Tendencia débil o mercado lateral
- ADX > 50: Tendencia muy fuerte

#### 1.2.8 MFI (Money Flow Index)

**Concepto**: RSI ponderado por volumen, mide presión compradora/vendedora.

**Fórmulas**:
```
Precio_típico = (Alto + Bajo + Cierre) / 3
Flujo_monetario = Precio_típico × Volumen

Flujo_positivo = Σ(Flujo_monetario cuando Precio_típico ↑)
Flujo_negativo = Σ(Flujo_monetario cuando Precio_típico ↓)

Ratio_flujo = Flujo_positivo / Flujo_negativo

MFI = 100 - (100 / (1 + Ratio_flujo))
```

**Interpretación**:
- MFI > 80: Sobrecompra
- MFI < 20: Sobreventa
- Similar al RSI pero considera volumen

### 1.3 Detección de Régimen de Mercado

**Algoritmo**:
```python
if ADX > 25:
    if +DI > -DI:
        régimen = "tendencia_alcista"
    else:
        régimen = "tendencia_bajista"
elif ATR > percentil_75(ATR_histórico):
    régimen = "alta_volatilidad"
elif ATR < percentil_25(ATR_histórico):
    régimen = "baja_volatilidad"
else:
    régimen = "lateral"
```

### 1.4 Señal de Mercado Unificada

**Algoritmo de votación ponderada**:
```python
señales = {
    'RSI': (-1 si RSI>70, +1 si RSI<30, 0 si neutral),
    'MACD': (+1 si MACD>signal, -1 si MACD<signal),
    'Bollinger': (-1 si precio>banda_sup, +1 si precio<banda_inf, 0 neutral),
    'Volumen': (+0.5 si ratio>1.5 y precio↑, -0.5 si ratio>1.5 y precio↓)
}

pesos = {
    'RSI': 0.3,
    'MACD': 0.4,
    'Bollinger': 0.2,
    'Volumen': 0.1
}

score_ponderado = Σ(señal_i × peso_i)

if score_ponderado > 0.2:
    señal_final = "alcista"
elif score_ponderado < -0.2:
    señal_final = "bajista"
else:
    señal_final = "neutral"
```

**Ejemplo completo**:
```
RSI = 65 → señal = 0 (neutral)
MACD = 2.3, Signal = 1.8 → MACD > Signal → señal = +1
Precio = 155, Banda_sup = 160, Banda_inf = 142 → señal = 0
Ratio_volumen = 1.8, Precio ↑ → señal = +0.5

score = (0 × 0.3) + (1 × 0.4) + (0 × 0.2) + (0.5 × 0.1)
      = 0 + 0.4 + 0 + 0.05 = 0.45

0.45 > 0.2 → Señal = "ALCISTA"
```

---

## 2. AGENTE DE MODELO PREDICTIVO (ModelAgent)

### 2.1 Arquitectura del Ensemble

**Modelos utilizados**:
1. Random Forest Regressor
2. XGBoost Regressor
3. LightGBM Regressor
4. Gradient Boosting Regressor
5. Ridge Regression

### 2.2 Features (Variables de Entrada)

**Features técnicos** (ventana de 30 días):
```
X = [
    RSI, MACD, MACD_signal, ATR, OBV,
    BB_upper, BB_lower, BB_width,
    SMA_20, EMA_12, EMA_26,
    Volumen_ratio, ADX, MFI,
    Precio_lag_1, Precio_lag_2, Precio_lag_3,
    Retorno_1d, Retorno_5d, Retorno_10d,
    Volatilidad_20d
]

Total features: 21 variables
```

### 2.3 Target (Variable Objetivo)

```
y = Precio_cierre(día siguiente)
```

### 2.4 División de Datos

```
Total datos: últimos 6 meses (≈126 días de trading)

Train set: primeros 80% (≈100 días)
Test set: últimos 20% (≈26 días)

Validación temporal: Sin shuffle (mantener orden cronológico)
```

### 2.5 Configuración de Modelos

#### 2.5.1 Random Forest

```python
Hiperparámetros:
- n_estimators = 100
- max_depth = 15
- min_samples_split = 5
- min_samples_leaf = 2
- random_state = 42
```

**Funcionamiento**:
- Crea 100 árboles de decisión
- Cada árbol vota por una predicción
- Predicción final = promedio de todos los árboles

#### 2.5.2 XGBoost

```python
Hiperparámetros:
- n_estimators = 100
- max_depth = 6
- learning_rate = 0.1
- subsample = 0.8
- colsample_bytree = 0.8
- random_state = 42
```

**Algoritmo**:
```
F₀(x) = ȳ  (predicción inicial = media)

Para m = 1 hasta M:
    1. Calcular residuales: rᵢ = yᵢ - Fₘ₋₁(xᵢ)
    2. Entrenar árbol hₘ(x) para predecir residuales
    3. Actualizar: Fₘ(x) = Fₘ₋₁(x) + η × hₘ(x)

donde η = learning_rate = 0.1
```

#### 2.5.3 LightGBM

```python
Hiperparámetros:
- n_estimators = 100
- max_depth = 6
- learning_rate = 0.1
- num_leaves = 31
- random_state = 42
```

**Diferencia con XGBoost**: Construye árboles leaf-wise (más profundo) en vez de level-wise.

#### 2.5.4 Gradient Boosting

```python
Hiperparámetros:
- n_estimators = 100
- max_depth = 5
- learning_rate = 0.1
- subsample = 0.8
- random_state = 42
```

#### 2.5.5 Ridge Regression

```python
Hiperparámetros:
- alpha = 1.0  (regularización L2)
```

**Fórmula**:
```
min ||y - Xβ||² + α||β||²

donde:
- y = precios objetivo
- X = matriz de features
- β = coeficientes a optimizar
- α = parámetro de regularización
```

### 2.6 Predicción del Ensemble

**Método 1: Promedio Ponderado por Rendimiento**

```python
Paso 1: Obtener predicción de cada modelo
pred_rf = modelo_rf.predict(X_test)
pred_xgb = modelo_xgb.predict(X_test)
pred_lgbm = modelo_lgbm.predict(X_test)
pred_gb = modelo_gb.predict(X_test)
pred_ridge = modelo_ridge.predict(X_test)

Paso 2: Calcular RMSE de cada modelo en validación
rmse_rf = RMSE(y_val, pred_rf_val)
rmse_xgb = RMSE(y_val, pred_xgb_val)
... (similar para otros)

Paso 3: Convertir RMSE a pesos (mejor modelo = mayor peso)
peso_i = (1 / rmse_i) / Σ(1 / rmse_j)

Paso 4: Predicción final
predicción_final = Σ(peso_i × pred_i)
```

**Ejemplo**:
```
Modelo          RMSE    1/RMSE   Peso (normalizado)
Random Forest   5.20    0.192    0.23 (23%)
XGBoost         4.80    0.208    0.25 (25%)
LightGBM        4.95    0.202    0.24 (24%)
Gradient Boost  5.10    0.196    0.23 (23%)
Ridge           9.50    0.105    0.13 (13%)  ← peor, menor peso
                        ------   ----
Total                   0.903    1.00

Predicciones individuales:
RF:    $152.30
XGB:   $153.10
LGBM:  $152.80
GB:    $152.50
Ridge: $151.00

Predicción_ensemble = (0.23×152.30) + (0.25×153.10) + (0.24×152.80) +
                      (0.23×152.50) + (0.13×151.00)
                    = 35.03 + 38.28 + 36.67 + 35.08 + 19.63
                    = $152.69
```

### 2.7 Cálculo de Confianza

**Fórmula**:
```
Confianza = 1 - (Varianza_predicciones / Precio_promedio)

Varianza_predicciones = Σ(pred_i - pred_mean)² / n

Límite: Confianza ∈ [0.3, 0.95]
```

**Ejemplo**:
```
Predicciones: [152.30, 153.10, 152.80, 152.50, 151.00]
Media = 152.34

Varianza = [(152.30-152.34)² + (153.10-152.34)² + (152.80-152.34)² +
            (152.50-152.34)² + (151.00-152.34)²] / 5
         = [0.0016 + 0.5776 + 0.2116 + 0.0256 + 1.7956] / 5
         = 2.612 / 5 = 0.522

Confianza = 1 - (0.522 / 152.34) = 1 - 0.0034 = 0.9966

Aplicar límite superior: min(0.9966, 0.95) = 0.95

Confianza_final = 95%
```

Si la varianza fuera más alta:
```
Predicciones muy dispersas: [145, 155, 148, 160, 142]
Media = 150
Varianza = 50.0

Confianza = 1 - (50 / 150) = 1 - 0.333 = 0.667 = 67%
```

### 2.8 Métricas de Evaluación

#### 2.8.1 RMSE (Root Mean Squared Error)

**Fórmula**:
```
RMSE = √[Σ(yᵢ - ŷᵢ)² / n]

donde:
- yᵢ = precio real
- ŷᵢ = precio predicho
- n = número de predicciones
```

**Interpretación**: Error promedio en dólares

**Ejemplo**:
```
Precios reales:    [150, 152, 148, 155, 153]
Precios predichos: [151, 153, 147, 154, 152]
Errores:           [ -1,  -1,   1,   1,   1]
Errores²:          [  1,   1,   1,   1,   1]

RMSE = √(5 / 5) = √1 = $1.00

Interpretación: En promedio, el modelo se equivoca ±$1.00
```

#### 2.8.2 MAE (Mean Absolute Error)

**Fórmula**:
```
MAE = Σ|yᵢ - ŷᵢ| / n
```

**Ejemplo**:
```
Usando datos anteriores:
MAE = (1 + 1 + 1 + 1 + 1) / 5 = $1.00
```

#### 2.8.3 MAPE (Mean Absolute Percentage Error)

**Fórmula**:
```
MAPE = (100 / n) × Σ|yᵢ - ŷᵢ| / |yᵢ|
```

**Ejemplo**:
```
MAPE = (100/5) × (1/150 + 1/152 + 1/148 + 1/155 + 1/153)
     = 20 × (0.0067 + 0.0066 + 0.0068 + 0.0065 + 0.0065)
     = 20 × 0.0331
     = 0.66%

Interpretación: El modelo tiene un error promedio del 0.66%
```

#### 2.8.4 R² (Coeficiente de Determinación)

**Fórmula**:
```
R² = 1 - (SS_res / SS_tot)

donde:
SS_res = Σ(yᵢ - ŷᵢ)²  (suma de cuadrados residuales)
SS_tot = Σ(yᵢ - ȳ)²   (suma de cuadrados totales)
ȳ = media de precios reales
```

**Interpretación**:
- R² = 1.0: Predicción perfecta
- R² = 0.9: El modelo explica el 90% de la variabilidad
- R² = 0.0: El modelo no es mejor que predecir la media

---

## 3. AGENTE DE SENTIMIENTO (SentimentAgent)

### 3.1 Fuentes de Noticias

**API utilizada**: Yahoo Finance News
```
Endpoint: /v1/finance/search
Parámetros:
- q = ticker
- newsCount = 10
```

### 3.2 Métodos de Análisis

#### 3.2.1 VADER (Valence Aware Dictionary and sEntiment Reasoner)

**Características**:
- Diseñado específicamente para redes sociales
- Considera emoticonos, mayúsculas, puntuación
- Retorna 4 scores: positivo, negativo, neutral, compuesto

**Fórmula del Score Compuesto**:
```
compound = Normalizar(suma_valencias)

Normalización:
compound = valencia / √(valencia² + α)

donde α = 15 (constante de normalización)

Rango: [-1, +1]
```

**Interpretación**:
```
compound ≥ 0.05:  Sentimiento POSITIVO
compound ≤ -0.05: Sentimiento NEGATIVO
-0.05 < compound < 0.05: NEUTRAL
```

**Ejemplo**:
```
Noticia: "Tesla stock surges 10% on strong earnings!"

VADER analiza:
- "surges" → valencia positiva (+3.5)
- "strong" → valencia positiva (+2.5)
- "!" → intensificador (×1.2)

Valencia_total = (3.5 + 2.5) × 1.2 = 7.2
compound = 7.2 / √(7.2² + 15) = 7.2 / √66.84 = 7.2 / 8.17 = 0.88

Resultado: POSITIVO (score = 0.88)
```

#### 3.2.2 TextBlob

**Funcionamiento**:
- Análisis léxico basado en diccionario
- Retorna: polaridad [-1, +1] y subjetividad [0, 1]

**Fórmula**:
```
Polaridad = Σ(valencia_palabra_i) / n_palabras

Subjetividad = n_palabras_subjetivas / n_palabras_totales
```

**Ejemplo**:
```
Noticia: "Good performance but uncertain outlook"

Polaridades:
- "good" → +0.7
- "performance" → 0.0
- "but" → 0.0
- "uncertain" → -0.3
- "outlook" → 0.0

Polaridad = (0.7 + 0 + 0 - 0.3 + 0) / 5 = 0.4 / 5 = 0.08

Subjetividad:
Palabras subjetivas: "good", "uncertain" = 2
Total palabras: 5
Subjetividad = 2/5 = 0.4
```

#### 3.2.3 FinBERT (Transformer para finanzas)

**Arquitectura**: BERT fine-tuned en textos financieros

**Proceso**:
1. Tokenización del texto
2. Encoding con BERT (768 dimensiones)
3. Clasificación en 3 clases: {positivo, negativo, neutral}

**Output**:
```
Probabilidades:
P(positivo) = 0.75
P(negativo) = 0.10
P(neutral) = 0.15

Sentimiento = argmax(P) = "positivo"
Score = P(positivo) - P(negativo) = 0.75 - 0.10 = 0.65
```

### 3.3 Ensemble de Sentimiento

**Método de combinación**:
```python
# Normalizar todos los scores a [-1, +1]
score_vader = vader_compound
score_textblob = textblob_polarity
score_finbert = finbert_score

# Promedio ponderado
pesos = {
    'vader': 0.20,      # Menos peso (general purpose)
    'textblob': 0.25,   # Peso moderado
    'finbert': 0.55     # Mayor peso (especializado en finanzas)
}

score_final = (score_vader × 0.20) +
              (score_textblob × 0.25) +
              (score_finbert × 0.55)
```

**Ejemplo completo**:
```
Para 10 noticias de AAPL:

Noticia 1: "Apple beats earnings expectations"
- VADER: 0.72
- TextBlob: 0.65
- FinBERT: 0.85
Score_1 = (0.72×0.20) + (0.65×0.25) + (0.85×0.55) = 0.144 + 0.163 + 0.468 = 0.775

Noticia 2: "iPhone sales decline in China"
- VADER: -0.45
- TextBlob: -0.30
- FinBERT: -0.60
Score_2 = (-0.45×0.20) + (-0.30×0.25) + (-0.60×0.55) = -0.090 - 0.075 - 0.330 = -0.495

... (continuar con las 10 noticias)

Scores: [0.775, -0.495, 0.320, 0.150, -0.200, 0.410, 0.550, -0.100, 0.280, 0.350]

Score_promedio = Σ scores / 10 = 2.040 / 10 = 0.204
```

### 3.4 Clasificación de Sentimiento

```python
if score_final > 0.05:
    sentimiento = "positivo"
elif score_final < -0.05:
    sentimiento = "negativo"
else:
    sentimiento = "neutral"
```

### 3.5 Cálculo de Confianza

**Fórmula**:
```
Base_confianza = 0.5

# Ajuste por número de noticias
ajuste_cantidad = min(n_noticias / 10, 1.0) × 0.2

# Ajuste por acuerdo entre métodos
desviación_métodos = std([score_vader, score_textblob, score_finbert])
ajuste_acuerdo = (1 - desviación_métodos) × 0.3

Confianza = Base_confianza + ajuste_cantidad + ajuste_acuerdo

Límites: Confianza ∈ [0.3, 0.9]
```

**Ejemplo**:
```
n_noticias = 10
Scores por noticia (promedio de 3 métodos):
VADER scores: [0.72, -0.45, 0.32, ...]
TextBlob scores: [0.65, -0.30, 0.28, ...]
FinBERT scores: [0.85, -0.60, 0.38, ...]

Para la noticia 1:
Desviación = std([0.72, 0.65, 0.85]) = 0.10 (bajo → alto acuerdo)

Confianza_1:
Base = 0.5
Ajuste_cantidad = min(10/10, 1.0) × 0.2 = 0.2
Ajuste_acuerdo = (1 - 0.10) × 0.3 = 0.27
Confianza = 0.5 + 0.2 + 0.27 = 0.97 → limitado a 0.9

Confianza_final = 90%
```

Si solo hay 3 noticias:
```
Ajuste_cantidad = min(3/10, 1.0) × 0.2 = 0.3 × 0.2 = 0.06
Confianza = 0.5 + 0.06 + 0.27 = 0.83 = 83%
```

---

## 4. AGENTE DE RECOMENDACIÓN (RecommendationAgent)

### 4.1 Modelo de Factores Multi-Señal

#### 4.1.1 Construcción del Vector de Factores

**15 factores normalizados a escala [-1, +1]**:

**A. Factores Técnicos (40% peso total)**:

1. **Trend Signal** (peso: 0.12):
```
trend = {
    "alcista": +0.8,
    "neutral": 0.0,
    "bajista": -0.8
}
```

2. **Momentum Signal** (peso: 0.10):
```
if RSI < 30:
    momentum = +0.7    # Sobreventa = oportunidad de compra
elif RSI > 70:
    momentum = -0.7    # Sobrecompra = cautela
else:
    momentum = (50 - RSI) / 50 × 0.5
```

Ejemplo:
```
RSI = 35 → momentum = (50-35)/50 × 0.5 = 0.15
RSI = 65 → momentum = (50-65)/50 × 0.5 = -0.15
```

3. **Volatility Signal** (peso: 0.08):
```
volatility_signal = -min(ATR / 5, 1.0) + 0.5

# Alta volatilidad genera cautela (señal negativa)
```

Ejemplo:
```
ATR = 2.0 → signal = -min(2/5, 1) + 0.5 = -0.4 + 0.5 = 0.1
ATR = 4.0 → signal = -min(4/5, 1) + 0.5 = -0.8 + 0.5 = -0.3
ATR = 6.0 → signal = -min(6/5, 1) + 0.5 = -1.0 + 0.5 = -0.5
```

4. **Volume Signal** (peso: 0.06):
```
if volumen_ratio > 1.5:
    signal = 0.5 × sign(variación_precio)  # Alto volumen confirma dirección
elif volumen_ratio < 0.5:
    signal = -0.3  # Bajo volumen = cautela
else:
    signal = 0.0
```

5. **Support/Resistance** (peso: 0.04):
```
# Placeholder (requiere análisis de niveles históricos)
signal = 0.0
```

**B. Factores de Predicción (35% peso total)**:

6. **Model Prediction** (peso: 0.15):
```
signal = tanh(variación_pct / 5)

# tanh normaliza a [-1, +1]
```

Ejemplo:
```
variación = +5% → signal = tanh(5/5) = tanh(1) = 0.76
variación = +2.5% → signal = tanh(0.5) = 0.46
variación = -5% → signal = tanh(-1) = -0.76
```

7. **Prediction Confidence** (peso: 0.10):
```
signal = (confianza × 2) - 1

# Convierte [0, 1] a [-1, +1]
```

Ejemplo:
```
confianza = 0.8 → signal = (0.8×2) - 1 = 0.6
confianza = 0.5 → signal = (0.5×2) - 1 = 0.0
confianza = 0.3 → signal = (0.3×2) - 1 = -0.4
```

8. **Ensemble Agreement** (peso: 0.10):
```
signal = confianza × 0.8
```

**C. Factores de Sentimiento (15% peso total)**:

9. **Sentiment Score** (peso: 0.08):
```
sent_map = {
    "positivo": +0.7,
    "neutral": 0.0,
    "negativo": -0.7
}

signal = sent_map[sentimiento] × confianza_sentimiento
```

Ejemplo:
```
Sentimiento = "positivo", confianza = 0.6
signal = 0.7 × 0.6 = 0.42
```

10. **Sentiment Trend** (peso: 0.04):
```
signal = sentiment_score_numérico × 0.5
```

11. **News Impact** (peso: 0.03):
```
signal = sentiment_factor × 0.5
```

**D. Factores de Riesgo (10% peso total)**:

12. **Risk-Adjusted Return** (peso: 0.05):
```
risk_adj = variación_pct / (volatilidad + 0.5)
signal = tanh(risk_adj / 2)
```

Ejemplo:
```
variación = 3%, volatilidad = 2%
risk_adj = 3 / (2 + 0.5) = 1.2
signal = tanh(1.2/2) = tanh(0.6) = 0.54
```

13. **Market Regime** (peso: 0.03):
```
regime_map = {
    "tendencia_alcista": +0.5,
    "tendencia_bajista": -0.5,
    "alta_volatilidad": -0.3,
    "baja_volatilidad": +0.2,
    "lateral": 0.0,
    "normal": 0.0
}
```

14. **Correlation Factor** (peso: 0.02):
```
# Placeholder (requiere correlación con índices)
signal = 0.0
```

#### 4.1.2 Cálculo del Composite Score

**Fórmula**:
```
composite_score = Σ(factor_i × peso_i) / Σ(pesos_i)
```

**Ejemplo completo para TSLA**:

```
DATOS DE ENTRADA:
- Tendencia: neutral
- RSI: 50
- Volatilidad (ATR): 3.3%
- Ratio volumen: 1.2
- Variación predicha: +2.83%
- Confianza modelo: 0.54
- Sentimiento: positivo (score: 0.16, confianza: 0.39)
- Régimen: normal

CÁLCULO DE FACTORES:

Factor                    | Valor raw | Normalizado | Peso  | Contribución
--------------------------|-----------|-------------|-------|-------------
1. trend_signal           | neutral   |  0.00       | 0.12  |  0.000
2. momentum_signal        | RSI=50    |  0.00       | 0.10  |  0.000
3. volatility_signal      | ATR=3.3   | -0.16       | 0.08  | -0.013
4. volume_signal          | ratio=1.2 |  0.00       | 0.06  |  0.000
5. support_resistance     | -         |  0.00       | 0.04  |  0.000
--------------------------|-----------|-------------|-------|-------------
6. model_prediction       | +2.83%    |  0.49       | 0.15  |  0.074  ✓
7. prediction_confidence  | 0.54      |  0.08       | 0.10  |  0.008
8. ensemble_agreement     | 0.54      |  0.43       | 0.10  |  0.043  ✓
--------------------------|-----------|-------------|-------|-------------
9. sentiment_score        | pos×0.39  |  0.27       | 0.08  |  0.022  ✓
10. sentiment_trend       | 0.16      |  0.16       | 0.04  |  0.006
11. news_impact           | 0.14      |  0.14       | 0.03  |  0.004
--------------------------|-----------|-------------|-------|-------------
12. risk_adjusted_return  | 2.83/3.8  |  0.60       | 0.05  |  0.030  ✓
13. market_regime         | normal    |  0.00       | 0.03  |  0.000
14. correlation_factor    | -         |  0.00       | 0.02  |  0.000
--------------------------|-----------|-------------|-------|-------------
SUMA                                                        |  0.174
```

```
composite_score = 0.174 / 1.00 = 0.174
```

### 4.2 Evaluación de Riesgo

#### 4.2.1 Componentes del Risk Assessment

**1. Volatility Score**:
```
volatility_score = min(ATR / 5.0, 1.0)

Interpretación:
- ATR = 2.0 → score = 0.40 (volatilidad moderada)
- ATR = 5.0 → score = 1.00 (volatilidad muy alta)
```

**2. Value at Risk (VaR 95%)**:
```
VaR_95 = |variación_pct| × 1.65

# 1.65 es el z-score para 95% de confianza en distribución normal
```

Ejemplo:
```
variación = +2.83%
VaR_95 = 2.83 × 1.65 = 4.67%

Interpretación: Hay 95% de probabilidad de que la pérdida no exceda 4.67%
```

**3. Maximum Drawdown Esperado**:
```
max_drawdown = ATR × 2.5
```

Ejemplo:
```
ATR = 3.3%
max_drawdown = 3.3 × 2.5 = 8.25%
```

**4. Correlation Risk**:
```
if market_regime in ["alta_volatilidad", "tendencia_bajista"]:
    correlation_risk = 0.3
else:
    correlation_risk = 0.15
```

**5. Liquidity Risk**:
```
# Simplificado (en producción usar volumen/float)
liquidity_risk = 0.1
```

**6. Event Risk**:
```
event_risk = 1 - confianza_sentimiento
```

Ejemplo:
```
confianza_sentimiento = 0.39
event_risk = 1 - 0.39 = 0.61 (alta incertidumbre)
```

#### 4.2.2 Overall Risk Score

**Fórmula ponderada**:
```
overall_risk = (volatility_score × 0.35) +
               (VaR_95 / 10 × 0.25) +
               (correlation_risk × 0.15) +
               (liquidity_risk × 0.10) +
               (event_risk × 0.15)

Límite: min(overall_risk, 1.0)
```

**Ejemplo TSLA**:
```
volatility_score = min(3.3/5, 1) = 0.66
VaR_95 = 2.83 × 1.65 = 4.67
correlation_risk = 0.15 (mercado normal)
liquidity_risk = 0.1
event_risk = 0.61

overall_risk = (0.66 × 0.35) + (4.67/10 × 0.25) + (0.15 × 0.15) +
               (0.1 × 0.10) + (0.61 × 0.15)
             = 0.231 + 0.117 + 0.023 + 0.010 + 0.092
             = 0.473

Nivel de riesgo: MODERADO (0.4 < risk < 0.6)
```

**Clasificación de Risk Level**:
```
if overall_risk < 0.2:
    risk_level = "muy_bajo"
elif overall_risk < 0.4:
    risk_level = "bajo"
elif overall_risk < 0.6:
    risk_level = "moderado"
elif overall_risk < 0.8:
    risk_level = "alto"
else:
    risk_level = "muy_alto"
```

### 4.3 Probabilidad de Ganancia

**Fórmula de 3 componentes**:

```
prob_ganancia = base_prob + confidence_adj + risk_adj

donde:
base_prob = 0.5 + (composite_score × 0.3)
confidence_adj = prediction_confidence × 0.1
risk_adj = -overall_risk_score × 0.1

Límites: prob ∈ [0.2, 0.8]
```

**Desglose del cálculo**:

1. **Probabilidad base (50% ± 30%)**:
```
Si composite_score = +0.5 → base = 0.5 + (0.5×0.3) = 0.65 (65%)
Si composite_score = 0.0 → base = 0.5 + (0.0×0.3) = 0.50 (50%)
Si composite_score = -0.5 → base = 0.5 + (-0.5×0.3) = 0.35 (35%)
```

2. **Ajuste por confianza (±10%)**:
```
Si confianza = 0.8 → adj = 0.8 × 0.1 = +0.08 (+8%)
Si confianza = 0.5 → adj = 0.5 × 0.1 = +0.05 (+5%)
Si confianza = 0.3 → adj = 0.3 × 0.1 = +0.03 (+3%)
```

3. **Penalización por riesgo (±10%)**:
```
Si risk = 0.3 → adj = -0.3 × 0.1 = -0.03 (-3%)
Si risk = 0.5 → adj = -0.5 × 0.1 = -0.05 (-5%)
Si risk = 0.7 → adj = -0.7 × 0.1 = -0.07 (-7%)
```

**Ejemplo TSLA completo**:
```
composite_score = 0.174
prediction_confidence = 0.54
overall_risk = 0.473

base_prob = 0.5 + (0.174 × 0.3) = 0.5 + 0.052 = 0.552
confidence_adj = 0.54 × 0.1 = 0.054
risk_adj = -0.473 × 0.1 = -0.047

prob = 0.552 + 0.054 - 0.047 = 0.559

Aplicar límites: clip(0.559, 0.2, 0.8) = 0.559

Probabilidad final = 55.9% ≈ 56%
```

### 4.4 Position Sizing (Kelly Criterion)

**Fórmula de Kelly modificada**:

```
Kelly_óptimo = (b × p - q) / b

donde:
b = expected_return / volatility (odds)
p = probabilidad de ganancia
q = 1 - p (probabilidad de pérdida)

Kelly_conservador = Kelly_óptimo × 0.25  # Usar solo 25% del Kelly
```

**Ajuste por riesgo**:
```
risk_adjustment = 1 - risk_score
asignación_base = Kelly_conservador × risk_adjustment × 100

# Convertir a porcentaje del portfolio
asignación_sugerida = clip(asignación_base, 1, 10)  # Límites: 1-10%
asignación_máxima = clip(asignación_sugerida × 1.5, 1, 15)  # Max: 15%
```

**Ejemplo TSLA**:
```
expected_return = 2.83%
volatility = 3.3%
prob_ganancia = 0.56
risk_score = 0.473

b = 2.83 / 3.3 = 0.858
p = 0.56
q = 1 - 0.56 = 0.44

Kelly_óptimo = (0.858 × 0.56 - 0.44) / 0.858
             = (0.480 - 0.44) / 0.858
             = 0.040 / 0.858
             = 0.047 (4.7%)

Kelly_conservador = 0.047 × 0.25 = 0.012 (1.2%)

risk_adjustment = 1 - 0.473 = 0.527
asignación_base = 0.012 × 0.527 × 100 = 0.63%

asignación_sugerida = max(0.63, 1) = 1.0%  # Mínimo 1%
asignación_máxima = min(1.0 × 1.5, 15) = 1.5%

Recomendación: Asignar 1-1.5% del portfolio a TSLA
```

**Stop Loss y Take Profit**:
```
stop_loss = clip(volatility × 1.5, 2, 10)  # 2-10%
take_profit = |expected_return| × 1.5 si expected_return > 0
              else volatility × 2

risk_reward_ratio = take_profit / stop_loss
```

Ejemplo TSLA:
```
stop_loss = clip(3.3 × 1.5, 2, 10) = clip(4.95, 2, 10) = 4.95%
take_profit = 2.83 × 1.5 = 4.25%

risk_reward = 4.25 / 4.95 = 0.86:1

Interpretación: Riesgo ligeramente mayor que recompensa (no ideal)
```

### 4.5 Determinación del Tipo de Recomendación

**Umbrales de decisión basados en composite_score**:

```
if score ≥ 0.60:
    tipo = "COMPRA FUERTE"
elif score ≥ 0.30:
    tipo = "COMPRA"
elif score ≥ 0.10:
    tipo = "COMPRA DÉBIL"
elif score ≥ -0.10:
    tipo = "MANTENER"
elif score ≥ -0.30:
    tipo = "VENTA DÉBIL"
elif score ≥ -0.60:
    tipo = "VENTA"
else:
    tipo = "VENTA FUERTE"
```

**Ejemplo TSLA**:
```
composite_score = 0.174

0.174 está entre 0.10 y 0.30

Tipo = "COMPRA DÉBIL"
Tipo_simplificado = "compra"
```

### 4.6 Confianza de la Recomendación

**Fórmula multi-factor**:

```
score_confidence = |composite_score|  # Magnitud del score

# Acuerdo entre factores
directions = [dirección de top 5 factores]  # "bullish", "bearish", "neutral"
bullish_count = count(directions == "bullish")
bearish_count = count(directions == "bearish")
agreement = |bullish_count - bearish_count| / len(directions)

# Penalización por riesgo
risk_penalty = overall_risk_score × 0.2

confianza = (score_confidence × 0.4) + (agreement × 0.4) + 0.2 - risk_penalty

Límites: confianza ∈ [0.3, 0.95]
```

**Ejemplo TSLA**:
```
score_confidence = |0.174| = 0.174

Top 5 factores y sus direcciones:
1. model_prediction (0.074) → bullish
2. ensemble_agreement (0.043) → bullish
3. risk_adjusted_return (0.030) → bullish
4. sentiment_score (0.022) → bullish
5. volatility_signal (-0.013) → bearish

bullish = 4, bearish = 1
agreement = |4 - 1| / 5 = 0.6

risk_penalty = 0.473 × 0.2 = 0.095

confianza = (0.174 × 0.4) + (0.6 × 0.4) + 0.2 - 0.095
          = 0.070 + 0.240 + 0.200 - 0.095
          = 0.415

Confianza final = 41.5% ≈ 42%
```

---

## 5. AGENTE DE ALERTAS (AlertAgent)

### 5.1 Tipos de Alertas

**Clasificación por severidad**:

```
if |variación_pct| ≥ umbral_crítico:
    nivel = "CRÍTICO"
    tipo = "precio" si variación normal
           "volatilidad" si ATR muy alto
           "volumen" si volumen anormal

elif |variación_pct| ≥ umbral_warning:
    nivel = "WARNING"
    tipo = similar al anterior

else:
    sin_alerta = True
```

### 5.2 Umbrales Configurables

**Valores por defecto**:
```
umbral_warning = 3.0%
umbral_crítico = 7.0%

Configurables por usuario en tiempo real
```

### 5.3 Detección de Condiciones Especiales

**1. Alta Volatilidad**:
```
if ATR > percentil_90(ATR_histórico):
    añadir_factor("Alta volatilidad detectada")
```

**2. Volumen Anormal**:
```
if volumen_ratio > 3.0:
    añadir_factor("Volumen excepcionalmente alto")
elif volumen_ratio < 0.3:
    añadir_factor("Volumen inusualmente bajo")
```

**3. Divergencias**:
```
if (precio ↑ y sentimiento negativo) or (precio ↓ y sentimiento positivo):
    añadir_factor("Divergencia precio-sentimiento")
```

### 5.4 Generación de Mensaje de Alerta

**Template**:
```
if nivel == "CRÍTICO":
    mensaje = f"⚠️ ALERTA CRÍTICA: {ticker} muestra variación de {variación:+.2f}%
               ({dirección}). {factores_adicionales}"

elif nivel == "WARNING":
    mensaje = f"⚠️ ADVERTENCIA: {ticker} con variación de {variación:+.2f}%.
               {factores_adicionales}"
```

**Ejemplo**:
```
ticker = "TSLA"
variación = -8.5%
umbral_crítico = 7.0%
ATR = 5.2% (muy alto)
volumen_ratio = 3.5 (muy alto)

Detección:
|- variación| = 8.5% > 7.0% → CRÍTICO
ATR > percentil_90 → factor: "Alta volatilidad"
volumen_ratio > 3.0 → factor: "Volumen excepcional"

Mensaje generado:
"⚠️ ALERTA CRÍTICA: TSLA muestra variación de -8.50% (bajista fuerte).
Factores adicionales: Alta volatilidad detectada (ATR: 5.2%),
Volumen excepcional (3.5x promedio)"
```

### 5.5 Persistencia de Alertas

```sql
INSERT INTO alertas (
    usuario_id,
    ticker,
    tipo,
    nivel,
    mensaje,
    variacion_pct,
    precio_actual,
    leida,
    fecha_creacion
) VALUES (?, ?, ?, ?, ?, ?, ?, 0, NOW())
```

---

## 6. FLUJO DE INTEGRACIÓN

### 6.1 Pipeline Completo de Análisis

```
Usuario solicita análisis de TICKER
         ↓
┌────────────────────────────────────────┐
│ 1. MarketAgent                         │
│   - Descargar datos (6 meses)         │
│   - Calcular 14 indicadores técnicos  │
│   - Detectar régimen de mercado       │
│   - Generar señal unificada           │
│   Output: market_data                 │
└────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────┐
│ 2. ModelAgent                          │
│   - Construir features (21 variables) │
│   - Ejecutar 5 modelos ML             │
│   - Ensemble ponderado                │
│   - Calcular métricas (RMSE, MAE)     │
│   Output: prediction                  │
└────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────┐
│ 3. SentimentAgent                      │
│   - Obtener 10 noticias recientes     │
│   - Análisis con VADER + TextBlob +   │
│     FinBERT                           │
│   - Promedio ponderado (FinBERT 55%) │
│   - Clasificar sentimiento            │
│   Output: sentiment                   │
└────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────┐
│ 4. RecommendationAgent                 │
│   - Construir vector de 15 factores   │
│   - Calcular composite_score          │
│   - Evaluar riesgo (6 componentes)    │
│   - Calcular prob. ganancia           │
│   - Position sizing (Kelly)           │
│   - Determinar tipo de recomendación  │
│   Output: recommendation              │
└────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────┐
│ 5. AlertAgent                          │
│   - Comparar vs umbrales              │
│   - Detectar condiciones especiales   │
│   - Generar mensaje si aplica         │
│   - Persistir en BD                   │
│   Output: alert (opcional)            │
└────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────┐
│ 6. Consolidación y Respuesta           │
│   - Integrar todos los outputs        │
│   - Formatear para dashboard          │
│   - Retornar JSON completo            │
└────────────────────────────────────────┘
```

### 6.2 Ejemplo de Flujo Completo: TSLA

**INPUT**:
```
ticker = "TSLA"
umbral_warning = 3.0%
umbral_crítico = 7.0%
```

**PASO 1 - MarketAgent**:
```
Datos descargados: 126 días
Precio actual: $397.21
Precio anterior: $396.50

Indicadores calculados:
- RSI: 52.3
- MACD: 2.15
- Signal: 1.89
- ATR: 3.28
- Bollinger: (385.2, 398.5, 411.8)
- Volumen ratio: 1.15
- ADX: 22.1

Régimen detectado: "neutral" (ADX < 25)
Señal técnica: "neutral" (score = 0.05)
```

**PASO 2 - ModelAgent**:
```
Features construidos: 21 variables × 125 samples

Modelos entrenados:
- Random Forest: RMSE = $13.50
- XGBoost: RMSE = $12.80
- LightGBM: RMSE = $13.10
- Gradient Boost: RMSE = $13.25
- Ridge: RMSE = $18.90

Pesos calculados:
- RF: 22%
- XGB: 24% (mejor modelo)
- LGBM: 23%
- GB: 23%
- Ridge: 8%

Predicciones individuales:
- RF: $408.20
- XGB: $409.10
- LGBM: $408.50
- GB: $408.30
- Ridge: $405.80

Predicción ensemble: $408.45
Variación: +2.83%
Confianza: 54%
RMSE: $13.10
```

**PASO 3 - SentimentAgent**:
```
Noticias obtenidas: 10

Análisis por noticia:
1. "Tesla expands production capacity" → +0.65
2. "Concerns about competition" → -0.30
3. "Strong Q4 deliveries expected" → +0.72
...

Scores promedio:
- VADER: 0.18
- TextBlob: 0.12
- FinBERT: 0.22

Score final: (0.18×0.20) + (0.12×0.25) + (0.22×0.55) = 0.187
Sentimiento: POSITIVO
Confianza: 39%
```

**PASO 4 - RecommendationAgent**:
```
Factores construidos (15):
- Top factor: model_prediction (+0.074)
- 2do: ensemble_agreement (+0.043)
- 3ro: risk_adjusted_return (+0.030)

Composite score: 0.174

Risk assessment:
- Volatility score: 0.66
- VaR 95%: 4.67%
- Overall risk: 0.473 (MODERADO)

Probabilidad ganancia: 56%

Position sizing:
- Sugerida: 1.0% del portfolio
- Máxima: 1.5%
- Stop loss: 4.95%
- Take profit: 4.25%

Tipo: COMPRA DÉBIL (score = 0.174 ∈ [0.10, 0.30])
Confianza: 42%
```

**PASO 5 - AlertAgent**:
```
Variación: 2.83%
Umbral warning: 3.0%
Umbral crítico: 7.0%

2.83% < 3.0% → Sin alerta

Output: { tiene_alerta: false }
```

**OUTPUT FINAL JSON**:
```json
{
  "ticker": "TSLA",
  "fecha_analisis": "2026-02-05T18:32:52",
  "mercado": {
    "ultimo_precio": 397.21,
    "precio_anterior": 396.50,
    "variacion_diaria": 0.18,
    "senal": "neutral",
    "indicadores": {
      "rsi": 52.3,
      "macd": 2.15,
      "macd_signal": 1.89,
      "atr": 3.28,
      "bb_upper": 411.8,
      "bb_lower": 385.2,
      "adx": 22.1,
      "mfi": 58.2
    }
  },
  "prediccion": {
    "precio_predicho": 408.45,
    "variacion_pct": 2.83,
    "confianza": 0.54,
    "metricas": {
      "rmse": 13.10,
      "mae": 10.52,
      "mape": 2.65
    }
  },
  "sentimiento": {
    "sentimiento": "positivo",
    "score": 0.187,
    "confianza": 0.39
  },
  "recomendacion": {
    "tipo": "compra",
    "accion_sugerida": "Considerar comprar TSLA",
    "confianza": 0.42,
    "probability_profit": 0.56,
    "risk_level": "moderado",
    "position_sizing": {
      "suggested_allocation": 1.0,
      "stop_loss": 4.95,
      "take_profit": 4.25
    }
  },
  "alerta": {
    "tiene_alerta": false
  }
}
```

---

## GLOSARIO DE TÉRMINOS

**ATR (Average True Range)**: Indicador de volatilidad que mide el rango promedio de movimiento del precio.

**Composite Score**: Puntuación combinada de múltiples factores de análisis, normalizada entre -1 y +1.

**Ensemble**: Combinación de múltiples modelos de machine learning para mejorar precisión.

**Kelly Criterion**: Fórmula matemática para calcular el tamaño óptimo de una apuesta/inversión.

**MACD**: Indicador de momentum basado en medias móviles exponenciales.

**Risk-Adjusted Return**: Retorno esperado dividido por la volatilidad (Sharpe ratio simplificado).

**RSI**: Indicador que mide velocidad y magnitud de cambios de precio (0-100).

**Sentiment Score**: Puntuación numérica del sentimiento de mercado basado en análisis de noticias.

**VaR (Value at Risk)**: Pérdida máxima esperada con un nivel de confianza dado (95%).

---

## REFERENCIAS

1. Wilder, J. W. (1978). *New Concepts in Technical Trading Systems*. Trend Research.
2. Appel, G. (2005). *Technical Analysis: Power Tools for Active Investors*. FT Press.
3. Bollinger, J. (2001). *Bollinger on Bollinger Bands*. McGraw-Hill.
4. Kelly, J. L. (1956). "A New Interpretation of Information Rate". *Bell System Technical Journal*.
5. Hutto, C. & Gilbert, E. (2014). "VADER: A Parsimonious Rule-based Model for Sentiment Analysis". *ICWSM*.
6. Araci, D. (2019). "FinBERT: Financial Sentiment Analysis with Pre-trained Language Models". arXiv.
7. Chen, T. & Guestrin, C. (2016). "XGBoost: A Scalable Tree Boosting System". *KDD*.

---

**Fin del Anexo Técnico**

*Documento generado para: Sistema Multiagente de Seguimiento Financiero*
*Versión: 1.0*
*Fecha: Febrero 2026*
