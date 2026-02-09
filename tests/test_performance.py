"""
Pruebas de carga y rendimiento del sistema
"""

import sys
import io
import requests
import time
import concurrent.futures
from statistics import mean, stdev
import json
from datetime import datetime

# Fix encoding for Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class PerformanceTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token = None

    def authenticate(self):
        """Obtener token de autenticación"""
        response = requests.post(
            f"{self.base_url}/auth/login",
            data={"username": "admin", "password": "admin123"}
        )
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            return True
        return False

    def single_request(self, ticker: str) -> dict:
        """Ejecuta una sola request y mide el tiempo"""
        headers = {"Authorization": f"Bearer {self.token}"}
        start = time.time()

        try:
            response = requests.get(
                f"{self.base_url}/predict/{ticker}",
                headers=headers,
                timeout=30
            )
            latency = time.time() - start

            return {
                "success": response.status_code == 200,
                "latency": latency,
                "status_code": response.status_code
            }
        except Exception as e:
            return {
                "success": False,
                "latency": time.time() - start,
                "error": str(e)
            }

    def concurrent_load_test(self, ticker: str, num_users: int):
        """Simula múltiples usuarios concurrentes"""
        print(f"\n⚡ Prueba de carga: {num_users} usuarios concurrentes")
        print(f"   Ticker: {ticker}")

        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_users) as executor:
            futures = [executor.submit(self.single_request, ticker) for _ in range(num_users)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        total_time = time.time() - start_time

        # Calcular estadísticas
        successes = [r for r in results if r["success"]]
        failures = [r for r in results if not r["success"]]
        latencies = [r["latency"] for r in successes]

        stats = {
            "concurrent_users": num_users,
            "total_requests": len(results),
            "successful": len(successes),
            "failed": len(failures),
            "success_rate": len(successes) / len(results) * 100,
            "total_time_seconds": round(total_time, 2),
            "requests_per_second": round(len(results) / total_time, 2),
        }

        if latencies:
            stats.update({
                "avg_latency_ms": round(mean(latencies) * 1000, 2),
                "min_latency_ms": round(min(latencies) * 1000, 2),
                "max_latency_ms": round(max(latencies) * 1000, 2),
                "stdev_latency_ms": round(stdev(latencies) * 1000, 2) if len(latencies) > 1 else 0
            })

        # Imprimir resultados
        print(f"   ✅ Éxitos: {stats['successful']}/{stats['total_requests']} ({stats['success_rate']:.1f}%)")
        if latencies:
            print(f"   ⏱️  Latencia promedio: {stats['avg_latency_ms']:.0f}ms")
            print(f"   📊 Min/Max: {stats['min_latency_ms']:.0f}ms / {stats['max_latency_ms']:.0f}ms")
        print(f"   🚀 Throughput: {stats['requests_per_second']:.1f} req/s")

        return stats

    def run_load_tests(self, ticker: str = "AAPL"):
        """Ejecuta pruebas con diferentes niveles de carga"""
        print(f"\n{'='*60}")
        print(f"🔥 PRUEBAS DE CARGA Y RENDIMIENTO")
        print(f"{'='*60}")

        if not self.authenticate():
            print("❌ Error de autenticación")
            return None

        user_levels = [1, 5, 10, 25, 50]
        results = []

        for num_users in user_levels:
            result = self.concurrent_load_test(ticker, num_users)
            results.append(result)
            time.sleep(2)  # Pausa entre tests

        return results

    def save_results(self, results, output_dir="test_results"):
        """Guardar resultados"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/performance_test_{timestamp}.json"

        with open(filename, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\n💾 Resultados guardados en: {filename}")
        return filename


def main():
    tester = PerformanceTester()
    results = tester.run_load_tests(ticker="AAPL")

    if results:
        tester.save_results(results)

        print(f"\n{'='*60}")
        print("📊 RESUMEN DE RENDIMIENTO")
        print(f"{'='*60}")
        print(f"{'Usuarios':<12} {'Req/s':<12} {'Lat. (ms)':<12} {'Éxito %':<12}")
        print(f"{'-'*60}")

        for r in results:
            print(f"{r['concurrent_users']:<12} "
                  f"{r['requests_per_second']:<12.1f} "
                  f"{r.get('avg_latency_ms', 0):<12.0f} "
                  f"{r['success_rate']:<12.1f}")


if __name__ == "__main__":
    main()
