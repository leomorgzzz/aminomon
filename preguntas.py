"""Preguntas de captura y de la Chaperona, con repaso espaciado."""

import curses
import random

import datos
import dibujo as d
import progreso
from idioma import tr

AA = datos.AMINOACIDOS

TIPOS_PROPIEDAD = ["carga", "grupo", "nutricion", "codon", "hidro", "pka", "pi",
                   "calc_pi"]
# reconocer la estructura, en orden de dificultad
RECONOCER = ["nombre", "tres", "una"]
# letras que no salen del nombre: opciones que confunden
TRAMPAS_UNA = {"W": "TPY", "K": "LYI"}
# estructuras que se parecen: salen como distractores para que reconocer cueste
PARECIDOS = {
    "G": "ASP", "A": "GSV", "V": "ILT", "L": "IVM", "I": "LVT", "M": "CLI", "P": "VAL",
    "F": "YWH", "Y": "FWH", "W": "FYH", "S": "TCA", "T": "SVC", "C": "SMA", "N": "QDE",
    "Q": "NEK", "D": "ENS", "E": "DQN", "K": "RQM", "R": "KHQ", "H": "RKW",
}


def pares():
    """Aminoácidos que se confunden: {aa: (pareja o None, cómo distinguirlos)}."""
    qn = tr("Gln (Q) y Asn (N) son las amidas: Gln tiene un CH2 más, igual que Glu "
            "frente a Asp. N de asparagiNe; Q de 'Q-tamina'.")
    ed = tr("Glu (E) y Asp (D) son los ácidos: Glu tiene un CH2 más. Asp es el corto y "
            "va primero, como la D antes de la E.")
    il = tr("Ile y Leu tienen la misma fórmula: Ile se ramifica en el carbono β (pegado "
            "al Cα) y Leu en el γ, un carbono más lejos.")
    st = tr("Ser (S) termina en CH2-OH; Thr (T) tiene además un metilo en el carbono β: "
            "CH(OH)-CH3.")
    return {
        "Q": ("N", qn), "N": ("Q", qn), "E": ("D", ed), "D": ("E", ed),
        "I": ("L", il), "L": ("I", il), "S": ("T", st), "T": ("S", st),
        "W": (None, tr("Trp = W: anillo doble (double ring). La T ya era de Thr y la P "
                       "de Pro.")),
        "K": (None, tr("Lys = K: la letra antes de L, porque la L ya era de Leu.")),
    }


def _nota_par(aa):
    par = pares().get(aa)
    return " " + par[1] if par else ""


def aplica(aa, tipo):
    a = AA[aa]
    if tipo in ("pka", "calc_pi"):
        return a["pkr"] is not None
    return True


def _opciones(correcta, distractores, n=4, fijos=()):
    """fijos: distractores que siempre aparecen (la pareja que se confunde)."""
    fijos = [x for x in dict.fromkeys(fijos) if x != correcta][: n - 1]
    distractores = [x for x in dict.fromkeys(distractores) if x != correcta and x not in fijos]
    random.shuffle(distractores)
    ops = [correcta] + fijos + distractores[: n - 1 - len(fijos)]
    random.shuffle(ops)
    return ops


