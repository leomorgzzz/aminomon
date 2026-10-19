"""Después de la Aminodex completa: la selenocisteína (fuera de los 20) y el
Laboratorio del René-virus (titulación, electroforesis e intercambio iónico).

La Sec no cuenta en el 20/20: no tiene codón propio. Se codifica con UGA (que
normalmente es paro) solo si el ARNm trae un elemento SECIS, y se arma sobre un
ARNt propio que primero se carga con Ser."""

import curses
import random

import datos
import dibujo as d
import progreso
from idioma import tr

AA = datos.AMINOACIDOS
SEC_ARTE = ["        H", "        |", "  H3N+--C--COO-", "        |", "        CH2", "        |",
            "        SeH"]


# --------------------------------------------------------- selenocisteína
def _pregunta(win, titulo, texto, correcta, otras):
    ops = [correcta] + otras
    random.shuffle(ops)
    win.erase()
    d.put(win, 0, 1, titulo, d.c("titulo", curses.A_BOLD))
    d.popup(win, texto, tr("Pregunta"), ancho=72, esperar=False)
    alto = win.getmaxyx()[0]
    op = d.menu(win, tr("¿Cuál?"), ops, y=alto - len(ops) - 3)
    return op is not None and ops[op] == correcta


def dar_sec(juego):
    """Una Sec se une al equipo (una sola vez, también en partidas viejas)."""
    if "sec_equipo" in juego["recompensas"]:
        return False
    juego["recompensas"].append("sec_equipo")
    nivel = max((m["nivel"] for m in juego["equipo"] if m["id"] == "S"), default=5)
    juego["equipo"].append(progreso.nuevo_mon("U", nivel))
    return True


def evento_sec(win, juego):
    """El evento de la selenocisteína: hay que saber cómo la mete la célula."""
    if juego.get("sec"):
        if dar_sec(juego):
            progreso.guardar(juego)
            d.popup(win, tr("Una selenocisteína se unió a tu equipo."), tr("René-virus"),
                    attr=d.c("bien"))
        tarjeta_sec(win)
        return
    if not any(m["id"] == "S" for m in juego["equipo"]):
        d.popup(win, tr("Para este evento necesitas una Ser en tu equipo: la Sec se arma "
                        "sobre una Ser."), tr("René-virus"))
        return
    d.dialogo(win, [
        tr("Hay un aminoácido fuera de los 20: la selenocisteína (Sec, U). Unas 25 "
           "proteínas humanas la usan, como la glutatión peroxidasa."),
        tr("CÓMO FUNCIONA\n\n• Son 3 preguntas sobre cómo la célula mete la Sec en una "
           "proteína.\n• Después de cada una te digo si acertaste y por qué.\n• Con las 3 "
           "bien, una Sec se une a tu equipo. Si fallas alguna, repítelo cuando quieras."),
    ], tr("René-virus"))
    preguntas = [
        (tr("En el ARNm de una selenoproteína, ¿qué codón lee la Sec?"), "UGA",
         ["AUG", "UAA", "UGG"],
         tr("UGA, que normalmente es de paro.")),
        (tr("Ese codón normalmente es de paro. ¿Qué lleva el ARNm para que se lea como Sec?"),
         tr("Un elemento SECIS (una horquilla en el ARNm)"),
         [tr("Una cola de poli(A) más larga"), tr("Un segundo AUG antes del codón"),
          tr("Un intrón sin cortar")],
         tr("La horquilla SECIS recluta las proteínas que traen el ARNt-Sec al ribosoma.")),
        (tr("El ARNt-Sec se carga primero con otro aminoácido y luego se convierte. ¿Con cuál?"),
         tr("Serina"), [tr("Cisteína"), tr("Metionina"), tr("Treonina")],
         tr("Se parece a la Cys (Se en lugar de S), pero nace de una Ser: la seril-ARNt "
            "sintetasa carga Ser y luego enzimas cambian su O por Se, del selenofosfato.")),
    ]
    aciertos = 0
    for n, (texto, correcta, otras, porque) in enumerate(preguntas, start=1):
        titulo = tr("SELENOCISTEÍNA · pregunta {n}/3 · aciertos {a}", n=n, a=aciertos)
        bien = _pregunta(win, titulo, texto, correcta, otras)
        aciertos += bien
        win.erase()
        d.popup(win, (tr("Correcto.") if bien else tr("No. Era: {r}.", r=correcta)) + " " + porque,
                tr("Aciertos {a}/{n}", a=aciertos, n=n), attr=d.c("bien" if bien else "mal"))
    if aciertos < 3:
        win.erase()
        d.popup(win, tr("{a}/3. Necesitas las 3: vuelve cuando quieras.", a=aciertos),
                tr("René-virus"))
        return
    juego["sec"] = True
    dar_sec(juego)
    progreso.guardar(juego)
    win.erase()
    d.popup(win, tr("¡3/3! Una Ser se cargó en el ARNt-Sec y, con selenofosfato, se convirtió "
                    "en selenocisteína. Ya está en tu equipo y en la Aminodex, en una sección "
                    "aparte: no cuenta en el 20/20."), tr("René-virus"), attr=d.c("bien"))
    tarjeta_sec(win)


