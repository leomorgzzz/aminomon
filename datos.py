"""Datos de los 20 aminoácidos estándar, sus modificaciones
covalentes, tipos, movimientos, zonas del mapa y glosario.

Valores fisicoquímicos: Lehninger, 25 °C (masa del aminoácido libre en g/mol;
pK1 = α-COOH, pK2 = α-NH3+, pKR = cadena lateral, pI = punto isoeléctrico).
Hidropatía: escala de Kyte-Doolittle (1982).

Los textos están en español; en inglés se traducen al final de cada sección
con idioma.traducir() (las traducciones viven en en.py).
"""

from idioma import tr, traducir

# ================================================================== tipos
# Los tipos son los 5 grupos de Lehninger (según la cadena lateral R).
# Solo los aromáticos llevan un segundo tipo, tomado del propio Lehninger:
# "Phe, Tyr y Trp son relativamente no polares; Tyr y Trp son bastante más
# polares que Phe (por el OH de Tyr y el N del indol de Trp)".
TIPOS = {
    "NP": dict(
        nombre="No polar alifático", corto="No polar",
        desc="Cadena de C e H (Gly, Ala, Pro, Val, Leu, Ile; la Met lleva además un S). No forma "
             "puentes de H con el agua: se agrupa con otras cadenas no polares "
             "por el efecto hidrofóbico.",
    ),
    "ARO": dict(
        nombre="Aromático", corto="Aromát.",
        desc="Anillo aromático (Phe, Tyr, Trp) con electrones π: se apila con "
             "otros anillos (π–π) y atrae cationes por su cara (catión–π). "
             "Son relativamente no polares; Tyr y Trp, menos que Phe.",
    ),
    "POL": dict(
        nombre="Polar sin carga", corto="Polar",
        desc="OH, SH o amida (Ser, Thr, Cys, Asn, Gln) que forman puentes de H "
             "con el agua y con otros grupos polares, sin carga neta a pH 7.",
    ),
    "POS": dict(
        nombre="Cargado + (básico)", corto="Básico+",
        desc="Lys (amonio), Arg (guanidinio) e His (imidazol). Lys y Arg tienen "
             "carga +1 a pH 7; His solo a pH ácido (pKR 6), pero Lehninger la "
             "pone en este grupo.",
    ),
    "NEG": dict(
        nombre="Cargado − (ácido)", corto="Ácido−",
        desc="Asp y Glu: carboxilato (COO−) con pKR ~4, así que a pH 7 ya "
             "perdieron su H+ y tienen carga −1.",
    ),
}
ORDEN_TIPOS = list(TIPOS)
NEUTRO = "NEU"     # movimientos que no dependen de la cadena lateral: ×1

# Tabla simétrica: la interacción entre dos cadenas laterales es la misma sin
# importar cuál "ataca".  EFECTIVIDAD[tipo del movimiento][tipo del rival]
_PARES = {
    ("NP", "NP"): (2, "efecto hidrofóbico"),
    ("NP", "ARO"): (2, "efecto hidrofóbico"),
    ("NP", "POL"): (0.5, "el agua los separa"),
    ("NP", "POS"): (0.5, "el agua los separa"),
    ("NP", "NEG"): (0.5, "el agua los separa"),
    ("ARO", "ARO"): (2, "apilamiento π–π"),
    ("ARO", "POL"): (1, "puente de H X–H···π"),
    ("ARO", "POS"): (2, "interacción catión–π"),
    ("ARO", "NEG"): (0.5, "repulsión anión–π"),
    ("POL", "POL"): (2, "puentes de hidrógeno"),
    ("POL", "POS"): (1, "puente de H"),
    ("POL", "NEG"): (1, "puente de H"),
    ("POS", "POS"): (0, "repulsión (+ con +)"),
    ("POS", "NEG"): (2, "puente salino"),
    ("NEG", "NEG"): (0, "repulsión (− con −)"),
}
EFECTIVIDAD = {a: {} for a in ORDEN_TIPOS}
for (_a, _b), (_mult, _texto) in _PARES.items():
    EFECTIVIDAD[_a][_b] = EFECTIVIDAD[_b][_a] = (_mult, tr(_texto))


def multiplicador(tipo_mov, tipos_def):
    """Multiplicador total contra un defensor de uno o dos tipos.
    Devuelve (multiplicador, [(tipo_def, mult_parcial, interacción)])."""
    if tipo_mov == NEUTRO:
        return 1.0, [(t, 1, tr("interacción del esqueleto / van der Waals")) for t in tipos_def]
    total, partes = 1.0, []
    for t in tipos_def:
        m, texto = EFECTIVIDAD[tipo_mov][t]
        total *= m
        partes.append((t, m, texto))
    return total, partes


def fmt_mult(m):
    return {0.25: "¼", 0.5: "½"}.get(m, f"{m:g}")


# ===================================================== estructuras ASCII
ESQUELETO = [
    "        H",
    "        |",
    "  H3N+--C--COO-",
    "        |",
]

BENCENO = [
    "        C",
    "      /   \\\\",
    "    HC     CH",
    "    ||     |",
    "    HC     CH",
    "      \\   //",
]

GRUPOS = {
    "alifatico": "No polar alifático",
    "aromatico": "Aromático",
    "polar": "Polar sin carga",
    "acido": "Cargado − (ácido)",
    "basico": "Cargado + (básico)",
}

NUTRICION = {
    "Esencial": "No lo sintetizamos (o no lo bastante rápido): debe venir de "
                "la dieta.",
    "Condicional": "Normalmente se sintetiza, pero en prematuridad, estrés "
                   "metabólico, enfermedad o crecimiento rápido la síntesis no "
                   "alcanza.",
    "No esencial": "Lo sintetizamos en cantidad suficiente.",
}

