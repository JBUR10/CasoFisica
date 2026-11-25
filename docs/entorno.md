# Entorno experimental

Información registrada por `herramientas.labmedicion.describir_entorno()` durante la ejecución formal del 25 de noviembre de 2026. La medición se realizó en el mismo equipo para A, B y C.

| Propiedad | Registro |
|---|---|
| Fecha y hora del registro | 2026-11-25 09:31:48 (hora local de Python) |
| Sistema operativo | Windows 11 |
| Equipo | ASUS TUF Gaming A15 FA506NCG_FA506NCG |
| Arquitectura | AMD64 |
| Procesador | AMD64 Family 25 Model 124 Stepping 0 (identificador reportado por el sistema) |
| Núcleos lógicos | 12 |
| Memoria instalada | 16.395.886.592 bytes (aprox. 15,27 GiB) |
| Python | CPython 3.13.15 |
| psutil | No instalado |
| Frecuencia de CPU | No disponible por sensores |
| Temperatura de CPU | No disponible; plan B: reportar “no medida”, sin estimación |
| Energía RAPL | No disponible; plan B: no reportar energía |
| Alimentación | No registrada durante la sesión |
| Aplicaciones abiertas | No registradas durante la sesión |

La salida completa generada automáticamente está en `resultados/resultados.entorno.json`. El uso de CPU del proceso se calcula en el CSV de mediciones como tiempo de CPU dividido por tiempo de pared. No equivale a potencia eléctrica ni a energía.

Para repetir el registro en este equipo:

```powershell
py -3.13 -c "import json; from herramientas.labmedicion import describir_entorno; print(json.dumps(describir_entorno(), indent=2, ensure_ascii=False))"
```
