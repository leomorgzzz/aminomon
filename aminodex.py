"""Aminodex: fichas de los 20 aminoácidos (completas al capturarlos)."""

import curses

import datos
import dibujo as d
import jefes
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
    d.put(win, y + 1, x, tr("modificación postraduccional"), d.c("tenue"))
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


def ficha_peptido(win, juego, pid, y, x, ancho):
    pep = datos.PEPTIDOS[pid]
    d.put(win, y, x, pep["nombre"], d.c("titulo", curses.A_BOLD))
    d.put(win, y + 1, x, tr("péptido sintetizado para el René-virus"), d.c("tenue"))
    jefes.dibujar_resumen(win, y + 3, x, ancho, pep)


def entradas(juego):
    """Lista de la Aminodex: cada aminoácido seguido de las formas modificadas
    que ya conseguiste (las demás no aparecen). Tras el examen final, al final
    va el catálogo de péptidos."""
    lista = []
    for c in datos.ORDEN:
        lista.append(("aa", c))
        for e in datos.modificaciones_de(c):
            if e in juego["evos_vistas"]:
                lista.append(("evo", e))
    if juego.get("doctorado"):
        lista += [("pep", p) for p in datos.PEPTIDOS]
    return lista


X_ESTRUCTURA = 24


def _ancho_dibujo(cid):
    """Columnas de la estructura de una entrada con su rótulo de grupo R."""
    if cid in datos.MODIFICACIONES:
        etiqueta = datos.MODIFICACIONES[cid]["nombre"]
    else:
        etiqueta = datos.GRUPO_R[cid][0]
    return d.ancho_estructura(datos.forma(cid)["arte"], etiqueta)


def columna_ficha(lista, cid, ancho):
    """Columna de la ficha: a la derecha de la estructura más ancha de la
    lista (así no salta al cambiar de entrada); si con eso la ficha queda muy
    angosta, a la derecha de la estructura actual."""
    base = 46 if ancho < 100 else 50
    comun = max(base, X_ESTRUCTURA + max(_ancho_dibujo(c) for clase, c in lista
                                         if clase != "pep") + 3)
    if ancho - comun >= 48:
        return comun
    return max(base, X_ESTRUCTURA + _ancho_dibujo(cid) + 3)


def mostrar(win, juego):
    lista = entradas(juego)
    sel = 0
    while True:
        alto, ancho = win.getmaxyx()
        win.erase()
        n = sum(1 for c in datos.ORDEN if juego["capturados"].get(c))
        ne = len(juego["evos_vistas"])
        cabecera = tr("AMINODEX  ·  capturados {n}/20  ·  vistos {vistos}/20  ·  "
                      "modificaciones {ne}/{total}", n=n, vistos=len(juego["vistos"]),
                      ne=ne, total=len(datos.MODIFICACIONES))
        if juego.get("doctorado"):
            cabecera += tr("  ·  péptidos {n}/{total}", n=len(juego["peptidos"]),
                           total=len(datos.PEPTIDOS))
        d.put(win, 0, 1, cabecera, d.c("titulo", curses.A_BOLD))
        d.put(win, 1, 0, "─" * ancho, d.c("tenue"))
        visibles = alto - 3
        inicio = max(0, min(sel - visibles // 2, len(lista) - visibles))
        for fila, i in enumerate(range(inicio, min(len(lista), inicio + visibles))):
            clase, cid = lista[i]
            if clase == "aa":
                a = AA[cid]
                num = datos.ORDEN.index(cid) + 1
                if juego["capturados"].get(cid):
                    texto, attr = f"{num:2} ✓ {a['nombre']}", d.c(a["tipos"][0])
                elif cid in juego["vistos"]:
                    texto, attr = f"{num:2} · ¿¿??", d.c("tenue")
                else:
                    texto, attr = f"{num:2}   ------", d.c("tenue")
            elif clase == "pep":
                num = list(datos.PEPTIDOS).index(cid) + 1
                if cid in juego["peptidos"]:
                    texto, attr = f"P{num:<2}✓ {datos.PEPTIDOS[cid]['nombre'][:15]}", d.c("titulo")
                else:
                    texto, attr = f"P{num:<2}  ------", d.c("tenue")
            else:
                ev = datos.MODIFICACIONES[cid]
                texto, attr = f"   └ {ev['nombre'][:16]}", d.c(ev["tipos"][0])
            if i == sel:
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
        elif clase == "aa":
            if juego["capturados"].get(cid):
                d.estructura(win, 2, X_ESTRUCTURA, datos.forma(cid)["arte"],
                             etiqueta_r=datos.GRUPO_R[cid][0], color_r=AA[cid]["tipos"][0])
                ficha(win, juego, cid, 2, x_ficha, min(ancho - x_ficha - 1, 70))
            elif cid in juego["vistos"]:
                d.estructura(win, 2, X_ESTRUCTURA, datos.forma(cid)["arte"], d.c("tenue"))
                d.put(win, 2, x_ficha, "¿¿??", d.c("texto", curses.A_BOLD))
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
        d.put(win, alto - 1, 1, tr("↑/↓ elegir   ←/→ saltar de aminoácido   M manual   Esc salir"),
              d.c("tenue"))
        win.refresh()
        k = d.tecla(win)
        if k == d.ESC or d.es(k, "q", "x"):
            return
        if d.es(k, curses.KEY_DOWN, "j", "s"):
            sel = (sel + 1) % len(lista)
        elif d.es(k, curses.KEY_UP, "k", "w"):
            sel = (sel - 1) % len(lista)
        elif d.es(k, curses.KEY_RIGHT, "d"):
            sel = next((i for i in range(sel + 1, len(lista)) if lista[i][0] == "aa"), 0)
        elif d.es(k, curses.KEY_LEFT, "a"):
            previos = [i for i in range(sel) if lista[i][0] == "aa"]
            sel = previos[-1] if previos else max(i for i, e in enumerate(lista) if e[0] == "aa")
        elif d.es(k, "m", "?"):
            import manual
            manual.mostrar(win, juego)
