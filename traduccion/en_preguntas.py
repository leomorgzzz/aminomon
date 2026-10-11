"""Traducción al inglés de los textos de preguntas.py."""

EN = {
    'No tiene grupos que se ionicen a pH 7.':
        'It has no groups that ionize at pH 7.',
    'Su imidazol tiene pKR ≈ 6: a pH 7 solo ~10% está protonado.':
        'Its imidazole has pKR ≈ 6: at pH 7 only ~10% is protonated.',
    'Su pKR ({pkr}) es mayor que 7: a pH 7 conserva el H+ y queda neutra.':
        'Its pKR ({pkr}) is above 7: at pH 7 it keeps its H+ and stays neutral.',
    'Hidrofóbico (KD > 0)':
        'Hydrophobic (KD > 0)',
    'Hidrofílico (KD < 0)':
        'Hydrophilic (KD < 0)',
    'ácido':
        'acidic',
    'Incorrecto. Era: {respuesta}. ':
        'Wrong. It was: {respuesta}. ',
    '¿Qué aminoácido es este? Fíjate en su cadena lateral.':
        'Which amino acid is this? Look at its side chain.',
    'Es {nombre} ({tres}, {una}). {pista}':
        "It's {nombre} ({tres}, {una}). {pista}",
    'Escribe el código de 3 letras de {nombre}:':
        'Type the 3-letter code of {nombre}:',
    'Escribe el código de 1 letra de {nombre} ({tres}):':
        'Type the 1-letter code of {nombre} ({tres}):',
    '¿Carga de la cadena lateral de {nombre} a pH 7?':
        'Charge of the side chain of {nombre} at pH 7?',
    '¿A qué grupo (Lehninger) pertenece {nombre}?':
        'Which (Lehninger) group does {nombre} belong to?',
    'En humanos, {nombre} es…':
        'In humans, {nombre} is…',
    'Esenciales (9): His Ile Leu Lys Met Phe Thr Trp Val. Condicionales (6): Arg Cys Gln Gly Pro Tyr. No esenciales (5): Ala Asp Asn Glu Ser.':
        'Essential (9): His Ile Leu Lys Met Phe Thr Trp Val. Conditional (6): Arg Cys Gln Gly Pro Tyr. Nonessential (5): Ala Asp Asn Glu Ser.',
    '¿Cuál de estos codones codifica {nombre}?':
        'Which of these codons encodes {nombre}?',
    'Según Kyte-Doolittle, {nombre} es…':
        'According to Kyte-Doolittle, {nombre} is…',
    '¿pKR (cadena lateral) de {nombre}?':
        'pKR (side chain) of {nombre}?',
    '¿Punto isoeléctrico (pI) de {nombre}?':
        'Isoelectric point (pI) of {nombre}?',
    'pI = ({p1:.2f} + {p2:.2f}) / 2 = {pi:.2f}. Extremos: Asp 2.77 (el más ácido) y Arg 10.76 (el más básico).':
        'pI = ({p1:.2f} + {p2:.2f}) / 2 = {pi:.2f}. Extremes: Asp 2.77 (the most acidic) and Arg 10.76 (the most basic).',
    'básico':
        'basic',
    'con cadena ionizable':
        'with an ionizable side chain',
    '{nombre}: pK1 {pk1:.2f}, pK2 {pk2:.2f}, pKR {pkr:.2f}. Calcula su pI:':
        '{nombre}: pK1 {pk1:.2f}, pK2 {pk2:.2f}, pKR {pkr:.2f}. Calculate its pI:',
    'Se promedian los dos pKa que rodean la forma neutra. Para este aminoácido {tipo}: ({p1:.2f} + {p2:.2f}) / 2 = {pi:.2f}.':
        'Average the two pKa values on either side of the neutral form. For this amino acid {tipo}: ({p1:.2f} + {p2:.2f}) / 2 = {pi:.2f}.',
    'Su carboxilo (pKR ~4) ya perdió el H+ a pH 7.':
        'Its carboxyl (pKR ~4) has already lost its H+ at pH 7.',
    'Su grupo básico conserva el H+ a pH 7.':
        'Its basic group keeps its H+ at pH 7.',
    'KD de {tres} = {kd:+.1f}. ':
        'KD of {tres} = {kd:+.1f}. ',
    'Coincide con la inicial.':
        'It matches the initial.',
    "F de 'Fenilalanina'.":
        "F sounds like the start of 'Fenylalanine'.",
    "Y de 'tYrosina'.":
        "Y from 'tYrosine'.",
    'W: el triptófano tiene un anillo doble (double ring → W).':
        'W: tryptophan has a double ring (double ring → W).',
    "N de 'asparagiNe'.":
        "N from 'asparagiNe'.",
    "Q de 'Q-tamina' (Glutamina).":
        "Q from 'Q-tamine' (Glutamine).",
    "D de 'asparDate' (Asp, el más pequeño de los ácidos).":
        "D from 'asparDic' (Asp, the smaller of the acidic ones).",
    "E de 'glutEmate'.":
        "E from 'glutEmic' (E comes right after D).",
    'K: la letra antes de L (lisina).':
        'K: the letter before L (lysine).',
    "R de 'aRginina'.":
        "R from 'aRginine'.",
    "I de 'Isoleucina'; la L se la quedó Leu.":
        "I from 'Isoleucine'; Leu already had L.",
    "T de 'Treonina'; la S es de Ser.":
        "T from 'Threonine'; S belongs to Ser.",
    "Gln (Q) y Asn (N) son las amidas: Gln tiene un CH2 más, igual que Glu frente a Asp. N de asparagiNe; Q de 'Q-tamina'.":
        "Gln (Q) and Asn (N) are the amides: Gln has one more CH2, just like Glu versus Asp. N from asparagiNe; Q from 'Q-tamine'.",
    'Glu (E) y Asp (D) son los ácidos: Glu tiene un CH2 más. Asp es el corto y va primero, como la D antes de la E.':
        'Glu (E) and Asp (D) are the acids: Glu has one more CH2. Asp is the short one and comes first, like D before E.',
    'Ile y Leu tienen la misma fórmula: Ile se ramifica en el carbono β (pegado al Cα) y Leu en el γ, un carbono más lejos.':
        'Ile and Leu share the same formula: Ile branches at the β carbon (next to Cα) and Leu at the γ carbon, one carbon further.',
    'Ser (S) termina en CH2-OH; Thr (T) tiene además un metilo en el carbono β: CH(OH)-CH3.':
        'Ser (S) ends in CH2-OH; Thr (T) also has a methyl on the β carbon: CH(OH)-CH3.',
    'Trp = W: anillo doble (double ring). La T ya era de Thr y la P de Pro.':
        'Trp = W: double ring. T was already Thr and P was Pro.',
    'Lys = K: la letra antes de L, porque la L ya era de Leu.':
        'Lys = K: the letter before L, because L was already Leu.',
    '¿Cuál es el código de 3 letras de este aminoácido?':
        'What is the 3-letter code of this amino acid?',
    '¿Cuál es el código de 1 letra de este aminoácido?':
        'What is the 1-letter code of this amino acid?',
    'Captura primero a alguno de estos: Gln, Asn, Glu, Asp, Ile, Leu, Ser, Thr, Trp o Lys.':
        'First catch one of these: Gln, Asn, Glu, Asp, Ile, Leu, Ser, Thr, Trp or Lys.',
    'Práctica de pares':
        'Pair practice',
    'PRÁCTICA DE PARES · {i}/{total} · aciertos {n}':
        'PAIR PRACTICE · {i}/{total} · correct {n}',
    '{n}/{total} correctas. Los que fallaste saldrán más seguido, en la práctica y en el campo.':
        '{n}/{total} correct. The ones you missed will show up more often, in practice and in the field.',
}
