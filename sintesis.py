"""Encargos de síntesis del René-virus (post-juego): una historia de 6
péptidos que se arman en un ribosoma, codón por codón y contra el tiempo.

En cada codón que llega al sitio A se elige el ARNt cuyo anticodón se aparea
con él (A–U, G–C). Si se falla no se dice la respuesta: al final solo se
marcan los codones que salieron mal y se repite con otros codones."""

import curses
import random
import time

import datos
import dibujo as d
import jefes
import progreso
from idioma import tr

AA = datos.AMINOACIDOS
CODIGO = jefes.CODIGO
STOP = jefes.STOP
PAR = {"A": "U", "U": "A", "G": "C", "C": "G"}
PARO = "*"

# (péptido, segundos por codón, ¿se ven los anticodones?, pedido, al terminar)
HISTORIA = [
    ("rgd", 20, True,
     tr("Mis células de cultivo no se pegan a la placa y flotan. Las integrinas de su "
        "membrana se agarran a un motivo de 3 aminoácidos: RGD. Si cubro la placa con "
        "ese péptido, se pegan. Empecemos con algo corto."),
     tr("Las células ya se pegan. Fácil, ¿no? El siguiente es más largo.")),
    ("metenc", 16, True,
     tr("Me pegué en la membrana con la mesa del laboratorio. Tu cerebro tiene sus "
        "propios analgésicos: las encefalinas. Hazme una Met-encefalina (5 aminoácidos)."),
     tr("Ya no me duele. La morfina funciona porque imita a este péptido.")),
    ("nls", 15, False,
     tr("Quiero meter una proteína al núcleo, pero el poro nuclear no deja pasar a "
        "cualquiera. Necesito su contraseña: una NLS, un parche de Lys y Arg. Desde aquí "
        "ya no te enseño los anticodones: elige por el aminoácido. Si no te sabes un "
        "codón, búscalo en la Chuleta del manual (M) antes de empezar."),
     tr("Mi proteína ya entra al núcleo. Las importinas reconocieron la NLS.")),
    ("ang2", 13, False,
     tr("Del susto se me bajó la presión. La angiotensina II contrae los vasos y la "
        "sube. Son 8 aminoácidos y el ribosoma ya va más rápido."),
     tr("Presión normal otra vez. Por cierto: los IECA bajan la presión justo porque "
        "impiden que se forme la angiotensina II.")),
    ("oxi", 12, False,
     tr("Mis ratones de laboratorio no se llevan bien. La oxitocina ayuda al vínculo "
        "social. Tiene 2 Cys: después de sintetizarla, las Cys 1 y 6 se unen con un "
        "puente disulfuro y cierran un anillo."),
     tr("Los ratones ya hasta se acurrucan. El disulfuro se formó solo al oxidarse las "
        "dos Cys.")),
    ("tat", 10, False,
     tr("El último. Quiero meter fármacos a las células, y un virus como yo sabe cómo: "
        "el péptido Tat del VIH-1 cruza membranas por su montón de Arg y Lys. Son 11 "
        "aminoácidos y el ribosoma va a toda velocidad."),
     tr("¡Lo lograste! Con este péptido pego fármacos y los meto a las células. Ya "
        "lees ARNm como un ribosoma.")),
]

HISTORIA_IDS = [h[0] for h in HISTORIA]
LIBRES = [p for p in datos.PEPTIDOS if p not in HISTORIA_IDS]   # se abren al terminar
LIBRE_SEG = 12
SEP = 8                 # columnas entre codones en el dibujo del ARNm


def _comp(cod):
    return "".join(PAR[b] for b in cod)


def _arnt(cod):
    """El ARNt que se aparea con cod: (aminoácido, anticodón escrito 3'→5')."""
    return CODIGO[cod], _comp(cod)


def opciones_arnt(cod, n=4):
    """n ARNt distintos para el codón cod, con la respuesta si no es de paro.
    Incluye las trampas típicas: el anticodón con las mismas letras que el
    codón y el que falla en una sola base."""
    correcta = CODIGO[cod]
    ops = []
    usados = set()
    if correcta != PARO:
        ops.append(_arnt(cod))
        usados.add(correcta)
    candidatos = [_comp(cod)]                   # anticodón = mismas letras
    for i in range(3):
        for b in "ACGU":
            if b != cod[i]:
                candidatos.append(cod[:i] + b + cod[i + 1:])
    random.shuffle(candidatos[1:])
    for otro in candidatos + [random.choice(AA[c]["codones"]) for c in random.sample(datos.ORDEN, 20)]:
        aa = CODIGO[otro]
        if len(ops) >= n:
            break
        if aa != PARO and aa not in usados:
            ops.append(_arnt(otro))
            usados.add(aa)
    random.shuffle(ops)
    return ops


