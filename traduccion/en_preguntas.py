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
    '{nombre}: pK1 {pk1:.2f}, pK2 {pk2:.2f}, pKR {pkr:.2f}. ¿Su punto isoeléctrico (pI)?':
        '{nombre}: pK1 {pk1:.2f}, pK2 {pk2:.2f}, pKR {pkr:.2f}. Its isoelectric point (pI)?',
    '{nombre}: pK1 {pk1:.2f}, pK2 {pk2:.2f}. ¿Su punto isoeléctrico (pI)?':
        '{nombre}: pK1 {pk1:.2f}, pK2 {pk2:.2f}. Its isoelectric point (pI)?',
    'pKR (Lehninger, 25 °C): Asp 3.65, Glu 4.25, His 6.00, Cys 8.18, Tyr 10.07, Lys 10.53, Arg 12.48.':
        'pKR (Lehninger, 25 °C): Asp 3.65, Glu 4.25, His 6.00, Cys 8.18, Tyr 10.07, Lys 10.53, Arg 12.48.',
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
    'Práctica de reconocimiento':
        'Recognition practice',
    'PRÁCTICA DE RECONOCIMIENTO · {i}/{total} · aciertos {n} · dominados {dom}/20':
        'RECOGNITION PRACTICE · {i}/{total} · correct {n} · mastered {dom}/20',
    '{n}/{total} correctas. Los que fallaste saldrán más seguido, en la práctica y en el campo.':
        '{n}/{total} correct. The ones you missed will show up more often, in practice and in the field.',
    'Captura primero algún aminoácido.':
        'Catch an amino acid first.',
    ' · Esc salir':
        ' · Esc exit',
    'Ahora salen justo esos, con su pareja en las opciones.':
        'Now exactly those come up, with their look-alike among the options.',
    'Contrarreloj':
        'Time trial',
    'Contrarreloj: 60 s, cuantas puedas (récord {r})':
        'Time trial: 60 s, as many as you can (record {r})',
    'Correcto: es la {n}).':
        "Correct: it's number {n}).",
    '¿Cuál es {nombre}? Pulsa 1-4 · Esc salir':
        'Which one is {nombre}? Press 1-4 · Esc quit',
    'Cuando era {era}, contestaste {dijo}: {n} {veces}':
        'When it was {era}, you answered {dijo}: {n} {veces}',
    'Elige la estructura':
        'Pick the structure',
    'ELIGE LA ESTRUCTURA · {i}/{total} · aciertos {n}':
        'PICK THE STRUCTURE · {i}/{total} · correct {n}',
    'Estructura → nombre y códigos ({n} preguntas)':
        'Structure → name and codes ({n} questions)',
    'Incorrecto: elegiste {otro}. {nombre} era la {n}).':
        'Wrong: you picked {otro}. {nombre} was number {n}).',
    '{n} aciertos y {f} fallos en {s} s.':
        '{n} right and {f} wrong in {s} s.',
    'Necesitas al menos 4 aminoácidos capturados para este modo.':
        'You need at least 4 caught amino acids for this mode.',
    'Nombre → elige su estructura entre 4':
        'Name → pick its structure out of 4',
    '{n}/{total} correctas.':
        '{n}/{total} correct.',
    'Solo la cadena lateral → nombre':
        'Side chain only → name',
    'Todavía no has confundido ningún aminoácido. Cuando falles uno, aquí verás con cuál lo confundiste para practicar justo eso.':
        "You haven't mixed up any amino acid yet. When you miss one, you'll see here which one you took it for, so you can practice exactly that.",
    'Tus confusiones':
        'Your mix-ups',
    'Tus confusiones ({n})':
        'Your mix-ups ({n})',
    '(Cα)':
        '(Cα)',
    'vez':
        'time',
    'veces':
        'times',
    '√ {nombre}':
        '√ {nombre}',
    '× era {nombre}, no {otro}':
        '× it was {nombre}, not {otro}',
    '¡Nuevo récord!':
        'New record!',
    'Récord: {r}.':
        'Record: {r}.',
    'CONTRARRELOJ · {s} s · aciertos {n} · fallos {f}':
        'TIME TRIAL · {s} s · right {n} · wrong {f}',
    'Pulsa el número · Esc salir':
        'Press the number · Esc quit',
    '(se ve solo la cadena lateral; el esqueleto es igual en todos)':
        '(only the side chain is shown; the backbone is the same in all)',
    'Volver':
        'Back',
    'Captura primero algún aminoácido con un grupo al final de la cadena (Ser, Cys, Lys, Asp…).':
        'First catch an amino acid with a group at the end of its chain (Ser, Cys, Lys, Asp…).',
    'Completa la cadena lateral':
        'Complete the side chain',
    'COMPLETA LA CADENA LATERAL · {i}/{total} · aciertos {n}':
        'COMPLETE THE SIDE CHAIN · {i}/{total} · correct {n}',
    'Correcto.':
        'Correct.',
    '¿Cuál es diferente?':
        'Which one is different?',
    '¿CUÁL ES DIFERENTE? · {i}/{total} · aciertos {n}':
        'WHICH ONE IS DIFFERENT? · {i}/{total} · correct {n}',
    '¿Cuál es diferente? (4 estructuras, una no es del grupo)':
        "Which one is different? (4 structures, one isn't in the group)",
    'Hoy no te toca repasar ninguno. Los que aciertas vuelven en 1, 3, 7 y 14 días; los que fallas, al día siguiente.':
        'Nothing to review today. The ones you get right come back after 1, 3, 7 and 14 days; the ones you miss, the next day.',
    'Incorrecto. Era: {g}.':
        'Wrong. It was: {g}.',
    'Incorrecto: era la {n}).':
        'Wrong: it was number {n}).',
    'Nombre → completa la cadena lateral':
        'Name → complete the side chain',
    '{nombre}: grupo R {r}.':
        '{nombre}: R group {r}.',
    '{nombres}: {grupo}. {intruso}: {otro}.':
        '{nombres}: {grupo}. {intruso}: {otro}.',
    '¿Qué grupo falta en {nombre}?':
        'Which group is missing in {nombre}?',
    'Repaso de hoy':
        "Today's review",
    'Repaso de hoy: {n} por repasar':
        "Today's review: {n} to review",
    'Tres son del mismo grupo y una no. ¿Cuál? Pulsa 1-4 · Esc salir':
        "Three are in the same group and one isn't. Which? Press 1-4 · Esc quit",
    '–H (nada más)':
        '–H (nothing else)',
    '–CH3':
        '–CH3',
    '–OH':
        '–OH',
    '–SH':
        '–SH',
    '–OH (fenol)':
        '–OH (phenol)',
    '–S–CH3 (tioéter)':
        '–S–CH3 (thioether)',
    '–CONH2 (amida)':
        '–CONH2 (amide)',
    '–COO− (carboxilato)':
        '–COO− (carboxylate)',
    '–NH3+ (amino)':
        '–NH3+ (amino)',
    'fenilo (anillo)':
        'phenyl (ring)',
    'indol (doble anillo)':
        'indole (double ring)',
}
