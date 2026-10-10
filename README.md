# AMINOMON

*English: `aminomon --en` or «English» on the title screen.*

RPG por turnos en la terminal para aprender los 20 aminoácidos estándar:
cadena lateral, tipo químico, carga, pK1/pK2/pKR, pI, hidropatía,
clasificación nutricional, codones y modificaciones postraduccionales.

Capturas aminoácidos en una célula, combates con interacciones químicas reales
y construyes péptidos para vencer a 7 jefes y al René-virus.

**Descargar:** [Windows](https://github.com/leomorgzzz/aminomon/releases/latest/download/Aminomon-Windows.exe) · [macOS](https://github.com/leomorgzzz/aminomon/releases/latest/download/Aminomon-macOS.zip) · doble clic y a jugar.

## Capturas

![Pantalla de inicio](capturas/pantalla-de-inicio.png)

![Mapa de la célula](capturas/juego-mapa.png)

![Combate](capturas/juego-combate.png)

## Instalación

### Windows

1. Descarga **[Aminomon-Windows.exe](https://github.com/leomorgzzz/aminomon/releases/latest/download/Aminomon-Windows.exe)**.
2. Ábrelo con doble clic. Se abre en pantalla completa.

No hay que instalar nada más. Windows puede avisar «Windows protegió su PC»
porque el programa no está firmado: **Más información → Ejecutar de todas
formas**.

### macOS

1. Descarga **[Aminomon-macOS.zip](https://github.com/leomorgzzz/aminomon/releases/latest/download/Aminomon-macOS.zip)** y ábrelo.
2. Doble clic en `Aminomon`. Si macOS no lo deja abrir: **Ajustes del Sistema →
   Privacidad y seguridad → Abrir de todos modos**.

Es para Mac con chip Apple (M1 o posterior).

### Linux o desde el código

```bash
git clone https://github.com/leomorgzzz/aminomon.git
cd aminomon
./instalar.sh        # crea el comando `aminomon` en ~/.local/bin
aminomon
```

Sin instalar: `python3 aminomon.py`. Quitar el comando: `./instalar.sh --quitar`.

Desde el código requiere Python 3 (solo biblioteca estándar; en Windows instala
`windows-curses` la primera vez). Funciona desde 80×24.

Archivos que crea:

- `~/.aminomon.json`: la partida (en Windows, `~` es `C:\Users\<tu usuario>`);
- `~/.aminomon_idioma`: el idioma.

## Controles

| Mapa | Acción |
|---|---|
| Flechas / WASD | moverse |
| M / ? | manual (también en combate) |
| X | Aminodex |
| E | equipo: líder (Enter), ordenar (O), modificar (V) |
| G / Q | guardar / guardar y salir |
| P | mostrar u ocultar la cadena que te sigue |

| Combate | Acción |
|---|---|
| 1-5 | interacciones |
| D | deducir el grupo del rival |
| T | lanzar ARNt para capturar |
| C / H / I | cambiar / huir / detalle de interacciones |
| V | velocidad de las animaciones |

Cualquier tecla salta una animación.

## Menú

- **Continuar** / **Nueva partida**.
- **Manual**.
- **English / Español**: cambia el idioma.
- **Salir**.

## Fuentes

- Valores fisicoquímicos y grupos de cadena lateral: Lehninger, a 25 °C.
- Hidropatía: escala de Kyte-Doolittle (1982).
