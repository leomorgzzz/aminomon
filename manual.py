"""Manual por pestañas: se abre con [M] o [?] en cualquier momento."""

import curses

import datos
import dibujo as d

PESTANAS = [
    ("jugar", "Jugar", "Jugar"),
    ("tipos", "Tipos", "Tipos"),
    ("afinidad", "Afinidad", "Afin."),
    ("interacciones", "Interacciones", "Inter."),
    ("modificaciones", "Modificaciones", "Modif."),
    ("zonas", "Zonas", "Zonas"),
    ("nutricion", "Nutrición", "Nutr."),
    ("glosario", "Glosario", "Glos."),
    ("chuleta", "Chuleta", "Chuleta"),
]

AA = datos.AMINOACIDOS
T_ = datos.TIPOS


def L(*segmentos):
    """Una línea: segmentos (texto, color[, attr extra]) o un str simple."""
    salida = []
    for s in segmentos:
        if isinstance(s, str):
            salida.append((s, "texto", 0))
        else:
            salida.append((s[0], s[1], s[2] if len(s) > 2 else 0))
    return salida


def tabla(filas, sangria="  ", sep=2):
    """Filas de celdas (str o (texto, color[, attr])) → líneas alineadas."""
    return [L((sangria, "texto"), *fila) for fila in d.alinear(filas, sep)]


def T(texto):
    return L((texto, "titulo", curses.A_BOLD))


def parrafo(texto, ancho, color="texto", sangria=""):
    if texto.startswith("• "):
        # sangría colgante: las líneas siguientes se alinean con el texto
        lineas = d.envolver(texto[2:], ancho - len(sangria) - 2)
        return [L((sangria + ("• " if i == 0 else "  ") + l, color)) for i, l in enumerate(lineas)]
    return [L((sangria + l, color)) for l in d.envolver(texto, ancho - len(sangria))]


def _nombre(c):
    return f"{AA[c]['tres']} ({c})"


def _marca(juego, c):
    return "✓" if juego["capturados"].get(c, 0) else " "


def _tipos_seg(tipos, corto=True):
    return [(f"[{T_[t]['corto' if corto else 'nombre']}]", t, curses.A_BOLD) for t in tipos]