def generar(aa, tipo, estructura=False, opciones=False):
    """Devuelve dict(texto, opciones|None, respuesta, explicacion).
    estructura: el jugador ve la estructura, así que los códigos se piden sin
    decir el nombre. opciones: los códigos se eligen en vez de escribirse."""
    a = AA[aa]
    pareja = pares().get(aa, (None, ""))[0]
    # la pareja que se confunde siempre; después, otras estructuras parecidas
    parecidos = random.sample(PARECIDOS[aa], len(PARECIDOS[aa]))
    cercanos = ([pareja] if pareja else []) + [x for x in parecidos if x != pareja]
    if tipo == "nombre":
        mismos = [x["nombre"] for x in AA.values() if x["grupo"] == a["grupo"]]
        otros = [x["nombre"] for x in AA.values()]
        random.shuffle(otros)
        return dict(
            texto=tr("¿Qué aminoácido es este? Fíjate en su cadena lateral."),
            opciones=_opciones(a["nombre"], mismos + otros,
                               fijos=[AA[x]["nombre"] for x in cercanos]),
            respuesta=a["nombre"],
            explicacion=tr("Es {nombre} ({tres}, {una}). {pista}", nombre=a["nombre"],
                           tres=a["tres"], una=aa, pista=a["pista"]) + _nota_par(aa),
        )
    if tipo == "tres":
        if estructura:
            texto = tr("¿Cuál es el código de 3 letras de este aminoácido?")
        else:
            texto = tr("Escribe el código de 3 letras de {nombre}:", nombre=a["nombre"])
        ops = None
        if opciones:
            ops = _opciones(a["tres"], [x["tres"] for x in AA.values()],
                            fijos=[AA[x]["tres"] for x in cercanos])
        return dict(
            texto=texto, opciones=ops, respuesta=a["tres"],
            explicacion=f"{a['nombre']} = {a['tres']}." + _nota_par(aa),
        )
    if tipo == "una":
        if estructura:
            texto = tr("¿Cuál es el código de 1 letra de este aminoácido?")
        else:
            texto = tr("Escribe el código de 1 letra de {nombre} ({tres}):",
                       nombre=a["nombre"], tres=a["tres"])
        ops = None
        if opciones:
            ops = _opciones(aa, list(datos.ORDEN), fijos=list(TRAMPAS_UNA.get(aa, "")) or cercanos)
        return dict(
            texto=texto, opciones=ops, respuesta=aa,
            explicacion=f"{a['tres']} = {aa}. " + (_nota_par(aa).strip() or _mnemo_una(aa)),
        )
    if tipo == "carga":
        ops = [tr("Positiva (+1)"), tr("Negativa (−1)"), tr("Neutra"),
               tr("Mayormente neutra (+ parcial)")]
        expl = {
            "acido": tr("Su carboxilo (pKR ~4) ya perdió el H+ a pH 7."),
            "basico": tr("Su grupo básico conserva el H+ a pH 7."),
        }.get(a["grupo"], tr("No tiene grupos que se ionicen a pH 7."))
        if aa == "H":
            expl = tr("Su imidazol tiene pKR ≈ 6: a pH 7 solo ~10% está protonado.")
        if aa in "CY":
            expl = tr("Su pKR ({pkr}) es mayor que 7: a pH 7 conserva el H+ y queda "
                      "neutra.", pkr=a["pkr"])
        return dict(
            texto=tr("¿Carga de la cadena lateral de {nombre} a pH 7?", nombre=a["nombre"]),
            opciones=ops, respuesta=a["carga"], explicacion=expl,
        )
    if tipo == "grupo":
        return dict(
            texto=tr("¿A qué grupo (Lehninger) pertenece {nombre}?", nombre=a["nombre"]),
            opciones=list(datos.GRUPOS.values()), respuesta=datos.GRUPOS[a["grupo"]],
            explicacion=f"{a['nombre']}: {datos.GRUPOS[a['grupo']]}. {a['pista']}",
        )
    if tipo == "nutricion":
        return dict(
            texto=tr("En humanos, {nombre} es…", nombre=a["nombre"]),
            opciones=list(datos.NUTRICION),
            respuesta=a["nutricion"],
            explicacion=tr("Esenciales (9): His Ile Leu Lys Met Phe Thr Trp Val. "
                           "Condicionales (6): Arg Cys Gln Gly Pro Tyr. "
                           "No esenciales (5): Ala Asp Asn Glu Ser."),
        )
    if tipo == "codon":
        otros = [cod for k, x in AA.items() if k != aa for cod in x["codones"]]
        correcta = random.choice(a["codones"])
        return dict(
            texto=tr("¿Cuál de estos codones codifica {nombre}?", nombre=a["nombre"]),
            opciones=_opciones(correcta, otros), respuesta=correcta,
            explicacion=f"{a['tres']}: {', '.join(a['codones'])}.",
        )
    if tipo == "hidro":
        fobico, filico = tr("Hidrofóbico (KD > 0)"), tr("Hidrofílico (KD < 0)")
        return dict(
            texto=tr("Según Kyte-Doolittle, {nombre} es…", nombre=a["nombre"]),
            opciones=[fobico, filico],
            respuesta=fobico if a["hidropatia"] > 0 else filico,
            explicacion=tr("KD de {tres} = {kd:+.1f}. ", tres=a["tres"], kd=a["hidropatia"])
                        + datos.NOTA_KD.get(aa, ""),
        )
    if tipo == "pka":
        correcta = f"{a['pkr']:.2f}"
        otros = [f"{x['pkr']:.2f}" for x in AA.values() if x["pkr"] and x["pkr"] != a["pkr"]]
        return dict(
            texto=tr("¿pKR (cadena lateral) de {nombre}?", nombre=a["nombre"]),
            opciones=_opciones(correcta, otros), respuesta=correcta,
            explicacion=tr("pKR (Lehninger, 25 °C): Asp 3.65, Glu 4.25, His 6.00, Cys 8.18, "
                           "Tyr 10.07, Lys 10.53, Arg 12.48."),
        )
    if tipo == "pi":
        correcta = f"{a['pi']:.2f}"
        otros = [f"{x['pi']:.2f}" for x in AA.values() if abs(x["pi"] - a["pi"]) > 0.05]
        pi, (p1, p2) = datos.calcular_pi(aa)
        return dict(
            texto=(tr("{nombre}: pK1 {pk1:.2f}, pK2 {pk2:.2f}, pKR {pkr:.2f}. ¿Su punto "
                      "isoeléctrico (pI)?", nombre=a["nombre"], pk1=a["pk1"], pk2=a["pk2"],
                      pkr=a["pkr"]) if a["pkr"] else
                   tr("{nombre}: pK1 {pk1:.2f}, pK2 {pk2:.2f}. ¿Su punto isoeléctrico (pI)?",
                      nombre=a["nombre"], pk1=a["pk1"], pk2=a["pk2"])),
            opciones=_opciones(correcta, otros), respuesta=correcta,
            explicacion=tr("pI = ({p1:.2f} + {p2:.2f}) / 2 = {pi:.2f}. Extremos: Asp "
                           "2.77 (el más ácido) y Arg 10.76 (el más básico).",
                           p1=p1, p2=p2, pi=a["pi"]),
        )
    if tipo == "calc_pi":
        pi, (p1, p2) = datos.calcular_pi(aa)
        pks = [a["pk1"], a["pk2"], a["pkr"]]
        candidatos = {f"{(x + y) / 2:.2f}" for i, x in enumerate(pks)
                      for y in pks[i + 1:]}
        correcta = f"{a['pi']:.2f}"
        otros = [o for o in list(candidatos) + [f"{a['pkr']:.2f}", f"{a['pk2']:.2f}"]
                 if abs(float(o) - a["pi"]) > 0.05]
        tipo_g = (tr("ácido") if a["grupo"] == "acido" else tr("básico") if a["grupo"] == "basico"
                  else tr("con cadena ionizable"))
        return dict(
            texto=tr("{nombre}: pK1 {pk1:.2f}, pK2 {pk2:.2f}, pKR {pkr:.2f}. Calcula su pI:",
                     nombre=a["nombre"], pk1=a["pk1"], pk2=a["pk2"], pkr=a["pkr"]),
            opciones=_opciones(correcta, otros), respuesta=correcta,
            explicacion=tr("Se promedian los dos pKa que rodean la forma neutra. "
                           "Para este aminoácido {tipo}: ({p1:.2f} + {p2:.2f}) / 2 = "
                           "{pi:.2f}.", tipo=tipo_g, p1=p1, p2=p2, pi=a["pi"]),
        )
    raise ValueError(tipo)


