"""Estrategia C: fórmula cerrada y reutilización del factor tasa–plazo.

El interés total del sistema francés es m por la cuota menos el capital.
El factor de cuota se memoiza porque el conjunto de entrada repite tasas y
plazos. La caché se limita a las combinaciones posibles del portafolio.
"""
from __future__ import annotations

from functools import lru_cache


@lru_cache(maxsize=256)
def _factor_cuota(i: float, m: int) -> float:
    return i / (1 - (1 + i) ** (-m))


def intereses_credito(monto: float, i: float, m: int) -> float:
    cuota = monto * _factor_cuota(i, m)
    return m * cuota - monto


def ejecutar(solicitudes) -> float:
    return round(sum(intereses_credito(p, i, m) for p, i, m in solicitudes), 2)
