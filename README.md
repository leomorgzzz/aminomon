# AMINOMON

RPG por turnos en la terminal para aprender los 20 aminoácidos estándar:
estructura de la cadena lateral, tipos químicos, carga, pK1/pK2/pKR, pI,
hidropatía, clasificación nutricional (esencial / condicional / no esencial),
codones y modificaciones postraduccionales.

## Jugar

```bash
git clone https://github.com/leomorgzzz/aminomon.git
cd aminomon
./instalar.sh        # crea el comando `aminomon` en ~/.local/bin
aminomon             # desde cualquier carpeta
```

También se puede abrir sin instalar: `python3 aminomon.py`. Para quitar el
comando: `./instalar.sh --quitar`. Si mueves la carpeta del juego, vuelve a
correr `./instalar.sh`.

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
| E | equipo: líder (Enter), ordenar (O) y modificar (V) |
| G / Q | guardar / guardar y salir |
| P | mostrar u ocultar la cadena que te sigue (regalo por la Aminodex completa) |

| Combate | |
|---|---|
| 1-5 | interacciones (cada una con su grupo, multiplicador e interacción concreta) |
| D | deducir el grupo del rival (+10 afinidad si aciertas) |
| V | velocidad de las animaciones (lenta por defecto) |
| T | lanzar ARNt (afinidad ≥ 50 + pregunta) |
| C / H / I | cambiar / huir / detalle de tus interacciones |

Cualquier tecla salta una animación.

## Progreso

1. Captura los 20 aminoácidos. Cada uno vive donde su química es favorable; la
   Arg solo aparece dentro del núcleo, y para entrar necesitas una NLS con al
   menos 4 Lys (en los ribosomas ∴).
2. Vence a los 7 jefes (J): cada uno pide construir un péptido, y cada
   aminoácido se puede usar tantas veces como lo tengas en tu equipo.
3. Consigue las modificaciones postraduccionales (Equipo → V).
4. Presenta el examen de la Chaperona (H): con 8 aciertos la proteína queda
   nativa; los aciertos 9 y 10 son extras.
5. Presenta el examen final del René-virus (V), un virus inofensivo que usa
   los ribosomas de la célula: traducir ARNm y analizar mutaciones reales.
6. Post-juego: el René-virus te hace encargos de síntesis de péptidos reales
   (encefalinas, oxitocina, angiotensina II, Tat del VIH…). Los traduces de su
   ARNm y, si tu equipo tiene las copias necesarias de cada residuo, entran al
   catálogo de péptidos de la Aminodex.

Al completar la Aminodex y luego todas las modificaciones, el René-virus te
da regalos que cambian cómo se ve el mapa.

## Tipos

Los tipos son los 5 grupos de Lehninger: no polar alifático, aromático, polar
sin carga, cargado + (básico) y cargado − (ácido). Solo Phe (aromático / no
polar), Tyr y Trp (aromático / polar) llevan un segundo tipo, como describe el
propio Lehninger. La tabla de afinidad es simétrica y se basa en la
interacción física real (efecto hidrofóbico, π–π, catión–π, puente de H,
puente salino, repulsión). Los puentes de H exigen un donador y un aceptor.

Cada movimiento es una interacción nombrada por su clase y por el grupo R
que la forma (p. ej. «Electrostática · guanidinio»), más el puente de H
del esqueleto y van der Waals, que todos tienen.

## Archivos

| Archivo | Contenido |
|---|---|
| `datos.py` | aminoácidos (valores Lehninger), tipos, tabla de afinidad, movimientos, modificaciones postraduccionales, zonas, péptidos del post-juego, glosario |
| `aminomon.py` | inicio, intro, mapa con cámara y panel lateral |
| `mapa.py` | célula de 150×48 generada con geometría, minimapa |
| `combate.py` | turnos, deducción de tipos, captura |
| `animaciones.py` | animaciones de cada interacción |
| `preguntas.py` | preguntas con repaso espaciado |
| `jefes.py` | 7 retos de péptidos, examen de la Chaperona, examen final del René-virus y encargos de síntesis |
| `manual.py`, `aminodex.py`, `equipo.py` | pantallas |
| `dibujo.py` | colores y utilidades de curses |
| `progreso.py` | guardado, experiencia, modificaciones |

Para corregir o ampliar un dato (un pKa, una pista, una estructura ASCII)
basta con editar `datos.py`.
