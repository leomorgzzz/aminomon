"""Combate por turnos: subir la afinidad del salvaje y capturarlo con un ARNt."""

import curses
import random

import animaciones as anim
import datos
import dibujo as d
import manual
import preguntas
import progreso

AFINIDAD_TRNA = 50
TURNOS_PARA_REVELAR = 3
SPRITE_W = 24

# Grupo químico de la cadena lateral, escrito para el lado izquierdo (─X) y
# para el derecho (X─) de la arena.
GRUPO = {
    "G": ("─H", "H─"), "A": ("─CH₃", "H₃C─"), "V": ("─CH(CH₃)₂", "(H₃C)₂CH─"),
    "L": ("─CH₂CH(CH₃)₂", "(H₃C)₂CHCH₂─"), "I": ("─CH(CH₃)C₂H₅", "H₅C₂(H₃C)CH─"),
    "M": ("─CH₂CH₂SCH₃", "H₃CSCH₂CH₂─"), "P": ("─pirrolidina", "pirrolidina─"),
    "F": ("─CH₂─fenilo", "fenilo─CH₂─"), "Y": ("─fenol─OH", "HO─fenol─"),
    "W": ("─indol(N─H)", "(H─N)indol─"), "S": ("─CH₂─OH", "HO─CH₂─"),
    "T": ("─CH(CH₃)OH", "HO(H₃C)CH─"), "C": ("─CH₂─SH", "HS─CH₂─"),
    "N": ("─CONH₂", "H₂NOC─"), "Q": ("─CH₂CONH₂", "H₂NOCCH₂─"),
    "D": ("─COO⁻", "⁻OOC─"), "E": ("─CH₂COO⁻", "⁻OOCCH₂─"),
    "K": ("─NH₃⁺", "⁺H₃N─"), "R": ("─guanidinio⁺", "⁺guanidinio─"),
    "H": ("─imidazol(H⁺)", "(H⁺)imidazol─"),
    "Hyp": ("─pirrolidina─OH", "HO─pirrolidina─"), "Hyl": ("─NH₃⁺", "⁺H₃N─"),
    "Kac": ("─NH─COCH₃", "H₃COC─NH─"), "Kme3": ("─N⁺(CH₃)₃", "(H₃C)₃N⁺─"),
    "pS": ("─O─PO₃²⁻", "²⁻O₃P─O─"), "pT": ("─O─PO₃²⁻", "²⁻O₃P─O─"),
    "pY": ("─fenil─O─PO₃²⁻", "²⁻O₃P─O─fenil─"), "Cis": ("─S─S─", "─S─S─"),
    "Gla": ("─CH(COO⁻)₂", "(⁻OOC)₂CH─"), "Nglc": ("─CONH─glicano", "glicano─HNOC─"),
    "Cit": ("─NH─CO─NH₂", "H₂N─OC─NH─"),
}

# Puentes de H: papel del grupo polar (D = donador, A = aceptor) y cómo se
# escribe con el átomo que participa pegado a la línea de puntos.
#            papel  donador_izq   aceptor_izq    donador_der    aceptor_der
HB = {
    "S": ("DA", "─O─H", "─(H)O:", "H─O─", ":O(H)─"),
    "T": ("DA", "─O─H", "─(H)O:", "H─O─", ":O(H)─"),
    "Y": ("DA", "─fenol─O─H", "─fenol(H)O:", "H─O─fenol─", ":O(H)─fenol─"),
    "W": ("D", "─indol─N─H", None, "H─N─indol─", None),
    "N": ("DA", "─CON(H)─H", "─(H₂N)C═O:", "H─N(H)OC─", ":O═C(NH₂)─"),
    "Q": ("DA", "─CON(H)─H", "─(H₂N)C═O:", "H─N(H)OC─", ":O═C(NH₂)─"),
    "C": ("DA", "─S─H", "─(H)S:", "H─S─", ":S(H)─"),
    "Hyp": ("DA", "─O─H", "─(H)O:", "H─O─", ":O(H)─"),
    "Kac": ("DA", "─N(Ac)─H", "─(HN)C═O:", "H─N(Ac)─", ":O═C(NH)─"),
    "Nglc": ("DA", "─CON(H)─H", "─(HN)C═O:", "H─N(H)OC─", ":O═C(NH)─"),
    "Cit": ("DA", "─CON(H)─H", "─(H₂N)C═O:", "H─N(H)OC─", ":O═C(NH₂)─"),
    "H": ("DA", "─imidazol─N─H", "─imidazol─N:", "H─N─imidazol─", ":N─imidazol─"),
}
CARGADO = {
    "POS": ("D", "─NH₃⁺", "⁺H₃N─"),
    "NEG": ("A", "─COO⁻", "⁻OOC─"),
}
INTERACCION_H = {("POL", "POL"), ("POL", "POS"), ("POL", "NEG"),
                 ("POS", "POL"), ("NEG", "POL")}


