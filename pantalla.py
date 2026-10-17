"""Tamaño de la pantalla, igual en todas las computadoras.

Dos problemas que se veían:
  · muy grande: la letra era enorme (o la ventana medía más que el monitor) y
    solo se veía un pedazo del juego;
  · muy pequeño: en monitores grandes la letra quedaba diminuta.

En la consola clásica de Windows (la que abre el acceso directo del
instalador) el juego sí puede elegir la fuente: se calcula con el tamaño del
monitor en píxeles para que quepan ~180 columnas y al menos 48 filas, y luego
el búfer se iguala a la ventana (si el búfer es más grande que la ventana,
curses dibuja en una zona que no se ve).

En las demás terminales (Windows Terminal, Linux, macOS) el programa no puede
cambiar la letra: si el tamaño queda lejos de lo ideal, una pantalla de
calibración dice qué teclas usar y muestra el tamaño en vivo.

Este archivo es igual en Aminomon y en Reviewer 2 (cambia solo NOMBRE)."""

import os
import sys
import time

COLUMNAS_IDEAL = 180
FILAS_MIN = 48
RANGO_COLUMNAS = (130, 240)
RANGO_FILAS = (40, 80)


def _nombre():
    base = os.path.basename(sys.argv[0]).lower()
    return "aminomon" if "aminomon" in base else "reviewer2"


def _archivo_aviso():
    return os.path.expanduser(f"~/.{_nombre()}_pantalla")


# ---------------------------------------------------------------- Windows
def ajustar_consola_windows():
    """Maximiza y pone en pantalla completa la consola clásica, elige la
    fuente con el tamaño del monitor y deja el búfer del tamaño de la ventana.
    Devuelve True si pudo controlar la consola."""
    if os.name != "nt":
        return False
    import ctypes
    from ctypes import wintypes
    kernel32, user32 = ctypes.windll.kernel32, ctypes.windll.user32
    try:
        user32.SetProcessDPIAware()             # tamaños en píxeles reales
    except AttributeError:
        pass
    consola = kernel32.GetConsoleWindow()
    clase = ctypes.create_unicode_buffer(64)
    user32.GetClassNameW(consola, clase, 64)
    if not consola or clase.value != "ConsoleWindowClass":
        return False                            # Windows Terminal u otra: no se puede
    user32.ShowWindow(consola, 3)               # SW_MAXIMIZE
    user32.SetForegroundWindow(consola)
    time.sleep(0.2)
    nada = ctypes.c_uint32()
    salida = kernel32.GetStdHandle(-11)
    if not kernel32.SetConsoleDisplayMode(salida, 1, ctypes.byref(nada)):
        _alt_enter(user32)
    time.sleep(0.5)

    class MONITOR(ctypes.Structure):
        _fields_ = [("cbSize", wintypes.DWORD), ("rcMonitor", wintypes.RECT),
                    ("rcWork", wintypes.RECT), ("dwFlags", wintypes.DWORD)]

    m = MONITOR()
    m.cbSize = ctypes.sizeof(MONITOR)
    user32.GetMonitorInfoW(user32.MonitorFromWindow(consola, 2), ctypes.byref(m))
    ancho_px = (m.rcMonitor.right - m.rcMonitor.left) or user32.GetSystemMetrics(0)
    alto_px = (m.rcMonitor.bottom - m.rcMonitor.top) or user32.GetSystemMetrics(1)
    # Consolas: el ancho de la celda es ~la mitad de la altura de la fuente
    alto_fuente = int(min(2 * ancho_px / COLUMNAS_IDEAL, alto_px / FILAS_MIN))
    alto_fuente = max(8, min(72, alto_fuente))
    _poner_fuente(alto_fuente)
    # se corrige con lo que de verdad quedó (la consola tarda en redimensionar)
    for _ in range(6):
        time.sleep(0.25)
        cols, filas = tamano_consola()
        if not cols:
            break
        if cols > RANGO_COLUMNAS[1] or (filas > RANGO_FILAS[1] and cols > COLUMNAS_IDEAL):
            alto_fuente += 1
        elif (cols < RANGO_COLUMNAS[0] or filas < FILAS_MIN - 6) and alto_fuente > 8:
            alto_fuente -= 1
        else:
            break
        _poner_fuente(alto_fuente)
    igualar_bufer()
    return True


def _alt_enter(user32):
    alt, enter, soltar = 0x12, 0x0D, 0x0002
    user32.keybd_event(alt, 0, 0, 0)
    user32.keybd_event(enter, 0, 0, 0)
    user32.keybd_event(enter, 0, soltar, 0)
    user32.keybd_event(alt, 0, soltar, 0)


def _estructuras():
    import ctypes
    from ctypes import wintypes

    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    class FUENTE(ctypes.Structure):
        _fields_ = [("cbSize", wintypes.ULONG), ("nFont", wintypes.DWORD),
                    ("dwFontSize", COORD), ("FontFamily", ctypes.c_uint),
                    ("FontWeight", ctypes.c_uint), ("FaceName", ctypes.c_wchar * 32)]

    class BUFER(ctypes.Structure):
        _fields_ = [("dwSize", COORD), ("dwCursorPosition", COORD),
                    ("wAttributes", wintypes.WORD), ("srWindow", wintypes.SMALL_RECT),
                    ("dwMaximumWindowSize", COORD)]
    return COORD, FUENTE, BUFER