def filas_sec():
    """Ficha de la Sec: (rótulo, valor)."""
    sec = datos.SEC
    movs = ", ".join(datos.MOVIMIENTOS[m]["nombre"] for m in datos.forma("U")["movs"])
    return [
        (tr("Grupo"), tr("Fuera de los 5 grupos de Lehninger. En el juego: Polar (como la Cys) "
                         "y Cargado − (a pH 7 casi toda está como –Se−).")),
        (tr("Carga pH 7"), sec["carga"]),
        ("pKR", tr("≈ 5.2 (selenol; el tiol de la Cys es 8.18)")),
        (tr("Masa"), f"{sec['masa']:.2f} g/mol"),
        (tr("Codón"), tr("UGA + un elemento SECIS en el ARNm")),
        (tr("Cómo se hace"), tr("Sobre su ARNt: se carga con Ser y la Ser se convierte en Sec. "
                                "No es una modificación postraduccional.")),
        (tr("Dónde está"), tr("~25 proteínas humanas: glutatión peroxidasas, tiorredoxina "
                              "reductasas y desyodasas tiroideas.")),
        (tr("Interacciones"), movs),
    ]


def tarjeta_sec(win):
    win.erase()
    alto, ancho = win.getmaxyx()
    d.put(win, 0, 1, tr("SELENOCISTEÍNA · Sec · U  (fuera de los 20)"), d.c("titulo", curses.A_BOLD))
    d.estructura(win, 2, 2, SEC_ARTE, etiqueta_r=datos.SEC["grupo_r"][0], color_r="POL")
    y = 2
    x = max(30, 2 + d.ancho_estructura(SEC_ARTE, datos.SEC["grupo_r"][0]) + 3)
    col = max(len(r) for r, _ in filas_sec()) + 2
    for rotulo, valor in filas_sec():
        for i, l in enumerate(d.envolver(valor, max(20, ancho - x - col - 2))):
            if y >= alto - 2:
                break
            if i == 0:
                d.put(win, y, x, rotulo, d.c("tenue"))
            d.put(win, y, x + col, l, d.c("texto"))
            y += 1
    d.put(win, alto - 1, 1, tr("[Enter] seguir"), d.c("tenue"))
    win.refresh()
    curses.flushinp()
    while d.tecla(win) not in d.ENTER:
        pass


def pregunta_sec(tipo):
    """Pregunta de reconocimiento de la Sec con el formato de preguntas.generar."""
    if tipo == "nombre":
        correcta = datos.SEC["nombre"]
        ops = [correcta, AA["C"]["nombre"], AA["S"]["nombre"], AA["M"]["nombre"]]
        texto = tr("¿Qué aminoácido es este? Fíjate en su cadena lateral.")
    elif tipo == "tres":
        correcta, ops = "Sec", ["Sec", "Cys", "Ser", "Met"]
        texto = tr("¿Cuál es el código de 3 letras de este aminoácido?")
    else:
        correcta, ops = "U", ["U", "C", "S", "M"]
        texto = tr("¿Cuál es el código de 1 letra de este aminoácido?")
    random.shuffle(ops)
    return dict(texto=texto, opciones=ops, respuesta=correcta,
                explicacion=tr("Es la selenocisteína (Sec, U): como la Cys, pero con Se en "
                               "lugar de S."))


def practica_sec(win, juego):
    """Cys (–SH) o Sec (–SeH): se confunden como Gln y Asn."""
    aciertos = 0
    for i in range(8):
        es_sec = random.random() < 0.5
        win.erase()
        d.put(win, 0, 1, tr("¿Cys o Sec? · {i}/8 · aciertos {n}", i=i + 1, n=aciertos),
              d.c("titulo", curses.A_BOLD))
        d.estructura(win, 2, 2, SEC_ARTE if es_sec else datos.forma("C")["arte"])
        d.put(win, 11, 2, tr("1) Cisteína (Cys, C)   2) Selenocisteína (Sec, U)   Esc salir"),
              d.c("texto", curses.A_BOLD))
        win.refresh()
        while True:
            k = d.tecla(win)
            if k == d.ESC or (isinstance(k, str) and k in "12"):
                break
        if k == d.ESC:
            return
        bien = (k == "2") == es_sec
        aciertos += bien
        progreso.registrar(juego, "sec:cys", bien)
        d.popup(win, (tr("Correcto.") if bien else tr("Incorrecto.")) + " "
                + tr("Fíjate en el último átomo: S en la Cys, Se en la Sec."), tr("Resultado"),
                attr=d.c("bien" if bien else "mal"))
    d.popup(win, tr("{n}/8 correctas.", n=aciertos), tr("¿Cys o Sec?"))


