"""Colores, cajas, barras, menús y ventanas emergentes con curses."""

import curses
import textwrap

# Paleta: grises neutros + acentos desaturados (índices xterm-256).
# (color 256, respaldo de 8 colores)
_PALETA = {
    "texto": (254, curses.COLOR_WHITE),
    "tenue": (245, curses.COLOR_WHITE),
    "oscuro": (240, curses.COLOR_WHITE),
    "titulo": (187, curses.COLOR_YELLOW),
    "NP": (144, curses.COLOR_YELLOW),
    "ARO": (139, curses.COLOR_MAGENTA),
    "POL": (108, curses.COLOR_GREEN),
    "NEG": (138, curses.COLOR_RED),
    "POS": (103, curses.COLOR_BLUE),
    "NEU": (247, curses.COLOR_WHITE),
    "agua": (109, curses.COLOR_CYAN),
    "bien": (108, curses.COLOR_GREEN),
    "mal": (138, curses.COLOR_RED),
}
_PARES = {}

COLOR_GRUPO = {
    "alifatico": "NP", "aromatico": "ARO", "polar": "POL",
    "acido": "NEG", "basico": "POS",
}


def init_colores():
    curses.start_color()
    try:
        curses.use_default_colors()
        fondo = -1
    except curses.error:
        fondo = curses.COLOR_BLACK
    muchos = curses.COLORS >= 256
    for i, (nombre, (c256, c8)) in enumerate(_PALETA.items(), start=1):
        curses.init_pair(i, c256 if muchos else c8, fondo)
        _PARES[nombre] = i


def c(nombre, extra=0):
    if nombre in _PARES:
        attr = curses.color_pair(_PARES[nombre])
        if nombre in ("tenue", "oscuro") and curses.COLORS < 256:
            attr |= curses.A_DIM
        return attr | extra
    return extra


def etiqueta_tipos(win, y, x, tipos, corto=False):
    """Dibuja [Tipo][Tipo] con el color de cada tipo. Devuelve el ancho usado."""
    import datos
    cx = x
    for t in tipos:
        nombre = datos.TIPOS[t]["corto" if corto else "nombre"] if t in datos.TIPOS else "Neutro"
        texto = f"[{nombre}]"
        put(win, y, cx, texto, c(t, curses.A_BOLD))
        cx += len(texto)
    return cx - x


def put(win, y, x, texto, attr=0):
    """addstr que recorta al tamaño de la ventana y nunca revienta."""
    alto, ancho = win.getmaxyx()
    if y < 0 or y >= alto or x >= ancho:
        return
    texto = str(texto)[: max(0, ancho - x - (1 if y == alto - 1 else 0))]
    try:
        win.addstr(y, x, texto, attr)
    except curses.error:
        pass


def caja(win, y, x, h, w, titulo=None, attr=None):
    attr = c("tenue") if attr is None else attr
    put(win, y, x, "┌" + "─" * (w - 2) + "┐", attr)
    for i in range(1, h - 1):
        put(win, y + i, x, "│", attr)
        put(win, y + i, x + w - 1, "│", attr)
    put(win, y + h - 1, x, "└" + "─" * (w - 2) + "┘", attr)
    if titulo:
        put(win, y, x + 2, f" {titulo} ", c("titulo", curses.A_BOLD))


def limpiar_area(win, y, x, h, w):
    for i in range(h):
        put(win, y + i, x, " " * w)


def barra(win, y, x, ancho, valor, maximo, attr):
    llenos = 0 if maximo <= 0 else round(ancho * max(0, min(valor, maximo)) / maximo)
    put(win, y, x, "█" * llenos, attr)
    put(win, y, x + llenos, "░" * (ancho - llenos), c("tenue"))


def estructura(win, y, x, lineas, attr=None):
    attr = c("texto") if attr is None else attr
    for i, l in enumerate(lineas):
        put(win, y + i, x, l, attr)


def envolver(texto, ancho):
    salida = []
    for parrafo in str(texto).split("\n"):
        salida.extend(textwrap.wrap(parrafo, ancho) or [""])
    return salida


def tecla(win):
    """Lee una tecla; devuelve int de curses o str de un carácter."""
    while True:
        try:
            return win.get_wch()
        except curses.error:
            continue