# ============================================================ aminoácidos
# cadena: líneas debajo del Cα. completa: estructura entera (solo Pro).
AMINOACIDOS = {
    "G": dict(
        nombre="Glicina", tres="Gly", grupo="alifatico", tipos=("NP",),
        carga="Neutra", pk1=2.34, pk2=9.60, pkr=None, pi=5.97,
        hidropatia=-0.4, masa=75.07, nutricion="Condicional", codones=["GGU", "GGC", "GGA", "GGG"],
        cadena=["        H"],
        pista="Su R es un H: la más pequeña y la única sin carbono quiral. Cabe donde ninguna otra (es 1 de cada 3 residuos del colágeno) y da flexibilidad a la cadena.",
    ),
    "A": dict(
        nombre="Alanina", tres="Ala", grupo="alifatico", tipos=("NP",),
        carga="Neutra", pk1=2.34, pk2=9.69, pkr=None, pi=6.01,
        hidropatia=1.8, masa=89.09, nutricion="No esencial", codones=["GCU", "GCC", "GCA", "GCG"],
        cadena=["        CH3"],
        pista="Su R es un metilo: pequeño, no polar y sin nada que estorbe. Es la mejor formadora de hélices α.",
    ),
    "V": dict(
        nombre="Valina", tres="Val", grupo="alifatico", tipos=("NP",),
        carga="Neutra", pk1=2.32, pk2=9.62, pkr=None, pi=5.97,
        hidropatia=4.2, masa=117.15, nutricion="Esencial", codones=["GUU", "GUC", "GUA", "GUG"],
        cadena=[
            "        CH",
            "       /  \\",
            "    H3C    CH3",
        ],
        pista="Ramificada en el carbono β (forma de «V»): esa rama estorba en la hélice α, así que prefiere las hojas β.",
    ),
    "L": dict(
        nombre="Leucina", tres="Leu", grupo="alifatico", tipos=("NP",),
        carga="Neutra", pk1=2.36, pk2=9.60, pkr=None, pi=5.98,
        hidropatia=3.8, masa=131.17, nutricion="Esencial",
        codones=["UUA", "UUG", "CUU", "CUC", "CUA", "CUG"],
        cadena=[
            "        CH2",
            "        |",
            "        CH",
            "       /  \\",
            "    H3C    CH3",
        ],
        pista="Isobutilo: no polar y flexible. En las cremalleras de leucina, sus R encajan entre dos hélices como dientes.",
    ),
    "I": dict(
        nombre="Isoleucina", tres="Ile", grupo="alifatico", tipos=("NP",),
        carga="Neutra", pk1=2.36, pk2=9.68, pkr=None, pi=6.02,
        hidropatia=4.5, masa=131.17, nutricion="Esencial", codones=["AUU", "AUC", "AUA"],
        cadena=[
            "    H3C-CH",
            "        |",
            "        CH2",
            "        |",
            "        CH3",
        ],
        pista="Ramificada en β como la Val, con dos carbonos quirales (Cα y Cβ). Isómero de la Leu y la más hidrofóbica (KD 4.5).",
    ),
    "M": dict(
        nombre="Metionina", tres="Met", grupo="alifatico", tipos=("NP",),
        carga="Neutra", pk1=2.28, pk2=9.21, pkr=None, pi=5.74,
        hidropatia=1.9, masa=149.21, nutricion="Esencial", codones=["AUG"],
        cadena=[
            "        CH2",
            "        |",
            "        CH2",
            "        |",
            "        S",
            "        |",
            "        CH3",
        ],
        pista="Tioéter: su S no tiene H, así que no forma disulfuros y es casi no polar. AUG (Met) es el codón de inicio.",
    ),
    "P": dict(
        nombre="Prolina", tres="Pro", grupo="alifatico", tipos=("NP",),
        carga="Neutra", pk1=1.99, pk2=10.96, pkr=None, pi=6.48,
        hidropatia=-1.6, masa=115.13, nutricion="Condicional", codones=["CCU", "CCC", "CCA", "CCG"],
        cadena=None,
        completa=[
            "        H",
            "        |",
            "  H2N+--C--COO-",
            "    |   |",
            "   H2C  CH2",
            "     \\  /",
            "      CH2",
        ],
        pista="Su R se cierra sobre el N del α-amino (amina secundaria). Sin H en ese N no da el puente de H de la hélice, y el anillo rígido la tuerce: rompe hélices α y forma giros.",
    ),
    "F": dict(
        nombre="Fenilalanina", tres="Phe", grupo="aromatico", tipos=("ARO", "NP"),
        carga="Neutra", pk1=1.83, pk2=9.13, pkr=None, pi=5.48,
        hidropatia=2.8, masa=165.19, nutricion="Esencial", codones=["UUU", "UUC"],
        cadena=["        CH2", "        |"] + BENCENO + ["        CH"],
        pista="Bencilo: un anillo aromático sin grupos polares, muy hidrofóbico. Se apila con otros anillos (π–π) y atrae cationes (catión–π).",
    ),
    "Y": dict(
        nombre="Tirosina", tres="Tyr", grupo="aromatico", tipos=("ARO", "POL"),
        carga="Neutra", pk1=2.20, pk2=9.11, pkr=10.07, pi=5.66,
        hidropatia=-1.3, masa=181.19, nutricion="Condicional", codones=["UAU", "UAC"],
        cadena=["        CH2", "        |"] + BENCENO + [
            "        C",
            "        |",
            "        OH",
        ],
        pista="Phe + OH: el fenol (pKR 10.07) forma puentes de H y se puede fosforilar. Su anillo absorbe luz a 280 nm.",
    ),
    "W": dict(
        nombre="Triptófano", tres="Trp", grupo="aromatico", tipos=("ARO", "POL"),
        carga="Neutra", pk1=2.38, pk2=9.39, pkr=None, pi=5.89,
        hidropatia=-0.9, masa=204.23, nutricion="Esencial", codones=["UGG"],
        cadena=[
            "        CH2",
            "        |",
            "        C=====CH",
            "        |       \\",
            "   HC---C        NH",
            "  //     \\\\      /",
            " HC       C-----",
            "  \\       /",
            "   CH===CH",
        ],
        pista="Indol: el R más grande, con un N–H que forma puentes de H. Es el que más absorbe a 280 nm.",
    ),
    "S": dict(
        nombre="Serina", tres="Ser", grupo="polar", tipos=("POL",),
        carga="Neutra", pk1=2.21, pk2=9.15, pkr=None, pi=5.68,
        hidropatia=-0.8, masa=105.09, nutricion="No esencial",
        codones=["UCU", "UCC", "UCA", "UCG", "AGU", "AGC"],
        cadena=["        CH2", "        |", "        OH"],
        pista="Hidroximetilo: su OH forma puentes de H y es nucleófilo. Por ese OH se fosforila, y es el nucleófilo de las serín-proteasas.",
    ),
    "T": dict(
        nombre="Treonina", tres="Thr", grupo="polar", tipos=("POL",),
        carga="Neutra", pk1=2.11, pk2=9.62, pkr=None, pi=5.87,
        hidropatia=-0.7, masa=119.12, nutricion="Esencial", codones=["ACU", "ACC", "ACA", "ACG"],
        cadena=["        CH-OH", "        |", "        CH3"],
        pista="Como la Ser, con un CH3 extra (y dos carbonos quirales). Su OH también forma puentes de H y se fosforila.",
    ),
    "C": dict(
        nombre="Cisteína", tres="Cys", grupo="polar", tipos=("POL",),
        carga="Neutra", pk1=1.96, pk2=10.28, pkr=8.18, pi=5.07,
        hidropatia=2.5, masa=121.16, nutricion="Condicional", codones=["UGU", "UGC"],
        cadena=["        CH2", "        |", "        SH"],
        pista="Tiol (SH, pKR 8.18): su S− es muy nucleófilo y se oxida; dos Cys forman un puente disulfuro (cistina). Lehninger la pone en polares sin carga, aunque su KD (+2.5) dice que es bastante hidrofóbica.",
    ),
    "N": dict(
        nombre="Asparagina", tres="Asn", grupo="polar", tipos=("POL",),
        carga="Neutra", pk1=2.02, pk2=8.80, pkr=None, pi=5.41,
        hidropatia=-3.5, masa=132.12, nutricion="No esencial", codones=["AAU", "AAC"],
        cadena=[
            "        CH2",
            "        |",
            "        C",
            "       // \\",
            "      O    NH2",
        ],
        pista="Amida del Asp: neutra, con un C=O que acepta y un NH2 que dona puentes de H. En la secuencia N-X-S/T recibe azúcares en su N.",
    ),
    "Q": dict(
        nombre="Glutamina", tres="Gln", grupo="polar", tipos=("POL",),
        carga="Neutra", pk1=2.17, pk2=9.13, pkr=None, pi=5.65,
        hidropatia=-3.5, masa=146.15, nutricion="Condicional", codones=["CAA", "CAG"],
        cadena=[
            "        CH2",
            "        |",
            "        CH2",
            "        |",
            "        C",
            "       // \\",
            "      O    NH2",
        ],
        pista="Amida del Glu, un CH2 más larga que la Asn. Neutra: su amida acepta y dona puentes de H.",
    ),
    "D": dict(
        nombre="Aspartato", tres="Asp", grupo="acido", tipos=("NEG",),
        carga="Negativa (−1)", pk1=1.88, pk2=9.60, pkr=3.65, pi=2.77,
        hidropatia=-3.5, masa=133.10, nutricion="No esencial", codones=["GAU", "GAC"],
        cadena=[
            "        CH2",
            "        |",
            "        C",
            "       // \\",
            "      O    O-",
        ],
        pista="Carboxilato (pKR 3.65): a pH 7 tiene carga −, y su pI (2.77) es el más bajo de todos. Forma puentes salinos y une cationes como el Ca²+.",
    ),
    "E": dict(
        nombre="Glutamato", tres="Glu", grupo="acido", tipos=("NEG",),
        carga="Negativa (−1)", pk1=2.19, pk2=9.67, pkr=4.25, pi=3.22,
        hidropatia=-3.5, masa=147.13, nutricion="No esencial", codones=["GAA", "GAG"],
        cadena=[
            "        CH2",
            "        |",
            "        CH2",
            "        |",
            "        C",
            "       // \\",
            "      O    O-",
        ],
        pista="Un CH2 más que el Asp (pKR 4.25): también − a pH 7. Con la cadena más larga, forma hélices α mejor que el Asp.",
    ),
    "K": dict(
        nombre="Lisina", tres="Lys", grupo="basico", tipos=("POS",),
        carga="Positiva (+1)", pk1=2.18, pk2=8.95, pkr=10.53, pi=9.74,
        hidropatia=-3.9, masa=146.19, nutricion="Esencial", codones=["AAA", "AAG"],
        cadena=[
            "        CH2",
            "        |",
            "        CH2",
            "        |",
            "        CH2",
            "        |",
            "        CH2",
            "        |",
            "        NH3+",
        ],
        pista="Amonio al final de 4 CH2 (pKR 10.53): + a pH 7. Cuando pierde su H+, ese N es nucleófilo: por eso se acetila, se metila y se ubiquitina.",
    ),
    "R": dict(
        nombre="Arginina", tres="Arg", grupo="basico", tipos=("POS",),
        carga="Positiva (+1)", pk1=2.17, pk2=9.04, pkr=12.48, pi=10.76,
        hidropatia=-4.5, masa=174.20, nutricion="Condicional",
        codones=["CGU", "CGC", "CGA", "CGG", "AGA", "AGG"],
        cadena=[
            "        CH2",
            "        |",
            "        CH2",
            "        |",
            "        CH2",
            "        |",
            "        NH",
            "        |",
            "        C",
            "       // \\",
            "   +H2N    NH2",
        ],
        pista="Guanidinio (pKR 12.48): su carga + se reparte entre 3 N por resonancia, así que casi nunca la pierde. El pI más alto (10.76) y la más hidrofílica (KD −4.5).",
    ),
    "H": dict(
        nombre="Histidina", tres="His", grupo="basico", tipos=("POS",),
        carga="Mayormente neutra (+ parcial)", pk1=1.82, pk2=9.17, pkr=6.00,
        pi=7.59, hidropatia=-3.2, masa=155.16, nutricion="Esencial", codones=["CAU", "CAC"],
        cadena=[
            "        CH2",
            "        |",
            "        C------NH",
            "        ||       \\",
            "        ||        CH",
            "        ||       //",
            "        HC------N",
        ],
        pista="Imidazol con pKR ≈ 6, cerca del pH de la célula: a pH 7 solo ~10% está protonado y a pH 5 casi todo. Por eso toma y cede H+ en los sitios activos.",
    ),
}

