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


def aplica(aa, tipo):
    a = AA[aa]
    if tipo in ("pka", "calc_pi"):
        return a["pkr"] is not None
    return True


def _opciones(correcta, distractores, n=4):
    distractores = [x for x in dict.fromkeys(distractores) if x != correcta]
    random.shuffle(distractores)
    ops = [correcta] + distractores[: n - 1]
    random.shuffle(ops)
    return ops


def generar(aa, tipo):
    """Devuelve dict(texto, opciones|None, respuesta, explicacion)."""
    a = AA[aa]
    if tipo == "nombre":
        mismos = [x["nombre"] for x in AA.values() if x["grupo"] == a["grupo"]]
        otros = [x["nombre"] for x in AA.values()]
        random.shuffle(otros)
        return dict(
            texto=tr("¿Qué aminoácido es este?"),
            opciones=_opciones(a["nombre"], mismos + otros),
            respuesta=a["nombre"],
            explicacion=tr("Es {nombre} ({tres}, {una}). {pista}", nombre=a["nombre"],
                           tres=a["tres"], una=aa, pista=a["pista"]),
        )
    if tipo == "tres":
        return dict(
            texto=tr("Escribe el código de 3 letras de {nombre}:", nombre=a["nombre"]),
            opciones=None, respuesta=a["tres"],
            explicacion=f"{a['nombre']} = {a['tres']}.",
        )
    if tipo == "una":
        return dict(
            texto=tr("Escribe el código de 1 letra de {nombre} ({tres}):",
                     nombre=a["nombre"], tres=a["tres"]),
            opciones=None, respuesta=aa,
            explicacion=f"{a['tres']} = {aa}. " + _mnemo_una(aa),
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
            explicacion="pKR: Asp 3.65, Glu 4.25, His 6.00, Cys 8.18, "
                        "Tyr 10.07, Lys 10.53, Arg 12.48.",
        )
    if tipo == "pi":
        correcta = f"{a['pi']:.2f}"
        otros = [f"{x['pi']:.2f}" for x in AA.values() if abs(x["pi"] - a["pi"]) > 0.05]
        pi, (p1, p2) = datos.calcular_pi(aa)
        return dict(
            texto=tr("¿Punto isoeléctrico (pI) de {nombre}?", nombre=a["nombre"]),
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
    }
    return tr(trucos.get(aa, "Coincide con la inicial."))


def elegir_tipo(juego, aa):
    """Dificultad progresiva según cuántas veces lo has capturado."""
    n = juego["capturados"].get(aa, 0)
    if n == 0:
        return "nombre"
    if n == 1:
        return "tres"
    if n == 2:
        return "una"
    tipos = [t for t in TIPOS_PROPIEDAD if aplica(aa, t)]
    pesos = [progreso.peso(juego, f"{aa}:{t}") for t in tipos]
    return random.choices(tipos, pesos)[0]


def elegir_aleatoria(juego):
    """Para la Chaperona: aminoácido y tipo ponderados por fallos."""
    claves = [(aa, t) for aa in datos.ORDEN for t in TIPOS_PROPIEDAD + ["tres", "una"]
              if aplica(aa, t)]
    pesos = [progreso.peso(juego, f"{aa}:{t}") for aa, t in claves]
    return random.choices(claves, pesos)[0]


def preguntar(win, juego, aa, tipo, y, x, ancho, alto_min=0):
    """Muestra la pregunta en un área y devuelve True si acierta. alto_min
    estira el recuadro para tapar por completo lo que haya debajo."""
    p = generar(aa, tipo)
    texto = d.envolver(p["texto"], ancho - 4)
    alto = max(alto_min, len(texto) + (len(p["opciones"]) if p["opciones"] else 2) + 4)
    d.limpiar_area(win, y, x, alto, ancho)
    d.caja(win, y, x, alto, ancho, tr("Pregunta"))
    for i, l in enumerate(texto):
        d.put(win, y + 1 + i, x + 2, l, d.c("texto", curses.A_BOLD))
    y1 = y + 1 + len(texto)
    if p["opciones"]:
        for i, o in enumerate(p["opciones"]):
            d.put(win, y1 + i, x + 4, f"{i + 1}) {o}", d.c("texto"))
        d.put(win, y + alto - 2, x + 2, tr("Pulsa el número de tu respuesta"), d.c("tenue"))
        win.refresh()
        while True:
            k = d.tecla(win)
            if isinstance(k, str) and k.isdigit() and 1 <= int(k) <= len(p["opciones"]):
                eleccion = p["opciones"][int(k) - 1]
                break
    else:
        r = d.pedir_texto(win, y1 + 1, x + 4, "> ", 6)
        eleccion = (r or "").strip()
    bien = eleccion.lower() == p["respuesta"].lower()
    progreso.registrar(juego, f"{aa}:{tipo}", bien)
    if bien:
        texto = tr("Correcto. ") + p["explicacion"]
        attr = d.c("bien")
    else:
        texto = tr("Incorrecto. Era: {respuesta}. ", respuesta=p["respuesta"]) + p["explicacion"]
        attr = d.c("mal")
    d.popup(win, texto, tr("Resultado"), ancho=min(70, ancho + 6), attr=attr)
    return bien
