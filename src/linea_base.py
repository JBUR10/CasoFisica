"""
Línea base — Equipo 5: Cálculo computacional intensivo.

Situación inicial: la plataforma de créditos calcula, para cada solicitud,
la cuota mensual fija y el TOTAL DE INTERESES del plan de pagos. El código
actual:
  * calcula (1 + i)^m multiplicando en un bucle (m multiplicaciones),
  * vuelve a calcularlo en CADA mes del plan,
  * repite todo aunque muchas solicitudes tienen la misma tasa y plazo.

Fórmula de la cuota (sistema francés):  C = P · i / (1 - (1 + i)^-m)
  P monto [COP], i tasa mensual [adimensional], m plazo [meses]

preparar(n) -> lista de n solicitudes (monto, tasa_mensual, plazo)
ejecutar(solicitudes) -> suma de intereses de todas las solicitudes [COP]
"""
import random
import time


def potencia_lenta(base: float, exponente: int) -> float:
    r = 1.0
    for _ in range(exponente):
        r *= base
    return r


def intereses_credito(monto: float, i: float, m: int) -> float:
    saldo, total_intereses = monto, 0.0
    for _ in range(m):
        cuota = monto * i / (1 - 1 / potencia_lenta(1 + i, m))   # se recalcula cada mes
        interes = saldo * i
        total_intereses += interes
        saldo -= cuota - interes
    return total_intereses


def preparar(n: int, semilla: int = 5):
    rng = random.Random(semilla)
    tasas = [0.009, 0.0125, 0.015, 0.018, 0.021]             # tasas mensuales del portafolio
    plazos = [12, 24, 36, 48, 60, 72]
    return [(rng.randrange(1, 200) * 500_000.0, rng.choice(tasas), rng.choice(plazos)) for _ in range(n)]


def ejecutar(solicitudes) -> float:
    return round(sum(intereses_credito(p, i, m) for p, i, m in solicitudes), 2)


if __name__ == "__main__":
    s = preparar(5_000)
    t0 = time.perf_counter()
    print(f"Intereses totales: {ejecutar(s):,.2f} COP")
    print(f"Tiempo: {time.perf_counter() - t0:.2f} s")