# Casos en los que el grupo de Lehninger y el signo de KD parecen contradecirse.
# KD combina la energía de pasar del agua al vapor con qué tan seguido aparece
# enterrado cada residuo en proteínas de estructura conocida.
NOTA_KD = {
    "G": "No polar no es lo mismo que hidrofóbico. El R de la Gly es un H, sin superficie de C–H que esconder del agua, así que pesa más su esqueleto polar (N–H y C=O): KD ≈ 0 (−0.4). Lehninger: es formalmente no polar, pero casi no contribuye a las interacciones hidrofóbicas.",
    "P": "Por estructura es no polar (su anillo es solo C–H), pero KD −1.6. KD "
         "no mide solo la cadena: también cuenta qué tan seguido queda enterrada en "
         "proteínas, y la Pro, que rompe hélices y láminas, suele quedar en giros y "
         "lazos de la superficie, en contacto con el agua.",
    "C": "Es polar sin carga por el S–H, pero el S casi no es más electronegativo "
         "que el C (2.58 frente a 2.55): el S–H es muy poco polar y forma puentes "
         "de H débiles. Además suele estar enterrada en las proteínas (sola o en "
         "disulfuros), así que su KD es +2.5. Otros libros la ponen con los "
         "hidrofóbicos.",
    "Y": "Su anillo es poco polar, pero el O–H del fenol forma puentes de H con el "
         "agua: KD −1.3, mucho menos hidrofóbica que la Phe (+2.8).",
    "W": "El indol es grande y poco polar, pero su N–H forma puentes de H y suele "
         "quedar en la interfase membrana-agua: KD −0.9.",
}

ORDEN = list("GAVLIMPFYWSTCNQDEKRH")
for _c, _aa in AMINOACIDOS.items():
    _aa["una"] = _c


def calcular_pi(aa):
    """pI = promedio de los dos pKa que flanquean la especie neutra."""
    a = AMINOACIDOS[aa]
    pks = sorted(p for p in (a["pk1"], a["pk2"], a["pkr"]) if p is not None)
    carga_inicial = 1 + (1 if a["grupo"] == "basico" else 0)
    i = carga_inicial - 1
    return (pks[i] + pks[i + 1]) / 2, (pks[i], pks[i + 1])


# Cargas parciales a cualquier pH (Henderson-Hasselbalch, solo cadenas laterales)
PKA_IONIZABLES = {"D": (3.65, -1), "E": (4.25, -1), "H": (6.00, +1),
                  "C": (8.18, -1), "Y": (10.07, -1), "K": (10.53, +1),
                  "R": (12.48, +1)}


def carga_cadena(aa, ph):
    if aa not in PKA_IONIZABLES:
        return 0.0
    pka, signo = PKA_IONIZABLES[aa]
    if signo > 0:
        return 1 / (1 + 10 ** (ph - pka))
    return -1 / (1 + 10 ** (pka - ph))


