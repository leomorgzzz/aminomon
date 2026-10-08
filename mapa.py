"""Mapa de la célula (150×48). Se genera con geometría y una semilla fija, y
se dibuja con una cámara que sigue al jugador y llena toda la terminal."""

import curses
import math
import random

import dibujo as d

ANCHO, ALTO = 150, 48
CX, CY, RX, RY = 75, 24, 70, 21.5            # célula
NX, NY, NRX, NRY = 100, 22, 21, 9.5          # núcleo
NUCLEOLO = (104, 21, 5.5, 2.4)
MITOS = [(36, 15, 8, 2.4), (118, 35, 6, 2.0)]
LISOSOMAS = [(20, 26, 4, 1.8), (130, 20, 3.5, 1.6)]
GOLGI = (52, 28)
CENTROSOMA = (63, 31)

# carácter lógico -> (glifo, color, zona)
TILES = {
    " ": (" ", "texto", "citosol"),
    ",": ("·", "POL", "citosol"),
    "h": ("◦", "ARO", "interfase"),
    "~": ("≈", "NP", "membrana"),
    "N": (" ", "texto", "nucleo"),
    "c": ("§", "POS", "nucleo"),
    "u": ("▓", "POS", "nucleolo"),
    "=": ("█", "oscuro", None),
    "O": ("O", "mal", "nucleo"),
    "r": ("░", "NEG", "re"),
    "g": ("═", "POL", "golgi"),
    "m": ("·", "titulo", "mitocondria"),
    "l": ("●", "NEG", "lisosoma"),
    "b": ("∴", "POS", "ribosomas"),
    "e": (" ", "texto", "mec"),
    "x": ("╳", "tenue", "mec"),
}
PAREDES = {"="}
HIERBA = {",": "citosol", "h": "interfase", "~": "membrana", "c": "nucleo",
          "u": "nucleolo", "r": "re", "g": "golgi", "l": "lisosoma",
          "b": "ribosomas", "x": "mec"}

CARTELES = {
    "c_inicio": ((62, 22), "Bienvenida",
                 "Estás en el citosol. Las zonas con símbolos (· ≈ ◦ ∴ ░ ═ ● § ▓ ╳) "
                 "tienen aminoácidos salvajes. El panel de la derecha muestra "
                 "quién vive en cada zona. [M] abre el manual."),
    "c_poro": ((76, 21), "Envoltura nuclear",
               "Doble membrana con poros (O). Las moléculas pequeñas (< ~40 kDa) "
               "difunden; las proteínas grandes necesitan una señal de "
               "localización nuclear (NLS): un parche rico en Lys y Arg. Afuera "
               "solo hay Lys (en los polirribosomas ∴): con 4 basta para entrar, "
               "y adentro te espera la Arg."),
    "c_golgi": ((50, 24), "Aparato de Golgi",
                "Cara cis (hacia el RE) → cara trans (hacia la membrana). Las "
                "proteínas avanzan cisterna por cisterna mientras maduran sus "
                "glicanos."),
    "c_mito": ((36, 19), "Mitocondria",
               "Pisa sus crestas para recuperar la energía de tu equipo y "
               "recargar ATP."),
    "c_liso": ((25, 30), "Lisosoma",
               "La V-ATPasa bombea H⁺ al interior y baja el pH a ~5. A ese pH la His "
               "(pKR 6) está protonada: aquí cuenta como +."),
    "c_membrana": ((75, 6), "Bicapa lipídica",
                   "Cabezas polares (◦) hacia el agua, colas hidrofóbicas (≈) "
                   "hacia adentro. Mide ~30 Å: justo lo que cubre una hélice α "
                   "de ~20 residuos hidrofóbicos."),
    "c_mec": ((6, 8), "Matriz extracelular",
              "Colágeno, elastina y proteoglicanos secretados por los "
              "fibroblastos. El colágeno es la proteína más abundante del "
              "cuerpo."),
    "c_centro": ((CENTROSOMA[0] + 2, CENTROSOMA[1] + 1), "Centrosoma",
                 "De aquí salen los microtúbulos (─ │ ╱ ╲): rieles por los que "
                 "las vesículas viajan del Golgi a la membrana."),
    "c_ribo": ((52, 15), "Polirribosomas",
               "Varios ribosomas traduciendo el mismo ARNm. Sus proteínas "
               "ribosomales son ricas en Lys (K)."),
}


