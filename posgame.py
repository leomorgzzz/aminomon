"""Después de la Aminodex completa: la selenocisteína (el aminoácido 21) y el
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
    d.popup(win, texto, titulo, ancho=72, esperar=False)
    alto = win.getmaxyx()[0]
    op = d.menu(win, tr("¿Cuál?"), ops, y=alto - len(ops) - 3)
    return op is not None and ops[op] == correcta


def evento_sec(win, juego):
    """El evento del aminoácido 21: hay que saber cómo se hace en la célula."""
    if juego.get("sec"):
        tarjeta_sec(win)
        return
    if not any(m["id"] == "S" for m in juego["equipo"]):
        d.popup(win, tr("Para el aminoácido 21 necesitas una Ser en tu equipo: la Sec se arma "
                        "sobre una Ser."), tr("René-virus"))
        return
    d.dialogo(win, [
        tr("Hay un aminoácido que no está en los 20: la selenocisteína (Sec, U). Unas 25 "
           "proteínas humanas la usan, como la glutatión peroxidasa y las desyodasas "
           "tiroideas."),
        tr("No tiene codón propio. Para meterla, la célula reinterpreta un codón y usa un "
           "ARNt especial. Contesta bien y tu Ser se convertirá en Sec."),
    ], tr("René-virus"))
    preguntas = [
        (tr("En el ARNm de una selenoproteína, ¿qué codón lee la Sec?"), "UGA",
         ["AUG", "UAA", "UGG"]),
        (tr("Ese codón normalmente es de paro. ¿Qué lleva el ARNm para que se lea como Sec?"),
         tr("Un elemento SECIS (una horquilla en el ARNm)"),
         [tr("Una cola de poli(A) más larga"), tr("Un segundo AUG antes del codón"),
          tr("Un intrón sin cortar")]),
        (tr("El ARNt-Sec se carga primero con otro aminoácido y luego se convierte. ¿Con cuál?"),
         tr("Serina"), [tr("Cisteína"), tr("Metionina"), tr("Treonina")]),
    ]
    for texto, correcta, otras in preguntas:
        if not _pregunta(win, tr("El aminoácido 21"), texto, correcta, otras):
            win.erase()
            d.popup(win, tr("No. Era: {r}. Vuelve a intentarlo cuando quieras.", r=correcta),
                    tr("René-virus"), attr=d.c("mal"))
            return
    juego["sec"] = True
    progreso.guardar(juego)
    win.erase()
    d.popup(win, tr("¡Tu Ser se cargó en el ARNt-Sec y, con selenofosfato, se convirtió en "
                    "selenocisteína! Ya está en tu Aminodex como el 21, fuera del 20/20."),
            tr("René-virus"), attr=d.c("bien"))
    tarjeta_sec(win)


def tarjeta_sec(win):
    win.erase()
    alto, ancho = win.getmaxyx()
    d.put(win, 0, 1, tr("21 · SELENOCISTEÍNA · Sec · U"), d.c("titulo", curses.A_BOLD))
    d.estructura(win, 2, 2, SEC_ARTE, etiqueta_r=tr("selenometilo (–CH2–SeH)"), color_r="POL")
    texto = tr("Como la Cys, pero con selenio en lugar de azufre: –SeH en vez de –SH. El "
               "selenol (pKa ≈ 5.2) está desprotonado a pH 7 y es mucho más reactivo que el "
               "tiol de la Cys (pKa 8.2): por eso está en el sitio activo de enzimas "
               "redox. Se codifica con UGA + SECIS.")
    for i, l in enumerate(d.envolver(texto, ancho - 4)):
        d.put(win, 12 + i, 2, l, d.c("texto"))
    d.put(win, alto - 1, 1, tr("[Enter] seguir"), d.c("tenue"))
    win.refresh()
    curses.flushinp()
    d.tecla(win)


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


def _equivalentes(aa, ph):
    """OH− agregados (equivalentes) hasta llegar a ese pH."""
    a = AA[aa]
    pks = [a["pk1"], a["pk2"]] + ([a["pkr"]] if a["pkr"] else [])
    return sum(1 / (1 + 10 ** (pk - ph)) for pk in pks)


def _titulacion(win, juego):
    aa = random.choice([c for c in "GADEKHC" if c in AA])
    a = AA[aa]
    alto, ancho = win.getmaxyx()
    h, w = min(14, alto - 9), min(56, ancho - 10)
    n_eq = 3 if a["pkr"] else 2
    puntos = {}
    for k, ph in (("pK1", a["pk1"]), ("pK2", a["pk2"]), ("pKR", a["pkr"]), ("pI", a["pi"])):
        if ph:
            puntos[k] = ph
    letras = "ABCD"
    orden = sorted(puntos, key=lambda k: puntos[k])
    etiqueta = {k: letras[i] for i, k in enumerate(orden)}
    win.erase()
    d.put(win, 0, 1, tr("TITULACIÓN · {nombre}", nombre=a["nombre"]), d.c("titulo", curses.A_BOLD))
    d.put(win, 1, 1, tr("pH (vertical) contra equivalentes de OH− agregados (horizontal)"),
          d.c("tenue"))
    for i in range(w):
        eq = i / (w - 1) * n_eq
        lo, hi = 0.0, 14.0
        for _ in range(40):          # pH que corresponde a esos equivalentes
            mid = (lo + hi) / 2
            if _equivalentes(aa, mid) < eq:
                lo = mid
            else:
                hi = mid
        fila = 2 + h - 1 - round(mid / 14 * (h - 1))
        d.put(win, fila, 6 + i, "•", d.c("agua"))
    for k, ph in puntos.items():
        eq = _equivalentes(aa, ph)
        col = 6 + round(eq / n_eq * (w - 1))
        fila = 2 + h - 1 - round(ph / 14 * (h - 1))
        d.put(win, fila, min(col + 1, 6 + w), etiqueta[k], d.c("mal", curses.A_BOLD))
    for ph in (0, 7, 14):
        d.put(win, 2 + h - 1 - round(ph / 14 * (h - 1)), 1, f"{ph:>3}", d.c("tenue"))
    pide = random.choice(list(puntos))
    nombres = {"pK1": tr("el pK1 (α-COOH)"), "pK2": tr("el pK2 (α-NH3+)"),
               "pKR": tr("el pKR (cadena lateral)"), "pI": tr("el pI (carga neta 0)")}
    ops = [etiqueta[k] for k in orden]
    op = d.menu(win, tr("¿Qué letra marca {que}?", que=nombres[pide]), ops,
                y=min(alto - len(ops) - 3, 2 + h + 1))
    bien = op is not None and ops[op] == etiqueta[pide]
    d.popup(win, (tr("Correcto.") if bien else tr("No: era la {l}.", l=etiqueta[pide])) + " "
            + tr("Las mesetas son los pK (ahí el grupo amortigua); el pI queda entre los dos "
                 "pK que rodean la forma neutra."), tr("Titulación"),
            attr=d.c("bien" if bien else "mal"))
    return bien


def _electroforesis(win, juego):
    aa = random.choice(datos.ORDEN)
    ph = random.choice([3.0, 6.0, 7.0, 9.5, 11.0])
    q = round(carga(aa, ph), 1) + 0.0      # sin «−0.0»
    # 0: al cátodo (carga +) · 1: al ánodo (carga −) · 2: casi no se mueve
    real = 2 if abs(q) < 0.25 else (0 if q > 0 else 1)
    ops = [tr("Al cátodo (−): tiene carga +"), tr("Al ánodo (+): tiene carga −"),
           tr("Casi no se mueve: carga neta ≈ 0")]
    win.erase()
    d.popup(win, tr("Electroforesis a pH {ph}: ¿hacia dónde migra {nombre} (pI {pi})?",
                    ph=ph, nombre=AA[aa]["nombre"], pi=AA[aa]["pi"]), tr("Electroforesis"),
            ancho=66, esperar=False)
    op = d.menu(win, tr("¿Cuál?"), ops, y=win.getmaxyx()[0] - len(ops) - 4)
    bien = op == real
    d.popup(win, (tr("Correcto.") if bien else tr("No.")) + " "
            + tr("A pH {ph} su carga neta es {q:+.1f}: por debajo del pI es +, por encima es −.",
                 ph=ph, q=q), tr("Electroforesis"), attr=d.c("bien" if bien else "mal"))
    return bien


def _intercambio(win, juego):
    tres = random.sample(datos.ORDEN, 3)
    ph = 6.0
    cargas = {c: round(carga(c, ph), 1) + 0.0 for c in tres}
    primero = min(tres, key=lambda c: cargas[c])       # intercambio catiónico: el más − sale primero
    ops = [AA[c]["nombre"] for c in tres]
    win.erase()
    d.popup(win, tr("Columna de intercambio CATIÓNICO (resina −) a pH 6 con {a}, {b} y "
                    "{c}: ¿cuál sale primero?", a=ops[0], b=ops[1], c=ops[2]),
            tr("Intercambio iónico"), ancho=66, esperar=False)
    op = d.menu(win, tr("¿Cuál?"), ops, y=win.getmaxyx()[0] - len(ops) - 4)
    bien = op is not None and tres[op] == primero
    detalle = ", ".join(f"{AA[c]['tres']} {cargas[c]:+.1f}" for c in tres)
    d.popup(win, (tr("Correcto.") if bien else tr("No: sale primero {n}.", n=AA[primero]["nombre"]))
            + " " + tr("La resina negativa retiene lo positivo; lo más negativo pasa de largo. "
                       "Cargas a pH 6: {d}.", d=detalle), tr("Intercambio iónico"),
            attr=d.c("bien" if bien else "mal"))
    return bien


def laboratorio(win, juego):
    """El laboratorio del René-virus: 6 problemas de proteómica clásica."""
    d.dialogo(win, [tr("Bienvenida a mi laboratorio de proteómica. Aquí la química de cada "
                       "aminoácido se mide: titulación, electroforesis e intercambio iónico. "
                       "Son 6 problemas.")], tr("René-virus"))
    juegos = [_titulacion, _electroforesis, _intercambio] * 2
    random.shuffle(juegos)
    aciertos = sum(1 for f in juegos if f(win, juego))
    mejor = juego.setdefault("records", {})
    nuevo = aciertos > mejor.get("laboratorio", 0)
    if nuevo:
        mejor["laboratorio"] = aciertos
    progreso.guardar(juego)
    d.popup(win, tr("{n}/6 problemas resueltos.", n=aciertos)
            + (" " + tr("¡Nuevo récord!") if nuevo else ""), tr("Laboratorio del René-virus"),
            attr=d.c("bien" if aciertos >= 5 else "texto"))
