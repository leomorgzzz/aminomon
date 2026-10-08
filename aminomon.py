#!/usr/bin/env python3
"""AMINOMON — atrapa y aprende los 20 aminoácidos en la terminal."""

import curses
import locale
import os
import random
import sys

import aminodex
import animaciones as anim
import combate
import datos
import dibujo as d
import equipo
import idioma
import jefes
import manual
import mapa
import progreso
from idioma import tr

PROB_ENCUENTRO = 0.10
PANEL_W = 34
LARGO_CADENA = 12         # residuos del equipo que te siguen por el mapa
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
        d.put(win, 0, 0, tr("Agranda la terminal a 80×24 o más (ahora {ancho}×{alto}).",
                            ancho=ancho, alto=alto))
        d.put(win, 1, 0, tr("Lo ideal: pantalla completa (F11)."))
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
        sub = tr("Atrapa y aprende los 20 aminoácidos")
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
            aviso = tr("Consejo: pon la terminal en pantalla completa (F11). Ahora: {ancho}×{alto}",
                       ancho=ancho, alto=alto)
            d.put(win, alto - 2, (ancho - len(aviso)) // 2, aviso, d.c("agua"))
        opciones = (["continuar"] if hay_partida else []) + ["nueva", "manual", "idioma", "salir"]
        # la opción de idioma se escribe en el otro idioma para que se entienda
        textos = {"continuar": tr("Continuar"), "nueva": tr("Nueva partida"),
                  "manual": tr("Manual"), "salir": tr("Salir"),
                  "idioma": "English" if idioma.ACTUAL == "es" else "Español"}
        sel = d.menu(win, None, [textos[o] for o in opciones], y=y0 + 10)
        if sel is None:
            return "salir"
        if opciones[sel] == "manual":
            manual.mostrar(win, progreso.nuevo_juego(mapa.INICIO))
            continue
        if opciones[sel] == "idioma":
            idioma.guardar("en" if idioma.ACTUAL == "es" else "es")
            return "idioma"
        if opciones[sel] == "nueva" and hay_partida:
            if d.menu(win, tr("¿Borrar la partida guardada?"),
                      [tr("No"), tr("Sí, empezar de cero")]) != 1:
                continue
        return opciones[sel]


def intro(win):
    juego = progreso.nuevo_juego(mapa.INICIO)
    d.dialogo(win, [
        tr("Soy el René-virus, un virus inofensivo: no enfermo a nadie, solo "
           "estudio proteómica. Como todo virus, no tengo ribosomas propios: mis "
           "proteínas las fabrican los ribosomas de la célula con los 20 "
           "aminoácidos estándar. Tu trabajo es encontrarlos y caracterizarlos."),
        tr("Cada aminoácido abunda donde su química es favorable: los no polares "
           "en la membrana, los básicos junto al ARN ribosomal y al ADN."),
        tr("Cada aminoácido pertenece a uno de los 5 grupos de Lehninger y cada "
           "movimiento usa la química de uno de ellos. La afinidad depende de la "
           "interacción real entre los dos grupos; la tabla completa está en el "
           "manual [M]."),
        tr("Empiezas con Metionina: AUG es el codón de inicio, así que toda "
           "proteína comienza con ella."),
    ], tr("René-virus"))
    progreso.capturar(juego, "M", 3)

    while True:
        alto, ancho = win.getmaxyx()
        win.erase()
        col = max(26, min(36, ancho // 3))
        x0 = (ancho - col * 3) // 2
        d.put(win, 0, x0, tr("Elige un segundo aminoácido (1-3)"), d.c("titulo", curses.A_BOLD))
        textos = [
            tr("Cargado +. Puente salino ×2 contra los ácidos del RE y catión–π "
               "contra los aromáticos."),
            tr("Cargado −. Puente salino ×2 contra los básicos de los ribosomas y "
               "del núcleo."),
            tr("Polar sin carga. Puentes de H ×2 contra los polares. Con ATP una "
               "quinasa la fosforila y se vuelve Cargado −."),
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
            if d.menu(win, tr("¿Elegir a {nombre}?", nombre=a["nombre"]), [tr("Sí"), tr("No")]) == 0:
                break
    progreso.capturar(juego, c, 3)
    d.dialogo(win, [
        tr("Tu equipo inicial: Metionina y {nombre}.\n\n"
           "En las zonas marcadas con símbolos aparecen aminoácidos salvajes. "
           "Deduce su grupo [D], usa movimientos afines y, con afinidad ≥ 50, "
           "lanza un ARNt [T].", nombre=a["nombre"]),
        tr("La mitocondria (◉) restablece a tu equipo y recarga ATP. Los jefes "
           "(J) piden construir péptidos. Para entrar al núcleo necesitas una NLS "
           "rica en Lys (K), que encontrarás en los ribosomas (∴); la Arg (R) "
           "solo vive dentro del núcleo. Los carteles (i) describen cada "
           "compartimento. Yo soy la V del mapa: búscame cuando quieras un consejo."),
    ], tr("René-virus"))
    progreso.guardar(juego)
    return juego


# --------------------------------------------------------------------- mapa
class Partida:
    def __init__(self, win, juego):
        self.win, self.juego = win, juego
        self.mensaje = tr("Explora la célula. [M] abre el manual.")
        if not mapa.transitable(*juego["pos"]):
            juego["pos"] = list(mapa.INICIO)
        self.zona = mapa.zona(*juego["pos"])
        self.rastro = []          # casillas por las que pasaste, la más reciente primero

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
        if "ptm" in j["recompensas"]:
            # regalo por completar las modificaciones: el título con los 5 grupos
            for i, letra in enumerate("AMINOMON"):
                d.put(w, 0, 1 + i, letra, d.c(datos.ORDEN_TIPOS[i % 5], curses.A_BOLD))
        else:
            d.put(w, 0, 1, "AMINOMON", d.c("titulo", curses.A_BOLD))
        d.put(w, 0, 11, f"· {info.get('nombre', '')}", d.c(info.get("color", "texto"), curses.A_BOLD))
        if not panel:
            d.put(w, 0, max(40, vw - 42),
                  tr("Aminodex {n}/20  Insignias {i}/{total}  ATP {atp}", n=n,
                     i=len(j["insignias"]), total=len(jefes.JEFES), atp=j["objetos"]["ATP"]),
                  d.c("tenue"))
        mapa.dibujar(w, 1, 0, vh, vw, j, self.cadena())
        d.put(w, alto - 2, 1, self.mensaje[: ancho - 2], d.c("texto"))
        pie = tr("WASD/flechas mover · M manual · X aminodex · E equipo · G guardar · Q salir")
        if "cadena" in j["recompensas"]:
            pie += tr(" · P cadena")
        d.put(w, alto - 1, 1, pie, d.c("tenue"))
        if panel:
            self.panel(ancho - PANEL_W, alto)
        w.redrawln(alto - 2, 1)
        w.refresh()

    def cadena(self):
        """Tu equipo te sigue como un péptido (regalo por la Aminodex completa).
        Con todas las modificaciones, los residuos modificados se marcan."""
        j = self.juego
        if "cadena" not in j["recompensas"] or not j.setdefault("ajustes", {}).get("cadena", True):
            return []
        marcar = "ptm" in j["recompensas"]
        casillas = []
        for (x, y), m in zip(self.rastro, j["equipo"]):
            f = datos.forma(m["id"])
            base = datos.AMINOACIDOS[f["base"]]
            if f["evo"] and marcar:
                attr = d.c(f["tipos"][0], curses.A_BOLD | curses.A_REVERSE)
            else:
                attr = d.c(base["tipos"][0], curses.A_BOLD)
            casillas.append((x, y, f["base"], attr))
        return casillas

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
            d.put(w, y, x + 1, tr("Aquí viven:"), d.c("tenue"))
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
            d.put(w, y, x + 1, tr("Niveles {a}–{b}", a=info["niveles"][0], b=info["niveles"][1]),
                  d.c("tenue"))
        elif self.zona == "mitocondria":
            d.put(w, y, x + 1, tr("Zona segura: cura y ATP"), d.c("bien"))
        y += 2

        d.put(w, y, x + 1, tr("EQUIPO"), d.c("titulo", curses.A_BOLD))
        y += 1
        max_eq = max(1, (alto - 30) if alto > 34 else 3)
        for i, m in enumerate(j["equipo"][:max_eq]):
            f = datos.forma(m["id"])
            emax = progreso.energia_max(m)
            marca = "★" if i == 0 else " "
            d.put(w, y, x + 1, f"{marca}{f['tres'][:7]:<8}{tr('Nv')}{m['nivel']:<3}", d.c(f["tipos"][0]))
            d.barra(w, y, x + 16, 10, m["energia"], emax, d.c("titulo"))
            d.put(w, y, x + 27, f"{m['energia']:>3}", d.c("tenue"))
            y += 1
        if len(j["equipo"]) > max_eq:
            d.put(w, y, x + 1, tr("  … y {n} más [E]", n=len(j["equipo"]) - max_eq), d.c("tenue"))
            y += 1
        y += 1
        o = j["objetos"]
        d.put(w, y, x + 1, tr("ATP {atp}  Vit C {c}  Vit K {k}", atp=o["ATP"], c=o["Vitamina C"],
                              k=o["Vitamina K"]), d.c("texto"))
        y += 1
        n = sum(1 for v in j["capturados"].values() if v)
        d.put(w, y, x + 1, tr("Aminodex {n}/20", n=n), d.c("texto"))
        y += 1
        if j.get("doctorado"):
            d.put(w, y, x + 1, tr("Péptidos {n}/{total}", n=len(j["peptidos"]), total=len(datos.PEPTIDOS)),
                  d.c("texto"))
            y += 1
        etiqueta = tr("Insignias ")
        d.put(w, y, x + 1, etiqueta, d.c("texto"))
        cx = x + 1 + len(etiqueta)
        for z in jefes.JEFES:
            ok = z in j["insignias"]
            d.put(w, y, cx, "◆" if ok else "◇", d.c("bien" if ok else "oscuro"))
            cx += 2
        y += 2

        mh = min(12, alto - y - 3)
        if mh >= 6:
            d.put(w, y, x + 1, tr("MAPA"), d.c("titulo", curses.A_BOLD))
            mapa.minimapa(w, y + 1, x + 1, mh, PANEL_W - 2, j)

    # ---------------------------------------------------------- acciones
    def mover(self, dx, dy):
        j = self.juego
        x, y = j["pos"]
        nx, ny = x + dx, y + dy
        if not mapa.transitable(nx, ny):
            if mapa.tile(nx, ny) == "=":
                self.mensaje = tr("La envoltura nuclear no deja pasar: entra por un poro (O).")
            return
        if mapa.tile(nx, ny) == "O" and "nucleo" not in j["insignias"]:
            if not jefes.retar(self.win, j, "nucleo"):
                self.mensaje = tr("El poro nuclear no te deja pasar sin una NLS (≥ 4 Lys). "
                                  "Búscalas en los ribosomas (∴).")
                return
            progreso.guardar(j)
        self.rastro.insert(0, (x, y))
        del self.rastro[LARGO_CADENA:]
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
        self.mensaje = tr("Entraste a: {zona}", zona=info["nombre"])
        if zona == "mitocondria":
            progreso.curar_equipo(j)
            j["objetos"]["ATP"] = max(j["objetos"]["ATP"], 5)
            self.mensaje = tr("Mitocondria: equipo restablecido y ATP recargado (5).")
        if zona not in j["zonas_visitadas"]:
            j["zonas_visitadas"].append(zona)
            self.zona = zona
            self.dibujar()
            texto = info["por_que"]
            n = len(info["aminos"])
            if n == 1:
                texto += "\n\n" + tr("En esta zona aparece un solo aminoácido.")
            elif n:
                texto += "\n\n" + tr("En esta zona aparecen {n} aminoácidos distintos.", n=n)
            d.popup(self.win, texto, info["nombre"])

    def interactuar(self, especial):
        j = self.juego
        if especial == "rene":
            self.regalos()
            self.consejo()
            if j.get("doctorado"):
                op = d.menu(self.win, tr("René-virus"), [tr("Encargo de síntesis"),
                                                         tr("Repetir el examen final"),
                                                         tr("Nada por ahora")])
                if op == 0:
                    jefes.encargo(self.win, j)
                elif op == 1:
                    jefes.examen_rene(self.win, j)
                progreso.guardar(j)
            elif j.get("terminado"):
                if d.menu(self.win, tr("¿Tomar el examen final del René-virus?"),
                          [tr("Sí"), tr("Ahora no")]) == 0:
                    jefes.examen_rene(self.win, j)
                    progreso.guardar(j)
        elif especial == "chaperona":
            jefes.chaperona(self.win, j)
            progreso.guardar(j)
        elif especial.startswith("jefe_"):
            zona = especial[5:]
            if zona in j["insignias"]:
                self.mensaje = tr("Ya tienes la insignia de esta zona.")
            elif jefes.retar(self.win, j, zona):
                progreso.guardar(j)
        elif especial in ("vit_c", "vit_k"):
            objeto = "Vitamina C" if especial == "vit_c" else "Vitamina K"
            if j["objetos"].get(objeto, 0) < 3:
                j["objetos"][objeto] = j["objetos"].get(objeto, 0) + 1
                self.mensaje = tr("Encontraste 1 {objeto}: {desc}", objeto=tr(objeto),
                                  desc=datos.OBJETOS[objeto])
            else:
                self.mensaje = tr("Ya llevas el máximo de {objeto} (3).", objeto=tr(objeto))
        elif especial.startswith("c_"):
            _, titulo_c, texto = mapa.CARTELES[especial]
            if especial not in j["carteles_leidos"]:
                j["carteles_leidos"].append(especial)
            self.dibujar()
            d.popup(self.win, texto, titulo_c)

    def regalos(self):
        """Regalos del René-virus por completar la Aminodex y las modificaciones."""
        j = self.juego
        if progreso.aminodex_completa(j) and "cadena" not in j["recompensas"]:
            j["recompensas"].append("cadena")
            self.dibujar()
            d.popup(self.win, tr("¡Completaste la Aminodex! Te regalo una cadena "
                                 "naciente: desde ahora tu equipo te sigue por el mapa "
                                 "como un péptido, cada residuo con su código de 1 letra "
                                 "y el color de su grupo. [P] la muestra u oculta."),
                    tr("René-virus"), attr=d.c("bien"))
        if progreso.modificaciones_completas(j) and "ptm" not in j["recompensas"]:
            j["recompensas"].append("ptm")
            self.dibujar()
            d.popup(self.win, tr("¡Conseguiste todas las modificaciones "
                                 "postraduccionales! En tu cadena, los residuos "
                                 "modificados ahora se ven marcados con el color de su "
                                 "nuevo grupo, y el título del mapa se pinta con los 5 "
                                 "grupos de Lehninger."),
                    tr("René-virus"), attr=d.c("bien"))
        progreso.guardar(j)

    def consejo(self):
        j = self.juego
        partes = []
        faltan = [c for c in datos.ORDEN if not j["capturados"].get(c)]
        if faltan:
            zonas = [z for z, info in datos.ZONAS.items()
                     if any(c in info["aminos"] for c in faltan)]
            nombres = ", ".join(datos.ZONAS[z]["nombre"] for z in zonas)
            partes.append(tr("Faltan {n} aminoácidos. Zonas con especies pendientes: {zonas}.",
                             n=len(faltan), zonas=nombres))
        else:
            mods = [ev["nombre"] for e, ev in datos.MODIFICACIONES.items()
                    if e not in j["evos_vistas"]]
            if mods:
                partes.append(tr("Aminodex completa. Te faltan {n} modificaciones: {mods}. Sus "
                                 "requisitos están en el manual [M].", n=len(mods),
                                 mods=", ".join(mods)))
            else:
                partes.append(tr("Aminodex completa, con todas las modificaciones."))
        pendientes = [jefes.JEFES[z]["reto"] for z in jefes.JEFES if z not in j["insignias"]]
        if pendientes:
            partes.append(tr("Retos pendientes: {retos}.", retos=", ".join(pendientes)))
        elif not j.get("terminado"):
            partes.append(tr("Ya tienes todas las insignias: presenta el examen de la "
                             "Chaperona (H)."))
        elif not j.get("doctorado"):
            partes.append(tr("Ya tienes la Maestría de la Chaperona. Solo te falta mi "
                             "examen final."))
        else:
            n, total = len(j["peptidos"]), len(datos.PEPTIDOS)
            if n < total:
                partes.append(tr("Encargos de síntesis: {n}/{total} péptidos del catálogo. Los "
                                 "largos piden varias copias del mismo aminoácido: sigue "
                                 "capturando.", n=n, total=total))
            else:
                partes.append(tr("Catálogo de péptidos completo. Puedes repetir encargos "
                                 "y mi examen para seguir practicando."))
        if not all(m["energia"] > 0 for m in j["equipo"]):
            partes.append(tr("Tu equipo está cansado: ve a la mitocondria (◉)."))
        d.popup(self.win, "\n\n".join(partes), tr("René-virus"))

    def encuentro(self, zona):
        j = self.juego
        info = datos.ZONAS[zona]
        aa = random.choice(info["aminos"])
        nivel = random.randint(*info["niveles"])
        self.dibujar()
        curses.flushinp()
        anim.transicion(self.win)
        curses.flushinp()
        d.popup(self.win, tr("Un aminoácido salvaje se acerca."), info["nombre"], ancho=44)
        curses.flushinp()
        resultado = combate.combate(self.win, j, aa, nivel, zona)
        if resultado == "capturado":
            # se avisa una sola vez: al capturar el último que faltaba
            if progreso.aminodex_completa(j) and "aviso_aminodex" not in j["recompensas"]:
                j["recompensas"].append("aviso_aminodex")
                d.popup(self.win, tr("Capturaste los 20 aminoácidos estándar. Habla con "
                                     "el René-virus (V): tiene algo para ti."),
                        tr("Aminodex completa"),
                        attr=d.c("bien"))
            progreso.guardar(j)
            self.mensaje = tr("Partida guardada.")
        elif resultado == "derrota":
            progreso.curar_equipo(j)
            j["pos"] = list(mapa.CENTRO_MITO)
            self.rastro = []
            self.zona = "mitocondria"
            d.popup(self.win, tr("Todo tu equipo se desnaturalizó. Vuelves a la "
                                 "mitocondria con la energía restablecida."),
                    tr("Equipo desnaturalizado"))
        elif resultado == "huiste":
            self.mensaje = tr("Escapaste sin problemas.")

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
            elif d.es(k, "p") and "cadena" in self.juego["recompensas"]:
                ajustes = self.juego.setdefault("ajustes", {})
                ajustes["cadena"] = not ajustes.get("cadena", True)
                self.mensaje = tr("Cadena visible.") if ajustes["cadena"] else tr("Cadena oculta.")
            elif d.es(k, "g"):
                progreso.guardar(self.juego)
                self.mensaje = tr("Partida guardada en ~/.aminomon.json")
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
    if eleccion in ("salir", "idioma"):
        return eleccion
    juego = progreso.cargar() if eleccion == "continuar" else intro(win)
    Partida(win, juego).jugar()


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, "")
    if curses.wrapper(main) == "idioma":
        # los textos se traducen al importar: se reinicia en el idioma nuevo
        args = [a for a in sys.argv[1:] if a not in ("--es", "--en")]
        os.execv(sys.executable, [sys.executable, os.path.abspath(__file__)] + args)
