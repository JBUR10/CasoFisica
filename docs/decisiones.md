# Registro de decisiones técnicas (ADR breve)

Cada decisión importante se registra aquí y se enlaza desde el issue o PR correspondiente.

## D-001 — Estrategias de optimización comparables
- **Fecha:** 2026-11-18 · **Autor(es):** Integrante C · **Issue/PR:** pendiente
- **Contexto:** La línea base repite la potencia y la cuota en cada mes y no reutiliza cálculos con la misma tasa y plazo.
- **Opciones consideradas:** B) mover cálculos invariantes fuera del ciclo mensual; C) usar la identidad del interés total y memoizar el factor tasa–plazo.
- **Decisión:** Mantener A como referencia, añadir B y C como módulos independientes y medirlas con las mismas solicitudes.
- **Justificación (incluya evidencia o principio físico):** Reducir operaciones reduce los ciclos requeridos, relacionados con el tiempo de CPU por `N = f·t`. C utiliza `I_total = m·C − P`, válido para un plan francés amortizado; los resultados se comparan en COP contra A para detectar diferencias numéricas.
- **Consecuencias / riesgos:** C puede presentar pequeñas diferencias de redondeo por coma flotante y debe ser verificada contra la línea base. El efecto en energía solo se reportará si el sensor RAPL está disponible.
