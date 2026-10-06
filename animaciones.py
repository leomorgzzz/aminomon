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


def esqueleto_triple(h, w, ctx):
    y = max(0, h // 2 - 2)
    largo = w - 8
    cuadros = []
    for i in range(1, 10):
        n = largo * i // 9
        filas = []
        for k, col in enumerate((ctx["color_mio"], "tenue", ctx["color_rival"])):
            filas.append((y + k, 4, "".join("╲╱"[(j + k) % 2] for j in range(n)), col))
        cuadros.append(filas + [_sub(h, w, "tres cadenas Gly–X–Y se enrollan")])
    return _final(cuadros, h, w, ctx.get("nombre", "triple hélice: N–H de Gly ··· O═C de otra cadena"))


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


def enlace(h, w, ctx):
    izq, der = ctx["mio"], ctx["rival"]
    cuadros, (y, fi, fd) = _acercar(h, w, izq, der, ctx["color_mio"], ctx["color_rival"],
                                    hueco=3, sub="dos grupos se acercan")
    base = _sin_sub(cuadros[-1], h)
    for i in range(5):
        cuadros.append(base + [(y, fi + len(izq), "═══" if i % 2 == 0 else "───", "titulo"),
                               _sub(h, w, "se forma un enlace entre fibras")])
    return _final(cuadros, h, w, ctx.get("nombre", "entrecruzamiento"))


# ------------------------------------------- cambios sobre tu aminoácido
def fosforilar(h, w, ctx):
    y = h // 2 - 1
    xa, xo = 2, w - 8
    cuadros = []
    for i in range(12):
        x = _lerp(xa + 4, xo - 5, i / 11)
        cuadros.append([(y, xa, "ATP", "titulo"), (y, xo, "─O─H", ctx["color_mio"]),
                        (y - 1, x, "PO₃²⁻", "NEG"), (y + 1, 1, "quinasa", "tenue"),
                        _sub(h, w, "la quinasa toma el fosforilo γ del ATP")])
    for i in range(4):
        cuadros.append([(y, xa, "ADP", "tenue"), (y, xo - 6, "─O─PO₃²⁻", "NEG"),
                        (y + 1, 1, "quinasa", "tenue"),
                        _sub(h, w, "y lo une al OH: ATP → ADP + H⁺")])
    return _final(cuadros, h, w, "fosforilado: carga ≈ −2 (Cargado −)", "NEG")


def acetilar(h, w, ctx):
    y = h // 2 - 1
    xa, xo = 2, w - 8
    cuadros = []
    for i in range(12):
        x = _lerp(xa + 11, xo - 6, i / 11)
        cuadros.append([(y, xa, "acetil-CoA", "titulo"), (y, xo, "─NH₃⁺", "POS"),
                        (y - 1, x, "CH₃CO", "texto"), (y + 1, 1, "HAT", "tenue"),
                        _sub(h, w, "la HAT toma el acetilo del acetil-CoA")])
    for i in range(4):
        cuadros.append([(y, xa, "CoA─SH", "tenue"), (y, xo - 6, "─NH─COCH₃", "POL"),
                        (y + 1, 1, "HAT   + H⁺", "tenue"),
                        _sub(h, w, "el NH₃⁺ suelta un H⁺ y queda como amida neutra")])
    return _final(cuadros, h, w, "acetilada: sin carga (Polar sin carga)", "POL")


def calcio(h, w, ctx):
    y = h // 2 - 1
    xi, xd = w // 2 - 8, w // 2 + 4
    cuadros = []
    for i in range(y + 1):
        cuadros.append([(y, xi, "─COO⁻", ctx["color_mio"]), (y, xd, "⁻OOC─", ctx["color_mio"]),
                        (i, w // 2 - 2, "Ca²⁺", "titulo"), (y + 1, xi - 1, "tu proteína (mano EF)", "tenue"),
                        _sub(h, w, "un Ca²⁺ llega a DOS carboxilatos de tu proteína")])
    base = _sin_sub(cuadros[-1], h)
    for i in range(4):
        cuadros.append(base + [(y, xi + 5, "·" if i % 2 == 0 else " ", "bien"),
                               (y, xd - 1, "·" if i % 2 == 0 else " ", "bien"),
                               _sub(h, w, "el Ca²⁺ ordena y estabiliza la estructura")])
    return _final(cuadros, h, w, "Ca²⁺ unido: tu proteína se estabiliza")


def helice(h, w, ctx):
    y = max(0, h // 2 - 2)
    cuadros = []
    vueltas = max(2, (w - 8) // 4)
    for i in range(1, vueltas + 1):
        c = []
        for k in range(i):
            x = 3 + k * 4
            c += [(y, x, " _", ctx["color_mio"]), (y + 1, x, "/ \\", ctx["color_mio"]),
                  (y + 2, x + 2, "\\_", ctx["color_mio"])]
        c.append(_sub(h, w, "la cadena se enrolla sobre sí misma"))
        cuadros.append(c)
    return _final(cuadros, h, w, "hélice α: C=O(i) ··· H–N(i+4), 3.6 residuos por vuelta")


def lamina(h, w, ctx):
    y = max(0, h // 2 - 2)
    largo = w - 8
    cuadros = []
    for i in range(1, 9):
        n = largo * i // 8
        cuadros.append([(y, 3, ("═" * n)[:-1] + "►" if n else "", ctx["color_mio"]),
                        (y + 2, 3 + largo - n, "◄" + "═" * max(0, n - 1), ctx["color_rival"]),
                        _sub(h, w, "dos hebras se alinean en sentidos opuestos")])
    base = _sin_sub(cuadros[-1], h)
    for i in range(5):
        enlaces = "".join("⁞" if (k + i) % 4 == 0 else " " for k in range(largo))
        cuadros.append(base + [(y + 1, 4, enlaces, "titulo"),
                               _sub(h, w, "N–H ··· O═C entre las hebras")])
    return _final(cuadros, h, w, "lámina β antiparalela (puentes de H del esqueleto)")


def flexible(h, w, ctx):
    y = h // 2 - 1
    cuadros = []
    for i in range(14):
        linea = "".join("╱╲"[(k + i) % 2] for k in range(w - 6))
        cuadros.append([(y, 3, linea, ctx["color_mio"]),
                        _sub(h, w, "sin cadena lateral, su esqueleto gira con libertad")])
    return _final(cuadros, h, w, "Gly: ángulos φ/ψ que otros no pueden")


def rigido(h, w, ctx):
    y = max(0, h // 2 - 3)
    anillo = ["  N───Cα", "  │    │", "  Cδ   Cβ", "   ╲  ╱", "    Cγ"]
    cuadros = []
    for i in range(1, len(anillo) + 1):
        cuadros.append([(y + k, w // 2 - 5, l, ctx["color_mio"]) for k, l in enumerate(anillo[:i])
                        if y + k < h - 1]
                       + [_sub(h, w, "la cadena lateral se cierra sobre el N del esqueleto")])
    base = _sin_sub(cuadros[-1], h)
    for i in range(5):
        cuadros.append(base + [(y + 1, w // 2 + 6, "φ ≈ −65° fijo" if i % 2 == 0 else "", "titulo"),
                               _sub(h, w, "el anillo bloquea el giro del esqueleto")])
    return _final(cuadros, h, w, "anillo rígido: resiste la agitación")


def codon(h, w, ctx):
    y = h // 2 - 1
    arn = "5'─AUG─GCU─UCA─AAG─3'"
    cuadros = []
    for i in range(1, len(arn) + 1, 2):
        cuadros.append([(y, 2, arn[:i], "texto"), _sub(h, w, "el ribosoma busca el codón de inicio")])
    for i in range(6):
        cuadros.append([(y, 2, arn, "texto"),
                        (y, 6, "AUG", "titulo" if i % 2 == 0 else "texto"),
                        (y + 1, 6, "UAC", "agua"), (y + 1, 10, "← anticodón 3'-UAC-5'", "tenue"),
                        (y - 1, 6, "Met", "NP"),
                        _sub(h, w, "el ARNt iniciador trae la Met")])
    return _final(cuadros, h, w, "¡AUG! la traducción empieza con Met")


def ph(h, w, ctx):
    y = h // 2 - 1
    cuadros = []
    escala = "pH 4 ──── 5 ──── 6 ──── 7 ──── 8"
    x0 = _centro(w, escala)
    destino = ctx.get("ph_destino", 5)
    origen = 7.4 if destino < 7 else 5
    for i in range(12):
        valor = origen + (destino - origen) * i / 11
        pos = x0 + 3 + round((valor - 4) * 6)
        cuadros.append([(y, x0, escala, "tenue"), (y - 1, pos, "▼", "titulo"),
                        (y + 1, x0 + 15, "pKR 6", "POS"),
                        _sub(h, w, "cambia el pH alrededor de la His")])
    texto = ("pH < pKR: el imidazol toma un H⁺ (Cargado +)" if destino < 6
             else "pH > pKR: el imidazol suelta su H⁺ (neutro)")
    return _final(cuadros, h, w, texto, "POS" if destino < 6 else "POL")


def antioxidante(h, w, ctx):
    y = h // 2 - 1
    cuadros = []
    for i in range(12):
        x = _lerp(2, w - 18, i / 11)
        cuadros.append([(y - 1, x, "H₂O₂", "mal"), (y, w - 12, "─S─CH₃", ctx["color_mio"]),
                        _sub(h, w, "una especie reactiva de oxígeno se acerca")])
    for i in range(4):
        cuadros.append([(y, w - 14, "─S(═O)─CH₃", "titulo"), (y + 1, 2, "H₂O", "agua"),
                        _sub(h, w, "la Met se oxida a Met-sulfóxido y la neutraliza")])
    return _final(cuadros, h, w, "antioxidante: protege a los demás residuos")


def fluorescencia(h, w, ctx):
    y = h // 2 - 1
    cuadros = []
    for i in range(0, w // 2 - 6, 2):
        cuadros.append([(y, 1, "~" * i + "»", "agua"), (y - 1, 1, "excitación 295 nm", "tenue"),
                        (y, w // 2 - 2, "Trp", ctx["color_mio"]),
                        _sub(h, w, "el indol absorbe luz UV")])
    lam = ctx.get("lambda", 340)
    for i in range(0, w // 2 - 6, 2):
        cuadros.append([(y, w // 2 - 2, "Trp", ctx["color_mio"]),
                        (y, w // 2 + 2, "~" * i + "»", "titulo"),
                        (y - 1, w // 2 + 2, f"emisión ~{lam} nm", "tenue"),
                        _sub(h, w, "y emite: el color depende de qué tan polar es su vecino")])
    return _final(cuadros, h, w, ctx.get("revelado", "¡identificado!"))


def glicanos(h, w, ctx):
    y = max(0, h // 2 - 2)
    arbol = ["        ◇─◇", "  ◇─◇─◇<", "        ◇─◇"]
    cuadros = []
    for i in range(1, 12):
        c = [(y + 1, 2, "Asn─N", ctx["color_mio"])]
        for k, l in enumerate(arbol):
            c.append((y + k, 7, l[:i], "POL"))
        c.append(_sub(h, w, "un árbol de azúcares cubre la superficie"))
        cuadros.append(c)
    return _final(cuadros, h, w, "los glicanos protegen de proteasas")


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
    "esqueleto": esqueleto, "esqueleto_triple": esqueleto_triple,
    "disulfuro": disulfuro, "enlace": enlace, "fosforilar": fosforilar,
    "acetilar": acetilar, "calcio": calcio, "helice": helice, "lamina": lamina,
    "flexible": flexible, "rigido": rigido, "codon": codon, "ph": ph,
    "antioxidante": antioxidante, "fluorescencia": fluorescencia,
    "glicanos": glicanos, "agitacion": agitacion, "trna": trna,
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
    """Alterna entre dos sprites (evolución)."""
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
