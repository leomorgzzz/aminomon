"""Aminodex: fichas de los 20 aminoácidos (completas al capturarlos)."""

import curses

import datos
import dibujo as d
import jefes
import preguntas
import progreso
from idioma import tr

AA = datos.AMINOACIDOS
HIDRO = tr("Hidropatía")


def como_modificar(req):
    """Requisitos de una modificación en una lista de textos cortos."""
    como = [tr("nivel {n}", n=req["nivel"])]
    if "objeto" in req:
        como.append(f"1 {tr(req['objeto'])}")
    if "zona" in req:
        como.append(tr("estar en {zona}", zona=datos.ZONAS[req["zona"]]["nombre"]))
    if req.get("otra_cys"):
        como.append(tr("otra Cys en el equipo"))
    return como


def registro(juego, c):
    """Aciertos/fallos al reconocerlo: por nombre, código de 3 y de 1 letra."""
    a = AA[c]
    partes = []
    for tipo, rotulo in zip(preguntas.RECONOCER, (tr("nombre"), a["tres"], c)):
        clave = f"{c}:{tipo}"
        marca = "√" if preguntas.dominado(juego, c, tipo) else "○"
        partes.append(f"{marca} {rotulo} {juego['aciertos'].get(clave, 0)}/"
                      f"{juego['fallos'].get(clave, 0)}")
    texto = "   ".join(partes)
    if preguntas.nivel(juego, c) == 3:
        texto += tr("  (dominado)")
    return texto + tr("  aciertos/fallos")


def ficha(win, juego, c, y, x, ancho):
    a = AA[c]
    alto = win.getmaxyx()[0]
    fy = y
    d.put(win, fy, x, a["nombre"], d.c(a["tipos"][0], curses.A_BOLD))
    d.put(win, fy, x + len(a["nombre"]) + 2, f"{a['tres']} · {c}", d.c("texto"))
    fy += 1
    d.etiqueta_tipos(win, fy, x, a["tipos"])
    fy += 2
    nombre_r, formula, clase = datos.GRUPO_R[c]
    d.put(win, fy, x, tr("Grupo R  "), d.c("tenue"))
    d.put(win, fy, x + 9, nombre_r, d.c(a["tipos"][0], curses.A_BOLD | curses.A_UNDERLINE))
    d.put(win, fy, x + 10 + len(nombre_r), formula, d.c("titulo"))
    fy += 1
    d.put(win, fy, x + 9, clase, d.c(a["tipos"][0]))
    fy += 2

    filas = [
        (tr("Grupo"), datos.GRUPOS[a["grupo"]]),
        (tr("Carga pH 7"), a["carga"]),
        ("pK1 · pK2", f"{a['pk1']:.2f} (α-COOH) · {a['pk2']:.2f} (α-NH3+)"),
        ("pKR", f"{a['pkr']:.2f}" if a["pkr"] else tr("— (cadena no ionizable)")),
        ("pI", f"{a['pi']:.2f}  = ({datos.calcular_pi(c)[1][0]:.2f} + "
               f"{datos.calcular_pi(c)[1][1]:.2f}) / 2"),
        (tr("Fuente pK"), "Lehninger, 25 °C"),
        (HIDRO, None),
        (tr("Masa"), f"{a['masa']:.2f} g/mol"),
        (tr("Nutrición"), a["nutricion"]),
    ]
    filas += [
        (tr("Codones"), " ".join(a["codones"])),
        (tr("Interacciones"), ", ".join(datos.MOVIMIENTOS[m]["nombre"] for m in datos.forma(c)["movs"])),
    ]
    todas = datos.modificaciones_de(c)
    obtenidas = [datos.MODIFICACIONES[e]["nombre"] for e in todas if e in juego["evos_vistas"]]
    faltan = len(todas) - len(obtenidas)
    texto_mod = ", ".join(obtenidas)
    if faltan:
        texto_mod += (" · " if obtenidas else "") + tr("{n} por descubrir", n=faltan)
    filas.append((tr("Modificaciones"), texto_mod or "—"))
    # tu avance va primero para que no se recorte en pantallas bajas
    filas.insert(0, (tr("Reconocer"), registro(juego, c)))
    conf = preguntas.confusiones(juego, c)
    if conf:        # matriz de confusión de este aminoácido
        filas.insert(1, (tr("Lo confundes con"), ", ".join(
            f"{AA[o]['tres']} ×{n}" for _, o, n in conf[:3])))

    col = max(len(etq) for etq, _ in filas) + 2      # columna de valores alineada
    for etq, valor in filas:
        if fy >= alto - 2:
            return
        d.put(win, fy, x, etq, d.c("tenue"))
        if etq == HIDRO:
            kd = a["hidropatia"]
            d.barra(win, fy, x + col, 12, kd + 4.5, 9, d.c("NP" if kd > 0 else "agua"))
            d.put(win, fy, x + col + 13, f"{kd:+.1f}", d.c("texto"))
            fy += 1
            continue
        for l in d.envolver(valor, ancho - col):
            d.put(win, fy, x + col, l, d.c("texto"))
            fy += 1
    fy += 1
    for l in d.envolver(a["pista"], ancho):
        if fy >= alto - 1:
            return
        d.put(win, fy, x, l, d.c("agua"))
        fy += 1
    if c in datos.NOTA_KD:
        fy += 1
        for l in d.envolver(f"{HIDRO}: {datos.NOTA_KD[c]}", ancho):
            if fy >= alto - 1:
                return
            d.put(win, fy, x, l, d.c("tenue"))
            fy += 1


