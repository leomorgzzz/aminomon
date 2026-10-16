"""Traducción al inglés de posgame.py y del menú del René-virus."""

EN = {
    '1) Cisteína (Cys, C)   2) Selenocisteína (Sec, U)   Esc salir':
        '1) Cysteine (Cys, C)   2) Selenocysteine (Sec, U)   Esc quit',
    '21 · Selenocisteína':
        '21 · Selenocysteine',
    '21 · SELENOCISTEÍNA · Sec · U':
        '21 · SELENOCYSTEINE · Sec · U',
    'A pH {ph} su carga neta es {q:+.1f}: por debajo del pI es +, por encima es −.':
        'At pH {ph} its net charge is {q:+.1f}: below the pI it is +, above it is −.',
    'Al ánodo (+): tiene carga −':
        'To the anode (+): it has a − charge',
    'Al cátodo (−): tiene carga +':
        'To the cathode (−): it has a + charge',
    'Bienvenida a mi laboratorio de proteómica. Aquí la química de cada aminoácido se mide: titulación, electroforesis e intercambio iónico. Son 6 problemas.':
        'Welcome to my proteomics lab. Here the chemistry of each amino acid gets measured: titration, electrophoresis and ion exchange. There are 6 problems.',
    'Casi no se mueve: carga neta ≈ 0':
        'It barely moves: net charge ≈ 0',
    'Columna de intercambio CATIÓNICO (resina −) a pH 6 con {a}, {b} y {c}: ¿cuál sale primero?':
        'CATION exchange column (− resin) at pH 6 with {a}, {b} and {c}: which comes out first?',
    'Como la Cys, pero con selenio en lugar de azufre: –SeH en vez de –SH. El selenol (pKa ≈ 5.2) está desprotonado a pH 7 y es mucho más reactivo que el tiol de la Cys (pKa 8.2): por eso está en el sitio activo de enzimas redox. Se codifica con UGA + SECIS.':
        "Like Cys, but with selenium instead of sulfur: –SeH instead of –SH. The selenol (pKa ≈ 5.2) is deprotonated at pH 7 and much more reactive than the Cys thiol (pKa 8.2): that's why it sits in the active site of redox enzymes. It is encoded by UGA + SECIS.",
    '¿Cuál?':
        'Which one?',
    '¿Cys o Sec?':
        'Cys or Sec?',
    '¿Cys o Sec? · {i}/8 · aciertos {n}':
        'Cys or Sec? · {i}/8 · correct {n}',
    '¿Cys o Sec? (el aminoácido 21)':
        'Cys or Sec? (amino acid 21)',
    'El aminoácido 21':
        'Amino acid 21',
    'El aminoácido 21 (evento)':
        'Amino acid 21 (event)',
    'El ARNt-Sec se carga primero con otro aminoácido y luego se convierte. ¿Con cuál?':
        'tRNA-Sec is first charged with another amino acid and then converted. Which one?',
    'el pI (carga neta 0)':
        'the pI (net charge 0)',
    'el pK1 (α-COOH)':
        'pK1 (α-COOH)',
    'el pK2 (α-NH3+)':
        'pK2 (α-NH3+)',
    'el pKR (cadena lateral)':
        'pKR (side chain)',
    'Electroforesis':
        'Electrophoresis',
    'Electroforesis a pH {ph}: ¿hacia dónde migra {nombre} (pI {pi})?':
        'Electrophoresis at pH {ph}: where does {nombre} (pI {pi}) migrate?',
    'En el ARNm de una selenoproteína, ¿qué codón lee la Sec?':
        'In a selenoprotein mRNA, which codon reads Sec?',
    'Ese codón normalmente es de paro. ¿Qué lleva el ARNm para que se lea como Sec?':
        "That codon is normally a stop. What does the mRNA carry so it's read as Sec?",
    'Fíjate en el último átomo: S en la Cys, Se en la Sec.':
        'Look at the last atom: S in Cys, Se in Sec.',
    'Hay un aminoácido que no está en los 20: la selenocisteína (Sec, U). Unas 25 proteínas humanas la usan, como la glutatión peroxidasa y las desyodasas tiroideas.':
        'There is an amino acid outside the 20: selenocysteine (Sec, U). About 25 human proteins use it, such as glutathione peroxidase and the thyroid deiodinases.',
    'La resina negativa retiene lo positivo; lo más negativo pasa de largo. Cargas a pH 6: {d}.':
        'The negative resin holds what is positive; the most negative passes straight through. Charges at pH 6: {d}.',
    'Laboratorio del René-virus':
        'René-virus lab',
    'Laboratorio del René-virus (titulación, electroforesis…)':
        'René-virus lab (titration, electrophoresis…)',
    'Las mesetas son los pK (ahí el grupo amortigua); el pI queda entre los dos pK que rodean la forma neutra.':
        'The plateaus are the pKs (where the group buffers); the pI lies between the two pKs around the neutral form.',
    'No.':
        'No.',
    'No: era la {l}.':
        'No: it was {l}.',
    'No. Era: {r}. Vuelve a intentarlo cuando quieras.':
        'No. It was: {r}. Try again whenever you want.',
    'No: sale primero {n}.':
        'No: {n} comes out first.',
    'No tiene codón propio. Para meterla, la célula reinterpreta un codón y usa un ARNt especial. Contesta bien y tu Ser se convertirá en Sec.':
        'It has no codon of its own. To insert it, the cell reinterprets a codon and uses a special tRNA. Answer correctly and your Ser will become Sec.',
    'Para el aminoácido 21 necesitas una Ser en tu equipo: la Sec se arma sobre una Ser.':
        'For amino acid 21 you need a Ser in your team: Sec is built on a Ser.',
    'pH (vertical) contra equivalentes de OH− agregados (horizontal)':
        'pH (vertical) against equivalents of OH− added (horizontal)',
    '¿Qué letra marca {que}?':
        'Which letter marks {que}?',
    'selenometilo (–CH2–SeH)':
        'selenomethyl (–CH2–SeH)',
    'Titulación':
        'Titration',
    'TITULACIÓN · {nombre}':
        'TITRATION · {nombre}',
    '¡Tu Ser se cargó en el ARNt-Sec y, con selenofosfato, se convirtió en selenocisteína! Ya está en tu Aminodex como el 21, fuera del 20/20.':
        "Your Ser was loaded onto tRNA-Sec and, with selenophosphate, became selenocysteine! It's now in your Aminodex as number 21, outside the 20/20.",
    'Un elemento SECIS (una horquilla en el ARNm)':
        'A SECIS element (a hairpin in the mRNA)',
    'Un intrón sin cortar':
        'An unspliced intron',
    'Un segundo AUG antes del codón':
        'A second AUG before the codon',
    'Una cola de poli(A) más larga':
        'A longer poly(A) tail',
    '¿Ver el evento del aminoácido 21?':
        'See the amino acid 21 event?',
    '{n}/6 problemas resueltos.':
        '{n}/6 problems solved.',
    '{n}/8 correctas.':
        '{n}/8 correct.',
    'Intercambio iónico':
        'Ion exchange',
    'Incorrecto.':
        'Wrong.',
}