# ---------------------------------------------------------------- pestañas
def p_jugar(juego, rival, an):
    return [
        T("Objetivo"),
        *parrafo("Recorre la célula, encuentra a los 20 aminoácidos, captúralos y "
                 "completa la Aminodex. Vence a los 7 jefes (J) y al final a la "
                 "Chaperona (H).", an), L(""),
        T("Pantalla completa"),
        *parrafo("El juego se adapta al tamaño de la terminal: en pantalla completa "
                 "(F11) ves toda la célula, el panel lateral con el minimapa y a tu "
                 "aminoácido en combate.", an), L(""),
        T("Controles en el mapa"),
        *tabla([[("←↑→↓ / WASD", "titulo"), "moverse"],
                [("M o ?", "titulo"), "este manual"],
                [("X", "titulo"), "Aminodex"],
                [("E", "titulo"), "equipo: líder, orden y modificaciones"],
                [("G / Q", "titulo"), "guardar / guardar y salir"]]),
        L(""),
        T("Símbolos del mapa"),
        *tabla([[("≈", "NP"), "membrana (colas)", ("◦", "ARO"), "interfase", ("·", "POL"), "citosol"],
                [("∴", "POS"), "ribosomas", ("░", "NEG"), "retículo", ("═", "POL"), "Golgi"],
                [("●", "NEG"), "lisosoma", ("§", "POS"), "cromatina", ("▓", "POS"), "nucléolo"],
                [("╳", "tenue"), "colágeno", ("◉", "titulo"), "mitocondria", ("O", "mal"), "poro nuclear"],
                [("█", "oscuro"), "envoltura", ("V", "titulo"), "René-virus", ("H", "titulo"), "Chaperona"],
                [("J", "mal"), "jefe", ("i", "agua"), "cartel", ("C K", "titulo"), "vitaminas C y K"]]),
        L(""),
        T("Combate"),
        *parrafo("En las zonas marcadas con símbolos aparecen aminoácidos salvajes. "
                 "Solo ves su estructura: deduce su grupo [D] para ganar +10 de "
                 "afinidad y ver qué interacción formará cada movimiento. Si no, "
                 "el grupo se revela tras 3 turnos.", an),
        *parrafo("Cada movimiento es una interacción formada por tu grupo R (o por "
                 "tu esqueleto) con el rival. Su nombre indica la clase de "
                 "interacción y el grupo que la forma; la interacción concreta "
                 "(puente salino, catión–π, repulsión…) depende del grupo del rival "
                 "y se muestra a la derecha de cada movimiento. Si el rival tiene "
                 "dos tipos, los factores se multiplican (×2 · ×2 = ×4).", an),
        *parrafo("Con afinidad ≥ 50 lanza un ARNt (T) y responde bien la pregunta. "
                 "El rival responde con agitación térmica que baja tu ENERGÍA.", an),
        L(""),
        *tabla([[("1-5", "titulo"), "interacciones", ("T", "titulo"), "lanzar ARNt"],
                [("D", "titulo"), "deducir el grupo", ("C", "titulo"), "cambiar de aminoácido"],
                [("H", "titulo"), "huir", ("I", "titulo"), "detalle de las interacciones"],
                [("V", "titulo"), "velocidad de animación", ("M", "titulo"), "manual"]]),
        *parrafo("Las animaciones muestran los grupos químicos reales y un "
                 "subtítulo con cada paso; cualquier tecla las salta.", an, "tenue"),
        L(""),
        T("Captura"),
        *parrafo("1.ª vez: ¿cuál es? 2.ª: código de 3 letras. 3.ª: de 1 letra. "
                 "Después: carga, grupo, pKR, pI (y calcularlo), nutrición, "
                 "codones e hidropatía. Lo que fallas "
                 "vuelve más seguido.", an),
        L(""),
        T("Jefes"),
        *parrafo("Cada jefe pide construir un péptido con lo que ya capturaste; "
                 "al lograrlo ves tu péptido dibujado. El poro nuclear es un jefe: "
                 "necesitas una NLS con al menos 4 Lys (viven en los "
                 "ribosomas ∴) para entrar al núcleo. La Arg solo vive "
                 "adentro (núcleo y nucléolo). En cada reto puedes usar cada "
                 "aminoácido tantas veces como lo tengas en tu equipo.", an),
        L(""),
        T("Después de la Chaperona"),
        *parrafo("Habla con el René-virus (V): su examen final te pide traducir "
                 "ARNm y analizar mutaciones reales (anemia falciforme, fibrosis "
                 "quística, KRAS, Huntington…).", an),
        L(""),
        T("Después del examen final"),
        *parrafo("El René-virus te hace encargos de síntesis: péptidos reales "
                 "(encefalinas, oxitocina, angiotensina II, sustancia P, Tat del "
                 "VIH…). Traduces su ARNm y, si tu equipo tiene suficientes copias "
                 "de cada residuo, se sintetiza y entra al catálogo de péptidos, al "
                 "final de la Aminodex. Los largos piden varias Arg, Gly o Phe: "
                 "sigue capturando.", an),
    ]


