# Registro de decisiones técnicas (ADR breve)

Cada decisión importante se registra aquí y se enlaza desde el issue o PR correspondiente.

## D-001 — Estrategias de optimización comparables
- **Fecha:** 2026-11-18 · **Autor(es):** Integrante C · **Issue/PR:** pendiente
- **Contexto:** La línea base repite la potencia y la cuota en cada mes y no reutiliza cálculos con la misma tasa y plazo.
- **Opciones consideradas:** B) mover cálculos invariantes fuera del ciclo mensual; C) usar la identidad del interés total y memoizar el factor tasa–plazo.
- **Decisión:** Mantener A como referencia, añadir B y C como módulos independientes y medirlas con las mismas solicitudes.
- **Justificación (incluya evidencia o principio físico):** Reducir operaciones reduce los ciclos requeridos, relacionados con el tiempo de CPU por `N = f·t`. C utiliza `I_total = m·C − P`, válido para un plan francés amortizado; los resultados se comparan en COP contra A para detectar diferencias numéricas.
- **Consecuencias / riesgos:** C puede presentar pequeñas diferencias de redondeo por coma flotante y debe ser verificada contra la línea base. El efecto en energía solo se reportará si el sensor RAPL está disponible.

## D-002 — Ejecución y registro formal
- **Fecha:** 2026-11-25 · **Autor(es):** Integrante A · **Issue/PR:** pendiente
- **Contexto:** El equipo necesitaba separar las mediciones de tiempo de las corridas utilizadas para estimar memoria y conservar una ejecución reproducible.
- **Opciones consideradas:** incluir memoria en todas las corridas o registrar una corrida separada de memoria para cada estrategia y tamaño.
- **Decisión:** mantener diez corridas de tiempo y una corrida separada con repetición 0 y `medicion_memoria = si`; excluir las corridas de memoria del resumen temporal.
- **Justificación:** `tracemalloc` añade sobrecosto y puede modificar el tiempo observado. Mantener la separación permite analizar tiempo sin contaminarlo y conserva la información de memoria como evidencia independiente.
- **Consecuencias / riesgos:** el pico de memoria reportado solo representa memoria rastreada por Python, no toda la memoria del proceso ni del sistema.
