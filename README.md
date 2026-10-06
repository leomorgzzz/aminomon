# AMINOMON

RPG por turnos en la terminal para aprender los 20 aminoácidos estándar:
estructura de la cadena lateral, tipos químicos, carga, pK1/pK2/pKR, pI,
hidropatía, clasificación nutricional (esencial / condicional / no esencial),
requerimientos, codones y modificaciones postraduccionales.

## Jugar

```bash
python3 ~/aminomon/aminomon.py
```

Requisitos: Python 3 (solo biblioteca estándar). Funciona desde 80×24, pero
está pensado para **pantalla completa** (F11): ahí ves la célula entera, el
panel lateral con minimapa y a tu aminoácido en combate. La partida se guarda
en `~/.aminomon.json`.

## Controles

| Mapa | |
|---|---|
| ←↑→↓ / WASD | moverse |
| M o ? | manual (también en combate) |
| X | Aminodex |
| E | equipo: líder (Enter), ordenar (O) y evolucionar (V) |
| G / Q | guardar / guardar y salir |

| Combate | |
|---|---|
| 1-5 | movimientos (cada uno con su tipo y su multiplicador) |
| D | deducir el grupo del rival (+10 afinidad si aciertas) |
| V | velocidad de las animaciones (lenta por defecto) |
| T | lanzar ARNt (afinidad ≥ 50 + pregunta) |
| C / H / I | cambiar / huir / explicación de tus movimientos |

Cualquier tecla salta una animación.

## Tipos

Los tipos son los 5 grupos de Lehninger: no polar alifático, aromático, polar
sin carga, cargado + (básico) y cargado − (ácido). Solo Phe (aromático / no
polar), Tyr y Trp (aromático / polar) llevan un segundo tipo, como describe el
propio Lehninger. La tabla de afinidad es simétrica y se basa en la
interacción física real (efecto hidrofóbico, π–π, catión–π, puente de H,
puente salino, repulsión). Los puentes de H exigen un donador y un aceptor.

## Archivos

| Archivo | Contenido |
|---|---|
| `datos.py` | aminoácidos (valores Lehninger), tipos, tabla de afinidad, movimientos, evoluciones, zonas, glosario |
| `aminomon.py` | inicio, intro, mapa con cámara y panel lateral |
| `mapa.py` | célula de 150×48 generada con geometría, minimapa |
| `combate.py` | turnos, deducción de tipos, captura |
| `animaciones.py` | animaciones de cada interacción |
| `preguntas.py` | preguntas con repaso espaciado |
| `jefes.py` | 7 retos de péptidos, examen de la Chaperona y reto final del Ribosoma Maestro |
| `manual.py`, `aminodex.py`, `equipo.py` | pantallas |
| `dibujo.py` | colores y utilidades de curses |
| `progreso.py` | guardado, experiencia, evolución |

Para corregir o ampliar un dato (un pKa, una pista, una estructura ASCII)
basta con editar `datos.py`.