def ficha_modificacion(win, juego, eid, y, x, ancho):
    ev = datos.MODIFICACIONES[eid]
    base = AA[ev["base"]]
    alto = win.getmaxyx()[0]
    d.put(win, y, x, ev["nombre"], d.c(ev["tipos"][0], curses.A_BOLD))
    d.put(win, y, x + len(ev["nombre"]) + 2, ev["tres"], d.c("texto"))
    d.put(win, y + 1, x, tr("residuo modificado dentro de una proteína"), d.c("tenue"))
    fy = y + 2
    ancho_b = d.etiqueta_tipos(win, fy, x, base["tipos"])
    d.put(win, fy, x + ancho_b + 1, "→", d.c("tenue"))
    d.etiqueta_tipos(win, fy, x + ancho_b + 3, ev["tipos"])
    fy += 2
    como = como_modificar(ev["req"])
    propias = [datos.MOVIMIENTOS[m]["nombre"] for m in datos.forma(eid)["movs"]
               if datos.MOVIMIENTOS[m]["tipo"] != datos.NEUTRO]
    filas = [
        (tr("De"), f"{base['nombre']} ({base['tres']})"),
        (tr("Carga"), ev["carga"]),
        (tr("Cómo"), ", ".join(como)),
        (tr("Interacciones"), ", ".join(propias)),
        (tr("Cambio"), ev["cambio"]),
    ]
    if ev.get("matiz"):                 # mismo grupo: ¿más o menos de ese grupo?
        filas.append((tr("En su grupo"), ev["matiz"]))
    col = max(len(etq) for etq, _ in filas) + 2
    for etq, valor in filas:
        for i, l in enumerate(d.envolver(valor, ancho - col)):
            if fy >= alto - 2:
                return
            if i == 0:
                d.put(win, fy, x, etq, d.c("tenue"))
            d.put(win, fy, x + col, l, d.c("texto"))
            fy += 1
    fy += 1
    for l in d.envolver(ev["bio"], ancho):
        if fy >= alto - 1:
            return
        d.put(win, fy, x, l, d.c("agua"))
        fy += 1


def ficha_sec(win, x, ancho, filas):
    alto = win.getmaxyx()[0]
    d.put(win, 2, x, datos.SEC["nombre"], d.c("POL", curses.A_BOLD))
    d.put(win, 2, x + len(datos.SEC["nombre"]) + 2, "Sec · U", d.c("texto"))
    d.put(win, 3, x, tr("fuera de los 20 estándar"), d.c("tenue"))
    fy = 5
    col = max(len(r) for r, _ in filas) + 2
    for rotulo, valor in filas:
        for i, l in enumerate(d.envolver(valor, ancho - col)):
            if fy >= alto - 2:
                return
            if i == 0:
                d.put(win, fy, x, rotulo, d.c("tenue"))
            d.put(win, fy, x + col, l, d.c("texto"))
            fy += 1


def ficha_peptido(win, juego, pid, y, x, ancho):
    pep = datos.PEPTIDOS[pid]
    d.put(win, y, x, pep["nombre"], d.c("titulo", curses.A_BOLD))
    d.put(win, y + 1, x, tr("péptido sintetizado para el René-virus"), d.c("tenue"))
    jefes.dibujar_resumen(win, y + 3, x, ancho, pep)


def entradas(juego, pestana="aa"):
    """Lista de la Aminodex. Pestaña «aa»: cada aminoácido seguido de las formas
    modificadas que ya conseguiste (las demás no aparecen) y, en una sección
    aparte, la Sec. Pestaña «pep» (tras el examen final): el catálogo de
    péptidos."""
    if pestana == "pep":
        return [("pep", p) for p in datos.PEPTIDOS]
    lista = []
    for c in datos.ORDEN:
        lista.append(("aa", c))
        for e in datos.modificaciones_de(c):
            if e in juego["evos_vistas"]:
                lista.append(("evo", e))
    if juego.get("sec") or progreso.aminodex_completa(juego):
        lista += [("sep", None), ("sec", "U")]
    return lista