# ------------------------------------------------ laboratorio del René-virus
# Un cuarto con tres mesas: caminas a una y resuelves su problema con un
# dibujo (la curva de titulación, el gel o la columna). 6 problemas por visita.
PROBLEMAS_LAB = 6
CUARTO = [
    "########################################################",
    "#                                                      #",
    "#     TTTTT              EEEEE              IIIII      #",
    "#     TTTTT              EEEEE              IIIII      #",
    "#     TTTTT              EEEEE              IIIII      #",
    "#                                                      #",
    "#                                                      #",
    "#                                                      #",
    "#                   V                                  #",
    "#                                                      #",
    "##########################  ############################",
]
# cómo se ve cada mesa (5 × 3)
DIBUJO_MESA = {"T": ["┌───┐", "│pH │", "└─┬─┘"], "E": ["┌───┐", "│−▓+│", "└───┘"],
               "I": ["┌─┬─┐", "│ ▓ │", "└─▼─┘"]}
MESAS = {"T": "titulacion", "E": "electroforesis", "I": "intercambio"}


def carga(aa, ph):
    """Carga neta de un aminoácido libre (Henderson-Hasselbalch)."""
    a = AA[aa]
    q = 1 / (1 + 10 ** (ph - a["pk2"])) - 1 / (1 + 10 ** (a["pk1"] - ph))
    if a["pkr"]:
        if a["grupo"] == "basico":
            q += 1 / (1 + 10 ** (ph - a["pkr"]))
        else:
            q -= 1 / (1 + 10 ** (a["pkr"] - ph))
    return q


def _pks(aa):
    a = AA[aa]
    return [a["pk1"], a["pk2"]] + ([a["pkr"]] if a["pkr"] else [])


def _equivalentes(aa, ph, conc=0.1):
    """OH− agregados (equivalentes por mol de aminoácido) hasta llegar a ese
    pH, con el balance de cargas de una solución 0.1 M: por eso la curva empieza
    cerca de pH 1.5 y no en 0, como en la figura de Lehninger."""
    agua = (10 ** -ph - 10 ** (ph - 14)) / conc
    return sum(1 / (1 + 10 ** (pk - ph)) for pk in _pks(aa)) - agua


