"""Menú de equipo: líder, orden y modificaciones postraduccionales."""

import curses
import unicodedata

import animaciones as anim
import datos
import dibujo as d
import progreso


def clave_nombre(mon):
    """Orden alfabético sin acentos ni prefijos griegos (γ-carboxiglutamato → c)."""
    nombre = datos.forma(mon["id"])["nombre"].lstrip("γ-")
    sin_acentos = unicodedata.normalize("NFD", nombre)
    return "".join(c for c in sin_acentos if not unicodedata.combining(c)).lower()


def ordenar(juego, criterio):
    """Ordena el equipo; el líder (posición 0) se queda primero."""
    lider, resto = juego["equipo"][0], juego["equipo"][1:]
    if criterio == "nombre":
        resto.sort(key=clave_nombre)
    elif criterio == "nivel":
        resto.sort(key=lambda m: (-m["nivel"], clave_nombre(m)))
    elif criterio == "grupo":
        resto.sort(key=lambda m: (datos.ORDEN_TIPOS.index(datos.forma(m["id"])["tipos"][0]),
                                  clave_nombre(m)))
    juego["equipo"] = [lider] + resto


ORDENES = ["nombre", "nivel", "grupo"]


def mostrar(win, juego, zona_actual):
    sel = 0
    while True:
        equipo = juego["equipo"]
        alto, ancho = win.getmaxyx()
        sel = max(0, min(sel, len(equipo) - 1))
        win.erase()
        d.put(win, 0, 1, f"EQUIPO ({len(equipo)})  ·  el primero (★) es el líder del combate",
              d.c("titulo", curses.A_BOLD))
        orden = juego.get("ajustes", {}).get("orden_equipo")
        if orden:
            d.put(win, 0, max(60, ancho - 28), f"orden: {orden}", d.c("tenue"))
        d.put(win, 1, 0, "─" * ancho, d.c("tenue"))
        visibles = alto - 12
        inicio = max(0, min(sel - visibles // 2, len(equipo) - visibles))
        for fila, i in enumerate(range(inicio, min(len(equipo), inicio + visibles))):
            m = equipo[i]
            f = datos.forma(m["id"])
            attr = d.c(f["tipos"][0])
            if i == sel:
                attr |= curses.A_REVERSE
            lider = "★" if i == 0 else " "
            emax = progreso.energia_max(m)
            d.put(win, 2 + fila, 1, f"{lider} {f['nombre'][:20]:<20} Nv{m['nivel']:>2}", attr)
            d.barra(win, 2 + fila, 30, 10, m["energia"], emax, d.c("titulo"))
            d.put(win, 2 + fila, 41, f"{m['energia']:>3}", d.c("tenue"))

        if equipo:
            m = equipo[sel]
            f = datos.forma(m["id"])
            d.estructura(win, 2, 52, f["arte"], d.c(f["tipos"][0]))
            movs = ", ".join(f"{datos.MOVIMIENTOS[x]['nombre']} "
                             f"[{datos.TIPOS.get(datos.MOVIMIENTOS[x]['tipo'], {}).get('corto', 'Neutro')}]"
                             for x in f["movs"])
            filas = [[("Nombre", "tenue"), (f"{f['nombre']} ({f['tres']})", "texto", curses.A_BOLD)],
                     [("Grupo", "tenue"), (datos.nombre_tipos(f["tipos"]), f["tipos"][0])],
                     [("Carga pH 7", "tenue"), f["carga"]],
                     [("Nivel · XP", "tenue"), f"{m['nivel']} · {m['xp']}/{progreso.xp_necesaria(m)}"],
                     [("Interacciones", "tenue"), movs[: ancho - 20]]]
            evos = progreso.modificaciones_posibles(m)
            if evos:
                filas.append([("Modificable a", "tenue"),
                              (", ".join(datos.MODIFICACIONES[e]["nombre"] for e in evos), "agua")])
            y = alto - 4 - len(filas)
            for k, fila in enumerate(d.alinear(filas)):
                d.fila_tabla(win, y + k, 1, fila)
        objs = "  ".join(f"{k}: {v}" for k, v in juego["objetos"].items())
        d.put(win, alto - 3, 1, f"Objetos   {objs}", d.c("titulo"))
        d.put(win, alto - 1, 1, "↑/↓ elegir  Enter hacer líder  O ordenar (A-Z/nivel/grupo)  "
                                "V modificar  Esc salir", d.c("tenue"))
        win.refresh()
        k = d.tecla(win)
        if k == d.ESC or d.es(k, "q", "e"):
            return
        if not equipo:
            continue
        if d.es(k, curses.KEY_DOWN, "j", "s"):
            sel = (sel + 1) % len(equipo)
        elif d.es(k, curses.KEY_UP, "k", "w"):
            sel = (sel - 1) % len(equipo)
        elif k in d.ENTER:
            equipo.insert(0, equipo.pop(sel))
            sel = 0
        elif d.es(k, "v"):
            modificar(win, juego, equipo[sel], zona_actual)
        elif d.es(k, "o"):
            ajustes = juego.setdefault("ajustes", {})
            actual = ajustes.get("orden_equipo")
            siguiente = ORDENES[(ORDENES.index(actual) + 1) % len(ORDENES)] if actual in ORDENES else "nombre"
            ajustes["orden_equipo"] = siguiente
            ordenar(juego, siguiente)
            sel = 0
        elif d.es(k, "m", "?"):
            import manual
            manual.mostrar(win, juego, "modificaciones")


def modificar(win, juego, mon, zona_actual):
    evos = progreso.modificaciones_posibles(mon)
    f = datos.forma(mon["id"])
    if not evos:
        d.popup(win, f"{f['nombre']} no tiene modificaciones disponibles en el juego (o ya está modificada).", "Modificación")
        return
    opciones = []
    for e in evos:
        ok = all(c for _, c in progreso.requisitos(juego, mon, e, zona_actual))
        opciones.append(f"{datos.MODIFICACIONES[e]['nombre']}  {'✓ lista' if ok else ''}")
    sel = d.menu(win, f"¿Qué modificación de {f['nombre']}?", opciones) if len(evos) > 1 else 0
    if sel is None:
        return
    eid = evos[sel]
    ev = datos.MODIFICACIONES[eid]
    reqs = progreso.requisitos(juego, mon, eid, zona_actual)
    if not all(c for _, c in reqs):
        lineas = [f"{'✓' if c else '✗'} {t}" for t, c in reqs]
        d.popup(win, "Requisitos:\n" + "\n".join(lineas) + f"\n\nPista: {ev['pista']}",
                f"{f['nombre']} → {ev['nombre']}")
        return
    progreso.modificar(juego, mon, eid)
    win.erase()
    d.put(win, 0, 1, f"Modificación postraduccional de {f['nombre']}…", d.c("titulo", curses.A_BOLD))
    anim.destello(win, 2, 1, f["arte"], datos.forma(eid)["arte"], f["tipos"][0], ev["tipos"][0])
    d.put(win, 0, 1, " " * 60)
    d.put(win, 0, 1, f"{f['nombre']} → {ev['nombre']}",
          d.c("bien", curses.A_BOLD))
    texto = (f"{ev['cambio']}\n\nGrupo: {datos.nombre_tipos(f['tipos'])} → "
             f"{datos.nombre_tipos(ev['tipos'])}\n"
             "Interacciones: " + ", ".join(datos.MOVIMIENTOS[m]["nombre"] for m in datos.forma(eid)["movs"]
                                          if datos.MOVIMIENTOS[m]["tipo"] != datos.NEUTRO) + "\n\n"
             f"{ev['bio']}")
    for i, l in enumerate(d.envolver(texto, 52)):
        d.put(win, 2 + i, 26, l, d.c("texto"))
    d.put(win, win.getmaxyx()[0] - 1, 1, "[Enter] seguir", d.c("tenue"))
    win.refresh()
    d.tecla(win)