def p_tipos(juego, rival, an):
    out = [T("Los 5 grupos de Lehninger"), *parrafo("Cada aminoácido tiene un tipo (puro) o dos "
                                                     "(doble). ✓ = ya lo capturaste.", an, "tenue"), L("")]
    for t, info in T_.items():
        puros = [c for c in datos.ORDEN if AA[c]["tipos"] == (t,)]
        dobles = [c for c in datos.ORDEN if t in AA[c]["tipos"] and len(AA[c]["tipos"]) == 2]
        out.append(L((f"■ {info['nombre']}", t, curses.A_BOLD)))
        out += parrafo(info["desc"], an, sangria="  ")
        if puros:
            out += parrafo("Puros: " + "  ".join(f"{_marca(juego, c)}{_nombre(c)}" for c in puros),
                           an, t, "  ")
        if dobles:
            out += parrafo("Dobles: " + "  ".join(
                f"{_marca(juego, c)}{_nombre(c)} ({datos.nombre_tipos(AA[c]['tipos'], True)})"
                for c in dobles), an, t, "  ")
        out.append(L(""))
    out += [T("¿Por qué solo los aromáticos tienen dos tipos?"),
            *parrafo("Los tipos del juego son exactamente los 5 grupos de "
                     "Lehninger. Solo los aromáticos llevan un segundo tipo, y sale "
                     "del mismo libro: «Phe, Tyr y Trp son relativamente no polares; "
                     "Tyr y Trp son bastante más polares que Phe por el OH de Tyr y "
                     "el N del indol de Trp».", an, sangria="  "),
            *parrafo("Phe = Aromático / No polar.  Tyr = Aromático / Polar (O–H).  "
                     "Trp = Aromático / Polar (N–H).", an, sangria="  "),
            *parrafo("Nota sobre His: Lehninger la clasifica como cargado +, aunque a "
                     "pH 7 solo ~10% está protonada (pKR 6).", an, sangria="  "),
            L(""),
            T("Resumen por grupo")]
    for g, nombre in datos.GRUPOS.items():
        miembros = [c for c in datos.ORDEN if AA[c]["grupo"] == g]
        out += parrafo(f"{nombre}: " + "  ".join(_nombre(c) for c in miembros), an,
                       d.COLOR_GRUPO[g], "  ")
    return out


def p_afinidad(juego, rival, an):
    tipos = datos.ORDEN_TIPOS
    out = [T("¿Qué tan afín es cada tipo de movimiento con cada tipo?"),
           *parrafo("Fila = tipo de TU movimiento. Columna = tipo del RIVAL.", an, "tenue"),
           L("")]
    filas = [[("Movimiento ↓ / Rival →", "tenue")] +
             [(T_[t]["corto"], t, curses.A_BOLD | curses.A_UNDERLINE if rival and t in rival else curses.A_BOLD)
              for t in tipos]]
    for a in tipos:
        fila = [(T_[a]["nombre"], a, curses.A_BOLD)]
        for b in tipos:
            m, _ = datos.EFECTIVIDAD[a][b]
            color = {2: "bien", 0: "mal", 0.5: "tenue"}.get(m, "texto")
            fila.append((f"×{datos.fmt_mult(m)}", color, curses.A_BOLD if rival and b in rival else 0))
        filas.append(fila)
    filas.append([("Neutro", "NEU", curses.A_BOLD)] + [("×1", "texto")] * len(tipos))
    out += tabla(filas, sep=3)
    out.append(L(""))
    if rival:
        out.append(L(("▶ Tu rival es ", "titulo"), *_tipos_seg(rival, False)))
        filas = sorted(((datos.multiplicador(a, rival)[0], a) for a in tipos), reverse=True)
        buenos = [(f"{T_[a]['nombre']} ×{datos.fmt_mult(m)}  ", a) for m, a in filas if m >= 2]
        out.append(L(("  Mejores: ", "bien"), *(buenos or [("ninguno llega a ×2", "tenue")])))
        malos = [(f"{T_[a]['nombre']} ×{datos.fmt_mult(m)}  ", a) for m, a in filas if m <= 0.5]
        if malos:
            out.append(L(("  Evita:   ", "mal"), *malos))
        out.append(L(""))
    out += [
        T("La química detrás (la tabla es simétrica)"),
        *tabla([[("Pareja", "tenue"), ("Interacción", "tenue"), ("×", "tenue")],
                [("No polar + No polar / Aromático", "NP"), "efecto hidrofóbico", ("×2", "bien")],
                [("No polar + Polar / cargado", "NP"), "el agua solvata al grupo polar", ("×½", "tenue")],
                [("Aromático + Aromático", "ARO"), "apilamiento π–π", ("×2", "bien")],
                [("Aromático + Cargado +", "ARO"), "catión–π", ("×2", "bien")],
                [("Aromático + Cargado −", "ARO"), "la cara π repele al anión", ("×½", "tenue")],
                [("Polar + Polar", "POL"), "puentes de H", ("×2", "bien")],
                [("Polar + cargado", "POL"), "puente de H", ("×1", "texto")],
                [("Cargado + + Cargado −", "POS"), "puente salino", ("×2", "bien")],
                [("Misma carga", "NEG"), "repulsión (el rival puede huir)", ("×0", "mal")],
                [("Neutro + cualquiera", "NEU"), "esqueleto peptídico o van der Waals", ("×1", "texto")]]),
        L(""),
        T("Reglas químicas que el juego respeta"),
        *parrafo("• Un puente de H necesita un DONADOR (X–H) y un ACEPTOR (par "
                 "libre). El N–H del Trp solo dona: con Lys, Arg o His (que también "
                 "solo donan) no hay puente de H (×½).", an, sangria="  "),
        *parrafo("• Cada aminoácido solo forma interacciones de su propio grupo R, "
                 "más las del esqueleto peptídico y van der Waals, que todos tienen.",
                 an, sangria="  "),
        *parrafo("• El N⁺(CH₃)₃ de la trimetil-lisina no tiene H: con grupos polares "
                 "solo hay atracción ion–dipolo, sin puente de H.", an, sangria="  "),
        *parrafo("• La Pro (y la Hyp) no tiene H en el N del esqueleto: no forma el "
                 "puente de H del esqueleto como donador.", an, sangria="  "),
        *parrafo("• El puente disulfuro solo existe entre dos Cys.", an, sangria="  "),
        L(""),
        T("Tipos dobles"),
        *parrafo("Contra un rival de dos tipos se multiplican los factores. Con un "
                 "movimiento No polar: Phe (Aromático/No polar) ×2·×2 = ×4, Tyr "
                 "y Trp (Aromático/Polar) ×2·×½ = ×1: Phe es la más hidrofóbica de "
                 "las tres.", an, sangria="  "),
    ]
    return out


