"""
Test funcional completo del sistema multiagente
Genera métricas reales de funcionamiento
"""

import sys
import io
import requests
import time
import json
from datetime import datetime
from typing import Dict, List
import pandas as pd
from collections import defaultdict

# Fix encoding for Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class SystemTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token = None
        self.results = defaultdict(list)

    def authenticate(self, username: str = "admin", password: str = "admin123"):
        """Autenticación y obtención de token"""
        print("🔐 Autenticando usuario...")
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                data={"username": username, "password": password}
            )
            if response.status_code == 200:
                self.token = response.json()["access_token"]
                print("✅ Autenticación exitosa")
                return True
            else:
                print(f"❌ Error de autenticación: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False

    def test_agent_functionality(self, ticker: str) -> Dict:
        """Prueba funcional de un ticker completo (todos los agentes)"""
        print(f"\n📊 Probando ticker: {ticker}")

        headers = {"Authorization": f"Bearer {self.token}"}
        start_time = time.time()

        try:
            response = requests.get(
                f"{self.base_url}/predict/{ticker}",
                headers=headers,
                timeout=30
            )
            latency = time.time() - start_time

            result = {
                "ticker": ticker,
                "timestamp": datetime.now().isoformat(),
                "status_code": response.status_code,
                "latency_seconds": round(latency, 3),
                "success": response.status_code == 200,
            }

            if response.status_code == 200:
                data = response.json()

                # Extraer datos con nombres en español (API actualizada)
                prediccion = data.get("prediccion", {})
                metricas = prediccion.get("metricas", {})
                sentimiento = data.get("sentimiento", {})
                recomendacion = data.get("recomendacion", {})

                result.update({
                    # Validación de agentes (nombres en español)
                    "market_agent_ok": "mercado" in data,
                    "model_agent_ok": "prediccion" in data,
                    "sentiment_agent_ok": "sentimiento" in data,
                    "recommendation_agent_ok": "recomendacion" in data,
                    "alert_agent_ok": "alerta" in data,

                    # Datos de predicción
                    "prediction_value": prediccion.get("precio_predicho"),
                    "variacion_pct": prediccion.get("variacion_pct"),
                    "modelo": prediccion.get("modelo"),

                    # Métricas de CLASIFICACIÓN (nuevas)
                    "accuracy": metricas.get("accuracy"),
                    "precision": metricas.get("precision"),
                    "recall": metricas.get("recall"),
                    "f1_score": metricas.get("f1"),
                    "auc": metricas.get("auc"),

                    # Métricas legacy (compatibilidad)
                    "rmse": metricas.get("rmse"),
                    "mape": metricas.get("mape"),

                    # Sentimiento y recomendación
                    "sentiment_score": sentimiento.get("score"),
                    "sentimiento": sentimiento.get("sentimiento"),
                    "recommendation": recomendacion.get("recomendacion"),
                    "recommendation_tipo": recomendacion.get("tipo"),
                    "recommendation_confianza": recomendacion.get("confianza"),
                })

                # Mostrar métricas de clasificación si existen
                if metricas.get("accuracy") is not None:
                    print(f"  ✅ Éxito - Latencia: {latency:.2f}s | Accuracy: {metricas.get('accuracy', 0):.1%} | Precision: {metricas.get('precision', 0):.1%}")
                else:
                    print(f"  ✅ Éxito - Latencia: {latency:.2f}s")
            else:
                print(f"  ❌ Error {response.status_code}")
                result["error_message"] = response.text[:200]

        except requests.Timeout:
            result = {
                "ticker": ticker,
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error_type": "timeout",
                "latency_seconds": 30.0
            }
            print(f"  ⏱️ Timeout después de 30s")

        except Exception as e:
            result = {
                "ticker": ticker,
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error_type": type(e).__name__,
                "error_message": str(e)[:200]
            }
            print(f"  ❌ Excepción: {e}")

        self.results["functional_tests"].append(result)
        return result

    def test_multiple_tickers(self, tickers: List[str], iterations: int = 1):
        """Ejecuta pruebas sobre múltiples tickers"""
        print(f"\n{'='*60}")
        print(f"🧪 PRUEBAS FUNCIONALES - {len(tickers)} tickers × {iterations} iteraciones")
        print(f"{'='*60}")

        total_tests = len(tickers) * iterations
        current = 0

        for iteration in range(iterations):
            if iterations > 1:
                print(f"\n🔄 Iteración {iteration + 1}/{iterations}")

            for ticker in tickers:
                current += 1
                print(f"[{current}/{total_tests}]", end=" ")
                self.test_agent_functionality(ticker)
                time.sleep(0.5)  # Pequeña pausa entre requests

    def test_alerts_endpoint(self):
        """Prueba el endpoint de alertas"""
        print(f"\n🚨 Probando endpoint de alertas...")

        headers = {"Authorization": f"Bearer {self.token}"}
        start_time = time.time()

        try:
            response = requests.get(
                f"{self.base_url}/alerts/",
                headers=headers,
                timeout=10
            )
            latency = time.time() - start_time

            result = {
                "endpoint": "/alerts/",
                "status_code": response.status_code,
                "latency_seconds": round(latency, 3),
                "success": response.status_code == 200
            }

            if response.status_code == 200:
                data = response.json()
                result["total_alerts"] = data.get("total", 0)
                alerts = data.get("alertas", [])

                # Contar por tipo
                alert_types = defaultdict(int)
                for alert in alerts:
                    alert_types[alert.get("tipo", "unknown")] += 1

                result["alert_distribution"] = dict(alert_types)
                print(f"  ✅ {result['total_alerts']} alertas encontradas")
                print(f"     Distribución: {dict(alert_types)}")
            else:
                print(f"  ❌ Error {response.status_code}")

            self.results["endpoint_tests"].append(result)
            return result

        except Exception as e:
            print(f"  ❌ Error: {e}")
            return None

    def generate_summary(self) -> Dict:
        """Genera resumen de todas las pruebas"""
        functional = self.results["functional_tests"]

        if not functional:
            return {"error": "No hay datos de pruebas"}

        df = pd.DataFrame(functional)

        summary = {
            "total_tests": len(df),
            "successful": int(df["success"].sum()),
            "failed": int((~df["success"]).sum()),
            "success_rate": round(df["success"].mean() * 100, 2),
            "avg_latency": round(df[df["success"]]["latency_seconds"].mean(), 3),
            "max_latency": round(df[df["success"]]["latency_seconds"].max(), 3),
            "min_latency": round(df[df["success"]]["latency_seconds"].min(), 3),
        }

        # Éxito por agente
        if "market_agent_ok" in df.columns:
            agent_stats = {}
            for agent in ["market", "model", "sentiment", "recommendation", "alert"]:
                col = f"{agent}_agent_ok"
                if col in df.columns:
                    total = df[col].notna().sum()
                    success = df[col].sum()
                    agent_stats[f"{agent}_agent"] = {
                        "tests": int(total),
                        "success": int(success),
                        "rate": round(success / total * 100, 1) if total > 0 else 0
                    }
            summary["agent_performance"] = agent_stats

        # Métricas de clasificación (si existen)
        metrics_cols = ["accuracy", "precision", "recall", "f1_score", "auc"]
        available_metrics = [col for col in metrics_cols if col in df.columns]

        if available_metrics:
            successful_tests = df[df["success"]]
            metrics_summary = {}
            for metric in available_metrics:
                values = successful_tests[metric].dropna()
                if len(values) > 0:
                    metrics_summary[metric] = {
                        "promedio": round(values.mean(), 4),
                        "min": round(values.min(), 4),
                        "max": round(values.max(), 4),
                        "std": round(values.std(), 4) if len(values) > 1 else 0
                    }
            if metrics_summary:
                summary["metricas_clasificacion"] = metrics_summary

        # Errores más comunes
        errors = df[~df["success"]]
        if len(errors) > 0:
            error_counts = errors.get("error_type", pd.Series()).value_counts()
            summary["error_types"] = error_counts.to_dict()

        return summary

    def save_results(self, output_dir: str = "test_results"):
        """Guarda resultados en archivos JSON y CSV"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Guardar JSON completo
        json_file = f"{output_dir}/functional_test_{timestamp}.json"
        with open(json_file, "w") as f:
            json.dump(dict(self.results), f, indent=2)
        print(f"\n💾 Resultados JSON guardados en: {json_file}")

        # Guardar CSV para análisis
        if self.results["functional_tests"]:
            df = pd.DataFrame(self.results["functional_tests"])
            csv_file = f"{output_dir}/functional_test_{timestamp}.csv"
            df.to_csv(csv_file, index=False)
            print(f"💾 Resultados CSV guardados en: {csv_file}")

        # Guardar resumen
        summary = self.generate_summary()
        summary_file = f"{output_dir}/summary_{timestamp}.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)
        print(f"💾 Resumen guardado en: {summary_file}")

        return json_file, summary_file

    def print_summary_table(self):
        """Imprime tabla resumen en consola"""
        summary = self.generate_summary()

        print(f"\n{'='*60}")
        print(f"📊 RESUMEN DE PRUEBAS FUNCIONALES")
        print(f"{'='*60}")
        print(f"Total de pruebas:     {summary['total_tests']}")
        print(f"Exitosas:             {summary['successful']} ({summary['success_rate']}%)")
        print(f"Fallidas:             {summary['failed']}")
        print(f"Latencia promedio:    {summary['avg_latency']}s")
        print(f"Latencia mínima:      {summary['min_latency']}s")
        print(f"Latencia máxima:      {summary['max_latency']}s")

        if "agent_performance" in summary:
            print(f"\n📊 Rendimiento por Agente:")
            print(f"{'Agente':<25} {'Pruebas':<10} {'Éxitos':<10} {'Tasa':<10}")
            print(f"{'-'*60}")
            for agent, stats in summary["agent_performance"].items():
                print(f"{agent:<25} {stats['tests']:<10} {stats['success']:<10} {stats['rate']}%")

        if "metricas_clasificacion" in summary:
            print(f"\n🎯 Métricas de Clasificación del Modelo:")
            print(f"{'Métrica':<15} {'Promedio':<12} {'Mín':<12} {'Máx':<12} {'Std':<12}")
            print(f"{'-'*60}")
            for metric, stats in summary["metricas_clasificacion"].items():
                metric_name = metric.upper().replace("_", " ")
                print(f"{metric_name:<15} {stats['promedio']:<12.2%} {stats['min']:<12.2%} {stats['max']:<12.2%} {stats['std']:<12.4f}")

        if "error_types" in summary:
            print(f"\n❌ Tipos de errores encontrados:")
            for error_type, count in summary["error_types"].items():
                print(f"  - {error_type}: {count}")


def main():
    """Función principal de ejecución"""

    # Tickers a probar (puedes agregar más)
    TICKERS = ["AAPL", "MSFT", "TSLA", "GOOGL", "AMZN", "META", "NVDA", "JPM", "V", "WMT"]

    # Configuración
    BASE_URL = "http://localhost:8000"
    ITERATIONS = 3  # Número de veces que se prueba cada ticker

    print(f"""
╔═══════════════════════════════════════════════════════════╗
║  🧪 SUITE DE PRUEBAS FUNCIONALES - SISTEMA MULTIAGENTE   ║
╚═══════════════════════════════════════════════════════════╝
    """)

    tester = SystemTester(base_url=BASE_URL)

    # 1. Autenticación
    if not tester.authenticate():
        print("\n❌ No se pudo autenticar. Verifica que el backend esté corriendo.")
        print("   Comando: uvicorn backend.main:app --reload")
        return

    # 2. Verificar que el servidor responde
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"✅ Servidor respondiendo: {response.status_code}")
    except Exception as e:
        print(f"\n❌ El servidor no está accesible: {e}")
        print("   Verifica que el backend esté corriendo en el puerto 8000")
        return

    # 3. Ejecutar pruebas funcionales
    tester.test_multiple_tickers(TICKERS, iterations=ITERATIONS)

    # 4. Probar endpoint de alertas
    tester.test_alerts_endpoint()

    # 5. Mostrar resumen
    tester.print_summary_table()

    # 6. Guardar resultados
    tester.save_results()

    print(f"\n✅ Pruebas completadas exitosamente!\n")


if __name__ == "__main__":
    main()
