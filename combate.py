"""Combate por turnos: subir la afinidad del salvaje y capturarlo con un ARNt."""

import curses
import random

import animaciones as anim
import datos
import dibujo as d
import manual
import preguntas
import progreso
from idioma import tr

AFINIDAD_TRNA = 50
TURNOS_PARA_REVELAR = 3
SPRITE_W = 24

# Grupo químico de la cadena lateral, escrito para el lado izquierdo (─X) y
# para el derecho (X─) de la arena.
GRUPO = {
    "G": ("─H", "H─"), "A": ("─CH₃", "H₃C─"), "V": ("─CH(CH₃)₂", "(H₃C)₂CH─"),
    "L": ("─CH₂CH(CH₃)₂", "(H₃C)₂CHCH₂─"), "I": ("─CH(CH₃)C₂H₅", "H₅C₂(H₃C)CH─"),
    "M": ("─CH₂CH₂SCH₃", "H₃CSCH₂CH₂─"), "P": (tr("─pirrolidina"), tr("pirrolidina─")),
    "F": (tr("─CH₂─fenilo"), tr("fenilo─CH₂─")), "Y": (tr("─fenol─OH"), tr("HO─fenol─")),
    "W": (tr("─indol(N─H)"), tr("(H─N)indol─")), "S": ("─CH₂─OH", "HO─CH₂─"),
    "T": ("─CH(CH₃)OH", "HO(H₃C)CH─"), "C": ("─CH₂─SH", "HS─CH₂─"),
    "N": ("─CONH₂", "H₂NOC─"), "Q": ("─CH₂CONH₂", "H₂NOCCH₂─"),
    "D": ("─COO⁻", "⁻OOC─"), "E": ("─CH₂COO⁻", "⁻OOCCH₂─"),
    "K": ("─NH₃⁺", "⁺H₃N─"), "R": (tr("─guanidinio⁺"), tr("⁺guanidinio─")),
    "H": (tr("─imidazol(H⁺)"), tr("(H⁺)imidazol─")),
    "Hyp": (tr("─pirrolidina─OH"), tr("HO─pirrolidina─")), "Hyl": ("─NH₃⁺", "⁺H₃N─"),
    "Kac": ("─NH─COCH₃", "H₃COC─NH─"), "Kme3": ("─N⁺(CH₃)₃", "(H₃C)₃N⁺─"),
    "pS": ("─O─PO₃²⁻", "²⁻O₃P─O─"), "pT": ("─O─PO₃²⁻", "²⁻O₃P─O─"),
    "pY": (tr("─fenil─O─PO₃²⁻"), tr("²⁻O₃P─O─fenil─")), "Cis": ("─S─S─", "─S─S─"),
    "Gla": ("─CH(COO⁻)₂", "(⁻OOC)₂CH─"), "Nglc": (tr("─CONH─glicano"), tr("glicano─HNOC─")),
    "Cit": ("─NH─CO─NH₂", "H₂N─OC─NH─"),
    "gS": ("─CH₂─O─GalNAc", "GalNAc─O─CH₂─"), "gT": ("─CH(CH₃)─O─GalNAc", "GalNAc─O─CH─"),
}

