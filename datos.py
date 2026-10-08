"""Datos de los 20 aminoácidos estándar, sus modificaciones
postraduccionales, tipos, movimientos, zonas del mapa y glosario.

Valores fisicoquímicos: Lehninger, 25 °C (masa del aminoácido libre en g/mol;
pK1 = α-COOH, pK2 = α-NH3+, pKR = cadena lateral, pI = punto isoeléctrico).
Hidropatía: escala de Kyte-Doolittle (1982).
"""

# ================================================================== tipos
# Los tipos son los 5 grupos de Lehninger (según la cadena lateral R).
# Solo los aromáticos llevan un segundo tipo, tomado del propio Lehninger:
# "Phe, Tyr y Trp son relativamente no polares; Tyr y Trp son bastante más
# polares que Phe (por el OH de Tyr y el N del indol de Trp)".
TIPOS = {
    "NP": dict(
        nombre="No polar alifático", corto="No polar",
        desc="Cadena de C e H (Gly, Ala, Pro, Val, Leu, Ile, Met). No forma "
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
for (_a, _b), _v in _PARES.items():
    EFECTIVIDAD[_a][_b] = _v
    EFECTIVIDAD[_b][_a] = _v


def multiplicador(tipo_mov, tipos_def):
    """Multiplicador total contra un defensor de uno o dos tipos.
    Devuelve (multiplicador, [(tipo_def, mult_parcial, interacción)])."""
    if tipo_mov == NEUTRO:
        return 1.0, [(t, 1, "interacción del esqueleto / van der Waals") for t in tipos_def]
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
    "acido": "Ácido (carga −)",
    "basico": "Básico (carga +)",
}

NUTRICION = {
    "Esencial": "No la sintetizamos (o no lo bastante rápido): debe venir de "
                "la dieta.",
    "Condicional": "Normalmente se sintetiza, pero en prematuridad, estrés "
                   "metabólico, enfermedad o crecimiento rápido la síntesis no "
                   "alcanza.",
    "No esencial": "La sintetizamos en cantidad suficiente.",
}

# ============================================================ aminoácidos
# cadena: líneas debajo del Cα. completa: estructura entera (solo Pro).
AMINOACIDOS = {
    "G": dict(
        nombre="Glicina", tres="Gly", grupo="alifatico", tipos=("NP",),
        carga="Neutra", pk1=2.34, pk2=9.60, pkr=None, pi=5.97,
        hidropatia=-0.4, masa=75.07, nutricion="Condicional", codones=["GGU", "GGC", "GGA", "GGG"],
        cadena=["        H"],
        pista="La más pequeña y la única sin carbono quiral (su R es un H). "
              "Es 1 de cada 3 residuos del colágeno.",
    ),
    "A": dict(
        nombre="Alanina", tres="Ala", grupo="alifatico", tipos=("NP",),
        carga="Neutra", pk1=2.34, pk2=9.69, pkr=None, pi=6.01,
        hidropatia=1.8, masa=89.09, nutricion="No esencial", codones=["GCU", "GCC", "GCA", "GCG"],
        cadena=["        CH3"],
        pista="Un simple metilo. Es la mejor formadora de hélices α y viaja "
              "del músculo al hígado en el ciclo glucosa-alanina.",
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
        pista="Ramificada en β (forma de 'V'). Aminoácido de cadena "
              "ramificada (BCAA) como Leu e Ile.",
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
        pista="Isobutilo. Forma cremalleras de leucina en factores de "
              "transcripción como Fos y Jun.",
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
        pista="La más hidrofóbica (KD 4.5). Tiene dos carbonos quirales "
              "(Cα y Cβ). Isómero de Leu.",
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
        pista="Tioéter (S sin H). AUG es el codón de inicio: toda proteína "
              "empieza con Met. Da origen a la SAM, el donador de metilos.",
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
        pista="Su α-amino es secundario: la cadena lateral se cierra sobre el N. "
              "Ese anillo rígido rompe hélices α y forma giros. Su pK2 (10.96) "
              "es el más alto de todos.",
    ),
    "F": dict(
        nombre="Fenilalanina", tres="Phe", grupo="aromatico", tipos=("ARO", "NP"),
        carga="Neutra", pk1=1.83, pk2=9.13, pkr=None, pi=5.48,
        hidropatia=2.8, masa=165.19, nutricion="Esencial", codones=["UUU", "UUC"],
        cadena=["        CH2", "        |"] + BENCENO + ["        CH"],
        pista="Bencilo. La fenilalanina hidroxilasa la convierte en Tyr; "
              "si falla esa enzima → fenilcetonuria (PKU).",
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
        pista="Phe + OH (fenol). Absorbe a 280 nm. Precursora de dopamina, "
              "adrenalina, melanina y hormonas tiroideas.",
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
        pista="Indol (anillo doble con N). El más grande y el que más "
              "absorbe a 280 nm. Precursor de serotonina y melatonina.",
    ),
    "S": dict(
        nombre="Serina", tres="Ser", grupo="polar", tipos=("POL",),
        carga="Neutra", pk1=2.21, pk2=9.15, pkr=None, pi=5.68,
        hidropatia=-0.8, masa=105.09, nutricion="No esencial",
        codones=["UCU", "UCC", "UCA", "UCG", "AGU", "AGC"],
        cadena=["        CH2", "        |", "        OH"],
        pista="Hidroximetilo. Nucleófilo de las serín-proteasas "
              "(tripsina, quimotripsina). Blanco clásico de quinasas.",
    ),
    "T": dict(
        nombre="Treonina", tres="Thr", grupo="polar", tipos=("POL",),
        carga="Neutra", pk1=2.11, pk2=9.62, pkr=None, pi=5.87,
        hidropatia=-0.7, masa=119.12, nutricion="Esencial", codones=["ACU", "ACC", "ACA", "ACG"],
        cadena=["        CH-OH", "        |", "        CH3"],
        pista="Como Ser pero con un CH3 extra; también tiene dos carbonos "
              "quirales. Se fosforila igual que Ser.",
    ),
    "C": dict(
        nombre="Cisteína", tres="Cys", grupo="polar", tipos=("POL",),
        carga="Neutra", pk1=1.96, pk2=10.28, pkr=8.18, pi=5.07,
        hidropatia=2.5, masa=121.16, nutricion="Condicional", codones=["UGU", "UGC"],
        cadena=["        CH2", "        |", "        SH"],
        pista="Tiol (SH). Dos Cys se oxidan y forman un puente disulfuro "
              "(cistina). Lehninger la clasifica como polar sin carga, aunque "
              "su KD (+2.5) indica que es bastante hidrofóbica.",
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
        pista="Amida de Asp. Primer aminoácido aislado (de los espárragos). "
              "Sitio de N-glicosilación (secuón N-X-S/T).",
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
        pista="Amida de Glu. El aminoácido más abundante en sangre: "
              "transporta nitrógeno (NH3) de forma no tóxica.",
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
        pista="Carboxilato a pH 7. El pI más bajo de todos (2.77). Dona N al "
              "ciclo de la urea y forma parte de la tríada catalítica "
              "(Ser-His-Asp).",
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
        pista="Un CH2 más que Asp. Principal neurotransmisor excitador y "
              "sabor 'umami'. Centro del metabolismo del nitrógeno; precursor "
              "de Gln y Pro.",
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
        pista="Cadena de 4 CH2 con amonio. Abunda en histonas y proteínas "
              "ribosomales; se acetila, metila y ubiquitina.",
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
        pista="Guanidinio: la base más fuerte (pKR 12.5), siempre +. El pI "
              "más alto (10.76) y la más hidrofílica (KD −4.5). Origen del "
              "óxido nítrico (NO).",
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
        pista="Imidazol con pKR ≈ 6: a pH 7 solo ~10% está "
              "protonada, a pH 5 casi toda. Por eso cede o toma H+ en sitios "
              "activos y en la hemoglobina.",
    ),
}

# Casos en los que el grupo de Lehninger y el signo de KD parecen contradecirse.
# KD combina la energía de pasar del agua al vapor con qué tan seguido aparece
# enterrado cada residuo en proteínas de estructura conocida.
NOTA_KD = {
    "G": "No polar no es lo mismo que hidrofóbico. La Gly es no polar porque su "
         "R es un H, pero ese H no tiene superficie que esconder del agua: el "
         "efecto hidrofóbico crece con la superficie de C–H que se entierra. Sin "
         "cadena lateral pesa más su esqueleto polar (N–H y C=O), por eso KD ≈ 0 "
         "(−0.4). Lehninger: es formalmente no polar, pero su cadena tan pequeña "
         "no contribuye de verdad a las interacciones hidrofóbicas.",
    "P": "Su anillo es de C–H, pero KD −1.6: rompe hélices y suele quedar en "
         "giros y lazos expuestos al agua, en la superficie de la proteína.",
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


# ============================================ modificaciones postraduccionales
MODIFICACIONES = {
    "Hyp": dict(
        base="P", nombre="Hidroxiprolina", tres="Hyp", tipos=("POL",),
        carga="Neutra", req=dict(nivel=5, objeto="Vitamina C"),
        cambio="Gana un OH en el anillo: de No polar a Polar sin carga.",
        bio="La prolil 4-hidroxilasa (en el RE) le pone un OH usando vitamina "
            "C (ascorbato) como cofactor. La Hyp estabiliza la triple hélice "
            "del colágeno; sin vitamina C el colágeno se deshace → escorbuto.",
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
        cambio="Conserva la carga + (sigue en el grupo básico) y gana un OH "
               "en el carbono δ.",
        bio="La lisil hidroxilasa (también dependiente de vitamina C) la "
            "forma en el RE. Sus OH reciben azúcares y crean entrecruzamientos "
            "que dan resistencia a las fibras de colágeno.",
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
        bio="Las acetiltransferasas de histonas (HAT) le pasan un acetilo del "
            "acetil-CoA. Sin carga +, la histona suelta al ADN (−): la "
            "cromatina se abre y los genes se expresan. Las HDAC lo revierten.",
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
        cambio="Sigue siendo + (amonio cuaternario: ya no puede perder la "
               "carga ni acetilarse, porque su N no tiene H).",
        bio="Las metiltransferasas de histonas (HMT) usan SAM, derivada de la "
            "Met. H3K4me3 marca genes activos; H3K9me3 y H3K27me3, genes "
            "silenciados. No cambia la carga, cambia quién se une.",
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
        bio="Las Ser/Thr quinasas (PKA, PKC, MAPK…) le transfieren el "
            "fosfato γ del ATP. Es el interruptor más común de la célula; las "
            "fosfatasas lo quitan.",
        pista="La mitocondria (◉) recarga ATP.",
        cadena=["        CH2", "        |", "        O", "        |",
                "        PO3(2-)"],
    ),
    "pT": dict(
        base="T", nombre="Fosfotreonina", tres="pThr", tipos=("NEG",),
        carga="Negativa (≈ −2)", req=dict(nivel=4, objeto="ATP"),
        cambio="Gana un fosfato: de Polar sin carga a Cargado − (≈ −2).",
        bio="Mismas Ser/Thr quinasas que la serina. El motivo pThr-Pro lo "
            "reconoce la isomerasa Pin1 y controla el ciclo celular (CDKs).",
        pista="La mitocondria (◉) recarga ATP.",
        cadena=["        CH-O-PO3(2-)", "        |", "        CH3"],
    ),
    "pY": dict(
        base="Y", nombre="Fosfotirosina", tres="pTyr", tipos=("NEG", "ARO"),
        carga="Negativa (≈ −2)", req=dict(nivel=5, objeto="ATP"),
        cambio="El OH del fenol se fosforila: conserva el anillo, pero ahora "
               "tiene carga ≈ −2 (Cargado − / Aromático).",
        bio="Las tirosina quinasas (como el receptor de insulina, un RTK) la "
            "generan. Los dominios SH2 la reconocen con una Arg que forma un "
            "puente salino con el fosfato, y así propagan la señal.",
        pista="La mitocondria (◉) recarga ATP.",
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
        bio="En el RE (ambiente oxidante) la PDI, proteína disulfuro "
            "isomerasa, forma y reacomoda puentes S–S. Estabilizan proteínas "
            "que salen de la célula: insulina, anticuerpos, queratina.",
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
        cambio="Gana un segundo carboxilo en el carbono γ: carga ≈ −2.",
        bio="La γ-glutamil carboxilasa (en el RE) usa vitamina K. Los Gla de "
            "la protrombina y los factores VII, IX y X atrapan Ca²⁺ y anclan "
            "los factores a la membrana: sin vit. K no hay coagulación (la "
            "warfarina bloquea este ciclo).",
        pista="Hay vitamina K en el retículo (K en el mapa).",
        cadena=[
            "        CH2", "        |", "        CH",
            "       /  \\", "   -OOC    COO-",
        ],
    ),
    "Nglc": dict(
        base="N", nombre="Asn N-glicosilada", tres="Asn-Glc", tipos=("POL",),
        carga="Neutra", req=dict(nivel=5, zona="re"),
        cambio="Se le une un árbol de azúcares al N de la amida: aún más polar.",
        bio="La oligosacariltransferasa (OST) del RE la añade en el secuón "
            "N-X-S/T (X ≠ Pro). Los glicanos ayudan al plegamiento (ciclo "
            "calnexina/calreticulina) y al control de calidad.",
        pista="La OST trabaja en el retículo endoplásmico.",
        cadena=[
            "        CH2", "        |", "        C", "       // \\",
            "      O    NH", "             \\", "             GlcNAc-GlcNAc-Man…",
        ],
    ),
    "gS": dict(
        base="S", nombre="Ser O-glicosilada", tres="Ser-GalNAc", tipos=("POL",),
        carga="Neutra", req=dict(nivel=5, zona="golgi"),
        cambio="Se le une una N-acetilgalactosamina (GalNAc) al O del OH: sigue "
               "siendo polar, pero ahora carga un azúcar.",
        bio="Las GalNAc-transferasas (GALNT) del Golgi le ponen la GalNAc y luego "
            "se alarga a un O-glicano tipo mucina. A diferencia de la "
            "N-glicosilación de la Asn (en el RE, sobre el secuón N-X-S/T), no "
            "tiene secuencia consenso y empieza en el Golgi. La GalNAc sola es el "
            "antígeno Tn, que aparece en muchos tumores.",
        pista="Las GALNT trabajan en el aparato de Golgi.",
        cadena=["        CH2", "        |", "        O", "        |", "        GalNAc…"],
    ),
    "gT": dict(
        base="T", nombre="Thr O-glicosilada", tres="Thr-GalNAc", tipos=("POL",),
        carga="Neutra", req=dict(nivel=5, zona="golgi"),
        cambio="Se le une una GalNAc al O del OH: sigue siendo polar, pero ahora "
               "carga un azúcar.",
        bio="Mismas GalNAc-transferasas del Golgi; muchas prefieren Thr. En las "
            "mucinas, los tramos ricos en Pro, Thr y Ser (PTS) quedan cubiertos de "
            "O-glicanos que atrapan agua: así se forma el moco.",
        pista="Las GALNT trabajan en el aparato de Golgi.",
        cadena=["        CH-O-GalNAc…", "        |", "        CH3"],
    ),
    "Cit": dict(
        base="R", nombre="Citrulina", tres="Cit", tipos=("POL",),
        carga="Neutra", req=dict(nivel=6),
        cambio="Pierde la carga +: el guanidinio se vuelve una urea neutra "
               "(de Cargado + a Polar sin carga).",
        bio="Las PAD (peptidil-arginina deiminasas, dependientes de Ca²⁺) la "
            "generan. PAD4 citrulina histonas en las trampas de neutrófilos "
            "(NETs). En la artritis reumatoide aparecen anticuerpos anti-CCP. "
            "La citrulina libre también es parte del ciclo de la urea.",
        pista="Solo requiere nivel.",
        cadena=[
            "        CH2", "        |", "        CH2", "        |",
            "        CH2", "        |", "        NH", "        |",
            "        C", "       // \\", "      O    NH2",
        ],
    ),
}

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
    "A": ("metilo", "–CH₃", "alquilo"),
    "V": ("isopropilo", "–CH(CH₃)₂", "alquilo ramificado"),
    "L": ("isobutilo", "–CH₂CH(CH₃)₂", "alquilo ramificado"),
    "I": ("sec-butilo", "–CH(CH₃)CH₂CH₃", "alquilo ramificado"),
    "M": ("metiltioetilo", "–CH₂CH₂–S–CH₃", "tioéter"),
    "P": ("pirrolidina", "–CH₂CH₂CH₂– (cerrado sobre el N)", "amina secundaria cíclica"),
    "F": ("bencilo", "–CH₂–C₆H₅", "fenilo"),
    "Y": ("p-hidroxibencilo", "–CH₂–C₆H₄–OH", "fenol"),
    "W": ("indolilmetilo", "–CH₂–indol", "indol"),
    "S": ("hidroximetilo", "–CH₂–OH", "alcohol primario"),
    "T": ("1-hidroxietilo", "–CH(OH)–CH₃", "alcohol secundario"),
    "C": ("sulfanilmetilo", "–CH₂–SH", "tiol"),
    "N": ("carbamoilmetilo", "–CH₂–CONH₂", "amida"),
    "Q": ("2-carbamoiletilo", "–CH₂CH₂–CONH₂", "amida"),
    "D": ("carboximetilo", "–CH₂–COO⁻", "carboxilato"),
    "E": ("2-carboxietilo", "–CH₂CH₂–COO⁻", "carboxilato"),
    "K": ("4-aminobutilo", "–(CH₂)₄–NH₃⁺", "amonio primario"),
    "R": ("3-guanidinopropilo", "–(CH₂)₃–NH–C(NH₂)₂⁺", "guanidinio"),
    "H": ("imidazolilmetilo", "–CH₂–imidazol", "imidazol"),
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
}


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
        "2 R–SH → R–S–S–R + 2H⁺ + 2e⁻ (oxidación)."),
}
MOVIMIENTOS["puente_disulfuro"]["efecto"] = "disulfuro"
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
        nombre="Polirribosomas", aminos=list("K"), niveles=(3, 5),
        glifo="∴", color="POS",
        por_que="Las proteínas ribosomales son muy ricas en Lys: sus cargas + "
                "neutralizan los fosfatos (−) del ARN ribosomal. Aquí "
                "consigues las Lys para tu NLS; la Arg solo vive dentro del "
                "núcleo.",
    ),
    "nucleo": dict(
        nombre="Núcleo (cromatina)", aminos=list("KR"), niveles=(5, 8),
        glifo="§", color="POS",
        por_que="Las histonas son ricas en Lys y Arg y abrazan al ADN, "
                "cargado (−) por sus fosfatos; H3 y H4 son las histonas "
                "«ricas en Arg». La Arg solo aparece aquí y en el nucléolo. "
                "Para entrar, tu proteína necesita una señal de localización "
                "nuclear (NLS).",
    ),
    "nucleolo": dict(
        nombre="Nucléolo", aminos=list("RG"), niveles=(6, 8),
        glifo="▓", color="POS",
        por_que="Aquí se ensamblan los ribosomas. La nucleolina y la "
                "fibrilarina tienen dominios RGG/GAR (repeticiones Arg-Gly-Gly) "
                "que se unen al ARN.",
    ),
    "re": dict(
        nombre="Retículo endoplásmico", aminos=list("DE"), niveles=(4, 7),
        glifo="░", color="NEG",
        por_que="Aquí viven los ácidos (−): el RE es el almacén de Ca²⁺ de "
                "la célula y proteínas como la calreticulina están llenas de "
                "Asp y Glu para retenerlo. Su membrana es continua con la "
                "envoltura nuclear.",
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
        por_que="pH ≈ 4.5–5: la His (pKR 6) queda protonada (+). Las "
                "catepsinas B y L son cisteín-proteasas: su Cys catalítica "
                "trabaja junto con una His (díada catalítica).",
    ),
    "mec": dict(
        nombre="Matriz extracelular", aminos=list("GP"), niveles=(5, 8),
        glifo="╳", color="tenue",
        por_que="Aquí viven Gly y Pro: el colágeno repite Gly-Pro-Hyp. La Gly "
                "es la única que cabe en el centro de la triple hélice y la "
                "Pro la rigidiza.",
    ),
    "mitocondria": dict(
        nombre="Mitocondria", aminos=[], niveles=(0, 0),
        glifo="◉", color="titulo",
        por_que="La fosforilación oxidativa produce ATP: aquí tu equipo "
                "restablece su energía y recargas ATP. También es donde se "
                "degradan los aminoácidos ramificados (Val, Leu, Ile).",
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
    ("Modificación postraduccional", "Cambio químico tras la traducción: "
                                     "fosforilación, acetilación, "
                                     "hidroxilación, glicosilación…"),
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


# ============================================================ utilidades
def forma(fid):
    """Datos de un aminoácido o de un residuo modificado con interfaz común."""
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
