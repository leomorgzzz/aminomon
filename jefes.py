"""Jefes de zona (construir péptidos), examen de la Chaperona y el reto final
del Ribosoma Maestro (traducción y mutaciones clínicas)."""

import curses
import random

import datos
import dibujo as d
import preguntas
import progreso

AA = datos.AMINOACIDOS
CARGA = {"K": 1, "R": 1, "D": -1, "E": -1}


def gravy(seq):
    return sum(AA[c]["hidropatia"] for c in seq) / len(seq) if seq else 0.0


def carga_neta(seq):
    return sum(CARGA.get(c, 0) for c in seq)


def carga_ph(seq, ph):
    return sum(datos.carga_cadena(c, ph) for c in seq)


def marco_colageno(seq):
    """Devuelve el marco (0, 1 o 2) en el que hay Gly cada 3 residuos, o None."""
    if len(seq) < 9:
        return None
    for o in range(3):
        if all(seq[i] == "G" for i in range(o, len(seq), 3)):
            return o
    return None


def frac_st(seq):
    return sum(c in "ST" for c in seq) / len(seq) if seq else 0.0


JEFES = {
    "membrana": dict(
        nombre="Guardián de la Membrana", reto="Hélice transmembrana",
        desc="Construye un segmento que pueda atravesar la bicapa: al menos 6 "
             "residuos con GRAVY > 1.5.",
        utiles="VLIFAM",
        condiciones=lambda s: [("Al menos 6 residuos", len(s) >= 6),
                               ("GRAVY > 1.5", len(s) > 0 and gravy(s) > 1.5)],
        bio="Las hélices transmembrana reales tienen ~20 residuos no polares: "
            "≈ 30 Å, el grosor del núcleo de la bicapa. Así las predice el "
            "gráfico de hidropatía de Kyte-Doolittle.",
        premio=("ATP", 3),
    ),
    "citosol": dict(
        nombre="Guardiana del Citosol", reto="Proteína soluble y regulable",
        desc="Construye una superficie soluble: al menos 6 residuos, GRAVY < "
             "−1.0 y al menos un sitio de fosforilación (S, T o Y).",
        utiles="STYNQ",
        condiciones=lambda s: [("Al menos 6 residuos", len(s) >= 6),
                               ("GRAVY < −1.0", len(s) > 0 and gravy(s) < -1.0),
                               ("Contiene S, T o Y", any(c in "STY" for c in s))],
        bio="Las proteínas solubles exponen residuos polares al agua. Los "
            "S/T/Y expuestos son blancos de quinasas: así se encienden y "
            "apagan las vías de señalización.",
        premio=("ATP", 3),
    ),
    "nucleo": dict(
        nombre="Complejo del Poro Nuclear", reto="Señal de localización nuclear",
        desc="Para entrar al núcleo, construye una NLS: entre 4 y 8 residuos "
             "con carga neta ≥ +4 (K, R = +1; D, E = −1).",
        utiles="KR",
        condiciones=lambda s: [("Entre 4 y 8 residuos", 4 <= len(s) <= 8),
                               ("Carga neta ≥ +4", carga_neta(s) >= 4)],
        bio="La NLS clásica es PKKKRKV (antígeno T de SV40). Las importinas "
            "reconocen ese parche básico y llevan la proteína a través del "
            "poro nuclear. Ya puedes cruzar los poros.",
        premio=("ATP", 3),
    ),
    "re": dict(
        nombre="Guardiana del Retículo", reto="Señal de retención en el RE",
        desc="Las proteínas solubles del RE llevan una etiqueta en su extremo "
             "C-terminal para no escaparse. Construye un péptido de al menos 4 "
             "residuos que termine en esa señal: K-D-E-L.",
        utiles="KDEL",
        condiciones=lambda s: [("Al menos 4 residuos", len(s) >= 4),
                               ("Termina en KDEL", s.endswith("KDEL"))],
        bio="BiP, la PDI y la calreticulina terminan en KDEL. Si escapan al "
            "Golgi, el receptor de KDEL las regresa al RE en vesículas COPI.",
        premio=("Vitamina K", 2),
    ),
    "golgi": dict(
        nombre="Guardián del Golgi", reto="Dominio tipo mucina",
        desc="En el Golgi se añaden O-glicanos al OH de Ser y Thr. Construye un "
             "dominio tipo mucina: al menos 6 residuos y al menos 60% de S o T.",
        utiles="ST",
        condiciones=lambda s: [("Al menos 6 residuos", len(s) >= 6),
                               ("≥ 60% de Ser o Thr", frac_st(s) >= 0.6)],
        bio="Las mucinas tienen dominios ricos en Pro, Thr y Ser (PTS). En el "
            "Golgi, las GalNAc-transferasas ponen O-glicanos en casi todas sus "
            "Ser/Thr: la proteína queda cubierta de azúcares y atrapa agua "
            "(el moco).",
        premio=("ATP", 3),
    ),
    "lisosoma": dict(
        nombre="Guardiana del Lisosoma", reto="Sensor de pH",
        desc="Construye un péptido de 3 a 8 residuos casi neutro en el "
             "citosol (carga entre −1 y +1 a pH 7.4) que se vuelva claramente "
             "positivo en el lisosoma (carga ≥ +2 a pH 5). Se cuentan solo las "
             "cadenas laterales.",
        utiles="H",
        condiciones=lambda s: [("Entre 3 y 8 residuos", 3 <= len(s) <= 8),
                               ("Carga a pH 7.4 entre −1 y +1", -1 <= carga_ph(s, 7.4) <= 1),
                               ("Carga a pH 5.0 ≥ +2", carga_ph(s, 5.0) >= 2)],
        bio="La His (pKR 6) es la única cadena lateral que cambia mucho de "
            "carga entre pH 7.4 y 5. Así funcionan los péptidos que escapan de "
            "endosomas y muchos sensores de pH en proteínas.",
        premio=("ATP", 3),
    ),
    "mec": dict(
        nombre="Guardián del Colágeno", reto="Hebra de colágeno",
        desc="Construye una hebra con el patrón Gly-X-Y: al menos 9 residuos, "
             "una Gly cada 3 (puede empezar en la posición 1, 2 o 3) y al menos "
             "una P.",
        utiles="GP",
        condiciones=lambda s: [("Al menos 9 residuos", len(s) >= 9),
                               ("Gly cada 3 residuos", marco_colageno(s) is not None),
                               ("Contiene Pro", "P" in s)],
        bio="Cada tercer residuo debe ser Gly: es la única cadena lateral (un "
            "H) que cabe en el centro de la triple hélice. Las mutaciones de "
            "esas Gly causan osteogénesis imperfecta.",
        premio=("Vitamina C", 2),
    ),
}


