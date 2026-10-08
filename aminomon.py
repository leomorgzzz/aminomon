#!/usr/bin/env python3
"""AMINOMON — atrapa y aprende los 20 aminoácidos en la terminal."""

import curses
import locale
import random

import aminodex
import animaciones as anim
import combate
import datos
import dibujo as d
import equipo
import jefes
import manual
import mapa
import progreso

PROB_ENCUENTRO = 0.10
PANEL_W = 34
LOGO = [
    "   _   __  __ ___ _  _  ___  __  __  ___  _  _ ",
    "  /_\\ |  \\/  |_ _| \\| |/ _ \\|  \\/  |/ _ \\| \\| |",
    " / _ \\| |\\/| || || .` | (_) | |\\/| | (_) | .` |",
    "/_/ \\_\\_|  |_|___|_|\\_|\\___/|_|  |_|\\___/|_|\\_|",
]
STARTERS = ["K", "E", "S"]


# ----------------------------------------------------------------- pantallas
def esperar_tamano(win):
    while True:
        alto, ancho = win.getmaxyx()
        if alto >= 24 and ancho >= 80:
            return
        win.erase()
        d.put(win, 0, 0, f"Agranda la terminal a 80×24 o más (ahora {ancho}×{alto}).")
        d.put(win, 1, 0, "Lo ideal: pantalla completa (F11).")
        win.refresh()
        d.tecla(win)


