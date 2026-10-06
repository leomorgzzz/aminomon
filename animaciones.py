"""Animaciones de combate en la "arena" (un recuadro entre los combatientes).

Cada generador recibe (alto, ancho, ctx) y devuelve una lista de cuadros;
cada cuadro es una lista de (fila, columna, texto, color). La última fila de
la arena se usa como subtítulo que explica qué está pasando.
"""

import curses
import math
import random

import dibujo as d

# ms por cuadro, ms de pausa final
VELOCIDADES = {"lenta": (140, 1800), "normal": (75, 900), "rápida": (30, 250)}
ORDEN_VEL = ["lenta", "normal", "rápida"]


# ------------------------------------------------------------- utilidades
def _centro(w, texto):
    return max(0, (w - len(texto)) // 2)


def _lerp(a, b, t):
    return round(a + (b - a) * t)


def _sub(h, w, texto, color="tenue"):
    """Subtítulo en la última fila."""
    return (h - 1, _centro(w, texto), texto, color)


def _acercar(h, w, izq, der, ci, cd, n=12, hueco=5, fila=None, sub=None):
    """Dos etiquetas que se acercan desde los bordes hasta dejar un hueco."""
    y = h // 2 - 1 if fila is None else fila
    fin_i = w // 2 - hueco // 2 - len(izq)
    fin_d = w // 2 + (hueco + 1) // 2
    cuadros = []
    for i in range(n + 1):
        t = 1 - (1 - i / n) ** 2          # desaceleración
        xi = _lerp(1, fin_i, t)
        xd = _lerp(w - len(der) - 1, fin_d, t)
        c = [(y, xi, izq, ci), (y, xd, der, cd)]
        if sub:
            c.append(_sub(h, w, sub))
        cuadros.append(c)
    return cuadros, (y, fin_i, fin_d)


def _sin_sub(cuadro, h):
    return [c for c in cuadro if c[0] != h - 1]


def _final(cuadros, h, w, texto, color="titulo"):
    ultimo = _sin_sub(cuadros[-1], h) if cuadros else []
    cuadros.append(ultimo + [_sub(h, w, texto, color)])
    return cuadros


# ------------------------------------------------- interacciones entre R
def salino(h, w, ctx):
    izq, der = ctx["mio"], ctx["rival"]
    cuadros, (y, fi, fd) = _acercar(h, w, izq, der, ctx["color_mio"], ctx["color_rival"],
                                    sub="dos grupos con carga opuesta se atraen")
    base = _sin_sub(cuadros[-1], h)
    for i in range(1, 7):
        puntos = "·" * max(1, min(i, fd - fi - len(izq) - 2))
        cuadros.append(base + [
            (y - 1, fi + len(izq) - 1, ctx["carga_mio"], ctx["color_mio"]),
            (y - 1, fd, ctx["carga_rival"], ctx["color_rival"]),
            (y, fi + len(izq) + 1, puntos, "titulo"),
            _sub(h, w, "atracción electrostática entre + y −"),
        ])
    return _final(cuadros, h, w, ctx.get("nombre", "puente salino"))


def repulsion(h, w, ctx):
    izq, der = ctx["mio"], ctx["rival"]
    cuadros, (y, fi, fd) = _acercar(h, w, izq, der, ctx["color_mio"], ctx["color_rival"],
                                    n=9, hueco=9, sub="se acercan dos grupos con la MISMA carga…")
    for i in range(1, 8):
        cuadros.append([(y, fi - i * 2, izq, ctx["color_mio"]),
                        (y, fd + i * 2, der, ctx["color_rival"]),
                        (y - 1, max(0, fi - i * 2 + len(izq) - 1), ctx["carga_mio"], "mal"),
                        (y - 1, fd + i * 2, ctx["carga_rival"], "mal"),
                        (y, w // 2 - 3, "⟵ ✕ ⟶", "mal"),
                        _sub(h, w, "cargas iguales se repelen")])
    return _final(cuadros, h, w, ctx.get("nombre", "repulsión electrostática"), "mal")


def hidrofobico(h, w, ctx):
    izq, der = ctx["mio"], ctx["rival"]
    rnd = random.Random(5)
    cx, cy = w // 2, h // 2 - 1
    aguas = [(k / 12 * 2 * math.pi, 0.85 + rnd.random() * 0.3) for k in range(12)]
    cuadros = []
    n = 16
    fin_i, fin_d = cx - 1 - len(izq), cx + 1
    for i in range(n + 1):
        t = i / n
        xi = _lerp(1, fin_i, t)
        xd = _lerp(w - len(der) - 1, fin_d, t)
        c = [(cy, xi, izq, ctx["color_mio"]), (cy, xd, der, ctx["color_rival"])]
        for ang, r in aguas:
            rr = r * (0.5 + t * 0.9)
            ax = cx + int(math.cos(ang) * rr * w * 0.36)
            ay = cy + int(math.sin(ang) * rr * h * 0.45)
            if 0 <= ay < h - 1 and 0 <= ax < w - 3 and ay != cy:
                c.append((ay, ax, "H₂O", "agua"))
        texto = ("cada cadena no polar está rodeada de agua ordenada" if t < 0.5
                 else "al juntarse, esa agua ordenada queda libre")
        c.append(_sub(h, w, texto))
        cuadros.append(c)
    return _final(cuadros, h, w, ctx.get("nombre", "efecto hidrofóbico: ↑ entropía del agua"))


def solvatacion(h, w, ctx):
    """No polar con polar/cargado: el agua se queda pegada al grupo polar."""
    izq, der = ctx["mio"], ctx["rival"]
    cuadros, (y, fi, fd) = _acercar(h, w, izq, der, ctx["color_mio"], ctx["color_rival"],
                                    n=10, hueco=13, sub="intentan juntarse…")
    polar_der = ctx.get("polar_lado", "der") == "der"
    base = _sin_sub(cuadros[-1], h)
    posiciones = [(-1, 0), (1, 0), (-1, 4), (1, 4), (0, -5)]
    for i in range(1, 8):
        capa = []
        for dy, dx in posiciones[: 1 + i // 2]:
            if polar_der:
                capa.append((y + dy, fd - 1 + dx, "H₂O", "agua"))
            else:
                capa.append((y + dy, fi + len(izq) - 3 - dx, "H₂O", "agua"))
        cuadros.append(base + capa + [_sub(h, w, "el agua forma una capa alrededor del grupo polar")])
    return _final(cuadros, h, w, ctx.get("nombre", "el agua los mantiene separados"), "tenue")


def puente_h(h, w, ctx):
    izq, der = ctx["hb_izq"], ctx["hb_der"]
    cuadros, (y, fi, fd) = _acercar(h, w, izq, der, ctx["color_mio"], ctx["color_rival"],
                                    hueco=5, sub="un H unido a O o N se acerca a otro O o N")
    base = _sin_sub(cuadros[-1], h)
    don_izq = ctx.get("donador") == "izq"
    for i in range(1, 6):
        cuadros.append(base + [
            (y, fi + len(izq) + 1, "·" * min(i, 3), "titulo"),
            (y - 1, fi + len(izq) - 1, "δ+" if don_izq else "δ−", "tenue"),
            (y - 1, fd, "δ−" if don_izq else "δ+", "tenue"),
            _sub(h, w, "H (δ+) del donador ··· par libre (δ−) del aceptor"),
        ])
    return _final(cuadros, h, w, ctx.get("nombre", "puente de hidrógeno"))


def sin_puente_h(h, w, ctx):
    izq, der = ctx["hb_izq"], ctx["hb_der"]
    cuadros, (y, fi, fd) = _acercar(h, w, izq, der, ctx["color_mio"], ctx["color_rival"],
                                    hueco=7, sub="se acercan…")
    base = _sin_sub(cuadros[-1], h)
    for i in range(6):
        cuadros.append(base + [(y, w // 2 - 1, "✕" if i % 2 == 0 else " ", "mal"),
                               _sub(h, w, ctx.get("motivo", "falta un donador o un aceptor"), "mal")])
    return _final(cuadros, h, w, ctx.get("nombre", "no se forma puente de H"), "mal")


ANILLO = [" __ ", "/  \\", "\\__/"]


def pi(h, w, ctx):
    cy = max(0, h // 2 - 3)
    cuadros = []
    n = 14
    cx = w // 2 - 2
    for i in range(n + 1):
        t = i / n
        xi = _lerp(1, cx - 2, t)
        xd = _lerp(w - 6, cx + 1, t)
        yd = cy + 1 - round(t)
        c = []
        for k, l in enumerate(ANILLO):
            c.append((cy + 1 + k, xi, l, ctx["color_mio"]))
            c.append((yd + k, xd, l, ctx["color_rival"]))
        c.append(_sub(h, w, "dos anillos aromáticos se acercan"))
        cuadros.append(c)
    base = _sin_sub(cuadros[-1], h)
    for i in range(5):
        cuadros.append(base + [(cy + 4, cx + 6, "← ~3.5 Å" if i % 2 == 0 else "", "tenue"),
                               _sub(h, w, "se apilan cara a cara, desplazados")])
    return _final(cuadros, h, w, ctx.get("nombre", "apilamiento π–π"))


def cation_pi(h, w, ctx):
    cx = w // 2 - 2
    base_y = max(2, h - 4)
    cuadros = []
    for i in range(base_y - 1):
        c = [(base_y + k, cx, l, ctx["color_anillo"]) for k, l in enumerate(ANILLO) if base_y + k < h - 1]
        c.append((i, cx - 1, ctx["cation"], ctx["color_cation"]))
        c.append(_sub(h, w, "un catión baja hacia la cara del anillo"))
        cuadros.append(c)
    base = _sin_sub(cuadros[-1], h)
    for i in range(5):
        cuadros.append(base + [(base_y - 1, cx + 7, "+···π" if i % 2 == 0 else "", "titulo"),
                               _sub(h, w, "la nube π (rica en electrones) atrae la carga +")])
    return _final(cuadros, h, w, ctx.get("nombre", "interacción catión–π"))


def oh_pi(h, w, ctx):
    cx = w // 2 - 2
    base_y = max(2, h - 4)
    cuadros = []
    for i in range(base_y - 1):
        c = [(base_y + k, cx, l, ctx["color_anillo"]) for k, l in enumerate(ANILLO) if base_y + k < h - 1]
        c.append((i, cx, ctx["donador_txt"], ctx["color_donador"]))
        c.append(_sub(h, w, "un X–H apunta hacia la cara del anillo"))
        cuadros.append(c)
    base = _sin_sub(cuadros[-1], h)
    for i in range(4):
        cuadros.append(base + [(base_y - 1, cx + 7, "H···π" if i % 2 == 0 else "", "titulo"),
                               _sub(h, w, "puente de H débil: la nube π hace de aceptor")])
    return _final(cuadros, h, w, ctx.get("nombre", "puente de H X–H···π"))


def vdw(h, w, ctx):
    izq, der = ctx["mio"], ctx["rival"]
    cuadros, (y, fi, fd) = _acercar(h, w, izq, der, ctx["color_mio"], ctx["color_rival"],
                                    hueco=3, sub="dos grupos se acercan hasta casi tocarse")
    base = _sin_sub(cuadros[-1], h)
    for i in range(8):
        signos = ("δ+", "δ−") if i % 2 == 0 else ("δ−", "δ+")
        cuadros.append(base + [(y - 1, fi, signos[0], "tenue"),
                               (y - 1, fd + len(der) - 2, signos[1], "tenue"),
                               _sub(h, w, "un dipolo instantáneo induce otro en el vecino")])
    return _final(cuadros, h, w, ctx.get("nombre", "fuerzas de London (van der Waals)"))


def esqueleto(h, w, ctx):
    y = max(0, h // 2 - 2)
    largo = w - 10
    arriba = ("─N─Cα─C─" * 20)[:largo]
    abajo = ("─C─Cα─N─" * 20)[:largo]
    cuadros = []
    for i in range(1, 9):
        n = largo * i // 8
        cuadros.append([(y, 4, arriba[:n], ctx["color_mio"]), (y + 3, 4, abajo[:n], ctx["color_rival"]),
                        _sub(h, w, "dos esqueletos peptídicos se alinean")])
    base = _sin_sub(cuadros[-1], h)
    for i in range(6):
        enlaces = []
        for k in range(1, largo - 2, 8):
            if (k // 8 + i) % 2 == 0 or i > 3:
                enlaces += [(y + 1, 4 + k, "H", "tenue"), (y + 2, 4 + k, "⁞", "titulo")]
        cuadros.append(base + enlaces + [_sub(h, w, "N–H de un esqueleto ··· O═C del otro")])
    return _final(cuadros, h, w, ctx.get("nombre", "puentes de H del esqueleto"))




def disulfuro(h, w, ctx):
    izq, der = "Cys─SH", "HS─Cys"
    cuadros, (y, fi, fd) = _acercar(h, w, izq, der, ctx["color_mio"], ctx["color_rival"],
                                    hueco=1, sub="dos tioles (SH) se acercan")
    for i in range(1, 7):
        cuadros.append([(y, fi, "Cys─S ", ctx["color_mio"]), (y, fd, " S─Cys", ctx["color_rival"]),
                        (max(0, y - i), fi + 5, "H", "agua"), (max(0, y - i), fd, "H", "agua"),
                        _sub(h, w, "se oxidan: salen 2H⁺ + 2e⁻")])
    final = [(y, w // 2 - 6, "Cys─S─S─Cys", "titulo"), (0, 1, "2H⁺ + 2e⁻", "tenue")]
    cuadros.append(final + [_sub(h, w, "enlace covalente S–S (cistina)", "titulo")])
    return cuadros




























def agitacion(h, w, ctx):
    y = h // 2 - 1
    cuadros = []
    for i in range(10):
        olas = "".join("≈ "[(k + i) % 2] for k in range(w - 4))
        cuadros.append([(y - 1, 2, olas, "mal"), (y + 1, 2, olas[::-1], "mal"),
                        (y, _centro(w, "agitación térmica"), "agitación térmica", "mal"),
                        _sub(h, w, "el movimiento térmico desordena tus interacciones")])
    return cuadros


def trna(h, w, ctx):
    """El ARNt sube y su anticodón se aparea con el codón del ARNm."""
    cod = ctx["codon"]
    anti = "".join({"A": "U", "U": "A", "G": "C", "C": "G"}[b] for b in cod)
    arn = f"5'─···─{cod}─···─3'"
    xa = _centro(w, arn)
    xc = xa + 6
    # anticodón arriba; el aminoácido va unido al extremo 3' (CCA), abajo
    figura = [(anti, "titulo"), ("└┬┘", "agua"), ("│ │", "agua"), ("┌┴┐", "agua"),
              (" │", "agua"), (ctx["tres"], ctx["color_rival"])]
    cuadros = []
    for paso in range(h - 1, 0, -1):
        c = [(0, xa, arn, "texto"), (0, xc, cod, "titulo")]
        for k, (l, color) in enumerate(figura):
            if 1 <= paso + k < h - 1:
                c.append((paso + k, xc, l, color))
        c.append(_sub(h, w, f"el ARNt trae la {ctx['tres']} unida a su extremo 3'"))
        cuadros.append(c)
    final = [(0, xa, arn, "texto"), (0, xc, cod, "bien"),
             (1, xc, "│││", "bien"), (2, xc, anti, "bien"),
             (1, xc + 5, f"codón     5'-{cod}-3'", "tenue"),
             (2, xc + 5, f"anticodón 3'-{anti}-5'", "tenue")]
    cuadros.append(final + [_sub(h, w, "bases complementarias y antiparalelas: A·U, G·C", "titulo")])
    return cuadros


ANIMACIONES = {
    "salino": salino, "repulsion": repulsion, "hidrofobico": hidrofobico,
    "solvatacion": solvatacion, "puente_h": puente_h, "sin_puente_h": sin_puente_h,
    "pi": pi, "cation_pi": cation_pi, "oh_pi": oh_pi, "vdw": vdw,
    "esqueleto": esqueleto, "disulfuro": disulfuro, "agitacion": agitacion,
    "trna": trna,
}


# ------------------------------------------------------------ reproductor
def reproducir(win, y, x, h, w, nombre, ctx, velocidad="lenta"):
    """Reproduce una animación dentro del rectángulo. Una tecla la salta."""
    pausa, espera = VELOCIDADES.get(velocidad, VELOCIDADES["lenta"])
    cuadros = ANIMACIONES.get(nombre, vdw)(h, w, ctx)
    win.nodelay(True)
    try:
        saltar = False
        for cuadro in cuadros:
            dibujar_cuadro(win, y, x, h, w, cuadro)
            win.refresh()
            if win.getch() != -1:
                saltar = True
                break
            curses.napms(pausa)
        if cuadros:
            dibujar_cuadro(win, y, x, h, w, cuadros[-1])
            win.refresh()
        if not saltar:
            # pausa final para leer el resultado (también se puede saltar)
            for _ in range(espera // 50):
                if win.getch() != -1:
                    break
                curses.napms(50)
    finally:
        win.nodelay(False)
    return cuadros[-1] if cuadros else []


def dibujar_cuadro(win, y, x, h, w, cuadro):
    for i in range(h):
        d.put(win, y + i, x, " " * w)
    for fy, fx, texto, color in cuadro:
        if 0 <= fy < h and fx < w:
            d.put(win, y + fy, x + max(0, fx), texto[: max(0, w - max(0, fx))], d.c(color))


def sacudir(win, y, x, arte, color, veces=4):
    """Sacude un sprite horizontalmente."""
    ancho = max(len(l) for l in arte) + 2
    win.nodelay(True)
    try:
        for i in range(veces * 2):
            dx = 1 if i % 2 == 0 else -1
            for k, l in enumerate(arte):
                d.put(win, y + k, max(0, x - 1), " " * ancho)
                d.put(win, y + k, max(0, x + dx), l, d.c(color))
            win.refresh()
            if win.getch() != -1:
                break
            curses.napms(60)
        for k, l in enumerate(arte):
            d.put(win, y + k, max(0, x - 1), " " * ancho)
            d.put(win, y + k, x, l, d.c(color))
        win.refresh()
    finally:
        win.nodelay(False)


def destello(win, y, x, arte_a, arte_b, color_a, color_b, veces=5):
    """Alterna entre dos sprites (modificación postraduccional)."""
    alto = max(len(arte_a), len(arte_b))
    ancho = max(len(l) for l in arte_a + arte_b) + 1
    for i in range(veces * 2 + 1):
        arte, color = (arte_a, color_a) if i % 2 == 0 else (arte_b, color_b)
        if i == veces * 2:
            arte, color = arte_b, color_b
        for k in range(alto):
            d.put(win, y + k, x, " " * ancho)
        for k, l in enumerate(arte):
            d.put(win, y + k, x, l, d.c(color, curses.A_BOLD if i % 2 else 0))
        win.refresh()
        curses.napms(160 + i * 30)


def transicion(win):
    """Barrido de pantalla al empezar un combate: bandas que se cierran desde
    arriba y abajo con los colores de los cinco grupos."""
    alto, ancho = win.getmaxyx()
    colores = ["NP", "ARO", "POL", "POS", "NEG"]
    pasos = (alto + 1) // 2
    for i in range(pasos):
        color = colores[i % len(colores)]
        for fila in (i, alto - 1 - i):
            d.put(win, fila, 0, "▀▄" * (ancho // 2), d.c(color))
        win.refresh()
        curses.napms(18)
    curses.napms(120)
    win.erase()
    win.refresh()