# ============================================ modificaciones covalentes
MODIFICACIONES = {
    "Hyp": dict(
        base="P", nombre="Hidroxiprolina", tres="Hyp", tipos=("POL",),
        carga="Neutra", req=dict(nivel=5, objeto="Vitamina C"),
        cambio="Gana un OH en el anillo: de No polar a Polar sin carga.",
        bio="La prolil 4-hidroxilasa del RE le pone el OH en el C4 del anillo; necesita vitamina C para seguir activa. Ese OH fija el pliegue del anillo que pide la triple hélice del colágeno: sin vitamina C el colágeno es inestable (escorbuto).",
        pista="Hay vitamina C en la matriz extracelular (C en el mapa).",
        completa=[
            "        H",
            "        |",
            "  H2N+--C--COO-",
            "    |   |",
            "   H2C  CH2",
            "     \\  /",
            "      CH-OH",
        ],
    ),
    "Hyl": dict(
        base="K", nombre="Hidroxilisina", tres="Hyl", tipos=("POS",),
        carga="Positiva (+1)", req=dict(nivel=5, objeto="Vitamina C"),
        matiz="▼ Un poco menos básica: el OH cercano baja el pKa del amonio "
              "(≈ 9.7 frente a 10.5 de la Lys), pero a pH 7 sigue siendo +1.",
        cambio="Conserva la carga + (sigue en el grupo básico) y gana un OH "
               "en el carbono δ.",
        bio="La lisil hidroxilasa del RE (también con vitamina C) le pone un OH en el carbono δ. Ese OH es un punto de anclaje: recibe azúcares y ayuda a entrecruzar las fibras de colágeno.",
        pista="Hay vitamina C en la matriz extracelular (C en el mapa).",
        cadena=[
            "        CH2", "        |", "        CH2", "        |",
            "        CH-OH", "        |", "        CH2", "        |",
            "        NH3+",
        ],
    ),
    "Kac": dict(
        base="K", nombre="Acetil-lisina", tres="Kac", tipos=("POL",),
        carga="Neutra", req=dict(nivel=6, zona="nucleo"),
        cambio="Pierde la carga +: el amonio se vuelve una amida neutra. De "
               "Cargado + a Polar sin carga.",
        bio="Las HAT pasan el acetilo del acetil-CoA al N de la Lys (cuando ese N está sin su H+ y es nucleófilo). Queda una amida sin carga: la histona se une menos al ADN (−) y la cromatina se abre. Las HDAC lo quitan.",
        pista="Las HAT actúan en el núcleo; entra por un poro.",
        cadena=[
            "        CH2", "        |", "        CH2", "        |",
            "        CH2", "        |", "        CH2", "        |",
            "        NH", "        |", "        C=O", "        |",
            "        CH3",
        ],
    ),
    "Kme3": dict(
        base="K", nombre="Trimetil-lisina", tres="Kme3", tipos=("POS",),
        carga="Positiva (+1, permanente)", req=dict(nivel=7, zona="nucleo"),
        matiz="▲ Más firmemente cargada: sin H en el N no tiene pKa, así que no "
              "pierde la carga + a ningún pH.",
        cambio="Sigue siendo + (amonio cuaternario: ya no puede perder la "
               "carga ni acetilarse, porque su N no tiene H).",
        bio="Las metiltransferasas (HMT) le pasan tres metilos de la SAM. Sin H en el N ya no dona puentes de H ni se puede acetilar: la reconocen «jaulas» de anillos aromáticos por catión–π. Según el sitio, activa (H3K4me3) o silencia (H3K9me3) genes.",
        pista="Las HMT actúan en el núcleo.",
        cadena=[
            "        CH2", "        |", "        CH2", "        |",
            "        CH2", "        |", "        CH2", "        |",
            "        N+(CH3)3",
        ],
    ),
    "pS": dict(
        base="S", nombre="Fosfoserina", tres="pSer", tipos=("NEG",),
        carga="Negativa (≈ −2)", req=dict(nivel=4, objeto="ATP"),
        cambio="Gana un fosfato: de Polar sin carga a Cargado − (≈ −2).",
        bio="¿Por qué Ser, Thr y Tyr? Son las únicas con un OH en la cadena lateral: ese O ataca al fosfato γ del ATP y queda un fosfoéster. Ese enlace casi no se rompe solo, pero una fosfatasa lo quita en segundos: un interruptor estable y reversible. El residuo pasa de neutro a ≈ −2 y cambia con quién se une. Una quinasa fosforila muchas copias de su blanco, así que la señal se amplifica.",
        pista="La mitocondria (Θ) recarga ATP.",
        cadena=["        CH2", "        |", "        O", "        |",
                "        PO3(2-)"],
    ),
    "pT": dict(
        base="T", nombre="Fosfotreonina", tres="pThr", tipos=("NEG",),
        carga="Negativa (≈ −2)", req=dict(nivel=4, objeto="ATP"),
        cambio="Gana un fosfato: de Polar sin carga a Cargado − (≈ −2).",
        bio="Mismo OH que la Ser, pero en un carbono con un CH3 al lado: más voluminosa, y algunas quinasas prefieren a una o a otra. Las CDK del ciclo celular fosforilan Ser y Thr seguidas de Pro.",
        pista="La mitocondria (Θ) recarga ATP.",
        cadena=["        CH-O-PO3(2-)", "        |", "        CH3"],
    ),
    "pY": dict(
        base="Y", nombre="Fosfotirosina", tres="pTyr", tipos=("NEG", "ARO"),
        carga="Negativa (≈ −2)", req=dict(nivel=5, objeto="ATP"),
        cambio="El OH del fenol se fosforila: conserva el anillo, pero ahora "
               "tiene carga ≈ −2 (Cargado − / Aromático).",
        bio="Su OH es de un fenol, más largo y rígido que el de Ser o Thr: lo fosforilan otras quinasas, las tirosina quinasas (como el receptor de insulina). La pTyr sobresale y los dominios SH2 la atrapan: una Arg hace puente salino con el fosfato y el anillo encaja en un bolsillo.",
        pista="La mitocondria (Θ) recarga ATP.",
        cadena=["        CH2", "        |"] + BENCENO + [
            "        C", "        |", "        O-PO3(2-)",
        ],
    ),
    "Cis": dict(
        base="C", nombre="Cistina", tres="Cys-Cys", tipos=("NP",),
        carga="Neutra", req=dict(nivel=4, zona="re", otra_cys=True),
        cambio="Dos Cys se unen por un enlace S–S covalente y pierden los SH. "
               "Lehninger: los residuos unidos por disulfuro son fuertemente "
               "hidrofóbicos (no polares).",
        bio="El S− de la Cys se oxida fácil, y dos Cys cercanas forman un S–S covalente. Solo se mantiene donde el ambiente es oxidante (RE, exterior); en el citosol el glutatión lo reduce. La PDI del RE los forma y reacomoda: por eso las proteínas secretadas (insulina, anticuerpos) los tienen.",
        pista="El RE es oxidante; lleva otra Cys en el equipo.",
        cadena=[
            "        CH2", "        |", "        S", "        |",
            "        S", "        |", "        CH2", "        |",
            "  -OOC--C--NH3+",
        ],
    ),
    "Gla": dict(
        base="E", nombre="γ-carboxiglutamato", tres="Gla", tipos=("NEG",),
        carga="Negativa (≈ −2)", req=dict(nivel=5, objeto="Vitamina K"),
        matiz="▲ Más ácido: dos carboxilatos, carga ≈ −2 frente a −1 del Glu.",
        cambio="Gana un segundo carboxilo en el carbono γ: carga ≈ −2.",
        bio="La γ-carboxilasa del RE, con vitamina K, le añade un CO2 en el carbono γ. Los dos carboxilatos juntos atrapan un Ca²+ entre ellos: así los factores de coagulación se pegan a la membrana. La warfarina impide reciclar la vitamina K.",
        pista="Hay vitamina K en el retículo (K en el mapa).",
        cadena=[
            "        CH2", "        |", "        CH",
            "       /  \\", "   -OOC    COO-",
        ],
    ),
    "Nglc": dict(
        base="N", nombre="Asn N-glicosilada", tres="Asn-Glc", tipos=("POL",),
        carga="Neutra", req=dict(nivel=5, zona="re"),
        matiz="▲ Más polar: el glicano trae muchos OH que forman puentes de H.",
        cambio="Se le une un árbol de azúcares al N de la amida: aún más polar.",
        bio="La OST del RE pasa un bloque de 14 azúcares al N de la amida mientras la cadena aún sale del ribosoma (es cotraduccional). Solo en N-X-S/T (X ≠ Pro): el OH de la Ser/Thr ayuda a activar ese N, y una Pro torcería el sitio. Los OH del glicano hacen la proteína más soluble y la marcan para el control de plegamiento.",
        pista="La OST trabaja en el retículo endoplásmico.",
        cadena=[
            "        CH2", "        |", "        C", "       // \\",
            "      O    NH", "             \\", "             GlcNAc", "               |",
            "             GlcNAc", "               |", "             Man…",
        ],
    ),
    "gS": dict(
        base="S", nombre="Ser O-glicosilada", tres="Ser-GalNAc", tipos=("POL",),
        carga="Neutra", req=dict(nivel=5, zona="golgi"),
        matiz="▲ Más polar: la GalNAc trae varios OH que forman puentes de H.",
        cambio="Se le une una N-acetilgalactosamina (GalNAc) al O del OH: sigue "
               "siendo polar, pero ahora carga un azúcar.",
        bio="Las GalNAc-transferasas (GALNT) del Golgi ponen la GalNAc en el O del OH, ya fuera del RE. A diferencia de la Asn, aquí el azúcar va en un O y no hay secuencia consenso: basta un tramo expuesto de Ser/Thr, a menudo con Pro cerca.",
        pista="Las GALNT trabajan en el aparato de Golgi.",
        cadena=["        CH2", "        |", "        O", "        |", "        GalNAc…"],
    ),
    "gT": dict(
        base="T", nombre="Thr O-glicosilada", tres="Thr-GalNAc", tipos=("POL",),
        carga="Neutra", req=dict(nivel=5, zona="golgi"),
        matiz="▲ Más polar: la GalNAc trae varios OH que forman puentes de H.",
        cambio="Se le une una GalNAc al O del OH: sigue siendo polar, pero ahora "
               "carga un azúcar.",
        bio="Mismas GALNT del Golgi; muchas prefieren Thr. En las mucinas, tramos de Pro, Thr y Ser se cubren de O-glicanos: sus OH atrapan agua y forman el moco.",
        pista="Las GALNT trabajan en el aparato de Golgi.",
        cadena=["        CH-O-GalNAc…", "        |", "        CH3"],
    ),
    "Cit": dict(
        base="R", nombre="Citrulina", tres="Cit", tipos=("POL",),
        carga="Neutra", req=dict(nivel=6),
        cambio="Pierde la carga +: el guanidinio se vuelve una urea neutra "
               "(de Cargado + a Polar sin carga).",
        bio="Las PAD (con Ca²+) hidrolizan el guanidinio de la Arg: sale NH4+ y queda una urea neutra. Perder un + cambia con qué se une la proteína: la PAD4 citrulina histonas y descompacta la cromatina. El sistema inmune puede tomar estas proteínas por extrañas (artritis reumatoide).",
        pista="Solo requiere nivel.",
        cadena=[
            "        CH2", "        |", "        CH2", "        |",
            "        CH2", "        |", "        NH", "        |",
            "        C", "       // \\", "      O    NH2",
        ],
    ),
}