def _mnemo_una(aa):
    trucos = {
        "F": "F de 'Fenilalanina'.", "Y": "Y de 'tYrosina'.",
        "W": "W: el triptófano tiene un anillo doble (double ring → W).",
        "N": "N de 'asparagiNe'.", "Q": "Q de 'Q-tamina' (Glutamina).",
        "D": "D de 'asparDate' (Asp, el más pequeño de los ácidos).",
        "E": "E de 'glutEmate'.", "K": "K: la letra antes de L (lisina).",
        "R": "R de 'aRginina'.",
        "I": "I de 'Isoleucina'; la L se la quedó Leu.",
        "T": "T de 'Treonina'; la S es de Ser.",
    }
    return tr(trucos.get(aa, "Coincide con la inicial."))


def dominado(juego, aa, tipo):
    """Lo dominas cuando lo has acertado más veces de las que lo has fallado."""
    clave = f"{aa}:{tipo}"
    return juego["aciertos"].get(clave, 0) > juego["fallos"].get(clave, 0)


def nivel(juego, aa):
    """0 nombre, 1 código de 3 letras, 2 código de 1 letra, 3 todo dominado."""
    return next((i for i, t in enumerate(RECONOCER) if not dominado(juego, aa, t)), 3)


def dominados(juego):
    """Cuántos de los 20 ya reconoces por nombre y por los dos códigos."""
    return sum(nivel(juego, aa) == 3 for aa in datos.ORDEN)


def elegir_reconocer(juego, aa):
    """Solo reconocimiento: el paso en que va, o cualquiera si ya lo domina."""
    n = nivel(juego, aa)
    if n < 3:
        return RECONOCER[n]
    return random.choices(RECONOCER, [progreso.peso(juego, f"{aa}:{t}") for t in RECONOCER])[0]


def elegir_tipo(juego, aa):
    """Para atrapar hay que reconocerlo: primero el nombre, luego el código de 3
    letras y luego el de 1; solo se sube al acertar más de lo que se falla.
    Ya dominado, el reconocimiento se sigue repasando junto a las propiedades."""
    n = nivel(juego, aa)
    if n < 3:
        return RECONOCER[n]
    tipos = RECONOCER + [t for t in TIPOS_PROPIEDAD if aplica(aa, t)]
    pesos = [progreso.peso(juego, f"{aa}:{t}") * (2 if t in RECONOCER else 1) for t in tipos]
    return random.choices(tipos, pesos)[0]


def elegir_aleatoria(juego, hechas=()):
    """Para la Chaperona: aminoácido y tipo ponderados por fallos. No repite ni el
    aminoácido ni el tipo de las ya hechas (mientras queden sin usar)."""
    claves = [(aa, t) for aa in datos.ORDEN for t in TIPOS_PROPIEDAD + ["tres", "una"]
              if aplica(aa, t)]
    usados_aa = {aa for aa, _ in hechas}
    usados_t = {t for _, t in hechas}
    for filtro in (lambda aa, t: aa not in usados_aa and t not in usados_t,
                   lambda aa, t: aa not in usados_aa,
                   lambda aa, t: (aa, t) not in hechas):
        libres = [k for k in claves if filtro(*k)]
        if libres:
            claves = libres
            break
    pesos = [progreso.peso(juego, f"{aa}:{t}") for aa, t in claves]
    return random.choices(claves, pesos)[0]


def preguntar(win, juego, aa, tipo, y, x, ancho, alto_min=0, estructura=False,
              opciones=False, salir=False, p=None):
    """Muestra la pregunta en un área y devuelve True si acierta. alto_min
    estira el recuadro para tapar por completo lo que haya debajo. Con salir,
    Esc la abandona sin contarla y devuelve None. p: una pregunta ya armada
    (la de la Sec, que no está en los 20)."""
    p = p or generar(aa, tipo, estructura, opciones)
    texto = d.envolver(p["texto"], ancho - 4)
    alto = max(alto_min, len(texto) + (len(p["opciones"]) if p["opciones"] else 2) + 4)
    d.limpiar_area(win, y, x, alto, ancho)
    # resaltado: aquí es donde hay que contestar
    d.caja(win, y, x, alto, ancho, tr("Pregunta · contesta aquí"), d.c("titulo", curses.A_BOLD), resaltar=True)
    for i, l in enumerate(texto):
        d.put(win, y + 1 + i, x + 2, l, d.c("texto", curses.A_BOLD))
    y1 = y + 1 + len(texto)
    if p["opciones"]:
        for i, o in enumerate(p["opciones"]):
            d.put(win, y1 + i, x + 4, f"{i + 1}) {o}", d.c("texto"))
        d.put(win, y + alto - 2, x + 2, tr("► Pulsa el número de tu respuesta") +
              (tr(" · Esc salir") if salir else ""), d.c("titulo", curses.A_BOLD))
        win.refresh()
        while True:
            k = d.tecla(win)
            if salir and k == d.ESC:
                return None
            if isinstance(k, str) and k.isdigit() and 1 <= int(k) <= len(p["opciones"]):
                eleccion = p["opciones"][int(k) - 1]
                break
    else:
        r = d.pedir_texto(win, y1 + 1, x + 4, "> ", 6)
        eleccion = (r or "").strip()
    bien = eleccion.lower() == p["respuesta"].lower()
    progreso.registrar(juego, f"{aa}:{tipo}", bien)
    if tipo in RECONOCER and aa in AA:
        progreso.repasar(juego, aa, bien)
    if not bien and tipo in RECONOCER and aa in AA:
        confundir(juego, aa, a_codigo(eleccion, tipo))
    if bien:
        texto = tr("Correcto. ") + p["explicacion"]
        attr = d.c("bien")
    else:
        texto = tr("Incorrecto. Era: {respuesta}. ", respuesta=p["respuesta"]) + p["explicacion"]
        attr = d.c("mal")
    d.popup(win, texto, tr("Resultado"), ancho=min(70, ancho + 6), attr=attr)
    return bien


def a_codigo(eleccion, tipo):
    """La opción elegida (nombre, código de 3 o de 1 letra) → código de 1 letra."""
    e = (eleccion or "").strip().lower()
    for c, a in AA.items():
        if e in (a["nombre"].lower(), a["tres"].lower(), c.lower()):
            return c
    return None