# Puentes de H: papel del grupo polar (D = donador, A = aceptor) y cómo se
# escribe con el átomo que participa pegado a la línea de puntos.
#            papel  donador_izq   aceptor_izq    donador_der    aceptor_der
HB = {
    "S": ("DA", "─O─H", "─(H)O:", "H─O─", ":O(H)─"),
    "T": ("DA", "─O─H", "─(H)O:", "H─O─", ":O(H)─"),
    "Y": ("DA", tr("─fenol─O─H"), tr("─fenol(H)O:"), tr("H─O─fenol─"), tr(":O(H)─fenol─")),
    "W": ("D", tr("─indol─N─H"), None, tr("H─N─indol─"), None),
    "N": ("DA", "─CON(H)─H", "─(H₂N)C═O:", "H─N(H)OC─", ":O═C(NH₂)─"),
    "Q": ("DA", "─CON(H)─H", "─(H₂N)C═O:", "H─N(H)OC─", ":O═C(NH₂)─"),
    "C": ("DA", "─S─H", "─(H)S:", "H─S─", ":S(H)─"),
    "Hyp": ("DA", "─O─H", "─(H)O:", "H─O─", ":O(H)─"),
    "Kac": ("DA", "─N(Ac)─H", "─(HN)C═O:", "H─N(Ac)─", ":O═C(NH)─"),
    "Nglc": ("DA", "─CON(H)─H", "─(HN)C═O:", "H─N(H)OC─", ":O═C(NH)─"),
    "Cit": ("DA", "─CON(H)─H", "─(H₂N)C═O:", "H─N(H)OC─", ":O═C(NH₂)─"),
    "gS": ("DA", "─GalNAc─O─H", "─GalNAc(H)O:", "H─O─GalNAc─", ":O(H)GalNAc─"),
    "gT": ("DA", "─GalNAc─O─H", "─GalNAc(H)O:", "H─O─GalNAc─", ":O(H)GalNAc─"),
    "H": ("DA", tr("─imidazol─N─H"), tr("─imidazol─N:"), tr("H─N─imidazol─"), tr(":N─imidazol─")),
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
        self.salvaje = dict(nivel=nivel, afinidad=0)
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
        pass

    @property
    def mon(self):
        return self.juego["equipo"][self.activo]

    def tipos_mio(self):
        return datos.forma(self.mon["id"])["tipos"]

    def tipos_salvaje(self):
        return datos.AMINOACIDOS[self.aa]["tipos"]

    def nombre_salvaje(self):
        return datos.AMINOACIDOS[self.aa]["nombre"] if self.nombre_visible else tr("¿¿??")

    def movimientos(self):
        return datos.forma(self.mon["id"])["movs"]

    def decir(self, texto):
        self.log.append(texto)
        self.log = self.log[-8:]

    @property
    def velocidad(self):
        return self.juego["ajustes"]["velocidad"]

    # ------------------------------------------------------ química real
    def _papel_mio(self, tipo_mov):
        if self.mon["id"] == "Kme3":
            return ""            # N⁺(CH₃)₃: sin H que donar ni par libre
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
        if m["efecto"] == "disulfuro":
            if self.aa == "C":
                return 2.0, [("POL", 2, tr("puente disulfuro (covalente)"))]
            return 0.0, [(self.tipos_salvaje()[0], 0, tr("sin otra Cys no hay disulfuro"))]
        mult, partes = datos.multiplicador(m["tipo"], self.tipos_salvaje())
        if m["tipo"] == datos.NEUTRO:
            texto = tr("puente de H del esqueleto") if mid == "puente_h_esqueleto" else "van der Waals"
            return mult, [(t, pm, texto) for t, pm, _ in partes]
        nuevas = []
        for t, pm, texto in partes:
            if (m["tipo"], t) in INTERACCION_H and not self._hb_posible(m["tipo"], t):
                if m["tipo"] == "POL":
                    pm, texto = 0.5, tr("sin puente de H (falta donador/aceptor)")
                else:
                    pm, texto = 1, tr("atracción ion–dipolo")
            nuevas.append((t, pm, texto))
        total = 1.0
        for _, pm, _ in nuevas:
            total *= pm
        return total, nuevas

    @staticmethod
    def _interaccion_principal(partes):
        if any(pm == 0 for _, pm, _ in partes):
            return next(tx for _, pm, tx in partes if pm == 0)
        return max(partes, key=lambda p: p[1])[2] if partes else tr("interacción")

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
        d.put(w, 0, 1, tr("Aminoácido salvaje  ·  {zona}  ·  turno {n}", zona=zona, n=self.turno),
              d.c("titulo", curses.A_BOLD))

        color = a["tipos"][0] if self.tipos_visible else "texto"
        d.estructura(w, 2, 1, datos.forma(self.aa)["arte"], d.c(color))

        d.caja(w, L["rival"], x, 4, cw, tr("Salvaje"))
        y = L["rival"] + 1
        d.put(w, y, x + 2, self.nombre_salvaje(), d.c("texto", curses.A_BOLD))
        d.put(w, y, x + 17, tr("Nv {n}", n=self.salvaje["nivel"]), d.c("tenue"))
        if self.tipos_visible:
            # con recuadros angostos los nombres largos de dos tipos no caben
            d.etiqueta_tipos(w, y, x + 24, a["tipos"], corto=cw < 64)
        else:
            d.put(w, y, x + 24, tr("[¿grupo?]  D: deducir"), d.c("tenue"))
        y += 1
        d.put(w, y, x + 2, tr("Afinidad"), d.c("texto"))
        listo = self.salvaje["afinidad"] >= AFINIDAD_TRNA
        # etiqueta(11) + barra + número(9) + "listo: [T] ARNt"(15) + borde(2)
        ancho_barra = max(10, cw - 38)
        d.barra(w, y, x + 11, ancho_barra, self.salvaje["afinidad"], 100,
                d.c("bien" if listo else "agua"))
        d.put(w, y, x + 12 + ancho_barra, f"{int(self.salvaje['afinidad']):3d}/100", d.c("tenue"))
        if listo:
            aviso = tr("listo: [T] ARNt") if cw - 23 - ancho_barra >= 15 else tr("[T] ARNt")
            d.put(w, y, x + 21 + ancho_barra, aviso, d.c("bien", curses.A_BOLD))

        d.caja(w, L["arena"], x, L["ah"], cw, None, d.c("oscuro"))
        anim.dibujar_cuadro(w, L["arena"] + 1, x + 1, L["ah"] - 2, cw - 2, self.cuadro)

        f = datos.forma(self.mon["id"])
        tipos = self.tipos_mio()
        d.caja(w, L["yo"], x, 4, cw, tr("Tu aminoácido"))
        y = L["yo"] + 1
        d.put(w, y, x + 2, f["nombre"][:20], d.c("texto", curses.A_BOLD))
        d.put(w, y, x + 23, tr("Nv {n}", n=self.mon["nivel"]), d.c("tenue"))
        d.etiqueta_tipos(w, y, x + 30, tipos, corto=True)
        y += 1
        emax = progreso.energia_max(self.mon)
        d.put(w, y, x + 2, tr("Energía"), d.c("texto"))
        d.barra(w, y, x + 11, ancho_barra, self.mon["energia"], emax, d.c("titulo"))
        d.put(w, y, x + 12 + ancho_barra, f"{self.mon['energia']:3d}/{emax}", d.c("tenue"))
        d.put(w, y, x + 21 + ancho_barra, f"ATP {self.juego['objetos']['ATP']}", d.c("tenue"))

        d.caja(w, L["movs"], x, L["nmov"] + 2, cw, tr("Interacciones"))
        con_chip = cw >= 90       # si no cabe la etiqueta, el color del nombre indica el grupo
        filas = []
        for i, mid in enumerate(self.movimientos()):
            m = datos.MOVIMIENTOS[mid]
            nombre_t = datos.TIPOS[m["tipo"]]["corto"] if m["tipo"] in datos.TIPOS else tr("Neutro")
            fila = [(f"{i + 1}) {m['nombre']}", "texto" if con_chip else m["tipo"])]
            if con_chip:
                fila.append((f" {nombre_t} ", m["tipo"], curses.A_BOLD | curses.A_REVERSE))
            fila.append((f"{m['poder']:>3}", "tenue"))
            if self.tipos_visible:
                mult, partes = self._mult_mov(mid)
                col = "bien" if mult >= 2 else "mal" if mult == 0 else "tenue" if mult < 1 else "texto"
                fila.append((f"×{datos.fmt_mult(mult)} {flechas(mult)}", col,
                             curses.A_BOLD if mult != 1 else 0))
                fila.append((self._interaccion_principal(partes), "tenue"))
            else:
                fila.append(("×?", "tenue"))
            filas.append(fila)
        filas = d.alinear(filas)
        for fila in filas:
            # la última columna (la interacción concreta) se recorta al ancho del recuadro
            usado = sum(len(celda[0]) for celda in fila[:-1])
            libre = cw - 4 - usado
            ultima = fila[-1]
            if self.tipos_visible and libre < 16:
                fila.pop()                     # no cabe: se ve en el registro y con [I]
            elif len(ultima[0]) > libre:
                fila[-1] = (ultima[0][: max(0, libre - 1)] + "…",) + tuple(ultima[1:])
        for i, fila in enumerate(filas):
            d.fila_tabla(w, L["movs"] + 1 + i, x + 2, fila)

        lineas = self.log[-L["nlog"]:]
        for i, l in enumerate(lineas):
            ultimo = i == len(lineas) - 1
            d.put(w, L["log"] + i, x, ("› " + l)[:cw].ljust(cw), d.c("texto" if ultimo else "tenue"))
        # el registro se desplaza cada turno: se repintan esas filas completas
        w.redrawln(L["log"], L["nlog"])
        if L["W"] >= 100:
            pie = tr("1-5 mover · T ARNt · D deducir · C cambiar · H huir · I info · "
                     "M manual · V velocidad: {vel}", vel=tr(self.velocidad))
        else:
            pie = tr("1-5 mover  T ARNt  D deducir  C cambiar  H huir  I info  M manual  V {vel}",
                     vel=tr(self.velocidad))
        d.put(w, L["H"] - 1, 1, pie, d.c("titulo"))

        if L["amplio"]:
            arte = f["arte"]
            xs = min(L["W"] - SPRITE_W - 1, x + cw + 3)
            yy = min(L["yo"], max(1, L["H"] - len(arte) - 2))
            d.put(w, yy, xs, tr("tu {tres}", tres=f["tres"]), d.c("tenue"))
            d.estructura(w, yy + 1, xs, arte, d.c(tipos[0]))
        w.refresh()

    # ------------------------------------------------------- animaciones
    def ctx_base(self, tipo_rival=None):
        tm = self.tipos_mio()
        ts = self.tipos_salvaje()
        t_rival = tipo_rival or ts[0]
        visible = self.nombre_visible or self.tipos_visible
        fid = self.mon["id"]
        mio = GRUPO.get(fid, ("─R", "R─"))[0]
        rival = GRUPO[self.aa][1] if visible else "R?─"
        return dict(
            mio=mio, rival=rival,
            color_mio=tm[0], color_rival=t_rival if self.tipos_visible else "texto",
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
            if T in CARGADO and not self._hb_posible(T, rt):
                return "vdw", ctx          # solo atracción ion–dipolo
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
        motivo = tr("los dos solo pueden donar H") if "D" in papel_m else tr("los dos solo pueden aceptar H")
        ctx.update(hb_izq=mio_d, hb_der=riv_d, motivo=motivo)
        return "sin_puente_h", ctx

    def sacudir_salvaje(self):
        a = datos.AMINOACIDOS[self.aa]
        color = a["tipos"][0] if self.tipos_visible else "texto"
        anim.sacudir(self.win, 2, 1, datos.forma(self.aa)["arte"], color)

    # ---------------------------------------------------------- acciones
    def usar(self, mid):
        """Forma la interacción con el rival."""
        m = datos.MOVIMIENTOS[mid]
        f = datos.forma(self.mon["id"])
        self.decir(f"{f['nombre']}: {m['nombre']}.")
        mult, partes = self._mult_mov(mid)
        principal = self._interaccion_principal(partes)
        texto_m = f"×{datos.fmt_mult(mult)} {flechas(mult)}".strip()

        if m["efecto"] == "disulfuro" and self.aa != "C":
            self.animar("sin_puente_h", dict(self.ctx_base(), hb_izq="─CH₂─S─H",
                                             hb_der=GRUPO[self.aa][1] if self.nombre_visible else "R?─",
                                             motivo=tr("el disulfuro solo se forma entre dos Cys"),
                                             nombre=tr("sin otra Cys no hay disulfuro")))
            self.decir(tr("Sin otra Cys no hay disulfuro: no se forma ninguna interacción."))
            self.ultimo_mult = 1.0
            return

        nombre_anim, ctx = self.animacion_interaccion(mid, partes)
        ctx["nombre"] = f"{principal} ({texto_m})"
        color_v = "bien" if mult >= 2 else "mal" if mult == 0 else "tenue" if mult < 1 else "texto"
        self.animar(nombre_anim, ctx, (texto_m, color_v))

        if m["efecto"] == "disulfuro":
            self.salvaje["afinidad"] = 100
            self.ultimo_mult = 2.0
            self.decir(tr("Enlace covalente S–S entre las dos Cys: afinidad máxima."))
            progreso.dar_xp(self.mon, 3)
            return

        factor = (1 + self.mon["nivel"] / 8) * (1 - min(0.4, self.salvaje["nivel"] / 30))
        ganancia = m["poder"] * 0.45 * mult * factor * random.uniform(0.85, 1.15)
        self.salvaje["afinidad"] = min(100, self.salvaje["afinidad"] + ganancia)
        self.ultimo_mult = mult

        if len(partes) > 1 and self.tipos_visible:
            desglose = " · ".join(f"{datos.TIPOS[t]['corto']} ×{datos.fmt_mult(pm)}"
                                  for t, pm, _ in partes)
            self.decir(f"{principal[:1].upper() + principal[1:]}: {desglose} → ×{datos.fmt_mult(mult)}")
        else:
            self.decir(f"{principal[:1].upper() + principal[1:]} (×{datos.fmt_mult(mult)})")
        if mult == 0:
            self.decir(tr("Sin afinidad: se repelen."))
        elif mult >= 2:
            self.decir(tr("Muy afín: +{n} de afinidad", n=int(ganancia)))
            self.sacudir_salvaje()
            for msg in progreso.dar_xp(self.mon, 3):
                self.decir(msg)
        else:
            self.decir(tr("+{n} de afinidad", n=int(ganancia)) + (tr("  (poco afín)") if mult < 1 else ""))

    def turno_salvaje(self):
        """Devuelve 'huyo' si el salvaje escapa."""
        s = self.salvaje
        nombre = self.nombre_salvaje()
        resultado = None
        if self.ultimo_mult == 0 and random.random() < 0.35:
            self.decir(tr("La repulsión aleja a {nombre}: escapó.", nombre=nombre))
            resultado = "huyo"
        else:
            dano = random.randint(3, 6) + s["nivel"]
            self.animar("agitacion", self.ctx_base())
            self.mon["energia"] = max(0, self.mon["energia"] - dano)
            self.decir(tr("Agitación térmica de {nombre}: −{n} de energía.", nombre=nombre, n=dano))
            if s["afinidad"] > 0 and random.random() < 0.2:
                s["afinidad"] = max(0, s["afinidad"] - 6)
                self.decir(tr("{nombre} se desordena un poco (−6 afinidad).", nombre=nombre))
        self.turno += 1
        return resultado

    def tras_mi_turno(self):
        self.turnos_jugador += 1
        if not self.tipos_visible and self.turnos_jugador >= TURNOS_PARA_REVELAR:
            self.tipos_visible = True
            self.decir(tr("Su grupo ya es evidente: {grupo}.", grupo=datos.nombre_tipos(self.tipos_salvaje())))

    def deducir(self):
        """Adivinar el grupo del salvaje. Devuelve True si gastó el turno."""
        if self.tipos_visible:
            self.decir(tr("Ya conoces su grupo."))
            return False
        nombres = [datos.TIPOS[t]["nombre"] for t in datos.ORDEN_TIPOS]
        p = d.menu(self.win, tr("¿Grupo de Lehninger?"), nombres,
                   ayuda=tr("¿Solo C/H? ¿anillo? ¿OH/SH/amida? ¿NH₃⁺? ¿COO⁻?"))
        if p is None:
            return False
        elegidos = (datos.ORDEN_TIPOS[p],)
        if elegidos == ("ARO",):
            s = d.menu(self.win, tr("¿Y su carácter?"), [tr("Más no polar (sin OH ni N–H)"),
                                                         tr("Algo polar (tiene OH o N–H)")])
            if s is None:
                return False
            elegidos = ("ARO", "NP" if s == 0 else "POL")
        self.tipos_visible = True
        if set(elegidos) == set(self.tipos_salvaje()):
            self.salvaje["afinidad"] = min(100, self.salvaje["afinidad"] + 10)
            msgs = progreso.dar_xp(self.mon, 5)
            self.decir(tr("Correcto: {grupo}. +10 afinidad, +5 XP",
                          grupo=datos.nombre_tipos(self.tipos_salvaje())))
            for msg in msgs:
                self.decir(msg)
            return False      # acertar no gasta el turno
        self.decir(tr("No. Era {grupo}. Pierdes el turno.", grupo=datos.nombre_tipos(self.tipos_salvaje())))
        return True

    def cambiar(self, forzado=False):
        equipo = self.juego["equipo"]
        filas, indices = [], []
        for i, m in enumerate(equipo):
            if i == self.activo or m["energia"] <= 0:
                continue
            f = datos.forma(m["id"])
            filas.append([f["nombre"], tr("Nv {n}", n=m["nivel"]),
                          datos.nombre_tipos(f["tipos"], corto=True),
                          tr("energía {n}", n=m["energia"])])
            indices.append(i)
        opciones = ["".join(c[0] for c in fila) for fila in d.alinear(filas)]
        if not opciones:
            return False
        while True:
            sel = d.menu(self.win, tr("¿Quién entra?"), opciones)
            if sel is not None:
                break
            if not forzado:
                return False
        self.activo = indices[sel]
        self._reiniciar_estado()
        self.decir(tr("Entra {nombre}.", nombre=datos.forma(self.mon["id"])["nombre"]))
        return True

    def lanzar_trna(self):
        """Devuelve 'capturado', 'huyo' o None."""
        if self.salvaje["afinidad"] < AFINIDAD_TRNA:
            self.decir(tr("El ARNt no se une: la afinidad debe ser ≥ {n}.", n=AFINIDAD_TRNA))
            return None
        self.dibujar()
        L = self.layout()
        tipo = preguntas.elegir_tipo(self.juego, self.aa)
        # la pregunta tapa la arena y tu recuadro completos, sin salirse
        bien = preguntas.preguntar(self.win, self.juego, self.aa, tipo,
                                   L["arena"], L["x"], L["w"],
                                   alto_min=L["yo"] + 4 - L["arena"])
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
            texto = tr("{nombre} ({tres}, {una}) se une a tu equipo.\n\nGrupo: {grupo}\n"
                       "Ficha completa en la Aminodex [X].", nombre=a["nombre"], tres=a["tres"],
                       una=self.aa, grupo=datos.nombre_tipos(a["tipos"]))
            if msgs:
                texto += "\n\n" + "\n".join(msgs)
            d.popup(self.win, texto, tr("Captura"), attr=d.c("bien"))
            return "capturado"
        self.salvaje["afinidad"] = max(0, self.salvaje["afinidad"] - 20)
        self.decir(tr("El ARNt se suelta (−20 afinidad)."))
        if random.random() < 0.3:
            self.decir(tr("{nombre} aprovechó para escapar.", nombre=self.nombre_salvaje()))
            return "huyo"
        return self.turno_salvaje()

    def info(self):
        f = datos.forma(self.mon["id"])
        nombre_r = datos.GRUPO_R.get(f["base"], ("", "", ""))
        lineas = [tr("Grupo: {grupo}", grupo=datos.nombre_tipos(f["tipos"]))]
        if not f["evo"]:
            lineas.append(tr("Grupo R: {nombre}  {formula}  ({clase})", nombre=nombre_r[0],
                             formula=nombre_r[1], clase=nombre_r[2]))
        lineas.append("")
        for i, mid in enumerate(self.movimientos()):
            m = datos.MOVIMIENTOS[mid]
            tipo = datos.TIPOS[m["tipo"]]["nombre"] if m["tipo"] in datos.TIPOS else tr("Neutro")
            contra = ""
            if self.tipos_visible:
                mult, partes = self._mult_mov(mid)
                contra = f"  → {self._interaccion_principal(partes)} ×{datos.fmt_mult(mult)}"
            lineas.append(tr("{i}) {nombre} [{tipo}] poder {poder}{contra}", i=i + 1, nombre=m["nombre"],
                             tipo=tipo, poder=m["poder"], contra=contra))
            lineas.append(f"   {m['desc']}")
            if m.get("ciencia"):
                lineas.append(f"   ↳ {m['ciencia']}")
        d.popup(self.win, "\n".join(lineas), tr("Interacciones de {nombre}", nombre=f["nombre"]), ancho=86)

    # -------------------------------------------------------------- bucle
    def jugar(self):
        if self.activo is None:
            return "derrota"
        self.decir(tr("Deduce su grupo [D] o interactúa [1-5]."))
        while True:
            self.dibujar()
            k = d.tecla(self.win)
            resultado = None
            movs = self.movimientos()
            if isinstance(k, str) and k.isdigit() and 1 <= int(k) <= len(movs):
                self.usar(movs[int(k) - 1])
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
                self.decir(tr("No lograste escapar."))
                resultado = self.turno_salvaje()
            elif d.es(k, "v"):
                i = anim.ORDEN_VEL.index(self.velocidad)
                self.juego["ajustes"]["velocidad"] = anim.ORDEN_VEL[(i + 1) % len(anim.ORDEN_VEL)]
                self.decir(tr("Velocidad de animación: {vel}.", vel=tr(self.velocidad)))
            elif d.es(k, "m", "?"):
                tipos = self.tipos_salvaje() if self.tipos_visible else None
                manual.mostrar(self.win, self.juego, "afinidad", rival=tipos)
            elif d.es(k, "i"):
                self.info()
            if resultado == "huyo":
                self.dibujar()
                d.popup(self.win, tr("{nombre} se escapó.", nombre=self.nombre_salvaje()), tr("Combate"))
                return "huyo"
            if self.mon["energia"] <= 0:
                nombre = datos.forma(self.mon["id"])["nombre"]
                self.decir(tr("{nombre} se desnaturalizó.", nombre=nombre))
                self.dibujar()
                if not self.cambiar(forzado=True):
                    return "derrota"


def combate(win, juego, aa, nivel, zona):
    return Combate(win, juego, aa, nivel, zona).jugar()