def _ph_de(aa, eq):
    lo, hi = 0.0, 14.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if _equivalentes(aa, mid) < eq:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def _titulacion(win, juego):
    """Un cursor recorre la curva: hay que dejarlo donde está lo que se pide."""
    aa = random.choice([c for c in "GAVDEKHC" if c in AA])
    a = AA[aa]
    n_eq = len(_pks(aa))
    puntos = {"pK1": a["pk1"], "pK2": a["pk2"], "pI": a["pi"]}
    if a["pkr"]:
        puntos["pKR"] = a["pkr"]
    pide = random.choice(list(puntos))
    nombres = {"pK1": tr("el pK1: donde amortigua el α-COOH"),
               "pK2": tr("el pK2: donde amortigua el α-NH3+"),
               "pKR": tr("el pKR: donde amortigua la cadena lateral"),
               "pI": tr("el pI: donde la carga neta es 0")}
    objetivo = puntos[pide]
    cursor = 0
    while True:
        alto, ancho = win.getmaxyx()
        h = max(10, min(22, alto - 12))
        w = max(30, min(72, ancho - 40))
        x0, y0 = 7, 3
        camino = _camino(aa, y0, x0, h, w, n_eq)
        cursor = min(cursor, len(camino) - 1)
        win.erase()
        d.put(win, 0, 1, tr("TITULACIÓN · {nombre} 0.1 M con NaOH", nombre=a["nombre"]),
              d.c("titulo", curses.A_BOLD))
        d.put(win, 1, 1, tr("Pon el cursor en {que}", que=nombres[pide]),
              d.c("titulo", curses.A_BOLD | curses.A_REVERSE))
        _dibujar_curva(win, aa, y0, x0, h, w, n_eq, camino)
        col, fila, ph, eq = camino[cursor]
        for yy in range(fila + 1, y0 + h):
            d.put(win, yy, col, "·", d.c("tenue"))
        d.put(win, fila, col, "♦", d.c("titulo", curses.A_BOLD))
        xl = x0 + w + 4
        leyenda = [(tr("Valores (Lehninger, 25 °C)"), "titulo"),
                   (f"pK1 (α-COOH)   {a['pk1']:.2f}", "texto"),
                   (f"pK2 (α-NH3+)   {a['pk2']:.2f}", "texto")]
        if a["pkr"]:
            leyenda.append((tr("pKR (cadena)   {v:.2f}", v=a["pkr"]), "texto"))
        leyenda += [("", "texto"), (tr("Cursor: {eq:.2f} eq de OH−", eq=eq), "agua"),
                    (tr("pH en el cursor: {ph:.1f}", ph=ph), "agua"), ("", "texto"),
                    (tr("En los tramos verticales el"), "tenue"),
                    (tr("cursor sube por la curva."), "tenue"), ("", "texto"),
                    (tr("Pista: un pK está en la mitad"), "tenue"),
                    (tr("de una meseta (ahí amortigua)."), "tenue"),
                    (tr("El pI, entre los dos pK que"), "tenue"),
                    (tr("rodean la forma neutra."), "tenue")]
        for i, (t, col) in enumerate(leyenda):
            d.put(win, y0 + i, xl, t, d.c(col, curses.A_BOLD if col == "titulo" else 0))
        d.put(win, alto - 1, 1, tr("←/→ mover el cursor (Shift o A/D: más rápido) · Enter aquí · "
                                   "Esc salir"), d.c("tenue"))
        win.refresh()
        k = d.tecla(win)
        if k == d.ESC:
            return None
        if k in d.ENTER:
            break
        paso = 3 if d.es(k, "a", "d", curses.KEY_SLEFT, curses.KEY_SRIGHT) else 1
        if d.es(k, curses.KEY_LEFT, "a", curses.KEY_SLEFT):
            cursor = max(0, cursor - paso)
        elif d.es(k, curses.KEY_RIGHT, "d", curses.KEY_SRIGHT):
            cursor = min(len(camino) - 1, cursor + paso)
    # se califica por pH: en un salto vertical todos los puntos tienen casi
    # los mismos equivalentes y lo que cambia es el pH
    # (en las mesetas el pH cambia poco por paso; en el salto, una fila entera)
    tolerancia = max(0.3, 0.6 * 14 / (h - 1)) if pide == "pI" else 0.3
    bien = abs(ph - objetivo) <= tolerancia
    # se revelan todos los puntos sobre la curva
    for k2, v in puntos.items():
        e2 = _equivalentes(aa, v)
        col = x0 + round(e2 / n_eq * (w - 1))
        fila = y0 + h - 1 - round(v / 14 * (h - 1))
        for xx in range(x0, col):
            d.put(win, fila, xx, "·", d.c("tenue"))
        d.put(win, fila, col, "X" if k2 == pide else "o", d.c("bien" if k2 == pide else "agua",
                                                              curses.A_BOLD))
        d.put(win, fila, col + 2, f"{k2} {v:.2f}", d.c("bien" if k2 == pide else "agua"))
    texto = ((tr("Correcto.") if bien else
              tr("Casi: {k} estaba en pH {ph:.2f} (marcado con X); dejaste el cursor en pH {tu:.1f}.",
                 k=pide, ph=objetivo, tu=ph)) + " "
             + tr("Cada pK queda a media meseta: ahí la mitad del grupo ya soltó su H+ y el pH "
                  "cambia poco. El pI queda entre dos mesetas: ahí la carga neta es 0."))
    yt = y0 + h + 2
    for i, l in enumerate(d.envolver(texto, min(ancho - 4, 100))):
        d.put(win, yt + i, 2, l, d.c("bien" if bien else "mal"))
    d.put(win, alto - 1, 1, tr("[Enter] seguir").ljust(ancho - 2), d.c("tenue"))
    win.refresh()
    curses.flushinp()
    while d.tecla(win) not in d.ENTER:
        pass
    return bien


def _camino(aa, y0, x0, h, w, n_eq):
    """Los puntos de la curva en orden, [(columna, fila, pH, eq)], sin huecos:
    en los saltos verticales se agregan las filas intermedias, así el cursor
    también puede pararse a media subida (donde suele estar el pI)."""
    camino = []
    anterior = None
    for i in range(w):
        eq = i / (w - 1) * n_eq
        ph = _ph_de(aa, eq)
        fila = y0 + h - 1 - round(ph / 14 * (h - 1))
        if anterior is not None and abs(fila - anterior) > 1:
            paso = 1 if fila > anterior else -1
            for yy in range(anterior + paso, fila, paso):
                camino.append((x0 + i, yy, (y0 + h - 1 - yy) / (h - 1) * 14, eq))
        camino.append((x0 + i, fila, ph, eq))
        anterior = fila
    return camino