POROS = [(round(NX + (NRX - 1.3) * math.cos(a)), round(NY + (NRY - 0.65) * math.sin(a)))
         for a in (k * math.pi / 4 + math.pi / 8 for k in range(8))]


def _e(x, y, cx, cy, rx, ry):
    return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2


def generar():
    rnd = random.Random(42)
    t = [["e"] * ANCHO for _ in range(ALTO)]
    deco = {}

    def es(x, y, *chars):
        return 0 <= x < ANCHO and 0 <= y < ALTO and t[y][x] in chars

    # membrana y citosol
    for y in range(ALTO):
        for x in range(ANCHO):
            e0 = _e(x, y, CX, CY, RX, RY)
            if e0 > 1:
                continue
            if _e(x, y, CX, CY, RX - 5, RY - 2.7) > 1:
                cabeza = (_e(x, y, CX, CY, RX - 1.3, RY - 0.65) > 1 or
                          _e(x, y, CX, CY, RX - 3.7, RY - 1.85) <= 1)
                t[y][x] = "h" if cabeza else "~"
            else:
                t[y][x] = " "

    # núcleo: envoltura, poros, nucleoplasma
    for y in range(ALTO):
        for x in range(ANCHO):
            en = _e(x, y, NX, NY, NRX, NRY)
            if en > 1:
                continue
            if _e(x, y, NX, NY, NRX - 2.6, NRY - 1.3) > 1:
                poro = any(_e(x, y, px, py, 1.8, 1.4) <= 1 for px, py in POROS)
                t[y][x] = "O" if poro else "="
            else:
                t[y][x] = "N"
    for _ in range(9):
        bx = NX + rnd.randint(-14, 14)
        by = NY + rnd.randint(-5, 5)
        rx, ry = rnd.uniform(2.5, 4.5), rnd.uniform(1.0, 1.8)
        for y in range(ALTO):
            for x in range(ANCHO):
                if t[y][x] == "N" and _e(x, y, bx, by, rx, ry) <= 1:
                    t[y][x] = "c"
    for y in range(ALTO):
        for x in range(ANCHO):
            if t[y][x] in "Nc" and _e(x, y, *NUCLEOLO) <= 1:
                t[y][x] = "u"

    # mitocondrias y lisosomas
    for (mx, my, rx, ry) in MITOS:
        for y in range(ALTO):
            for x in range(ANCHO):
                if t[y][x] == " " and _e(x, y, mx, my, rx, ry) <= 1:
                    t[y][x] = "m"
    for (lx, ly, rx, ry) in LISOSOMAS:
        for y in range(ALTO):
            for x in range(ANCHO):
                if t[y][x] == " " and _e(x, y, lx, ly, rx, ry) <= 1:
                    t[y][x] = "l"

    # retículo endoplásmico: cisternas concéntricas pegadas a la envoltura
    for y in range(ALTO):
        for x in range(ANCHO):
            if t[y][x] != " " or x > NX + 8:
                continue
            r = math.sqrt(_e(x, y, NX, NY, NRX, NRY))
            if 1.1 < r < 1.75 and int((r - 1.1) * 14) % 3 != 2:
                t[y][x] = "r"

    # Golgi: cisternas curvas apiladas
    gx, gy = GOLGI
    for k in range(5):
        for dx in range(-8, 9):
            y = gy + 2 * k - round((dx / 8) ** 2 * 2)
            if es(gx + dx, y, " "):
                t[y][gx + dx] = "g"

    def manchas(lista, char, sobre):
        for (px, py, rx, ry) in lista:
            for y in range(ALTO):
                for x in range(ANCHO):
                    if t[y][x] in sobre and _e(x, y, px, py, rx, ry) <= 1:
                        t[y][x] = char

    manchas([(52, 12, 3.5, 1.3), (60, 9, 3, 1.2), (26, 33, 3, 1.2),
             (45, 39, 3.5, 1.2), (70, 41, 3, 1.1), (126, 28, 3, 1.3)], "b", " ")
    manchas([(16, 22, 5, 2.5), (44, 8, 7, 1.5), (40, 20, 8, 2.5), (31, 36, 6, 1.8),
             (66, 35, 4, 1.5), (110, 40, 5, 1.5), (136, 25, 3, 3),
             (88, 6, 6, 1.5), (58, 18, 4, 1.3)], ",", " ")
    manchas([(9, 4, 9, 3), (141, 4, 9, 3), (9, 44, 9, 3), (141, 44, 9, 3),
             (75, 0, 30, 1.6), (75, 47, 30, 1.2), (2, 24, 2, 6), (148, 24, 2, 6)],
            "x", "e")

    # decoración: microtúbulos desde el centrosoma
    cx, cy = CENTROSOMA
    deco[(cx, cy)] = ("*", "titulo")
    for k in range(12):
        a = k / 12 * 2 * math.pi + 0.15
        dx, dy = math.cos(a), math.sin(a) * 0.5
        if abs(dx) > 2.2 * abs(dy):
            g = "─"
        elif abs(dy) > 0.9 * abs(dx) * 0.5 and abs(dx) < 0.3:
            g = "│"
        else:
            g = "╲" if dx * dy > 0 else "╱"
        for paso in range(2, 30):
            x, y = round(cx + dx * paso), round(cy + dy * paso)
            if not es(x, y, " "):
                break
            if paso % 4 != 0:
                deco[(x, y)] = (g, "oscuro")
    # vesículas
    for _ in range(40):
        x, y = rnd.randrange(ANCHO), rnd.randrange(ALTO)
        if es(x, y, " ") and (x, y) not in deco:
            deco[(x, y)] = ("o", "tenue")
    # crestas mitocondriales y borde
    for y in range(ALTO):
        for x in range(ANCHO):
            if t[y][x] == "m":
                borde = any(not es(x + a, y + b, "m") for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                deco[(x, y)] = ("◉", "titulo") if borde else (("│" if x % 3 == 0 else "·"), "titulo")
            elif t[y][x] == "e" and rnd.random() < 0.05:
                deco[(x, y)] = ("·", "oscuro")
            elif t[y][x] == "N" and rnd.random() < 0.04:
                deco[(x, y)] = ("~", "oscuro")
    return t, deco


MAPA, DECO = generar()


def tile(x, y):
    if 0 <= x < ANCHO and 0 <= y < ALTO:
        return MAPA[y][x]
    return None


def zona(x, y):
    t = tile(x, y)
    return TILES[t][2] if t else None


def transitable(x, y):
    t = tile(x, y)
    return t is not None and t not in PAREDES


def _cercano(objetivo, chars):
    ox, oy = objetivo
    mejor, dist = None, 1e9
    for y in range(ALTO):
        for x in range(ANCHO):
            if MAPA[y][x] in chars:
                dd = (x - ox) ** 2 + ((y - oy) * 2) ** 2
                if dd < dist:
                    mejor, dist = (x, y), dd
    return mejor


# Puntos especiales: nombre -> (x, y, glifo)
_ESPECIALES_OBJ = {
    "ribosoma": ((58, 24), " ", "R"),
    "chaperona": ((70, 27), " ", "H"),
    "jefe_membrana": ((75, 3), "~", "J"),
    "jefe_citosol": ((40, 20), ",", "J"),
    "jefe_re": ((80, 35), "r", "J"),
    "jefe_golgi": ((52, 31), "g", "J"),
    "jefe_lisosoma": ((20, 26), "l", "J"),
    "jefe_mec": ((8, 44), "x", "J"),
    "vit_c": ((142, 4), "x", "C"),
    "vit_k": ((68, 16), "r", "K"),
}
ESPECIALES = {}
for _n, (_obj, _chars, _g) in _ESPECIALES_OBJ.items():
    _x, _y = _cercano(_obj, _chars)
    ESPECIALES[_n] = (_x, _y, _g)
for _n, (_obj, _t, _txt) in CARTELES.items():
    _x, _y = _cercano(_obj, " e")
    ESPECIALES[_n] = (_x, _y, "i")
    DECO.pop((_x, _y), None)
for _n, (_x, _y, _g) in ESPECIALES.items():
    DECO.pop((_x, _y), None)
INICIO = (ESPECIALES["ribosoma"][0] + 2, ESPECIALES["ribosoma"][1])
CENTRO_MITO = (MITOS[0][0], MITOS[0][1])


def especial_en(x, y):
    for nombre, (ex, ey, _) in ESPECIALES.items():
        if (ex, ey) == (x, y):
            return nombre
    return None


def glifo(x, y, juego):
    """(glifo, color) de una casilla del mundo, sin contar al jugador."""
    t = MAPA[y][x]
    g, color, _ = TILES[t]
    if (x, y) in DECO:
        g, color = DECO[(x, y)]
    if t == "O":
        color = "bien" if "nucleo" in juego["insignias"] else "mal"
    return g, color


# Fondo gris (R=G=B) de cada compartimento: sombrea los organelos sin teñirlos
FONDO = {"N": 236, "c": 236, "u": 237, "O": 236, "m": 237, "l": 237, "~": 235, "h": 235}


def fondo(x, y):
    return FONDO.get(MAPA[y][x])


def _attr_especial(nombre, juego):
    if nombre.startswith("jefe"):
        if nombre[5:] in juego["insignias"]:
            return "✓", d.c("bien", curses.A_BOLD)
        return None, d.c("mal", curses.A_BOLD | curses.A_REVERSE)
    if nombre.startswith("c_"):
        return None, d.c("agua", curses.A_BOLD)
    if nombre == "chaperona" and juego.get("terminado"):
        return None, d.c("bien", curses.A_BOLD)
    return None, d.c("titulo", curses.A_BOLD | curses.A_REVERSE)


def camara(juego, vh, vw):
    px, py = juego["pos"]
    cx = 0 if vw >= ANCHO else max(0, min(px - vw // 2, ANCHO - vw))
    cy = 0 if vh >= ALTO else max(0, min(py - vh // 2, ALTO - vh))
    return cx, cy


def dibujar(win, oy, ox, vh, vw, juego):
    """Dibuja la vista de la cámara en el rectángulo (oy, ox, vh, vw)."""
    cx, cy = camara(juego, vh, vw)
    # si el mundo cabe entero, se centra
    mx = max(0, (vw - ANCHO) // 2)
    my = max(0, (vh - ALTO) // 2)
    filas = min(vh, ALTO)
    cols = min(vw, ANCHO)
    for fy in range(filas):
        y = cy + fy
        corrida, clave_c, x0 = [], None, 0
        for fx in range(cols):
            g, color = glifo(cx + fx, y, juego)
            clave = (color, fondo(cx + fx, y))
            if clave != clave_c and corrida:
                d.put(win, oy + my + fy, ox + mx + x0, "".join(corrida), d.c(clave_c[0], fondo=clave_c[1]))
                corrida, x0 = [], fx
            clave_c = clave
            corrida.append(g)
        if corrida:
            d.put(win, oy + my + fy, ox + mx + x0, "".join(corrida), d.c(clave_c[0], fondo=clave_c[1]))
    for nombre, (x, y, g) in ESPECIALES.items():
        if cx <= x < cx + cols and cy <= y < cy + filas:
            otro, attr = _attr_especial(nombre, juego)
            d.put(win, oy + my + y - cy, ox + mx + x - cx, otro or g, attr)
    px, py = juego["pos"]
    d.put(win, oy + my + py - cy, ox + mx + px - cx, "@",
          d.c("texto", curses.A_BOLD | curses.A_REVERSE))


MINI_COLOR = {"membrana": "NP", "interfase": "ARO", "citosol": "oscuro",
              "ribosomas": "POS", "nucleo": "POS", "nucleolo": "POS", "re": "NEG",
              "golgi": "POL", "lisosoma": "NEG", "mec": "oscuro",
              "mitocondria": "titulo"}


def minimapa(win, y0, x0, h, w, juego):
    """Mapa completo reducido."""
    px, py = juego["pos"]
    for fy in range(h):
        for fx in range(w):
            x = int((fx + 0.5) * ANCHO / w)
            y = int((fy + 0.5) * ALTO / h)
            t = MAPA[y][x]
            if t == "=":
                g, col = "█", "oscuro"
            elif t in ("e", "x"):
                g, col = ("░" if t == "x" else " "), "oscuro"
            elif t == " ":
                g, col = " ", "oscuro"
            else:
                g, col = "█", MINI_COLOR[TILES[t][2]]
            d.put(win, y0 + fy, x0 + fx, g, d.c(col))
    mxp = min(w - 1, int(px * w / ANCHO))
    myp = min(h - 1, int(py * h / ALTO))
    d.put(win, y0 + myp, x0 + mxp, "@", d.c("texto", curses.A_BOLD | curses.A_REVERSE))
