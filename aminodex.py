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
    if a["req"]:
        filas.append(("Requiere", f"{a['req']} mg/kg/día" +
                      (" (combinado)" if a.get("req_nota") else "")))
    if a.get("nota_nutricion"):
        filas.append(("Síntesis", a["nota_nutricion"]))
    filas += [
        ("Destino", a["destino"]),
        ("Codones", " ".join(a["codones"])),
        ("Movimientos", ", ".join(datos.MOVIMIENTOS[m]["nombre"] for m in a["movs"])),
    ]
    evos = [datos.EVOLUCIONES[e]["nombre"] for e in datos.evoluciones_de(c)]
    filas.append(("Evoluciona", ", ".join(evos) if evos else "—"))

    for etq, valor in filas:
        if fy >= alto - 2:
            return
        d.put(win, fy, x, f"{etq:<12}", d.c("tenue"))
        if etq == "Hidropatía":
            kd = a["hidropatia"]
            d.barra(win, fy, x + 12, 12, kd + 4.5, 9, d.c("NP" if kd > 0 else "agua"))
            d.put(win, fy, x + 25, f"{kd:+.1f}", d.c("texto"))
            fy += 1
            continue
        lineas = d.envolver(valor, ancho - 12)
        for l in lineas:
            d.put(win, fy, x + 12, l, d.c("texto"))
            fy += 1
    fy += 1
    for l in d.envolver(a["pista"], ancho):
        if fy >= alto - 1:
            break
        d.put(win, fy, x, l, d.c("agua"))
        fy += 1


def ficha_evolucion(win, juego, eid, y, x, ancho):
    ev = datos.EVOLUCIONES[eid]
    base = AA[ev["base"]]
    alto = win.getmaxyx()[0]
    obtenida = eid in juego["evos_vistas"]
    d.put(win, y, x, ev["nombre"], d.c(ev["tipos"][0], curses.A_BOLD))
    d.put(win, y, x + len(ev["nombre"]) + 2, ev["tres"], d.c("texto"))
    d.put(win, y + 1, x, ("✓ obtenida" if obtenida else "aún no la consigues"),
          d.c("bien" if obtenida else "tenue"))
    fy = y + 2
    d.etiqueta_tipos(win, fy, x, base["tipos"])
    ancho_b = sum(len(datos.TIPOS[t]["nombre"]) + 2 for t in base["tipos"])
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
    mov = datos.MOVIMIENTOS[ev["mov"]]
    filas = [
        ("De", f"{base['nombre']} ({base['tres']})"),
        ("Carga", ev["carga"]),
        ("Cómo", ", ".join(como)),
        ("Movimiento", mov["nombre"]),
        ("Cambio", ev["cambio"]),
    ]
    for etq, valor in filas:
        for i, l in enumerate(d.envolver(valor, ancho - 12)):
            if fy >= alto - 2:
                return
            if i == 0:
                d.put(win, fy, x, f"{etq:<12}", d.c("tenue"))
            d.put(win, fy, x + 12, l, d.c("texto"))
            fy += 1
    fy += 1
    for l in d.envolver(ev["bio"], ancho):
        if fy >= alto - 1:
            return
        d.put(win, fy, x, l, d.c("agua"))
        fy += 1


def entradas():
    """Lista de la Aminodex: cada aminoácido seguido de sus evoluciones."""
    lista = []
    for c in datos.ORDEN:
        lista.append(("aa", c))
        for e in datos.evoluciones_de(c):
            lista.append(("evo", e))
    return lista


def mostrar(win, juego):
    lista = entradas()
    sel = 0
    while True:
        alto, ancho = win.getmaxyx()
        win.erase()
        n = sum(1 for c in datos.ORDEN if juego["capturados"].get(c))
        ne = len(juego["evos_vistas"])
        d.put(win, 0, 1, f"AMINODEX  ·  capturados {n}/20  ·  vistos {len(juego['vistos'])}/20  "
                         f"·  evoluciones {ne}/{len(datos.EVOLUCIONES)}",
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
                ev = datos.EVOLUCIONES[cid]
                if juego["capturados"].get(ev["base"]):
                    marca = "✓" if cid in juego["evos_vistas"] else "·"
                    texto, attr = f"   └{marca}{ev['nombre'][:16]}", d.c(ev["tipos"][0])
                else:
                    texto, attr = "   └ ??", d.c("oscuro")
            if i == sel:
                attr |= curses.A_REVERSE
            d.put(win, 2 + fila, 1, f"{texto:<21}", attr)

        clase, cid = lista[sel]
        x_ficha = 46 if ancho < 100 else 50
        if clase == "aa":
            if juego["capturados"].get(cid):
                d.estructura(win, 2, 24, datos.forma(cid)["arte"], d.c(AA[cid]["tipos"][0]))
                ficha(win, juego, cid, 2, x_ficha, min(ancho - x_ficha - 1, 70))
            elif cid in juego["vistos"]:
                d.estructura(win, 2, 24, datos.forma(cid)["arte"], d.c("tenue"))
                d.put(win, 2, x_ficha, "¿¿??", d.c("texto", curses.A_BOLD))
                for i, l in enumerate(d.envolver(
                        "Ya viste su estructura, pero aún no lo capturas. ¿Puedes "
                        "deducir qué es y de qué grupo? Vive en: " +
                        ", ".join(datos.ZONAS[z]["nombre"] for z in datos.zonas_de(cid)),
                        ancho - x_ficha - 2)):
                    d.put(win, 4 + i, x_ficha, l, d.c("tenue"))
            else:
                d.put(win, 8, 30, "Aún no lo has encontrado.", d.c("tenue"))
        else:
            ev = datos.EVOLUCIONES[cid]
            if juego["capturados"].get(ev["base"]):
                d.estructura(win, 2, 24, datos.forma(cid)["arte"], d.c(ev["tipos"][0]))
                ficha_evolucion(win, juego, cid, 2, x_ficha, min(ancho - x_ficha - 1, 70))
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
