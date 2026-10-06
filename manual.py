"""Manual por pestañas: se abre con [M] o [?] en cualquier momento."""

import curses

import datos
import dibujo as d

PESTANAS = [
    ("jugar", "Jugar", "Jugar"),
    ("tipos", "Tipos", "Tipos"),
    ("afinidad", "Afinidad", "Afin."),
    ("movimientos", "Movimientos", "Movs"),
    ("evoluciones", "Evoluciones", "Evos"),
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


def T(texto):
    return L((texto, "titulo", curses.A_BOLD))


def parrafo(texto, ancho, color="texto", sangria=""):
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
        L(("  ←↑→↓ / WASD ", "titulo"), "moverse"),
        L(("  M o ?       ", "titulo"), "este manual"),
        L(("  X           ", "titulo"), "Aminodex (fichas de lo capturado)"),
        L(("  E           ", "titulo"), "equipo, líder y evoluciones"),
        L(("  G / Q       ", "titulo"), "guardar / guardar y salir"),
        L(""),
        T("Símbolos del mapa"),
        L(("  ≈ ", "NP"), "membrana  ", ("◦ ", "ARO"), "interfase  ", ("· ", "POL"),
          "citosol  ", ("∴ ", "POS"), "polirribosomas  ", ("░ ", "NEG"), "retículo"),
        L(("  ═ ", "POL"), "Golgi  ", ("● ", "NEG"), "lisosoma  ", ("§ ", "POS"),
          "cromatina  ", ("▓ ", "POS"), "nucléolo  ", ("╳ ", "tenue"), "colágeno"),
        L(("  ◉ ", "titulo"), "mitocondria (cura + ATP)  ", ("O ", "mal"),
          "poro nuclear (necesita NLS)  ", ("█ ", "oscuro"), "envoltura"),
        L(("  R ", "titulo"), "Profesor Ribosoma  ", ("H ", "titulo"), "Chaperona  ",
          ("J ", "mal"), "jefe  ", ("i ", "agua"), "cartel  ", ("C K ", "titulo"),
          "vitaminas"),
        L(""),
        T("Combate"),
        *parrafo("Al caminar por la hierba aparece un aminoácido salvaje. Solo ves "
                 "su ESTRUCTURA: deduce sus tipos (D) para ganar +10 de afinidad y "
                 "ver qué tan afín es cada movimiento. Si no, se revelan solos "
                 "tras 3 turnos.", an),
        *parrafo("No se pelea: se forman interacciones. Cada movimiento usa la "
                 "química de un grupo de Lehninger y sube la AFINIDAD según la "
                 "tabla (pestaña Afinidad). Si el rival tiene dos tipos, los "
                 "multiplicadores se multiplican (×2 · ×2 = ×4). Los movimientos "
                 "de tu grupo (★) valen ×1.5.", an),
        *parrafo("Con afinidad ≥ 50 lanza un ARNt (T) y responde bien la pregunta. "
                 "El rival responde con agitación térmica que baja tu ENERGÍA.", an),
        L(""),
        L(("  1-5 ", "titulo"), "movimientos  ", ("T ", "titulo"), "ARNt  ",
          ("D ", "titulo"), "deducir grupo  ", ("C ", "titulo"), "cambiar  ",
          ("H ", "titulo"), "huir  ", ("I ", "titulo"), "info"),
        L(("  V   ", "titulo"), "velocidad de las animaciones (lenta / normal / rápida)."),
        *parrafo("Las animaciones muestran los grupos químicos reales y un "
                 "subtítulo con cada paso; cualquier tecla las salta.", an, "tenue"),
        L(""),
        T("Captura"),
        *parrafo("1.ª vez: ¿cuál es? 2.ª: código de 3 letras. 3.ª: de 1 letra. "
                 "Después: carga, grupo, pKR, pI (y calcularlo), nutrición, "
                 "precursor, codones, destino… Lo que fallas "
                 "vuelve más seguido.", an),
        L(""),
        T("Jefes"),
        *parrafo("Cada jefe pide construir un péptido con lo que ya capturaste; "
                 "al lograrlo ves tu péptido dibujado. El poro nuclear es un jefe: "
                 "necesitas una NLS (K y R, que viven en los polirribosomas ∴) "
                 "para entrar al núcleo.", an),
        L(""),
        T("Después de la Chaperona"),
        *parrafo("Habla con el Profesor Ribosoma (R): el examen del Ribosoma "
                 "Maestro te pide traducir ARNm y analizar mutaciones reales "
                 "(anemia falciforme, fibrosis quística, KRAS, Huntington…).", an),
    ]