def _dibujar_curva(win, aa, y0, x0, h, w, n_eq, camino):
    """Ejes con marcas (pH de 2 en 2, equivalentes de 0.5 en 0.5) y la curva."""
    for ph in range(0, 15, 2):
        fila = y0 + h - 1 - round(ph / 14 * (h - 1))
        d.put(win, fila, x0 - 4, f"{ph:>2} ┤", d.c("tenue"))
    d.put(win, y0 - 1, x0 - 5, "pH", d.c("tenue", curses.A_BOLD))
    d.put(win, y0 + h, x0 - 1, "└" + "─" * w, d.c("tenue"))
    for i in range(int(n_eq * 2) + 1):
        col = x0 + round(i / 2 / n_eq * (w - 1))
        d.put(win, y0 + h, col, "┬", d.c("tenue"))
        etiqueta = f"{i / 2:g}"
        d.put(win, y0 + h + 1, col - len(etiqueta) // 2, etiqueta, d.c("tenue"))
    d.put(win, y0 + h + 1, x0 + w + 1, tr("eq de OH−"), d.c("tenue", curses.A_BOLD))
    for col, fila, _, _ in camino:
        d.put(win, fila, col, "•", d.c("agua"))


def _muestras(ph, n, separacion, rango=None):
    """n aminoácidos con cargas bien distintas a ese pH (sin empates dudosos)."""
    while True:
        tres = random.sample(rango or datos.ORDEN, n)
        q = sorted(carga(c, ph) for c in tres)
        if all(q[i + 1] - q[i] >= separacion for i in range(n - 1)):
            return tres


def _electroforesis(win, juego):
    """Tres carriles: eliges hacia dónde va cada banda y luego se corre el gel."""
    ph = random.choice([3.0, 6.0, 7.0, 9.5])
    while True:
        carriles = random.sample(datos.ORDEN, 3)
        lados = {0 if abs(carga(c, ph)) < 0.1 else carga(c, ph) > 0 for c in carriles}
        if len(lados) >= 2 and all(abs(carga(c, ph)) < 0.1 or abs(carga(c, ph)) > 0.35
                                   for c in carriles):
            break
    real = [0 if abs(carga(c, ph)) < 0.1 else (-1 if carga(c, ph) > 0 else 1) for c in carriles]
    elegido = [0, 0, 0]
    sel = 0
    alto, ancho = win.getmaxyx()
    largo = min(60, ancho - 30)
    centro = 16 + largo // 2

    def dibujar(pos=None):
        win.erase()
        d.put(win, 0, 1, tr("ELECTROFORESIS · amortiguador a pH {ph}", ph=ph),
              d.c("titulo", curses.A_BOLD))
        d.put(win, 1, 1, tr("¿Hacia dónde migra cada aminoácido? ↑/↓ carril · ←/→ dirección · "
                            "Enter correr el gel"), d.c("titulo", curses.A_BOLD | curses.A_REVERSE))
        d.put(win, 3, 16, tr("(−) cátodo"), d.c("POS", curses.A_BOLD))
        d.put(win, 3, 16 + largo - 9, tr("ánodo (+)"), d.c("NEG", curses.A_BOLD))
        for i, c in enumerate(carriles):
            y = 5 + i * 3
            a = AA[c]
            d.put(win, y, 1, f"{a['tres']} pI {a['pi']:.2f}", d.c(a["tipos"][0], curses.A_BOLD))
            d.put(win, y, 16, "░" * largo, d.c("oscuro"))
            d.put(win, y, centro, "▓", d.c("tenue"))
            if pos is None:
                flecha = {-1: "◄ ", 0: " · ", 1: " ►"}[elegido[i]]
                d.put(win, y + 1, centro - 1, flecha, d.c("titulo", curses.A_BOLD))
                if i == sel:
                    d.put(win, y, 14, "►", d.c("titulo", curses.A_BOLD))
            else:
                d.put(win, y, pos[i], "█", d.c(a["tipos"][0], curses.A_BOLD))
        win.refresh()

    while True:
        dibujar()
        k = d.tecla(win)
        if k == d.ESC:
            return None
        if k in d.ENTER:
            break
        if d.es(k, curses.KEY_UP, "w"):
            sel = (sel - 1) % 3
        elif d.es(k, curses.KEY_DOWN, "s"):
            sel = (sel + 1) % 3
        elif d.es(k, curses.KEY_LEFT, "a"):
            elegido[sel] = max(-1, elegido[sel] - 1)
        elif d.es(k, curses.KEY_RIGHT, "d"):
            elegido[sel] = min(1, elegido[sel] + 1)
    # se corre el gel: cada banda avanza según su carga
    destino = [centro - round(carga(c, ph) * (largo // 2 - 2) / 2) for c in carriles]
    destino = [max(16, min(16 + largo - 1, x)) for x in destino]
    for paso in range(13):
        dibujar([centro + round((x - centro) * paso / 12) for x in destino])
        curses.napms(70)
    bien = elegido == real
    lineas = []
    for c, e, r in zip(carriles, elegido, real):
        q = round(carga(c, ph), 1) + 0.0
        marca = "√" if e == r else "x"
        lado = {-1: tr("al cátodo"), 0: tr("casi no se mueve"), 1: tr("al ánodo")}[r]
        lineas.append(f"{marca} {AA[c]['tres']}: {tr('carga')} {q:+.1f} → {lado}")
    texto = "\n".join(lineas) + "\n\n" + tr("Por debajo de su pI un aminoácido tiene carga + y "
                                             "va al cátodo (−); por encima, carga − y va al ánodo (+).")
    y = 15
    for i, l in enumerate(d.envolver(texto, min(ancho - 4, 90))):
        d.put(win, y + i, 2, l, d.c("bien" if bien else "mal") if i < 3 else d.c("texto"))
    d.put(win, alto - 1, 1, tr("[Enter] seguir"), d.c("tenue"))
    win.refresh()
    curses.flushinp()
    while d.tecla(win) not in d.ENTER:
        pass
    return bien


def _intercambio(win, juego):
    """Columna catiónica: das el orden de salida y luego se ve bajar a cada banda."""
    ph = 6.0
    tres = _muestras(ph, 3, 0.4)
    letras = "ABC"
    cargas = {c: carga(c, ph) for c in tres}
    real = sorted(tres, key=lambda c: cargas[c])          # lo más − sale primero
    orden = []
    alto, ancho = win.getmaxyx()
    hc = max(8, min(14, alto - 12))
    xc = 6

    def dibujar(posiciones=None):
        win.erase()
        d.put(win, 0, 1, tr("INTERCAMBIO IÓNICO · resina catiónica (−) · pH {ph}", ph=ph),
              d.c("titulo", curses.A_BOLD))
        d.put(win, 1, 1, tr("¿En qué orden salen? Pulsa las letras del primero al último · "
                            "Retroceso borra"), d.c("titulo", curses.A_BOLD | curses.A_REVERSE))
        d.put(win, 3, xc, "┌──────┐", d.c("tenue"))
        for i in range(hc):
            d.put(win, 4 + i, xc, "│" + (" − − " if i % 2 else "− − −").center(6) + "│", d.c("NEG"))
        d.put(win, 4 + hc, xc, "└──┬───┘", d.c("tenue"))
        d.put(win, 5 + hc, xc + 3, "▼", d.c("tenue"))
        d.put(win, 6 + hc, xc - 1, tr("salida"), d.c("tenue"))
        if posiciones:
            for c, y in posiciones.items():
                if 4 <= y < 4 + hc:
                    d.put(win, y, xc + 1, letras[tres.index(c)] * 6,
                          d.c(AA[c]["tipos"][0], curses.A_BOLD | curses.A_REVERSE))
        for i, c in enumerate(tres):
            a = AA[c]
            d.put(win, 4 + i * 2, xc + 14, f"{letras[i]} = {a['nombre']} ({a['tres']})  pI {a['pi']:.2f}",
                  d.c(a["tipos"][0], curses.A_BOLD))
        d.put(win, 11, xc + 14, tr("Tu orden: {o}", o=", ".join(letras[tres.index(c)] for c in orden)
                                   or "…"), d.c("titulo"))
        d.put(win, 13, xc + 14, tr("La resina tiene cargas −: retiene lo que es +."), d.c("tenue"))
        win.refresh()

    while len(orden) < 3:
        dibujar()
        k = d.tecla(win)
        if k == d.ESC:
            return None
        if k in (curses.KEY_BACKSPACE, "\x7f", "\b") and orden:
            orden.pop()
        elif isinstance(k, str) and k.upper() in letras:
            c = tres[letras.index(k.upper())]
            if c not in orden:
                orden.append(c)
    # elución: lo más negativo baja más rápido
    vel = {c: 0.35 + 0.5 * (1 - (cargas[c] - min(cargas.values())) /
                            max(0.01, max(cargas.values()) - min(cargas.values()))) for c in tres}
    for t in range(int(hc / 0.35) + 4):
        dibujar({c: 4 + int(t * vel[c]) for c in tres})
        curses.napms(60)
    bien = orden == real
    detalle = ", ".join(f"{AA[c]['tres']} {cargas[c]:+.1f}" for c in real)
    texto = ((tr("Correcto.") if bien else
              tr("No: el orden era {o}.", o=", ".join(AA[c]["tres"] for c in real))) + " "
             + tr("Cargas a pH 6, de la primera en salir a la última: {d}. Lo más negativo pasa "
                  "de largo; lo más positivo se queda pegado a la resina.", d=detalle))
    for i, l in enumerate(d.envolver(texto, min(ancho - xc - 16, 70))):
        d.put(win, 15 + i, xc + 14, l, d.c("bien" if bien else "mal"))
    d.put(win, alto - 1, 1, tr("[Enter] seguir"), d.c("tenue"))
    win.refresh()
    curses.flushinp()
    while d.tecla(win) not in d.ENTER:
        pass
    return bien


def _ayuda_lab():
    return tr("CÓMO FUNCIONA\n\n• Camina con WASD o las flechas hasta una mesa.\n"
              "• T titulación: pon el cursor sobre la curva donde está el pK o el pI.\n"
              "• E electroforesis: elige hacia qué electrodo va cada aminoácido.\n"
              "• I intercambio iónico: di en qué orden salen de la columna.\n"
              "• Son {n} problemas por visita; arriba ves tu cuenta. La salida está abajo.",
              n=PROBLEMAS_LAB)


def laboratorio(win, juego):
    """El laboratorio del René-virus: un cuarto con tres mesas."""
    d.dialogo(win, [tr("Te doy la bienvenida a mi laboratorio de proteómica: aquí la química de cada aminoácido se mide."), _ayuda_lab()], tr("René-virus"))
    pos = [27, 9]
    hechos = aciertos = 0
    por_mesa = {m: 0 for m in MESAS}
    mensaje = ""
    while hechos < PROBLEMAS_LAB:
        alto, ancho = win.getmaxyx()
        win.erase()
        record = juego.get("records", {}).get("laboratorio", 0)
        d.put(win, 0, 1, tr("LABORATORIO DEL RENÉ-VIRUS · problemas {h}/{n} · aciertos {a} · "
                            "récord {r}", h=hechos, n=PROBLEMAS_LAB, a=aciertos, r=record),
              d.c("titulo", curses.A_BOLD))
        y0, x0 = 2, max(1, (ancho - len(CUARTO[0]) - 34) // 2)
        rotulos = {"T": tr("Titulación"), "E": tr("Electroforesis"), "I": tr("Intercambio"),
                   "V": tr("René-virus")}
        dibujadas = set()
        for y, fila in enumerate(CUARTO):
            for x, t in enumerate(fila):
                if t == "#":
                    d.put(win, y0 + y, x0 + x, "█", d.c("oscuro"))
                elif t in MESAS and t not in dibujadas:
                    dibujadas.add(t)
                    for k, l in enumerate(DIBUJO_MESA[t]):
                        d.put(win, y0 + y + k, x0 + x, l, d.c("titulo", curses.A_BOLD))
                    for k, l in enumerate((rotulos[t], tr("hechos: {n}", n=por_mesa[t]))):
                        d.put(win, y0 + y + 3 + k, x0 + x + 2 - len(l) // 2, l,
                              d.c("titulo" if k == 0 else "tenue"))
                elif t == "V":
                    d.put(win, y0 + y, x0 + x, "V", d.c("bien", curses.A_BOLD))
                    d.put(win, y0 + y, x0 + x + 2, rotulos[t], d.c("bien"))
        d.put(win, y0 + pos[1], x0 + pos[0], "@", d.c("texto", curses.A_BOLD | curses.A_REVERSE))
        xl = x0 + len(CUARTO[0]) + 3
        if ancho - xl >= 24:                 # en 80 columnas no cabe: queda en H
            for i, l in enumerate(d.envolver(_ayuda_lab(), min(32, ancho - xl - 1))):
                d.put(win, y0 + i, xl, l, d.c("titulo" if i == 0 else "tenue"))
        d.put(win, y0 + len(CUARTO) + 1, x0, mensaje, d.c("texto"))
        d.put(win, alto - 1, 1, tr("WASD/flechas caminar · Esc salir del laboratorio"), d.c("tenue"))
        win.refresh()
        k = d.tecla(win)
        if k == d.ESC:
            break
        dx, dy = 0, 0
        if d.es(k, curses.KEY_UP, "w"):
            dy = -1
        elif d.es(k, curses.KEY_DOWN, "s"):
            dy = 1
        elif d.es(k, curses.KEY_LEFT, "a"):
            dx = -1
        elif d.es(k, curses.KEY_RIGHT, "d"):
            dx = 1
        nx, ny = pos[0] + dx, pos[1] + dy
        if not (0 <= ny < len(CUARTO)) or ny == len(CUARTO) - 1 and CUARTO[ny][nx] == " ":
            break                               # la puerta de salida
        t = CUARTO[ny][nx]
        if t == "#":
            continue
        if t in MESAS:
            r = {"titulacion": _titulacion, "electroforesis": _electroforesis,
                 "intercambio": _intercambio}[MESAS[t]](win, juego)
            if r is not None:
                hechos += 1
                aciertos += bool(r)
                por_mesa[t] += 1
                mensaje = tr("√ Resuelto.") if r else tr("x Esta vez no.")
            continue                            # te quedas junto a la mesa
        if t == "V":
            d.popup(win, _ayuda_lab(), tr("René-virus"))
            continue
        pos = [nx, ny]
    if not hechos:
        return
    mejor = juego.setdefault("records", {})
    nuevo = hechos == PROBLEMAS_LAB and aciertos > mejor.get("laboratorio", 0)
    if nuevo:
        mejor["laboratorio"] = aciertos
    progreso.guardar(juego)
    win.erase()
    d.popup(win, tr("{a}/{h} problemas resueltos.", a=aciertos, h=hechos)
            + (" " + tr("¡Nuevo récord!") if nuevo else ""), tr("Laboratorio del René-virus"),
            attr=d.c("bien" if aciertos >= 5 else "texto"))


# ------------------------------------------------------- el final de todo
def _saltar(win):
    """Enter salta la animación (no la detiene cualquier tecla)."""
    win.nodelay(True)
    try:
        while True:
            try:
                k = win.get_wch()
            except curses.error:
                return False
            if k in d.ENTER:
                return True
    finally:
        win.nodelay(False)


def final(win, juego):
    """Regalo por terminar todo: fuegos de aminoácidos, una cadena que se pliega
    en hélice y un certificado."""
    import math
    alto, ancho = win.getmaxyx()
    letras = [(c, AA[c]["tipos"][0]) for c in datos.ORDEN] + [("U", "POL")]
    saltar = False
    # 1. fuegos: cada estallido son letras de un grupo que salen del centro
    for t in range(36):
        if saltar or _saltar(win):
            saltar = True
            break
        if t % 6 == 0:
            cy, cx = random.randint(3, alto - 6), random.randint(10, ancho - 10)
            grupo = random.choice(datos.ORDEN_TIPOS)
            propios = [c for c, g in letras if g == grupo] or ["G"]
        r = (t % 6) + 1
        for k in range(10):
            ang = k / 10 * 2 * math.pi
            d.put(win, cy + round(math.sin(ang) * r * 0.5), cx + round(math.cos(ang) * r),
                  random.choice(propios), d.c(grupo, curses.A_BOLD))
        win.refresh()
        curses.napms(70)
        if t % 6 == 5:
            win.erase()
    # 2. la cadena entra y se pliega en hélice
    y = alto // 2
    n = len(letras)
    x0 = (ancho - n * 3) // 2
    for t in range(40):
        if saltar or _saltar(win):
            saltar = True
            break
        win.erase()
        amp = min(1.0, max(0.0, (t - 14) / 16)) * 3
        for i, (c, g) in enumerate(letras):
            x = x0 + i * 3 + max(0, (20 - t) * 4)
            yy = y + round(math.sin(i * 1.7 + t * 0.3) * amp)
            d.put(win, yy, x, c, d.c(g, curses.A_BOLD))
        win.refresh()
        curses.napms(80)
    import sintesis
    # 3. el certificado
    win.erase()
    reloj = juego.get("records", {})
    aciertos = sum(juego["aciertos"].values())
    texto = (tr("Capturaste los 20 aminoácidos, conseguiste las {m} modificaciones, ganaste las {i} insignias, aprobaste los dos exámenes, conociste a la selenocisteína, cumpliste los {p} encargos de síntesis (y la selenoproteína) y resolviste el laboratorio.",
                m=len(datos.MODIFICACIONES), i=len(juego["insignias"]), p=len(sintesis.HISTORIA))
             + "\n\n" + tr("Aciertos de reconocimiento: {a} · contrarreloj: {r} · laboratorio: {l}/6",
                           a=aciertos, r=reloj.get("reloj", 0), l=reloj.get("laboratorio", 0))
             + "\n\n" + tr("De regalo: un ♦ junto al título del mapa. Gracias por jugar; puedes "
                           "seguir practicando todo lo que quieras."))
    d.popup(win, texto, tr("CERTIFICADO · Aminomon completo"), ancho=72, attr=d.c("bien"))