def confundir(juego, era, dijo):
    """Matriz de confusión: «cuando era Gln, contestaste Asn»."""
    if dijo and dijo != era:
        m = juego.setdefault("confusiones", {})
        m[f"{era}>{dijo}"] = m.get(f"{era}>{dijo}", 0) + 1


def confusiones(juego, aa=None):
    """[(era, dijo, veces)] de más a menos; con aa, solo las de ese aminoácido."""
    salida = []
    for clave, n in juego.get("confusiones", {}).items():
        era, dijo = clave.split(">")
        if aa is None or era == aa:
            salida.append((era, dijo, n))
    return sorted(salida, key=lambda x: -x[2])


PREGUNTAS_PRACTICA = 10


def practica(win, juego):
    """Menú de práctica: cinco formas de reconocer las estructuras."""
    capturados = [aa for aa in datos.ORDEN if juego["capturados"].get(aa)]
    if not capturados:
        d.popup(win, tr("Captura primero algún aminoácido."), tr("Práctica de reconocimiento"))
        return
    while True:
        record = juego.get("records", {}).get("reloj", 0)
        n_conf = len(confusiones(juego))
        hoy = len(progreso.para_hoy(juego))
        modos = ["hoy", "normal", "cadena", "elegir", "completar", "diferente", "mods",
                 "reloj", "confusiones"] + (["sec"] if juego.get("sec") else [])
        textos = [tr("Repaso de hoy: {n} por repasar", n=hoy),
                  tr("Estructura → nombre y códigos ({n} preguntas)", n=PREGUNTAS_PRACTICA),
                  tr("Solo la cadena lateral → nombre"),
                  tr("Nombre → elige su estructura entre 4"),
                  tr("Nombre → completa la cadena lateral"),
                  tr("¿Cuál es diferente? (4 estructuras, una no es del grupo)"),
                  tr("Modificaciones: ¿qué cambio es? ({n} descubiertas)",
                     n=len(juego["evos_vistas"])),
                  tr("Contrarreloj: 60 s, cuantas puedas (récord {r})", r=record),
                  tr("Tus confusiones ({n})", n=n_conf)] + (
                     [tr("¿Cys o Sec? (selenocisteína)")] if juego.get("sec") else []) + [tr("Volver")]
        win.erase()
        op = d.menu(win, tr("Práctica de reconocimiento"), textos)
        if op is None or op == len(modos):
            return
        modo = modos[op]
        if modo == "hoy" and not hoy:
            d.popup(win, tr("Hoy no te toca repasar ninguno. Los que aciertas vuelven en 1, "
                            "3, 7 y 14 días; los que fallas, al día siguiente."),
                    tr("Repaso de hoy"))
            continue
        if modo == "mods" and not juego["evos_vistas"]:
            d.popup(win, tr("Todavía no descubres ninguna modificación: se consiguen subiendo "
                            "de nivel a tu equipo en la zona correcta (Equipo → V)."),
                    tr("Modificaciones"))
            continue
        if modo == "confusiones" and not n_conf:
            d.popup(win, tr("Todavía no has confundido ningún aminoácido. Cuando falles uno, "
                            "aquí verás con cuál lo confundiste para practicar justo eso."),
                    tr("Tus confusiones"))
            continue
        if len(capturados) < 4 and modo == "elegir":
            d.popup(win, tr("Necesitas al menos 4 aminoácidos capturados para este modo."),
                    tr("Práctica de reconocimiento"))
            continue
        {"hoy": lambda w, j: _practica_normal(w, j, solo=set(progreso.para_hoy(j))),
         "normal": _practica_normal, "cadena": lambda w, j: _practica_normal(w, j, cadena=True),
         "elegir": _practica_elegir, "completar": _practica_completar,
         "diferente": _practica_diferente, "mods": _practica_mods, "reloj": _contrarreloj,
         "confusiones": _practica_confusiones,
         "sec": lambda w, j: __import__("posgame").practica_sec(w, j)}[modo](win, juego)
        # el logro se anuncia al cumplirlo, no hasta volver al mapa
        import logros
        logros.anunciar(win, juego)


def _solo_cadena(arte):
    """Las filas de la cadena lateral (sin H, Cα, NH3+ ni COO−)."""
    return arte[d._filas_esqueleto(arte):] or arte


def _practica_normal(win, juego, cadena=False, solo=None):
    """Práctica de reconocimiento con los que ya capturaste: estructura →
    nombre y códigos. Salen más los que fallas, y los que se confunden
    (Gln/Asn, Glu/Asp, Ile/Leu, Ser/Thr) aparecen juntos en las opciones.
    cadena: solo se ve la cadena lateral. solo: limita a esos aminoácidos."""
    claves = [(aa, t) for aa in datos.ORDEN if juego["capturados"].get(aa)
              and (solo is None or aa in solo) for t in (["nombre"] if cadena else RECONOCER)]
    if not claves:
        d.popup(win, tr("Captura primero algún aminoácido."), tr("Práctica de reconocimiento"))
        return
    aciertos = hechas = 0
    import posgame
    for i in range(PREGUNTAS_PRACTICA):
        aa, tipo = random.choices(claves, [progreso.peso(juego, f"{a}:{t}") for a, t in claves])[0]
        p = None
        if juego.get("sec") and solo is None and random.random() < 0.12:
            # la Sec también sale, aunque no cuente en el 20/20
            aa, tipo = "U", "nombre" if cadena else random.choice(RECONOCER)
            p = posgame.pregunta_sec(tipo)
        alto, ancho = win.getmaxyx()
        win.erase()
        d.put(win, 0, 1, tr("PRÁCTICA DE RECONOCIMIENTO · {i}/{total} · aciertos {n} · "
                            "dominados {dom}/20", i=i + 1, total=PREGUNTAS_PRACTICA,
                            n=aciertos, dom=dominados(juego)),
              d.c("titulo", curses.A_BOLD))
        arte = datos.forma(aa)["arte"]
        if cadena:
            arte = _solo_cadena(arte)
            d.put(win, 2, 1, tr("(Cα)"), d.c("tenue"))
            d.estructura(win, 3, 1, arte)
        else:
            d.estructura(win, 2, 1, arte)
        x = d.ancho_estructura(arte) + 4
        if ancho - x < 40:          # no cabe al lado: la pregunta va debajo
            y, x = len(arte) + 3, 1
        else:
            y = 2
        bien = preguntar(win, juego, aa, tipo, y, x, min(64, ancho - x - 1), estructura=True,
                         opciones=True, salir=True, p=p)
        if bien is None:
            break
        aciertos += bien
        hechas += 1
    progreso.guardar(juego)
    if not hechas:
        return
    win.erase()
    d.popup(win, tr("{n}/{total} correctas. Los que fallaste saldrán más seguido, en la "
                    "práctica y en el campo.", n=aciertos, total=hechas),
            tr("Práctica de reconocimiento"), attr=d.c("bien" if aciertos >= 0.8 * hechas else "texto"))


