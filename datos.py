"""Datos de los 20 aminoácidos estándar, sus evoluciones (modificaciones
postraduccionales), tipos, movimientos, zonas del mapa y glosario.

Valores fisicoquímicos: Lehninger, 25 °C (masa del aminoácido libre en g/mol;
pK1 = α-COOH, pK2 = α-NH3+, pKR = cadena lateral, pI = punto isoeléctrico).
Hidropatía: escala de Kyte-Doolittle (1982).
Requerimientos: FAO/OMS/UNU 2007, adulto, mg/kg/día.
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
    ("NP", "POL"): (0.5, "el agua solvata al grupo polar: no se juntan"),
    ("NP", "POS"): (0.5, "el agua solvata la carga: no se juntan"),
    ("NP", "NEG"): (0.5, "el agua solvata la carga: no se juntan"),
    ("ARO", "ARO"): (2, "apilamiento π–π"),
    ("ARO", "POL"): (1, "puente de H débil con la nube π"),
    ("ARO", "POS"): (2, "interacción catión–π"),
    ("ARO", "NEG"): (0.5, "la cara π (rica en electrones) repele al anión"),
    ("POL", "POL"): (2, "puentes de hidrógeno"),
    ("POL", "POS"): (1, "puente de H con el grupo cargado"),
    ("POL", "NEG"): (1, "puente de H con el carboxilato"),
    ("POS", "POS"): (0, "repulsión electrostática (+ con +)"),
    ("POS", "NEG"): (2, "puente salino"),
    ("NEG", "NEG"): (0, "repulsión electrostática (− con −)"),
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
        hidropatia=-0.4, masa=75.07, nutricion="Condicional",
        precursor="Serina", nota_nutricion="Se sintetiza desde Ser (serina "
                                         "hidroximetiltransferasa).",
        destino="Glucogénico", codones=["GGU", "GGC", "GGA", "GGG"],
        movs=["puente_h_esqueleto", "flexibilidad", "van_der_waals"],
        cadena=["        H"],
        pista="La más pequeña y la única sin carbono quiral (su R es un H). "
              "Es 1 de cada 3 residuos del colágeno.",
    ),
    "A": dict(
        nombre="Alanina", tres="Ala", grupo="alifatico", tipos=("NP",),
        carga="Neutra", pk1=2.34, pk2=9.69, pkr=None, pi=6.01,
        hidropatia=1.8, masa=89.09, nutricion="No esencial",
        destino="Glucogénico", codones=["GCU", "GCC", "GCA", "GCG"],
        movs=["efecto_hidrofobico", "helice_alfa", "van_der_waals"],
        cadena=["        CH3"],
        pista="Un simple metilo. Es la mejor formadora de hélices α y viaja "
              "del músculo al hígado en el ciclo glucosa-alanina.",
    ),
    "V": dict(
        nombre="Valina", tres="Val", grupo="alifatico", tipos=("NP",),
        carga="Neutra", pk1=2.32, pk2=9.62, pkr=None, pi=5.97,
        hidropatia=4.2, masa=117.15, nutricion="Esencial", req=26,
        destino="Glucogénico", codones=["GUU", "GUC", "GUA", "GUG"],
        movs=["efecto_hidrofobico", "lamina_beta", "van_der_waals"],
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
        hidropatia=3.8, masa=131.17, nutricion="Esencial", req=39,
        destino="Cetogénico",
        codones=["UUA", "UUG", "CUU", "CUC", "CUA", "CUG"],
        movs=["efecto_hidrofobico", "cremallera", "van_der_waals"],
        cadena=[
            "        CH2",
            "        |",
            "        CH",
            "       /  \\",
            "    H3C    CH3",
        ],
        pista="Isobutilo. Forma 'cremalleras de leucina' en factores de "
              "transcripción. Junto con Lys, es puramente cetogénica. Es el "
              "esencial que más se requiere (39 mg/kg/día).",
    ),
    "I": dict(
        nombre="Isoleucina", tres="Ile", grupo="alifatico", tipos=("NP",),
        carga="Neutra", pk1=2.36, pk2=9.68, pkr=None, pi=6.02,
        hidropatia=4.5, masa=131.17, nutricion="Esencial", req=20,
        destino="Ambos", codones=["AUU", "AUC", "AUA"],
        movs=["efecto_hidrofobico", "nucleo_hidrofobico", "lamina_beta", "van_der_waals"],
        cadena=[
            "    H3C-CH",
            "        |",
            "        CH2",
            "        |",
            "        CH3",
        ],
        pista="La más hidrofóbica (KD 4.5). Tiene DOS carbonos quirales "
              "(Cα y Cβ). Isómero de Leu.",
    ),
    "M": dict(
        nombre="Metionina", tres="Met", grupo="alifatico", tipos=("NP",),
        carga="Neutra", pk1=2.28, pk2=9.21, pkr=None, pi=5.74,
        hidropatia=1.9, masa=149.21, nutricion="Esencial", req=15,
        req_nota="15 mg/kg/día es para Met + Cys juntas (la Cys sale de la Met).",
        destino="Glucogénico", codones=["AUG"],
        movs=["codon_inicio", "efecto_hidrofobico", "tioeter", "antioxidante"],
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
        hidropatia=-1.6, masa=115.13, nutricion="Condicional",
        precursor="Glutamato", nota_nutricion="Se sintetiza desde Glu.",
        destino="Glucogénico", codones=["CCU", "CCC", "CCA", "CCG"],
        movs=["efecto_hidrofobico", "anillo_rigido", "van_der_waals"],
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
        pista="Iminoácido: su cadena se cierra sobre el N del esqueleto. "
              "Ese anillo rígido rompe hélices α y forma giros. Su pK2 (10.96) "
              "es el más alto de todos.",
    ),
    "F": dict(
        nombre="Fenilalanina", tres="Phe", grupo="aromatico", tipos=("ARO", "NP"),
        carga="Neutra", pk1=1.83, pk2=9.13, pkr=None, pi=5.48,
        hidropatia=2.8, masa=165.19, nutricion="Esencial", req=25,
        req_nota="25 mg/kg/día es para Phe + Tyr juntas (la Tyr sale de la Phe).",
        destino="Ambos", codones=["UUU", "UUC"],
        movs=["apilamiento_pi", "efecto_hidrofobico", "van_der_waals"],
        cadena=["        CH2", "        |"] + BENCENO + ["        CH"],
        pista="Bencilo. La fenilalanina hidroxilasa la convierte en Tyr; "
              "si falla esa enzima → fenilcetonuria (PKU).",
    ),
    "Y": dict(
        nombre="Tirosina", tres="Tyr", grupo="aromatico", tipos=("ARO", "POL"),
        carga="Neutra", pk1=2.20, pk2=9.11, pkr=10.07, pi=5.66,
        hidropatia=-1.3, masa=181.19, nutricion="Condicional",
        precursor="Fenilalanina",
        nota_nutricion="Depende de Phe (fenilalanina hidroxilasa); en la PKU "
                       "se vuelve esencial.",
        destino="Ambos", codones=["UAU", "UAC"],
        movs=["apilamiento_pi", "puente_h", "fosforilar"],
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
        hidropatia=-0.9, masa=204.23, nutricion="Esencial", req=4,
        destino="Ambos", codones=["UGG"],
        movs=["apilamiento_pi", "fluorescencia", "puente_h", "van_der_waals"],
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
              "absorbe a 280 nm. Precursor de serotonina y melatonina. El "
              "esencial que menos se requiere (4 mg/kg/día).",
    ),
    "S": dict(
        nombre="Serina", tres="Ser", grupo="polar", tipos=("POL",),
        carga="Neutra", pk1=2.21, pk2=9.15, pkr=None, pi=5.68,
        hidropatia=-0.8, masa=105.09, nutricion="No esencial",
        destino="Glucogénico",
        codones=["UCU", "UCC", "UCA", "UCG", "AGU", "AGC"],
        movs=["puente_h", "fosforilar", "van_der_waals"],
        cadena=["        CH2", "        |", "        OH"],
        pista="Hidroximetilo. Nucleófilo de las serín-proteasas "
              "(tripsina, quimotripsina). Blanco clásico de quinasas.",
    ),
    "T": dict(
        nombre="Treonina", tres="Thr", grupo="polar", tipos=("POL",),
        carga="Neutra", pk1=2.11, pk2=9.62, pkr=None, pi=5.87,
        hidropatia=-0.7, masa=119.12, nutricion="Esencial", req=15,
        destino="Ambos", codones=["ACU", "ACC", "ACA", "ACG"],
        movs=["puente_h", "fosforilar", "lamina_beta"],
        cadena=["        CH-OH", "        |", "        CH3"],
        pista="Como Ser pero con un CH3 extra; también tiene dos carbonos "
              "quirales. Se fosforila igual que Ser.",
    ),
    "C": dict(
        nombre="Cisteína", tres="Cys", grupo="polar", tipos=("POL",),
        carga="Neutra", pk1=1.96, pk2=10.28, pkr=8.18, pi=5.07,
        hidropatia=2.5, masa=121.16, nutricion="Condicional",
        precursor="Metionina",
        nota_nutricion="Depende de Met (transulfuración, junto con Ser).",
        destino="Glucogénico", codones=["UGU", "UGC"],
        movs=["puente_disulfuro", "tiol", "van_der_waals"],
        cadena=["        CH2", "        |", "        SH"],
        pista="Tiol (SH). Dos Cys se oxidan y forman un puente disulfuro "
              "(cistina). Lehninger la pone con las polares sin carga, aunque "
              "su KD (+2.5) dice que es bastante hidrofóbica.",
    ),
    "N": dict(
        nombre="Asparagina", tres="Asn", grupo="polar", tipos=("POL",),
        carga="Neutra", pk1=2.02, pk2=8.80, pkr=None, pi=5.41,
        hidropatia=-3.5, masa=132.12, nutricion="No esencial",
        destino="Glucogénico", codones=["AAU", "AAC"],
        movs=["puente_h", "amida_doble", "van_der_waals"],
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
        hidropatia=-3.5, masa=146.15, nutricion="Condicional",
        precursor="Glutamato",
        nota_nutricion="Se forma de Glu + NH3 (glutamina sintetasa); la "
                       "demanda sube mucho en catabolismo (trauma, sepsis).",
        destino="Glucogénico", codones=["CAA", "CAG"],
        movs=["puente_h", "amida_doble", "van_der_waals"],
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
        hidropatia=-3.5, masa=133.10, nutricion="No esencial",
        destino="Glucogénico", codones=["GAU", "GAC"],
        movs=["puente_salino_neg", "unir_calcio", "van_der_waals"],
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
        hidropatia=-3.5, masa=147.13, nutricion="No esencial",
        destino="Glucogénico", codones=["GAA", "GAG"],
        movs=["puente_salino_neg", "unir_calcio", "van_der_waals"],
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
        hidropatia=-3.9, masa=146.19, nutricion="Esencial", req=30,
        destino="Cetogénico", codones=["AAA", "AAG"],
        movs=["puente_salino_pos", "acetilar", "abrazar_adn"],
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
              "ribosomales; se acetila, metila y ubiquitina. Puramente "
              "cetogénica (con Leu).",
    ),
    "R": dict(
        nombre="Arginina", tres="Arg", grupo="basico", tipos=("POS",),
        carga="Positiva (+1)", pk1=2.17, pk2=9.04, pkr=12.48, pi=10.76,
        hidropatia=-4.5, masa=174.20, nutricion="Condicional",
        precursor="Citrulina (ciclo de la urea)",
        nota_nutricion="Se forma en el ciclo de la urea (desde citrulina); "
                       "esencial en neonatos y prematuros.",
        destino="Glucogénico",
        codones=["CGU", "CGC", "CGA", "CGG", "AGA", "AGG"],
        movs=["puente_salino_pos", "guanidinio", "van_der_waals"],
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
        pi=7.59, hidropatia=-3.2, masa=155.16, nutricion="Esencial", req=10,
        destino="Glucogénico", codones=["CAU", "CAC"],
        movs=["puente_salino_pos", "cambio_ph", "van_der_waals"],
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

ORDEN = list("GAVLIMPFYWSTCNQDEKRH")
for _c, _aa in AMINOACIDOS.items():
    _aa["una"] = _c
    _aa.setdefault("req", None)
    _aa.setdefault("precursor", None)


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


# ============================================================ evoluciones
EVOLUCIONES = {
    "Hyp": dict(
        base="P", nombre="Hidroxiprolina", tres="Hyp", tipos=("POL",), quita=["efecto_hidrofobico"], agrega=["puente_h"],
        carga="Neutra", req=dict(nivel=5, objeto="Vitamina C"),
        mov="triple_helice",
        cambio="Gana un OH en el anillo: de No polar a Polar sin carga.",
        bio="La prolil 4-hidroxilasa (en el RE) le pone un OH usando vitamina "
            "C (ascorbato) como cofactor. La Hyp estabiliza la triple hélice "
            "del colágeno; sin vitamina C el colágeno se deshace → escorbuto.",
        pista="Algo que abunda en los cítricos…",
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
        base="K", nombre="Hidroxilisina", tres="Hyl", tipos=("POS",), quita=[],
        carga="Positiva (+1)", req=dict(nivel=5, objeto="Vitamina C"),
        mov="entrecruzar",
        cambio="Conserva la carga + (sigue en el grupo básico) y gana un OH "
               "en el carbono δ.",
        bio="La lisil hidroxilasa (también dependiente de vitamina C) la "
            "forma en el RE. Sus OH reciben azúcares y crean entrecruzamientos "
            "que dan resistencia a las fibras de colágeno.",
        pista="La misma vitamina que necesita la prolina.",
        cadena=[
            "        CH2", "        |", "        CH2", "        |",
            "        CH-OH", "        |", "        CH2", "        |",
            "        NH3+",
        ],
    ),
    "Kac": dict(
        base="K", nombre="Acetil-lisina", tres="Kac", tipos=("POL",), quita=["acetilar", "puente_salino_pos", "abrazar_adn"], agrega=["van_der_waals"],
        carga="Neutra", req=dict(nivel=6, zona="nucleo"),
        mov="abrir_cromatina",
        cambio="Pierde la carga +: el amonio se vuelve una amida neutra. De "
               "Cargado + a Polar sin carga.",
        bio="Las acetiltransferasas de histonas (HAT) le pasan un acetilo del "
            "acetil-CoA. Sin carga +, la histona suelta al ADN (−): la "
            "cromatina se abre y los genes se expresan. Las HDAC lo revierten.",
        pista="Ocurre donde están las histonas.",
        cadena=[
            "        CH2", "        |", "        CH2", "        |",
            "        CH2", "        |", "        CH2", "        |",
            "        NH", "        |", "        C=O", "        |",
            "        CH3",
        ],
    ),
    "Kme3": dict(
        base="K", nombre="Trimetil-lisina", tres="Kme3", tipos=("POS",), quita=["acetilar"],
        carga="Positiva (+1, permanente)", req=dict(nivel=7, zona="nucleo"),
        mov="marca_epigenetica",
        cambio="Sigue siendo + (amonio cuaternario: ya no puede perder la "
               "carga ni acetilarse, porque su N no tiene H).",
        bio="Las metiltransferasas de histonas (HMT) usan SAM, derivada de la "
            "Met. H3K4me3 marca genes activos; H3K9me3 y H3K27me3, genes "
            "silenciados. No cambia la carga, cambia quién se une.",
        pista="Ocurre en el núcleo, pero hace falta más experiencia.",
        cadena=[
            "        CH2", "        |", "        CH2", "        |",
            "        CH2", "        |", "        CH2", "        |",
            "        N+(CH3)3",
        ],
    ),
    "pS": dict(
        base="S", nombre="Fosfoserina", tres="pSer", tipos=("NEG",), quita=["fosforilar", "puente_h"],
        carga="Negativa (≈ −2)", req=dict(nivel=4, objeto="ATP"),
        mov="fosfato",
        cambio="Gana un fosfato: de Polar sin carga a Cargado − (≈ −2).",
        bio="Las Ser/Thr quinasas (PKA, PKC, MAPK…) le transfieren el "
            "fosfato γ del ATP. Es el interruptor más común de la célula; las "
            "fosfatasas lo quitan.",
        pista="La moneda energética que dan en la mitocondria.",
        cadena=["        CH2", "        |", "        O", "        |",
                "        PO3(2-)"],
    ),
    "pT": dict(
        base="T", nombre="Fosfotreonina", tres="pThr", tipos=("NEG",), quita=["fosforilar", "puente_h"],
        carga="Negativa (≈ −2)", req=dict(nivel=4, objeto="ATP"),
        mov="fosfato",
        cambio="Gana un fosfato: de Polar sin carga a Cargado − (≈ −2).",
        bio="Mismas Ser/Thr quinasas que la serina. El motivo pThr-Pro lo "
            "reconoce la isomerasa Pin1 y controla el ciclo celular (CDKs).",
        pista="La moneda energética que dan en la mitocondria.",
        cadena=["        CH-O-PO3(2-)", "        |", "        CH3"],
    ),
    "pY": dict(
        base="Y", nombre="Fosfotirosina", tres="pTyr", tipos=("NEG", "ARO"), quita=["fosforilar", "puente_h"],
        carga="Negativa (≈ −2)", req=dict(nivel=5, objeto="ATP"),
        mov="sh2",
        cambio="El OH del fenol se fosforila: conserva el anillo, pero ahora "
               "tiene carga ≈ −2 (Cargado − / Aromático).",
        bio="Las tirosina quinasas (como el receptor de insulina, un RTK) la "
            "generan. Los dominios SH2 la reconocen con una Arg que forma un "
            "puente salino con el fosfato, y así propagan la señal.",
        pista="La moneda energética que dan en la mitocondria.",
        cadena=["        CH2", "        |"] + BENCENO + [
            "        C", "        |", "        O-PO3(2-)",
        ],
    ),
    "Cis": dict(
        base="C", nombre="Cistina", tres="Cys-Cys", tipos=("NP",), quita=["puente_disulfuro", "tiol"], agrega=["efecto_hidrofobico"],
        carga="Neutra", req=dict(nivel=4, zona="re", otra_cys=True),
        mov="disulfuro_estable",
        cambio="Dos Cys se unen por un enlace S–S covalente y pierden los SH. "
               "Lehninger: los residuos unidos por disulfuro son fuertemente "
               "hidrofóbicos (no polares).",
        bio="En el RE (ambiente oxidante) la PDI, proteína disulfuro "
            "isomerasa, forma y reacomoda puentes S–S. Estabilizan proteínas "
            "que salen de la célula: insulina, anticuerpos, queratina.",
        pista="Necesita una pareja igual y un ambiente oxidante.",
        cadena=[
            "        CH2", "        |", "        S", "        |",
            "        S", "        |", "        CH2", "        |",
            "  -OOC--C--NH3+",
        ],
    ),
    "Gla": dict(
        base="E", nombre="γ-carboxiglutamato", tres="Gla", tipos=("NEG",), quita=[],
        carga="Negativa (≈ −2)", req=dict(nivel=5, objeto="Vitamina K"),
        mov="coagular",
        cambio="Gana un segundo carboxilo en el carbono γ: carga ≈ −2.",
        bio="La γ-glutamil carboxilasa (en el RE) usa vitamina K. Los Gla de "
            "la protrombina y los factores VII, IX y X atrapan Ca²⁺ y anclan "
            "los factores a la membrana: sin vit. K no hay coagulación (la "
            "warfarina bloquea este ciclo).",
        pista="La vitamina de la coagulación.",
        cadena=[
            "        CH2", "        |", "        CH",
            "       /  \\", "   -OOC    COO-",
        ],
    ),
    "Nglc": dict(
        base="N", nombre="Asn N-glicosilada", tres="Asn-Glc", tipos=("POL",), quita=[],
        carga="Neutra", req=dict(nivel=5, zona="re"),
        mov="escudo_glicanos",
        cambio="Se le une un árbol de azúcares al N de la amida: aún más polar.",
        bio="La oligosacariltransferasa (OST) del RE la añade en el secuón "
            "N-X-S/T (X ≠ Pro). Los glicanos ayudan al plegamiento (ciclo "
            "calnexina/calreticulina) y al control de calidad.",
        pista="Ocurre en el retículo, mientras la proteína entra.",
        cadena=[
            "        CH2", "        |", "        C", "       // \\",
            "      O    NH", "             \\", "             GlcNAc-GlcNAc-Man…",
        ],
    ),
    "Cit": dict(
        base="R", nombre="Citrulina", tres="Cit", tipos=("POL",), quita=["puente_salino_pos", "guanidinio"], agrega=["van_der_waals"],
        carga="Neutra", req=dict(nivel=6),
        mov="citrulinar",
        cambio="Pierde la carga +: el guanidinio se vuelve una urea neutra "
               "(de Cargado + a Polar sin carga).",
        bio="Las PAD (peptidil-arginina deiminasas, dependientes de Ca²⁺) la "
            "generan. PAD4 citrulina histonas en las trampas de neutrófilos "
            "(NETs). En la artritis reumatoide aparecen anticuerpos anti-CCP. "
            "La citrulina libre también es parte del ciclo de la urea.",
        pista="Solo necesita experiencia.",
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
# tipo: grupo de Lehninger cuya química usa el movimiento (o NEUTRO si no
#       depende de la cadena lateral).  La animación se elige en combate según
#       la interacción REAL con el tipo del rival.
# efecto: clave que interpreta combate.py.  poder 0 = solo cambia a tu
#       aminoácido (no forma interacción con el rival).
def _m(nombre, tipo, poder, desc, ciencia=None, efecto=None, anim=None):
    return dict(nombre=nombre, tipo=tipo, poder=poder, desc=desc,
                ciencia=ciencia, efecto=efecto, anim=anim)


MOVIMIENTOS = {
    # --- interacciones de cadena lateral
    "efecto_hidrofobico": _m(
        "Efecto hidrofóbico", "NP", 40,
        "Junta su cadena no polar con la del rival y expulsa el agua.",
        "Al juntarse, se libera el agua ordenada que rodeaba a las cadenas no "
        "polares: aumenta la entropía. Es la fuerza principal del plegamiento."),
    "cremallera": _m(
        "Cremallera de leucinas", "NP", 60,
        "Interacción no polar muy fuerte entre hélices.",
        "En los factores bZIP (Fos/Jun) hay una Leu cada 7 residuos: las Leu "
        "de dos hélices encajan como un cierre."),
    "nucleo_hidrofobico": _m(
        "Núcleo hidrofóbico", "NP", 55,
        "Se entierra junto al rival en el interior de la proteína.",
        "Ile, Leu, Val y Phe forman el núcleo de casi todas las proteínas "
        "globulares."),
    "tioeter": _m(
        "Tioéter", "NP", 40,
        "El S de la Met (sin H, no polar) contacta otras cadenas no polares y "
        "anillos aromáticos.",
        "Las interacciones Met–aromático son frecuentes en proteínas; el S "
        "grande y polarizable aporta contactos de van der Waals."),
    "apilamiento_pi": _m(
        "Apilamiento π", "ARO", 40,
        "Su anillo aromático se apila con el del rival o atrae una carga +.",
        "π–π: dos anillos se apilan desplazados. Catión–π: un NH₃⁺ o "
        "guanidinio se coloca sobre la cara del anillo."),
    "puente_h": _m(
        "Puente de hidrógeno", "POL", 40,
        "Un H unido a O o N se comparte con otro O o N del rival.",
        "Cada puente de H vale ~2–5 kcal/mol; en agua compiten con el "
        "solvente, por eso importan más en el interior de la proteína."),
    "amida_doble": _m(
        "Amida doble", "POL", 50,
        "La amida dona (NH₂) y acepta (C=O) puentes de H a la vez.",
        "Asn y Gln forman puentes de H bidentados."),
    "tiol": _m(
        "Tiol", "POL", 35,
        "El SH forma puentes de H débiles.",
        "El S es menos electronegativo que el O: el SH da puentes de H más "
        "débiles que el OH de la Ser."),
    "puente_disulfuro": _m(
        "Puente disulfuro", "POL", 45,
        "Contra otra Cys forma un enlace covalente S–S (afinidad al máximo). "
        "Contra los demás es solo un tiol polar.",
        "2 R–SH → R–S–S–R + 2H⁺ + 2e⁻ (oxidación). Solo ocurre entre dos Cys.",
        efecto="disulfuro"),
    "puente_salino_neg": _m(
        "Puente salino", "NEG", 40,
        "Tu carboxilato (−) atrae a una carga +.",
        "Atracción electrostática COO⁻···⁺H₃N (como Asp–Lys)."),
    "puente_salino_pos": _m(
        "Puente salino", "POS", 40,
        "Tu grupo + atrae a un carboxilato (−).",
        "Atracción electrostática ⁺H₃N···⁻OOC (como Lys–Asp). Necesita "
        "tener la carga +: si se acetila o se desprotona, no funciona."),
    "abrazar_adn": _m(
        "Abrazar ADN", "POS", 55,
        "Varias cargas + juntas forman puentes salinos múltiples.",
        "Así las histonas (ricas en Lys y Arg) enrollan 147 pb de ADN, cuyos "
        "fosfatos son (−)."),
    "guanidinio": _m(
        "Guanidinio", "POS", 60,
        "Puente salino doble y muy estable.",
        "El guanidinio (pKR 12.5) nunca pierde su carga y forma dos puentes "
        "de H en paralelo con un carboxilato. También es el mejor socio "
        "catión–π."),
    # --- interacciones del esqueleto (iguales para los 20)
    "van_der_waals": _m(
        "Van der Waals", NEUTRO, 25,
        "Fuerzas de London: débiles, pero existen entre cualquier par de "
        "átomos (×1 con todos).",
        "Dipolos instantáneos inducen dipolos en los átomos vecinos."),
    "puente_h_esqueleto": _m(
        "Puente de H del esqueleto", NEUTRO, 35,
        "El N–H de su esqueleto se une al C=O del esqueleto del rival.",
        "Todos los aminoácidos tienen N–H y C=O en el enlace peptídico (salvo "
        "Pro, que no tiene H en el N). Sin cadena lateral, Gly se acerca más."),
    "lamina_beta": _m(
        "Lámina β", NEUTRO, 35,
        "Forma una lámina con el rival: puentes de H entre esqueletos. Además "
        "recibe la mitad de agitación 2 turnos.",
        "Los ramificados en β (Val, Ile, Thr) prefieren las láminas β.",
        efecto="escudo2"),
    # --- cambios sobre tu propio aminoácido (poder 0)
    "flexibilidad": _m(
        "Flexibilidad", NEUTRO, 0,
        "Esquiva la siguiente agitación del rival.",
        "Sin cadena lateral, Gly adopta ángulos φ/ψ prohibidos para los demás.",
        efecto="esquiva", anim="flexible"),
    "anillo_rigido": _m(
        "Anillo rígido", NEUTRO, 0,
        "Recibe la mitad de agitación 3 turnos.",
        "El anillo de la Pro fija el ángulo φ (≈ −65°): su esqueleto casi no "
        "se deforma.",
        efecto="escudo3", anim="rigido"),
    "helice_alfa": _m(
        "Hélice α", NEUTRO, 0,
        "Se enrolla: tu siguiente movimiento vale ×1.5.",
        "Ala es el residuo con mayor tendencia a formar hélice α (puentes de H "
        "del C=O del residuo i al N–H del i+4).",
        efecto="potenciar", anim="helice"),
    "codon_inicio": _m(
        "Codón de inicio", NEUTRO, 0,
        "Toma la iniciativa: tu siguiente movimiento vale ×1.5.",
        "AUG inicia la traducción: la Met siempre va primero.",
        efecto="potenciar", anim="codon"),
    "antioxidante": _m(
        "Antioxidante", NEUTRO, 0,
        "Atrapa especies reactivas de oxígeno: recibe la mitad de agitación "
        "3 turnos.",
        "Las Met expuestas se oxidan a Met-sulfóxido y protegen a otros "
        "residuos; la enzima MsrA las regenera.",
        efecto="escudo3", anim="antioxidante"),
    "fosforilar": _m(
        "Fosforilación", NEUTRO, 0,
        "Gasta 1 ATP: se vuelve Cargado − por 3 turnos.",
        "Una quinasa pasa el fosforilo γ del ATP al OH: carga ≈ −2.",
        efecto="fosforilar", anim="fosforilar"),
    "acetilar": _m(
        "Acetilación", NEUTRO, 0,
        "Pierde la carga +: se vuelve Polar sin carga por 3 turnos.",
        "Una acetiltransferasa (HAT) pasa el acetilo del acetil-CoA al NH₃⁺, "
        "que queda como amida neutra.",
        efecto="acetilar", anim="acetilar"),
    "cambio_ph": _m(
        "Cambio de pH", NEUTRO, 0,
        "Alterna entre protonada (Cargado +) y neutra (Polar sin carga).",
        "Con pKR ≈ 6, la His se protona con solo bajar un poco el pH "
        "(endosomas, lisosomas).",
        efecto="ph", anim="ph"),
    "unir_calcio": _m(
        "Unir Ca²⁺", NEUTRO, 0,
        "Dos carboxilatos de tu proteína atrapan un Ca²⁺: se estabiliza y "
        "recibe la mitad de agitación 3 turnos.",
        "Así funcionan las manos EF de la calmodulina. El Ca²⁺ se une a TUS "
        "carboxilatos; no cambia la repulsión con un rival ácido.",
        efecto="escudo3", anim="calcio"),
    "fluorescencia": _m(
        "Fluorescencia", NEUTRO, 0,
        "Revela el nombre y el grupo del rival.",
        "El Trp se excita a 295 nm y emite a ~330 nm en un entorno no polar "
        "o a ~350 nm en uno polar: su color delata a su vecino.",
        efecto="revelar", anim="fluorescencia"),
    # --- de evoluciones
    "triple_helice": _m(
        "Triple hélice", NEUTRO, 60,
        "Empaqueta tres cadenas como el colágeno (puentes de H del esqueleto).",
        "El N–H de la Gly de una cadena se une al C=O de otra; el OH de la "
        "Hyp estabiliza la hélice a través del agua."),
    "entrecruzar": _m(
        "Entrecruzamiento", "POS", 55,
        "Su amonio forma puentes salinos y, en el colágeno, enlaces covalentes "
        "entre fibras.",
        "La lisil oxidasa convierte Lys/Hyl en aldehídos que se unen a otras "
        "fibras."),
    "abrir_cromatina": _m(
        "Unirse a bromodominio", "POL", 50,
        "La amida del acetilo forma un puente de H.",
        "Los bromodominios reconocen la acetil-lisina con un puente de H a "
        "una Asn conservada."),
    "marca_epigenetica": _m(
        "Jaula aromática", "POS", 50,
        "Su carga + permanente se mete en una jaula de anillos aromáticos.",
        "Los cromodominios (HP1 con H3K9me3) reconocen la metil-lisina con "
        "2–4 anillos aromáticos: interacción catión–π."),
    "fosfato": _m(
        "Fosfato (−2)", "NEG", 55,
        "Su fosfato forma puentes salinos con Arg y Lys.",
        "Dominios como 14-3-3 y FHA reconocen pSer/pThr con Arg y Lys."),
    "sh2": _m(
        "Unión a SH2", "NEG", 60,
        "Su fosfato atrapa la Arg del dominio SH2.",
        "Los dominios SH2 reconocen pTyr con una Arg conservada (vía del "
        "receptor de insulina, Grb2…)."),
    "disulfuro_estable": _m(
        "Disulfuro estable", "NP", 45,
        "Contacto no polar; además recibe la mitad de agitación 3 turnos.",
        "Los puentes S–S resisten la desnaturalización.",
        efecto="escudo3"),
    "coagular": _m(
        "Gla (carga −2)", "NEG", 55,
        "Sus dos carboxilatos forman puentes salinos fuertes.",
        "En la sangre, los Gla atrapan Ca²⁺ y con él anclan los factores de "
        "coagulación a la membrana."),
    "escudo_glicanos": _m(
        "Escudo de glicanos", NEUTRO, 0,
        "Recibe la mitad de agitación 3 turnos.",
        "Los glicanos protegen de proteasas y ayudan al plegamiento.",
        efecto="escudo3", anim="glicanos"),
    "imidazol_h": _m(
        "Puente de H del imidazol", "POL", 40,
        "Solo si la His está neutra: su imidazol dona y acepta puentes de H.",
        "Neutro, el imidazol tiene un N–H (donador) y un N: (aceptor)."),
    "citrulinar": _m(
        "Urea de la citrulina", "POL", 50,
        "La urea neutra forma puentes de H.",
        "La PAD convierte Arg (+) en citrulina (neutra)."),
}


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
        nombre="Polirribosomas", aminos=list("KR"), niveles=(3, 5),
        glifo="∴", color="POS",
        por_que="Las proteínas ribosomales son ricísimas en Lys y Arg: sus "
                "cargas + neutralizan los fosfatos (−) del ARN ribosomal. "
                "Aquí puedes conseguir K y R antes de entrar al núcleo.",
    ),
    "nucleo": dict(
        nombre="Núcleo (cromatina)", aminos=list("KR"), niveles=(5, 8),
        glifo="§", color="POS",
        por_que="Las histonas son ricas en Lys y Arg y abrazan al ADN, "
                "cargado (−) por sus fosfatos. Para entrar, tu proteína "
                "necesita una señal de localización nuclear (NLS).",
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
        por_que="Centro de recuperación: la fosforilación oxidativa produce "
                "ATP. Tu equipo recupera energía y recibes ATP. Aquí también "
                "se degradan los ramificados (Val, Leu, Ile).",
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
    ("Glucogénico", "Su esqueleto de carbono puede convertirse en glucosa "
                    "(da piruvato o intermediarios del ciclo de Krebs)."),
    ("Cetogénico", "Da acetil-CoA o acetoacetato: puede formar cuerpos "
                   "cetónicos, no glucosa. Solo Leu y Lys son puramente "
                   "cetogénicos."),
    ("Código de 1 letra", "Los difíciles: F=Phe, Y=Tyr, W=Trp, N=Asn, Q=Gln, "
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
    """Datos de un aminoácido base o de una evolución con interfaz común."""
    if fid in AMINOACIDOS:
        aa = AMINOACIDOS[fid]
        return dict(
            id=fid, base=fid, nombre=aa["nombre"], tres=aa["tres"],
            tipos=tuple(aa["tipos"]), carga=aa["carga"], masa=aa["masa"],
            movs=list(aa["movs"]), arte=arte(aa), evo=False,
        )
    ev = EVOLUCIONES[fid]
    base = AMINOACIDOS[ev["base"]]
    return dict(
        id=fid, base=ev["base"], nombre=ev["nombre"], tres=ev["tres"],
        tipos=tuple(ev["tipos"]), carga=ev["carga"], masa=base["masa"] + 40,
        movs=[m for m in base["movs"] if m not in ev["quita"]] + ev.get("agrega", []) + [ev["mov"]],
        arte=arte(ev), evo=True,
    )


def arte(d):
    if d.get("completa"):
        return list(d["completa"])
    return ESQUELETO + d["cadena"]


def evoluciones_de(base):
    return [k for k, v in EVOLUCIONES.items() if v["base"] == base]


def nombre_tipos(tipos, corto=False):
    clave = "corto" if corto else "nombre"
    return " / ".join(TIPOS[t][clave] for t in tipos)


def zonas_de(aa):
    return [z for z, info in ZONAS.items() if aa in info["aminos"]]
