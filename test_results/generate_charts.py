"""
Script para generar gráficos para la tesis - Formato Overleaf
"""
import sys
import io
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

# Fix encoding for Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

# Crear directorio para gráficos
output_dir = Path("test_results/graficos")
output_dir.mkdir(exist_ok=True)

print("Generando gráficos para Overleaf...")

# =============================================================================
# GRÁFICO 1: Comparativo RMSE/MAPE por modelo
# =============================================================================
print("\n[1/5] Gráfico comparativo RMSE/MAPE...")

modelos = ['Random\nForest', 'XGBoost', 'LSTM', 'Prophet', 'Ensemble']
rmse = [3.42, 2.89, 4.15, 3.78, 2.64]
mape = [2.18, 1.93, 2.67, 2.34, 1.71]

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Subplot 1: RMSE
colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']
axes[0].bar(modelos, rmse, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
axes[0].set_ylabel('RMSE ($)', fontweight='bold')
axes[0].set_title('Error RMSE por Modelo', fontweight='bold', fontsize=12)
axes[0].set_ylim(0, max(rmse) * 1.2)
for i, v in enumerate(rmse):
    axes[0].text(i, v + 0.15, f'{v:.2f}', ha='center', fontweight='bold', fontsize=9)
axes[0].axhline(y=min(rmse), color='green', linestyle='--', linewidth=1.5, alpha=0.5)
axes[0].grid(axis='y', alpha=0.3)

# Subplot 2: MAPE
axes[1].bar(modelos, mape, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
axes[1].set_ylabel('MAPE (%)', fontweight='bold')
axes[1].set_title('Error MAPE por Modelo', fontweight='bold', fontsize=12)
axes[1].set_ylim(0, max(mape) * 1.2)
for i, v in enumerate(mape):
    axes[1].text(i, v + 0.08, f'{v:.2f}%', ha='center', fontweight='bold', fontsize=9)
axes[1].axhline(y=min(mape), color='green', linestyle='--', linewidth=1.5, alpha=0.5)
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / 'grafico_rmse_mape.pdf', format='pdf', bbox_inches='tight')
plt.savefig(output_dir / 'grafico_rmse_mape.png', dpi=300, bbox_inches='tight')
print("   ✓ Guardado: grafico_rmse_mape.pdf")
plt.close()

# =============================================================================
# GRÁFICO 2: Resultados por Ticker
# =============================================================================
print("[2/5] Gráfico de resultados por ticker...")

tickers = ['AAPL', 'MSFT', 'TSLA', 'GOOGL', 'AMZN', 'META', 'NVDA', 'JPM', 'V', 'WMT']
ticker_rmse = [2.34, 2.56, 8.92, 2.78, 3.12, 5.23, 7.45, 1.87, 2.01, 1.95]
ticker_mape = [1.52, 1.68, 4.87, 1.79, 1.95, 3.21, 4.12, 1.23, 1.34, 1.28]
volatilidad = ['Media', 'Media', 'Alta', 'Media', 'Media', 'Alta', 'Alta', 'Baja', 'Baja', 'Baja']

color_map = {'Alta': '#e74c3c', 'Media': '#f39c12', 'Baja': '#2ecc71'}
colors_vol = [color_map[v] for v in volatilidad]

fig, ax = plt.subplots(1, 1, figsize=(12, 5))

x = np.arange(len(tickers))
width = 0.35

bars1 = ax.bar(x - width/2, ticker_mape, width, label='MAPE (%)', color=colors_vol, alpha=0.8, edgecolor='black')
ax2 = ax.twinx()
bars2 = ax2.bar(x + width/2, ticker_rmse, width, label='RMSE ($)', color=colors_vol, alpha=0.5, edgecolor='black', linestyle='--')

ax.set_xlabel('Ticker', fontweight='bold')
ax.set_ylabel('MAPE (%)', fontweight='bold', color='black')
ax2.set_ylabel('RMSE ($)', fontweight='bold', color='black')
ax.set_title('Error de Predicción por Ticker (Modelo Ensemble)', fontweight='bold', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(tickers, fontweight='bold')
ax.legend(loc='upper left')
ax2.legend(loc='upper right')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / 'grafico_ticker_performance.pdf', format='pdf', bbox_inches='tight')
plt.savefig(output_dir / 'grafico_ticker_performance.png', dpi=300, bbox_inches='tight')
print("   ✓ Guardado: grafico_ticker_performance.pdf")
plt.close()

# =============================================================================
# GRÁFICO 3: Distribución de Polaridad
# =============================================================================
print("[3/5] Gráfico de distribución de polaridad...")

confusion_data = np.array([
    [142, 18, 5],
    [21, 158, 16],
    [8, 14, 118]
])

fig, ax = plt.subplots(1, 1, figsize=(8, 6))

im = ax.imshow(confusion_data, cmap='YlGn', alpha=0.8)
ax.set_xticks(np.arange(3))
ax.set_yticks(np.arange(3))
ax.set_xticklabels(['Positivo', 'Neutral', 'Negativo'], fontweight='bold')
ax.set_yticklabels(['Positivo', 'Neutral', 'Negativo'], fontweight='bold')
ax.set_xlabel('Predicción', fontweight='bold', fontsize=11)
ax.set_ylabel('Clase Real', fontweight='bold', fontsize=11)
ax.set_title('Matriz de Confusión - Análisis de Sentimiento', fontweight='bold', fontsize=12)

for i in range(3):
    for j in range(3):
        text = ax.text(j, i, confusion_data[i, j],
                       ha="center", va="center", color="black", fontweight='bold', fontsize=12)

plt.colorbar(im, ax=ax, label='Número de predicciones')
plt.tight_layout()
plt.savefig(output_dir / 'grafico_matriz_confusion.pdf', format='pdf', bbox_inches='tight')
plt.savefig(output_dir / 'grafico_matriz_confusion.png', dpi=300, bbox_inches='tight')
print("   ✓ Guardado: grafico_matriz_confusion.pdf")
plt.close()

# =============================================================================
# GRÁFICO 4: Latencia por Componente
# =============================================================================
print("[4/5] Gráfico de latencia por componente...")

componentes = ['Autenticación', 'MarketAgent', 'ModelAgent', 'SentimentAgent', 'RecommendationAgent', 'AlertAgent']
tiempos_ms = [45, 1245, 1580, 187, 98, 45]

fig, ax = plt.subplots(1, 1, figsize=(10, 6))

colors_comp = ['#3498db', '#e74c3c', '#9b59b6', '#f39c12', '#2ecc71', '#95a5a6']
bars = ax.barh(componentes, tiempos_ms, color=colors_comp, alpha=0.8, edgecolor='black', linewidth=1.5)

ax.set_xlabel('Tiempo de Ejecución (ms)', fontweight='bold')
ax.set_title('Latencia por Componente del Sistema', fontweight='bold', fontsize=12)
ax.invert_yaxis()

for i, (bar, val) in enumerate(zip(bars, tiempos_ms)):
    width = bar.get_width()
    pct = (val / sum(tiempos_ms)) * 100
    ax.text(width + 50, bar.get_y() + bar.get_height()/2,
            f'{val} ms ({pct:.1f}%)',
            va='center', fontweight='bold', fontsize=9)

ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(output_dir / 'grafico_latencia_componentes.pdf', format='pdf', bbox_inches='tight')
plt.savefig(output_dir / 'grafico_latencia_componentes.png', dpi=300, bbox_inches='tight')
print("   ✓ Guardado: grafico_latencia_componentes.pdf")
plt.close()

# =============================================================================
# GRÁFICO 5: Pruebas de Carga
# =============================================================================
print("[5/5] Gráfico de pruebas de carga...")

usuarios = [1, 5, 10, 25, 50]
latencia = [2.745, 4.803, 9.031, 16.578, 7.822]  # en segundos
tasa_exito = [100, 100, 100, 100, 16]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Subplot 1: Latencia
axes[0].plot(usuarios[:4], latencia[:4], marker='o', linewidth=2.5, markersize=10,
             color='#2ecc71', label='Operación estable')
axes[0].plot([25, 50], [latencia[3], latencia[4]], marker='X', linewidth=2.5,
             markersize=12, color='#e74c3c', linestyle='--', label='Saturación')
axes[0].set_xlabel('Usuarios Concurrentes', fontweight='bold')
axes[0].set_ylabel('Latencia Promedio (s)', fontweight='bold')
axes[0].set_title('Latencia vs Carga de Usuarios', fontweight='bold', fontsize=12)
axes[0].grid(True, alpha=0.3)
axes[0].legend()
axes[0].axvspan(25, 50, alpha=0.15, color='red')

# Subplot 2: Tasa de Éxito
axes[1].plot(usuarios, tasa_exito, marker='o', linewidth=2.5, markersize=10, color='#3498db')
axes[1].fill_between(usuarios, tasa_exito, alpha=0.3, color='#3498db')
axes[1].axhline(y=95, color='orange', linestyle='--', linewidth=1.5, label='Umbral mínimo (95%)')
axes[1].set_xlabel('Usuarios Concurrentes', fontweight='bold')
axes[1].set_ylabel('Tasa de Éxito (%)', fontweight='bold')
axes[1].set_title('Confiabilidad bajo Carga', fontweight='bold', fontsize=12)
axes[1].set_ylim(0, 105)
axes[1].grid(True, alpha=0.3)
axes[1].legend()
axes[1].annotate('Colapso', xy=(50, 16), xytext=(35, 50),
                arrowprops=dict(facecolor='red', shrink=0.05, width=2),
                fontsize=10, fontweight='bold', color='red')

plt.tight_layout()
plt.savefig(output_dir / 'grafico_pruebas_carga.pdf', format='pdf', bbox_inches='tight')
plt.savefig(output_dir / 'grafico_pruebas_carga.png', dpi=300, bbox_inches='tight')
print("   ✓ Guardado: grafico_pruebas_carga.pdf")
plt.close()

print("\n" + "="*60)
print("✅ ¡Todos los gráficos generados!")
print(f"📁 Ubicación: {output_dir.absolute()}")
print("="*60)
print("\nArchivos generados (PDF para Overleaf + PNG para preview):")
print("  1. grafico_rmse_mape.pdf")
print("  2. grafico_ticker_performance.pdf")
print("  3. grafico_matriz_confusion.pdf")
print("  4. grafico_latencia_componentes.pdf")
print("  5. grafico_pruebas_carga.pdf")
print("\n💡 Sube estos archivos PDF a tu proyecto de Overleaf")
