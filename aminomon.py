#!/usr/bin/env python3
"""AMINOMON — atrapa y aprende los 20 aminoácidos en la terminal."""

import locale
import os
import random
import sys


def _asegurar_curses():
    """Python en Windows no trae curses: la primera vez se instala
    windows-curses con pip."""
    try:
        import curses  # noqa: F401
        return
    except ImportError:
        if os.name != "nt":
            raise
    import importlib
    import site
    import subprocess
    print("Instalando windows-curses (solo la primera vez)...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "windows-curses"])
    except (OSError, subprocess.CalledProcessError):
        sys.exit("No se pudo instalar windows-curses. Prueba en una terminal:\n"
                 "    py -m pip install windows-curses")
    site.addsitedir(site.getusersitepackages())
    importlib.invalidate_caches()


def _pantalla_completa():
    """Al abrir el ejecutable con doble clic: en la consola clásica de Windows
    (la del acceso directo) pone pantalla completa y elige la fuente con el
    tamaño del monitor (ver pantalla.py); en Windows Terminal hace Alt+Enter, y
    en macOS manda la secuencia de maximizar. Si la terminal no se deja, la
    pantalla de calibración explica qué teclas usar."""
    if not getattr(sys, "frozen", False) or os.environ.get("AMINOMON_REINICIO"):
        return
    import time
    if sys.platform == "darwin":
        sys.stdout.write("\033[9;1t")
        sys.stdout.flush()
        time.sleep(0.4)
        return
    if os.name != "nt":
        return
    import ctypes
    import msvcrt
    import pantalla
    if not pantalla.ajustar_consola_windows():
        user32 = ctypes.windll.user32
        clase = ctypes.create_unicode_buffer(64)
        for _ in range(20):                 # Windows Terminal tarda un poco en aparecer
            user32.GetClassNameW(user32.GetForegroundWindow(), clase, 64)
            if clase.value == "CASCADIA_HOSTING_WINDOW_CLASS":
                pantalla._alt_enter(user32)
                time.sleep(0.6)
                break
            time.sleep(0.05)
    while msvcrt.kbhit():                   # por si la terminal dejó pasar el Enter
        msvcrt.getwch()


def _con_aviso_de_error(funcion):
    """En el ejecutable, un error no cierra la ventana sin decir nada: se
    muestra y se guarda en ~/aminomon-error.txt."""
    if not getattr(sys, "frozen", False):
        return funcion()
    try:
        return funcion()
    except Exception:
        import traceback
        texto = traceback.format_exc()
        try:
            with open(os.path.expanduser("~/aminomon-error.txt"), "w", encoding="utf-8") as f:
                f.write(texto)
        except OSError:
            pass
        print(texto)
        print("El juego se cerró por un error. Se guardó en ~/aminomon-error.txt")
        input("Pulsa Enter para salir...")


_asegurar_curses()

import curses  # noqa: E402

import actualizar
import aminodex
import animaciones as anim
import combate
import datos
import dibujo as d
import equipo
import idioma
import jefes
import caras
import logros
import posgame
import manual
import mapa
import progreso
import sintesis
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
INSTALAR = None           # instalador descargado: se corre al cerrar el juego


# ----------------------------------------------------------------- pantallas
def esperar_tamano(win):
    while True:
        alto, ancho = win.getmaxyx()
        if alto >= 24 and ancho >= 80:
            return
        win.erase()
        d.put(win, 0, 0, tr("Agranda la terminal a 80×24 o más (ahora {ancho}×{alto}).",
                            ancho=ancho, alto=alto))
        d.put(win, 1, 0, tr("Lo ideal: pantalla completa (F11 o Alt+Enter)."))
        win.refresh()
        d.tecla(win)


def actualizar_juego(win):
    """Opción «Actualizar» de la pantalla de título. Devuelve True si hay que
    cerrar el juego (para correr el instalador o abrir la versión nueva)."""
    global INSTALAR
    d.popup(win, tr("Descargando {version}...", version=actualizar.NUEVA), esperar=False)
    res = actualizar.preparar()
    if res == "pagina":
        d.popup(win, tr("Se abrió la página de descarga en el navegador."))
        return False
    if res is None:
        d.popup(win, tr("No se pudo actualizar. Descarga la versión nueva de: {pagina}",
                        pagina=actualizar.PAGINA))
        return False
    if res == "git":
        d.popup(win, tr("Listo. El juego se va a cerrar; vuelve a abrirlo para usar la "
                        "versión nueva. Tu partida se conserva."))
    else:
        INSTALAR = res
        d.popup(win, tr("El juego se va a cerrar para instalar la versión nueva y se abrirá "
                        "solo al terminar. Tu partida se conserva."))
    return True


def titulo(win):
    hay_partida = progreso.cargar() is not None
    actualizar.esperar()
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
            aviso = tr("Consejo: pon la terminal en pantalla completa (F11 o Alt+Enter). Ahora: {ancho}×{alto}",
                       ancho=ancho, alto=alto)
            d.put(win, alto - 2, (ancho - len(aviso)) // 2, aviso, d.c("agua"))
        d.put(win, alto - 1, 1, f"v{actualizar.version()}", d.c("tenue"))
        opciones = (["continuar"] if hay_partida else []) + ["nueva", "manual", "pantalla", "idioma"]
        if actualizar.NUEVA:
            opciones.append("actualizar")
        opciones.append("salir")
        # la opción de idioma se escribe en el otro idioma para que se entienda
        textos = {"continuar": tr("Continuar"), "nueva": tr("Nueva partida"),
                  "manual": tr("Manual"), "salir": tr("Salir"),
                  "actualizar": tr("Actualizar a {version}", version=actualizar.NUEVA),
                  "pantalla": tr("Tamaño de la pantalla"),
                  "idioma": "English" if idioma.ACTUAL == "es" else "Español"}
        sel = d.menu(win, None, [textos[o] for o in opciones], y=y0 + 10)
        if sel is None:
            return "salir"
        if opciones[sel] == "actualizar":
            if actualizar_juego(win):
                return "salir"
            continue
        if opciones[sel] == "manual":
            manual.mostrar(win, progreso.nuevo_juego(mapa.INICIO))
            continue
        if opciones[sel] == "pantalla":
            import pantalla
            pantalla.calibrar(win, d, tr, forzar=True)
            continue
        if opciones[sel] == "idioma":
            idioma.guardar("en" if idioma.ACTUAL == "es" else "es")
            return "idioma"
        if opciones[sel] == "nueva" and hay_partida:
            if d.menu(win, tr("¿Borrar la partida guardada?"),
                      [tr("No"), tr("Sí, empezar de cero")]) != 1:
                continue
        return opciones[sel]


def bienvenida(win, c):
    """Tarjeta «¡X se unió a tu equipo!» con su estructura y una carita feliz."""
    a = datos.AMINOACIDOS[c]
    arte = datos.forma(c)["arte"]
    etiqueta = datos.GRUPO_R[c][0]
    color = a["tipos"][0]
    alto, ancho = win.getmaxyx()
    ancho_est = d.ancho_estructura(arte, etiqueta)
    cara = caras.carita(c)
    w = min(ancho - 2, max(60, ancho_est + len(cara[0]) + 12))
    h = min(alto - 1, max(len(arte) + 2, len(cara)) + 8)
    y0, x0 = (alto - h) // 2, (ancho - w) // 2
    win.erase()
    d.caja(win, y0, x0, h, w, attr=d.c(color, curses.A_BOLD))
    titulo = tr("¡{nombre} se unió a tu equipo!", nombre=a["nombre"])
    d.put(win, y0 + 1, x0 + (w - len(titulo)) // 2, titulo, d.c("bien", curses.A_BOLD))
    codigos = f"{a['tres']} · {a['una']}"
    d.put(win, y0 + 2, x0 + (w - len(codigos)) // 2, codigos, d.c("titulo"))
    yc = y0 + 4
    xc = x0 + 3
    color_grupo = d.COLOR_GRUPO[a["grupo"]]          # el color del grupo de Lehninger
    for i, l in enumerate(cara):
        d.put(win, yc + max(0, len(arte) - len(cara)) // 2 + i, xc, l,
              d.c(color_grupo, curses.A_BOLD))
    d.estructura(win, yc, xc + len(cara[0]) + 5, arte, etiqueta_r=etiqueta, color_r=color)
    d.put(win, y0 + h - 4, x0 + 3, datos.GRUPOS[a["grupo"]], d.c(color_grupo, curses.A_BOLD))
    d.put(win, y0 + h - 2, x0 + w - 18, tr("[Enter] seguir"), d.c("tenue"))
    win.refresh()
    curses.flushinp()
    while d.tecla(win) not in d.ENTER:
        pass


def intro(win):
    juego = progreso.nuevo_juego(mapa.INICIO)
    d.dialogo(win, [
        tr("Soy el René-virus: no enfermo a nadie, solo estudio proteómica. Como la mayoría de los virus, no traigo ribosomas: mis proteínas las hacen los de la célula con los 20 aminoácidos estándar. (Algunos virus gigantes y fagos traen genes de unas pocas proteínas ribosomales, pero ninguno arma un ribosoma completo.) Tu trabajo: encontrar y caracterizar esos 20."),
        tr("En el juego, cada aminoácido vive donde su química es protagonista: los no polares en la membrana, los básicos junto al ARN y al ADN. En una célula real hay aminoácidos libres en todas partes."),
        tr("Cada aminoácido es de uno de los 5 grupos de Lehninger y cada movimiento usa la química de uno de ellos. La afinidad depende de la interacción real entre los dos grupos (tabla en el manual [M])."),
        tr("Empiezas con Metionina: AUG es el codón de inicio, así que casi toda proteína se empieza a sintetizar con ella."),
    ], tr("René-virus"))
    progreso.capturar(juego, "M", 3)
    bienvenida(win, "M")

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
    bienvenida(win, c)
    d.dialogo(win, [
        tr("Tu equipo inicial: Metionina y {nombre}.\n\n"
           "En las zonas marcadas con símbolos aparecen aminoácidos salvajes. "
           "Deduce su grupo [D], usa movimientos afines y, con afinidad ≥ 50, "
           "lanza un ARNt [T].", nombre=a["nombre"]),
        tr("La mitocondria (☼) restablece a tu equipo y recarga el ATP, que se gasta al fosforilar (Equipo → V). Los jefes (J) piden construir péptidos. Para entrar al núcleo necesitas una NLS: junta 4 Lys (K) en los ribosomas (÷). Los carteles (i) explican cada zona. Yo soy la V del mapa: búscame para pedir consejo."),
        tr("Para atrapar un aminoácido hay que reconocer su estructura. Practica en la Aminodex ([X] y luego [P]): los que fallas saldrán más seguido."),
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
        self.ultimo_salvaje = None   # para no repetir el mismo encuentro seguido

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
            if "final" in j["recompensas"]:
                d.put(w, 0, 9, "♦", d.c("bien", curses.A_BOLD))   # terminaste todo
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
        pie = tr("WASD/flechas mover · M manual · X Aminodex (P practicar) · E equipo · G guardar · Q salir")
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
            base = datos.forma(f["base"])
            if f["evo"] and marcar:
                casillas.append((x, y, f["base"], f["tipos"][0], curses.A_BOLD | curses.A_REVERSE))
            else:
                casillas.append((x, y, f["base"], base["tipos"][0], curses.A_BOLD))
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
            marca = "* " if i == 0 else "  "
            d.put(w, y, x + 1, f"{marca}{f['tres'][:6]:<7}{tr('Nv')}{m['nivel']:<3}", d.c(f["tipos"][0]))
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
        # no son de combate: se gastan al modificar (fosforilar, hidroxilar…)
        d.put(w, y, x + 1, tr("  para modificar: [E] → V"), d.c("tenue"))
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
            d.put(w, y, cx, "♦" if ok else "◊", d.c("bien" if ok else "oscuro"))
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
                                  "Búscalas en los ribosomas (÷).")
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
                ops = [("encargo", tr("Encargo de síntesis")),
                       ("lab", tr("Laboratorio del René-virus (titulación, electroforesis…)")),
                       ("sec", tr("Selenocisteína (ficha)") if j.get("sec")
                        else tr("Selenocisteína (evento)")),
                       ("examen", tr("Repetir el examen final")), ("nada", tr("Nada por ahora"))]
                op = d.menu(self.win, tr("René-virus"), [t for _, t in ops])
                clave = ops[op][0] if op is not None else "nada"
                if clave == "encargo":
                    sintesis.encargo(self.win, j)
                elif clave == "lab":
                    posgame.laboratorio(self.win, j)
                elif clave == "sec":
                    posgame.evento_sec(self.win, j)
                elif clave == "examen":
                    jefes.examen_rene(self.win, j)
                progreso.guardar(j)
            elif progreso.aminodex_completa(j) and not j.get("sec"):
                if d.menu(self.win, tr("¿Ver el evento de la selenocisteína?"),
                          [tr("Sí"), tr("Ahora no")]) == 0:
                    posgame.evento_sec(self.win, j)
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

    def trampa(self):
        """Solo con --trampa (para probar sin volver a jugar todo). Usa su propia
        partida, ~/.aminomon_trampa.json, así que la normal no se toca."""
        j = self.juego
        ops = ["Desbloquear hasta el post-juego (sin péptidos ni laboratorio)",
               "Completar todo (habla con el René-virus para ver el final)",
               "Borrar avisos y regalos (para volver a verlos)",
               "ATP 99 y equipo curado",
               "Ir con el René-virus"]
        op = d.menu(self.win, "Trampa", ops)
        if op in (0, 1):
            desbloquear(j, todo=op == 1)
        if op == 2:
            j["recompensas"] = [r for r in j["recompensas"] if r == "sec_equipo"]
        elif op == 3:
            j["objetos"]["ATP"] = 99
            progreso.curar_equipo(j)
        elif op == 4:
            j["pos"] = list(mapa.INICIO)
            self.zona = mapa.zona(*j["pos"])
            self.rastro = []
        if op is not None:
            progreso.guardar(j)
            self.mensaje = "Trampa aplicada."

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
        if progreso.todo_completo(j) and "final" not in j["recompensas"]:
            j["recompensas"].append("final")
            progreso.guardar(j)
            posgame.final(self.win, j)
        if j.get("sec") and posgame.dar_sec(j):          # partidas de antes
            self.dibujar()
            d.popup(self.win, tr("Una selenocisteína se unió a tu equipo."), tr("René-virus"),
                    attr=d.c("bien"))
        progreso.guardar(j)

    def consejo(self):
        j = self.juego
        partes = []
        faltan = [c for c in datos.ORDEN if not j["capturados"].get(c)]
        if faltan:
            zonas = [z for z, info in datos.ZONAS.items()
                     if any(c in info["aminos"] for c in faltan)]
            nombres = ", ".join(datos.ZONAS[z]["nombre"] for z in zonas)
            partes.append(tr("Aminoácidos por capturar: {n}. Zonas con especies pendientes: {zonas}.",
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
            n, total = sintesis.capitulo(j), len(sintesis.HISTORIA)
            if n < total:
                partes.append(tr("Encargos de síntesis: llevas {n}/{total}. Cada uno es un "
                                 "péptido real que armas en el ribosoma.", n=n, total=total))
            else:
                partes.append(tr("Terminaste mis encargos. En «Síntesis libre» quedan los "
                                 "otros péptidos del catálogo, y puedes repetir mi examen."))
        if not all(m["energia"] > 0 for m in j["equipo"]):
            partes.append(tr("Tu equipo está cansado: ve a la mitocondria (☼)."))
        lista = progreso.pendientes(j)
        hechos = sum(h for _, h in lista)
        partes.append(tr("Para terminar todo ({h}/{n}):", h=hechos, n=len(lista)) + "\n"
                      + "\n".join(f"{'√' if h else '·'} {t}" for t, h in lista))
        d.popup(self.win, "\n\n".join(partes), tr("René-virus"))

    def encuentro(self, zona):
        j = self.juego
        info = datos.ZONAS[zona]
        # salen más los que fallas al reconocerlos y menos los que ya dominas,
        # pero no el mismo dos veces seguidas
        candidatos = [a for a in info["aminos"] if a != self.ultimo_salvaje] or info["aminos"]
        aa = random.choices(candidatos, [progreso.peso_aa(j, a) for a in candidatos])[0]
        self.ultimo_salvaje = aa
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
                self.dibujar()          # sin el aviso de captura detrás
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
            logros.anunciar(self.win, self.juego, self.dibujar)
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
            elif d.es(k, "b"):
                ajustes = self.juego.setdefault("ajustes", {})
                ajustes["sonido"] = not ajustes.get("sonido", False)
                self.mensaje = (tr("Sonido activado: una campana al acertar, dos al fallar.")
                                if ajustes["sonido"] else tr("Sonido desactivado."))
                if ajustes["sonido"]:
                    progreso.sonar(True)
            elif TRAMPA and (k == curses.KEY_F9 or k == "*"):
                self.trampa()
            elif d.es(k, "g"):
                progreso.guardar(self.juego)
                self.mensaje = tr("Partida guardada en ~/.aminomon.json")
            elif d.es(k, "q"):
                progreso.guardar(self.juego)
                return
            elif k == curses.KEY_RESIZE:
                esperar_tamano(self.win)


def main(win):
    d.cursor(0)
    d.init_colores()
    win.keypad(True)
    # sin optimizaciones de insertar/borrar caracteres: con texto acentuado
    # algunas terminales se desfasan y dejan restos de líneas anteriores
    win.idcok(False)
    win.idlok(False)
    if hasattr(curses, "set_escdelay"):
        curses.set_escdelay(25)
    esperar_tamano(win)
    import pantalla
    pantalla.calibrar(win, d, tr)
    if TRAMPA:
        # directo a una partida con todo desbloqueado, junto al René-virus
        juego = progreso.cargar()
        if juego is None:
            juego = progreso.nuevo_juego(mapa.INICIO)
            desbloquear(juego)
            progreso.guardar(juego)
        partida = Partida(win, juego)
        partida.mensaje = "Modo trampa: * o F9 abre el menú de trampas."
        partida.jugar()
        return None
    eleccion = titulo(win)
    if eleccion in ("salir", "idioma"):
        return eleccion
    juego = progreso.cargar() if eleccion == "continuar" else intro(win)
    Partida(win, juego).jugar()


TRAMPA = "--trampa" in sys.argv


def desbloquear(j, todo=False):
    """La trampa: todo lo del juego principal hecho (y con todo=True, también
    el post-juego)."""
    for c in datos.ORDEN:
        if not progreso.capturado(j, c):
            progreso.capturar(j, c, 30)
    for m in datos.MODIFICACIONES:
        if m not in j["evos_vistas"]:
            j["evos_vistas"].append(m)
            j["equipo"].append(progreso.nuevo_mon(m, 30))
    j["vistos"] = list(dict.fromkeys(j["vistos"] + list(datos.ORDEN)))
    j["insignias"] = list(jefes.JEFES)
    j["zonas_visitadas"] = list(datos.ZONAS)
    j["terminado"] = j["doctorado"] = j["sec"] = True
    posgame.dar_sec(j)
    if todo:
        j["peptidos"] = list(datos.PEPTIDOS)
        j.setdefault("records", {})["laboratorio"] = 6

if TRAMPA:
    progreso.ARCHIVO = os.path.expanduser("~/.aminomon_trampa.json")

if __name__ == "__main__":
    if "--update" in sys.argv or "--actualizar" in sys.argv:
        bien, salida = actualizar.git_pull()
        print(salida)
        sys.exit(0 if bien else 1)
    if not os.environ.get("AMINOMON_REINICIO"):
        actualizar.revisar_en_fondo()
    import pantalla
    pantalla.locale_utf8()
    _pantalla_completa()
    resultado = _con_aviso_de_error(lambda: curses.wrapper(main))
    if INSTALAR:
        actualizar.correr_instalador(INSTALAR)
    elif resultado == "idioma":
        # los textos se traducen al importar: se reinicia en el idioma nuevo
        args = [a for a in sys.argv[1:] if a not in ("--es", "--en")]
        programa = [sys.executable] if getattr(sys, "frozen", False) else \
            [sys.executable, os.path.abspath(__file__)]
        os.environ["AMINOMON_REINICIO"] = "1"     # ya está en pantalla completa
        if os.name == "nt":             # en Windows execv no reemplaza el proceso
            import subprocess
            sys.exit(subprocess.call(programa + args))
        os.execv(sys.executable, programa + args)
