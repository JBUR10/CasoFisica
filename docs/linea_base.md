# Línea base de cálculo de créditos

La estrategia A reproduce el cálculo inicial del simulador para créditos con cuota fija del sistema francés. Para cada solicitud se reciben el capital `P` en COP, la tasa periódica `i` (adimensional) y el plazo `m` en meses. La cuota teórica es

`C = P · i / (1 − (1 + i)^−m)`.

En cada uno de los `m` meses, `intereses_credito` calcula el interés del saldo (`saldo · i`), acumula ese interés y actualiza el saldo restando la parte de capital de la cuota. La función devuelve la suma de intereses del plan. `ejecutar` repite el cálculo para cada solicitud y redondea el total a dos decimales en COP.

## Costo computacional

La función `potencia_lenta` calcula `(1 + i)^m` con `m` multiplicaciones. La línea base la vuelve a ejecutar dentro de cada iteración mensual, aunque `P`, `i` y `m` no cambian durante el crédito. Por eso el costo dominante por solicitud crece como `O(m²)`; para `n` solicitudes el costo es `O(n · m²)`. Además, no conserva resultados para solicitudes con la misma tasa y plazo.

La línea base sirve como referencia de corrección y rendimiento, no como método más eficiente. Las estrategias B y C deben recibir las mismas solicitudes deterministas y producir el mismo total monetario dentro de una tolerancia de `0,01 COP`. La tolerancia reconoce diferencias de redondeo de coma flotante; una discrepancia mayor hace fallar la verificación.

## Datos reproducibles

`preparar(n, semilla=5)` crea las solicitudes en memoria con un generador pseudoaleatorio local. El portafolio usa tasas mensuales de `0,009` a `0,021`, plazos de 12 a 72 meses en pasos de 12 y capitales que son múltiplos de `500 000 COP`. Mantener la misma semilla permite que las tres estrategias reciban exactamente los mismos créditos.

Para ejecutar la referencia y las pruebas de equivalencia desde la raíz del repositorio:

```bash
python -m src.linea_base
python -m unittest discover -s pruebas -v
```

El tiempo de una ejecución aislada es evidencia exploratoria. La comparación formal se obtiene con el arnés `experimentos.ejecutar_experimento`, que aleatoriza el orden y repite las corridas.