def p_interacciones(juego, rival, an):
    out = [T("Interacciones por aminoácido"),
           *parrafo("Cada interacción se nombra por su clase y por el grupo R que la "
                    "forma. Todos tienen además «Van der Waals» y, salvo la Pro, "
                    "«Puente de H · esqueleto».", an, "tenue"), L("")]
    filas = [[("", "tenue"), ("Grupo R", "tenue"), ("Clase", "tenue"),
              ("Interacciones de cadena lateral", "tenue")]]
    for c in datos.ORDEN:
        a = AA[c]
        nombre_r, _, clase = datos.GRUPO_R[c]
        propias = [datos.MOVIMIENTOS[m] for m in datos.forma(c)["movs"]
                   if datos.MOVIMIENTOS[m]["tipo"] != datos.NEUTRO]
        texto = ", ".join(f"{m['nombre']} ({m['poder']})" for m in propias) or "— (su R es un H)"
        filas.append([(a["tres"], a["tipos"][0], curses.A_BOLD), (nombre_r, a["tipos"][0]),
                      (clase, "tenue"), texto])
    out += tabla(filas)
    out += [L(""), T("Qué hace cada clase de interacción")]
    for t in datos.ORDEN_TIPOS:
        desc, ciencia = datos.DESC_TIPO[t]
        out.append(L((f"  {datos.INTERACCION[t]} ({T_[t]['nombre']})", t, curses.A_BOLD)))
        out += parrafo(desc, an, sangria="    ")
        out += parrafo(ciencia, an, "agua", "    ")
    for mid in ("puente_h_esqueleto", "van_der_waals", "puente_disulfuro"):
        m = datos.MOVIMIENTOS[mid]
        out.append(L((f"  {m['nombre']}", "titulo", curses.A_BOLD), (f"  poder {m['poder']}", "tenue")))
        out += parrafo(m["desc"], an, sangria="    ")
        out += parrafo(m["ciencia"], an, "agua", "    ")
    return out


