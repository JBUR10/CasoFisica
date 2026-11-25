# Equipo 5 — Cálculo computacional intensivo

> Proyecto: *Laboratorio colaborativo de rendimiento y eficiencia computacional desde la física aplicada*
> Física Aplicada al Desarrollo de Software · SENA · ADSO · 7.º trimestre

## 1. Problema empresarial
**Empresa (caso simulado):** FinanCréditos Cooperativa, simulador de créditos de libre inversión

El simulador de créditos recalcula planes de pago completos para miles de solicitudes al día y el servidor permanece al 100 % de CPU en horas pico.

## 2. Situación inicial medible
src/linea_base.py calcula potencias con bucles, recalcula la cuota cada mes y repite cálculos para combinaciones tasa–plazo idénticas.

| Medición preliminar (Clase 3) | Valor | Unidad |
|---|---:|---|
| n utilizado | 5.000 | solicitudes |
| Intereses totales | 93.103.574.568,94 | COP |
| Tiempo de ejecución (1 corrida) | 0,32 | s |
| Equipo y fecha | ASUS TUF Gaming A15 FA506NCG, Windows 11, CPython 3.13.15 · 25-11-2026 | — |

Comando ejecutado: `py -3.13 -m src.linea_base`. El tiempo aislado es evidencia preliminar y no se usa como comparación formal.

## 3. Pregunta de investigación
_¿Cómo cambia el tiempo de ejecución (s) cuando se cambia la estrategia de cálculo (A, B o C) y el número de solicitudes (2.000, 5.000 o 10.000), manteniendo iguales los datos de entrada por tamaño, el equipo y la versión de Python?_

## 4. Hipótesis
Ver [docs/hipotesis.md](docs/hipotesis.md).

## 5. Estrategias
| Id | Estrategia | Idea principal | Efecto físico esperado | Responsable |
|---|---|---|---|---|
| A | Línea base | (situación inicial) | — | R2 |
| B | Invariantes fuera del ciclo | Calcula una vez la potencia y cuota por solicitud; conserva el recorrido mensual | Menos operaciones repetidas y ciclos de CPU por solicitud | R3 (Integrante C) |
| C | Fórmula cerrada con caché | Calcula el interés total con `m·cuota − P` y reutiliza el factor para tasa–plazo | Evita el recorrido por mes y aprovecha combinaciones repetidas | R3 (Integrante C) |

## 6. Cómo reproducir
```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt                          # opcional: psutil, matplotlib
python -m src.linea_base                                 # situación inicial
python -m unittest discover -s pruebas                   # corrección
python -m experimentos.ejecutar_experimento              # experimento formal -> resultados/resultados.csv
python analizar_resultados.py resultados/resultados.csv
```

El análisis genera `resultados/resumen_estadistico.csv`, `tiempo_vs_n.png` y
`comparacion_n_mayor.png`. Los gráficos usan las corridas de tiempo, sin la
corrida separada de memoria.

La descripción de la referencia A y su costo computacional está en
[docs/linea_base.md](docs/linea_base.md). Las pruebas de R2 verifican B y C
contra A con tolerancia monetaria de `0,01 COP`.

## 7. Integrantes y roles
| Rol | Integrante | Responsabilidad principal |
|---|---|---|
| R1 — Coordinación y protocolo experimental | _(nombre)_ | Mantiene el protocolo y la bitácora de decisiones; controla variables; modera issues y la planeación. |
| R2 — Desarrollo de estrategia base | _(nombre)_ | Comprende y documenta la línea base; asegura la verificación de corrección (pruebas) de todas las estrategias. |
| R3 — Estrategias alternativas y optimización | _(nombre)_ | Diseña e implementa las estrategias alternativas y justifica físicamente por qué deberían cambiar las magnitudes. |
| R4 — Automatización de mediciones y análisis | _(nombre)_ | Automatiza experimentos y registro CSV; produce estadísticas y gráficos; documenta el entorno. |

Los roles son flexibles: **todos** participan en la comprensión física y en el código.

## 8. Documentación
- [Variables](docs/variables.md) · [Protocolo](docs/protocolo.md) · [Entorno](docs/entorno.md)
- [Decisiones técnicas](docs/decisiones.md) · [Uso de IA](docs/uso_ia.md) · [Informe](docs/informe.md)

## 9. Resultados y conclusiones (Clase 5)
El experimento formal registró 10 corridas por estrategia y tamaño. Para n = 10.000, las medias fueron A: 0,4838 s, B: 0,02570 s y C: 0,001903 s; las reducciones observadas frente a A fueron 94,69 % y 99,61 %. La equivalencia monetaria cumplió la tolerancia de 0,01 COP, con una diferencia máxima justo en ese límite. Hay CV > 10 % en B para n=10.000 y en C para todos los tamaños; esos grupos deben repetirse con mediciones más largas. No se midieron energía ni temperatura.

- Tabla estadística: [resumen con media, mediana, desviación, CV e IC95 %](resultados/resumen_estadistico.csv)
- Gráficos: [tiempo vs. n](resultados/tiempo_vs_n.png) · [comparación para n mayor](resultados/comparacion_n_mayor.png)
- Interpretación y propuesta: [informe científico](docs/informe.md) · [decisiones de hipótesis](docs/hipotesis.md)
- Evidencia cruda: [resultados/resultados.csv](resultados/resultados.csv)