def titulo(win):
    hay_partida = progreso.cargar() is not None
    destacado = random.choice([c for c in datos.ORDEN if c != "G"])
    while True:
        alto, ancho = win.getmaxyx()
        win.erase()
        y0 = max(1, alto // 2 - 9)
        x0 = (ancho - len(LOGO[0])) // 2
        for i, l in enumerate(LOGO):
            # cada fila del logotipo con el color de un grupo de Lehninger
            d.put(win, y0 + i, x0, l, d.c(["NP", "ARO", "POL", "POS"][i], curses.A_BOLD))
        sub = "Atrapa y aprende los 20 aminoácidos"
        d.put(win, y0 + 5, (ancho - len(sub)) // 2, sub, d.c("tenue"))
        muestra = datos.ORDEN
        xm = (ancho - len(muestra) * 3) // 2
        for i, c in enumerate(muestra):
            d.put(win, y0 + 7, xm + i * 3, c, d.c(datos.AMINOACIDOS[c]["tipos"][0], curses.A_BOLD))
        if alto >= 34 and ancho >= 100:
            a = datos.AMINOACIDOS[destacado]
            arte = datos.forma(destacado)["arte"]
            xs = ancho // 2 + 16
            d.put(win, y0 + 10, xs, f"{a['nombre']} · {datos.GRUPO_R[destacado][0]}",
                  d.c(a["tipos"][0], curses.A_BOLD))
            d.estructura(win, y0 + 12, xs + 1, arte, etiqueta_r=datos.GRUPO_R[destacado][2],
                         color_r=a["tipos"][0])
        if ancho < 120 or alto < 36:
            aviso = f"Consejo: pon la terminal en pantalla completa (F11). Ahora: {ancho}×{alto}"
            d.put(win, alto - 2, (ancho - len(aviso)) // 2, aviso, d.c("agua"))
        opciones = (["Continuar"] if hay_partida else []) + ["Nueva partida", "Manual", "Salir"]
        sel = d.menu(win, None, opciones, y=y0 + 10)
        if sel is None:
            return "Salir"
        if opciones[sel] == "Manual":
            manual.mostrar(win, progreso.nuevo_juego(mapa.INICIO))
            continue
        if opciones[sel] == "Nueva partida" and hay_partida:
            if d.menu(win, "¿Borrar la partida guardada?", ["No", "Sí, empezar de cero"]) != 1:
                continue
        return opciones[sel]


def intro(win):
    juego = progreso.nuevo_juego(mapa.INICIO)
    d.dialogo(win, [
        "Soy el Profesor Ribosoma. Traduzco ARN mensajero a proteína y para "
        "eso necesito los 20 aminoácidos estándar. Tu trabajo es encontrarlos "
        "y caracterizarlos.",
        "Cada aminoácido abunda donde su química es favorable: los no polares "
        "en la membrana, los básicos junto al ARN ribosomal y al ADN.",
        "Cada aminoácido pertenece a uno de los 5 grupos de Lehninger y cada "
        "movimiento usa la química de uno de ellos. La afinidad depende de la "
        "interacción real entre los dos grupos; la tabla completa está en el "
        "manual [M].",
        "Empiezas con Metionina: AUG es el codón de inicio, así que toda "
        "proteína comienza con ella.",
    ], "Profesor Ribosoma")
    progreso.capturar(juego, "M", 3)

    while True:
        alto, ancho = win.getmaxyx()
        win.erase()
        col = max(26, min(36, ancho // 3))
        x0 = (ancho - col * 3) // 2
        d.put(win, 0, x0, "Elige un segundo aminoácido (1-3)", d.c("titulo", curses.A_BOLD))
        textos = [
            "Cargado +. Puente salino ×2 contra los ácidos del RE y catión–π "
            "contra los aromáticos.",
            "Cargado −. Puente salino ×2 contra los básicos de los ribosomas y "
            "del núcleo.",
            "Polar sin carga. Puentes de H ×2 contra los polares. Con ATP una "
            "quinasa la fosforila y se vuelve Cargado −.",
        ]
        for i, c in enumerate(STARTERS):
            a = datos.AMINOACIDOS[c]
            x = x0 + i * col
            d.put(win, 2, x, f"{i + 1}) {a['nombre']} ({a['tres']})", d.c(a["tipos"][0], curses.A_BOLD))
            d.etiqueta_tipos(win, 3, x, a["tipos"])
            d.estructura(win, 5, x, datos.forma(c)["arte"], d.c(a["tipos"][0]))
            for j, l in enumerate(d.envolver(textos[i], col - 2)):
                d.put(win, 19 + j, x, l, d.c("tenue"))
        win.refresh()
        k = d.tecla(win)
        if isinstance(k, str) and k in "123":
            c = STARTERS[int(k) - 1]
            a = datos.AMINOACIDOS[c]
            if d.menu(win, f"¿Elegir a {a['nombre']}?", ["Sí", "No"]) == 0:
                break
    progreso.capturar(juego, c, 3)
    d.dialogo(win, [
        f"Tu equipo inicial: Metionina y {a['nombre']}.\n\n"
        "En las zonas marcadas con símbolos aparecen aminoácidos salvajes. "
        "Deduce su grupo [D], usa movimientos afines y, con afinidad ≥ 50, "
        "lanza un ARNt [T].",
        "La mitocondria (◉) restablece a tu equipo y recarga ATP. Los jefes "
        "(J) piden construir péptidos. Para entrar al núcleo necesitas una NLS "
        "rica en Lys (K), que encontrarás en los polirribosomas (∴); la Arg (R) "
        "solo vive dentro del núcleo. Los carteles (i) describen cada "
        "compartimento.",
    ], "Profesor Ribosoma")
    progreso.guardar(juego)
    return juego


# --------------------------------------------------------------------- mapa
class Partida:
    def __init__(self, win, juego):
        self.win, self.juego = win, juego
        self.mensaje = "Explora la célula. [M] abre el manual."
        if not mapa.transitable(*juego["pos"]):
            juego["pos"] = list(mapa.INICIO)
        self.zona = mapa.zona(*juego["pos"])

    # ------------------------------------------------------------ dibujo
    def dimensiones(self):
        alto, ancho = self.win.getmaxyx()
        panel = ancho >= 112
        vw = ancho - (PANEL_W + 1 if panel else 0)
        vh = alto - 3
        return alto, ancho, panel, vh, vw

    def dibujar(self):
        w, j = self.win, self.juego
        w.erase()
        alto, ancho, panel, vh, vw = self.dimensiones()
        info = datos.ZONAS.get(self.zona, {})
        n = sum(1 for v in j["capturados"].values() if v)
        d.put(w, 0, 1, "AMINOMON", d.c("titulo", curses.A_BOLD))
        d.put(w, 0, 11, f"· {info.get('nombre', '')}", d.c(info.get("color", "texto"), curses.A_BOLD))
        if not panel:
            d.put(w, 0, max(40, vw - 42),
                  f"Aminodex {n}/20  Insignias {len(j['insignias'])}/{len(jefes.JEFES)}  "
                  f"ATP {j['objetos']['ATP']}", d.c("tenue"))
        mapa.dibujar(w, 1, 0, vh, vw, j)
        d.put(w, alto - 2, 1, self.mensaje[: ancho - 2], d.c("texto"))
        d.put(w, alto - 1, 1, "WASD/flechas mover · M manual · X aminodex · E equipo · "
                              "G guardar · Q salir", d.c("tenue"))
        if panel:
            self.panel(ancho - PANEL_W, alto)
        w.redrawln(alto - 2, 1)
        w.refresh()

    def panel(self, x, alto):
        w, j = self.win, self.juego
        for yy in range(alto - 2):
            d.put(w, yy, x - 1, "│", d.c("oscuro"))
        y = 0
        info = datos.ZONAS.get(self.zona, {})
        d.put(w, y, x + 1, info.get("nombre", "")[: PANEL_W - 2],
              d.c(info.get("color", "texto"), curses.A_BOLD))
        y += 1
        if info.get("aminos"):
            d.put(w, y, x + 1, "Aquí viven:", d.c("tenue"))
            cx = x + 13
            for c in info["aminos"]:
                if progreso.capturado(j, c):
                    texto, attr = datos.AMINOACIDOS[c]["tres"], d.c(datos.AMINOACIDOS[c]["tipos"][0])
                else:
                    texto, attr = "???", d.c("oscuro")
                if cx + 4 > x + PANEL_W:
                    y += 1
                    cx = x + 13
                d.put(w, y, cx, texto, attr)
                cx += 4
            y += 1
            d.put(w, y, x + 1, f"Niveles {info['niveles'][0]}–{info['niveles'][1]}", d.c("tenue"))
        elif self.zona == "mitocondria":
            d.put(w, y, x + 1, "Zona segura: cura y ATP", d.c("bien"))
        y += 2

        d.put(w, y, x + 1, "EQUIPO", d.c("titulo", curses.A_BOLD))
        y += 1
        max_eq = max(1, (alto - 30) if alto > 34 else 3)
        for i, m in enumerate(j["equipo"][:max_eq]):
            f = datos.forma(m["id"])
            emax = progreso.energia_max(m)
            marca = "★" if i == 0 else " "
            d.put(w, y, x + 1, f"{marca}{f['tres'][:7]:<8}Nv{m['nivel']:<3}", d.c(f["tipos"][0]))
            d.barra(w, y, x + 16, 10, m["energia"], emax, d.c("titulo"))
            d.put(w, y, x + 27, f"{m['energia']:>3}", d.c("tenue"))
            y += 1
        if len(j["equipo"]) > max_eq:
            d.put(w, y, x + 1, f"  … y {len(j['equipo']) - max_eq} más [E]", d.c("tenue"))
            y += 1
        y += 1
        o = j["objetos"]
        d.put(w, y, x + 1, f"ATP {o['ATP']}  Vit C {o['Vitamina C']}  Vit K {o['Vitamina K']}",
              d.c("texto"))
        y += 1
        n = sum(1 for v in j["capturados"].values() if v)
        d.put(w, y, x + 1, f"Aminodex {n}/20", d.c("texto"))
        y += 1
        d.put(w, y, x + 1, "Insignias ", d.c("texto"))
        cx = x + 11
        for z in jefes.JEFES:
            ok = z in j["insignias"]
            d.put(w, y, cx, "◆" if ok else "◇", d.c("bien" if ok else "oscuro"))
            cx += 2
        y += 2

        mh = min(12, alto - y - 3)
        if mh >= 6:
            d.put(w, y, x + 1, "MAPA", d.c("titulo", curses.A_BOLD))
            mapa.minimapa(w, y + 1, x + 1, mh, PANEL_W - 2, j)

    # ---------------------------------------------------------- acciones
    def mover(self, dx, dy):
        j = self.juego
        x, y = j["pos"]
        nx, ny = x + dx, y + dy
        if not mapa.transitable(nx, ny):
            if mapa.tile(nx, ny) == "=":
                self.mensaje = "La envoltura nuclear no deja pasar: entra por un poro (O)."
            return
        if mapa.tile(nx, ny) == "O" and "nucleo" not in j["insignias"]:
            if not jefes.retar(self.win, j, "nucleo"):
                self.mensaje = ("El poro nuclear no te deja pasar sin una NLS (≥ 4 Lys). "
                                "Búscalas en los polirribosomas (∴).")
                return
            progreso.guardar(j)
        j["pos"] = [nx, ny]
        self.mensaje = ""
        zona = mapa.zona(nx, ny)
        if zona != self.zona:
            self.entrar_zona(zona)
        self.zona = zona
        especial = mapa.especial_en(nx, ny)
        if especial:
            self.interactuar(especial)
            return
        t = mapa.tile(nx, ny)
        if t in mapa.HIERBA and random.random() < PROB_ENCUENTRO:
            self.encuentro(mapa.HIERBA[t])

    def entrar_zona(self, zona):
        j = self.juego
        info = datos.ZONAS[zona]
        self.mensaje = f"Entraste a: {info['nombre']}"
        if zona == "mitocondria":
            progreso.curar_equipo(j)
            j["objetos"]["ATP"] = max(j["objetos"]["ATP"], 5)
            self.mensaje = "Mitocondria: equipo restablecido y ATP recargado (5)."
        if zona not in j["zonas_visitadas"]:
            j["zonas_visitadas"].append(zona)
            self.zona = zona
            self.dibujar()
            texto = info["por_que"]
            n = len(info["aminos"])
            if n == 1:
                texto += "\n\nEn esta zona aparece un solo aminoácido."
            elif n:
                texto += f"\n\nEn esta zona aparecen {n} aminoácidos distintos."
            d.popup(self.win, texto, info["nombre"])

    def interactuar(self, especial):
        j = self.juego
        if especial == "ribosoma":
            self.consejo()
            if j.get("terminado"):
                titulo_r = "¿Tomar el examen del Ribosoma Maestro?"
                if j.get("doctorado"):
                    titulo_r = "¿Repetir el examen del Ribosoma Maestro?"
                if d.menu(self.win, titulo_r, ["Sí", "Ahora no"]) == 0:
                    jefes.ribosoma_maestro(self.win, j)
                    progreso.guardar(j)
        elif especial == "chaperona":
            jefes.chaperona(self.win, j)
            progreso.guardar(j)
        elif especial.startswith("jefe_"):
            zona = especial[5:]
            if zona in j["insignias"]:
                self.mensaje = "Ya tienes la insignia de esta zona."
            elif jefes.retar(self.win, j, zona):
                progreso.guardar(j)
        elif especial in ("vit_c", "vit_k"):
            objeto = "Vitamina C" if especial == "vit_c" else "Vitamina K"
            if j["objetos"].get(objeto, 0) < 3:
                j["objetos"][objeto] = j["objetos"].get(objeto, 0) + 1
                self.mensaje = f"Encontraste 1 {objeto}: {datos.OBJETOS[objeto]}"
            else:
                self.mensaje = f"Ya llevas el máximo de {objeto} (3)."
        elif especial.startswith("c_"):
            _, titulo_c, texto = mapa.CARTELES[especial]
            if especial not in j["carteles_leidos"]:
                j["carteles_leidos"].append(especial)
            self.dibujar()
            d.popup(self.win, texto, titulo_c)

    def consejo(self):
        j = self.juego
        faltan = [c for c in datos.ORDEN if not j["capturados"].get(c)]
        if not faltan:
            texto = ("Aminodex completa. Quedan por conseguir las modificaciones "
                     "y el examen de la Chaperona (H).")
        else:
            zonas = [z for z, info in datos.ZONAS.items()
                     if any(c in info["aminos"] for c in faltan)]
            nombres = ", ".join(datos.ZONAS[z]["nombre"] for z in zonas)
            texto = f"Faltan {len(faltan)} aminoácidos. Zonas con especies pendientes: {nombres}."
        pendientes = [jefes.JEFES[z]["reto"] for z in jefes.JEFES if z not in j["insignias"]]
        if pendientes:
            texto += f"\n\nRetos pendientes: {', '.join(pendientes)}."
        if not all(m["energia"] > 0 for m in j["equipo"]):
            texto += "\n\nTu equipo está cansado: ve a la mitocondria (◉)."
        d.popup(self.win, texto, "Profesor Ribosoma")

    def encuentro(self, zona):
        j = self.juego
        info = datos.ZONAS[zona]
        aa = random.choice(info["aminos"])
        nivel = random.randint(*info["niveles"])
        self.dibujar()
        curses.flushinp()
        anim.transicion(self.win)
        curses.flushinp()
        d.popup(self.win, "Un aminoácido salvaje se acerca.", info["nombre"], ancho=44)
        curses.flushinp()
        resultado = combate.combate(self.win, j, aa, nivel, zona)
        if resultado == "capturado":
            if all(j["capturados"].get(c) for c in datos.ORDEN):
                d.popup(self.win, "Capturaste los 20 aminoácidos estándar.",
                        "Aminodex completa",
                        attr=d.c("bien"))
            progreso.guardar(j)
            self.mensaje = "Partida guardada."
        elif resultado == "derrota":
            progreso.curar_equipo(j)
            j["pos"] = list(mapa.CENTRO_MITO)
            self.zona = "mitocondria"
            d.popup(self.win, "Todo tu equipo se desnaturalizó. Vuelves a la "
                              "mitocondria con la energía restablecida.",
                    "Equipo desnaturalizado")
        elif resultado == "huiste":
            self.mensaje = "Escapaste sin problemas."

    def jugar(self):
        while True:
            self.dibujar()
            k = d.tecla(self.win)
            if d.es(k, curses.KEY_UP, "w"):
                self.mover(0, -1)
            elif d.es(k, curses.KEY_DOWN, "s"):
                self.mover(0, 1)
            elif d.es(k, curses.KEY_LEFT, "a"):
                self.mover(-1, 0)
            elif d.es(k, curses.KEY_RIGHT, "d"):
                self.mover(1, 0)
            elif d.es(k, "m", "?"):
                manual.mostrar(self.win, self.juego)
            elif d.es(k, "x"):
                aminodex.mostrar(self.win, self.juego)
            elif d.es(k, "e"):
                equipo.mostrar(self.win, self.juego, self.zona)
            elif d.es(k, "g"):
                progreso.guardar(self.juego)
                self.mensaje = "Partida guardada en ~/.aminomon.json"
            elif d.es(k, "q"):
                progreso.guardar(self.juego)
                return
            elif k == curses.KEY_RESIZE:
                esperar_tamano(self.win)


def main(win):
    curses.curs_set(0)
    d.init_colores()
    win.keypad(True)
    # sin optimizaciones de insertar/borrar caracteres: con texto acentuado
    # algunas terminales se desfasan y dejan restos de líneas anteriores
    win.idcok(False)
    win.idlok(False)
    curses.set_escdelay(25)
    esperar_tamano(win)
    eleccion = titulo(win)
    if eleccion == "Salir":
        return
    juego = progreso.cargar() if eleccion == "Continuar" else intro(win)
    Partida(win, juego).jugar()


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, "")
    curses.wrapper(main)