def p_modificaciones(juego, rival, an):
    out = [T("Modificaciones postraduccionales"),
           *parrafo("Se activan desde el menú Equipo [E] → V cuando se cumplen los "
                    "requisitos. ✓ = ya la conseguiste.", an), L("")]
    for eid, ev in datos.MODIFICACIONES.items():
        base = AA[ev["base"]]
        visto = "✓ " if eid in juego["evos_vistas"] else "  "
        req = ev["req"]
        como = [f"nivel {req['nivel']}"]
        if "objeto" in req:
            como.append(f"1 {req['objeto']}")
        if "zona" in req:
            como.append(f"estar en {datos.ZONAS[req['zona']]['nombre']}")
        if req.get("otra_cys"):
            como.append("otra Cys en el equipo (se fusionan)")
        out.append(L((visto, "bien"),
                     (f"{base['nombre']} ({base['tres']})", base["tipos"][0], curses.A_BOLD),
                     ("  →  ", "tenue"),
                     (f"{ev['nombre']} ({ev['tres']})", ev["tipos"][0], curses.A_BOLD)))
        out.append(L(("    Cómo: ", "titulo"), ", ".join(como)))
        out.append(L(("    Tipos: ", "titulo"), *_tipos_seg(base["tipos"]), ("  →  ", "tenue"),
                     *_tipos_seg(ev["tipos"])))
        propias = [datos.MOVIMIENTOS[m] for m in datos.forma(eid)["movs"]
                   if datos.MOVIMIENTOS[m]["tipo"] != datos.NEUTRO]
        out.append(L(("    Interacciones: ", "titulo"),
                     *[(f"{m['nombre']}  ", m["tipo"]) for m in propias]))
        out += parrafo("Cambio: " + ev["cambio"], an, sangria="    ")
        out += parrafo("Biología: " + ev["bio"], an, "agua", "    ")
        out.append(L(""))
    out.append(L(("Objetos: ", "titulo"),
                 "  ".join(f"{k} ({juego['objetos'].get(k, 0)})" for k in datos.OBJETOS)))
    for k, v in datos.OBJETOS.items():
        out += parrafo(f"• {k}: {v}", an, sangria="  ")
    return out


def p_zonas(juego, rival, an):
    out = [T("Zonas de la célula")]
    for z, info in datos.ZONAS.items():
        visitada = "" if z in juego["zonas_visitadas"] else "   (sin visitar)"
        out.append(L((f" {info['glifo']} ", info["color"]),
                     (info["nombre"], info["color"], curses.A_BOLD), (visitada, "tenue")))
        if info["aminos"]:
            out.append(L(("   Aparecen: ", "titulo"),
                         ", ".join(_nombre(c) for c in info["aminos"]),
                         (f"   (niveles {info['niveles'][0]}–{info['niveles'][1]})", "tenue")))
        out += parrafo(info["por_que"], an, sangria="   ")
        out.append(L(""))
    return out


def p_nutricion(juego, rival, an):
    out = [T("Clasificación nutricional en humanos")]
    for cat, desc in datos.NUTRICION.items():
        miembros = [c for c in datos.ORDEN if AA[c]["nutricion"] == cat]
        out.append(L((f"■ {cat} ({len(miembros)})", "titulo", curses.A_BOLD)))
        out += parrafo(desc, an, sangria="  ")
        out += parrafo("  ".join(_nombre(c) for c in miembros), an, "texto", "  ")
        out.append(L(""))
    out.append(T("Truco para los esenciales"))
    out += parrafo("'PVT TIM HaLL': Phe Val Thr Trp Ile Met His (Arg) Leu Lys. La A "
                   "es Arg, que solo es esencial en neonatos (condicional).", an, sangria="  ")
    return out


def p_glosario(juego, rival, an):
    out = [T("Glosario")]
    for termino, definicion in datos.GLOSARIO:
        out.append(L((f"  {termino}", "titulo", curses.A_BOLD)))
        out += parrafo(definicion, an, sangria="    ")
    return out


