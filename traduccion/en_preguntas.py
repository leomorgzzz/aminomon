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
    'Modificaciones: ¿qué cambio es? ({n} descubiertas)':
        'Modifications: which change is it? ({n} discovered)',
    'Todavía no descubres ninguna modificación: se consiguen subiendo de nivel a tu equipo en la zona correcta (Equipo → V).':
        "You haven't discovered any modification yet: you get them by leveling up your team in the right area (Team → V).",
    '¿De qué aminoácido viene este residuo modificado?':
        'Which amino acid does this modified residue come from?',
    'MODIFICACIONES · {i}/{total} · aciertos {n}':
        'MODIFICATIONS · {i}/{total} · correct {n}',
    '{nombre} ({tres}), de {base}: {cambio}':
        '{nombre} ({tres}), from {base}: {cambio}',
    'Pregunta · contesta aquí':
        'Question · answer here',
    '► Pulsa el número de tu respuesta':
        '► Press the number of your answer',
    '¿Cys o Sec? (selenocisteína)':
        'Cys or Sec? (selenocysteine)',
    '¿Qué modificación covalente es esta?':
        'Which covalent modification is this?',
    '¿Por qué la falta de vitamina C debilita el colágeno?':
        'Why does a lack of vitamin C weaken collagen?',
    'Sin ella no se forma la Hyp y la triple hélice pierde estabilidad':
        'Without it no Hyp forms and the triple helix loses stability',
    'La vitamina C es uno de los aminoácidos del colágeno':
        "Vitamin C is one of collagen's amino acids",
    'Sin ella el ribosoma no puede leer los codones de la Pro':
        "Without it the ribosome can't read Pro codons",
    'La vitamina C forma los puentes disulfuro entre las fibras':
        'Vitamin C forms the disulfide bridges between fibers',
    '¿Para qué sirve el OH nuevo de la hidroxilisina en el colágeno?':
        "What is hydroxylysine's new OH for in collagen?",
    'Recibe azúcares y forma entrecruzamientos':
        'It receives sugars and forms cross-links',
    'Le quita la carga + a la Lys para que se pliegue':
        'It removes the Lys + charge so it can fold',
    'Le da un segundo carboxilo que atrapa Ca²+ entre las fibras':
        'It gives it a second carboxyl that traps Ca²+ between fibers',
    'Vuelve aromática a la Lys para que se apile con la Pro':
        'It makes Lys aromatic so it stacks with Pro',
    '¿Por qué acetilar las Lys de una histona abre la cromatina?':
        "Why does acetylating a histone's Lys open chromatin?",
    'La Lys pierde su + y se une menos al ADN (−)':
        'Lys loses its + and binds DNA (−) less',
    'El acetilo le da a la Lys una carga − que repele al ADN':
        'The acetyl gives Lys a − charge that repels DNA',
    'El acetilo corta los enlaces fosfodiéster del ADN':
        "The acetyl cuts DNA's phosphodiester bonds",
    'La Lys se vuelve aromática y se apila con las bases':
        'Lys becomes aromatic and stacks with the bases',
    '¿Por qué la trimetil-lisina ya no se puede acetilar?':
        "Why can't trimethyl-lysine be acetylated anymore?",
    'Su N tiene 4 enlaces y ningún par libre: ya no es nucleófilo':
        "Its N has 4 bonds and no lone pair: it's no longer a nucleophile",
    'Al metilarse perdió su carga + y ya no atrae al acetilo':
        'Methylation removed its + charge, so it no longer attracts the acetyl',
    'Los tres metilos la vuelven un ácido con carga −':
        'The three methyls turn it into an acid with a − charge',
    'La SAM se queda unida y tapa a la Lys para siempre':
        'SAM stays bound and blocks the Lys forever',
    '¿Por qué Ser, Thr y Tyr son las que más se fosforilan?':
        'Why are Ser, Thr and Tyr the ones phosphorylated most?',
    'Su OH ataca al fosfato del ATP: queda un fosfoéster estable que una fosfatasa quita':
        "Their OH attacks ATP's phosphate: a stable phosphoester is left that a phosphatase removes",
    'Son las únicas que ya tienen carga − a pH 7':
        "They're the only ones already charged − at pH 7",
    'Son las más hidrofóbicas, y el fosfato las vuelve solubles':
        "They're the most hydrophobic, and the phosphate makes them soluble",
    'Tienen un azufre que se une directo al fósforo':
        'They have a sulfur that binds the phosphorus directly',
    '¿Qué le pasa a un residuo al fosforilarse a pH 7?':
        "What happens to a residue when it's phosphorylated at pH 7?",
    'Pasa de neutro a ≈ −2 y cambia con qué se une':
        'It goes from neutral to ≈ −2 and changes what it binds',
    'Gana una carga + y se une al ADN':
        'It gains a + charge and binds DNA',
    'Se vuelve no polar y entra a la membrana':
        'It becomes nonpolar and enters the membrane',
    'Pierde su cadena lateral y se vuelve Gly':
        'It loses its side chain and becomes Gly',
    '¿Cómo reconoce un dominio SH2 a una fosfotirosina?':
        'How does an SH2 domain recognize a phosphotyrosine?',
    'Una Arg suya hace puente salino con el fosfato y el anillo entra en un bolsillo':
        'One of its Arg makes a salt bridge with the phosphate and the ring fits into a pocket',
    'Forma un puente disulfuro con el OH de la Tyr':
        'It forms a disulfide bridge with the Tyr OH',
    'La pTyr tiene carga + y atrae al SH2, que es ácido':
        'pTyr has a + charge and attracts the SH2, which is acidic',
    'Le quita el fosfato y se queda unido al ATP':
        'It removes the phosphate and stays bound to ATP',
    '¿Por qué hay disulfuros en el RE pero casi no en el citosol?':
        'Why are there disulfides in the ER but hardly any in the cytosol?',
    'El RE es oxidante; en el citosol el glutatión los reduce':
        'The ER is oxidizing; in the cytosol glutathione reduces them',
    'En el citosol no hay Cys libres':
        'There are no free Cys in the cytosol',
    'El RE no tiene agua y la reacción no se hidroliza':
        "The ER has no water so the reaction isn't hydrolyzed",
    'En el citosol las Cys están todas fosforiladas':
        'In the cytosol all Cys are phosphorylated',
    '¿Para qué sirve el segundo carboxilato del Gla?':
        "What is Gla's second carboxylate for?",
    'Los dos carboxilatos juntos atrapan un Ca²+':
        'The two carboxylates together trap a Ca²+',
    'Le dan carga + para unirse a los fosfolípidos':
        'They give it a + charge to bind phospholipids',
    'Forman un puente disulfuro con otro Gla':
        'They form a disulfide bridge with another Gla',
    'Lo vuelven hidrofóbico para meterse a la membrana':
        'They make it hydrophobic so it gets into the membrane',
    '¿Por qué la N-glicosilación necesita la secuencia N-X-S/T?':
        'Why does N-glycosylation need the N-X-S/T sequence?',
    'El OH de la Ser/Thr ayuda a activar al N de la amida de la Asn':
        'The Ser/Thr OH helps activate the Asn amide N',
    'El azúcar se une a la Ser/Thr y no a la Asn':
        'The sugar binds Ser/Thr and not Asn',
    'La X tiene que ser una Pro para doblar la cadena':
        'X has to be a Pro to bend the chain',
    'La Ser/Thr le pasa su carga + al azúcar':
        'Ser/Thr passes its + charge to the sugar',
    '¿En qué se diferencia la O-glicosilación de la N-glicosilación?':
        'How does O-glycosylation differ from N-glycosylation?',
    'El azúcar va en el O de Ser/Thr, en el Golgi y sin secuencia consenso':
        'The sugar goes on the O of Ser/Thr, in the Golgi and with no consensus sequence',
    'El azúcar va en el N de la Asn, en el RE y con N-X-S/T':
        'The sugar goes on the Asn N, in the ER and with N-X-S/T',
    'El azúcar va en el S de la Cys, en el citosol':
        'The sugar goes on the Cys S, in the cytosol',
    'Solo ocurre mientras el ribosoma traduce, en el núcleo':
        'It only happens while the ribosome translates, in the nucleus',
    '¿Por qué las mucinas cubiertas de O-glicanos forman moco?':
        'Why do mucins covered in O-glycans form mucus?',
    'Los muchos OH de sus azúcares atrapan agua':
        'The many OH groups of their sugars trap water',
    'Sus azúcares son hidrofóbicos y repelen el agua':
        'Their sugars are hydrophobic and repel water',
    'Sus azúcares forman puentes disulfuro entre sí':
        'Their sugars form disulfide bridges with each other',
    'Sus azúcares tienen carga + y se pegan al ADN':
        'Their sugars have a + charge and stick to DNA',
    '¿Qué pierde la Arg al volverse citrulina?':
        'What does Arg lose when it becomes citrulline?',
    'Su carga +: el guanidinio se vuelve una urea neutra':
        'Its + charge: the guanidinium becomes a neutral urea',
    'Su anillo aromático: se vuelve no polar':
        'Its aromatic ring: it becomes nonpolar',
    'Su carga −: el carboxilato se vuelve amida':
        'Its − charge: the carboxylate becomes an amide',
    'Su fosfato: la PAD es una fosfatasa':
        'Its phosphate: PAD is a phosphatase',
}
