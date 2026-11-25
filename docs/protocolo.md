# Protocolo experimental reproducible

**Responsable:** Integrante A (R1 y apoyo a R4) · **Revisado por:** Equipo 5 · **Versión:** 1 · **Fecha de ejecución:** 2026-11-25

## 1. Objetivo

Comparar el tiempo de ejecución de tres implementaciones que calculan el interés total de la misma cartera de créditos: A, línea base; B, cálculo de invariantes fuera del ciclo mensual; y C, fórmula cerrada con caché. Se comprueba primero que B y C reproduzcan el total de A con diferencia máxima de 0,01 COP. La variable independiente es la estrategia y el tamaño de entrada; la variable principal observada es el tiempo en segundos.

## 2. Preparación del entorno

1. Ejecutar desde la raíz del repositorio con Python 3.10 o superior. Registrar sistema operativo, procesador y versión de Python en `docs/entorno.md`.
2. Usar la misma máquina y mantener alimentación y perfil de energía constantes durante todas las corridas. Cerrar tareas que puedan cargar la CPU y anotar cualquier aplicación o incidente relevante. Si no se registró una condición, declararla como no registrada.
3. Crear cada conjunto una sola vez con `linea_base.preparar(n)` (semilla predeterminada 5); reutilizar exactamente esa lista para A, B y C. La preparación queda fuera del tiempo medido.
4. Correr las pruebas de corrección antes de medir. La captura de pantalla no reemplaza los archivos CSV como evidencia reproducible.

## 3. Procedimiento ejecutado

| Paso | Acción | Comando | Evidencia |
|---|---|---|---|
| 1 | Registrar referencia aislada de 5.000 solicitudes | `py -3.13 -m src.linea_base` | Salida de consola anotada en README |
| 2 | Verificar equivalencia de estrategias | `py -3.13 -m unittest discover -s pruebas -v` | Cuatro pruebas aprobadas |
| 3 | Comprobar el arnés con una corrida rápida | `py -3.13 -m experimentos.ejecutar_experimento --rapido` | CSV temporal, reemplazado por la corrida formal |
| 4 | Medir experimento formal | `py -3.13 -m experimentos.ejecutar_experimento` | `resultados/resultados.csv` y `resultados/resultados.entorno.json` |
| 5 | Calcular estadística descriptiva e IC | `py -3.13 analizar_resultados.py resultados/resultados.csv` | `resultados/resumen_estadistico.csv` |

El programa calienta cada estrategia una vez, aleatoriza el orden de las mediciones con semilla 42 y realiza 10 corridas de tiempo por combinación. La medición de memoria se registra aparte (repetición 0) para no mezclar el sobrecosto de `tracemalloc` con el tiempo. Las filas de memoria no entran al resumen temporal.

## 4. Parámetros y justificación

- **Tamaños:** `n = 2.000, 5.000 y 10.000` solicitudes. Cubren una progresión de cinco veces en carga total con puntos intermedios para observar cómo escala el tiempo sin hacer excesivamente larga la estrategia A, cuyo trabajo crece aproximadamente como `n·m²`.
- **Repeticiones:** 10 medidas por estrategia y tamaño. Permiten estimar media, desviación estándar e intervalo de confianza del 95 % sin incluir el calentamiento.
- **Calentamiento:** una ejecución sin registro por estrategia, con el primer tamaño.
- **Orden:** las 90 combinaciones se mezclan con `random.Random(42)` para reducir sesgos por deriva térmica o temporal.
- **Datos:** para cada tamaño se usa el mismo conjunto determinista para las tres estrategias. La semilla de `preparar` es 5.

## 5. Criterios de calidad y lectura de resultados

- La diferencia absoluta entre cada resultado optimizado y A debe ser como máximo `0,01 COP`. El arnés detiene el experimento si no se cumple.
- Se reportan las diez repeticiones, media, desviación estándar, coeficiente de variación (CV) e IC95 %. Un CV superior a 10 % se marca para revisión y repetición; no se eliminan valores atípicos sin una causa documentada.
- En esta ejecución, el CV superó 10 % para B con `n=10.000` (11,005 %) y para C en los tres tamaños (20,516 % a 45,426 %). Como C termina en aproximadamente 0,0004–0,0019 s, el ruido del sistema y la resolución de la medición pesan más. Estos grupos deben tratarse como evidencia preliminar y repetirse con más trabajo por corrida antes de sostener conclusiones finas sobre sus diferencias. No se excluyeron datos.
- Temperatura, energía RAPL y frecuencia no se midieron porque los sensores no estaban disponibles. No se infiere consumo de energía a partir del uso de CPU.

## 6. Registro de ejecución e incidentes

| Fecha/hora local | Incidente o condición | Corridas afectadas | Decisión |
|---|---|---|---|
| 2026-11-25 09:31 | Sesión en Windows 11, CPython 3.13.15; no disponibles psutil, frecuencia, temperatura ni RAPL. Alimentación y aplicaciones abiertas no quedaron registradas. | Ejecución formal completa | Se conservaron las mediciones de tiempo; los campos de sensores quedan sin dato y se documenta la limitación. |
| 2026-11-25 | CV por encima del 10 % en B (n=10.000) y C (todos los n). | 6 combinaciones | Se conservan todas las corridas y se señala que deben repetirse para conclusiones robustas. |