def p_chuleta(juego, rival, an):
    out = [T("Preguntas que pueden salir al lanzar el ARNt"),
           L("  1.ª: ¿qué aminoácido es?  2.ª: código de 3 letras  3.ª: código de 1 letra"),
           L("  Después: carga · grupo · pKR · pI · calcular el pI · nutrición ·"),
           L("           codón · hidropatía"),
           L(""), T("Tabla rápida (Lehninger, 25 °C)"),
           ]
    filas = [[(h, "tenue") for h in ("1L", "3L", "Nombre", "Tipos", "MW", "pK1", "pK2",
                                     "pKR", "pI", "KD", "Nutrición")]]
    for c in datos.ORDEN:
        a = AA[c]
        filas.append([
            (c, a["tipos"][0], curses.A_BOLD), (a["tres"], a["tipos"][0]),
            (a["nombre"], a["tipos"][0]),
            (datos.nombre_tipos(a["tipos"], True), "tenue"),
            f"{a['masa']:.0f}".rjust(3), f"{a['pk1']:.2f}", f"{a['pk2']:.2f}".rjust(5),
            (f"{a['pkr']:.2f}" if a["pkr"] else "—").rjust(5), f"{a['pi']:.2f}".rjust(5),
            f"{a['hidropatia']:+.1f}".replace("-", "−").rjust(4), a["nutricion"],
        ])
    out += tabla(filas)
    out += [L(""), T("Trucos"),
            *parrafo("• Códigos de 1 letra menos intuitivos: F=Fenilalanina, Y=tYrosina, W=Trp (doble "
                     "anillo), N=asparagiNe, Q=Q-tamina, D=asparDate, "
                     "E=glutEmate, K=antes de L, R=aRginina.", an, sangria="  "),
            *parrafo("• Cargas a pH 7: D E (−), K R (+), H ≈ neutra (+ a pH 5).", an, sangria="  "),
            *parrafo("• pI: ácidos (pK1+pKR)/2, básicos (pK2+pKR)/2, el resto "
                     "(pK1+pK2)/2. Asp 2.77 es el más bajo; Arg 10.76 el más alto.", an, sangria="  ")]
    return out


GENERADORES = {
    "jugar": p_jugar, "tipos": p_tipos, "afinidad": p_afinidad,
    "interacciones": p_interacciones, "modificaciones": p_modificaciones,
    "zonas": p_zonas, "nutricion": p_nutricion, "glosario": p_glosario,
    "chuleta": p_chuleta,
}


def mostrar(win, juego, pestana="jugar", rival=None):
    idx = [p[0] for p in PESTANAS].index(pestana)
    scroll = 0
    while True:
        alto, ancho = win.getmaxyx()
        an = min(ancho - 4, 100)
        x0 = max(1, (ancho - an) // 2) if ancho > 110 else 1
        lineas = GENERADORES[PESTANAS[idx][0]](juego, rival, an)
        visibles = alto - 4
        scroll = max(0, min(scroll, len(lineas) - visibles))
        win.erase()
        corto = ancho < 100
        x = x0
        for i, p in enumerate(PESTANAS):
            etiqueta = f" {p[2] if corto else p[1]} "
            attr = d.c("titulo", curses.A_REVERSE | curses.A_BOLD) if i == idx else d.c("tenue")
            d.put(win, 0, x, etiqueta, attr)
            x += len(etiqueta)
        d.put(win, 1, 0, "─" * ancho, d.c("tenue"))
        for i, linea in enumerate(lineas[scroll:scroll + visibles]):
            cx = x0
            for texto, color, extra in linea:
                d.put(win, 2 + i, cx, texto, d.c(color, extra))
                cx += len(texto)
        pie = "←/→ pestaña  ↑/↓ desplazar  1-9 ir  Esc cerrar"
        if len(lineas) > visibles:
            pie += f"   [{scroll + 1}-{min(len(lineas), scroll + visibles)}/{len(lineas)}]"
        d.put(win, alto - 1, x0, pie, d.c("tenue"))
        win.refresh()
        k = d.tecla(win)
        if k == d.ESC or d.es(k, "q", "m"):
            return
        if d.es(k, curses.KEY_RIGHT, "l", "\t"):
            idx, scroll = (idx + 1) % len(PESTANAS), 0
        elif d.es(k, curses.KEY_LEFT, "h"):
            idx, scroll = (idx - 1) % len(PESTANAS), 0
        elif d.es(k, curses.KEY_DOWN, "j"):
            scroll += 1
        elif d.es(k, curses.KEY_UP, "k"):
            scroll -= 1
        elif d.es(k, curses.KEY_NPAGE, " "):
            scroll += visibles - 1
        elif d.es(k, curses.KEY_PPAGE):
            scroll -= visibles - 1
        elif isinstance(k, str) and k.isdigit() and 1 <= int(k) <= len(PESTANAS):
            idx, scroll = int(k) - 1, 0