# ============================================ péptidos (encargos post-juego)
# Péptidos reales que el René-virus encarga tras el examen final: se traducen
# de su ARNm y se construyen con los residuos del equipo.
PEPTIDOS = {
    "rgd": dict(
        nombre="Motivo RGD", seq="RGD",
        bio="Arg-Gly-Asp: el motivo de la fibronectina que reconocen las "
            "integrinas para pegar la célula a la matriz extracelular. Algunos "
            "antiplaquetarios imitan este motivo."),
    "trh": dict(
        nombre="TRH (tiroliberina)", seq="QHP",
        bio="El hipotálamo la libera para que la hipófisis secrete TSH. Madura "
            "con dos modificaciones: la Gln N-terminal se cicla a piroglutamato y "
            "el extremo C queda amidado."),
    "devd": dict(
        nombre="Sitio de la caspasa-3", seq="DEVD",
        bio="La caspasa-3, verdugo de la apoptosis, corta justo después del Asp "
            "de DEVD (por ejemplo, en PARP). Las caspasas son cisteín-proteasas "
            "que cortan después de un Asp."),
    "metenc": dict(
        nombre="Met-encefalina", seq="YGGFM",
        bio="Opioide endógeno que se une a receptores δ y μ y reduce el dolor. "
            "Sale del corte de la proencefalina."),
    "leuenc": dict(
        nombre="Leu-encefalina", seq="YGGFL",
        bio="Como la Met-encefalina, pero termina en Leu. Su Tyr N-terminal es "
            "clave: el fenol de la morfina imita a esa Tyr."),
    "abeta": dict(
        nombre="Aβ(16–22)", seq="KLVFFAE",
        bio="Fragmento central del péptido β-amiloide del Alzheimer. Su parche "
            "hidrofóbico (Leu, Val, Phe, Phe) hace que las hebras se apilen en "
            "fibras amiloides."),
    "nls": dict(
        nombre="NLS del antígeno T de SV40", seq="PKKKRKV",
        bio="La NLS clásica, de un virus: las importinas reconocen su parche de "
            "Lys y Arg y llevan la proteína al núcleo a través del poro."),
    "ang2": dict(
        nombre="Angiotensina II", seq="DRVYIHPF",
        bio="La ECA la corta de la angiotensina I. Contrae los vasos y sube la "
            "presión; los IECA (como el enalapril) bloquean su formación."),
    "oxi": dict(
        nombre="Oxitocina", seq="CYIQNCPLG",
        bio="Hormona de la hipófisis posterior: contracciones del parto y "
            "salida de la leche. Sus Cys 1 y 6 forman un disulfuro que cierra un "
            "anillo, y el extremo C está amidado."),
    "avp": dict(
        nombre="Vasopresina", seq="CYFQNCPRG",
        bio="Hormona antidiurética: el riñón retiene agua. Difiere de la "
            "oxitocina solo en las posiciones 3 (Phe) y 8 (Arg); también tiene el "
            "disulfuro Cys1–Cys6."),
    "bradi": dict(
        nombre="Bradicinina", seq="RPPGFSPFR",
        bio="Vasodilatador e inflamatorio. La ECA también la degrada: por eso los "
            "IECA pueden causar tos seca."),
    "gnrh": dict(
        nombre="GnRH", seq="QHWSYGLRPG",
        bio="Del hipotálamo: hace que la hipófisis libere LH y FSH. Como la TRH, "
            "empieza con piroglutamato y termina amidada."),
    "kiss": dict(
        nombre="Kisspeptina-10", seq="YNWNSFGLRF",
        bio="Activa a las neuronas de GnRH y dispara la pubertad. Termina en "
            "Arg-Phe-NH2, como toda la familia de péptidos RF-amida."),
    "sustp": dict(
        nombre="Sustancia P", seq="RPKPQQFFGLM",
        bio="Neuropéptido del dolor y la inflamación. Termina en "
            "Phe-X-Gly-Leu-Met-NH2, la firma de las taquicininas."),
    "tat": dict(
        nombre="Péptido Tat del VIH-1", seq="YGRKKRRQRRR",
        bio="Residuos 47–57 de la proteína Tat del VIH-1: tan rico en Arg que "
            "atraviesa membranas. Se usa como péptido penetrante para meter "
            "fármacos a las células. Al René-virus le cae bien."),
}