def p_tipos(juego, rival, an):
    out = [T("Los 7 tipos"), *parrafo("Cada aminoácido tiene un tipo (puro) o dos "
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
            *parrafo("Ojo con His: Lehninger la pone en Cargado +, aunque a pH 7 "
                     "solo ~10% está protonada (pKR 6). En combate puede "
                     "desprotonarse con «Cambio de pH».", an, sangria="  "),
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
    cab = [("  Movim. ↓ Rival →", "tenue")]
    for t in tipos:
        extra = curses.A_BOLD | curses.A_UNDERLINE if rival and t in rival else 0
        cab.append((f" {T_[t]['corto']:<8}", t, extra))
    out.append(L(*cab))
    for a in tipos:
        fila = [(f"  {T_[a]['nombre']:<17}", a, curses.A_BOLD)]
        for b in tipos:
            m, _ = datos.EFECTIVIDAD[a][b]
            color = {2: "bien", 0: "mal", 0.5: "tenue"}.get(m, "texto")
            fila.append((f" ×{datos.fmt_mult(m):<7}", color,
                         curses.A_BOLD if rival and b in rival else 0))
        out.append(L(*fila))
    out.append(L(("  Neutro           ", "NEU", curses.A_BOLD), (" ×1 contra todos", "texto")))
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
        L(("  No polar", "NP"), " + No polar o Aromático → efecto hidrofóbico (×2)."),
        L(("  No polar", "NP"), " + Polar o cargado → el agua solvata al grupo polar (×½)."),
        L(("  Aromático", "ARO"), " + Aromático → apilamiento π–π (×2)."),
        L(("  Aromático", "ARO"), " + Cargado + → catión–π (×2)."),
        L(("  Aromático", "ARO"), " + Cargado − → la cara π repele al anión (×½)."),
        L(("  Polar", "POL"), " + Polar → puentes de H (×2); + cargado → puente de H (×1)."),
        L(("  Cargado +", "POS"), " + Cargado − → puente salino (×2)."),
        L(("  Cargado +/−", "NEG"), " + misma carga → repulsión (×0, el rival puede huir)."),
        L(("  Neutro", "NEU"), " → esqueleto peptídico o van der Waals: ×1 con todos."),
        L(""),
        T("Reglas químicas que el juego respeta"),
        *parrafo("• Un puente de H necesita un DONADOR (X–H) y un ACEPTOR (par "
                 "libre). El N–H del Trp solo dona: con Lys, Arg o His (que también "
                 "solo donan) no hay puente de H (×½).", an, sangria="  "),
        *parrafo("• Cada aminoácido solo usa movimientos de su propio grupo (o "
                 "neutros). Si cambia de grupo (fosforilada, acetilada, His "
                 "neutra) pierde los de su grupo anterior y gana uno nuevo.", an, sangria="  "),
        *parrafo("• Unir Ca²⁺ estabiliza a TU proteína (dos de tus carboxilatos "
                 "atrapan el Ca²⁺); no cambia la repulsión Ácido–Ácido, que siempre "
                 "es ×0.", an, sangria="  "),
        *parrafo("• Puente disulfuro solo existe entre dos Cys.", an, sangria="  "),
        *parrafo("• ★ Mismo grupo: si el movimiento es de tu grupo, ×1.5.", an, sangria="  "),
        L(""),
        T("Tipos dobles"),
        *parrafo("Contra un rival de dos tipos se multiplican los factores. Con un "
                 "movimiento No polar: Phe (Aromático/No polar) ×2·×2 = ×4, Tyr "
                 "y Trp (Aromático/Polar) ×2·×½ = ×1: Phe es la más hidrofóbica de "
                 "las tres.", an, sangria="  "),
    ]
    return out


def p_movimientos(juego, rival, an):
    duenos = {}
    for c in datos.ORDEN:
        for mid in AA[c]["movs"]:
            duenos.setdefault(mid, []).append(AA[c]["tres"])
    for ev in datos.EVOLUCIONES.values():
        duenos.setdefault(ev["mov"], []).append(ev["tres"])
    out = [T("Movimientos por tipo"),
           *parrafo("Cada movimiento tiene un tipo que decide su afinidad (pestaña "
                    "Afinidad). Entre corchetes: quién lo aprende.", an, "tenue")]
    for t in datos.ORDEN_TIPOS + [datos.NEUTRO]:
        movs = [(mid, m) for mid, m in datos.MOVIMIENTOS.items() if m["tipo"] == t]
        if not movs:
            continue
        nombre = T_[t]["nombre"] if t in T_ else "Neutro"
        out += [L(""), L((f"■ {nombre}", t, curses.A_BOLD))]
        for mid, m in movs:
            out.append(L((f"  {m['nombre']}", t, curses.A_BOLD),
                         (f"  poder {m['poder']}  [{', '.join(duenos.get(mid, []))}]", "tenue")))
            out += parrafo(m["desc"], an, sangria="    ")
            if m.get("ciencia"):
                out += parrafo("↳ " + m["ciencia"], an, "agua", "    ")
    return out


def p_evoluciones(juego, rival, an):
    out = [T("Evoluciones = modificaciones postraduccionales"),
           *parrafo("Se activan desde el menú Equipo [E] → V cuando se cumplen los "
                    "requisitos. ✓ = ya la conseguiste.", an), L("")]
    for eid, ev in datos.EVOLUCIONES.items():
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
        mov = datos.MOVIMIENTOS[ev["mov"]]
        out.append(L(("    Nuevo movimiento: ", "titulo"), (mov["nombre"], mov["tipo"]),
                     (f"  poder {mov['poder']}", "tenue")))
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
    out.append(T("Requerimientos de los esenciales (adulto, FAO/OMS/UNU 2007)"))
    out.append(L(("  mg/kg/día: ", "tenue"),
                 "His 10 · Ile 20 · Leu 39 · Lys 30 · Met+Cys 15 · Phe+Tyr 25 · "))
    out.append(L("             Thr 15 · Trp 4 · Val 26"))
    out += parrafo("Met y Cys, igual que Phe y Tyr, se reportan juntos porque Cys y "
                   "Tyr se sintetizan a partir de Met y Phe.", an, "tenue", "  ")
    out.append(L(""))
    out.append(T("Condicionales: de dónde salen"))
    for c in datos.ORDEN:
        a = AA[c]
        if a["nutricion"] == "Condicional":
            out += parrafo(f"{a['tres']}: {a['nota_nutricion']}", an, sangria="  ")
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
           L("           precursor · codón · hidropatía · destino"),
           L(""), T("Tabla rápida (Lehninger, 25 °C)"),
           L(("  1L 3L  Nombre       Tipos               MW  pK1   pK2   pKR    pI    KD  Nutr.",
              "tenue"))]
    for c in datos.ORDEN:
        a = AA[c]
        pkr = f"{a['pkr']:5.2f}" if a["pkr"] else "   - "
        nutr = {"Esencial": "Esen", "Condicional": "Cond", "No esencial": "No"}[a["nutricion"]]
        out.append(L((f"  {c}  {a['tres']}  {a['nombre']:<12} ", a["tipos"][0]),
                     (f"{datos.nombre_tipos(a['tipos'], True):<19}", "tenue"),
                     (f"{a['masa']:4.0f} {a['pk1']:4.2f}  {a['pk2']:5.2f} {pkr}  {a['pi']:5.2f} "
                      f"{a['hidropatia']:+5.1f}  {nutr}", "texto")))
    out += [L(""), T("Trucos"),
            *parrafo("• Solo cetogénicos: Leu y Lys. Ambos: Ile, Phe, Trp, Tyr, Thr.", an, sangria="  "),
            *parrafo("• Letras raras: F=Fenilalanina, Y=tYrosina, W=Trp (doble "
                     "anillo), N=asparagiNe, Q=Q-tamina, D=asparDate, "
                     "E=glutEmate, K=antes de L, R=aRginina.", an, sangria="  "),
            *parrafo("• Cargas a pH 7: D E (−), K R (+), H ≈ neutra (+ a pH 5).", an, sangria="  "),
            *parrafo("• pI: ácidos (pK1+pKR)/2, básicos (pK2+pKR)/2, el resto "
                     "(pK1+pK2)/2. Asp 2.77 es el más bajo; Arg 10.76 el más alto.", an, sangria="  ")]
    return out


GENERADORES = {
    "jugar": p_jugar, "tipos": p_tipos, "afinidad": p_afinidad,
    "movimientos": p_movimientos, "evoluciones": p_evoluciones,
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