def pista_faltantes(juego, zona):
    """Texto con los aminoácidos útiles que aún no tienes y dónde buscarlos."""
    faltan = [c for c in JEFES[zona]["utiles"] if not progreso.capturado(juego, c)]
    if not faltan:
        return ""
    partes = []
    for c in faltan:
        donde = ", ".join(datos.ZONAS[z]["nombre"] for z in datos.zonas_de(c))
        partes.append(f"{AA[c]['tres']} ({c}) → {donde}")
    return "Útiles y aún sin capturar: " + "; ".join(partes)


# ================================================== dibujo de tu péptido
CADENA = {
    "G": "H", "A": "CH₃", "V": "CH(CH₃)₂", "L": "CH₂CHMe₂", "I": "CHMeEt",
    "M": "(CH₂)₂SCH₃", "P": "(CH₂)₃→N", "F": "CH₂-Ph", "Y": "CH₂-PhOH",
    "W": "CH₂-indol", "S": "CH₂OH", "T": "CHOHCH₃", "C": "CH₂SH",
    "N": "CH₂CONH₂", "Q": "(CH₂)₂CONH₂", "D": "CH₂COO⁻", "E": "(CH₂)₂COO⁻",
    "K": "(CH₂)₄NH₃⁺", "R": "…guan⁺", "H": "CH₂-imid",
}
CELDA = 11


