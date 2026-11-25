"""Resume resultados del experimento y genera los gráficos requeridos.

Uso: python analizar_resultados.py resultados/resultados.csv
Requiere matplotlib solo para los PNG; el resumen estadístico usa biblioteca
estándar. Se excluyen las filas dedicadas a medir memoria del análisis de tiempo.
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
import statistics

# Valores críticos de Student bilateral para un IC del 95 % (gl = n - 1).
T95 = {2: 12.706, 3: 4.303, 4: 3.182, 5: 2.776, 6: 2.571, 7: 2.447,
       8: 2.365, 9: 2.306, 10: 2.262, 11: 2.228, 12: 2.201, 13: 2.179,
       14: 2.160, 15: 2.145, 16: 2.131, 17: 2.120, 18: 2.110,
       19: 2.101, 20: 2.093, 21: 2.086, 22: 2.080, 23: 2.074,
       24: 2.069, 25: 2.064, 26: 2.060, 27: 2.056, 28: 2.052,
       29: 2.048, 30: 2.045}


def media_ic95(valores: list[float]) -> tuple[float, float, float, float]:
    n = len(valores)
    media = statistics.mean(valores)
    sd = statistics.stdev(valores) if n > 1 else 0.0
    cv = sd / media * 100 if media else 0.0
    t_critico = T95.get(n, 1.96) if n > 1 else 0.0
    margen = t_critico * sd / math.sqrt(n) if n > 1 else 0.0
    return media, sd, cv, margen


def cargar(ruta: Path):
    grupos: dict[tuple[str, int], list[float]] = defaultdict(list)
    with ruta.open(newline="", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            if fila.get("medicion_memoria", "no").lower() == "si":
                continue
            try:
                grupos[(fila["estrategia"], int(fila["n"]))].append(float(fila["tiempo_s"]))
            except (KeyError, ValueError):
                continue
    return grupos


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("csv", type=Path)
    p.add_argument("--salida", type=Path, default=Path("resultados"))
    a = p.parse_args()
    grupos = cargar(a.csv)
    if not grupos:
        raise SystemExit("No hay mediciones de tiempo válidas en el CSV.")
    a.salida.mkdir(parents=True, exist_ok=True)

    resumen = a.salida / "resumen_estadistico.csv"
    with resumen.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["estrategia", "n", "repeticiones", "media_s", "mediana_s", "sd_s", "cv_pct", "ic95_inf_s", "ic95_sup_s"])
        for (estrategia, n), vals in sorted(grupos.items(), key=lambda x: (x[0][1], x[0][0])):
            media, sd, cv, margen = media_ic95(vals)
            w.writerow([estrategia, n, len(vals), f"{media:.8f}", f"{statistics.median(vals):.8f}", f"{sd:.8f}", f"{cv:.3f}", f"{media-margen:.8f}", f"{media+margen:.8f}"])

    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise SystemExit(f"Resumen guardado en {resumen}; instala matplotlib para los gráficos: {e}")

    estrategias = sorted({e for e, _ in grupos})
    ns = sorted({n for _, n in grupos})
    fig, ax = plt.subplots()
    for estrategia in estrategias:
        xs, ys, es = [], [], []
        for n in ns:
            vals = grupos.get((estrategia, n))
            if vals:
                media, _, _, margen = media_ic95(vals)
                xs.append(n); ys.append(media); es.append(margen)
        if xs:
            ax.errorbar(xs, ys, yerr=es, marker="o", capsize=3, label=estrategia)
    ax.set(xscale="log", yscale="log", xlabel="Número de solicitudes, n (solicitudes)", ylabel="Tiempo de ejecución (s)", title="Tiempo de ejecución por tamaño de entrada")
    ax.grid(True, which="both", alpha=.25); ax.legend(); fig.tight_layout()
    fig.savefig(a.salida / "tiempo_vs_n.png", dpi=160); plt.close(fig)

    nmax = max(ns)
    nombres = [e for e in estrategias if (e, nmax) in grupos]
    medias = [media_ic95(grupos[(e, nmax)])[0] for e in nombres]
    errores = [media_ic95(grupos[(e, nmax)])[3] for e in nombres]
    fig, ax = plt.subplots()
    posiciones = list(range(len(nombres)))
    ax.errorbar(medias, posiciones, xerr=errores, fmt="o", capsize=5, markersize=7)
    ax.set_xscale("log")
    ax.set_yticks(posiciones, nombres)
    ax.set(xlabel="Tiempo de ejecución medio (s, escala logarítmica)", title=f"Tiempo por estrategia para n = {nmax} solicitudes")
    for y, media in zip(posiciones, medias):
        ax.annotate(f"{media:.4g} s", (media, y), xytext=(8, 0), textcoords="offset points", va="center")
    ax.grid(True, axis="x", which="both", alpha=.25); fig.tight_layout()
    fig.savefig(a.salida / "comparacion_n_mayor.png", dpi=160); plt.close(fig)
    print(f"Resumen: {resumen}\nGráficos: {a.salida / 'tiempo_vs_n.png'}, {a.salida / 'comparacion_n_mayor.png'}")


if __name__ == "__main__":
    main()