def _poner_fuente(alto):
    import ctypes
    COORD, FUENTE, _ = _estructuras()
    kernel32 = ctypes.windll.kernel32
    f = FUENTE()
    f.cbSize = ctypes.sizeof(FUENTE)
    f.nFont, f.dwFontSize, f.FontFamily, f.FontWeight = 0, COORD(0, alto), 54, 400
    f.FaceName = "Consolas"
    kernel32.SetCurrentConsoleFontEx(kernel32.GetStdHandle(-11), False, ctypes.byref(f))


def tamano_consola():
    """(columnas, filas) de la ventana visible de la consola, o (0, 0)."""
    if os.name != "nt":
        return 0, 0
    import ctypes
    _, _, BUFER = _estructuras()
    b = BUFER()
    if not ctypes.windll.kernel32.GetConsoleScreenBufferInfo(
            ctypes.windll.kernel32.GetStdHandle(-11), ctypes.byref(b)):
        return 0, 0
    return b.srWindow.Right - b.srWindow.Left + 1, b.srWindow.Bottom - b.srWindow.Top + 1


def igualar_bufer():
    """Búfer = ventana: si el búfer es más grande, se dibuja fuera de la vista."""
    if os.name != "nt":
        return
    import ctypes
    COORD, _, _ = _estructuras()
    cols, filas = tamano_consola()
    if cols and filas:
        ctypes.windll.kernel32.SetConsoleScreenBufferSize(
            ctypes.windll.kernel32.GetStdHandle(-11), COORD(cols, filas))


# ----------------------------------------------------------- calibración
def _teclas():
    if sys.platform == "darwin":
        return ["Cmd y +  agranda la letra · Cmd y −  la achica",
                "Ctrl+Cmd+F pone la ventana en pantalla completa"]
    if os.name == "nt":
        return ["Ctrl + rueda del ratón (consola) o Ctrl y + / Ctrl y − (Windows Terminal)",
                "Alt+Enter o F11 pone la ventana en pantalla completa"]
    return ["Ctrl+Shift y +  agranda la letra · Ctrl y −  la achica (GNOME, Konsole…)",
            "F11 pone la ventana en pantalla completa"]


def fuera_de_rango(alto, ancho):
    return not (RANGO_COLUMNAS[0] <= ancho <= RANGO_COLUMNAS[1]
                and RANGO_FILAS[0] <= alto <= RANGO_FILAS[1])


def calibrar(win, d, tr, forzar=False):
    """Pantalla para dejar la terminal de buen tamaño. Sale sola la primera vez
    si el tamaño está lejos de lo ideal; con N no vuelve a salir."""
    import curses
    if not forzar and os.path.exists(_archivo_aviso()):
        return
    alto, ancho = win.getmaxyx()
    if not forzar and not fuera_de_rango(alto, ancho):
        return
    while True:
        alto, ancho = win.getmaxyx()
        win.erase()
        # esquinas: si no se ven las cuatro, la ventana es más chica que el juego
        for y, x, ch in ((0, 0, "┌"), (0, ancho - 1, "┐"), (alto - 1, 0, "└"),
                         (alto - 1, ancho - 2, "┘")):
            d.put(win, y, x, ch, d.c("titulo", curses.A_BOLD))
        bien = not fuera_de_rango(alto, ancho)
        lineas = [
            tr("TAMAÑO DE LA PANTALLA"), "",
            tr("Ahora: {a} columnas × {b} filas").replace("{a}", str(ancho)).replace("{b}", str(alto)),
            tr("Ideal: entre {a} y {b} columnas, y al menos {c} filas")
            .replace("{a}", str(RANGO_COLUMNAS[0])).replace("{b}", str(RANGO_COLUMNAS[1]))
            .replace("{c}", str(RANGO_FILAS[0])), "",
            tr("¿Ves las 4 esquinas marcadas? Si falta alguna, la ventana es más grande que "
               "la pantalla: achica la letra."), "",
            tr("Muchas columnas: la letra es muy chica, agrándala."),
            tr("Pocas columnas: la letra es muy grande, achícala."), "",
        ] + [tr(t) for t in _teclas()] + ["",
            tr("Enter seguir · N no volver a mostrar") if bien else
            tr("Enter seguir así · N no volver a mostrar")]
        filas = []                              # (texto, color, negrita)
        for i, l in enumerate(lineas):
            color = ("titulo" if i == 0 else "bien" if (i == 2 and bien) else
                     "mal" if i == 2 else "texto")
            for trozo in d.envolver(l, max(10, ancho - 6)) if l else [""]:
                filas.append((trozo, color, i in (0, 2)))
        y0 = max(1, (alto - len(filas)) // 2)
        for i, (trozo, color, negrita) in enumerate(filas[: max(0, alto - 2)]):
            d.put(win, y0 + i, max(1, (ancho - len(trozo)) // 2), trozo,
                  d.c(color, curses.A_BOLD if negrita else 0))
        win.refresh()
        k = d.tecla(win)
        if d.es(k, "n"):
            try:
                open(_archivo_aviso(), "w", encoding="utf-8").write("no preguntar\n")
            except OSError:
                pass
            return
        if k in d.ENTER or k == d.ESC:
            return


def locale_utf8():
    """curses dibuja acentos y cajas solo con un locale UTF-8; con LANG=C (o
    sin LANG, como en algunos contenedores y servidores) se ven símbolos raros."""
    import locale
    try:
        locale.setlocale(locale.LC_ALL, "")
    except locale.Error:
        pass
    if "utf" in (locale.setlocale(locale.LC_CTYPE) or "").lower().replace("-", ""):
        return
    for nombre in ("C.UTF-8", "C.utf8", "en_US.UTF-8", "es_MX.UTF-8", "es_ES.UTF-8"):
        try:
            locale.setlocale(locale.LC_ALL, nombre)
            return
        except locale.Error:
            continue