def _nota(zona, seq, i):
    """Anotación química bajo cada residuo según el reto."""
    c = seq[i]
    if zona == "citosol":
        if c in "STY":
            return "◆ quinasa", "NEG"
        return ("H₂O ✓", "agua") if AA[c]["hidropatia"] < 0 else ("", "tenue")
    if zona == "nucleo":
        return {"K": ("+ importina", "POS"), "R": ("+ importina", "POS"),
                "D": ("−", "NEG"), "E": ("−", "NEG")}.get(c, ("", "tenue"))
    if zona == "re":
        return ("▶ receptor", "titulo") if i >= len(seq) - 4 else ("", "tenue")
    if zona == "golgi":
        return ("◇ O-GalNAc", "POL") if c in "ST" else ("", "tenue")
    if zona == "mec":
        o = marco_colageno(seq) or 0
        pos = (i - o) % 3
        return [("▼ centro", "titulo"), ("X (fuera)", "tenue"), ("Y (fuera)", "tenue")][pos]
    if zona == "lisosoma":
        return f"{carga_ph(c, 7.4):+.2f}→{carga_ph(c, 5.0):+.2f}", "POS" if c == "H" else "tenue"
    return "", "tenue"


def dibujar_peptido(win, y, x, ancho, seq, zona):
    """Cadena extendida N→C con las cadenas laterales alternando arriba y
    abajo (así quedan en una hebra extendida). Devuelve la fila siguiente."""
    por_fila = max(2, (ancho - 12) // CELDA)
    for ini in range(0, len(seq), por_fila):
        trozo = seq[ini:ini + por_fila]
        cx = x
        inicio = "H₃N⁺─" if ini == 0 else "  …─"
        d.put(win, y + 2, cx, inicio, d.c("tenue"))
        cx += len(inicio)
        for k, c in enumerate(trozo):
            i = ini + k
            a = AA[c]
            col = a["tipos"][0]
            centro = cx + 1
            arriba = i % 2 == 0
            lado = CADENA[c][: CELDA - 1]
            d.put(win, y + (0 if arriba else 4), centro, lado, d.c(col))
            d.put(win, y + (1 if arriba else 3), centro + 1, "│", d.c(col))
            d.put(win, y + 2, cx, f"[{a['tres']}]", d.c(col, curses.A_BOLD))
            fin = i == len(seq) - 1
            d.put(win, y + 2, cx + 5, "─COO⁻" if fin else ("─" * (CELDA - 5) if k < len(trozo) - 1 else "─…"),
                  d.c("tenue"))
            nota, ncol = _nota(zona, seq, i)
            d.put(win, y + 5, cx, nota[: CELDA - 1], d.c(ncol))
            cx += CELDA
        y += 7
    return y


def dibujar_membrana(win, y, x, seq):
    """La hélice cruza la bicapa: un residuo por fila entre las capas."""
    filas = ["agua", "cabezas"] + ["colas"] * len(seq) + ["cabezas", "agua"]
    for k, capa in enumerate(filas):
        glifo, col = {"agua": ("  H₂O  H₂O  ", "agua"), "cabezas": ("◦◦◦◦◦◦◦◦◦◦◦◦", "ARO"),
                      "colas": ("≈≈≈≈≈≈≈≈≈≈≈≈", "NP")}[capa]
        d.put(win, y + k, x, glifo, d.c(col))
        d.put(win, y + k, x + 26, glifo, d.c(col))
        if capa == "colas":
            c = seq[k - 2]
            a = AA[c]
            d.put(win, y + k, x + 14, f"{a['tres']}", d.c(a["tipos"][0], curses.A_BOLD))
            d.put(win, y + k, x + 40, f"KD {a['hidropatia']:+.1f}", d.c("tenue"))
    d.put(win, y + 1, x + 40, "N-terminal ↓", d.c("tenue"))
    return y + len(filas) + 1


def mostrar_exito(win, juego, zona, seq):
    j = JEFES[zona]
    alto, ancho = win.getmaxyx()
    win.erase()
    d.put(win, 0, 1, f"Reto superado: {j['reto']}  ·  {seq}", d.c("bien", curses.A_BOLD))
    if zona == "membrana":
        y = dibujar_membrana(win, 2, 2, seq[: max(1, alto - 14)])
    else:
        y = dibujar_peptido(win, 2, 1, ancho - 2, seq, zona)
    if zona == "lisosoma":
        d.put(win, y, 1, f"carga a pH 7.4: {carga_ph(seq, 7.4):+.2f}   →   a pH 5.0: "
                         f"{carga_ph(seq, 5.0):+.2f}", d.c("titulo"))
        y += 2
    objeto, n = j["premio"]
    texto = (f"{j['bio']}\n\nRecibes la insignia «{j['reto']}», {n} {objeto} y +10 XP "
             "para todo tu equipo.")
    for l in d.envolver(texto, min(ancho - 4, 96)):
        if y >= alto - 2:
            break
        d.put(win, y, 2, l, d.c("texto"))
        y += 1
    d.put(win, alto - 1, 1, "[Enter] seguir", d.c("tenue"))
    win.refresh()
    while d.tecla(win) not in d.ENTER:
        pass


def retar(win, juego, zona):
    j = JEFES[zona]
    conteo = progreso.conteo_equipo(juego)
    disponibles = sorted(conteo, key=datos.ORDEN.index)
    intro = (f"Reto: {j['reto']}.\n\n{j['desc']}\n\nUsa los aminoácidos de tu equipo, en "
             "código de 1 letra, del extremo N al C. Cada uno se puede usar tantas "
             "veces como lo tengas en el equipo (×n).")
    pista = pista_faltantes(juego, zona)
    if pista:
        intro += "\n\n" + pista
    d.dialogo(win, [intro], j["nombre"])
    seq = ""
    aviso = ""
    while True:
        alto, ancho = win.getmaxyx()
        win.erase()
        d.put(win, 0, 1, f"{j['nombre'].upper()} · {j['reto']}", d.c("mal", curses.A_BOLD))
        y = 2
        for l in d.envolver(j["desc"], ancho - 4):
            d.put(win, y, 1, l, d.c("texto"))
            y += 1
        y += 1
        d.put(win, y, 1, "En tu equipo:", d.c("tenue"))
        cx = 15
        for c in disponibles:
            a = AA[c]
            quedan = conteo[c] - seq.count(c)
            texto = f"{c}={a['tres']}×{quedan}({a['hidropatia']:+.1f}) "
            if cx + len(texto) > ancho - 1:
                y += 1
                cx = 15
            d.put(win, y, cx, texto, d.c(a["tipos"][0]) if quedan else d.c("oscuro"))
            cx += len(texto)
        if not disponibles:
            d.put(win, y, 15, "(ninguno)", d.c("mal"))
        if pista:
            y += 1
            for l in d.envolver(pista, ancho - 4):
                y += 1
                d.put(win, y, 1, l, d.c("agua"))
        y += 2
        d.put(win, y, 1, "Secuencia: N─", d.c("texto"))
        cx = 14
        for c in seq:
            d.put(win, y, cx, c, d.c(AA[c]["tipos"][0], curses.A_BOLD))
            cx += 1
        d.put(win, y, cx, "_", d.c("tenue", curses.A_BLINK))
        y += 2
        resumen = (f"Largo {len(seq)}   GRAVY {gravy(seq):+.2f}   "
                   f"Carga neta pH 7 {carga_neta(seq):+d}")
        if zona == "lisosoma":
            resumen = (f"Largo {len(seq)}   Carga pH 7.4 {carga_ph(seq, 7.4):+.2f}   "
                       f"Carga pH 5.0 {carga_ph(seq, 5.0):+.2f}")
        if zona == "golgi":
            resumen += f"   Ser+Thr {frac_st(seq):.0%}"
        d.put(win, y, 1, resumen, d.c("titulo"))
        conds = j["condiciones"](seq)
        for i, (texto, ok) in enumerate(conds):
            d.put(win, y + 2 + i, 3, f"{'✓' if ok else '✗'} {texto}",
                  d.c("bien" if ok else "mal"))
        if aviso:
            d.put(win, y + 3 + len(conds), 1, aviso, d.c("mal"))
        d.put(win, alto - 1, 1, "Letras: agregar  Retroceso: borrar  Enter: presentar  "
                                "? manual  Esc salir", d.c("tenue"))
        win.refresh()
        k = d.tecla(win)
        aviso = ""
        if k == d.ESC:
            return False
        if k in d.ENTER:
            if all(ok for _, ok in conds):
                break
            aviso = "Todavía no cumple todas las condiciones."
        elif k in (curses.KEY_BACKSPACE, "\x7f", "\b", 127, 8):
            seq = seq[:-1]
        elif k == "?":
            import manual
            manual.mostrar(win, juego, "chuleta")
        elif isinstance(k, str) and k.isalpha():
            c = k.upper()
            if c not in AA:
                aviso = f"'{c}' no es el código de ningún aminoácido estándar."
            elif c not in disponibles:
                donde = ", ".join(datos.ZONAS[z]["nombre"] for z in datos.zonas_de(c))
                aviso = f"No tienes {AA[c]['nombre']} ({c}) en tu equipo. Búscalo en: {donde}."
            elif seq.count(c) >= conteo[c]:
                donde = ", ".join(datos.ZONAS[z]["nombre"] for z in datos.zonas_de(c))
                aviso = (f"Solo tienes {conteo[c]} {AA[c]['nombre']} ({c}) en tu equipo. "
                         f"Captura más en: {donde}.")
            elif len(seq) < 20:
                seq += c

    juego["insignias"].append(zona)
    objeto, n = j["premio"]
    juego["objetos"][objeto] = juego["objetos"].get(objeto, 0) + n
    for m in juego["equipo"]:
        progreso.dar_xp(m, 10)
    mostrar_exito(win, juego, zona, seq)
    return True


# ===================================================== examen: plegamiento
# Cada acierto pliega una parte de la proteína. (fila, col, texto, color)
PLIEGUE = [
    ("hélice α 1: C=O(i) ··· H–N(i+4)",
     [(0, 0, " _   _   _", "titulo"), (1, 0, "/ \\_/ \\_/ \\_", "titulo")]),
    ("hélice α 2",
     [(0, 20, " _   _   _", "titulo"), (1, 20, "/ \\_/ \\_/ \\_", "titulo")]),
    ("lazo que une las dos hélices",
     [(1, 13, "╭─────╮", "tenue"), (2, 13, "│     │", "tenue")]),
    ("hebra β 1", [(4, 0, "══════════►", "POL")]),
    ("giro β (Gly–Pro) que dobla la cadena", [(4, 11, "╮", "NP"), (5, 11, "│", "NP"), (6, 11, "╯", "NP")]),
    ("hebra β 2: lámina antiparalela", [(6, 0, "◄══════════", "POL")]),
    ("puentes de H entre las hebras", [(5, 1, "⁞  ⁞  ⁞  ⁞", "titulo")]),
    ("núcleo hidrofóbico: Leu, Ile, Val, Phe adentro",
     [(3, 15, "●Leu ●Ile", "NP"), (4, 15, "●Val ●Phe", "NP")]),
    ("puente salino en la superficie: Lys⁺···⁻Asp", [(6, 15, "Lys⁺···⁻Asp", "POS")]),
    ("puente disulfuro Cys–S–S–Cys (proteína secretada)", [(7, 2, "Cys─S─S─Cys", "titulo")]),
]


def dibujar_pliegue(win, y, x, aciertos, fallos):
    d.caja(win, y, x, 12, 40, f"Plegamiento {aciertos}/10")
    for k, (texto, piezas) in enumerate(PLIEGUE):
        for fy, fx, t, col in piezas:
            if k < aciertos:
                d.put(win, y + 1 + fy, x + 2 + fx, t, d.c(col, curses.A_BOLD))
            else:
                d.put(win, y + 1 + fy, x + 2 + fx, "·" * len(t.strip()), d.c("oscuro"))
    if fallos:
        d.put(win, y + 9, x + 2, ("~" * fallos)[:30] + " mal plegado", d.c("mal"))
    if aciertos:
        d.put(win, y + 10, x + 2, ("✓ " + PLIEGUE[aciertos - 1][0])[:36], d.c("bien"))


def chaperona(win, juego):
    if len(juego["insignias"]) < len(JEFES):
        faltan = [JEFES[z]["reto"] for z in JEFES if z not in juego["insignias"]]
        d.popup(win, "La Hsp70 asiste el plegamiento de las proteínas recién "
                     f"sintetizadas. Para presentar su examen necesitas las {len(JEFES)} "
                     "insignias.\n\nPendientes: " + ", ".join(faltan), "Chaperona")
        return
    d.dialogo(win, ["Examen de 10 preguntas. Cada respuesta correcta pliega una "
                    "región de la proteína; con 8 alcanza su estado nativo."], "Chaperona")
    aciertos = fallos = 0
    for i in range(10):
        aa, tipo = preguntas.elegir_aleatoria(juego)
        alto, ancho = win.getmaxyx()
        win.erase()
        d.put(win, 0, 1, f"EXAMEN DE LA CHAPERONA · pregunta {i + 1}/10 · aciertos {aciertos}",
              d.c("titulo", curses.A_BOLD))
        if ancho >= 112:
            w = min(64, ancho - 46)
            dibujar_pliegue(win, 2, w + 4, aciertos, fallos)
            qy, qx = 2, 1
        else:
            w = min(70, ancho - 2)
            dibujar_pliegue(win, alto - 13, (ancho - 40) // 2, aciertos, fallos)
            qy, qx = 1, (ancho - w) // 2
        if preguntas.preguntar(win, juego, aa, tipo, qy, qx, w):
            aciertos += 1
        else:
            fallos += 1
    win.erase()
    alto, ancho = win.getmaxyx()
    dibujar_pliegue(win, 1, (ancho - 40) // 2, aciertos, fallos)
    if aciertos >= 8:
        juego["terminado"] = True
        texto = (f"{aciertos}/10. La proteína alcanzó su estado nativo: obtienes la "
                 "Maestría en Aminoácidos.\n\nPuedes seguir explorando. El siguiente "
                 "nivel es el examen del Ribosoma Maestro; habla con el Profesor "
                 "Ribosoma (R).")
        d.popup(win, texto, "Estado nativo", attr=d.c("bien"))
    else:
        d.popup(win, f"{aciertos}/10. Quedaron regiones hidrofóbicas expuestas: la "
                     "Hsp70 se une a ellas, gasta ATP y te deja intentar de nuevo. "
                     "Repasa el manual y vuelve cuando quieras.", "Chaperona")


# ================================================ reto final: Ribosoma Maestro
STOP = ("UAA", "UAG", "UGA")
CODIGO = {cod: c for c, a in AA.items() for cod in a["codones"]}
for _s in STOP:
    CODIGO[_s] = "*"

MUTACIONES = [
    dict(texto="Anemia falciforme (HbS): en la β-globina, Glu6 → Val (E6V). "
               "¿Qué cambia en ese residuo de la superficie?",
         correcta="Pierde una carga − y gana una cadena no polar: la Hb "
                  "desoxigenada polimeriza por ese parche hidrofóbico",
         otras=["Gana una carga + y forma un puente salino nuevo",
                "Se forma un puente disulfuro entre dos globinas",
                "Pierde un sitio de fosforilación"],
         expl="Glu es Cargado − (pKR 4.25); Val es No polar (KD +4.2). La Val6 "
              "encaja en un bolsillo hidrofóbico de otra Hb: se forman fibras y "
              "el eritrocito toma forma de hoz."),
    dict(texto="Hemoglobina C: Glu6 → Lys (E6K). ¿Cuánto cambia la carga de esa "
               "cadena lateral a pH 7?",
         correcta="+2 (de −1 a +1)", otras=["+1", "0", "−2"],
         expl="Glu a pH 7 es −1; Lys es +1. Por eso HbC migra distinto en la "
              "electroforesis."),
    dict(texto="Osteogénesis imperfecta: una Gly del colágeno tipo I (Gly-X-Y) "
               "cambia a Ser. ¿Por qué es tan grave?",
         correcta="La Gly es la única que cabe en el centro de la triple hélice; "
                  "cualquier cadena lateral la desestabiliza",
         otras=["La Ser se fosforila y repele a las otras cadenas",
                "La Ser forma un disulfuro con otra cadena",
                "La Ser vuelve al colágeno demasiado hidrofóbico"],
         expl="En la triple hélice, cada tercer residuo queda en el eje central, "
              "donde solo cabe un H. Sustituir esa Gly rompe el plegamiento: "
              "huesos frágiles."),
    dict(texto="Fibrosis quística: la mutación más común de CFTR (ΔF508) elimina "
               "una Phe. ¿Qué le pasa a la proteína?",
         correcta="Se pliega mal; el control de calidad del RE la retiene y la "
                  "manda a degradar (ERAD)",
         otras=["Se vuelve más ácida y precipita en el citosol",
                "Pierde su péptido señal y se queda en el citosol",
                "Gana un sitio de N-glicosilación y se acumula en el Golgi"],
         expl="Sin la Phe508 el dominio NBD1 no se pliega bien. Las chaperonas "
              "del RE la detectan, la ubiquitinan y el proteasoma la degrada: "
              "casi no llega a la membrana."),
    dict(texto="KRAS G12D (frecuente en cáncer de páncreas): Gly12 → Asp. "
               "¿Qué cambia?",
         correcta="Entra una cadena con carga − donde solo había un H: estorba "
                  "la hidrólisis de GTP y KRAS queda encendida",
         otras=["KRAS pierde su sitio de unión a ATP",
                "Se forma un puente disulfuro que la inactiva",
                "Nada: Gly y Asp son del mismo grupo"],
         expl="La Gly12 está pegada al sitio del GTP; cualquier cadena lateral "
              "impide que la GAP acelere la hidrólisis. KRAS-GTP sigue mandando "
              "señales de proliferación."),
    dict(texto="Fenilcetonuria: en la fenilalanina hidroxilasa, Arg408 → Trp "
               "(R408W). ¿Qué se pierde en ese sitio?",
         correcta="Una carga + que hacía puentes salinos; entra un anillo grande "
                  "sin carga y la enzima se pliega mal",
         otras=["Un sitio de fosforilación",
                "Un puente disulfuro",
                "Un grupo Ácido que unía al cofactor"],
         expl="Arg es Cargado + (pKR 12.5); Trp es Aromático. Sin la enzima, la "
              "Phe se acumula y la Tyr se vuelve esencial para el paciente."),
    dict(texto="Enfermedad de Huntington: la huntingtina tiene demasiadas "
               "repeticiones del codón CAG. ¿Qué tramo se alarga en la proteína?",
         correcta="Poliglutamina (CAG = Gln)",
         otras=["Polialanina (CAG = Ala)", "Poliserina (CAG = Ser)",
                "Policisteína (CAG = Cys)"],
         expl="CAG codifica Gln. Con más de ~36 repeticiones, el tramo poli-Q "
              "se agrega y daña las neuronas."),
    dict(texto="p53 R175H (mutación frecuente en cáncer). Arg e His son del "
               "grupo básico, ¿por qué la His no sustituye bien a la Arg?",
         correcta="Con pKR 6 la His casi no tiene carga a pH 7, mientras la Arg "
                  "(pKR 12.5) siempre es +",
         otras=["La His es más grande que la Arg",
                "La His es ácida a pH 7",
                "La His forma disulfuros"],
         expl="Estar en el mismo grupo de Lehninger no hace a dos residuos "
              "intercambiables: el pKR decide si la carga existe a pH 7."),
    dict(texto="El alelo de la HbS se debe a GAG → GUG en el codón 6. ¿Qué tipo "
               "de mutación es?",
         correcta="De sentido erróneo (missense): Glu → Val",
         otras=["Silenciosa", "Sin sentido (nonsense)", "Corrimiento del marco de lectura"],
         expl="GAG = Glu y GUG = Val: cambia un aminoácido por otro."),
    dict(texto="Un codón UGG (Trp) muta a UGA. ¿Qué le pasa a la proteína?",
         correcta="UGA es codón de paro: la proteína sale truncada (mutación sin sentido)",
         otras=["Nada: UGA también codifica Trp", "Se cambia Trp por Cys",
                "Se corre el marco de lectura"],
         expl="UAA, UAG y UGA son los codones de paro (en mitocondrias humanas "
              "UGA sí es Trp, pero no en el citosol)."),
    dict(texto="Un codón CUU (Leu) muta a CUC. ¿Efecto en la proteína?",
         correcta="Ninguno: CUC también es Leu (mutación silenciosa)",
         otras=["Leu → Pro", "Leu → Phe", "Codón de paro"],
         expl="El código es degenerado: Leu tiene 6 codones (UUA, UUG, CUU, "
              "CUC, CUA, CUG)."),
]


def _arn_aleatorio():
    """ARNm con 5'UTR (sin AUG), un marco abierto y 3'UTR."""
    prot = "M" + "".join(random.choice(datos.ORDEN) for _ in range(random.randint(4, 6)))
    orf = "".join(random.choice(AA[c]["codones"]) for c in prot) + random.choice(STOP)
    while True:
        utr5 = "".join(random.choice("ACGU") for _ in range(random.randint(5, 8)))
        utr3 = "".join(random.choice("ACGU") for _ in range(random.randint(3, 6)))
        arn = utr5 + orf + utr3
        if arn.find("AUG") == len(utr5):
            return arn, prot, len(utr5)


def traducir(win, juego, n, total):
    arn, prot, ini = _arn_aleatorio()
    alto, ancho = win.getmaxyx()
    win.erase()
    d.put(win, 0, 1, f"RIBOSOMA MAESTRO · {n}/{total} · Traducción", d.c("titulo", curses.A_BOLD))
    texto = ("Lee este ARNm como un ribosoma: busca el primer AUG, lee de 3 en 3 "
             "y detente en el codón de paro (UAA, UAG o UGA). Escribe la proteína "
             "en código de 1 letra (incluye la Met inicial, no el paro).")
    y = 2
    for l in d.envolver(texto, min(ancho - 4, 90)):
        d.put(win, y, 2, l, d.c("texto"))
        y += 1
    y += 1
    d.put(win, y, 2, f"5'-{arn}-3'", d.c("titulo", curses.A_BOLD))
    y += 2
    r = d.pedir_texto(win, y, 2, "Proteína: ", 12)
    respuesta = (r or "").strip().upper()
    bien = respuesta == prot
    codones = [arn[i:i + 3] for i in range(ini, ini + 3 * (len(prot) + 1), 3)]
    lectura = "  ".join(f"{cod}={CODIGO[cod] if CODIGO[cod] != '*' else 'paro'}" for cod in codones)
    progreso.registrar(juego, "maestro:traduccion", bien)
    d.popup(win, ("Correcto. " if bien else f"Incorrecto. Era {prot}. ")
            + f"UTR 5' de {ini} nt, luego: {lectura}",
            "Traducción", ancho=min(ancho - 2, 90), attr=d.c("bien" if bien else "mal"))
    return bien


def mutacion(win, juego, caso, n, total):
    alto, ancho = win.getmaxyx()
    win.erase()
    d.put(win, 0, 1, f"RIBOSOMA MAESTRO · {n}/{total} · Mutaciones reales",
          d.c("titulo", curses.A_BOLD))
    w = min(ancho - 2, 90)
    x = (ancho - w) // 2
    ops = [caso["correcta"]] + caso["otras"]
    random.shuffle(ops)
    lineas = d.envolver(caso["texto"], w - 4)
    y = 2
    d.caja(win, y, x, len(lineas) + 3 + sum(len(d.envolver(o, w - 10)) for o in ops) + 2, w, "Pregunta")
    for l in lineas:
        y += 1
        d.put(win, y, x + 2, l, d.c("texto", curses.A_BOLD))
    y += 1
    for i, o in enumerate(ops):
        for k, l in enumerate(d.envolver(o, w - 10)):
            y += 1
            d.put(win, y, x + 4, (f"{i + 1}) " if k == 0 else "   ") + l, d.c("texto"))
    d.put(win, y + 2, x + 2, "Pulsa el número de tu respuesta", d.c("tenue"))
    win.refresh()
    while True:
        k = d.tecla(win)
        if isinstance(k, str) and k in "1234":
            break
    bien = ops[int(k) - 1] == caso["correcta"]
    progreso.registrar(juego, "maestro:mutacion", bien)
    d.popup(win, ("Correcto. " if bien else f"Incorrecto. Era: {caso['correcta']}.\n\n")
            + caso["expl"], "Resultado", ancho=w, attr=d.c("bien" if bien else "mal"))
    return bien


def ribosoma_maestro(win, juego):
    d.dialogo(win, [
        "Traduce 3 ARNm y analiza 5 mutaciones asociadas a enfermedades "
        "humanas. Se aprueba con 7 de 8."], "Ribosoma Maestro")
    total = 8
    aciertos = 0
    for n in range(1, 4):
        aciertos += traducir(win, juego, n, total)
    for n, caso in enumerate(random.sample(MUTACIONES, 5), start=4):
        aciertos += mutacion(win, juego, caso, n, total)
    if aciertos >= 7:
        juego["doctorado"] = True
        d.popup(win, f"{aciertos}/8. Aprobado: Doctorado en Proteínas.",
                "Ribosoma Maestro", attr=d.c("bien"))
    else:
        d.popup(win, f"{aciertos}/8. No aprobado. Repasa los codones (pestaña "
                     "Chuleta) y las propiedades de cada grupo; las preguntas "
                     "cambian en cada intento.", "Ribosoma Maestro")
