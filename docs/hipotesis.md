# Plantilla de hipótesis

Una hipótesis verificable **predice un resultado medible** y **puede resultar falsa**.

## Estructura
> **Si** _(cambio en la variable independiente)_, **entonces** _(variable dependiente, con unidad)_
> **aumentará / disminuirá** aproximadamente _(magnitud o factor)_, **porque** _(mecanismo físico/computacional)_,
> **manteniendo constantes** _(variables controladas)_.

## Ejemplo (problema neutro de la demostración, NO de un equipo)
> **Si** se reemplaza la lista intermedia por un generador al sumar n cuadrados, **entonces** el pico de memoria
> (MiB) **disminuirá** en más de un 90 % para n = 10⁶ y el tiempo (s) variará menos de un 20 %, **porque** el
> generador no almacena los n valores (memoria constante) pero realiza el mismo número de operaciones,
> **manteniendo** el mismo equipo, versión de Python y n.

## Hipótesis del equipo
| Id | Hipótesis completa | VI | VD (unidad) | Predicción cuantitativa | Mecanismo físico | ¿Cómo la refutaríamos? |
|---|---|---|---|---|---|---|
| H1 | **Si** se reemplaza A por B en cargas de 2.000, 5.000 y 10.000 solicitudes, **entonces** el tiempo de pared disminuirá, **porque** B calcula una sola vez la potencia y la cuota de cada solicitud en vez de repetirlas dentro de todos los meses, manteniendo iguales los datos de entrada, el equipo y el procedimiento. | Estrategia: A frente a B | Tiempo de pared t (s) | Al menos 10 veces menos tiempo para n = 10.000 | B reduce operaciones dentro de `m` meses; con menos instrucciones ejecutadas puede reducirse el tiempo de CPU y la duración de pared. | No se confirmaría si las medias coinciden dentro de sus IC95 % o si B no reduce el tiempo de manera coherente. |
| H2 | **Si** se reemplaza B por C para las mismas cargas, **entonces** el tiempo de pared disminuirá, **porque** C evita recorrer los meses y reutiliza el factor de tasa–plazo, manteniendo iguales los datos de entrada, el equipo y el procedimiento. | Estrategia: B frente a C | Tiempo de pared t (s) | C será al menos 5 veces más rápido para n = 10.000 | C transforma el trabajo mensual en una fórmula cerrada y aprovecha combinaciones repetidas; se esperan menos operaciones y menos ciclos de CPU por solicitud. | No se confirmaría si los IC95 % de las medias se solapan ampliamente o si la diferencia no supera el factor propuesto. |
| H3 | **Si** aumenta el número de solicitudes de 2.000 a 10.000 en las tres estrategias, **entonces** el tiempo de pared aumentará, **porque** crece la cantidad de solicitudes procesadas, manteniendo constantes la estrategia, el equipo y las condiciones de medición. | Número de solicitudes n (solicitudes) | Tiempo de pared t (s) | El tiempo crecerá de forma aproximadamente proporcional o mayor con n, sin extrapolar fuera del rango medido | Más solicitudes implica ejecutar más operaciones y sumar más contribuciones, aunque el crecimiento real depende de las operaciones dominantes y de la memoria disponible. | Se refutaría si la relación observada no muestra crecimiento al aumentar n o si el patrón queda determinado por ruido y corridas atípicas. |

## Lista de verificación
- [ ] Tiene dirección (aumenta/disminuye) y una magnitud aproximada.
- [ ] La VD es medible con las herramientas disponibles en el laboratorio.
- [ ] Indica qué resultado la **refutaría**.
- [ ] Explica el mecanismo con al menos una magnitud física y su unidad SI.
- [ ] No afirma ahorro de energía si no se va a medir energía.
