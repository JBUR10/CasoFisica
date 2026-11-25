# Variables experimentales

La comparación cambia la estrategia y el tamaño del lote, mientras mantiene iguales la cartera de solicitudes, el equipo y el procedimiento de medición.

| Tipo | Variable | Símbolo | Unidad | Valores / rango | Instrumento o forma de obtención | Justificación |
|---|---|---|---|---|---|---|
| Independiente | Estrategia de cálculo | — | — | A, B, C | Módulos `src.linea_base`, `src.estrategia_b` y `src.estrategia_c` | Factor cuyo efecto sobre el costo se compara. |
| Independiente | Solicitudes procesadas | n | solicitudes | 2.000, 5.000, 10.000 | Generadas con `preparar(n, semilla=5)` | Permite observar el escalamiento al aumentar la carga. |
| Dependiente principal | Tiempo de pared | t | s | Una medida por corrida | `time.perf_counter()` en `herramientas.labmedicion` | Indicador directo del tiempo que tarda cada estrategia. |
| Dependiente | Tiempo de CPU del proceso | t_CPU | s | Una medida por corrida | `time.process_time()` | Aproxima el tiempo de CPU consumido por el proceso. |
| Dependiente | Uso de CPU del proceso | U | % | Una medida por corrida | 100 × `t_CPU / t` | Separa ocupación del proceso de duración de pared; no es potencia. |
| Dependiente | Pico de memoria Python | M | MiB | Corrida separada | `tracemalloc` | Estima asignaciones rastreadas por Python; no mide toda la memoria del sistema. |
| Dependiente opcional | Temperatura | θ | °C | Sin dato en esta sesión | `herramientas.sensores` | Sensor no disponible; no se imputa. |
| Dependiente opcional | Energía | E | J | Sin dato en esta sesión | RAPL, si estuviera disponible | Sin sensor RAPL, no se estima energía. |
| Controlada | Equipo | — | — | Mismo ASUS TUF Gaming A15 | `platform` y WMI | Evita comparar arquitecturas distintas. |
| Controlada | Versión de Python | — | — | CPython 3.13.15 | `sys.version` | La implementación puede cambiar el rendimiento. |
| Controlada | Datos de entrada | — | — | Una misma lista por tamaño y estrategia | `linea_base.preparar(n)`; semilla 5 | Aísla el efecto del algoritmo. |
| Controlada | Orden y calentamiento | — | — | 1 calentamiento; orden pseudoaleatorio, semilla 42 | `experimentos.ejecutar_experimento` | Mitiga caché inicial y deriva temporal. |
| Controlada | Repeticiones | — | — | 10 por combinación | Arnés `Experimento` | Permite estimar dispersión e incertidumbre. |
| Controlada no verificada | Alimentación y aplicaciones abiertas | — | — | No registradas | Anotación del operador | Pueden afectar frecuencia y carga; registrar al repetir. |

## Mapa de dependencias

`Estrategia → operaciones ejecutadas → ciclos de CPU N ≈ f·t_CPU → tiempo t`

`n y plazo m → cantidad de trabajo → tiempo t`

`Estrategia → temporales asignados → pico M`

La energía requiere medición directa del sistema (por ejemplo, RAPL). Una reducción de operaciones podría reducir energía si la potencia y el resto de las condiciones son comparables, pero este experimento no permite afirmar ese ahorro.

## Variables no controladas y mitigación

| Variable no controlada | Efecto posible | Mitigación |
|---|---|---|
| Frecuencia dinámica y temperatura | Cambia los ciclos por segundo y el tiempo | Usar la misma máquina, aleatorizar el orden y registrar temperatura/frecuencia si hay sensor. |
| Procesos del sistema operativo | Añaden competencia por CPU y memoria | Cerrar tareas pesadas antes de medir; repetir grupos con CV > 10 %. |
| Alimentación o perfil de energía | Puede limitar frecuencia del procesador | Mantener y anotar el mismo estado en futuras sesiones. |
| Ruido de cronometraje en funciones muy breves | Aumenta la dispersión relativa en C | Aumentar trabajo por corrida o repeticiones y reportar CV e IC95 %. |
| Sincronización de archivos en carpeta compartida | Puede generar carga incidental de disco/CPU | Evitar actividad de sincronización durante corridas futuras o registrar el incidente. |