# ============================================ la selenocisteína (posgame)
# No es una modificación postraduccional: la Ser se convierte en Sec sobre su
# ARNt, antes de entrar a la proteína. No está en los 5 grupos de Lehninger;
# en el juego es Polar como la Cys y Cargado − porque a pH 7 su selenol (pKa
# ≈ 5.2) está casi todo desprotonado (–Se−).
SEC = dict(
    nombre="Selenocisteína", tres="Sec", una="U", tipos=("POL", "NEG"),
    carga="≈ −1 a pH 7 (selenolato, pKa ≈ 5.2)", masa=168.06,
    grupo_r=("selanilmetilo", "–CH2–SeH", "selenol"),
    cadena=["        CH2", "        |", "        SeH"],
)

OBJETOS = {
    "ATP": "Donador de fosfato para las quinasas. Lo da la mitocondria.",
    "Vitamina C": "Cofactor de las hidroxilasas de Pro y Lys (colágeno).",
    "Vitamina K": "Cofactor de la γ-glutamil carboxilasa (coagulación).",
}


# ============================================================ movimientos
# Todos los movimientos son interacciones no covalentes (o el disulfuro)
# entre tu aminoácido y el rival. Se nombran por la clase de interacción y el
# grupo R que la forma; la interacción concreta (puente salino, catión–π,
# repulsión…) depende del grupo del rival y se muestra en combate.

# Nombre, fórmula y clase química del grupo R
GRUPO_R = {
    "G": ("hidrógeno", "–H", "sin cadena lateral"),
    "A": ("metilo", "–CH3", "alquilo"),
    "V": ("isopropilo", "–CH(CH3)2", "alquilo ramificado"),
    "L": ("isobutilo", "–CH2CH(CH3)2", "alquilo ramificado"),
    "I": ("sec-butilo", "–CH(CH3)CH2CH3", "alquilo ramificado"),
    "M": ("metiltioetilo", "–CH2CH2–S–CH3", "tioéter"),
    "P": ("pirrolidina", "–CH2CH2CH2– (cerrado sobre el N)", "amina secundaria cíclica"),
    "F": ("bencilo", "–CH2–C6H5", "fenilo"),
    "Y": ("p-hidroxibencilo", "–CH2–C6H4–OH", "fenol"),
    "W": ("indolilmetilo", "–CH2–indol", "indol"),
    "S": ("hidroximetilo", "–CH2–OH", "alcohol primario"),
    "T": ("1-hidroxietilo", "–CH(OH)–CH3", "alcohol secundario"),
    "C": ("sulfanilmetilo", "–CH2–SH", "tiol"),
    "N": ("carbamoilmetilo", "–CH2–CONH2", "amida"),
    "Q": ("2-carbamoiletilo", "–CH2CH2–CONH2", "amida"),
    "D": ("carboximetilo", "–CH2–COO−", "carboxilato"),
    "E": ("2-carboxietilo", "–CH2CH2–COO−", "carboxilato"),
    "K": ("4-aminobutilo", "–(CH2)4–NH3+", "amonio primario"),
    "R": ("3-guanidinopropilo", "–(CH2)3–NH–C(NH2)2+", "guanidinio"),
    "H": ("imidazolilmetilo", "–CH2–imidazol", "imidazol"),
}

INTERACCION = {"NP": "Efecto hidrofóbico", "ARO": "Interacción π",
               "POL": "Puente de H", "POS": "Electrostática", "NEG": "Electrostática"}

DESC_TIPO = {
    "NP": ("Junta su cadena no polar con la del rival y libera el agua "
           "ordenada que las rodeaba.",
           "Con no polares y aromáticos: efecto hidrofóbico. Con polares o "
           "cargados no funciona: el agua solvata a esos grupos."),
    "ARO": ("La nube π del anillo interactúa con el grupo del rival.",
            "Con otro anillo: apilamiento π–π. Con un catión: catión–π. Con un "
            "X–H: puente de H débil hacia la cara π. Con un anión: repulsión."),
    "POL": ("Forma un puente de H: un H unido a O o N se comparte con un O o "
            "N del rival.",
            "Necesita un donador (X–H) y un aceptor (par libre). Con no "
            "polares no hay con quién formarlo."),
    "POS": ("Su carga + interactúa electrostáticamente con el rival.",
            "Con un anión: puente salino. Con un anillo: catión–π. Con un "
            "grupo polar: puente de H. Con otra carga +: repulsión."),
    "NEG": ("Su carga − interactúa electrostáticamente con el rival.",
            "Con un catión: puente salino. Con un grupo polar: puente de H. "
            "Con un anillo o con otra carga −: repulsión."),
}

# Interacciones de cadena lateral: (tipo, grupo que la forma, poder)
INTERACCIONES_R = {
    "G": [],
    "A": [("NP", "metilo", 30)],
    "V": [("NP", "isopropilo", 40)],
    "L": [("NP", "isobutilo", 45)],
    "I": [("NP", "sec-butilo", 45)],
    "M": [("NP", "tioéter", 40)],
    "P": [("NP", "pirrolidina", 35)],
    "F": [("ARO", "fenilo", 45), ("NP", "bencilo", 40)],
    "Y": [("ARO", "fenol", 40), ("POL", "O–H fenólico", 40)],
    "W": [("ARO", "indol", 50), ("POL", "N–H del indol", 35)],
    "S": [("POL", "hidroxilo", 40)],
    "T": [("POL", "hidroxilo", 40)],
    "C": [("POL", "tiol", 30)],
    "N": [("POL", "carboxamida", 50)],
    "Q": [("POL", "carboxamida", 50)],
    "D": [("NEG", "carboxilato", 45)],
    "E": [("NEG", "carboxilato", 45)],
    "K": [("POS", "ε-amonio", 45)],
    "R": [("POS", "guanidinio", 55)],
    "H": [("POS", "imidazolio", 40)],
    "Hyp": [("POL", "hidroxilo de la Hyp", 45)],
    "Hyl": [("POS", "ε-amonio", 45)],
    "Kac": [("POL", "acetamida", 45)],
    "Kme3": [("POS", "trimetilamonio", 50)],
    "pS": [("NEG", "fosfato", 55)],
    "pT": [("NEG", "fosfato", 55)],
    "pY": [("NEG", "fosfato", 55), ("ARO", "fenilo", 40)],
    "Cis": [("NP", "disulfuro", 50)],
    "Gla": [("NEG", "dicarboxilato", 55)],
    "Nglc": [("POL", "glicano (O–H)", 55)],
    "gS": [("POL", "O-glicano (O–H)", 55)],
    "gT": [("POL", "O-glicano (O–H)", 55)],
    "Cit": [("POL", "ureido", 50)],
    "U": [("POL", "selenol", 40)],
}