def es(k, *opciones):
    """Compara una tecla con caracteres (sin importar mayúsculas) o códigos."""
    for o in opciones:
        if isinstance(o, str) and isinstance(k, str) and k.lower() == o.lower():
            return True
        if isinstance(o, int) and k == o:
            return True
    return False


ESC = "\x1b"
ENTER = ("\n", "\r", curses.KEY_ENTER)


def popup(win, texto, titulo=None, ancho=60, attr=None, esperar=True):
    """Ventana centrada con texto; espera una tecla."""
    alto_p, ancho_p = win.getmaxyx()
    ancho = min(ancho, ancho_p - 2)
    lineas = envolver(texto, ancho - 4)
    h = min(len(lineas) + 4, alto_p - 1)
    y0 = max(0, (alto_p - h) // 2)
    x0 = max(0, (ancho_p - ancho) // 2)
    limpiar_area(win, y0, x0, h, ancho)
    caja(win, y0, x0, h, ancho, titulo)
    for i, l in enumerate(lineas[: h - 4]):
        put(win, y0 + 1 + i, x0 + 2, l, attr if attr is not None else c("texto"))
    if esperar:
        put(win, y0 + h - 2, x0 + ancho - 18, "[Enter] seguir", c("tenue"))
        win.refresh()
        while True:
            k = tecla(win)
            if k != curses.KEY_RESIZE:
                return k
    win.refresh()


def dialogo(win, paginas, titulo=None):
    for p in paginas:
        win.erase()
        popup(win, p, titulo)


def menu(win, titulo, opciones, y=None, x=None, ancho=None, ayuda=None,
         inicial=0):
    """Menú vertical. opciones: lista de str. Devuelve índice o None (Esc)."""
    alto_p, ancho_p = win.getmaxyx()
    ancho = ancho or min(max([len(o) for o in opciones] + [len(titulo or "")]) + 8,
                         ancho_p - 2)
    h = min(len(opciones) + 2 + (2 if ayuda else 0), alto_p - 1)
    y = (alto_p - h) // 2 if y is None else y
    x = (ancho_p - ancho) // 2 if x is None else x
    sel = inicial
    visibles = h - 2 - (2 if ayuda else 0)
    while True:
        limpiar_area(win, y, x, h, ancho)
        caja(win, y, x, h, ancho, titulo)
        inicio = max(0, min(sel - visibles + 1, len(opciones) - visibles))
        inicio = max(0, min(inicio, sel))
        for i, o in enumerate(opciones[inicio:inicio + visibles]):
            idx = inicio + i
            marca = "▸ " if idx == sel else "  "
            attr = c("titulo", curses.A_BOLD) if idx == sel else c("texto")
            put(win, y + 1 + i, x + 2, (marca + o)[: ancho - 4], attr)
        if ayuda:
            put(win, y + h - 2, x + 2, ayuda[: ancho - 4], c("tenue"))
        win.refresh()
        k = tecla(win)
        if es(k, curses.KEY_UP, "k", "w"):
            sel = (sel - 1) % len(opciones)
        elif es(k, curses.KEY_DOWN, "j", "s"):
            sel = (sel + 1) % len(opciones)
        elif k in ENTER or k == " ":
            return sel
        elif k == ESC or es(k, "q"):
            return None
        elif isinstance(k, str) and k.isdigit() and 1 <= int(k) <= len(opciones):
            return int(k) - 1


def pedir_texto(win, y, x, prompt, largo=10, attr=None):
    """Campo de texto simple. Devuelve str o None si se pulsa Esc."""
    texto = ""
    curses.curs_set(1)
    try:
        while True:
            put(win, y, x, prompt, attr if attr is not None else c("texto"))
            put(win, y, x + len(prompt), texto + " " * (largo - len(texto)),
                c("titulo", curses.A_BOLD | curses.A_UNDERLINE))
            try:
                win.move(y, x + len(prompt) + len(texto))
            except curses.error:
                pass
            win.refresh()
            k = tecla(win)
            if k in ENTER:
                return texto
            if k == ESC:
                return None
            if k in (curses.KEY_BACKSPACE, "\x7f", "\b", 127, 8):
                texto = texto[:-1]
            elif isinstance(k, str) and k.isprintable() and len(texto) < largo:
                texto += k
    finally:
        curses.curs_set(0)
