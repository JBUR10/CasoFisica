"""Estrategia B: calcular una vez la cuota de cada solicitud.

Conserva la simulación mes a mes de la línea base, pero saca del bucle la
potencia y la cuota, que son invariantes durante el plan de pagos.
"""
from __future__ import annotations


def intereses_credito(monto: float, i: float, m: int) -> float:
    saldo = monto
    total_intereses = 0.0
    factor = (1 + i) ** m
    cuota = monto * i / (1 - 1 / factor)
    for _ in range(m):
        interes = saldo * i
        total_intereses += interes
        saldo -= cuota - interes
    return total_intereses


def ejecutar(solicitudes) -> float:
    return round(sum(intereses_credito(p, i, m) for p, i, m in solicitudes), 2)
