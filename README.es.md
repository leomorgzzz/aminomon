# AMINOMON

*[English](README.md) · Español*

![Combate](capturas/juego-combate.png)

RPG por turnos en la terminal para aprender los 20 aminoácidos estándar:
cadena lateral, tipo químico, carga, pK1/pK2/pKR, pI, hidropatía,
clasificación nutricional, codones y modificaciones postraduccionales.

**¿Para quién es?** Para quien tiene que aprenderse los aminoácidos en un curso
de bioquímica o biología, de prepa a posgrado. No necesitas saber nada: empiezas
con la Met y el manual (M) explica cada propiedad.

Valores de Lehninger a 25 °C; hidropatía de Kyte-Doolittle (1982)
([Fuentes](#fuentes)).

**Jugar:**

- **Windows:** [Aminomon-Instalador-Windows.exe](https://github.com/leomorgzzz/aminomon/releases/latest/download/Aminomon-Instalador-Windows.exe), instala y a jugar.
- **macOS:** [Aminomon-macOS.zip](https://github.com/leomorgzzz/aminomon/releases/latest/download/Aminomon-macOS.zip), descomprime y doble clic.
- **Linux:** `git clone https://github.com/leomorgzzz/aminomon.git && cd aminomon && ./instalar.sh && aminomon`

> **En desarrollo.** El juego se sigue actualizando: al abrirlo te avisa si hay
> una versión nueva y se actualiza desde la pantalla de título, sin reinstalar.
> Tu partida se conserva. Errores, ideas o datos que corregir:
> [Issues](https://github.com/leomorgzzz/aminomon/issues).

## Capturas

![Pantalla de inicio](capturas/pantalla-de-inicio.png)

![Mapa de la célula](capturas/juego-mapa.png)

## Instalación

### Windows

1. Descarga **[Aminomon-Instalador-Windows.exe](https://github.com/leomorgzzz/aminomon/releases/latest/download/Aminomon-Instalador-Windows.exe)** y ábrelo.
2. Sigue el instalador (no pide permisos de administrador). Al terminar, el
   juego queda en el menú Inicio y, si quieres, en el escritorio. Se abre en
   pantalla completa.

El instalador no está firmado (firmarlo cuesta una licencia anual), así que la
primera vez Windows puede avisar «Windows protegió su PC»: **Más información →
Ejecutar de todas formas**. Solo pasa al instalar. Para desinstalar:
**Configuración → Aplicaciones**.

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

Sin instalar: `python3 aminomon.py`. Actualizar: `aminomon --update` (hace
`git pull`). Quitar el comando: `./instalar.sh --quitar`.

Desde el código requiere Python 3 (solo biblioteca estándar; en Windows instala
`windows-curses` la primera vez). Funciona desde 80×24.

### Qué guarda y qué conecta

Solo escribe estos archivos:

- `~/.aminomon.json`: la partida (en Windows, `~` es `C:\Users\<tu usuario>`);
- `~/.aminomon_idioma`: el idioma (la primera vez se usa el del sistema).

Su única conexión: al abrir, consulta en GitHub si hay una versión nueva, y no
envía nada más. Para desactivarla: `aminomon --sin-actualizar`.

## Salir de pantalla completa

| Sistema | Tecla |
|---|---|
| Windows | Alt+Enter (o F11 en Windows Terminal) |
| macOS | Ctrl+Cmd+F |
| Linux | F11 en la mayoría de las terminales |

## Controles

| Mapa | Acción |
|---|---|
| Flechas / WASD | moverse |
| M / ? | manual (también en combate) |
| X | Aminodex (P práctica, L logros) |
| E | equipo: líder (Enter), ordenar (O), modificar (V) |
| B | sonido al acertar o fallar (sí/no) |
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
- **Actualizar a vX**: aparece cuando hay una versión nueva.
- **Salir**.

## Fuentes

- Valores fisicoquímicos y grupos de cadena lateral: Lehninger, a 25 °C.
- Hidropatía: escala de Kyte-Doolittle (1982).

## Pruebas

```bash
python3 pruebas/correr.py
```

Revisan que todo importe en los dos idiomas, que cada `tr("…")` tenga su
traducción en `traduccion/`, que los datos no queden en español en la versión
en inglés y que solo haya símbolos que la consola de Windows sabe dibujar.
Corren solas en GitHub en cada push y antes de compilar una versión.