INTERACCION = {k: tr(v) for k, v in INTERACCION.items()}
DESC_TIPO = {k: (tr(a), tr(b)) for k, (a, b) in DESC_TIPO.items()}
INTERACCIONES_R = {k: [(t, tr(g), p) for t, g, p in v] for k, v in INTERACCIONES_R.items()}
GRUPO_R = {k: tuple(tr(x) for x in v) for k, v in GRUPO_R.items()}


def _m(nombre, tipo, poder, desc, ciencia=None, efecto=None):
    return dict(nombre=nombre, tipo=tipo, poder=poder, desc=desc,
                ciencia=ciencia, efecto=efecto)


MOVIMIENTOS = {
    "van_der_waals": _m(
        "Van der Waals", NEUTRO, 25,
        "Fuerzas de London entre átomos en contacto: débiles, pero existen "
        "con cualquier grupo (×1).",
        "Un dipolo instantáneo induce otro en el átomo vecino."),
    "puente_h_esqueleto": _m(
        "Puente de H · esqueleto", NEUTRO, 35,
        "El N–H de su enlace peptídico se une al C=O del esqueleto del rival "
        "(×1 con todos).",
        "Así se aparean las hebras de una lámina β. La Pro no puede: su N no "
        "tiene H. La Gly, sin cadena lateral, se acerca más."),
    "puente_disulfuro": _m(
        "Puente disulfuro", "POL", 50,
        "Enlace covalente S–S. Solo se forma con otra Cys: afinidad máxima. "
        "Con cualquier otro residuo no ocurre.",
        "2 R–SH → R–S–S–R + 2H+ + 2e− (oxidación)."),
}
MOVIMIENTOS["puente_selenilsulfuro"] = _m(
    "Puente selenilsulfuro", "POL", 50,
    "Enlace covalente Se–S. Solo se forma con una Cys: afinidad máxima. "
    "Con cualquier otro residuo no ocurre.",
    "R–SeH + R'–SH → R–Se–S–R' + 2H+ + 2e− (así trabaja la tiorredoxina reductasa).")
MOVIMIENTOS["puente_disulfuro"]["efecto"] = "disulfuro"
MOVIMIENTOS["puente_selenilsulfuro"]["efecto"] = "disulfuro"
traducir(MOVIMIENTOS, "nombre", "desc", "ciencia")      # los fijos (los de R ya vienen traducidos)
for _fid, _lista in INTERACCIONES_R.items():
    for _tipo, _grupo, _poder in _lista:
        _desc, _ciencia = DESC_TIPO[_tipo]
        MOVIMIENTOS[f"{_fid}:{_tipo}"] = _m(
            f"{INTERACCION[_tipo]} · {_grupo}", _tipo, _poder, _desc, _ciencia)


def movimientos_de(fid):
    """Interacciones de un aminoácido o residuo modificado."""
    movs = [f"{fid}:{t}" for t, _, _ in INTERACCIONES_R[fid]]
    if fid == "C":
        movs.append("puente_disulfuro")
    if fid == "U":
        movs.append("puente_selenilsulfuro")
    base = MODIFICACIONES[fid]["base"] if fid in MODIFICACIONES else fid
    if base != "P":          # la Pro (y la Hyp) no tiene H en el N del esqueleto
        movs.append("puente_h_esqueleto")
    movs.append("van_der_waals")
    return movs


# ================================================================== zonas
ZONAS = {
    "membrana": dict(
        nombre="Membrana (colas lipídicas)", aminos=list("AVLIMF"),
        niveles=(2, 5), glifo="≈", color="NP",
        por_que="Aquí viven los no polares (y Phe): las hélices "
                "transmembrana esconden sus cadenas entre las colas de ácidos "
                "grasos, lejos del agua.",
    ),
    "interfase": dict(
        nombre="Interfase de la membrana", aminos=list("WY"),
        niveles=(3, 6), glifo="◦", color="ARO",
        por_que="Cinturón aromático: Trp y Tyr se colocan justo donde las "
                "cabezas polares de los lípidos tocan el agua. Su anillo es "
                "poco polar, pero su N–H u O–H forma puentes de H con las "
                "cabezas.",
    ),
    "citosol": dict(
        nombre="Citosol", aminos=list("STNQC"), niveles=(2, 5),
        glifo="·", color="POL",
        por_que="Aquí viven los polares: en la superficie de las proteínas "
                "solubles forman puentes de H con el agua.",
    ),
    "ribosomas": dict(
        nombre="Ribosomas", aminos=list("K"), niveles=(3, 5),
        glifo="÷", color="POS",
        por_que="Ribosomas libres traduciendo ARNm. Sus proteínas son ricas en Lys: sus cargas + neutralizan los fosfatos (−) del ARN ribosomal. Aquí consigues las Lys para tu NLS; la Arg solo vive en el núcleo.",
    ),
    "nucleo": dict(
        nombre="Núcleo (cromatina)", aminos=list("KR"), niveles=(5, 8),
        glifo="§", color="POS",
        por_que="Las histonas son ricas en Lys y Arg: sus cargas + abrazan al ADN, cargado (−) por sus fosfatos. Para entrar, tu proteína necesita una señal de localización nuclear (NLS).",
    ),
    "nucleolo": dict(
        nombre="Nucléolo", aminos=list("RG"), niveles=(6, 8),
        glifo="▓", color="POS",
        por_que="Aquí se ensamblan los ribosomas. Proteínas como la nucleolina repiten Arg-Gly-Gly: las Arg (+) se unen al ARN (−) y las Gly le dan flexibilidad.",
    ),
    "re": dict(
        nombre="Retículo endoplásmico", aminos=list("DE"), niveles=(4, 7),
        glifo="░", color="NEG",
        por_que="Aquí viven los ácidos (−): el RE guarda Ca²+, y proteínas como la calreticulina lo retienen con muchos Asp y Glu.",
    ),
    "golgi": dict(
        nombre="Aparato de Golgi", aminos=list("NST"), niveles=(4, 7),
        glifo="═", color="POL",
        por_que="Aquí se recortan y amplían los N-glicanos que la Asn trae "
                "del RE, y se añaden O-glicanos (O-GalNAc) al OH de Ser y Thr.",
    ),
    "lisosoma": dict(
        nombre="Lisosoma", aminos=list("HC"), niveles=(5, 8),
        glifo="●", color="NEG",
        por_que="pH ≈ 4.5–5, por debajo del pKR de la His (6): aquí queda protonada (+). Sus proteasas (catepsinas B y L) usan una Cys catalítica junto a una His.",
    ),
    "mec": dict(
        nombre="Matriz extracelular", aminos=list("GP"), niveles=(5, 8),
        glifo="×", color="tenue",
        por_que="Aquí viven Gly y Pro: el colágeno repite Gly-Pro-Hyp. La Gly "
                "es la única que cabe en el centro de la triple hélice y la "
                "Pro la rigidiza.",
    ),
    "mitocondria": dict(
        nombre="Mitocondria", aminos=[], niveles=(0, 0),
        glifo="Θ", color="titulo",
        por_que="La fosforilación oxidativa produce ATP: aquí tu equipo restablece su energía y tú recargas ATP.",
    ),
}