def flechas(m):
    if m == 0:
        return "✕"
    if m >= 4:
        return "▲▲"
    if m >= 2:
        return "▲"
    if m < 1:
        return "▼"
    return ""


class Combate:
    def __init__(self, win, juego, aa, nivel, zona):
        self.win, self.juego, self.zona = win, juego, zona
        self.aa = aa
        conocido = progreso.capturado(juego, aa)
        self.salvaje = dict(nivel=nivel, afinidad=0, aturdido=False)
        self.nombre_visible = conocido
        self.tipos_visible = conocido
        self.turno = 1
        self.turnos_jugador = 0
        self.log = []
        self.ultimo_mult = 1.0
        self.cuadro = []
        self.activo = self._primer_vivo()
        self._reiniciar_estado()
        juego.setdefault("ajustes", {}).setdefault("velocidad", "lenta")
        if aa not in juego["vistos"]:
            juego["vistos"].append(aa)

    # ---------------------------------------------------------- utilidades
    def _primer_vivo(self):
        for i, m in enumerate(self.juego["equipo"]):
            if m["energia"] > 0:
                return i
        return None

    def _reiniciar_estado(self):
        self.estado = dict(tipos_temp=None, turnos_temp=0, escudo=0, esquiva=False,
                           potenciar=False, extra=[], his_neutra=False)

    @property
    def mon(self):
        return self.juego["equipo"][self.activo]

    def tipos_mio(self):
        return self.estado["tipos_temp"] or datos.forma(self.mon["id"])["tipos"]

    def tipos_salvaje(self):
        return datos.AMINOACIDOS[self.aa]["tipos"]

    def nombre_salvaje(self):
        return datos.AMINOACIDOS[self.aa]["nombre"] if self.nombre_visible else "¿¿??"

    def movimientos(self):
        f = datos.forma(self.mon["id"])
        return f["movs"] + [m for m in self.estado["extra"] if m not in f["movs"]]

    def disponible(self, mid):
        """Un movimiento con química de un grupo solo sirve si tienes ese grupo."""
        t = datos.MOVIMIENTOS[mid]["tipo"]
        return t == datos.NEUTRO or t in self.tipos_mio()

    def decir(self, texto):
        self.log.append(texto)
        self.log = self.log[-8:]

    @property
    def velocidad(self):
        return self.juego["ajustes"]["velocidad"]

    # ------------------------------------------------------ química real
    def _papel_mio(self, tipo_mov):
        if tipo_mov in CARGADO:
            return CARGADO[tipo_mov][0]
        return HB.get(self.mon["id"], ("DA",))[0]

    def _papel_rival(self, tipo):
        if tipo in CARGADO:
            return CARGADO[tipo][0]
        return HB.get(self.aa, ("DA",))[0]

    def _hb_posible(self, tipo_mov, tipo_rival):
        a, b = self._papel_mio(tipo_mov), self._papel_rival(tipo_rival)
        return ("D" in a and "A" in b) or ("A" in a and "D" in b)

    def _mult_mov(self, mid):
        m = datos.MOVIMIENTOS[mid]
        mult, partes = datos.multiplicador(m["tipo"], self.tipos_salvaje())
        if m["tipo"] == datos.NEUTRO:
            return mult, partes
        nuevas = []
        for t, pm, texto in partes:
            if (m["tipo"], t) in INTERACCION_H and not self._hb_posible(m["tipo"], t):
                if m["tipo"] == "POL":
                    pm, texto = 0.5, "no se forma puente de H (falta donador o aceptor)"
                else:
                    pm, texto = 1, "ese grupo no puede formar puente de H con el tuyo"
            nuevas.append((t, pm, texto))
        total = 1.0
        for _, pm, _ in nuevas:
            total *= pm
        return total, nuevas

    # -------------------------------------------------------------- layout
    def layout(self):
        H, W = self.win.getmaxyx()
        amplio = W >= 110 and H >= 34
        x0 = SPRITE_W + 2
        libre = W - x0 - (SPRITE_W + 2 if amplio else 1)
        cw = min(libre, 92)
        x0 += (libre - cw) // 2 if amplio else 0
        ah = 10 if H >= 34 else (8 if H >= 28 else 6)
        nmov = len(self.movimientos())
        L = dict(W=W, H=H, amplio=amplio, x=x0, w=cw)
        L["rival"] = 1
        L["arena"] = 5
        L["ah"] = ah
        L["yo"] = 5 + ah
        L["movs"] = L["yo"] + 4
        L["nmov"] = nmov
        L["log"] = L["movs"] + nmov + 2
        sobra = L["log"] + 1 - (H - 1)
        if sobra > 0:
            # en terminales chicas la arena cede filas
            L["ah"] -= sobra
            for k in ("yo", "movs", "log"):
                L[k] -= sobra
        L["nlog"] = max(1, H - 1 - L["log"])
        return L

    # ------------------------------------------------------------- dibujo
    def dibujar(self):
        w = self.win
        w.erase()
        L = self.layout()
        x, cw = L["x"], L["w"]
        a = datos.AMINOACIDOS[self.aa]
        zona = datos.ZONAS[self.zona]["nombre"]
        d.put(w, 0, 1, f"¡Un aminoácido salvaje!  ·  {zona}  ·  turno {self.turno}",
              d.c("titulo", curses.A_BOLD))

        color = a["tipos"][0] if self.tipos_visible else "texto"
        d.estructura(w, 2, 1, datos.forma(self.aa)["arte"], d.c(color))

        d.caja(w, L["rival"], x, 4, cw, "Salvaje")
        y = L["rival"] + 1
        d.put(w, y, x + 2, self.nombre_salvaje(), d.c("texto", curses.A_BOLD))
        d.put(w, y, x + 17, f"Nv {self.salvaje['nivel']}", d.c("tenue"))
        if self.tipos_visible:
            d.etiqueta_tipos(w, y, x + 24, a["tipos"])
        else:
            d.put(w, y, x + 24, "[¿grupo?]  D: deducir", d.c("tenue"))
        y += 1
        d.put(w, y, x + 2, "Afinidad", d.c("texto"))
        listo = self.salvaje["afinidad"] >= AFINIDAD_TRNA
        ancho_barra = max(10, cw - 34)
        d.barra(w, y, x + 11, ancho_barra, self.salvaje["afinidad"], 100,
                d.c("bien" if listo else "agua"))
        d.put(w, y, x + 12 + ancho_barra, f"{int(self.salvaje['afinidad']):3d}/100", d.c("tenue"))
        if listo:
            d.put(w, y, x + 21 + ancho_barra, "¡[T] ARNt!", d.c("bien", curses.A_BOLD))

        d.caja(w, L["arena"], x, L["ah"], cw, None, d.c("oscuro"))
        anim.dibujar_cuadro(w, L["arena"] + 1, x + 1, L["ah"] - 2, cw - 2, self.cuadro)

        f = datos.forma(self.mon["id"])
        tipos = self.tipos_mio()
        d.caja(w, L["yo"], x, 4, cw, "Tu aminoácido")
        y = L["yo"] + 1
        d.put(w, y, x + 2, f["nombre"][:20], d.c("texto", curses.A_BOLD))
        d.put(w, y, x + 23, f"Nv {self.mon['nivel']}", d.c("tenue"))
        ancho_t = d.etiqueta_tipos(w, y, x + 30, tipos, corto=True)
        if self.estado["tipos_temp"]:
            d.put(w, y, x + 31 + ancho_t, f"({self.estado['turnos_temp']} t)", d.c("tenue"))
        y += 1
        emax = progreso.energia_max(self.mon)
        d.put(w, y, x + 2, "Energía", d.c("texto"))
        d.barra(w, y, x + 11, ancho_barra, self.mon["energia"], emax, d.c("titulo"))
        d.put(w, y, x + 12 + ancho_barra, f"{self.mon['energia']:3d}/{emax}", d.c("tenue"))
        d.put(w, y, x + 21 + ancho_barra, f"ATP {self.juego['objetos']['ATP']}", d.c("tenue"))

        d.caja(w, L["movs"], x, L["nmov"] + 2, cw, "Movimientos")
        for i, mid in enumerate(self.movimientos()):
            m = datos.MOVIMIENTOS[mid]
            yy = L["movs"] + 1 + i
            ok = self.disponible(mid)
            d.put(w, yy, x + 2, f"{i + 1}) {m['nombre'][:25]}", d.c("texto" if ok else "oscuro"))
            d.etiqueta_tipos(w, yy, x + 30, [m["tipo"]], corto=True)
            if not ok:
                d.put(w, yy, x + 41, "sin esa química ahora", d.c("oscuro"))
                continue
            if m["poder"] == 0:
                d.put(w, yy, x + 41, "—  efecto propio", d.c("tenue"))
                continue
            d.put(w, yy, x + 41, f"{m['poder']:>3}", d.c("tenue"))
            if m["tipo"] in tipos:
                d.put(w, yy, x + 45, "★", d.c("titulo"))
            if self.tipos_visible:
                mult, _ = self._mult_mov(mid)
                col = "bien" if mult >= 2 else "mal" if mult == 0 else "tenue" if mult < 1 else "texto"
                d.put(w, yy, x + 47, f"×{datos.fmt_mult(mult)} {flechas(mult)}",
                      d.c(col, curses.A_BOLD if mult != 1 else 0))
            else:
                d.put(w, yy, x + 47, "×?", d.c("tenue"))
        if cw >= 70:
            d.put(w, L["movs"], x + cw - 26, " ★ = tu grupo (×1.5) ", d.c("tenue"))

        lineas = self.log[-L["nlog"]:]
        for i, l in enumerate(lineas):
            ultimo = i == len(lineas) - 1
            d.put(w, L["log"] + i, x, ("› " + l)[:cw].ljust(cw), d.c("texto" if ultimo else "tenue"))
        # el registro se desplaza cada turno: se repintan esas filas completas
        w.redrawln(L["log"], L["nlog"])
        d.put(w, L["H"] - 1, 1, f"1-5 mover · T ARNt · D deducir · C cambiar · H huir · I info · "
                                f"M manual · V vel: {self.velocidad}", d.c("titulo"))

        if L["amplio"]:
            arte = f["arte"]
            xs = min(L["W"] - SPRITE_W - 1, x + cw + 3)
            yy = min(L["yo"], max(1, L["H"] - len(arte) - 2))
            d.put(w, yy, xs, f"tu {f['tres']}", d.c("tenue"))
            d.estructura(w, yy + 1, xs, arte, d.c(tipos[0]))
        w.refresh()

    # ------------------------------------------------------- animaciones
    def ctx_base(self, tipo_rival=None):
        tm = self.tipos_mio()
        ts = self.tipos_salvaje()
        tr = tipo_rival or ts[0]
        visible = self.nombre_visible or self.tipos_visible
        fid = self.mon["id"]
        mio = GRUPO.get(fid, ("─R", "R─"))[0]
        if fid == "H" and self.estado["his_neutra"]:
            mio = "─imidazol"
        rival = GRUPO[self.aa][1] if visible else "R?─"
        return dict(
            mio=mio, rival=rival,
            color_mio=tm[0], color_rival=tr if self.tipos_visible else "texto",
            carga_mio="+" if "POS" in tm else "−" if "NEG" in tm else "δ",
            carga_rival="+" if "POS" in ts else "−" if "NEG" in ts else "δ",
            tres=datos.forma(fid)["tres"],
        )

    def animar(self, nombre, ctx, veredicto=None):
        L = self.layout()
        self.dibujar()
        self.cuadro = anim.reproducir(self.win, L["arena"] + 1, L["x"] + 1,
                                      L["ah"] - 2, L["w"] - 2, nombre, ctx, self.velocidad)
        if veredicto:
            texto, color = veredicto
            self.cuadro = self.cuadro + [(0, L["w"] - 3 - len(texto), texto, color)]

    def animacion_interaccion(self, mid, partes):
        """Elige la animación según la interacción física que de verdad ocurre."""
        m = datos.MOVIMIENTOS[mid]
        T = m["tipo"]
        if T == datos.NEUTRO:
            nombre = {"puente_h_esqueleto": "esqueleto", "lamina_beta": "lamina",
                      "triple_helice": "esqueleto_triple"}.get(mid, "vdw")
            return nombre, self.ctx_base()
        if mid == "puente_disulfuro" and self.aa == "C":
            return "disulfuro", self.ctx_base()
        if mid == "entrecruzar":
            return "enlace", self.ctx_base()
        if any(pm == 0 for _, pm, _ in partes):
            return "repulsion", self.ctx_base()
        rt = max(partes, key=lambda p: p[1])[0]
        ctx = self.ctx_base(rt)
        par = (T, rt)
        if par in (("NP", "NP"), ("NP", "ARO"), ("ARO", "NP")):
            return "hidrofobico", ctx
        if par == ("ARO", "ARO"):
            return "pi", ctx
        if par in (("ARO", "POS"), ("POS", "ARO")):
            mio_cat = T == "POS"
            ctx.update(cation=(ctx["mio"].lstrip("─") if mio_cat else ctx["rival"].rstrip("─")),
                       color_cation=ctx["color_mio"] if mio_cat else ctx["color_rival"],
                       color_anillo=ctx["color_rival"] if mio_cat else ctx["color_mio"])
            return "cation_pi", ctx
        if par in (("POS", "NEG"), ("NEG", "POS")):
            return "salino", ctx
        if par in (("POL", "ARO"), ("ARO", "POL")):
            if T == "POL":
                don = HB.get(self.mon["id"], ("DA", "─X─H"))[1].lstrip("─")
                ctx.update(donador_txt=don, color_donador=ctx["color_mio"],
                           color_anillo=ctx["color_rival"])
            else:
                don = HB.get(self.aa, ("DA", "", "", "H─X─"))[3]
                ctx.update(donador_txt=don, color_donador=ctx["color_rival"],
                           color_anillo=ctx["color_mio"])
            return "oh_pi", ctx
        if par in INTERACCION_H:
            return self._ctx_puente_h(T, rt, ctx)
        # no polar o anión frente a un grupo polar/cargado: el agua los separa
        ctx["polar_lado"] = "der" if rt in ("POL", "POS", "NEG") else "izq"
        return "solvatacion", ctx

    def _ctx_puente_h(self, T, rt, ctx):
        papel_m = self._papel_mio(T)
        papel_r = self._papel_rival(rt)
        relleno = ("DA", "─X─H", "─X:", "H─X─", ":X─")
        if T in CARGADO:
            mio_d = mio_a = CARGADO[T][1]
        else:
            fila = HB.get(self.mon["id"], relleno)
            mio_d, mio_a = fila[1], fila[2] or fila[1]
        if rt in CARGADO:
            riv_d = riv_a = CARGADO[rt][2]
        else:
            fila = HB.get(self.aa, relleno)
            riv_d, riv_a = fila[3], fila[4] or fila[3]
        if "D" in papel_m and "A" in papel_r:
            ctx.update(hb_izq=mio_d, hb_der=riv_a, donador="izq")
            return "puente_h", ctx
        if "A" in papel_m and "D" in papel_r:
            ctx.update(hb_izq=mio_a, hb_der=riv_d, donador="der")
            return "puente_h", ctx
        motivo = "los dos solo pueden donar H" if "D" in papel_m else "los dos solo pueden aceptar H"
        ctx.update(hb_izq=mio_d, hb_der=riv_d, motivo=motivo)
        return "sin_puente_h", ctx

    def sacudir_salvaje(self):
        a = datos.AMINOACIDOS[self.aa]
        color = a["tipos"][0] if self.tipos_visible else "texto"
        anim.sacudir(self.win, 2, 1, datos.forma(self.aa)["arte"], color)

    # ---------------------------------------------------------- acciones
    def usar(self, mid):
        """Devuelve False si el movimiento no se pudo usar (no gasta turno)."""
        m = datos.MOVIMIENTOS[mid]
        f = datos.forma(self.mon["id"])
        e = self.estado
        efecto = m["efecto"]
        if not self.disponible(mid):
            self.decir(f"{f['nombre']} no puede usar {m['nombre']}: ahora es "
                       f"{datos.nombre_tipos(self.tipos_mio())}, no "
                       f"{datos.TIPOS[m['tipo']]['nombre']}.")
            return False
        tipo_txt = datos.TIPOS[m["tipo"]]["nombre"] if m["tipo"] in datos.TIPOS else "Neutro"
        self.decir(f"{f['nombre']} usa {m['nombre']} [{tipo_txt}].")

        # --- efectos sobre tu propio aminoácido
        if efecto == "fosforilar":
            if self.juego["objetos"]["ATP"] < 1:
                self.decir("¡Sin ATP! La quinasa necesita ATP como donador de fosforilo.")
                return True
            self.juego["objetos"]["ATP"] -= 1
            nuevos = ("NEG", "ARO") if "ARO" in self.tipos_mio() else ("NEG",)
            e["tipos_temp"], e["turnos_temp"] = nuevos, 3
            e["extra"] = ["fosfato"]
            self.animar("fosforilar", self.ctx_base())
            self.decir(f"Gana un fosfato (≈ −2): ahora es {datos.nombre_tipos(nuevos)} "
                       "y puede usar «Fosfato (−2)».")
            return True
        if efecto == "acetilar":
            e["tipos_temp"], e["turnos_temp"] = ("POL",), 3
            e["extra"] = ["abrir_cromatina"]
            self.animar("acetilar", self.ctx_base())
            self.decir("Pierde su carga +: ahora es Polar sin carga (ya no hace puentes salinos).")
            return True
        if efecto == "ph":
            ctx = self.ctx_base()
            if not e["his_neutra"]:
                e["his_neutra"] = True
                e["tipos_temp"], e["turnos_temp"] = ("POL",), 3
                e["extra"] = ["imidazol_h"]
                ctx["ph_destino"] = 7.4
                self.animar("ph", ctx)
                self.decir("pH 7.4 > pKR 6: el imidazol suelta su H+ (neutro: Polar sin carga).")
            else:
                e["his_neutra"] = False
                e["tipos_temp"], e["turnos_temp"], e["extra"] = None, 0, []
                ctx["ph_destino"] = 5
                self.animar("ph", ctx)
                self.decir("pH 5 < pKR 6: el imidazol se protona (Cargado +).")
            return True
        if efecto == "revelar":
            ts = self.tipos_salvaje()
            polar = any(t in ("POL", "POS", "NEG") for t in ts)
            nombre = datos.AMINOACIDOS[self.aa]["nombre"]
            ctx = self.ctx_base()
            ctx["lambda"] = 350 if polar else 330
            ctx["revelado"] = f"vecino {'polar' if polar else 'no polar'}: es {nombre}"
            self.animar("fluorescencia", ctx)
            self.nombre_visible = self.tipos_visible = True
            self.decir(f"Emisión a ~{ctx['lambda']} nm: entorno {'polar' if polar else 'no polar'}. "
                       f"¡Es {nombre} ({datos.nombre_tipos(ts)})!")
            return True
        if m["poder"] == 0:
            self.animar(m["anim"], self.ctx_base())
            if efecto == "esquiva":
                e["esquiva"] = True
                self.decir("Su esqueleto flexible esquivará la próxima agitación.")
            elif efecto == "potenciar":
                e["potenciar"] = True
                self.decir("Tu siguiente movimiento vale ×1.5.")
            elif efecto in ("escudo2", "escudo3"):
                e["escudo"] = 2 if efecto == "escudo2" else 3
                self.decir(f"Se estabiliza: recibirá la mitad de agitación {e['escudo']} turnos.")
            return True

        # --- interacción con el rival
        mult, partes = self._mult_mov(mid)
        stab = 1.5 if m["tipo"] in self.tipos_mio() else 1.0
        extra = 1.0
        if e["potenciar"]:
            extra = 1.5
            e["potenciar"] = False

        nombre_anim, ctx = self.animacion_interaccion(mid, partes)
        principal = max(partes, key=lambda p: p[1])[2] if partes else "interacción"
        if any(pm == 0 for _, pm, _ in partes):
            principal = next(tx for _, pm, tx in partes if pm == 0)
        texto_m = f"×{datos.fmt_mult(mult)} {flechas(mult)}".strip()
        ctx["nombre"] = f"{principal} ({texto_m})"
        color_v = "bien" if mult >= 2 else "mal" if mult == 0 else "tenue" if mult < 1 else "texto"
        self.animar(nombre_anim, ctx, (texto_m, color_v))

        if efecto == "disulfuro":
            if self.aa == "C":
                self.salvaje["afinidad"] = 100
                self.ultimo_mult = 2.0
                self.decir("¡Enlace covalente S–S entre las dos Cys! Afinidad al máximo.")
                progreso.dar_xp(self.mon, 3)
                return True
            self.decir("Sin otra Cys no hay disulfuro: solo actúa como tiol polar.")

        factor = (1 + self.mon["nivel"] / 8) * (1 - min(0.4, self.salvaje["nivel"] / 30))
        ganancia = m["poder"] * 0.32 * mult * stab * extra * factor * random.uniform(0.85, 1.15)
        self.salvaje["afinidad"] = min(100, self.salvaje["afinidad"] + ganancia)
        self.ultimo_mult = mult

        if len(partes) > 1 and self.tipos_visible:
            desglose = " · ".join(f"{datos.TIPOS[t]['corto']} ×{datos.fmt_mult(pm)}"
                                  for t, pm, _ in partes)
            self.decir(f"{principal[:1].upper() + principal[1:]}: {desglose} → ×{datos.fmt_mult(mult)}"
                       + (" · ★×1.5" if stab > 1 else ""))
        else:
            self.decir(f"{principal[:1].upper() + principal[1:]} (×{datos.fmt_mult(mult)})"
                       + (" · ★ tu grupo ×1.5" if stab > 1 else ""))
        if mult == 0:
            self.decir("¡No hay afinidad: se repelen!")
        elif mult >= 2:
            self.decir(f"¡Súper afín! +{int(ganancia)} de afinidad")
            self.sacudir_salvaje()
            for msg in progreso.dar_xp(self.mon, 3):
                self.decir(msg)
        else:
            self.decir(f"+{int(ganancia)} de afinidad" + ("  (poco afín)" if mult < 1 else ""))
        if efecto in ("escudo2", "escudo3"):
            e["escudo"] = 2 if efecto == "escudo2" else 3
            self.decir(f"Además se estabiliza: mitad de agitación {e['escudo']} turnos.")
        return True

    def turno_salvaje(self):
        """Devuelve 'huyo' si el salvaje escapa."""
        s, e = self.salvaje, self.estado
        nombre = self.nombre_salvaje()
        resultado = None
        if s["aturdido"]:
            s["aturdido"] = False
            self.decir(f"{nombre} pierde su turno.")
        elif self.ultimo_mult == 0 and random.random() < 0.35:
            self.decir(f"La repulsión empuja a {nombre} lejos… ¡se escapó!")
            resultado = "huyo"
        else:
            dano = random.randint(3, 6) + s["nivel"]
            if e["esquiva"]:
                e["esquiva"] = False
                self.decir(f"{nombre} se agita, pero tu aminoácido lo esquiva.")
                dano = 0
            elif e["escudo"] > 0:
                dano //= 2
            if dano:
                self.animar("agitacion", self.ctx_base())
                self.mon["energia"] = max(0, self.mon["energia"] - dano)
                self.decir(f"Agitación térmica de {nombre}: −{dano} de energía.")
            if s["afinidad"] > 0 and random.random() < 0.2:
                s["afinidad"] = max(0, s["afinidad"] - 6)
                self.decir(f"{nombre} se desordena un poco (−6 afinidad).")
        if e["escudo"] > 0:
            e["escudo"] -= 1
        if e["tipos_temp"]:
            e["turnos_temp"] -= 1
            if e["turnos_temp"] <= 0:
                e["tipos_temp"], e["extra"], e["his_neutra"] = None, [], False
                self.decir("El efecto temporal terminó: vuelve a su grupo original.")
        self.turno += 1
        return resultado

    def tras_mi_turno(self):
        self.turnos_jugador += 1
        if not self.tipos_visible and self.turnos_jugador >= TURNOS_PARA_REVELAR:
            self.tipos_visible = True
            self.decir(f"Ya observaste bastante su química: es "
                       f"{datos.nombre_tipos(self.tipos_salvaje())}.")

    def deducir(self):
        """Adivinar el grupo del salvaje. Devuelve True si gastó el turno."""
        if self.tipos_visible:
            self.decir("Ya conoces su grupo.")
            return False
        nombres = [datos.TIPOS[t]["nombre"] for t in datos.ORDEN_TIPOS]
        p = d.menu(self.win, "¿Grupo de Lehninger?", nombres,
                   ayuda="¿Solo C/H? ¿anillo? ¿OH/SH/amida? ¿NH₃⁺? ¿COO⁻?")
        if p is None:
            return False
        elegidos = (datos.ORDEN_TIPOS[p],)
        if elegidos == ("ARO",):
            s = d.menu(self.win, "¿Y su carácter?", ["Más no polar (sin OH ni N–H)",
                                                     "Algo polar (tiene OH o N–H)"])
            if s is None:
                return False
            elegidos = ("ARO", "NP" if s == 0 else "POL")
        self.tipos_visible = True
        if set(elegidos) == set(self.tipos_salvaje()):
            self.salvaje["afinidad"] = min(100, self.salvaje["afinidad"] + 10)
            msgs = progreso.dar_xp(self.mon, 5)
            self.decir(f"¡Correcto! {datos.nombre_tipos(self.tipos_salvaje())}. +10 afinidad, +5 XP")
            for msg in msgs:
                self.decir(msg)
            return False      # acertar no gasta el turno
        self.decir(f"No. Era {datos.nombre_tipos(self.tipos_salvaje())}. Pierdes el turno.")
        return True

    def cambiar(self, forzado=False):
        equipo = self.juego["equipo"]
        opciones, indices = [], []
        for i, m in enumerate(equipo):
            if i == self.activo or m["energia"] <= 0:
                continue
            f = datos.forma(m["id"])
            opciones.append(f"{f['nombre']:<20} Nv{m['nivel']:>2}  "
                            f"{datos.nombre_tipos(f['tipos'], corto=True):<17} E {m['energia']}")
            indices.append(i)
        if not opciones:
            return False
        while True:
            sel = d.menu(self.win, "¿Quién entra?", opciones)
            if sel is not None:
                break
            if not forzado:
                return False
        self.activo = indices[sel]
        self._reiniciar_estado()
        self.decir(f"¡Adelante, {datos.forma(self.mon['id'])['nombre']}!")
        return True

    def lanzar_trna(self):
        """Devuelve 'capturado', 'huyo' o None."""
        if self.salvaje["afinidad"] < AFINIDAD_TRNA:
            self.decir(f"El ARNt no se une: la afinidad debe ser ≥ {AFINIDAD_TRNA}.")
            return None
        self.dibujar()
        L = self.layout()
        tipo = preguntas.elegir_tipo(self.juego, self.aa)
        bien = preguntas.preguntar(self.win, self.juego, self.aa, tipo,
                                   L["arena"], L["x"], L["w"])
        a = datos.AMINOACIDOS[self.aa]
        if bien:
            self.nombre_visible = self.tipos_visible = True
            ctx = self.ctx_base()
            ctx["codon"] = random.choice(a["codones"])
            ctx["tres"] = a["tres"]
            ctx["color_rival"] = a["tipos"][0]
            self.animar("trna", ctx)
            progreso.capturar(self.juego, self.aa, self.salvaje["nivel"])
            msgs = progreso.dar_xp(self.mon, 15)
            texto = (f"¡{a['nombre']} ({a['tres']}, {self.aa}) fue capturado y se "
                     f"une a tu equipo!\n\nGrupo: {datos.nombre_tipos(a['tipos'])}\n"
                     f"Su ficha completa ya está en la Aminodex [X].")
            if msgs:
                texto += "\n\n" + "\n".join(msgs)
            d.popup(self.win, texto, "¡Capturado!", attr=d.c("bien"))
            return "capturado"
        self.salvaje["afinidad"] = max(0, self.salvaje["afinidad"] - 20)
        self.decir("El ARNt se suelta (−20 afinidad).")
        if random.random() < 0.3:
            self.decir(f"{self.nombre_salvaje()} aprovechó para escapar.")
            return "huyo"
        return self.turno_salvaje()

    def info(self):
        lineas = [f"Tu grupo ahora: {datos.nombre_tipos(self.tipos_mio())}. Los movimientos "
                  "de tu mismo grupo (★) valen ×1.5; los de un grupo que no tienes no se "
                  "pueden usar.", ""]
        for i, mid in enumerate(self.movimientos()):
            m = datos.MOVIMIENTOS[mid]
            tipo = datos.TIPOS[m["tipo"]]["nombre"] if m["tipo"] in datos.TIPOS else "Neutro"
            mult = ""
            if self.tipos_visible and m["poder"] > 0 and self.disponible(mid):
                mult = f"  → ×{datos.fmt_mult(self._mult_mov(mid)[0])} contra el rival"
            lineas.append(f"{i + 1}) {m['nombre']} [{tipo}] poder {m['poder']}{mult}")
            lineas.append(f"   {m['desc']}")
            if m.get("ciencia"):
                lineas.append(f"   ↳ {m['ciencia']}")
        d.popup(self.win, "\n".join(lineas),
                f"Movimientos de {datos.forma(self.mon['id'])['nombre']}", ancho=86)

    # -------------------------------------------------------------- bucle
    def jugar(self):
        if self.activo is None:
            return "derrota"
        self.decir("Observa la estructura: ¿de qué grupo es? D para deducir, 1-5 para interactuar.")
        while True:
            self.dibujar()
            k = d.tecla(self.win)
            resultado = None
            movs = self.movimientos()
            if isinstance(k, str) and k.isdigit() and 1 <= int(k) <= len(movs):
                if self.usar(movs[int(k) - 1]):
                    self.tras_mi_turno()
                    resultado = self.turno_salvaje()
            elif d.es(k, "t"):
                resultado = self.lanzar_trna()
                if resultado == "capturado":
                    return resultado
            elif d.es(k, "d"):
                if self.deducir():
                    resultado = self.turno_salvaje()
            elif d.es(k, "c"):
                if self.cambiar():
                    resultado = self.turno_salvaje()
            elif d.es(k, "h"):
                if random.random() < 0.8:
                    return "huiste"
                self.decir("¡No pudiste escapar!")
                resultado = self.turno_salvaje()
            elif d.es(k, "v"):
                i = anim.ORDEN_VEL.index(self.velocidad)
                self.juego["ajustes"]["velocidad"] = anim.ORDEN_VEL[(i + 1) % len(anim.ORDEN_VEL)]
                self.decir(f"Velocidad de animación: {self.velocidad}.")
            elif d.es(k, "m", "?"):
                tipos = self.tipos_salvaje() if self.tipos_visible else None
                manual.mostrar(self.win, self.juego, "afinidad", rival=tipos)
            elif d.es(k, "i"):
                self.info()
            if resultado == "huyo":
                self.dibujar()
                d.popup(self.win, f"{self.nombre_salvaje()} se escapó.", "Combate")
                return "huyo"
            if self.mon["energia"] <= 0:
                nombre = datos.forma(self.mon["id"])["nombre"]
                self.decir(f"¡{nombre} se desnaturalizó!")
                self.dibujar()
                if not self.cambiar(forzado=True):
                    return "derrota"


def combate(win, juego, aa, nivel, zona):
    return Combate(win, juego, aa, nivel, zona).jugar()