def _practica_elegir(win, juego):
    """Se da el nombre y hay que elegir su estructura entre 4 parecidas."""
    capturados = [aa for aa in datos.ORDEN if juego["capturados"].get(aa)]
    aciertos = hechas = 0
    for i in range(PREGUNTAS_PRACTICA):
        aa = random.choices(capturados, [progreso.peso(juego, f"{c}:estructura") for c in capturados])[0]
        pareja = pares().get(aa, (None, ""))[0]
        cercanos = [x for x in ([pareja] if pareja else []) + list(PARECIDOS[aa]) if x != aa]
        ops = list(dict.fromkeys(cercanos))[:3]
        resto = [x for x in datos.ORDEN if x != aa and x not in ops]
        random.shuffle(resto)
        ops = [aa] + (ops + resto)[:3]
        random.shuffle(ops)
        alto, ancho = win.getmaxyx()
        completas = alto >= max(len(datos.forma(c)["arte"]) for c in ops) + 8
        win.erase()
        d.put(win, 0, 1, tr("ELIGE LA ESTRUCTURA · {i}/{total} · aciertos {n}", i=i + 1,
                            total=PREGUNTAS_PRACTICA, n=aciertos), d.c("titulo", curses.A_BOLD))
        d.put(win, 2, 1, tr("¿Cuál es {nombre}? Pulsa 1-4 · Esc salir", nombre=AA[aa]["nombre"]),
              d.c("texto", curses.A_BOLD))
        if not completas:
            d.put(win, 3, 1, tr("(se ve solo la cadena lateral; el esqueleto es igual en todos)"),
                  d.c("tenue"))
        col = max(18, (ancho - 2) // 4)
        for j, c in enumerate(ops):
            x = 1 + j * col
            arte = datos.forma(c)["arte"] if completas else _solo_cadena(datos.forma(c)["arte"])
            d.put(win, 5, x, f"{j + 1})", d.c("titulo", curses.A_BOLD))
            d.estructura(win, 6, x, arte)
        win.refresh()
        while True:
            k = d.tecla(win)
            if k == d.ESC:
                break
            if isinstance(k, str) and k in "1234":
                break
        if k == d.ESC:
            break
        dijo = ops[int(k) - 1]
        bien = dijo == aa
        progreso.registrar(juego, f"{aa}:estructura", bien)
        if not bien:
            confundir(juego, aa, dijo)
        aciertos += bien
        hechas += 1
        texto = (tr("Correcto: es la {n}).", n=int(k)) if bien else
                 tr("Incorrecto: elegiste {otro}. {nombre} era la {n}).", otro=AA[dijo]["nombre"],
                    nombre=AA[aa]["nombre"], n=ops.index(aa) + 1))
        d.popup(win, texto + " " + AA[aa]["pista"] + _nota_par(aa), tr("Resultado"),
                attr=d.c("bien" if bien else "mal"))
    progreso.guardar(juego)
    if hechas:
        d.popup(win, tr("{n}/{total} correctas.", n=aciertos, total=hechas),
                tr("Elige la estructura"), attr=d.c("bien" if aciertos >= 0.8 * hechas else "texto"))


CONTRARRELOJ = 60


def _contrarreloj(win, juego):
    """60 s de estructura → nombre, sin pausas: cuenta los aciertos."""
    import time
    capturados = [aa for aa in datos.ORDEN if juego["capturados"].get(aa)]
    aciertos = fallos = 0
    fin = time.monotonic() + CONTRARRELOJ
    ultimo = ""
    win.timeout(250)
    try:
        while time.monotonic() < fin:
            aa = random.choices(capturados, [progreso.peso(juego, f"{c}:nombre") for c in capturados])[0]
            p = generar(aa, "nombre", estructura=True, opciones=True)
            eleccion = None
            while eleccion is None and time.monotonic() < fin:
                alto, ancho = win.getmaxyx()
                win.erase()
                quedan = max(0, int(fin - time.monotonic()) + 1)
                d.put(win, 0, 1, tr("CONTRARRELOJ · {s} s · aciertos {n} · fallos {f}", s=quedan,
                                    n=aciertos, f=fallos),
                      d.c("mal" if quedan <= 10 else "titulo", curses.A_BOLD))
                d.put(win, 1, 1, ultimo, d.c("tenue"))
                arte = datos.forma(aa)["arte"]
                d.estructura(win, 3, 1, arte)
                x = d.ancho_estructura(arte) + 5
                y = 3 if ancho - x >= 30 else len(arte) + 4
                x = x if ancho - x >= 30 else 1
                for i, o in enumerate(p["opciones"]):
                    d.put(win, y + i, x, f"{i + 1}) {o}", d.c("texto", curses.A_BOLD))
                d.put(win, y + 5, x, tr("Pulsa el número · Esc salir"), d.c("tenue"))
                win.refresh()
                k = win.getch()
                if k == 27:
                    return
                if 49 <= k <= 48 + len(p["opciones"]):
                    eleccion = p["opciones"][k - 49]
            if eleccion is None:
                break
            bien = eleccion == p["respuesta"]
            progreso.registrar(juego, f"{aa}:nombre", bien)
            if bien:
                aciertos += 1
                ultimo = tr("√ {nombre}", nombre=p["respuesta"])
            else:
                fallos += 1
                confundir(juego, aa, a_codigo(eleccion, "nombre"))
                ultimo = tr("× era {nombre}, no {otro}", nombre=p["respuesta"], otro=eleccion)
    finally:
        win.timeout(-1)
    records = juego.setdefault("records", {})
    nuevo = aciertos > records.get("reloj", 0)
    if nuevo:
        records["reloj"] = aciertos
    progreso.guardar(juego)
    curses.flushinp()
    d.popup(win, tr("{n} aciertos y {f} fallos en {s} s.", n=aciertos, f=fallos, s=CONTRARRELOJ)
            + (" " + tr("¡Nuevo récord!") if nuevo else
               " " + tr("Récord: {r}.", r=records.get("reloj", 0))),
            tr("Contrarreloj"), attr=d.c("bien" if nuevo else "texto"))


def _practica_confusiones(win, juego):
    """Muestra con qué confundes a cada uno y practica justo esos."""
    top = confusiones(juego)[:6]
    lineas = [tr("Cuando era {era}, contestaste {dijo}: {n} {veces}", era=AA[e]["nombre"],
                 dijo=AA[o]["nombre"], n=n, veces=tr("vez") if n == 1 else tr("veces"))
              for e, o, n in top]
    win.erase()
    d.popup(win, "\n".join(lineas) + "\n\n" + tr("Ahora salen justo esos, con su pareja en "
                                                  "las opciones."), tr("Tus confusiones"))
    solo = {c for e, o, _ in top for c in (e, o) if juego["capturados"].get(c)}
    _practica_normal(win, juego, solo=solo)


# ------------------------------------------------- completar la cadena lateral
# cuántas filas del final se tapan y qué grupo es (lo que el jugador elige)
COMPLETAR = {
    "G": (1, "–H (nada más)"), "A": (1, "–CH3"), "S": (1, "–OH"), "C": (1, "–SH"),
    "Y": (2, "–OH (fenol)"), "M": (3, "–S–CH3 (tioéter)"), "N": (3, "–CONH2 (amida)"),
    "Q": (3, "–CONH2 (amida)"), "D": (3, "–COO− (carboxilato)"),
    "E": (3, "–COO− (carboxilato)"), "K": (1, "–NH3+ (amino)"),
    "R": (5, "guanidinio"), "H": (5, "imidazol"), "F": (7, "fenilo (anillo)"),
    "W": (7, "indol (doble anillo)"),
}


def _con_hueco(aa):
    arte = list(datos.forma(aa)["arte"])
    n, _ = COMPLETAR[aa]
    # el hueco va bajo el último enlace que se ve
    ultima = arte[-n - 1]
    sangria = max(0, len(ultima) - len(ultima.lstrip()) - 2)
    return arte[:-n] + [" " * sangria + "[ ? ]"]


def _practica_completar(win, juego):
    """Se da el nombre y se ve la estructura sin el grupo del final: elige cuál falta."""
    capturados = [aa for aa in datos.ORDEN if juego["capturados"].get(aa) and aa in COMPLETAR]
    if not capturados:
        d.popup(win, tr("Captura primero algún aminoácido con un grupo al final de la cadena "
                        "(Ser, Cys, Lys, Asp…)."), tr("Completa la cadena lateral"))
        return
    grupos = sorted({g for _, g in COMPLETAR.values()})
    aciertos = hechas = 0
    for i in range(PREGUNTAS_PRACTICA):
        aa = random.choices(capturados, [progreso.peso(juego, f"{c}:completar") for c in capturados])[0]
        correcta = tr(COMPLETAR[aa][1])  # las etiquetas se traducen al mostrarse
        cercanos = [tr(COMPLETAR[c][1]) for c in PARECIDOS[aa] if c in COMPLETAR]
        ops = _opciones(correcta, [tr(g) for g in grupos], fijos=cercanos)
        win.erase()
        d.put(win, 0, 1, tr("COMPLETA LA CADENA LATERAL · {i}/{total} · aciertos {n}", i=i + 1,
                            total=PREGUNTAS_PRACTICA, n=aciertos), d.c("titulo", curses.A_BOLD))
        arte = _con_hueco(aa)
        d.estructura(win, 2, 1, arte)
        alto, ancho = win.getmaxyx()
        x = d.ancho_estructura(arte) + 5
        y = 2
        if ancho - x < 40:
            x, y = 1, len(arte) + 3
        d.put(win, y, x, tr("¿Qué grupo falta en {nombre}?", nombre=AA[aa]["nombre"]),
              d.c("texto", curses.A_BOLD))
        for j, o in enumerate(ops):
            d.put(win, y + 2 + j, x + 2, f"{j + 1}) {o}", d.c("texto"))
        d.put(win, y + 7, x, tr("Pulsa el número · Esc salir"), d.c("tenue"))
        win.refresh()
        while True:
            k = d.tecla(win)
            if k == d.ESC or (isinstance(k, str) and k in "1234"):
                break
        if k == d.ESC:
            break
        bien = ops[int(k) - 1] == correcta
        progreso.registrar(juego, f"{aa}:completar", bien)
        aciertos += bien
        hechas += 1
        texto = (tr("Correcto.") if bien else tr("Incorrecto. Era: {g}.", g=correcta))
        d.popup(win, texto + " " + tr("{nombre}: grupo R {r}.", nombre=AA[aa]["nombre"],
                                     r=datos.GRUPO_R[aa][0]) + " " + AA[aa]["pista"],
                tr("Resultado"), attr=d.c("bien" if bien else "mal"))
    progreso.guardar(juego)
    if hechas:
        d.popup(win, tr("{n}/{total} correctas.", n=aciertos, total=hechas),
                tr("Completa la cadena lateral"),
                attr=d.c("bien" if aciertos >= 0.8 * hechas else "texto"))


# ------------------------------------------------------- ¿cuál es diferente?
def _practica_diferente(win, juego):
    """4 estructuras: 3 son del mismo grupo de Lehninger y una no."""
    por_grupo = {}
    for c in datos.ORDEN:
        por_grupo.setdefault(AA[c]["grupo"], []).append(c)
    grandes = [g for g, l in por_grupo.items() if len(l) >= 3]
    aciertos = hechas = 0
    for i in range(PREGUNTAS_PRACTICA):
        g = random.choice(grandes)
        mismos = random.sample(por_grupo[g], 3)
        intruso = random.choice([c for c in datos.ORDEN if AA[c]["grupo"] != g])
        ops = mismos + [intruso]
        random.shuffle(ops)
        alto, ancho = win.getmaxyx()
        completas = alto >= max(len(datos.forma(c)["arte"]) for c in ops) + 8
        win.erase()
        d.put(win, 0, 1, tr("¿CUÁL ES DIFERENTE? · {i}/{total} · aciertos {n}", i=i + 1,
                            total=PREGUNTAS_PRACTICA, n=aciertos), d.c("titulo", curses.A_BOLD))
        d.put(win, 2, 1, tr("Tres son del mismo grupo y una no. ¿Cuál? Pulsa 1-4 · Esc salir"),
              d.c("texto", curses.A_BOLD))
        if not completas:
            d.put(win, 3, 1, tr("(se ve solo la cadena lateral; el esqueleto es igual en todos)"),
                  d.c("tenue"))
        col = max(18, (ancho - 2) // 4)
        for j, c in enumerate(ops):
            arte = datos.forma(c)["arte"] if completas else _solo_cadena(datos.forma(c)["arte"])
            d.put(win, 5, 1 + j * col, f"{j + 1})", d.c("titulo", curses.A_BOLD))
            d.estructura(win, 6, 1 + j * col, arte)
        win.refresh()
        while True:
            k = d.tecla(win)
            if k == d.ESC or (isinstance(k, str) and k in "1234"):
                break
        if k == d.ESC:
            break
        bien = ops[int(k) - 1] == intruso
        progreso.registrar(juego, f"{intruso}:grupo", bien)
        aciertos += bien
        hechas += 1
        nombres = ", ".join(AA[c]["nombre"] for c in mismos)
        texto = ((tr("Correcto.") if bien else tr("Incorrecto: era la {n}).", n=ops.index(intruso) + 1))
                 + " " + tr("{nombres}: {grupo}. {intruso}: {otro}.", nombres=nombres,
                            grupo=datos.GRUPOS[g], intruso=AA[intruso]["nombre"],
                            otro=datos.GRUPOS[AA[intruso]["grupo"]]))
        d.popup(win, texto, tr("Resultado"), attr=d.c("bien" if bien else "mal"))
    progreso.guardar(juego)
    if hechas:
        d.popup(win, tr("{n}/{total} correctas.", n=aciertos, total=hechas), tr("¿Cuál es diferente?"),
                attr=d.c("bien" if aciertos >= 0.8 * hechas else "texto"))


# --------------------------------------------- modificaciones covalentes
# ¿Por qué? de cada modificación: (pregunta, correcta, distractores)
POR_QUE = {
    "Hyp": (tr("¿Por qué la falta de vitamina C debilita el colágeno?"),
            tr("Sin ella no se forma la Hyp y la triple hélice pierde estabilidad"),
            [tr("La vitamina C es uno de los aminoácidos del colágeno"),
             tr("Sin ella el ribosoma no puede leer los codones de la Pro"),
             tr("La vitamina C forma los puentes disulfuro entre las fibras")]),
    "Hyl": (tr("¿Para qué sirve el OH nuevo de la hidroxilisina en el colágeno?"),
            tr("Recibe azúcares y forma entrecruzamientos"),
            [tr("Le quita la carga + a la Lys para que se pliegue"),
             tr("Le da un segundo carboxilo que atrapa Ca²+ entre las fibras"),
             tr("Vuelve aromática a la Lys para que se apile con la Pro")]),
    "Kac": (tr("¿Por qué acetilar las Lys de una histona abre la cromatina?"),
            tr("La Lys pierde su + y se une menos al ADN (−)"),
            [tr("El acetilo le da a la Lys una carga − que repele al ADN"),
             tr("El acetilo corta los enlaces fosfodiéster del ADN"),
             tr("La Lys se vuelve aromática y se apila con las bases")]),
    "Kme3": (tr("¿Por qué la trimetil-lisina ya no se puede acetilar?"),
             tr("Su N tiene 4 enlaces y ningún par libre: ya no es nucleófilo"),
             [tr("Al metilarse perdió su carga + y ya no atrae al acetilo"),
              tr("Los tres metilos la vuelven un ácido con carga −"),
              tr("La SAM se queda unida y tapa a la Lys para siempre")]),
    "pS": (tr("¿Por qué Ser, Thr y Tyr son las que más se fosforilan?"),
           tr("Su OH ataca al fosfato del ATP: queda un fosfoéster estable que una fosfatasa quita"),
           [tr("Son las únicas que ya tienen carga − a pH 7"),
            tr("Son las más hidrofóbicas, y el fosfato las vuelve solubles"),
            tr("Tienen un azufre que se une directo al fósforo")]),
    "pT": (tr("¿Qué le pasa a un residuo al fosforilarse a pH 7?"),
           tr("Pasa de neutro a ≈ −2 y cambia con qué se une"),
           [tr("Gana una carga + y se une al ADN"),
            tr("Se vuelve no polar y entra a la membrana"),
            tr("Pierde su cadena lateral y se vuelve Gly")]),
    "pY": (tr("¿Cómo reconoce un dominio SH2 a una fosfotirosina?"),
           tr("Una Arg suya hace puente salino con el fosfato y el anillo entra en un bolsillo"),
           [tr("Forma un puente disulfuro con el OH de la Tyr"),
            tr("La pTyr tiene carga + y atrae al SH2, que es ácido"),
            tr("Le quita el fosfato y se queda unido al ATP")]),
    "Cis": (tr("¿Por qué hay disulfuros en el RE pero casi no en el citosol?"),
            tr("El RE es oxidante; en el citosol el glutatión los reduce"),
            [tr("En el citosol no hay Cys libres"),
             tr("El RE no tiene agua y la reacción no se hidroliza"),
             tr("En el citosol las Cys están todas fosforiladas")]),
    "Gla": (tr("¿Para qué sirve el segundo carboxilato del Gla?"),
            tr("Los dos carboxilatos juntos atrapan un Ca²+"),
            [tr("Le dan carga + para unirse a los fosfolípidos"),
             tr("Forman un puente disulfuro con otro Gla"),
             tr("Lo vuelven hidrofóbico para meterse a la membrana")]),
    "Nglc": (tr("¿Por qué la N-glicosilación necesita la secuencia N-X-S/T?"),
             tr("El OH de la Ser/Thr ayuda a activar al N de la amida de la Asn"),
             [tr("El azúcar se une a la Ser/Thr y no a la Asn"),
              tr("La X tiene que ser una Pro para doblar la cadena"),
              tr("La Ser/Thr le pasa su carga + al azúcar")]),
    "gS": (tr("¿En qué se diferencia la O-glicosilación de la N-glicosilación?"),
           tr("El azúcar va en el O de Ser/Thr, en el Golgi y sin secuencia consenso"),
           [tr("El azúcar va en el N de la Asn, en el RE y con N-X-S/T"),
            tr("El azúcar va en el S de la Cys, en el citosol"),
            tr("Solo ocurre mientras el ribosoma traduce, en el núcleo")]),
    "gT": (tr("¿Por qué las mucinas cubiertas de O-glicanos forman moco?"),
           tr("Los muchos OH de sus azúcares atrapan agua"),
           [tr("Sus azúcares son hidrofóbicos y repelen el agua"),
            tr("Sus azúcares forman puentes disulfuro entre sí"),
            tr("Sus azúcares tienen carga + y se pegan al ADN")]),
    "Cit": (tr("¿Qué pierde la Arg al volverse citrulina?"),
            tr("Su carga +: el guanidinio se vuelve una urea neutra"),
            [tr("Su anillo aromático: se vuelve no polar"),
             tr("Su carga −: el carboxilato se vuelve amida"),
             tr("Su fosfato: la PAD es una fosfatasa")]),
}


def _practica_mods(win, juego):
    """Con la estructura de un residuo modificado: ¿qué modificación es? o ¿de
    qué aminoácido viene? Solo las que ya descubriste."""
    mods = datos.MODIFICACIONES
    vistas = [e for e in juego["evos_vistas"] if e in mods]
    nombres = [m["nombre"] for m in mods.values()]
    aciertos = hechas = 0
    for i in range(PREGUNTAS_PRACTICA):
        e = random.choices(vistas, [progreso.peso(juego, f"{x}:mod") for x in vistas])[0]
        ev = mods[e]
        tirada = random.random()
        explicacion = tr("{nombre} ({tres}), de {base}: {cambio}", nombre=ev["nombre"],
                         tres=ev["tres"], base=AA[ev["base"]]["nombre"], cambio=ev["cambio"])
        if tirada < 0.35 and e in POR_QUE:
            texto, correcta, otras = POR_QUE[e]
            ops = [correcta] + otras
            random.shuffle(ops)
            explicacion = ev["bio"]
        elif tirada < 0.75:
            texto = tr("¿Qué modificación covalente es esta?")
            correcta = ev["nombre"]
            mismas = [m["nombre"] for m in mods.values() if m["base"] == ev["base"]]
            ops = _opciones(correcta, nombres, fijos=mismas)
        else:
            texto = tr("¿De qué aminoácido viene este residuo modificado?")
            correcta = AA[ev["base"]]["nombre"]
            ops = _opciones(correcta, [AA[c]["nombre"] for c in datos.ORDEN],
                            fijos=[AA[c]["nombre"] for c in PARECIDOS[ev["base"]]])
        win.erase()
        d.put(win, 0, 1, tr("MODIFICACIONES · {i}/{total} · aciertos {n}", i=i + 1,
                            total=PREGUNTAS_PRACTICA, n=aciertos), d.c("titulo", curses.A_BOLD))
        arte = datos.forma(e)["arte"]
        d.estructura(win, 2, 1, arte)
        alto, ancho = win.getmaxyx()
        x, y = d.ancho_estructura(arte) + 5, 2
        if ancho - x < 40:
            x, y = 1, len(arte) + 3
        an = max(20, ancho - x - 2)
        for l in d.envolver(texto, an):
            d.put(win, y, x, l, d.c("texto", curses.A_BOLD))
            y += 1
        y += 1
        for j, o in enumerate(ops):
            for n, l in enumerate(d.envolver(f"{j + 1}) {o}", an - 2)):
                d.put(win, y, x + 2 + (3 if n else 0), l, d.c("texto"))
                y += 1
        d.put(win, y + 1, x, tr("Pulsa el número · Esc salir"), d.c("tenue"))
        win.refresh()
        while True:
            k = d.tecla(win)
            if k == d.ESC or (isinstance(k, str) and k in "1234"):
                break
        if k == d.ESC:
            break
        bien = ops[int(k) - 1] == correcta
        progreso.registrar(juego, f"{e}:mod", bien)
        aciertos += bien
        hechas += 1
        d.popup(win, (tr("Correcto.") if bien else tr("Incorrecto. Era: {g}.", g=correcta))
                + " " + explicacion, tr("Resultado"), attr=d.c("bien" if bien else "mal"))
    progreso.guardar(juego)
    if hechas:
        d.popup(win, tr("{n}/{total} correctas.", n=aciertos, total=hechas), tr("Modificaciones"),
                attr=d.c("bien" if aciertos >= 0.8 * hechas else "texto"))
