# Ejemplos de Uso

Este documento proporciona ejemplos prácticos de cómo usar el Sistema Multiagente de Seguimiento Financiero.

## 📑 Contenidos

- [Uso Básico desde Dashboard](#uso-básico-desde-dashboard)
- [Uso de la API con cURL](#uso-de-la-api-con-curl)
- [Uso de la API con Python](#uso-de-la-api-con-python)
- [Uso de la API con JavaScript](#uso-de-la-api-con-javascript)
- [Casos de Uso Reales](#casos-de-uso-reales)
- [Scripts de Automatización](#scripts-de-automatización)

---

## Uso Básico desde Dashboard

### 1. Primera Vez - Registro

1. Abre el navegador en `http://localhost:8501`
2. Click en "Registrarse"
3. Completa el formulario:
   - **Usuario**: investor123
   - **Email**: investor@example.com
   - **Contraseña**: SecurePass123!
4. Click en "Crear cuenta"

### 2. Iniciar Sesión

1. Ingresa tu usuario y contraseña
2. Click en "Iniciar Sesión"
3. Serás redirigido al dashboard principal

### 3. Analizar un Activo

**Ejemplo: Analizar Apple (AAPL)**

1. En el campo de búsqueda, ingresa: `AAPL`
2. Click en el botón "Analizar 🔍"
3. Espera 10-20 segundos mientras el sistema:
   - Descarga datos históricos
   - Calcula 20+ indicadores técnicos
   - Entrena ensemble de 5+ modelos ML
   - Analiza 7 noticias con NLP
   - Genera recomendación multi-factor
4. Revisa los resultados:
   - **Análisis Técnico**: Score 6.8/10, tendencia alcista
   - **Predicción**: $188.75 (rango: $183.20 - $194.30)
   - **Sentimiento**: Positivo (0.42)
   - **Recomendación**: COMPRA MODERADA (confianza: 82%)

### 4. Interpretar la Recomendación

**Ejemplo de resultado:**

```
🟢 COMPRA MODERADA
Confianza: 82%

Razón:
"Señales técnicas alcistas combinadas con sentimiento positivo
y predicción favorable. RSI en 58 indica momentum positivo sin
sobrecompra. MACD bullish crossover confirmado."

Factores:
- Técnico: 6.8/10 (peso 40%) → 2.72
- Predicción: 7.5/10 (peso 35%) → 2.63
- Sentimiento: 6.5/10 (peso 15%) → 0.98
- Riesgo: 5.2/10 (peso 10%) → 0.52
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Score Total: 6.85/10

Position Sizing:
- Allocación sugerida: 5.0% del portafolio
- Stop Loss: $176.15 (-5.0%)
- Take Profit: $195.80 (+5.6%)
- Risk/Reward: 2.5:1

Riesgos:
⚠️ Volatilidad moderada (ATR: 2.45)
⚠️ Exposición al sector tecnológico
```

### 5. Gestionar Alertas

1. Click en la pestaña "Alertas"
2. Verás alertas como:
   ```
   ⚠️ TSLA - Variación crítica (-7.8%)
   Precio actual: $245.30
   Precio predicho: $265.50
   Hace 2 horas
   ```
3. Click en "✓" para marcar como leída
4. Las alertas críticas aparecen en rojo, warnings en amarillo

---

## Uso de la API con cURL

### 1. Registro de Usuario

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "trader_pro",
    "email": "trader@example.com",
    "password": "StrongPass456!"
  }'
```

**Respuesta:**
```json
{
  "id": 1,
  "username": "trader_pro",
  "email": "trader@example.com",
  "rol": "user",
  "fecha_registro": "2026-02-05T10:30:00"
}
```

### 2. Login y Obtener Token

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=trader_pro&password=StrongPass456!"
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0cmFkZXJfcHJvIiwiZXhwIjoxNzA3MTM2MjAwfQ.xyz123",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Guardar token en variable:**
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 3. Análisis Completo de Activo

```bash
curl -X GET "http://localhost:8000/predict/AAPL" \
  -H "Authorization: Bearer $TOKEN" \
  | jq '.'  # Formatear JSON con jq
```

### 4. Solo Análisis Técnico

```bash
curl -X GET "http://localhost:8000/predict/AAPL/market" \
  -H "Authorization: Bearer $TOKEN" \
  | jq '.market_data'
```

### 5. Solo Análisis de Sentimiento

```bash
curl -X GET "http://localhost:8000/predict/AAPL/sentiment" \
  -H "Authorization: Bearer $TOKEN" \
  | jq '.sentiment'
```

### 6. Listar Alertas

```bash
curl -X GET "http://localhost:8000/alerts?skip=0&limit=10" \
  -H "Authorization: Bearer $TOKEN" \
  | jq '.alertas'
```

### 7. Estadísticas de Alertas

```bash
curl -X GET "http://localhost:8000/alerts/stats" \
  -H "Authorization: Bearer $TOKEN" \
  | jq '.'
```

### 8. Marcar Alerta como Leída

```bash
curl -X PUT "http://localhost:8000/alerts/45/read" \
  -H "Authorization: Bearer $TOKEN"
```

### 9. Eliminar Alerta

```bash
curl -X DELETE "http://localhost:8000/alerts/45" \
  -H "Authorization: Bearer $TOKEN"
```

### 10. Health Check

```bash
curl -X GET "http://localhost:8000/health"
```

---

## Uso de la API con Python

### Cliente Python Completo

```python
import requests
from typing import Optional, Dict, Any
import json

class FinancialTrackerClient:
    """Cliente Python para la API de Financial Tracker"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token: Optional[str] = None

    def register(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Registrar nuevo usuario"""
        response = requests.post(
            f"{self.base_url}/auth/register",
            json={"username": username, "email": email, "password": password}
        )
        response.raise_for_status()
        return response.json()

    def login(self, username: str, password: str) -> str:
        """Iniciar sesión y obtener token"""
        response = requests.post(
            f"{self.base_url}/auth/login",
            data={"username": username, "password": password}
        )
        response.raise_for_status()
        data = response.json()
        self.token = data["access_token"]
        return self.token

    def _headers(self) -> Dict[str, str]:
        """Headers con autenticación"""
        if not self.token:
            raise ValueError("No estás autenticado. Ejecuta login() primero.")
        return {"Authorization": f"Bearer {self.token}"}

    def analyze_ticker(self, ticker: str) -> Dict[str, Any]:
        """Análisis completo de un ticker"""
        response = requests.get(
            f"{self.base_url}/predict/{ticker}",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def get_market_data(self, ticker: str) -> Dict[str, Any]:
        """Solo datos de mercado"""
        response = requests.get(
            f"{self.base_url}/predict/{ticker}/market",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def get_sentiment(self, ticker: str) -> Dict[str, Any]:
        """Solo análisis de sentimiento"""
        response = requests.get(
            f"{self.base_url}/predict/{ticker}/sentiment",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def get_alerts(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """Obtener alertas del usuario"""
        response = requests.get(
            f"{self.base_url}/alerts",
            params={"skip": skip, "limit": limit},
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def mark_alert_read(self, alert_id: int) -> Dict[str, Any]:
        """Marcar alerta como leída"""
        response = requests.put(
            f"{self.base_url}/alerts/{alert_id}/read",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def delete_alert(self, alert_id: int) -> bool:
        """Eliminar alerta"""
        response = requests.delete(
            f"{self.base_url}/alerts/{alert_id}",
            headers=self._headers()
        )
        return response.status_code == 204


# Ejemplo de uso
if __name__ == "__main__":
    # Crear cliente
    client = FinancialTrackerClient()

    # Login
    client.login("trader_pro", "StrongPass456!")
    print("✅ Autenticado correctamente")

    # Analizar Apple
    print("\n📊 Analizando AAPL...")
    analysis = client.analyze_ticker("AAPL")

    # Mostrar resultados
    print(f"\n🔍 Análisis de {analysis['ticker']}")
    print(f"Precio actual: ${analysis['market_data']['precio_actual']}")
    print(f"Precio predicho: ${analysis['prediction']['precio_predicho']}")
    print(f"Sentimiento: {analysis['sentiment']['categoria']} ({analysis['sentiment']['score']})")
    print(f"Recomendación: {analysis['recommendation']['accion'].upper()}")
    print(f"Confianza: {analysis['recommendation']['confianza'] * 100:.1f}%")

    # Ver alertas
    print("\n🚨 Alertas activas:")
    alerts = client.get_alerts(limit=5)
    for alert in alerts['alertas']:
        if not alert['leida']:
            print(f"  {alert['tipo'].upper()}: {alert['ticker']} - {alert['mensaje']}")
```

### Ejemplo Simple

```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/auth/login",
    data={"username": "trader_pro", "password": "StrongPass456!"}
)
token = response.json()["access_token"]

# Analizar Tesla
headers = {"Authorization": f"Bearer {token}"}
analysis = requests.get(
    "http://localhost:8000/predict/TSLA",
    headers=headers
).json()

print(f"Tesla Price: ${analysis['market_data']['precio_actual']}")
print(f"Recommendation: {analysis['recommendation']['accion']}")
```

---

## Uso de la API con JavaScript

### Cliente JavaScript (Node.js)

```javascript
const axios = require('axios');

class FinancialTrackerClient {
  constructor(baseURL = 'http://localhost:8000') {
    this.baseURL = baseURL;
    this.token = null;
  }

  async login(username, password) {
    const response = await axios.post(`${this.baseURL}/auth/login`,
      `username=${username}&password=${password}`,
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
    );
    this.token = response.data.access_token;
    return this.token;
  }

  async analyzeTicker(ticker) {
    const response = await axios.get(`${this.baseURL}/predict/${ticker}`, {
      headers: { Authorization: `Bearer ${this.token}` }
    });
    return response.data;
  }

  async getAlerts(skip = 0, limit = 100) {
    const response = await axios.get(`${this.baseURL}/alerts`, {
      params: { skip, limit },
      headers: { Authorization: `Bearer ${this.token}` }
    });
    return response.data;
  }
}

// Uso
(async () => {
  const client = new FinancialTrackerClient();

  await client.login('trader_pro', 'StrongPass456!');
  console.log('✅ Authenticated');

  const analysis = await client.analyzeTicker('AAPL');
  console.log(`📊 ${analysis.ticker}`);
  console.log(`Price: $${analysis.market_data.precio_actual}`);
  console.log(`Recommendation: ${analysis.recommendation.accion}`);
})();
```

### Cliente JavaScript (Browser - Fetch API)

```javascript
class FinancialTracker {
  constructor(baseURL = 'http://localhost:8000') {
    this.baseURL = baseURL;
    this.token = null;
  }

  async login(username, password) {
    const response = await fetch(`${this.baseURL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: `username=${username}&password=${password}`
    });
    const data = await response.json();
    this.token = data.access_token;
    return this.token;
  }

  async analyzeTicker(ticker) {
    const response = await fetch(`${this.baseURL}/predict/${ticker}`, {
      headers: { Authorization: `Bearer ${this.token}` }
    });
    return await response.json();
  }

  async getAlerts() {
    const response = await fetch(`${this.baseURL}/alerts`, {
      headers: { Authorization: `Bearer ${this.token}` }
    });
    return await response.json();
  }
}

// Uso en HTML
const tracker = new FinancialTracker();

document.getElementById('loginBtn').addEventListener('click', async () => {
  await tracker.login('trader_pro', 'StrongPass456!');
  alert('Logged in!');
});

document.getElementById('analyzeBtn').addEventListener('click', async () => {
  const ticker = document.getElementById('tickerInput').value;
  const analysis = await tracker.analyzeTicker(ticker);
  console.log(analysis);
  // Mostrar resultados en la UI
});
```

---

## Casos de Uso Reales

### Caso 1: Monitoreo de Portafolio

**Objetivo:** Analizar múltiples activos de un portafolio

```python
import pandas as pd
from financial_tracker_client import FinancialTrackerClient

# Portafolio actual
portfolio = {
    'AAPL': 10,  # 10 acciones
    'MSFT': 15,
    'GOOGL': 5,
    'TSLA': 8,
    'AMZN': 3
}

client = FinancialTrackerClient()
client.login("investor", "password123")

# Analizar cada ticker
results = []
for ticker, shares in portfolio.items():
    print(f"Analizando {ticker}...")
    analysis = client.analyze_ticker(ticker)

    results.append({
        'Ticker': ticker,
        'Acciones': shares,
        'Precio Actual': analysis['market_data']['precio_actual'],
        'Precio Predicho': analysis['prediction']['precio_predicho'],
        'Recomendación': analysis['recommendation']['accion'],
        'Confianza': analysis['recommendation']['confianza'],
        'Sentimiento': analysis['sentiment']['score']
    })

# Crear DataFrame
df = pd.DataFrame(results)
df['Valor Actual'] = df['Acciones'] * df['Precio Actual']
df['Valor Predicho'] = df['Acciones'] * df['Precio Predicho']
df['Ganancia Esperada'] = df['Valor Predicho'] - df['Valor Actual']

print("\n📊 Resumen del Portafolio:")
print(df.to_string(index=False))
print(f"\nValor Total Actual: ${df['Valor Actual'].sum():.2f}")
print(f"Valor Total Predicho: ${df['Valor Predicho'].sum():.2f}")
print(f"Ganancia Esperada: ${df['Ganancia Esperada'].sum():.2f}")
```

### Caso 2: Alertas Automáticas por Email

**Objetivo:** Enviar email cuando hay alertas críticas

```python
import smtplib
from email.mime.text import MIMEText
from financial_tracker_client import FinancialTrackerClient

def send_alert_email(alerts, to_email):
    """Enviar email con alertas críticas"""
    subject = f"🚨 {len(alerts)} Alertas Críticas en tu Portafolio"

    body = "Alertas críticas detectadas:\n\n"
    for alert in alerts:
        body += f"⚠️ {alert['ticker']}: {alert['mensaje']}\n"
        body += f"   Variación: {alert['variacion_pct']:.2f}%\n"
        body += f"   Precio: ${alert['precio_actual']}\n\n"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'alerts@financialtracker.com'
    msg['To'] = to_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your_email@gmail.com', 'your_app_password')
        server.send_message(msg)

# Script principal
client = FinancialTrackerClient()
client.login("investor", "password123")

# Obtener alertas
alerts_data = client.get_alerts()
critical_alerts = [
    a for a in alerts_data['alertas']
    if a['tipo'] == 'critical' and not a['leida']
]

if critical_alerts:
    print(f"⚠️  {len(critical_alerts)} alertas críticas encontradas")
    send_alert_email(critical_alerts, "investor@example.com")
    print("✅ Email enviado")

    # Marcar como leídas
    for alert in critical_alerts:
        client.mark_alert_read(alert['id'])
```

### Caso 3: Screener de Oportunidades

**Objetivo:** Encontrar las mejores oportunidades de compra

```python
from financial_tracker_client import FinancialTrackerClient
import time

# Lista de tickers a analizar
tickers = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
    'META', 'NVDA', 'AMD', 'NFLX', 'DIS'
]

client = FinancialTrackerClient()
client.login("trader", "password123")

opportunities = []

for ticker in tickers:
    try:
        print(f"Analizando {ticker}...", end=" ")
        analysis = client.analyze_ticker(ticker)

        rec = analysis['recommendation']

        # Filtrar solo compras con alta confianza
        if rec['accion'] in ['compra', 'compra_fuerte'] and rec['confianza'] > 0.75:
            opportunities.append({
                'Ticker': ticker,
                'Acción': rec['accion'].upper(),
                'Confianza': f"{rec['confianza']*100:.1f}%",
                'Precio': f"${analysis['market_data']['precio_actual']:.2f}",
                'Predicción': f"${analysis['prediction']['precio_predicho']:.2f}",
                'Upside': f"{((analysis['prediction']['precio_predicho'] / analysis['market_data']['precio_actual']) - 1) * 100:.1f}%",
                'Score': rec['score_total']
            })
            print("✅ Oportunidad!")
        else:
            print("⏭️  Skip")

        time.sleep(2)  # Rate limiting

    except Exception as e:
        print(f"❌ Error: {e}")

# Ordenar por score
opportunities.sort(key=lambda x: x['Score'], reverse=True)

print("\n🎯 Top Oportunidades de Compra:")
print("=" * 80)
for opp in opportunities:
    print(f"{opp['Ticker']:6} | {opp['Acción']:15} | Conf: {opp['Confianza']:6} | "
          f"Precio: {opp['Precio']:8} | Target: {opp['Predicción']:8} | Upside: {opp['Upside']:7}")
```

---

## Scripts de Automatización

### Script de Monitoreo Continuo

```bash
#!/bin/bash
# monitor_portfolio.sh
# Ejecutar cada hora: */60 * * * * /path/to/monitor_portfolio.sh

PORTFOLIO="AAPL MSFT GOOGL TSLA AMZN"
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -d "username=trader&password=password123" \
  | jq -r '.access_token')

for TICKER in $PORTFOLIO; do
  echo "Analizando $TICKER..."

  curl -s -X GET "http://localhost:8000/predict/$TICKER" \
    -H "Authorization: Bearer $TOKEN" \
    | jq '{
        ticker: .ticker,
        precio: .market_data.precio_actual,
        recomendacion: .recommendation.accion,
        confianza: .recommendation.confianza
      }'

  sleep 5
done

# Verificar alertas
ALERTS=$(curl -s -X GET "http://localhost:8000/alerts" \
  -H "Authorization: Bearer $TOKEN" \
  | jq '.alertas | length')

if [ "$ALERTS" -gt 0 ]; then
  echo "⚠️  Tienes $ALERTS alertas nuevas"
fi
```

### Cronjob para Análisis Diario

```bash
# Editar crontab
crontab -e

# Agregar línea para ejecutar a las 9 AM todos los días
0 9 * * * cd /path/to/proyecto_final && python scripts/daily_analysis.py
```

**daily_analysis.py:**
```python
#!/usr/bin/env python3
import sys
sys.path.append('/path/to/proyecto_final')

from financial_tracker_client import FinancialTrackerClient
import logging

logging.basicConfig(
    filename='/var/log/financial_tracker_daily.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

portfolio = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']
client = FinancialTrackerClient()
client.login('trader', 'password123')

for ticker in portfolio:
    try:
        analysis = client.analyze_ticker(ticker)
        logging.info(f"{ticker}: {analysis['recommendation']['accion']} "
                    f"(confianza: {analysis['recommendation']['confianza']:.2f})")
    except Exception as e:
        logging.error(f"Error analizando {ticker}: {e}")
```

---

## Tips y Mejores Prácticas

### 1. Rate Limiting
```python
import time

# Esperar entre requests para evitar sobrecargar
for ticker in tickers:
    analysis = client.analyze_ticker(ticker)
    time.sleep(5)  # 5 segundos entre cada análisis
```

### 2. Manejo de Errores
```python
import requests
from requests.exceptions import RequestException, Timeout

try:
    analysis = client.analyze_ticker('AAPL')
except Timeout:
    print("⏱️  Timeout - el análisis tardó demasiado")
except RequestException as e:
    print(f"❌ Error de red: {e}")
except Exception as e:
    print(f"❌ Error inesperado: {e}")
```

### 3. Cache Local
```python
import json
from pathlib import Path
import time

CACHE_FILE = Path("analysis_cache.json")
CACHE_TTL = 300  # 5 minutos

def get_cached_analysis(ticker):
    if not CACHE_FILE.exists():
        return None

    with open(CACHE_FILE) as f:
        cache = json.load(f)

    if ticker in cache:
        if time.time() - cache[ticker]['timestamp'] < CACHE_TTL:
            return cache[ticker]['data']

    return None

def set_cached_analysis(ticker, data):
    cache = {}
    if CACHE_FILE.exists():
        with open(CACHE_FILE) as f:
            cache = json.load(f)

    cache[ticker] = {
        'timestamp': time.time(),
        'data': data
    }

    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

# Uso
analysis = get_cached_analysis('AAPL')
if not analysis:
    analysis = client.analyze_ticker('AAPL')
    set_cached_analysis('AAPL', analysis)
```

---

Para más información, consulta:
- [README.md](README.md) - Documentación principal
- [CONFIGURATION.md](CONFIGURATION.md) - Configuración avanzada
- API Docs: http://localhost:8000/docs