def _arn(seq):
    """AUG + el péptido + un codón de paro, con codones al azar."""
    return ["AUG"] + [random.choice(AA[c]["codones"]) for c in seq] + [random.choice(STOP)]


# ------------------------------------------------------------- el ribosoma
def _dibujar(win, titulo, codones, i, cadena, antis, malos, ops, ver_anti, quedan, total_seg,
             aviso, entrando=None):
    alto, ancho = win.getmaxyx()
    win.erase()
    d.put(win, 0, 1, titulo, d.c("titulo", curses.A_BOLD))
    # la cadena que va creciendo, del extremo N al C
    d.put(win, 2, 2, tr("Cadena (N → C):"), d.c("tenue"))
    x = 2
    for k, c in enumerate(cadena):
        texto = AA[c]["tres"] if c in AA else "???"
        if x + len(texto) + 1 >= ancho:
            break
        d.put(win, 3, x, texto, d.c("mal" if k - 1 in malos else "bien", curses.A_BOLD))
        x += len(texto)
        if k < len(cadena) - 1:
            d.put(win, 3, x, "─", d.c("tenue"))
            x += 1
    # el ribosoma: en P el último ARNt (con la cadena), en A el que entra
    x_p = max(6, min(ancho // 2 - 10, 34))
    y_r = 5
    d.caja(win, y_r, x_p - 5, 7, 22, tr("ribosoma"), d.c("tenue"))
    d.put(win, y_r + 1, x_p + 1, "P", d.c("titulo", curses.A_BOLD))
    d.put(win, y_r + 1, x_p + 1 + SEP, "A", d.c("titulo", curses.A_BOLD))
    ultimo = cadena[-1]
    d.put(win, y_r + 2, x_p - 1, f"[{AA[ultimo]['tres'] if ultimo in AA else '???'}]", d.c("texto"))
    d.put(win, y_r + 3, x_p - 2, f"3'{antis[-1]}5'", d.c("tenue"))
    if entrando:
        aa, anti = entrando
        d.put(win, y_r + 2, x_p - 1 + SEP, f"[{AA[aa]['tres']}]", d.c("titulo", curses.A_BOLD))
        d.put(win, y_r + 3, x_p - 2 + SEP, f"3'{anti}5'", d.c("titulo"))
    else:
        d.put(win, y_r + 2, x_p - 1 + SEP, "[ ? ]", d.c("titulo", curses.A_BOLD))
        d.put(win, y_r + 3, x_p - 2 + SEP, "3'···5'", d.c("tenue"))
    # el ARNm: el codón del sitio P queda siempre en x_p
    y_m = y_r + 5
    d.put(win, y_m, x_p - 5, " ", d.c("tenue"))          # el ARNm pasa por dentro
    d.put(win, y_m, x_p + 16, " ", d.c("tenue"))
    d.put(win, y_m, 0, "5'", d.c("tenue"))
    d.put(win, y_m, ancho - 3, "3'", d.c("tenue"))
    for k, cod in enumerate(codones):
        xc = x_p + (k - i + 1) * SEP
        if xc < 3 or xc + 3 >= ancho - 4:
            continue
        if k == i:
            attr = d.c("titulo", curses.A_BOLD | curses.A_REVERSE)
        elif k < i:
            attr = d.c("mal" if k - 1 in malos else "tenue")
        else:
            attr = d.c("texto")
        d.put(win, y_m, xc, cod, attr)
    # el tiempo
    y = y_r + 8
    barra = min(40, ancho - 22)
    d.put(win, y, 2, tr("Tiempo"), d.c("tenue"))
    d.barra(win, y, 10, barra, quedan, total_seg, d.c("mal" if quedan <= total_seg / 3 else "bien"))
    d.put(win, y, 11 + barra, f"{max(0, quedan):4.1f} s", d.c("tenue"))
    # los ARNt para elegir
    y += 2
    d.caja(win, y, 1, len(ops) + 4, min(ancho - 2, 64),
           tr("Elige el ARNt para el codón {cod}", cod=codones[i]), d.c("titulo", curses.A_BOLD),
           resaltar=True)
    for k, (aa, anti) in enumerate(ops):
        if ver_anti:
            texto = f"{k + 1}) {AA[aa]['tres']}  " + tr("anticodón") + f" 3'-{anti}-5'"
        else:
            texto = f"{k + 1}) {AA[aa]['tres']}  {AA[aa]['nombre']}"
        d.put(win, y + 1 + k, 3, texto, d.c("texto", curses.A_BOLD))
    d.put(win, y + 1 + len(ops), 3, f"{len(ops) + 1}) " + tr("Factor de liberación (codón de paro)"),
          d.c("texto", curses.A_BOLD))
    d.put(win, y + 2 + len(ops), 3, tr("Pulsa 1-{n} · Esc pausa", n=len(ops) + 1), d.c("tenue"))
    if aviso:                       # debajo de la cadena: así cabe también en 80×24
        d.put(win, 4, 2, aviso[0], d.c(aviso[1], curses.A_BOLD))
    win.refresh()


def ribosoma(win, juego, titulo, seq, segundos, ver_anti):
    """Una síntesis. Devuelve (bien, codones, posiciones mal, último codón leído)
    o None si se sale."""
    codones = _arn(seq)
    cadena = ["M"]          # el ARNt iniciador ya trae la Met al sitio P
    antis = ["UAC"]
    malos = set()
    aviso = None
    i = 1
    win.timeout(100)
    try:
        while i < len(codones):
            cod = codones[i]
            ops = opciones_arnt(cod)
            fin = time.monotonic() + segundos
            eleccion = None
            while eleccion is None:
                quedan = fin - time.monotonic()
                if quedan <= 0:
                    eleccion = "tiempo"
                    break
                _dibujar(win, titulo, codones, i, cadena, antis, malos, ops, ver_anti, quedan, segundos, aviso)
                k = win.getch()
                if k == 27:
                    pausa = time.monotonic()
                    win.timeout(-1)
                    op = d.menu(win, tr("Pausa"), [tr("Seguir"), tr("Salir del encargo")])
                    win.timeout(100)
                    if op == 1:
                        return None
                    fin += time.monotonic() - pausa
                elif 49 <= k <= 49 + len(ops):
                    eleccion = k - 49
            paro = CODIGO[cod] == PARO
            if eleccion == "tiempo":
                malos.add(i - 1)
                cadena.append("?")
                antis.append("···")
                aviso = (tr("Se acabó el tiempo en {cod}: cuenta como error.", cod=cod), "mal")
                if paro:
                    break
            elif eleccion == len(ops):              # factor de liberación
                if paro:
                    break
                malos.add(i - 1)
                aviso = (tr("Liberaste la cadena antes de tiempo: {cod} no es de paro.", cod=cod), "mal")
                break
            else:
                aa = ops[eleccion][0]
                _dibujar(win, titulo, codones, i, cadena, antis, malos, ops, ver_anti,
                         fin - time.monotonic(), segundos, aviso, entrando=ops[eleccion])
                time.sleep(0.35)
                cadena.append(aa)
                antis.append(ops[eleccion][1])
                if paro or aa != CODIGO[cod]:
                    malos.add(i - 1)
                    aviso = (tr("Ese ARNt no se aparea con {cod}.", cod=cod), "mal")
                    if paro:
                        aviso = (tr("{cod} es de paro: ningún ARNt lo reconoce.", cod=cod), "mal")
                        break
                else:
                    aviso = (tr("√ {aa} unida a la cadena.", aa=AA[aa]["tres"]), "bien")
            i += 1
    finally:
        win.timeout(-1)
    curses.flushinp()
    bien = not malos and i == len(codones) - 1
    progreso.registrar(juego, "encargo:ribosoma", bien)
    return bien, codones, malos, i


def _revision(win, codones, malos, leido, ver_anti):
    """Qué codones salieron mal, sin decir la respuesta."""
    marcas = "  ".join(f"{cod}{'×' if k - 1 in malos else '√' if k <= leido else '·'}"
                       for k, cod in enumerate(codones) if k > 0)
    texto = (tr("La proteína salió mal. Revisa los codones con × (· = no se llegó a leer):")
             + "\n\n" + marcas + "\n\n")
    if ver_anti:
        texto += tr("Recuerda: el anticodón se aparea base por base, A con U y G con C. "
                    "No es igual al codón: es su complemento.")
    else:
        texto += tr("Busca esos codones en la Chuleta del manual (M). Si te pasaste del "
                    "paro o paraste antes, revisa UAA, UAG y UGA.")
    texto += "\n\n" + tr("Lo repetimos con otros codones (el código es degenerado: un mismo "
                         "aminoácido tiene varios).")
    d.popup(win, texto, tr("René-virus"), ancho=72, attr=d.c("mal"))


def _sintetizado(win, juego, pid, despues=None):
    hechos = juego["peptidos"]
    pep = datos.PEPTIDOS[pid]
    primera = pid not in hechos
    if primera:
        hechos.append(pid)
        juego["objetos"]["ATP"] += 1
    for m in juego["equipo"]:
        progreso.dar_xp(m, 5)
    progreso.guardar(juego)
    alto, ancho = win.getmaxyx()
    win.erase()
    d.put(win, 0, 1, tr("Péptido sintetizado: {nombre}  ·  {seq}", nombre=pep["nombre"], seq=pep["seq"]),
          d.c("bien", curses.A_BOLD))
    y = 2
    for l in d.envolver(tr("El ribosoma soltó la cadena. Después se cortó la Met inicial y "
                           "quedó el péptido."), min(ancho - 4, 96)):
        d.put(win, y, 2, l, d.c("tenue"))
        y += 1
    y = jefes.dibujar_resumen(win, y + 1, 1, ancho - 2, pep) + 1
    premio = tr("+5 XP para todo tu equipo y 1 ATP.") if primera else tr("+5 XP para todo tu equipo.")
    for l in d.envolver(((despues + "\n\n") if despues else "") + premio, min(ancho - 4, 96)):
        d.put(win, y, 2, l, d.c("bien"))
        y += 1
    d.put(win, alto - 1, 1, tr("[Enter] seguir"), d.c("tenue"))
    win.refresh()
    curses.flushinp()
    while d.tecla(win) not in d.ENTER:
        pass


# ------------------------------------------------------------- explicación
def explicar(win):
    d.dialogo(win, [
        tr("DESDE CERO (1/7) · La receta\n\nUna proteína es una cadena de aminoácidos. "
           "La receta viene en el ARNm, una tira de 4 letras (bases): A, U, G y C."),
        tr("DESDE CERO (2/7) · Codones\n\nEl ARNm se lee de 3 en 3 letras. Cada trío es "
           "un codón y cada codón dice qué aminoácido sigue. Por ejemplo, UUC = Phe.\n\n"
           "Hay 64 codones: 61 dan un aminoácido y 3 (UAA, UAG, UGA) significan «fin». "
           "AUG es la Met y marca el inicio."),
        tr("DESDE CERO (3/7) · El ribosoma\n\nEs la máquina que lee el ARNm. Tiene tres "
           "sitios para ARNt; aquí importan dos:\n• P: el ARNt que carga toda la cadena.\n"
           "• A: donde llega el codón siguiente y entra un ARNt nuevo.\n(Por el tercero, "
           "el E, sale el ARNt ya vacío.)"),
        tr("DESDE CERO (4/7) · El ARNt\n\nEs el traductor. De un lado carga un "
           "aminoácido y del otro tiene 3 bases, el anticodón, que se pegan al codón: "
           "A con U y G con C.\n\nCodón      5'-UUC-3'\nAnticodón  3'-AAG-5'  → este ARNt "
           "carga Phe\n\nOjo: el anticodón NO es igual al codón; es su complemento. (En la "
           "célula la 3.ª base del codón se aparea con más holgura, el «bamboleo»; aquí "
           "todas se aparean exacto.)"),
        tr("DESDE CERO (5/7) · Unir y avanzar\n\nCuando el ARNt correcto entra al sitio "
           "A, el ribosoma pasa la cadena a su aminoácido con un enlace peptídico. "
           "Luego avanza un codón y el sitio A queda libre para el siguiente. La cadena "
           "crece del extremo N al C."),
        tr("DESDE CERO (6/7) · El final\n\nNingún ARNt reconoce UAA, UAG ni UGA. Ahí "
           "entra un factor de liberación y la cadena se suelta.\n\nEn la célula estos "
           "péptidos salen de proteínas más largas que unas proteasas cortan. El "
           "René-virus usa un ARNm de laboratorio: AUG + el péptido + paro. Al final se "
           "quita la Met."),
        tr("CÓMO FUNCIONA (7/7)\n\n• La Met inicial ya está en el sitio P.\n• Cada "
           "codón llega al sitio A: elige su ARNt con 1-4 antes de que se acabe la "
           "barra. En el codón de paro elige el factor de liberación (5).\n• Si fallas o "
           "se acaba el tiempo, la proteína sale mutada. No te digo la respuesta: al "
           "final te marco qué codones fallaste y lo repites con otros codones.\n• En "
           "los 2 primeros encargos ves los anticodones; después, solo el aminoácido.\n"
           "• Esc pausa el ribosoma."),
    ], tr("Encargos de síntesis"))


# ------------------------------------------------------------- menú
def capitulo(juego):
    """Índice del siguiente encargo de la historia (len(HISTORIA) si ya se acabó)."""
    hechos = juego["peptidos"]
    for n, (pid, *_) in enumerate(HISTORIA):
        if pid not in hechos:
            return n
    return len(HISTORIA)


def hechos(juego):
    """Cuántos encargos de la historia están cumplidos (en partidas viejas
    pueden estar salteados)."""
    return sum(p in juego["peptidos"] for p in HISTORIA_IDS)


def historia_completa(juego):
    return capitulo(juego) >= len(HISTORIA)


def _jugar_capitulo(win, juego, n):
    pid, seg, ver_anti, pedido, despues = HISTORIA[n]
    pep = datos.PEPTIDOS[pid]
    win.erase()
    d.popup(win, pedido + "\n\n" + tr("Péptido: {nombre}, {k} aminoácidos. Tiempo por "
                                          "codón: {s} s.", nombre=pep["nombre"], k=len(pep["seq"]),
                                          s=seg),
            tr("Encargo {n}/{t} del René-virus", n=n + 1, t=len(HISTORIA)), ancho=72)
    titulo = tr("ENCARGO {n}/{t} · {nombre}", n=n + 1, t=len(HISTORIA), nombre=pep["nombre"])
    while True:
        r = ribosoma(win, juego, titulo, pep["seq"], seg, ver_anti)
        if r is None:
            return
        bien, codones, malos, leido = r
        if bien:
            _sintetizado(win, juego, pid, despues)
            return
        _revision(win, codones, malos, leido, ver_anti)
        win.erase()
        if d.menu(win, tr("¿Otra vez?"), [tr("Sí, con otros codones"), tr("Ahora no")]) != 0:
            return


def _libre(win, juego):
    otros = LIBRES
    hechos = juego["peptidos"]
    opciones = [f"{'√' if p in hechos else ' '} {datos.PEPTIDOS[p]['nombre']} "
                f"({len(datos.PEPTIDOS[p]['seq'])} aa)" for p in otros]
    win.erase()
    sel = d.menu(win, tr("Síntesis libre ({n}/{t})", n=sum(p in hechos for p in otros), t=len(otros)),
                 opciones)
    if sel is None:
        return
    pid = otros[sel]
    pep = datos.PEPTIDOS[pid]
    while True:
        r = ribosoma(win, juego, tr("SÍNTESIS LIBRE · {nombre}", nombre=pep["nombre"]),
                     pep["seq"], LIBRE_SEG, False)
        if r is None:
            return
        bien, codones, malos, leido = r
        if bien:
            _sintetizado(win, juego, pid)
            return
        _revision(win, codones, malos, leido, False)
        win.erase()
        if d.menu(win, tr("¿Otra vez?"), [tr("Sí, con otros codones"), tr("Ahora no")]) != 0:
            return


def encargo(win, juego):
    if "intro_sintesis" not in juego["recompensas"]:
        juego["recompensas"].append("intro_sintesis")
        explicar(win)
    while True:
        n = capitulo(juego)
        ops = []
        if n < len(HISTORIA):
            ops.append(("sig", tr("Encargo {n}/{t}: {nombre}", n=n + 1, t=len(HISTORIA),
                                  nombre=datos.PEPTIDOS[HISTORIA[n][0]]["nombre"])))
        if hechos(juego):
            ops.append(("rep", tr("Repetir un encargo")))
        if n >= len(HISTORIA):
            ops.append(("libre", tr("Síntesis libre (los otros péptidos del catálogo)")))
        ops += [("como", tr("¿Cómo funciona?")), ("nada", tr("Volver"))]
        win.erase()
        op = d.menu(win, tr("Encargos de síntesis ({n}/{t})", n=hechos(juego),
                            t=len(HISTORIA)), [t for _, t in ops])
        clave = ops[op][0] if op is not None else "nada"
        if clave == "sig":
            _jugar_capitulo(win, juego, n)
        elif clave == "rep":
            listos = [k for k in range(len(HISTORIA)) if HISTORIA[k][0] in juego["peptidos"]]
            sel = d.menu(win, tr("Repetir un encargo"),
                         [f"{k + 1}. {datos.PEPTIDOS[HISTORIA[k][0]]['nombre']}" for k in listos])
            if sel is not None:
                _jugar_capitulo(win, juego, listos[sel])
        elif clave == "libre":
            _libre(win, juego)
        elif clave == "como":
            explicar(win)
        else:
            return
