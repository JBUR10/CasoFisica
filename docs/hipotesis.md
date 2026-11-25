# Hipótesis del equipo

Estas predicciones se formulan para orientar la lectura del experimento de Clase 5. Como el CSV ya había sido generado antes de completar esta hoja, deben considerarse hipótesis de análisis exploratorio, no preregistradas antes de medir.

| Id | Hipótesis completa | VI | VD (unidad) | Predicción cuantitativa | Mecanismo físico/computacional | Criterio de refutación |
|---|---|---|---|---|---|---|
| H1 | Si se usa B en vez de A, el tiempo medio disminuirá al menos 90 % para cada tamaño medido, manteniendo entradas y equipo constantes. | Estrategia | Tiempo (s) | Reducción ≥ 90 % para n = 2.000, 5.000 y 10.000 | B calcula la potencia y la cuota una vez por crédito. Evita repetir la potencia m veces dentro de cada uno de los m meses. Menos operaciones implican menos tiempo de CPU; N ≈ f·t_CPU. | Se refuta si, para cualquier tamaño, el límite superior del IC95 % de B no queda por debajo del 10 % del límite inferior del IC95 % de A. |
| H2 | Si se usa C en vez de A, el tiempo medio disminuirá al menos 99 % para cada tamaño medido, manteniendo entradas y equipo constantes. | Estrategia | Tiempo (s) | Reducción ≥ 99 % para n = 2.000, 5.000 y 10.000 | C evita el recorrido mensual usando I_total = m·C − P y reutiliza el factor de cuota para pares repetidos (i,m). El algoritmo hace menos operaciones por solicitud. | Se refuta si, para cualquier tamaño, el límite superior del IC95 % de C no queda por debajo del 1 % del límite inferior del IC95 % de A. |
| H3 | Si B o C sustituye a A, el interés total calculado conservará la corrección monetaria dentro de una diferencia absoluta máxima de 0,01 COP en todos los tamaños. | Estrategia | Diferencia absoluta (COP) | ≤ 0,01 COP para cada estrategia y n | Las expresiones representan el mismo plan francés, pero el orden de operaciones en coma flotante puede cambiar el redondeo finito. | Se refuta si alguna diferencia absoluta excede 0,01 COP en una entrada verificada. |

## Resultado de la comprobación

Con los IC95 % de medias del CSV, H1 y H2 cumplen sus umbrales en los tres tamaños: incluso el límite superior del tiempo optimizado queda bajo el umbral calculado con el límite inferior de A. Se consideran **respaldadas en este rango**, con cautela por CV > 10 % en B para n=10.000 y en C para todos los tamaños. No se extrapolan a cargas mayores.

La comparación directa de los totales redondeados produjo diferencias máximas de 0,00 COP para B y 0,01 COP para C (n=5.000). H3 queda **respaldada justo en el límite de tolerancia**; debe seguirse vigilando la precisión al cambiar los datos. Las pruebas de corrección existentes también aplican esta tolerancia.

Estas decisiones describen esta máquina, esta versión de Python y el intervalo de n ensayado. No prueban ahorro energético: no se midió energía.
