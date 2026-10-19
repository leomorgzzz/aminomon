"""Traducción al inglés de sintesis.py (encargos de síntesis en el ribosoma)."""

EN = {
    'ENCARGO {n}/{t} · {nombre}':
        'ORDER {n}/{t} · {nombre}',
    'Mis células de cultivo no se pegan a la placa y flotan. Las integrinas de su membrana se agarran a un motivo de 3 aminoácidos: RGD. Si cubro la placa con ese péptido, se pegan. Empecemos con algo corto.':
        "My cultured cells won't stick to the dish; they just float. The integrins in their membrane grab onto a 3-amino-acid motif: RGD. If I coat the dish with that peptide, they'll stick. Let's start with something short.",
    'Las células ya se pegan. Fácil, ¿no? El siguiente es más largo.':
        'The cells stick now. Easy, right? The next one is longer.',
    'Me pegué en la membrana con la mesa del laboratorio. Tu cerebro tiene sus propios analgésicos: las encefalinas. Hazme una Met-encefalina (5 aminoácidos).':
        'I bumped my membrane on the lab bench. Your brain has its own painkillers: the enkephalins. Make me a Met-enkephalin (5 amino acids).',
    'Ya no me duele. La morfina funciona porque imita a este péptido.':
        "It doesn't hurt anymore. Morphine works because it mimics this peptide.",
    'Quiero meter una proteína al núcleo, pero el poro nuclear no deja pasar a cualquiera. Necesito su contraseña: una NLS, un parche de Lys y Arg. Desde aquí ya no te enseño los anticodones: elige por el aminoácido. Si no te sabes un codón, búscalo en la Chuleta del manual (M) antes de empezar.':
        "I want to get a protein into the nucleus, but the nuclear pore doesn't let just anyone in. I need its password: an NLS, a patch of Lys and Arg. From now on I won't show you the anticodons: choose by the amino acid. If you don't know a codon, look it up in the manual's Cheat sheet (M) before you start.",
    'Mi proteína ya entra al núcleo. Las importinas reconocieron la NLS.':
        'My protein gets into the nucleus now. The importins recognized the NLS.',
    'Del susto se me bajó la presión. La angiotensina II contrae los vasos y la sube. Son 8 aminoácidos y el ribosoma ya va más rápido.':
        "The scare made my blood pressure drop. Angiotensin II constricts the vessels and raises it. It's 8 amino acids, and the ribosome is faster now.",
    'Presión normal otra vez. Por cierto: los IECA bajan la presión justo porque impiden que se forme la angiotensina II.':
        'Normal pressure again. By the way: ACE inhibitors lower blood pressure precisely because they stop angiotensin II from forming.',
    'Mis ratones de laboratorio no se llevan bien. La oxitocina ayuda al vínculo social. Tiene 2 Cys: después de sintetizarla, las Cys 1 y 6 se unen con un puente disulfuro y cierran un anillo.':
        "My lab mice don't get along. Oxytocin helps social bonding. It has 2 Cys: after it's synthesized, Cys 1 and 6 join through a disulfide bridge and close a ring.",
    'Los ratones ya hasta se acurrucan. El disulfuro se formó solo al oxidarse las dos Cys.':
        'Now the mice even cuddle. The disulfide formed on its own when the two Cys were oxidized.',
    'El último. Quiero meter fármacos a las células, y un virus como yo sabe cómo: el péptido Tat del VIH-1 cruza membranas por su montón de Arg y Lys. Son 11 aminoácidos y el ribosoma va a toda velocidad.':
        "The last one. I want to get drugs into cells, and a virus like me knows how: the HIV-1 Tat peptide crosses membranes thanks to its pile of Arg and Lys. It's 11 amino acids and the ribosome is at full speed.",
    'Cadena (N → C):':
        'Chain (N → C):',
    'ribosoma':
        'ribosome',
    'Tiempo':
        'Time',
    'Elige el ARNt para el codón {cod}':
        'Choose the tRNA for codon {cod}',
    'Pulsa 1-{n} · Esc pausa':
        'Press 1-{n} · Esc pause',
    'Recuerda: el anticodón se aparea base por base, A con U y G con C. No es igual al codón: es su complemento.':
        "Remember: the anticodon pairs base by base, A with U and G with C. It isn't the same as the codon: it's its complement.",
    'Busca esos codones en la Chuleta del manual (M). Si te pasaste del paro o paraste antes, revisa UAA, UAG y UGA.':
        "Look those codons up in the manual's Cheat sheet (M). If you read past the stop or stopped too early, check UAA, UAG and UGA.",
    'Lo repetimos con otros codones (el código es degenerado: un mismo aminoácido tiene varios).':
        "We'll repeat it with other codons (the code is degenerate: one amino acid has several).",
    'El ribosoma soltó la cadena. Después se cortó la Met inicial y quedó el péptido.':
        'The ribosome released the chain. Then the initial Met was cut off, leaving the peptide.',
    'Encargos de síntesis':
        'Synthesis orders',
    'Encargo {n}/{t} del René-virus':
        'René-virus order {n}/{t}',
    'Síntesis libre ({n}/{t})':
        'Free synthesis ({n}/{t})',
    'Factor de liberación (codón de paro)':
        'Release factor (stop codon)',
    'DESDE CERO (1/7) · La receta\n\nUna proteína es una cadena de aminoácidos. La receta viene en el ARNm, una tira de 4 letras (bases): A, U, G y C.':
        'FROM SCRATCH (1/7) · The recipe\n\nA protein is a chain of amino acids. The recipe comes in the mRNA, a strip of 4 letters (bases): A, U, G and C.',
    'DESDE CERO (2/7) · Codones\n\nEl ARNm se lee de 3 en 3 letras. Cada trío es un codón y cada codón dice qué aminoácido sigue. Por ejemplo, UUC = Phe.\n\nHay 64 codones: 61 dan un aminoácido y 3 (UAA, UAG, UGA) significan «fin». AUG es la Met y marca el inicio.':
        'FROM SCRATCH (2/7) · Codons\n\nThe mRNA is read 3 letters at a time. Each triplet is a codon, and each codon says which amino acid comes next. For example, UUC = Phe.\n\nThere are 64 codons: 61 give an amino acid and 3 (UAA, UAG, UGA) mean "end". AUG is Met and marks the start.',
    'DESDE CERO (3/7) · El ribosoma\n\nEs la máquina que lee el ARNm. Tiene tres sitios para ARNt; aquí importan dos:\n• P: el ARNt que carga toda la cadena.\n• A: donde llega el codón siguiente y entra un ARNt nuevo.\n(Por el tercero, el E, sale el ARNt ya vacío.)':
        "FROM SCRATCH (3/7) · The ribosome\n\nIt's the machine that reads the mRNA. It has three tRNA sites; two matter here:\n• P: the tRNA carrying the whole chain.\n• A: where the next codon arrives and a new tRNA enters.\n(The empty tRNA leaves through the third one, E.)",
    "DESDE CERO (4/7) · El ARNt\n\nEs el traductor. De un lado carga un aminoácido y del otro tiene 3 bases, el anticodón, que se pegan al codón: A con U y G con C.\n\nCodón      5'-UUC-3'\nAnticodón  3'-AAG-5'  → este ARNt carga Phe\n\nOjo: el anticodón NO es igual al codón; es su complemento. (En la célula la 3.ª base del codón se aparea con más holgura, el «bamboleo»; aquí todas se aparean exacto.)":
        "FROM SCRATCH (4/7) · The tRNA\n\nIt's the translator. On one end it carries an amino acid, and on the other it has 3 bases, the anticodon, which stick to the codon: A with U and G with C.\n\nCodon      5'-UUC-3'\nAnticodon  3'-AAG-5'  → this tRNA carries Phe\n\nCareful: the anticodon is NOT the same as the codon; it's its complement. (In the cell the codon's 3rd base pairs more loosely, called \"wobble\"; here every base pairs exactly.)",
    'DESDE CERO (5/7) · Unir y avanzar\n\nCuando el ARNt correcto entra al sitio A, el ribosoma pasa la cadena a su aminoácido con un enlace peptídico. Luego avanza un codón y el sitio A queda libre para el siguiente. La cadena crece del extremo N al C.':
        'FROM SCRATCH (5/7) · Join and move on\n\nWhen the right tRNA enters the A site, the ribosome hands the chain over to its amino acid with a peptide bond. Then it moves one codon forward and the A site is free for the next one. The chain grows from the N end to the C end.',
    'DESDE CERO (6/7) · El final\n\nNingún ARNt reconoce UAA, UAG ni UGA. Ahí entra un factor de liberación y la cadena se suelta.\n\nEn la célula estos péptidos salen de proteínas más largas que unas proteasas cortan. El René-virus usa un ARNm de laboratorio: AUG + el péptido + paro. Al final se quita la Met.':
        'FROM SCRATCH (6/7) · The end\n\nNo tRNA recognizes UAA, UAG or UGA. A release factor comes in there and the chain is let go.\n\nIn the cell these peptides come from longer proteins that proteases cut. The René-virus uses a lab mRNA: AUG + the peptide + stop. At the end the Met is removed.',
    'CÓMO FUNCIONA (7/7)\n\n• La Met inicial ya está en el sitio P.\n• Cada codón llega al sitio A: elige su ARNt con 1-4 antes de que se acabe la barra. En el codón de paro elige el factor de liberación (5).\n• Si fallas o se acaba el tiempo, la proteína sale mutada. No te digo la respuesta: al final te marco qué codones fallaste y lo repites con otros codones.\n• En los 2 primeros encargos ves los anticodones; después, solo el aminoácido.\n• Esc pausa el ribosoma.':
        "HOW IT WORKS (7/7)\n\n• The initial Met is already in the P site.\n• Each codon arrives at the A site: choose its tRNA with 1-4 before the bar runs out. At the stop codon choose the release factor (5).\n• If you miss or time runs out, the protein comes out mutated. I won't tell you the answer: at the end I mark the codons you missed and you repeat it with other codons.\n• In the first 2 orders you see the anticodons; after that, only the amino acid.\n• Esc pauses the ribosome.",
    'Péptido: {nombre}, {k} aminoácidos. Tiempo por codón: {s} s.':
        'Peptide: {nombre}, {k} amino acids. Time per codon: {s} s.',
    'SÍNTESIS LIBRE · {nombre}':
        'FREE SYNTHESIS · {nombre}',
    'Encargos de síntesis ({n}/{t})':
        'Synthesis orders ({n}/{t})',
    'La proteína salió mal. Revisa los codones con × (· = no se llegó a leer):':
        'The protein came out wrong. Check the codons marked × (· = never read):',
    '¿Otra vez?':
        'Again?',
    '¿Cómo funciona?':
        'How does it work?',
    'anticodón':
        'anticodon',
    'Se acabó el tiempo en {cod}: cuenta como error.':
        'Time ran out on {cod}: it counts as a mistake.',
    'Sí, con otros codones':
        'Yes, with other codons',
    'Encargo {n}/{t}: {nombre}':
        'Order {n}/{t}: {nombre}',
    'Repetir un encargo':
        'Repeat an order',
    'Síntesis libre (los otros péptidos del catálogo)':
        'Free synthesis (the other peptides in the catalog)',
    'Pausa':
        'Pause',
    'Liberaste la cadena antes de tiempo: {cod} no es de paro.':
        'You released the chain too early: {cod} is not a stop codon.',
    'Seguir':
        'Continue',
    'Salir del encargo':
        'Leave the order',
    'Ese ARNt no se aparea con {cod}.':
        "That tRNA doesn't pair with {cod}.",
    '√ {aa} unida a la cadena.':
        '√ {aa} joined to the chain.',
    '{cod} es de paro: ningún ARNt lo reconoce.':
        '{cod} is a stop codon: no tRNA recognizes it.',
    'Volver':
        'Back',
    'Selenoproteína sintetizada':
        'Selenoprotein synthesized',
    'ENCARGO ESPECIAL · La selenoproteína\n\nQuiero el final de la tiorredoxina reductasa 1 humana, la enzima que recarga a la tiorredoxina (la que repara proteínas oxidadas): Gly-Cys-Sec-Gly. Su Sec y la Cys vecina forman el puente selenilsulfuro que ya conoces.':
        'SPECIAL ORDER · The selenoprotein\n\nI want the end of human thioredoxin reductase 1, the enzyme that recharges thioredoxin (the one that repairs oxidized proteins): Gly-Cys-Sec-Gly. Its Sec and the neighboring Cys form the selenylsulfide bridge you already know.',
    'REPASO · ¿Cómo entra la Sec?\n\n• La Sec no tiene codón propio: usa UGA, que normalmente es de paro.\n• En el ARNm de una selenoproteína, después del codón de paro, hay una horquilla llamada SECIS (en el dibujo: ···SECIS).\n• Con ayuda de unas proteínas (SBP2 y EFSec), el SECIS atrae al ARNt-Sec, que ya trae la Sec (se armó sobre una Ser). Con él, ese UGA se lee como Sec.':
        "REVIEW · How does Sec get in?\n\n• Sec has no codon of its own: it uses UGA, which is normally a stop.\n• In a selenoprotein's mRNA, after the stop codon, there is a hairpin called SECIS (in the drawing: ···SECIS).\n• With the help of some proteins (SBP2 and EFSec), the SECIS recruits the Sec-tRNA, which already carries Sec (built on a Ser). With it, that UGA is read as Sec.",
    "CÓMO FUNCIONA\n\n• Igual que los otros encargos, con anticodones a la vista.\n• El anticodón del ARNt-Sec es 3'-ACU-5': se aparea con UGA.\n• Aquí el paro es UAA o UAG; en ese codón sí va el factor de liberación.\n• Son 4 aminoácidos y {s} s por codón.":
        "HOW IT WORKS\n\n• Same as the other orders, with the anticodons shown.\n• The Sec-tRNA's anticodon is 3'-ACU-5': it pairs with UGA.\n• Here the stop is UAA or UAG; that codon does take the release factor.\n• It's 4 amino acids and {s} s per codon.",
    'ENCARGO ESPECIAL · Tiorredoxina reductasa (Gly-Cys-Sec-Gly)':
        'SPECIAL ORDER · Thioredoxin reductase (Gly-Cys-Sec-Gly)',
    'Encargo especial: la selenoproteína':
        'Special order: the selenoprotein',
    'Liberaste la cadena: con el SECIS, este UGA no es de paro.':
        'You released the chain: with the SECIS, this UGA is not a stop.',
    '¡Lo lograste, {jugador}! Con este péptido pego fármacos y los meto a las células. Ya lees ARNm como un ribosoma.':
        'You did it, {jugador}! With this peptide I can attach drugs and get them into cells. You read mRNA like a ribosome now.',
    'El UGA se leyó como Sec gracias al SECIS, y el paro UAA/UAG soltó la cadena. En la enzima completa (casi 500 aminoácidos) este final es el sitio activo: la Sec y la Cys vecina reducen a la tiorredoxina y quedan unidas por un puente Se–S, que la propia enzima vuelve a abrir con NADPH.':
        'The UGA was read as Sec thanks to the SECIS, and the UAA/UAG stop released the chain. In the full enzyme (almost 500 amino acids) this end is the active site: the Sec and the neighboring Cys reduce thioredoxin and end up joined by a Se–S bridge, which the enzyme itself opens again with NADPH.',
    '{jugador}, sintetizaste Gly-Cys-Sec-Gly.':
        '{jugador}, you synthesized Gly-Cys-Sec-Gly.',
}
