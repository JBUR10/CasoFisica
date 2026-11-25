# Informe científico breve — Equipo 5

**Título:** Comparación de estrategias para el cálculo intensivo de intereses · **Integrantes:** Joel Andrés Mendoza Buriticá, Sebastian Ramirez Castrillon y Luis Felipe Sierra · **Fecha:** 25 de noviembre de 2026 · **Repositorio:** JBUR10/CasoFisica

## Resumen (≤ 150 palabras)
La cooperativa FinanCréditos necesita procesar miles de solicitudes de crédito sin que el tiempo de cálculo retrase las operaciones. Se compararon tres estrategias (A: línea base; B: cálculo de invariantes fuera del ciclo; C: fórmula cerrada con caché) usando n = 2.000, 5.000 y 10.000 solicitudes, diez corridas por combinación y el mismo conjunto de datos en cada tamaño. Para n = 10.000, el tiempo medio fue 0,483773 s para A, 0,025698 s para B y 0,001903 s para C. Las estrategias optimizadas conservaron la equivalencia monetaria dentro de 0,01 COP respecto de A. C fue aproximadamente 254 veces más rápida que A y 13 veces más rápida que B. Esta ventaja es medible para la carga y el equipo evaluados, pero no permite estimar energía ni extrapolar a toda la operación.

## 1. Introducción
El simulador recalcula planes completos para una cartera de solicitudes y puede consumir una cantidad importante de tiempo de CPU durante las horas pico. Se planteó comparar si reducir operaciones repetidas disminuye el tiempo observado al aumentar el tamaño de entrada. El trabajo se relaciona con el tiempo de CPU, los ciclos ejecutados y la dinámica de la memoria. Para una función que tarda t segundos a una frecuencia f, el número aproximado de ciclos es N ≈ f·t; retirar operaciones puede reducir N si la potencia de cómputo permanece comparable.

## 2. Hipótesis
H1: B reducirá el tiempo respecto de A en los tres tamaños, por calcular una vez la potencia y la cuota de cada solicitud.

H2: C reducirá el tiempo respecto de B, por evitar el recorrido mensual y reutilizar el factor tasa–plazo.

H3: El tiempo aumentará al pasar de 2.000 a 10.000 solicitudes en las tres estrategias.

Las hipótesis completas y los criterios de refutación están en `docs/hipotesis.md`.

## 3. Método
- Se compararon A, B y C con la misma lista de solicitudes por tamaño, generada con semilla 5.
- Las variables independientes fueron la estrategia y n = 2.000, 5.000 y 10.000 solicitudes. La variable principal fue el tiempo de pared medido con `time.perf_counter()` en segundos.
- El entorno formal fue Windows 11, AMD64, procesador AMD64 Family 25 Model 124, 12 núcleos lógicos y CPython 3.13.15. No se disponía de psutil ni sensores de frecuencia, temperatura o RAPL.
- Se realizó un calentamiento por estrategia, el orden de las corridas se aleatorizó con semilla 42 y se realizaron diez repeticiones de tiempo por combinación.
- Las mediciones de memoria se realizaron aparte con repetición 0 y no se incluyeron en las estadísticas de tiempo.

## 4. Resultados
| Estrategia | n | Repeticiones | Media (s) | SD (s) | CV (%) | IC95 % (s) |
|---|---:|---:|---:|---:|---:|---|
| A | 2.000 | 10 | 0,100928 | 0,006966 | 6,902 | 0,095945–0,105911 |
| B | 2.000 | 10 | 0,004865 | 0,000248 | 5,107 | 0,004687–0,005043 |
| C | 2.000 | 10 | 0,000449 | 0,000158 | 35,188 | 0,000336–0,000563 |
| A | 5.000 | 10 | 0,250177 | 0,020207 | 8,077 | 0,235722–0,264631 |
| B | 5.000 | 10 | 0,013276 | 0,001296 | 9,760 | 0,012349–0,014202 |
| C | 5.000 | 10 | 0,001034 | 0,000470 | 45,426 | 0,000698–0,001370 |
| A | 10.000 | 10 | 0,483773 | 0,014266 | 2,949 | 0,473569–0,493978 |
| B | 10.000 | 10 | 0,025698 | 0,002828 | 11,005 | 0,023675–0,027721 |
| C | 10.000 | 10 | 0,001903 | 0,000390 | 20,516 | 0,001624–0,002182 |

- Gráfico 1: `resultados/tiempo_vs_n.png`, tiempo frente a n en escala log–log.
- Gráfico 2: `resultados/comparacion_n_mayor.png`, comparación para n = 10.000.
- Medido: tiempo de pared, tiempo de CPU del proceso y pico de memoria Python de las corridas separadas.
- No medido: frecuencia, temperatura y energía RAPL.

El CV supera 10 % en B para n = 10.000 y en C para los tres tamaños. Las diferencias grandes observadas no justifican eliminar ninguna corrida. En C, el tiempo tan breve aumenta la sensibilidad al ruido y a la resolución del cronómetro.

## 5. Discusión
- **H1 — confirmada en el rango medido:** al pasar de A a B para n = 10.000, la media cayó de 0,483773 s a 0,025698 s, una reducción aproximada del 94,69 %. Los IC95 % no se solapan.
- **H2 — confirmada con cautela:** al pasar de B a C, la media cayó a 0,001903 s, aproximadamente 13 veces menos que B. Los intervalos no se solapan, pero el CV de C impide presentar diferencias menores como concluyentes. Se debe repetir C con más trabajo por medición.
- **H3 — confirmada:** las tres estrategias aumentaron su tiempo medio al pasar de 2.000 a 10.000 solicitudes.
- El mecanismo observado es coherente con una reducción de operaciones repetidas: B evita recalcular potencia y cuota dentro del ciclo mensual, mientras C sustituye el recorrido por una fórmula cerrada y reutiliza factores tasa–plazo.
- Limitaciones: una sola máquina, 10 repeticiones, perfil de alimentación y procesos abiertos no registrados, ausencia de frecuencia y RAPL, y ejecuciones muy breves para C. Por ello no se afirma ahorro de energía ni se extrapola fuera de n = 2.000–10.000.

## 6. Propuesta de mejora para la empresa
Se recomienda evaluar C para el procesamiento de lotes con tasas y plazos repetidos, manteniendo la prueba de equivalencia respecto de A. Para n = 10.000, C tendría una media medida 254 veces menor que A y 13 veces menor que B. Para una operación anual hipotética, no se traduce a ahorro energético sin medir potencia o consumo eléctrico.

El despliegue requiere conservar A como prueba de corrección, vigilar diferencias mayores de 0,01 COP y repetir mediciones en el servidor de producción. El riesgo principal es una carga real con nuevas combinaciones, tasas o plazos, donde la caché puede comportarse distinto. Se recomienda aumentar el trabajo por ejecución y registrar frecuencia, temperatura, alimentación y procesos activos antes de cambiar la estrategia definitiva.

## 7. Conclusiones
La línea base fue la más lenta, B mostró una mejora clara y C fue la alternativa más rápida para el rango evaluado. Todas conservaron la equivalencia monetaria dentro de la tolerancia establecida. La conclusión se limita al equipo y a la carga medidos; no se presenta como ahorro de energía ni como rendimiento garantizado en producción.

## 8. Referencias (verificables)
Documentación del proyecto: `docs/protocolo.md`, `docs/entorno.md`, `docs/variables.md`, `docs/hipotesis.md` y `README.md`.
## Anexo: uso de IA (resumen de docs/uso_ia.md)
