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
    'CÓMO FUNCIONA\n\n• Camina con WASD o las flechas hasta una mesa.\n• T titulación: pon el cursor sobre la curva donde está el pK o el pI.\n• E electroforesis: elige hacia qué electrodo va cada aminoácido.\n• I intercambio iónico: di en qué orden salen de la columna.\n• Son {n} problemas por visita; arriba ves tu cuenta. La salida está abajo.':
        'HOW IT WORKS\n\n• Walk with WASD or the arrows to a bench.\n• T titration: put the cursor on the curve where the pK or the pI is.\n• E electrophoresis: choose which electrode each amino acid moves to.\n• I ion exchange: say in what order they leave the column.\n• There are {n} problems per visit; your count is at the top. The exit is at the bottom.',
    'SELENOCISTEÍNA · pregunta {n}/3 · aciertos {a}':
        'SELENOCYSTEINE · question {n}/3 · correct {a}',
    '¡3/3! Una Ser se cargó en el ARNt-Sec y, con selenofosfato, se convirtió en selenocisteína. Ya está en tu equipo y en la Aminodex, en una sección aparte: no cuenta en el 20/20.':
        "3/3! A Ser was loaded onto tRNA-Sec and, with selenophosphate, became selenocysteine. It's now on your team and in the Aminodex, in a separate section: it doesn't count toward the 20/20.",
    'SELENOCISTEÍNA · Sec · U  (fuera de los 20)':
        'SELENOCYSTEINE · Sec · U  (outside the 20)',
    'el pK1: donde amortigua el α-COOH':
        'pK1: where the α-COOH buffers',
    'el pK2: donde amortigua el α-NH3+':
        'pK2: where the α-NH3+ buffers',
    'el pKR: donde amortigua la cadena lateral':
        'pKR: where the side chain buffers',
    'el pI: donde la carga neta es 0':
        'the pI: where the net charge is 0',
    'Cada pK queda a media meseta: ahí la mitad del grupo ya soltó su H+ y el pH cambia poco. El pI queda entre dos mesetas: ahí la carga neta es 0.':
        'Each pK sits in the middle of a plateau: there half of the group has released its H+ and the pH barely changes. The pI lies between two plateaus: there the net charge is 0.',
    'eq de OH−':
        'eq of OH−',
    'Por debajo de su pI un aminoácido tiene carga + y va al cátodo (−); por encima, carga − y va al ánodo (+).':
        'Below its pI an amino acid has a + charge and moves to the cathode (−); above it, a − charge and moves to the anode (+).',
    'Cargas a pH 6, de la primera en salir a la última: {d}. Lo más negativo pasa de largo; lo más positivo se queda pegado a la resina.':
        'Charges at pH 6, from first out to last: {d}. The most negative passes straight through; the most positive sticks to the resin.',
    'De regalo: un ♦ junto al título del mapa. Gracias por jugar; puedes seguir practicando todo lo que quieras.':
        'Your gift: a ♦ next to the map title. Thanks for playing; you can keep practicing as much as you like.',
    'CERTIFICADO · Aminomon completo':
        'CERTIFICATE · Aminomon complete',
    'Para este evento necesitas una Ser en tu equipo: la Sec se arma sobre una Ser.':
        'For this event you need a Ser on your team: Sec is built on a Ser.',
    'Hay un aminoácido fuera de los 20: la selenocisteína (Sec, U). Unas 25 proteínas humanas la usan, como la glutatión peroxidasa.':
        "There's an amino acid outside the 20: selenocysteine (Sec, U). About 25 human proteins use it, such as glutathione peroxidase.",
    'CÓMO FUNCIONA\n\n• Son 3 preguntas sobre cómo la célula mete la Sec en una proteína.\n• Después de cada una te digo si acertaste y por qué.\n• Con las 3 bien, una Sec se une a tu equipo. Si fallas alguna, repítelo cuando quieras.':
        'HOW IT WORKS\n\n• 3 questions about how the cell puts Sec into a protein.\n• After each one I tell you whether you got it and why.\n• Get all 3 right and a Sec joins your team. If you miss one, try again whenever you like.',
    'UGA, que normalmente es de paro.':
        'UGA, which is normally a stop codon.',
    'La horquilla SECIS recluta las proteínas que traen el ARNt-Sec al ribosoma.':
        'The SECIS hairpin recruits the proteins that bring tRNA-Sec to the ribosome.',
    'Se parece a la Cys (Se en lugar de S), pero nace de una Ser: la seril-ARNt sintetasa carga Ser y luego enzimas cambian su O por Se, del selenofosfato.':
        'It looks like Cys (Se instead of S), but it starts as a Ser: seryl-tRNA synthetase loads Ser and then enzymes swap its O for Se, from selenophosphate.',
    'Aciertos {a}/{n}':
        'Correct {a}/{n}',
    '{a}/3. Necesitas las 3: vuelve cuando quieras.':
        '{a}/3. You need all 3: come back whenever you like.',
    'Fuera de los 5 grupos de Lehninger. En el juego: Polar (como la Cys) y Cargado − (a pH 7 casi toda está como –Se−).':
        "Outside Lehninger's 5 groups. In the game: Polar (like Cys) and Charged − (at pH 7 almost all of it is –Se−).",
    '≈ 5.2 (selenol; el tiol de la Cys es 8.18)':
        '≈ 5.2 (selenol; the Cys thiol is 8.18)',
    'Codón':
        'Codon',
    'UGA + un elemento SECIS en el ARNm':
        'UGA + a SECIS element in the mRNA',
    'Cómo se hace':
        "How it's made",
    'Sobre su ARNt: se carga con Ser y la Ser se convierte en Sec. No es una modificación postraduccional.':
        "On its tRNA: it's loaded with Ser and the Ser is converted into Sec. It is not a post-translational modification.",
    'Dónde está':
        'Where it is',
    '~25 proteínas humanas: glutatión peroxidasas, tiorredoxina reductasas y desyodasas tiroideas.':
        '~25 human proteins: glutathione peroxidases, thioredoxin reductases and thyroid deiodinases.',
    'Es la selenocisteína (Sec, U): como la Cys, pero con Se en lugar de S.':
        "It's selenocysteine (Sec, U): like Cys, but with Se instead of S.",
    'TITULACIÓN · {nombre} 0.1 M con NaOH':
        'TITRATION · {nombre} 0.1 M with NaOH',
    'Pon el cursor en {que}':
        'Put the cursor on {que}',
    '←/→ mover el cursor (Shift o A/D: más rápido) · Enter aquí · Esc salir':
        '←/→ move the cursor (Shift or A/D: faster) · Enter here · Esc quit',
    'ELECTROFORESIS · amortiguador a pH {ph}':
        'ELECTROPHORESIS · buffer at pH {ph}',
    '¿Hacia dónde migra cada aminoácido? ↑/↓ carril · ←/→ dirección · Enter correr el gel':
        'Where does each amino acid migrate? ↑/↓ lane · ←/→ direction · Enter run the gel',
    '(−) cátodo':
        '(−) cathode',
    'ánodo (+)':
        'anode (+)',
    'INTERCAMBIO IÓNICO · resina catiónica (−) · pH {ph}':
        'ION EXCHANGE · cation resin (−) · pH {ph}',
    '¿En qué orden salen? Pulsa las letras del primero al último · Retroceso borra':
        'In what order do they come out? Press the letters from first to last · Backspace erases',
    'salida':
        'outlet',
    'Tu orden: {o}':
        'Your order: {o}',
    'La resina tiene cargas −: retiene lo que es +.':
        'The resin has − charges: it holds back what is +.',
    'Bienvenida a mi laboratorio de proteómica: aquí la química de cada aminoácido se mide.':
        "Welcome to my proteomics lab: here each amino acid's chemistry gets measured.",
    'LABORATORIO DEL RENÉ-VIRUS · problemas {h}/{n} · aciertos {a} · récord {r}':
        'RENÉ-VIRUS LAB · problems {h}/{n} · correct {a} · record {r}',
    'Intercambio':
        'Ion exchange',
    'WASD/flechas caminar · Esc salir del laboratorio':
        'WASD/arrows walk · Esc leave the lab',
    '{a}/{h} problemas resueltos.':
        '{a}/{h} problems solved.',
    'Una selenocisteína se unió a tu equipo.':
        'A selenocysteine joined your team.',
    'Valores (Lehninger, 25 °C)':
        'Values (Lehninger, 25 °C)',
    'Cursor: {eq:.2f} eq de OH−':
        'Cursor: {eq:.2f} eq of OH−',
    'Pista: un pK está en la mitad':
        'Hint: a pK is in the middle',
    'de una meseta (ahí amortigua).':
        'of a plateau (it buffers there).',
    'El pI, entre los dos pK que':
        'The pI, between the two pKs',
    'rodean la forma neutra.':
        'around the neutral form.',
    'al cátodo':
        'to the cathode',
    'casi no se mueve':
        'barely moves',
    'al ánodo':
        'to the anode',
    'No: el orden era {o}.':
        'No: the order was {o}.',
    'Aciertos de reconocimiento: {a} · contrarreloj: {r} · laboratorio: {l}/6':
        'Recognition hits: {a} · time trial: {r} · lab: {l}/6',
    'pKR (cadena)   {v:.2f}':
        'pKR (chain)    {v:.2f}',
    'carga':
        'charge',
    '√ Resuelto.':
        '√ Solved.',
    'x Esta vez no.':
        'x Not this time.',
    'No. Era: {r}.':
        'No. It was: {r}.',
    'hechos: {n}':
        'done: {n}',
    'Casi: {k} estaba en pH {ph:.2f} (marcado con X); dejaste el cursor en pH {tu:.1f}.':
        'Close: {k} was at pH {ph:.2f} (marked with X); you left the cursor at pH {tu:.1f}.',
    'Capturaste los 20 aminoácidos, conseguiste las {m} modificaciones, ganaste las {i} insignias, aprobaste los dos exámenes, conociste a la selenocisteína, cumpliste los {p} encargos de síntesis y resolviste el laboratorio.':
        'You caught the 20 amino acids, got the {m} modifications, won the {i} badges, passed both exams, met selenocysteine, completed the {p} synthesis orders and solved the lab.',
    'pH en el cursor: {ph:.1f}':
        'pH at the cursor: {ph:.1f}',
    'En los tramos verticales el':
        'On the vertical stretches the',
    'cursor sube por la curva.':
        'cursor climbs along the curve.',
}
