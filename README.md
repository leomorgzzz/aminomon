# AMINOMON

*English · [Español](README.es.md)*

A turn-based terminal RPG for learning the 20 standard amino acids. To catch
one you have to recognize its structure, and the ones you miss keep showing up
until you know them: name, 3- and 1-letter codes, side chain, chemical type,
charge, pK1/pK2/pKR, pI, hydropathy, nutritional class, codons and
post-translational modifications.

> **Work in progress.** The game keeps getting updated: when you open it, it
> tells you if there's a new version and updates from the title screen, no
> reinstall needed. Your save is kept. Bugs, ideas or data to fix:
> [Issues](https://github.com/leomorgzzz/aminomon/issues).

**Download:** [Windows](https://github.com/leomorgzzz/aminomon/releases/latest/download/Aminomon-Instalador-Windows.exe) · [macOS](https://github.com/leomorgzzz/aminomon/releases/latest/download/Aminomon-macOS.zip) · install and play.

## Screenshots

![Title screen](capturas/pantalla-de-inicio.png)

![Cell map](capturas/juego-mapa.png)

![Battle](capturas/juego-combate.png)

## Installation

### Linux, or from source

```bash
git clone https://github.com/leomorgzzz/aminomon.git
cd aminomon
./instalar.sh        # creates the `aminomon` command in ~/.local/bin
aminomon
```

Without installing: `python3 aminomon.py`. Update: `aminomon --update` (runs
`git pull`). Remove the command: `./instalar.sh --quitar`.

From source it needs Python 3 (standard library only; on Windows it installs
`windows-curses` the first time). Works from 80×24.

### Windows

1. Download **[Aminomon-Instalador-Windows.exe](https://github.com/leomorgzzz/aminomon/releases/latest/download/Aminomon-Instalador-Windows.exe)** and open it.
2. Follow the installer (no admin rights needed). When it's done, the game is
   in the Start menu and, if you want, on the desktop. It opens full screen.

The installer isn't signed (signing costs a yearly license), so the first time
Windows may warn "Windows protected your PC": **More info → Run anyway**. It
only happens when installing. To uninstall: **Settings → Apps**.

### macOS

1. Download **[Aminomon-macOS.zip](https://github.com/leomorgzzz/aminomon/releases/latest/download/Aminomon-macOS.zip)** and open it.
2. Double-click `Aminomon`. If macOS won't open it: **System Settings →
   Privacy & Security → Open Anyway**.

For Macs with Apple silicon (M1 or later).

### Files it creates

- `~/.aminomon.json`: your save (on Windows, `~` is `C:\Users\<your user>`);
- `~/.aminomon_idioma`: the language (the first time it follows your system).

On startup the game asks GitHub whether there's a new version; it sends
nothing else. To turn it off: `aminomon --no-update`.

## Leaving full screen

| System | Key |
|---|---|
| Windows | Alt+Enter (or F11 in Windows Terminal) |
| macOS | Ctrl+Cmd+F |
| Linux | F11 in most terminals |

## Controls

| Map | Action |
|---|---|
| Arrows / WASD | move |
| M / ? | manual (also in battle) |
| X | Aminodex |
| E | team: leader (Enter), sort (O), modify (V) |
| G / Q | save / save and quit |
| P | show or hide the chain that follows you |

| Battle | Action |
|---|---|
| 1-5 | interactions |
| D | deduce the rival's group |
| T | throw a tRNA to catch |
| C / H / I | switch / run / interaction details |
| V | animation speed |

Any key skips an animation.

## Menu

- **Continue** / **New game**.
- **Manual**.
- **Español / English**: switches the language.
- **Update to vX**: shows up when there's a new version.
- **Quit**.

## Sources

- Physicochemical values and side-chain groups: Lehninger, at 25 °C.
- Hydropathy: Kyte-Doolittle scale (1982).

## Tests

```bash
python3 pruebas/correr.py
```

They check that everything imports in both languages, that every `tr("…")`
has its translation in `traduccion/`, that the data doesn't stay in Spanish in
the English version, and that only symbols the Windows console can draw are
used. They run on GitHub on every push and before building a release.

## License

MIT · [LICENSE](LICENSE)