X_ESTRUCTURA = 24


def _ancho_dibujo(cid):
    """Columnas de la estructura de una entrada con su rótulo de grupo R."""
    if cid in datos.MODIFICACIONES:
        etiqueta = datos.MODIFICACIONES[cid]["nombre"]
    elif cid == "U":
        etiqueta = datos.SEC["grupo_r"][0]
    else:
        etiqueta = datos.GRUPO_R[cid][0]
    return d.ancho_estructura(datos.forma(cid)["arte"], etiqueta)


def columna_ficha(lista, cid, ancho):
    """Columna de la ficha: a la derecha de la estructura más ancha de la
    lista (así no salta al cambiar de entrada); si con eso la ficha queda muy
    angosta, a la derecha de la estructura actual."""
    base = 46 if ancho < 100 else 50
    comun = max(base, X_ESTRUCTURA + max([_ancho_dibujo(c) for clase, c in lista
                                          if clase not in ("pep", "sep")] or [0]) + 3)
    if ancho - comun >= 48:
        return comun
    return max(base, X_ESTRUCTURA + _ancho_dibujo(cid) + 3)


def mostrar(win, juego):
    pestana = "aa"
    lista = entradas(juego, pestana)
    sel = 0
    while True:
        alto, ancho = win.getmaxyx()
        win.erase()
        n = sum(1 for c in datos.ORDEN if juego["capturados"].get(c))
        ne = len(juego["evos_vistas"])
        partes = ["AMINODEX", tr("capturados {n}/20", n=n),
                  tr("dominados {n}/20", n=preguntas.dominados(juego)),
                  tr("vistos {n}/20", n=len(juego["vistos"])),
                  tr("modificaciones {n}/{total}", n=ne, total=len(datos.MODIFICACIONES))]
        if juego.get("doctorado"):
            partes.append(tr("péptidos {n}/{total}", n=len(juego["peptidos"]),
                             total=len(datos.PEPTIDOS)))
        partes.insert(3, tr("repasar hoy {n}", n=len(progreso.para_hoy(juego))))
        cabecera = "  ·  ".join(partes)
        for quitar in (4, 4):               # en 80 columnas no cabe todo: vistos, modificaciones
            if len(cabecera) <= ancho - 2:
                break
            del partes[quitar]
            cabecera = " · ".join(partes)
        d.put(win, 0, 1, cabecera, d.c("titulo", curses.A_BOLD))
        d.put(win, 1, 0, "─" * ancho, d.c("tenue"))
        if juego.get("doctorado"):          # pestañas: los péptidos van aparte
            cx = 2
            for clave, nombre in (("aa", tr("Aminoácidos")), ("pep", tr("Péptidos"))):
                texto = f" {nombre} "
                d.put(win, 1, cx, texto, d.c("titulo", curses.A_BOLD | curses.A_REVERSE)
                      if clave == pestana else d.c("tenue"))
                cx += len(texto) + 1
            d.put(win, 1, cx + 1, tr(" Tab cambia "), d.c("tenue"))
        visibles = alto - 3
        inicio = max(0, min(sel - visibles // 2, len(lista) - visibles))
        for fila, i in enumerate(range(inicio, min(len(lista), inicio + visibles))):
            clase, cid = lista[i]
            if clase == "aa":
                a = AA[cid]
                num = datos.ORDEN.index(cid) + 1
                if juego["capturados"].get(cid):
                    texto, attr = f"{num:2} √ {a['nombre']}", d.c(a["tipos"][0])
                elif cid in juego["vistos"]:
                    texto, attr = f"{num:2} · {tr('¿¿??')}", d.c("tenue")
                else:
                    texto, attr = f"{num:2}   ------", d.c("tenue")
            elif clase == "sep":
                texto, attr = tr("─ fuera de los 20 ─"), d.c("tenue")
            elif clase == "sec":
                if juego.get("sec"):
                    texto, attr = f" U √ {datos.SEC['nombre']}", d.c("POL")
                else:
                    texto, attr = "    ------", d.c("tenue")
            elif clase == "pep":
                num = list(datos.PEPTIDOS).index(cid) + 1
                if cid in juego["peptidos"]:
                    texto, attr = f"P{num:<2}√ {datos.PEPTIDOS[cid]['nombre'][:15]}", d.c("titulo")
                else:
                    texto, attr = f"P{num:<2}  ------", d.c("tenue")
            else:
                ev = datos.MODIFICACIONES[cid]
                texto, attr = f"   └ {ev['nombre'][:16]}", d.c(ev["tipos"][0])
            if i == sel and clase != "sep":
                attr |= curses.A_REVERSE
            d.put(win, 2 + fila, 1, f"{texto:<21}", attr)

        clase, cid = lista[sel]
        x_ficha = columna_ficha(lista, cid, ancho) if clase != "pep" else X_ESTRUCTURA
        if clase == "pep":
            if cid in juego["peptidos"]:
                ficha_peptido(win, juego, cid, 2, x_ficha, ancho - x_ficha - 1)
            else:
                d.put(win, 8, x_ficha, tr("Péptido {n}: aún no lo sintetizas. Pídeselo al "
                                          "René-virus (V).", n=list(datos.PEPTIDOS).index(cid) + 1),
                      d.c("tenue"))
        elif clase == "sec":
            if juego.get("sec"):
                import posgame
                d.estructura(win, 2, X_ESTRUCTURA, posgame.SEC_ARTE,
                             etiqueta_r=datos.SEC["grupo_r"][0], color_r="POL")
                ficha_sec(win, x_ficha, min(ancho - x_ficha - 1, 70), posgame.filas_sec())
            else:
                for i, l in enumerate(d.envolver(
                        tr("Hay un aminoácido fuera de los 20. Habla con el René-virus (V) "
                           "para su evento."), ancho - X_ESTRUCTURA - 2)):
                    d.put(win, 8 + i, X_ESTRUCTURA, l, d.c("tenue"))
        elif clase == "aa":
            if juego["capturados"].get(cid):
                d.estructura(win, 2, X_ESTRUCTURA, datos.forma(cid)["arte"],
                             etiqueta_r=datos.GRUPO_R[cid][0], color_r=AA[cid]["tipos"][0])
                ficha(win, juego, cid, 2, x_ficha, min(ancho - x_ficha - 1, 70))
            elif cid in juego["vistos"]:
                d.estructura(win, 2, X_ESTRUCTURA, datos.forma(cid)["arte"], d.c("tenue"))
                d.put(win, 2, x_ficha, tr("¿¿??"), d.c("texto", curses.A_BOLD))
                for i, l in enumerate(d.envolver(
                        tr("Estructura observada, aún sin capturar. Aparece en: ") +
                        ", ".join(datos.ZONAS[z]["nombre"] for z in datos.zonas_de(cid)),
                        ancho - x_ficha - 2)):
                    d.put(win, 4 + i, x_ficha, l, d.c("tenue"))
            else:
                d.put(win, 8, 30, tr("Aún no lo has encontrado."), d.c("tenue"))
        else:
            ev = datos.MODIFICACIONES[cid]
            if juego["capturados"].get(ev["base"]):
                d.estructura(win, 2, X_ESTRUCTURA, datos.forma(cid)["arte"],
                             etiqueta_r=ev["nombre"], color_r=ev["tipos"][0])
                ficha_modificacion(win, juego, cid, 2, x_ficha, min(ancho - x_ficha - 1, 70))
            else:
                base = AA[ev["base"]]["nombre"] if ev["base"] in juego["vistos"] else tr("su forma base")
                d.put(win, 8, 24, tr("Captura primero a {base}.", base=base),
                      d.c("tenue"))
        d.put(win, alto - 1, 1, tr("↑/↓ elegir   ←/→ saltar de aminoácido   P practicar   L logros   "
                                   "M manual   Esc salir"),
              d.c("tenue"))
        n_lista = len(lista)
        win.refresh()
        k = d.tecla(win)
        if k == d.ESC or d.es(k, "q", "x"):
            return
        if k == "\t" and juego.get("doctorado"):
            pestana = "pep" if pestana == "aa" else "aa"
            lista, sel = entradas(juego, pestana), 0
        elif d.es(k, curses.KEY_DOWN, "j", "s"):
            sel = (sel + 1) % n_lista
            if lista[sel][0] == "sep":
                sel = (sel + 1) % n_lista
        elif d.es(k, curses.KEY_UP, "k", "w"):
            sel = (sel - 1) % n_lista
            if lista[sel][0] == "sep":
                sel = (sel - 1) % n_lista
        elif d.es(k, curses.KEY_RIGHT, "d") and pestana == "aa":
            sel = next((i for i in range(sel + 1, n_lista) if lista[i][0] == "aa"), 0)
        elif d.es(k, curses.KEY_LEFT, "a") and pestana == "aa":
            previos = [i for i in range(sel) if lista[i][0] == "aa"]
            sel = previos[-1] if previos else max(i for i, e in enumerate(lista) if e[0] == "aa")
        elif d.es(k, "p"):
            preguntas.practica(win, juego)
        elif d.es(k, "l"):
            import logros
            logros.mostrar(win, juego)
        elif d.es(k, "m", "?"):
            import manual
            manual.mostrar(win, juego)