# =============================================================== glosario
GLOSARIO = [
    ("pH fisiológico", "Sangre ≈ 7.4, citosol ≈ 7.2, lisosoma ≈ 4.5–5."),
    ("pKa", "pH al que un grupo está 50% protonado. Si pH < pKa el grupo "
            "está mayormente protonado; si pH > pKa, desprotonado."),
    ("pK1, pK2, pKR", "pK1 = α-COOH (~2), pK2 = α-NH3+ (~9–10), pKR = cadena "
                      "lateral (solo D, E, H, C, Y, K, R)."),
    ("pI (punto isoeléctrico)", "pH al que la carga neta es 0. Se calcula "
                                "promediando los dos pKa que flanquean la "
                                "especie neutra: ácidos → (pK1 + pKR)/2; "
                                "básicos → (pK2 + pKR)/2; sin cadena "
                                "ionizable → (pK1 + pK2)/2."),
    ("Carga a pH 7", "Asp y Glu (pKR ~4) ya perdieron su H+: son −. Lys y "
                     "Arg (pKR >10) aún lo tienen: son +. His (pKR 6) está "
                     "casi siempre neutra."),
    ("pKR en proteínas", "Los pKR de la tabla son del aminoácido libre. "
                         "Dentro de una proteína cambian según el "
                         "microambiente (una His o Cys de sitio activo puede "
                         "moverse varias unidades). Para docking o asignar "
                         "protonación se usa PROPKA."),
    ("Hidropatía (KD)", "Escala de Kyte-Doolittle: positivo = hidrofóbico "
                        "(Ile 4.5), negativo = hidrofílico (Arg −4.5)."),
    ("No polar ≠ hidrofóbico", "No polar habla de la química del grupo R "
                               "(sin O–H ni N–H, no forma puentes de H). "
                               "Hidrofóbico habla de cuánto le conviene esconderse "
                               "del agua, y eso depende de su superficie de C–H. "
                               "Por eso Gly (no polar) tiene KD −0.4 y Cys (polar) "
                               "tiene KD +2.5."),
    ("GRAVY", "Promedio de la hidropatía de una secuencia. > 0 tiende a "
              "estar en membranas; < 0, soluble en agua."),
    ("Carga neta", "Suma de cargas: +1 por K y R, −1 por D y E (His ≈ 0 a "
                   "pH 7, ≈ +1 a pH 5)."),
    ("Esencial", "No lo sintetizamos (o no a la velocidad necesaria). Son 9: "
                 "His, Ile, Leu, Lys, Met, Phe, Thr, Trp, Val."),
    ("Condicionalmente esencial", "Normalmente se sintetiza, pero no alcanza "
                                  "en prematuridad, estrés, enfermedad o "
                                  "crecimiento rápido. Son 6: Arg, Cys, Gln, "
                                  "Gly, Pro, Tyr."),
    ("No esencial", "Son 5: Ala, Asp, Asn, Glu, Ser."),
    ("Código de 1 letra", "Los menos intuitivos: F=Phe, Y=Tyr, W=Trp, N=Asn, Q=Gln, "
                          "D=Asp, E=Glu, K=Lys, R=Arg."),
    ("Codón / anticodón", "Triplete del ARNm y su complemento en el ARNt "
                          "(antiparalelo). AUG = Met = inicio."),
    ("Modificación covalente", "Enlace nuevo en la cadena lateral de un residuo de una "
                               "proteína. Cotraduccional si ocurre mientras el ribosoma "
                               "traduce (N-glicosilación) y postraduccional si ocurre "
                               "después (fosforilación, acetilación)."),
    ("Puente salino", "Atracción entre una carga + y una − (Lys–Asp)."),
    ("Efecto hidrofóbico", "Las cadenas no polares se juntan porque así "
                           "liberan agua ordenada a su alrededor."),
    ("Catión–π", "Una carga + (Lys, Arg) se pega a la cara de un anillo "
                 "aromático (Phe, Tyr, Trp)."),
    ("Puente disulfuro", "Enlace covalente S–S entre dos Cys (oxidación). "
                         "Lehninger: los residuos unidos así (cistina) son "
                         "fuertemente hidrofóbicos."),
    ("Clasificación", "Los tipos del juego son los 5 grupos de Lehninger: no "
                      "polar alifático, aromático, polar sin carga, cargado + "
                      "y cargado −. Otras fuentes ponen Gly, Cys o Trp en "
                      "otros grupos según la escala de hidrofobicidad."),
]


# ============================================================ traducción
# Las claves de OBJETOS se quedan en español: son las del archivo de guardado.
traducir(TIPOS, "nombre", "corto", "desc")
GRUPOS = {k: tr(v) for k, v in GRUPOS.items()}
NUTRICION = {tr(k): tr(v) for k, v in NUTRICION.items()}
traducir(AMINOACIDOS, "nombre", "carga", "nutricion", "pista")
NOTA_KD = {k: tr(v) for k, v in NOTA_KD.items()}
traducir(MODIFICACIONES, "nombre", "carga", "cambio", "bio", "pista", "matiz")
OBJETOS = {k: tr(v) for k, v in OBJETOS.items()}
traducir(ZONAS, "nombre", "por_que")
GLOSARIO = [(tr(a), tr(b)) for a, b in GLOSARIO]
traducir(PEPTIDOS, "nombre", "bio")
SEC["nombre"], SEC["carga"] = tr(SEC["nombre"]), tr(SEC["carga"])
SEC["grupo_r"] = tuple(tr(x) for x in SEC["grupo_r"])


# ============================================================ utilidades
def forma(fid):
    """Datos de un aminoácido o de un residuo modificado con interfaz común."""
    if fid == "U":
        return dict(id="U", base="U", nombre=SEC["nombre"], tres="Sec", tipos=SEC["tipos"],
                    carga=SEC["carga"], masa=SEC["masa"], movs=movimientos_de("U"),
                    arte=arte(SEC), evo=False)
    if fid in AMINOACIDOS:
        aa = AMINOACIDOS[fid]
        return dict(
            id=fid, base=fid, nombre=aa["nombre"], tres=aa["tres"],
            tipos=tuple(aa["tipos"]), carga=aa["carga"], masa=aa["masa"],
            movs=movimientos_de(fid), arte=arte(aa), evo=False,
        )
    ev = MODIFICACIONES[fid]
    base = AMINOACIDOS[ev["base"]]
    return dict(
        id=fid, base=ev["base"], nombre=ev["nombre"], tres=ev["tres"],
        tipos=tuple(ev["tipos"]), carga=ev["carga"], masa=base["masa"] + 40,
        movs=movimientos_de(fid), arte=arte(ev), evo=True,
    )


def arte(d):
    if d.get("completa"):
        return list(d["completa"])
    return ESQUELETO + d["cadena"]


def modificaciones_de(base):
    return [k for k, v in MODIFICACIONES.items() if v["base"] == base]


def nombre_tipos(tipos, corto=False):
    clave = "corto" if corto else "nombre"
    return " / ".join(TIPOS[t][clave] for t in tipos)


def zonas_de(aa):
    return [z for z, info in ZONAS.items() if aa in info["aminos"]]
