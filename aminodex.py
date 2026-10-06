"""Aminodex: fichas de los 20 aminoácidos (completas al capturarlos)."""

import curses

import datos
import dibujo as d

AA = datos.AMINOACIDOS


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
    d.put(win, fy, x, "Grupo R  ", d.c("tenue"))
    d.put(win, fy, x + 9, nombre_r, d.c(a["tipos"][0], curses.A_BOLD | curses.A_UNDERLINE))
    d.put(win, fy, x + 10 + len(nombre_r), formula, d.c("titulo"))
    fy += 1
    d.put(win, fy, x + 9, clase, d.c(a["tipos"][0]))
    fy += 2

    filas = [
        ("Grupo", datos.GRUPOS[a["grupo"]]),
        ("Carga pH 7", a["carga"]),
        ("pK1 · pK2", f"{a['pk1']:.2f} (α-COOH) · {a['pk2']:.2f} (α-NH3+)"),
        ("pKR", f"{a['pkr']:.2f}" if a["pkr"] else "— (cadena no ionizable)"),
        ("pI", f"{a['pi']:.2f}  = ({datos.calcular_pi(c)[1][0]:.2f} + "
               f"{datos.calcular_pi(c)[1][1]:.2f}) / 2"),
        ("Hidropatía", None),
        ("Masa", f"{a['masa']:.2f} g/mol"),
        ("Nutrición", a["nutricion"]),
    ]
    filas += [
        ("Codones", " ".join(a["codones"])),
        ("Interacciones", ", ".join(datos.MOVIMIENTOS[m]["nombre"] for m in datos.forma(c)["movs"])),
    ]
    todas = datos.modificaciones_de(c)
    obtenidas = [datos.MODIFICACIONES[e]["nombre"] for e in todas if e in juego["evos_vistas"]]
    faltan = len(todas) - len(obtenidas)
    texto_mod = ", ".join(obtenidas)
    if faltan:
        texto_mod += (" · " if obtenidas else "") + f"{faltan} por descubrir"
    filas.append(("Modificaciones", texto_mod or "—"))

    col = max(len(etq) for etq, _ in filas) + 2      # columna de valores alineada
    for etq, valor in filas:
        if fy >= alto - 2:
            return
        d.put(win, fy, x, etq, d.c("tenue"))
        if etq == "Hidropatía":
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
            break
        d.put(win, fy, x, l, d.c("agua"))
        fy += 1


def ficha_modificacion(win, juego, eid, y, x, ancho):
    ev = datos.MODIFICACIONES[eid]
    base = AA[ev["base"]]
    alto = win.getmaxyx()[0]
    d.put(win, y, x, ev["nombre"], d.c(ev["tipos"][0], curses.A_BOLD))
    d.put(win, y, x + len(ev["nombre"]) + 2, ev["tres"], d.c("texto"))
    d.put(win, y + 1, x, "modificación postraduccional", d.c("tenue"))
    fy = y + 2
    ancho_b = d.etiqueta_tipos(win, fy, x, base["tipos"])
    d.put(win, fy, x + ancho_b + 1, "→", d.c("tenue"))
    d.etiqueta_tipos(win, fy, x + ancho_b + 3, ev["tipos"])
    fy += 2
    req = ev["req"]
    como = [f"nivel {req['nivel']}"]
    if "objeto" in req:
        como.append(f"1 {req['objeto']}")
    if "zona" in req:
        como.append(f"estar en {datos.ZONAS[req['zona']]['nombre']}")
    if req.get("otra_cys"):
        como.append("otra Cys en el equipo")
    propias = [datos.MOVIMIENTOS[m]["nombre"] for m in datos.forma(eid)["movs"]
               if datos.MOVIMIENTOS[m]["tipo"] != datos.NEUTRO]
    filas = [
        ("De", f"{base['nombre']} ({base['tres']})"),
        ("Carga", ev["carga"]),
        ("Cómo", ", ".join(como)),
        ("Interacciones", ", ".join(propias)),
        ("Cambio", ev["cambio"]),
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


def entradas(juego):
    """Lista de la Aminodex: cada aminoácido seguido de las formas modificadas
    que ya conseguiste (las demás no aparecen)."""
    lista = []
    for c in datos.ORDEN:
        lista.append(("aa", c))
        for e in datos.modificaciones_de(c):
            if e in juego["evos_vistas"]:
                lista.append(("evo", e))
    return lista


def mostrar(win, juego):
    lista = entradas(juego)
    sel = 0
    while True:
        alto, ancho = win.getmaxyx()
        win.erase()
        n = sum(1 for c in datos.ORDEN if juego["capturados"].get(c))
        ne = len(juego["evos_vistas"])
        d.put(win, 0, 1, f"AMINODEX  ·  capturados {n}/20  ·  vistos {len(juego['vistos'])}/20  "
                         f"·  modificaciones {ne}/{len(datos.MODIFICACIONES)}",
              d.c("titulo", curses.A_BOLD))
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
            else:
                ev = datos.MODIFICACIONES[cid]
                texto, attr = f"   └ {ev['nombre'][:16]}", d.c(ev["tipos"][0])
            if i == sel:
                attr |= curses.A_REVERSE
            d.put(win, 2 + fila, 1, f"{texto:<21}", attr)

        clase, cid = lista[sel]
        x_ficha = 46 if ancho < 100 else 50
        if clase == "aa":
            if juego["capturados"].get(cid):
                d.estructura(win, 2, 24, datos.forma(cid)["arte"],
                             etiqueta_r=datos.GRUPO_R[cid][0], color_r=AA[cid]["tipos"][0])
                ficha(win, juego, cid, 2, x_ficha, min(ancho - x_ficha - 1, 70))
            elif cid in juego["vistos"]:
                d.estructura(win, 2, 24, datos.forma(cid)["arte"], d.c("tenue"))
                d.put(win, 2, x_ficha, "¿¿??", d.c("texto", curses.A_BOLD))
                for i, l in enumerate(d.envolver(
                        "Estructura observada, aún sin capturar. Aparece en: " +
                        ", ".join(datos.ZONAS[z]["nombre"] for z in datos.zonas_de(cid)),
                        ancho - x_ficha - 2)):
                    d.put(win, 4 + i, x_ficha, l, d.c("tenue"))
            else:
                d.put(win, 8, 30, "Aún no lo has encontrado.", d.c("tenue"))
        else:
            ev = datos.MODIFICACIONES[cid]
            if juego["capturados"].get(ev["base"]):
                d.estructura(win, 2, 24, datos.forma(cid)["arte"],
                             etiqueta_r=ev["nombre"], color_r=ev["tipos"][0])
                ficha_modificacion(win, juego, cid, 2, x_ficha, min(ancho - x_ficha - 1, 70))
            else:
                d.put(win, 8, 24, f"Captura primero a {AA[ev['base']]['nombre'] if ev['base'] in juego['vistos'] else 'su forma base'}.",
                      d.c("tenue"))
        d.put(win, alto - 1, 1, "↑/↓ elegir   ←/→ saltar de aminoácido   M manual   Esc salir",
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
