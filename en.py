"""Traducción al inglés: texto en español (el que aparece en el código) →
texto en inglés. Lo usa idioma.tr(). Si cambias un texto en español en el
código, actualiza aquí su clave; si falta una traducción, el juego muestra el
español."""


EN = {
    'Atrapa y aprende los 20 aminoácidos':
        'Catch and learn the 20 amino acids',
    'René-virus':
        'René-virus',
    'Explora la célula. [M] abre el manual.':
        'Explore the cell. [M] opens the manual.',
    'WASD/flechas mover · M manual · X aminodex · E equipo · G guardar · Q salir':
        'WASD/arrows move · M manual · X aminodex · E team · G save · Q quit',
    'Insignias ':
        'Badges ',
    'Entraste a: {zona}':
        'You entered: {zona}',
    'Agranda la terminal a 80×24 o más (ahora {ancho}×{alto}).':
        'Enlarge the terminal to 80×24 or more (now {ancho}×{alto}).',
    'Lo ideal: pantalla completa (F11 o Alt+Enter).':
        'Best: full screen (F11 or Alt+Enter).',
    'Consejo: pon la terminal en pantalla completa (F11 o Alt+Enter). Ahora: {ancho}×{alto}':
        'Tip: put the terminal in full screen (F11 or Alt+Enter). Now: {ancho}×{alto}',
    'Continuar':
        'Continue',
    'Nueva partida':
        'New game',
    'Manual':
        'Manual',
    'Salir':
        'Quit',
    'Soy el René-virus, un virus inofensivo: no enfermo a nadie, solo estudio proteómica. Como todo virus, no tengo ribosomas propios: mis proteínas las fabrican los ribosomas de la célula con los 20 aminoácidos estándar. Tu trabajo es encontrarlos y caracterizarlos.':
        "I'm the René-virus, a harmless virus: I don't make anyone sick, I just study proteomics. Like every virus, I have no ribosomes of my own: my proteins are made by the cell's ribosomes from the 20 standard amino acids. Your job is to find them and characterize them.",
    'Cada aminoácido abunda donde su química es favorable: los no polares en la membrana, los básicos junto al ARN ribosomal y al ADN.':
        'Each amino acid is abundant where its chemistry is favorable: the nonpolar ones in the membrane, the basic ones next to ribosomal RNA and DNA.',
    'Cada aminoácido pertenece a uno de los 5 grupos de Lehninger y cada movimiento usa la química de uno de ellos. La afinidad depende de la interacción real entre los dos grupos; la tabla completa está en el manual [M].':
        "Each amino acid belongs to one of Lehninger's 5 groups, and each move uses the chemistry of one of them. Affinity depends on the real interaction between the two groups; the full table is in the manual [M].",
    'Empiezas con Metionina: AUG es el codón de inicio, así que toda proteína comienza con ella.':
        'You start with Methionine: AUG is the start codon, so every protein begins with it.',
    'Elige un segundo aminoácido (1-3)':
        'Choose a second amino acid (1-3)',
    'Cargado +. Puente salino ×2 contra los ácidos del RE y catión–π contra los aromáticos.':
        'Charged +. Salt bridge ×2 against the acidic ones in the ER and cation–π against the aromatic ones.',
    'Cargado −. Puente salino ×2 contra los básicos de los ribosomas y del núcleo.':
        'Charged −. Salt bridge ×2 against the basic ones in the ribosomes and the nucleus.',
    'Polar sin carga. Puentes de H ×2 contra los polares. Con ATP una quinasa la fosforila y se vuelve Cargado −.':
        'Polar uncharged. H-bonds ×2 against polar ones. With ATP a kinase phosphorylates it and it becomes Charged −.',
    'Tu equipo inicial: Metionina y {nombre}.\n\nEn las zonas marcadas con símbolos aparecen aminoácidos salvajes. Deduce su grupo [D], usa movimientos afines y, con afinidad ≥ 50, lanza un ARNt [T].':
        'Your starting team: Methionine and {nombre}.\n\nWild amino acids appear in the areas marked with symbols. Deduce their group [D], use moves with affinity and, with affinity ≥ 50, throw a tRNA [T].',
    'La mitocondria (◉) restablece a tu equipo y recarga ATP. Los jefes (J) piden construir péptidos. Para entrar al núcleo necesitas una NLS rica en Lys (K), que encontrarás en los ribosomas (∴); la Arg (R) solo vive dentro del núcleo. Los carteles (i) describen cada compartimento. Yo soy la V del mapa: búscame cuando quieras un consejo.':
        "The mitochondrion (◉) restores your team and recharges ATP. Bosses (J) ask you to build peptides. To enter the nucleus you need an NLS rich in Lys (K), which you'll find in the ribosomes (∴); Arg (R) only lives inside the nucleus. Signs (i) describe each compartment. I'm the V on the map: come find me whenever you want advice.",
    ' · P cadena':
        ' · P chain',
    'EQUIPO':
        'TEAM',
    'ATP {atp}  Vit C {c}  Vit K {k}':
        'ATP {atp}  Vit C {c}  Vit K {k}',
    'Aminodex {n}/20':
        'Aminodex {n}/20',
    'Mitocondria: equipo restablecido y ATP recargado (5).':
        'Mitochondrion: team restored and ATP recharged (5).',
    'Un aminoácido salvaje se acerca.':
        'A wild amino acid approaches.',
    'Partida guardada.':
        'Game saved.',
    'Aminodex {n}/20  Insignias {i}/{total}  ATP {atp}':
        'Aminodex {n}/20  Badges {i}/{total}  ATP {atp}',
    'Aquí viven:':
        'Lives here:',
    'Niveles {a}–{b}':
        'Levels {a}–{b}',
    '  … y {n} más [E]':
        '  … and {n} more [E]',
    'Péptidos {n}/{total}':
        'Peptides {n}/{total}',
    'MAPA':
        'MAP',
    'La envoltura nuclear no deja pasar: entra por un poro (O).':
        "The nuclear envelope won't let you through: enter through a pore (O).",
    'El poro nuclear no te deja pasar sin una NLS (≥ 4 Lys). Búscalas en los ribosomas (∴).':
        "The nuclear pore won't let you through without an NLS (≥ 4 Lys). Look for them in the ribosomes (∴).",
    '¡Completaste la Aminodex! Te regalo una cadena naciente: desde ahora tu equipo te sigue por el mapa como un péptido, cada residuo con su código de 1 letra y el color de su grupo. [P] la muestra u oculta.':
        "You completed the Aminodex! Here's a gift: a nascent chain. From now on your team follows you around the map like a peptide, each residue with its 1-letter code and its group's color. [P] shows or hides it.",
    '¡Conseguiste todas las modificaciones postraduccionales! En tu cadena, los residuos modificados ahora se ven marcados con el color de su nuevo grupo, y el título del mapa se pinta con los 5 grupos de Lehninger.':
        "You got all the post-translational modifications! In your chain, modified residues are now marked with their new group's color, and the map title is painted with Lehninger's 5 groups.",
    'Faltan {n} aminoácidos. Zonas con especies pendientes: {zonas}.':
        '{n} amino acids missing. Areas with species still to find: {zonas}.',
    'Retos pendientes: {retos}.':
        'Pending challenges: {retos}.',
    'Tu equipo está cansado: ve a la mitocondria (◉).':
        'Your team is tired: go to the mitochondrion (◉).',
    '¿Borrar la partida guardada?':
        'Delete the saved game?',
    '¿Elegir a {nombre}?':
        'Choose {nombre}?',
    'Zona segura: cura y ATP':
        'Safe zone: healing and ATP',
    'En esta zona aparece un solo aminoácido.':
        'Only one amino acid appears in this area.',
    'Aminodex completa. Te faltan {n} modificaciones: {mods}. Sus requisitos están en el manual [M].':
        "Aminodex complete. You're missing {n} modifications: {mods}. Their requirements are in the manual [M].",
    'Aminodex completa, con todas las modificaciones.':
        'Aminodex complete, with all the modifications.',
    'Ya tienes todas las insignias: presenta el examen de la Chaperona (H).':
        "You have all the badges: take the Chaperone's exam (H).",
    'Capturaste los 20 aminoácidos estándar. Habla con el René-virus (V): tiene algo para ti.':
        'You caught the 20 standard amino acids. Talk to the René-virus (V): it has something for you.',
    'Aminodex completa':
        'Aminodex complete',
    'Todo tu equipo se desnaturalizó. Vuelves a la mitocondria con la energía restablecida.':
        'Your whole team denatured. You return to the mitochondrion with your energy restored.',
    'Equipo desnaturalizado':
        'Team denatured',
    'Escapaste sin problemas.':
        'You got away safely.',
    'Sí, empezar de cero':
        'Yes, start over',
    'Sí':
        'Yes',
    'Nv':
        'Lv',
    'En esta zona aparecen {n} aminoácidos distintos.':
        '{n} different amino acids appear in this area.',
    'Encargo de síntesis':
        'Synthesis order',
    'Repetir el examen final':
        'Retake the final exam',
    'Nada por ahora':
        'Nothing for now',
    'Ya tienes la insignia de esta zona.':
        "You already have this area's badge.",
    'Ya tienes la Maestría de la Chaperona. Solo te falta mi examen final.':
        "You already have the Chaperone's Master's degree. All that's left is my final exam.",
    '¿Tomar el examen final del René-virus?':
        "Take the René-virus's final exam?",
    'Encontraste 1 {objeto}: {desc}':
        'You found 1 {objeto}: {desc}',
    'Ya llevas el máximo de {objeto} (3).':
        'You already carry the maximum of {objeto} (3).',
    'Encargos de síntesis: {n}/{total} péptidos del catálogo. Los largos piden varias copias del mismo aminoácido: sigue capturando.':
        'Synthesis orders: {n}/{total} peptides in the catalog. The long ones need several copies of the same amino acid: keep catching.',
    'Catálogo de péptidos completo. Puedes repetir encargos y mi examen para seguir practicando.':
        'Peptide catalog complete. You can repeat orders and my exam to keep practicing.',
    'Ahora no':
        'Not now',
    'Cadena visible.':
        'Chain visible.',
    'Cadena oculta.':
        'Chain hidden.',
    'Partida guardada en ~/.aminomon.json':
        'Game saved to ~/.aminomon.json',
    'Hidropatía':
        'Hydropathy',
    'nivel {n}':
        'level {n}',
    'Grupo R  ':
        'R group  ',
    'modificación postraduccional':
        'post-translational modification',
    'péptido sintetizado para el René-virus':
        'peptide synthesized for the René-virus',
    'AMINODEX  ·  capturados {n}/20  ·  vistos {vistos}/20  ·  modificaciones {ne}/{total}':
        'AMINODEX  ·  caught {n}/20  ·  seen {vistos}/20  ·  modifications {ne}/{total}',
    'estar en {zona}':
        'be in {zona}',
    'otra Cys en el equipo':
        'another Cys in the team',
    'Grupo':
        'Group',
    'Carga pH 7':
        'Charge pH 7',
    'Masa':
        'Mass',
    'Nutrición':
        'Nutrition',
    'Codones':
        'Codons',
    'Interacciones':
        'Interactions',
    '{n} por descubrir':
        '{n} to discover',
    'Modificaciones':
        'Modifications',
    'De':
        'From',
    'Carga':
        'Charge',
    'Cómo':
        'How',
    'Cambio':
        'Change',
    '  ·  péptidos {n}/{total}':
        '  ·  peptides {n}/{total}',
    '↑/↓ elegir   ←/→ saltar de aminoácido   M manual   Esc salir':
        '↑/↓ select   ←/→ jump between amino acids   M manual   Esc exit',
    '— (cadena no ionizable)':
        '— (non-ionizable side chain)',
    'Péptido {n}: aún no lo sintetizas. Pídeselo al René-virus (V).':
        'Peptide {n}: not synthesized yet. Ask the René-virus (V) for it.',
    'su forma base':
        'its base form',
    'Captura primero a {base}.':
        'Catch {base} first.',
    'Aún no lo has encontrado.':
        "You haven't found it yet.",
    'Estructura observada, aún sin capturar. Aparece en: ':
        'Structure observed, not caught yet. Appears in: ',
    'agitación térmica':
        'thermal agitation',
    'H δ+ entre dos átomos δ−: se atraen, no se repelen':
        "H δ+ between two δ− atoms: they attract, they don't repel",
    'el H δ+ apunta al par libre δ−: se atraen':
        'the δ+ H points at the δ− lone pair: they attract',
    'dos grupos con carga opuesta se atraen':
        'two groups with opposite charge attract each other',
    'puente salino':
        'salt bridge',
    'se acercan dos grupos con la MISMA carga…':
        'two groups with the SAME charge approach…',
    'repulsión electrostática':
        'electrostatic repulsion',
    'cada cadena no polar está rodeada de agua ordenada':
        'each nonpolar chain is surrounded by ordered water',
    'al juntarse, esa agua ordenada queda libre':
        'when they come together, that ordered water is set free',
    'efecto hidrofóbico: ↑ entropía del agua':
        'hydrophobic effect: ↑ water entropy',
    'intentan juntarse…':
        'they try to come together…',
    'el agua los mantiene separados':
        'water keeps them apart',
    'un H unido a O o N se acerca a otro O o N':
        'an H bonded to O or N approaches another O or N',
    'puente de hidrógeno':
        'hydrogen bond',
    'se acercan…':
        'they approach…',
    'no se forma puente de H':
        'no H-bond forms',
    'apilamiento π–π':
        'π–π stacking',
    'interacción catión–π':
        'cation–π interaction',
    'puente de H X–H···π':
        'X–H···π H-bond',
    'dos grupos se acercan hasta casi tocarse':
        'two groups approach until they almost touch',
    'fuerzas de London (van der Waals)':
        'London forces (van der Waals)',
    'puentes de H del esqueleto':
        'backbone H-bonds',
    'dos tioles (SH) se acercan':
        'two thiols (SH) approach',
    "codón     5'-{cod}-3'":
        "codon      5'-{cod}-3'",
    "anticodón 3'-{cod}-5'":
        "anticodon  3'-{cod}-5'",
    'dos anillos aromáticos se acercan':
        'two aromatic rings approach',
    'un catión baja hacia la cara del anillo':
        'a cation comes down toward the face of the ring',
    'un X–H apunta hacia la cara del anillo':
        'an X–H points toward the face of the ring',
    "el ARNt trae la {tres} unida a su extremo 3'":
        "the tRNA brings {tres} attached to its 3' end",
    'cargas iguales se repelen':
        'like charges repel',
    'dos esqueletos peptídicos se alinean':
        'two peptide backbones line up',
    'se oxidan: salen 2H⁺ + 2e⁻':
        'they oxidize: 2H⁺ + 2e⁻ leave',
    'enlace covalente S–S (cistina)':
        'covalent S–S bond (cystine)',
    'el movimiento térmico desordena tus interacciones':
        'thermal motion disrupts your interactions',
    'bases complementarias y antiparalelas: A·U, G·C':
        'complementary, antiparallel bases: A·U, G·C',
    'atracción electrostática entre + y −':
        'electrostatic attraction between + and −',
    'el agua forma una capa alrededor del grupo polar':
        'water forms a shell around the polar group',
    'H (δ+) del donador ··· par libre (δ−) del aceptor':
        'H (δ+) of the donor ··· lone pair (δ−) of the acceptor',
    'se apilan cara a cara, desplazados':
        'they stack face to face, offset',
    'la nube π (rica en electrones) atrae la carga +':
        'the π cloud (electron-rich) attracts the + charge',
    'puente de H débil: la nube π hace de aceptor':
        'weak H-bond: the π cloud acts as acceptor',
    'un dipolo instantáneo induce otro en el vecino':
        'an instantaneous dipole induces another in its neighbor',
    'N–H de un esqueleto ··· O═C del otro':
        'N–H of one backbone ··· O═C of the other',
    'falta un donador o un aceptor':
        'a donor or an acceptor is missing',
    '─pirrolidina':
        '─pyrrolidine',
    'pirrolidina─':
        'pyrrolidine─',
    '─CH₂─fenilo':
        '─CH₂─phenyl',
    'fenilo─CH₂─':
        'phenyl─CH₂─',
    '─fenol─OH':
        '─phenol─OH',
    'HO─fenol─':
        'HO─phenol─',
    '─indol(N─H)':
        '─indole(N─H)',
    '(H─N)indol─':
        '(H─N)indole─',
    '─guanidinio⁺':
        '─guanidinium⁺',
    '⁺guanidinio─':
        '⁺guanidinium─',
    '─imidazol(H⁺)':
        '─imidazole(H⁺)',
    '(H⁺)imidazol─':
        '(H⁺)imidazole─',
    '─pirrolidina─OH':
        '─pyrrolidine─OH',
    'HO─pirrolidina─':
        'HO─pyrrolidine─',
    '─fenil─O─PO₃²⁻':
        '─phenyl─O─PO₃²⁻',
    '²⁻O₃P─O─fenil─':
        '²⁻O₃P─O─phenyl─',
    '─CONH─glicano':
        '─CONH─glycan',
    'glicano─HNOC─':
        'glycan─HNOC─',
    '─fenol─O─H':
        '─phenol─O─H',
    '─fenol(H)O:':
        '─phenol(H)O:',
    'H─O─fenol─':
        'H─O─phenol─',
    ':O(H)─fenol─':
        ':O(H)─phenol─',
    '─indol─N─H':
        '─indole─N─H',
    'H─N─indol─':
        'H─N─indole─',
    '─imidazol─N─H':
        '─imidazole─N─H',
    '─imidazol─N:':
        '─imidazole─N:',
    'H─N─imidazol─':
        'H─N─imidazole─',
    ':N─imidazol─':
        ':N─imidazole─',
    'interacción':
        'interaction',
    'Aminoácido salvaje  ·  {zona}  ·  turno {n}':
        'Wild amino acid  ·  {zona}  ·  turn {n}',
    'Salvaje':
        'Wild',
    'Nv {n}':
        'Lv {n}',
    'Afinidad':
        'Affinity',
    'Tu aminoácido':
        'Your amino acid',
    'Energía':
        'Energy',
    '1-5 mover · T ARNt · D deducir · C cambiar · H huir · I info · M manual · V velocidad: {vel}':
        '1-5 move · T tRNA · D deduce · C change · H flee · I info · M manual · V speed: {vel}',
    '1-5 mover  T ARNt  D deducir  C cambiar  H huir  I info  M manual  V {vel}':
        '1-5 move  T tRNA  D deduce  C change  H flee  I info  M manual  V {vel}',
    'los dos solo pueden donar H':
        'both can only donate H',
    'los dos solo pueden aceptar H':
        'both can only accept H',
    '¿Grupo de Lehninger?':
        'Lehninger group?',
    'No. Era {grupo}. Pierdes el turno.':
        'No. It was {grupo}. You lose your turn.',
    'Entra {nombre}.':
        '{nombre} comes in.',
    '{nombre} ({tres}, {una}) se une a tu equipo.\n\nGrupo: {grupo}\nFicha completa en la Aminodex [X].':
        '{nombre} ({tres}, {una}) joins your team.\n\nGroup: {grupo}\nFull entry in the Aminodex [X].',
    'El ARNt se suelta (−20 afinidad).':
        'The tRNA lets go (−20 affinity).',
    'Grupo: {grupo}':
        'Group: {grupo}',
    'Interacciones de {nombre}':
        'Interactions of {nombre}',
    'Deduce su grupo [D] o interactúa [1-5].':
        'Deduce its group [D] or interact [1-5].',
    'puente de H del esqueleto':
        'backbone H-bond',
    '[¿grupo?]  D: deducir':
        '[group?]  D: deduce',
    'listo: [T] ARNt':
        'ready: [T] tRNA',
    '[T] ARNt':
        '[T] tRNA',
    'Neutro':
        'Neutral',
    'tu {tres}':
        'your {tres}',
    'Sin otra Cys no hay disulfuro: no se forma ninguna interacción.':
        "Without another Cys there's no disulfide: no interaction forms.",
    'Enlace covalente S–S entre las dos Cys: afinidad máxima.':
        'Covalent S–S bond between the two Cys: maximum affinity.',
    'Sin afinidad: se repelen.':
        'No affinity: they repel.',
    'La repulsión aleja a {nombre}: escapó.':
        'The repulsion pushes {nombre} away: it escaped.',
    'Agitación térmica de {nombre}: −{n} de energía.':
        'Thermal agitation from {nombre}: −{n} energy.',
    'Su grupo ya es evidente: {grupo}.':
        'Its group is now obvious: {grupo}.',
    'Ya conoces su grupo.':
        'You already know its group.',
    '¿Solo C/H? ¿anillo? ¿OH/SH/amida? ¿NH₃⁺? ¿COO⁻?':
        'Only C/H? ring? OH/SH/amide? NH₃⁺? COO⁻?',
    '¿Y su carácter?':
        'And its character?',
    'Correcto: {grupo}. +10 afinidad, +5 XP':
        'Correct: {grupo}. +10 affinity, +5 XP',
    '¿Quién entra?':
        'Who comes in?',
    'El ARNt no se une: la afinidad debe ser ≥ {n}.':
        "The tRNA doesn't bind: affinity must be ≥ {n}.",
    'Captura':
        'Capture',
    '{nombre} aprovechó para escapar.':
        '{nombre} took the chance to escape.',
    'Grupo R: {nombre}  {formula}  ({clase})':
        'R group: {nombre}  {formula}  ({clase})',
    '{i}) {nombre} [{tipo}] poder {poder}{contra}':
        '{i}) {nombre} [{tipo}] power {poder}{contra}',
    'Muy afín: +{n} de afinidad':
        'Strong affinity: +{n} affinity',
    '{nombre} se desordena un poco (−6 afinidad).':
        '{nombre} gets a bit disordered (−6 affinity).',
    'Más no polar (sin OH ni N–H)':
        'More nonpolar (no OH or N–H)',
    'Algo polar (tiene OH o N–H)':
        'Somewhat polar (has OH or N–H)',
    'energía {n}':
        'energy {n}',
    '{nombre} se escapó.':
        '{nombre} got away.',
    'Combate':
        'Battle',
    '{nombre} se desnaturalizó.':
        '{nombre} denatured.',
    'sin otra Cys no hay disulfuro':
        'no disulfide without another Cys',
    'sin puente de H (falta donador/aceptor)':
        'no H-bond (donor/acceptor missing)',
    'atracción ion–dipolo':
        'ion–dipole attraction',
    'el disulfuro solo se forma entre dos Cys':
        'a disulfide only forms between two Cys',
    '+{n} de afinidad':
        '+{n} affinity',
    'puente disulfuro (covalente)':
        'disulfide bridge (covalent)',
    '  (poco afín)':
        '  (weak affinity)',
    'No lograste escapar.':
        "You couldn't escape.",
    'Velocidad de animación: {vel}.':
        'Animation speed: {vel}.',
    'interacción del esqueleto / van der Waals':
        'backbone interaction / van der Waals',
    '[Enter] seguir':
        '[Enter] continue',
    'grupo R: ':
        'R group: ',
    'Modificación postraduccional de {nombre}…':
        'Post-translational modification of {nombre}…',
    'EQUIPO ({n})  ·  el primero (★ ) es el líder del combate':
        'TEAM ({n})  ·  the first one (★ ) leads in battle',
    'Objetos   {objetos}':
        'Items   {objetos}',
    '↑/↓ elegir  Enter hacer líder  O ordenar (A-Z/nivel/grupo)  V modificar  Esc salir':
        '↑/↓ select  Enter make leader  O sort (A-Z/level/group)  V modify  Esc exit',
    '{nombre} no tiene modificaciones disponibles en el juego (o ya está modificada).':
        '{nombre} has no modifications available in the game (or is already modified).',
    'Modificación':
        'Modification',
    '¿Qué modificación de {nombre}?':
        'Which modification of {nombre}?',
    'Interacciones: {movs}':
        'Interactions: {movs}',
    'orden: {orden}':
        'order: {orden}',
    'Pista: {pista}':
        'Hint: {pista}',
    'Grupo: {antes} → {despues}':
        'Group: {antes} → {despues}',
    'Nombre':
        'Name',
    'Nivel · XP':
        'Level · XP',
    '✓ lista':
        '✓ ready',
    'Modificable a':
        'Can become',
    'Requisitos:':
        'Requirements:',
    'Plegamiento {n}/{total}':
        'Folding {n}/{total}',
    'Lee este ARNm como un ribosoma: busca el primer AUG, lee de 3 en 3 y detente en el codón de paro (UAA, UAG o UGA). Escribe la proteína en código de 1 letra (incluye la Met inicial, no el paro).':
        'Read this mRNA like a ribosome: find the first AUG, read 3 by 3 and stop at the stop codon (UAA, UAG or UGA). Write the protein in 1-letter code (include the initial Met, not the stop).',
    'Necesito este péptido. Aquí está su ARNm, ya recortado: el marco empieza en la primera base. Tradúcelo de 3 en 3 hasta el codón de paro y escribe el péptido en código de 1 letra. Después lo sintetizo con los residuos de tu equipo.':
        "I need this peptide. Here's its mRNA, already trimmed: the frame starts at the first base. Translate it 3 by 3 up to the stop codon and write the peptide in 1-letter code. Then I'll synthesize it with your team's residues.",
    'Útiles y aún sin capturar: ':
        'Useful and not caught yet: ',
    'N-terminal ↓':
        'N-terminus ↓',
    'Reto superado: {reto}  ·  {seq}':
        'Challenge cleared: {reto}  ·  {seq}',
    'Recibes la insignia «{reto}», {n} {objeto} y +10 XP para todo tu equipo.':
        'You get the «{reto}» badge, {n} {objeto} and +10 XP for your whole team.',
    'Usa los aminoácidos de tu equipo, en código de 1 letra, del extremo N al C. Cada uno se puede usar tantas veces como lo tengas en el equipo (×n).':
        'Use the amino acids in your team, in 1-letter code, from the N to the C terminus. Each one can be used as many times as you have it in your team (×n).',
    'En tu equipo:':
        'In your team:',
    'Secuencia: N─':
        'Sequence: N─',
    'Largo {n}   GRAVY {gravy:+.2f}   Carga neta pH 7 {carga:+d}':
        'Length {n}   GRAVY {gravy:+.2f}   Net charge pH 7 {carga:+d}',
    'Chaperona':
        'Chaperone',
    '{n}/{total}. La proteína alcanzó su estado nativo: obtienes la Maestría en Aminoácidos.':
        "{n}/{total}. The protein reached its native state: you earn the Master's in Amino Acids.",
    'EXAMEN DEL RENÉ-VIRUS · {n}/{total} · Traducción':
        'RENÉ-VIRUS EXAM · {n}/{total} · Translation',
    'Proteína: ':
        'Protein: ',
    'Traducción':
        'Translation',
    'EXAMEN DEL RENÉ-VIRUS · {n}/{total} · Mutaciones reales':
        'RENÉ-VIRUS EXAM · {n}/{total} · Real mutations',
    'Pregunta':
        'Question',
    'Pulsa el número de tu respuesta':
        'Press the number of your answer',
    'Resultado':
        'Result',
    '{n}/8. Aprobado: Doctorado en Proteínas.':
        '{n}/8. Passed: PhD in Proteins.',
    'Encargos de síntesis ({n}/{total})':
        'Synthesis orders ({n}/{total})',
    'ENCARGO DEL RENÉ-VIRUS · {nombre}':
        'RENÉ-VIRUS ORDER · {nombre}',
    'Péptido: ':
        'Peptide: ',
    'Péptido sintetizado: {nombre}  ·  {seq}':
        'Peptide synthesized: {nombre}  ·  {seq}',
    '+5 XP para todo tu equipo y 1 ATP.':
        '+5 XP for your whole team and 1 ATP.',
    '+5 XP para todo tu equipo.':
        '+5 XP for your whole team.',
    ' ¡Completaste el catálogo de péptidos! Puedes repetir los encargos para seguir practicando la traducción.':
        ' You completed the peptide catalog! You can repeat orders to keep practicing translation.',
    'carga a pH 7.4: {a:+.2f}   →   a pH 5.0: {b:+.2f}':
        'charge at pH 7.4: {a:+.2f}   →   at pH 5.0: {b:+.2f}',
    'Reto: {reto}.':
        'Challenge: {reto}.',
    'Largo {n}   Carga pH 7.4 {a:+.2f}   Carga pH 5.0 {b:+.2f}':
        'Length {n}   Charge pH 7.4 {a:+.2f}   Charge pH 5.0 {b:+.2f}',
    'Letras: agregar  Retroceso: borrar  Enter: presentar  ? manual  Esc salir':
        'Letters: add  Backspace: delete  Enter: submit  ? manual  Esc exit',
    'Todavía no cumple todas las condiciones.':
        "It doesn't meet all the conditions yet.",
    'Examen de {total} preguntas. Cada respuesta correcta pliega una región de la proteína: con {nativo} queda completa en su estado nativo. Cada acierto de más le añade un extra que la estabiliza (un puente salino y un disulfuro) y te da 1 ATP.':
        "{total}-question exam. Each correct answer folds a region of the protein: with {nativo} it's complete in its native state. Each extra correct answer adds a bonus that stabilizes it (a salt bridge and a disulfide) and gives you 1 ATP.",
    'EXAMEN DE LA CHAPERONA · pregunta {i}/{total} · aciertos {n}':
        'CHAPERONE EXAM · question {i}/{total} · correct {n}',
    'Puedes seguir explorando. El siguiente nivel es el examen final; habla con el René-virus (V).':
        'You can keep exploring. The next level is the final exam; talk to the René-virus (V).',
    'Estado nativo':
        'Native state',
    '{n}/{total}. Quedaron regiones hidrofóbicas expuestas: la Hsp70 se une a ellas, gasta ATP y te deja intentar de nuevo. Repasa el manual y vuelve cuando quieras.':
        '{n}/{total}. Hydrophobic regions were left exposed: Hsp70 binds them, spends ATP and lets you try again. Review the manual and come back whenever you want.',
    "UTR 5' de {n} nt, luego: {lectura}":
        "5' UTR of {n} nt, then: {lectura}",
    'Traduce 3 ARNm y analiza 5 mutaciones asociadas a enfermedades humanas. Se aprueba con 7 de 8.':
        'Translate 3 mRNAs and analyze 5 mutations linked to human diseases. You pass with 7 out of 8.',
    '{n}/8. No aprobado. Repasa los codones (pestaña Chuleta) y las propiedades de cada grupo; las preguntas cambian en cada intento.':
        '{n}/8. Not passed. Review the codons (Cheat sheet tab) and the properties of each group; the questions change every attempt.',
    'Incorrecto. Era {seq}: {lectura}\n\nCada vez que lo pidas el ARNm usa codones distintos.':
        'Wrong. It was {seq}: {lectura}\n\nEach time you ask for it, the mRNA uses different codons.',
    '◆ quinasa':
        '◆ kinase',
    '▶ receptor':
        '▶ receptor',
    '◆ N-glic.':
        '◆ N-glyc.',
    '(ninguno)':
        '(none)',
    ' mal plegado':
        ' misfolded',
    'La Hsp70 asiste el plegamiento de las proteínas recién sintetizadas. Para presentar su examen necesitas las {n} insignias.\n\nPendientes: ':
        'Hsp70 assists the folding of newly synthesized proteins. To take its exam you need the {n} badges.\n\nPending: ',
    'Extra: {nombres}. Recibes {n} ATP.':
        'Extra: {nombres}. You get {n} ATP.',
    'Correcto. ':
        'Correct. ',
    'Incorrecto. Era {prot}. ':
        'Wrong. It was {prot}. ',
    'Ahora puedo hacerte encargos de síntesis: péptidos reales ({n} en el catálogo) que tendrás que traducir de su ARNm y construir con los residuos de tu equipo. Habla conmigo (V) cuando quieras. El catálogo está al final de la Aminodex [X].':
        "Now I can give you synthesis orders: real peptides ({n} in the catalog) that you'll have to translate from their mRNA and build with your team's residues. Talk to me (V) whenever you want. The catalog is at the end of the Aminodex [X].",
    'Captúralos y vuelve.':
        'Catch them and come back.',
    '▼ centro':
        '▼ center',
    'X (fuera)':
        'X (outside)',
    'Y (fuera)':
        'Y (outside)',
    'Incorrecto. Era: {r}.':
        'Wrong. It was: {r}.',
    'Al menos 6 residuos':
        'At least 6 residues',
    'Contiene S, T o Y':
        'Contains S, T or Y',
    'Entre 4 y 8 residuos':
        'Between 4 and 8 residues',
    'Carga neta ≥ +4':
        'Net charge ≥ +4',
    'Al menos 4 residuos':
        'At least 4 residues',
    'Termina en KDEL':
        'Ends in KDEL',
    '≥ 60% de Ser o Thr':
        '≥ 60% Ser or Thr',
    'Entre 3 y 8 residuos':
        'Between 3 and 8 residues',
    'Carga a pH 7.4 entre −1 y +1':
        'Charge at pH 7.4 between −1 and +1',
    'Carga a pH 5.0 ≥ +2':
        'Charge at pH 5.0 ≥ +2',
    'Al menos 9 residuos':
        'At least 9 residues',
    'Gly cada 3 residuos':
        'Gly every 3 residues',
    'Contiene Pro':
        'Contains Pro',
    '+ importina':
        '+ importin',
    'paro':
        'stop',
    "'{c}' no es el código de ningún aminoácido estándar.":
        "'{c}' is not the code of any standard amino acid.",
    'Traducción correcta, pero a tu equipo le faltan residuos para sintetizarlo:':
        'Correct translation, but your team is missing residues to synthesize it:',
    'No tienes {nombre} ({c}) en tu equipo. Búscalo en: {donde}.':
        "You don't have {nombre} ({c}) in your team. Look for it in: {donde}.",
    'Solo tienes {n} {nombre} ({c}) en tu equipo. Captura más en: {donde}.':
        'You only have {n} {nombre} ({c}) in your team. Catch more in: {donde}.',
    "'PVT TIM HaLL': Phe Val Thr Trp Ile Met His (Arg) Leu Lys. La A es Arg, que solo es esencial en neonatos (condicional).":
        "'PVT TIM HaLL' (Private Tim Hall): Phe Val Thr Trp Ile Met His (Arg) Leu Lys. The A is Arg, which is only essential in newborns (conditional).",
    '←/→ pestaña  ↑/↓ desplazar  1-9 ir  Esc cerrar':
        '←/→ tab  ↑/↓ scroll  1-9 go  Esc close',
    'Objetivo':
        'Goal',
    'Pantalla completa':
        'Full screen',
    'Controles en el mapa':
        'Map controls',
    'Símbolos del mapa':
        'Map symbols',
    'Jefes':
        'Bosses',
    'Después de la Chaperona':
        'After the Chaperone',
    'Después del examen final':
        'After the final exam',
    'Los 5 grupos de Lehninger':
        "Lehninger's 5 groups",
    '¿Por qué solo los aromáticos tienen dos tipos?':
        'Why do only the aromatic ones have two types?',
    'Resumen por grupo':
        'Summary by group',
    '¿Qué tan afín es cada tipo de movimiento con cada tipo?':
        'How strong is each type of move against each type?',
    'La química detrás (la tabla es simétrica)':
        'The chemistry behind it (the table is symmetric)',
    'Reglas químicas que el juego respeta':
        'Chemical rules the game follows',
    'Tipos dobles':
        'Dual types',
    'Interacciones por aminoácido':
        'Interactions by amino acid',
    '— (su R es un H)':
        '— (its R is an H)',
    'Qué hace cada clase de interacción':
        'What each class of interaction does',
    'Modificaciones postraduccionales':
        'Post-translational modifications',
    'Zonas de la célula':
        'Areas of the cell',
    '   (sin visitar)':
        '   (not visited)',
    'Clasificación nutricional en humanos':
        'Nutritional classification in humans',
    'Truco para los esenciales':
        'Trick for the essential ones',
    'Glosario':
        'Glossary',
    'Preguntas que pueden salir al lanzar el ARNt':
        'Questions that can come up when you throw the tRNA',
    '  1.ª: ¿qué aminoácido es?  2.ª: código de 3 letras  3.ª: código de 1 letra':
        '  1st: which amino acid is it?  2nd: 3-letter code  3rd: 1-letter code',
    '  Después: carga · grupo · pKR · pI · calcular el pI · nutrición ·':
        '  After that: charge · group · pKR · pI · calculate the pI · nutrition ·',
    '           codón · hidropatía':
        '              codon · hydropathy',
    'Tabla rápida (Lehninger, 25 °C)':
        'Quick table (Lehninger, 25 °C)',
    'Trucos':
        'Tricks',
    'Recorre la célula, encuentra a los 20 aminoácidos, captúralos y completa la Aminodex. Vence a los 7 jefes (J) y al final a la Chaperona (H).':
        'Travel through the cell, find the 20 amino acids, catch them and complete the Aminodex. Beat the 7 bosses (J) and, at the end, the Chaperone (H).',
    'El juego se adapta al tamaño de la terminal: en pantalla completa (F11 o Alt+Enter) ves toda la célula, el panel lateral con el minimapa y a tu aminoácido en combate.':
        'The game adapts to the size of the terminal: in full screen (F11 or Alt+Enter) you see the whole cell, the side panel with the minimap and your amino acid in battle.',
    'En las zonas marcadas con símbolos aparecen aminoácidos salvajes. Solo ves su estructura: deduce su grupo [D] para ganar +10 de afinidad y ver qué interacción formará cada movimiento. Si no, el grupo se revela tras 3 turnos.':
        'Wild amino acids appear in the areas marked with symbols. You only see their structure: deduce their group [D] to gain +10 affinity and see what interaction each move will form. Otherwise, the group is revealed after 3 turns.',
    'Cada movimiento es una interacción formada por tu grupo R (o por tu esqueleto) con el rival. Su nombre indica la clase de interacción y el grupo que la forma; la interacción concreta (puente salino, catión–π, repulsión…) depende del grupo del rival y se muestra a la derecha de cada movimiento. Si el rival tiene dos tipos, los factores se multiplican (×2 · ×2 = ×4).':
        "Each move is an interaction formed by your R group (or your backbone) with the rival. Its name tells you the class of interaction and the group that forms it; the specific interaction (salt bridge, cation–π, repulsion…) depends on the rival's group and is shown to the right of each move. If the rival has two types, the factors multiply (×2 · ×2 = ×4).",
    'Con afinidad ≥ 50 lanza un ARNt (T) y responde bien la pregunta. El rival responde con agitación térmica que baja tu ENERGÍA.':
        'With affinity ≥ 50 throw a tRNA (T) and answer the question correctly. The rival responds with thermal agitation that lowers your ENERGY.',
    'Las animaciones muestran los grupos químicos reales y un subtítulo con cada paso; cualquier tecla las salta.':
        'The animations show the real chemical groups and a subtitle for each step; any key skips them.',
    '1.ª vez: ¿cuál es? 2.ª: código de 3 letras. 3.ª: de 1 letra. Después: carga, grupo, pKR, pI (y calcularlo), nutrición, codones e hidropatía. Lo que fallas vuelve más seguido.':
        '1st time: which one is it? 2nd: 3-letter code. 3rd: 1-letter code. After that: charge, group, pKR, pI (and calculating it), nutrition, codons and hydropathy. What you get wrong comes back more often.',
    'Cada jefe pide construir un péptido con lo que ya capturaste; al lograrlo ves tu péptido dibujado. El poro nuclear es un jefe: necesitas una NLS con al menos 4 Lys (viven en los ribosomas ∴) para entrar al núcleo. La Arg solo vive adentro (núcleo y nucléolo). En cada reto puedes usar cada aminoácido tantas veces como lo tengas en tu equipo.':
        "Each boss asks you to build a peptide with what you've caught; when you succeed you see your peptide drawn. The nuclear pore is a boss: you need an NLS with at least 4 Lys (they live in the ribosomes ∴) to enter the nucleus. Arg only lives inside (nucleus and nucleolus). In each challenge you can use each amino acid as many times as you have it in your team.",
    'Habla con el René-virus (V): su examen final te pide traducir ARNm y analizar mutaciones reales (anemia falciforme, fibrosis quística, KRAS, Huntington…).':
        "Talk to the René-virus (V): its final exam asks you to translate mRNA and analyze real mutations (sickle cell anemia, cystic fibrosis, KRAS, Huntington's…).",
    'El René-virus te hace encargos de síntesis: péptidos reales (encefalinas, oxitocina, angiotensina II, sustancia P, Tat del VIH…). Traduces su ARNm y, si tu equipo tiene suficientes copias de cada residuo, se sintetiza y entra al catálogo de péptidos, al final de la Aminodex. Los largos piden varias Arg, Gly o Phe: sigue capturando.':
        'The René-virus gives you synthesis orders: real peptides (enkephalins, oxytocin, angiotensin II, substance P, HIV Tat…). You translate their mRNA and, if your team has enough copies of each residue, it gets synthesized and goes into the peptide catalog at the end of the Aminodex. The long ones need several Arg, Gly or Phe: keep catching.',
    'Cada aminoácido tiene un tipo (puro) o dos (doble). ✓ = ya lo capturaste.':
        "Each amino acid has one type (pure) or two (dual). ✓ = you've caught it.",
    'Los tipos del juego son exactamente los 5 grupos de Lehninger. Solo los aromáticos llevan un segundo tipo, y sale del mismo libro: «Phe, Tyr y Trp son relativamente no polares; Tyr y Trp son bastante más polares que Phe por el OH de Tyr y el N del indol de Trp».':
        "The game's types are exactly Lehninger's 5 groups. Only the aromatic ones carry a second type, and it comes from the same book: «Phe, Tyr and Trp are relatively nonpolar; Tyr and Trp are significantly more polar than Phe because of the OH of Tyr and the N of Trp's indole».",
    'Phe = Aromático / No polar.  Tyr = Aromático / Polar (O–H).  Trp = Aromático / Polar (N–H).':
        'Phe = Aromatic / Nonpolar.  Tyr = Aromatic / Polar (O–H).  Trp = Aromatic / Polar (N–H).',
    'Nota sobre His: Lehninger la clasifica como cargado +, aunque a pH 7 solo ~10% está protonada (pKR 6).':
        'Note on His: Lehninger classifies it as charged +, although at pH 7 only ~10% is protonated (pKR 6).',
    'Fila = tipo de TU movimiento. Columna = tipo del RIVAL.':
        'Row = type of YOUR move. Column = type of the RIVAL.',
    '• Un puente de H necesita un DONADOR (X–H) y un ACEPTOR (par libre). El N–H del Trp solo dona: con Lys, Arg o His (que también solo donan) no hay puente de H (×½).':
        "• An H-bond needs a DONOR (X–H) and an ACCEPTOR (lone pair). Trp's N–H only donates: with Lys, Arg or His (which also only donate) there's no H-bond (×½).",
    '• Cada aminoácido solo forma interacciones de su propio grupo R, más las del esqueleto peptídico y van der Waals, que todos tienen.':
        '• Each amino acid only forms interactions from its own R group, plus the peptide backbone and van der Waals ones, which everybody has.',
    '• El N⁺(CH₃)₃ de la trimetil-lisina no tiene H: con grupos polares solo hay atracción ion–dipolo, sin puente de H.':
        "• The N⁺(CH₃)₃ of trimethyl-lysine has no H: with polar groups there's only ion–dipole attraction, no H-bond.",
    '• La Pro (y la Hyp) no tiene H en el N del esqueleto: no forma el puente de H del esqueleto como donador.':
        "• Pro (and Hyp) has no H on its backbone N: it can't form the backbone H-bond as a donor.",
    '• El puente disulfuro solo existe entre dos Cys.':
        '• A disulfide bridge only exists between two Cys.',
    'Contra un rival de dos tipos se multiplican los factores. Con un movimiento No polar: Phe (Aromático/No polar) ×2·×2 = ×4, Tyr y Trp (Aromático/Polar) ×2·×½ = ×1: Phe es la más hidrofóbica de las tres.':
        'Against a rival with two types the factors multiply. With a Nonpolar move: Phe (Aromatic/Nonpolar) ×2·×2 = ×4, Tyr and Trp (Aromatic/Polar) ×2·×½ = ×1: Phe is the most hydrophobic of the three.',
    'Cada interacción se nombra por su clase y por el grupo R que la forma. Todos tienen además «Van der Waals» y, salvo la Pro, «Puente de H · esqueleto».':
        'Each interaction is named by its class and by the R group that forms it. Everyone also has «Van der Waals» and, except Pro, «H-bond · backbone».',
    'Grupo R':
        'R group',
    'Clase':
        'Class',
    'Interacciones de cadena lateral':
        'Side-chain interactions',
    'Se activan desde el menú Equipo [E] → V cuando se cumplen los requisitos. ✓ = ya la conseguiste.':
        "They're activated from the Team menu [E] → V when the requirements are met. ✓ = you've got it.",
    'otra Cys en el equipo (se fusionan)':
        'another Cys in the team (they fuse)',
    'Cambio: ':
        'Change: ',
    'Biología: ':
        'Biology: ',
    'Objetos: ':
        'Items: ',
    '• Códigos de 1 letra menos intuitivos: F=Fenilalanina, Y=tYrosina, W=Trp (doble anillo), N=asparagiNe, Q=Q-tamina, D=asparDate, E=glutEmate, K=antes de L, R=aRginina.':
        '• Least intuitive 1-letter codes: F=Fenylalanine (sounds like it), Y=tYrosine, W=Trp (tWo rings), N=asparagiNe, Q=Q-tamine, D=asparDic, E=glutEmic (one letter after D), K=before L, R=aRginine.',
    '• Cargas a pH 7: D E (−), K R (+), H ≈ neutra (+ a pH 5).':
        '• Charges at pH 7: D E (−), K R (+), H ≈ neutral (+ at pH 5).',
    '• pI: ácidos (pK1+pKR)/2, básicos (pK2+pKR)/2, el resto (pK1+pK2)/2. Asp 2.77 es el más bajo; Arg 10.76 el más alto.':
        '• pI: acidic (pK1+pKR)/2, basic (pK2+pKR)/2, the rest (pK1+pK2)/2. Asp 2.77 is the lowest; Arg 10.76 the highest.',
    'Puros: ':
        'Pure: ',
    'Dobles: ':
        'Dual: ',
    'Movimiento ↓ / Rival →':
        'Move ↓ / Rival →',
    '▶ Tu rival es ':
        '▶ Your rival is ',
    '  Mejores: ':
        '  Best: ',
    '  poder {n}':
        '  power {n}',
    '    Cómo: ':
        '    How: ',
    '    Tipos: ':
        '    Types: ',
    '    Interacciones: ':
        '    Interactions: ',
    'Tipos':
        'Types',
    'moverse':
        'move',
    'este manual':
        'this manual',
    'Aminodex':
        'Aminodex',
    'equipo: líder, orden y modificaciones':
        'team: leader, order and modifications',
    'guardar / guardar y salir':
        'save / save and quit',
    'membrana (colas)':
        'membrane (tails)',
    'interfase':
        'interface',
    'citosol':
        'cytosol',
    'ribosomas':
        'ribosomes',
    'retículo':
        'reticulum',
    'lisosoma':
        'lysosome',
    'cromatina':
        'chromatin',
    'nucléolo':
        'nucleolus',
    'colágeno':
        'collagen',
    'mitocondria':
        'mitochondrion',
    'poro nuclear':
        'nuclear pore',
    'envoltura':
        'envelope',
    'jefe':
        'boss',
    'cartel':
        'sign',
    'vitaminas C y K':
        'vitamins C and K',
    'interacciones':
        'interactions',
    'lanzar ARNt':
        'throw tRNA',
    'deducir el grupo':
        'deduce the group',
    'cambiar de aminoácido':
        'switch amino acid',
    'huir':
        'flee',
    'detalle de las interacciones':
        'interaction details',
    'velocidad de animación':
        'animation speed',
    'manual':
        'manual',
    '  Evita:   ':
        '  Avoid:   ',
    'efecto hidrofóbico':
        'hydrophobic effect',
    'el agua solvata al grupo polar':
        'water solvates the polar group',
    'catión–π':
        'cation–π',
    'la cara π repele al anión':
        'the π face repels the anion',
    'puentes de H':
        'H-bonds',
    'puente de H':
        'H-bond',
    'repulsión (el rival puede huir)':
        'repulsion (the rival may flee)',
    'esqueleto peptídico o van der Waals':
        'peptide backbone or van der Waals',
    '   Aparecen: ':
        '   Appear: ',
    '   (niveles {a}–{b})':
        '   (levels {a}–{b})',
    'Pareja':
        'Pair',
    'Interacción':
        'Interaction',
    'No polar + No polar / Aromático':
        'Nonpolar + Nonpolar / Aromatic',
    'No polar + Polar / cargado':
        'Nonpolar + Polar / charged',
    'Aromático + Aromático':
        'Aromatic + Aromatic',
    'Aromático + Cargado +':
        'Aromatic + Charged +',
    'Aromático + Cargado −':
        'Aromatic + Charged −',
    'Polar + Polar':
        'Polar + Polar',
    'Polar + cargado':
        'Polar + charged',
    'Cargado + + Cargado −':
        'Charged + + Charged −',
    'Misma carga':
        'Same charge',
    'Neutro + cualquiera':
        'Neutral + anything',
    'ninguno llega a ×2':
        'none reaches ×2',
    'Positiva (+1)':
        'Positive (+1)',
    'Negativa (−1)':
        'Negative (−1)',
    'Neutra':
        'Neutral',
    'Mayormente neutra (+ parcial)':
        'Mostly neutral (partial +)',
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
    '¿Qué aminoácido es este?':
        'Which amino acid is this?',
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
    '{nombre} sube al nivel {nivel}.':
        '{nombre} grows to level {nivel}.',
    'Nivel {req} (tiene {nivel})':
        'Level {req} (has {nivel})',
    '{nombre} ya puede modificarse (Equipo [E] → V).':
        '{nombre} can now be modified (Team [E] → V).',
    '1 {objeto} (tienes {n})':
        '1 {objeto} (you have {n})',
    'Estar en: {zona}':
        'Be in: {zona}',
    'Otra Cys en el equipo':
        'Another Cys in the team',
    'el agua los separa':
        'water keeps them apart',
    'repulsión anión–π':
        'anion–π repulsion',
    'puentes de hidrógeno':
        'hydrogen bonds',
    'repulsión (+ con +)':
        'repulsion (+ with +)',
    'repulsión (− con −)':
        'repulsion (− with −)',
    'Efecto hidrofóbico':
        'Hydrophobic effect',
    'Interacción π':
        'π interaction',
    'Puente de H':
        'H-bond',
    'Electrostática':
        'Electrostatic',
    'Junta su cadena no polar con la del rival y libera el agua ordenada que las rodeaba.':
        "Brings its nonpolar chain together with the rival's and releases the ordered water that surrounded them.",
    'Con no polares y aromáticos: efecto hidrofóbico. Con polares o cargados no funciona: el agua solvata a esos grupos.':
        "With nonpolar and aromatic ones: hydrophobic effect. With polar or charged ones it doesn't work: water solvates those groups.",
    'La nube π del anillo interactúa con el grupo del rival.':
        "The ring's π cloud interacts with the rival's group.",
    'Con otro anillo: apilamiento π–π. Con un catión: catión–π. Con un X–H: puente de H débil hacia la cara π. Con un anión: repulsión.':
        'With another ring: π–π stacking. With a cation: cation–π. With an X–H: weak H-bond toward the π face. With an anion: repulsion.',
    'Forma un puente de H: un H unido a O o N se comparte con un O o N del rival.':
        'Forms an H-bond: an H bonded to O or N is shared with an O or N of the rival.',
    'Necesita un donador (X–H) y un aceptor (par libre). Con no polares no hay con quién formarlo.':
        "Needs a donor (X–H) and an acceptor (lone pair). With nonpolar ones there's no partner to form it with.",
    'Su carga + interactúa electrostáticamente con el rival.':
        'Its + charge interacts electrostatically with the rival.',
    'Con un anión: puente salino. Con un anillo: catión–π. Con un grupo polar: puente de H. Con otra carga +: repulsión.':
        'With an anion: salt bridge. With a ring: cation–π. With a polar group: H-bond. With another + charge: repulsion.',
    'Su carga − interactúa electrostáticamente con el rival.':
        'Its − charge interacts electrostatically with the rival.',
    'Con un catión: puente salino. Con un grupo polar: puente de H. Con un anillo o con otra carga −: repulsión.':
        'With a cation: salt bridge. With a polar group: H-bond. With a ring or another − charge: repulsion.',
    'metilo':
        'methyl',
    'isopropilo':
        'isopropyl',
    'isobutilo':
        'isobutyl',
    'sec-butilo':
        'sec-butyl',
    'tioéter':
        'thioether',
    'pirrolidina':
        'pyrrolidine',
    'fenilo':
        'phenyl',
    'bencilo':
        'benzyl',
    'fenol':
        'phenol',
    'O–H fenólico':
        'phenolic O–H',
    'indol':
        'indole',
    'N–H del indol':
        'indole N–H',
    'hidroxilo':
        'hydroxyl',
    'tiol':
        'thiol',
    'carboxamida':
        'carboxamide',
    'carboxilato':
        'carboxylate',
    'ε-amonio':
        'ε-ammonium',
    'guanidinio':
        'guanidinium',
    'imidazolio':
        'imidazolium',
    'hidroxilo de la Hyp':
        'Hyp hydroxyl',
    'acetamida':
        'acetamide',
    'trimetilamonio':
        'trimethylammonium',
    'fosfato':
        'phosphate',
    'disulfuro':
        'disulfide',
    'dicarboxilato':
        'dicarboxylate',
    'glicano (O–H)':
        'glycan (O–H)',
    'O-glicano (O–H)':
        'O-glycan (O–H)',
    'ureido':
        'ureido',
    'hidrógeno':
        'hydrogen',
    'sin cadena lateral':
        'no side chain',
    'alquilo':
        'alkyl',
    'alquilo ramificado':
        'branched alkyl',
    'metiltioetilo':
        'methylthioethyl',
    '–CH₂CH₂CH₂– (cerrado sobre el N)':
        '–CH₂CH₂CH₂– (closed onto the N)',
    'amina secundaria cíclica':
        'cyclic secondary amine',
    'p-hidroxibencilo':
        'p-hydroxybenzyl',
    'indolilmetilo':
        'indolylmethyl',
    '–CH₂–indol':
        '–CH₂–indole',
    'hidroximetilo':
        'hydroxymethyl',
    'alcohol primario':
        'primary alcohol',
    '1-hidroxietilo':
        '1-hydroxyethyl',
    'alcohol secundario':
        'secondary alcohol',
    'sulfanilmetilo':
        'sulfanylmethyl',
    'carbamoilmetilo':
        'carbamoylmethyl',
    'amida':
        'amide',
    '2-carbamoiletilo':
        '2-carbamoylethyl',
    'carboximetilo':
        'carboxymethyl',
    '2-carboxietilo':
        '2-carboxyethyl',
    '4-aminobutilo':
        '4-aminobutyl',
    'amonio primario':
        'primary ammonium',
    '3-guanidinopropilo':
        '3-guanidinopropyl',
    'imidazolilmetilo':
        'imidazolylmethyl',
    '–CH₂–imidazol':
        '–CH₂–imidazole',
    'imidazol':
        'imidazole',
    'Van der Waals':
        'Van der Waals',
    'Fuerzas de London entre átomos en contacto: débiles, pero existen con cualquier grupo (×1).':
        'London forces between atoms in contact: weak, but they exist with any group (×1).',
    'Un dipolo instantáneo induce otro en el átomo vecino.':
        'An instantaneous dipole induces another in the neighboring atom.',
    'Puente de H · esqueleto':
        'H-bond · backbone',
    'El N–H de su enlace peptídico se une al C=O del esqueleto del rival (×1 con todos).':
        "The N–H of its peptide bond binds the C=O of the rival's backbone (×1 with everyone).",
    'Así se aparean las hebras de una lámina β. La Pro no puede: su N no tiene H. La Gly, sin cadena lateral, se acerca más.':
        "This is how the strands of a β sheet pair up. Pro can't: its N has no H. Gly, with no side chain, gets closer.",
    'Puente disulfuro':
        'Disulfide bridge',
    'Enlace covalente S–S. Solo se forma con otra Cys: afinidad máxima. Con cualquier otro residuo no ocurre.':
        "Covalent S–S bond. It only forms with another Cys: maximum affinity. With any other residue it doesn't happen.",
    '2 R–SH → R–S–S–R + 2H⁺ + 2e⁻ (oxidación).':
        '2 R–SH → R–S–S–R + 2H⁺ + 2e⁻ (oxidation).',
    'No polar alifático':
        'Nonpolar aliphatic',
    'No polar':
        'Nonpolar',
    'Cadena de C e H (Gly, Ala, Pro, Val, Leu, Ile, Met). No forma puentes de H con el agua: se agrupa con otras cadenas no polares por el efecto hidrofóbico.':
        "Chain of C and H (Gly, Ala, Pro, Val, Leu, Ile, Met). It doesn't form H-bonds with water: it clusters with other nonpolar chains through the hydrophobic effect.",
    'Aromático':
        'Aromatic',
    'Aromát.':
        'Aromat.',
    'Anillo aromático (Phe, Tyr, Trp) con electrones π: se apila con otros anillos (π–π) y atrae cationes por su cara (catión–π). Son relativamente no polares; Tyr y Trp, menos que Phe.':
        "Aromatic ring (Phe, Tyr, Trp) with π electrons: it stacks with other rings (π–π) and attracts cations to its face (cation–π). They're relatively nonpolar; Tyr and Trp less so than Phe.",
    'Polar sin carga':
        'Polar uncharged',
    'Polar':
        'Polar',
    'OH, SH o amida (Ser, Thr, Cys, Asn, Gln) que forman puentes de H con el agua y con otros grupos polares, sin carga neta a pH 7.':
        'OH, SH or amide (Ser, Thr, Cys, Asn, Gln) that form H-bonds with water and with other polar groups, with no net charge at pH 7.',
    'Cargado + (básico)':
        'Charged + (basic)',
    'Básico+':
        'Basic+',
    'Lys (amonio), Arg (guanidinio) e His (imidazol). Lys y Arg tienen carga +1 a pH 7; His solo a pH ácido (pKR 6), pero Lehninger la pone en este grupo.':
        'Lys (ammonium), Arg (guanidinium) and His (imidazole). Lys and Arg have a +1 charge at pH 7; His only at acidic pH (pKR 6), but Lehninger puts it in this group.',
    'Cargado − (ácido)':
        'Charged − (acidic)',
    'Ácido−':
        'Acidic−',
    'Asp y Glu: carboxilato (COO−) con pKR ~4, así que a pH 7 ya perdieron su H+ y tienen carga −1.':
        "Asp and Glu: carboxylate (COO−) with pKR ~4, so at pH 7 they've already lost their H+ and have a −1 charge.",
    'Ácido (carga −)':
        'Acidic (− charge)',
    'Básico (carga +)':
        'Basic (+ charge)',
    'Esencial':
        'Essential',
    'No la sintetizamos (o no lo bastante rápido): debe venir de la dieta.':
        "We don't synthesize it (or not fast enough): it must come from the diet.",
    'Condicional':
        'Conditional',
    'Normalmente se sintetiza, pero en prematuridad, estrés metabólico, enfermedad o crecimiento rápido la síntesis no alcanza.':
        "It's normally synthesized, but in prematurity, metabolic stress, illness or rapid growth, synthesis falls short.",
    'No esencial':
        'Nonessential',
    'La sintetizamos en cantidad suficiente.':
        'We synthesize enough of it.',
    'Glicina':
        'Glycine',
    'La más pequeña y la única sin carbono quiral (su R es un H). Es 1 de cada 3 residuos del colágeno.':
        "The smallest and the only one without a chiral carbon (its R is an H). It's 1 of every 3 residues in collagen.",
    'Alanina':
        'Alanine',
    'Un simple metilo. Es la mejor formadora de hélices α y viaja del músculo al hígado en el ciclo glucosa-alanina.':
        "A simple methyl. It's the best α-helix former and travels from muscle to liver in the glucose-alanine cycle.",
    'Valina':
        'Valine',
    "Ramificada en β (forma de 'V'). Aminoácido de cadena ramificada (BCAA) como Leu e Ile.":
        "Branched at β ('V' shape). A branched-chain amino acid (BCAA) like Leu and Ile.",
    'Leucina':
        'Leucine',
    'Isobutilo. Forma cremalleras de leucina en factores de transcripción como Fos y Jun.':
        'Isobutyl. It forms leucine zippers in transcription factors such as Fos and Jun.',
    'Isoleucina':
        'Isoleucine',
    'La más hidrofóbica (KD 4.5). Tiene dos carbonos quirales (Cα y Cβ). Isómero de Leu.':
        'The most hydrophobic (KD 4.5). It has two chiral carbons (Cα and Cβ). Isomer of Leu.',
    'Metionina':
        'Methionine',
    'Tioéter (S sin H). AUG es el codón de inicio: toda proteína empieza con Met. Da origen a la SAM, el donador de metilos.':
        'Thioether (S without H). AUG is the start codon: every protein starts with Met. It gives rise to SAM, the methyl donor.',
    'Prolina':
        'Proline',
    'Su α-amino es secundario: la cadena lateral se cierra sobre el N. Ese anillo rígido rompe hélices α y forma giros. Su pK2 (10.96) es el más alto de todos.':
        'Its α-amino is secondary: the side chain closes back onto the N. That rigid ring breaks α helices and forms turns. Its pK2 (10.96) is the highest of all.',
    'Fenilalanina':
        'Phenylalanine',
    'Bencilo. La fenilalanina hidroxilasa la convierte en Tyr; si falla esa enzima → fenilcetonuria (PKU).':
        'Benzyl. Phenylalanine hydroxylase converts it into Tyr; if that enzyme fails → phenylketonuria (PKU).',
    'Tirosina':
        'Tyrosine',
    'Phe + OH (fenol). Absorbe a 280 nm. Precursora de dopamina, adrenalina, melanina y hormonas tiroideas.':
        'Phe + OH (phenol). Absorbs at 280 nm. Precursor of dopamine, adrenaline, melanin and thyroid hormones.',
    'Triptófano':
        'Tryptophan',
    'Indol (anillo doble con N). El más grande y el que más absorbe a 280 nm. Precursor de serotonina y melatonina.':
        'Indole (double ring with N). The largest one and the strongest absorber at 280 nm. Precursor of serotonin and melatonin.',
    'Serina':
        'Serine',
    'Hidroximetilo. Nucleófilo de las serín-proteasas (tripsina, quimotripsina). Blanco clásico de quinasas.':
        'Hydroxymethyl. The nucleophile of serine proteases (trypsin, chymotrypsin). A classic kinase target.',
    'Treonina':
        'Threonine',
    'Como Ser pero con un CH3 extra; también tiene dos carbonos quirales. Se fosforila igual que Ser.':
        "Like Ser but with an extra CH3; it also has two chiral carbons. It's phosphorylated just like Ser.",
    'Cisteína':
        'Cysteine',
    'Tiol (SH). Dos Cys se oxidan y forman un puente disulfuro (cistina). Lehninger la clasifica como polar sin carga, aunque su KD (+2.5) indica que es bastante hidrofóbica.':
        "Thiol (SH). Two Cys oxidize and form a disulfide bridge (cystine). Lehninger classifies it as polar uncharged, although its KD (+2.5) shows it's quite hydrophobic.",
    'Asparagina':
        'Asparagine',
    'Amida de Asp. Primer aminoácido aislado (de los espárragos). Sitio de N-glicosilación (secuón N-X-S/T).':
        'Amide of Asp. The first amino acid ever isolated (from asparagus). N-glycosylation site (sequon N-X-S/T).',
    'Glutamina':
        'Glutamine',
    'Amida de Glu. El aminoácido más abundante en sangre: transporta nitrógeno (NH3) de forma no tóxica.':
        'Amide of Glu. The most abundant amino acid in blood: it carries nitrogen (NH3) in a non-toxic form.',
    'Aspartato':
        'Aspartate',
    'Carboxilato a pH 7. El pI más bajo de todos (2.77). Dona N al ciclo de la urea y forma parte de la tríada catalítica (Ser-His-Asp).':
        'Carboxylate at pH 7. The lowest pI of all (2.77). It donates N to the urea cycle and is part of the catalytic triad (Ser-His-Asp).',
    'Glutamato':
        'Glutamate',
    "Un CH2 más que Asp. Principal neurotransmisor excitador y sabor 'umami'. Centro del metabolismo del nitrógeno; precursor de Gln y Pro.":
        "One CH2 more than Asp. The main excitatory neurotransmitter and the 'umami' taste. Hub of nitrogen metabolism; precursor of Gln and Pro.",
    'Lisina':
        'Lysine',
    'Cadena de 4 CH2 con amonio. Abunda en histonas y proteínas ribosomales; se acetila, metila y ubiquitina.':
        'Chain of 4 CH2 with an ammonium. Abundant in histones and ribosomal proteins; it gets acetylated, methylated and ubiquitinated.',
    'Arginina':
        'Arginine',
    'Guanidinio: la base más fuerte (pKR 12.5), siempre +. El pI más alto (10.76) y la más hidrofílica (KD −4.5). Origen del óxido nítrico (NO).':
        'Guanidinium: the strongest base (pKR 12.5), always +. The highest pI (10.76) and the most hydrophilic (KD −4.5). Source of nitric oxide (NO).',
    'Histidina':
        'Histidine',
    'Imidazol con pKR ≈ 6: a pH 7 solo ~10% está protonada, a pH 5 casi toda. Por eso cede o toma H+ en sitios activos y en la hemoglobina.':
        "Imidazole with pKR ≈ 6: at pH 7 only ~10% is protonated, at pH 5 almost all of it. That's why it gives or takes H+ in active sites and in hemoglobin.",
    'No polar no es lo mismo que hidrofóbico. La Gly es no polar porque su R es un H, pero ese H no tiene superficie que esconder del agua: el efecto hidrofóbico crece con la superficie de C–H que se entierra. Sin cadena lateral pesa más su esqueleto polar (N–H y C=O), por eso KD ≈ 0 (−0.4). Lehninger: es formalmente no polar, pero su cadena tan pequeña no contribuye de verdad a las interacciones hidrofóbicas.':
        "Nonpolar is not the same as hydrophobic. Gly is nonpolar because its R is an H, but that H has no surface to hide from water: the hydrophobic effect grows with the C–H surface that gets buried. With no side chain, its polar backbone (N–H and C=O) weighs more, so KD ≈ 0 (−0.4). Lehninger: it's formally nonpolar, but its tiny side chain doesn't really contribute to hydrophobic interactions.",
    'Su anillo es de C–H, pero KD −1.6: rompe hélices y suele quedar en giros y lazos expuestos al agua, en la superficie de la proteína.':
        'Its ring is made of C–H, but KD −1.6: it breaks helices and usually sits in turns and loops exposed to water, on the protein surface.',
    'Es polar sin carga por el S–H, pero el S casi no es más electronegativo que el C (2.58 frente a 2.55): el S–H es muy poco polar y forma puentes de H débiles. Además suele estar enterrada en las proteínas (sola o en disulfuros), así que su KD es +2.5. Otros libros la ponen con los hidrofóbicos.':
        "It's polar uncharged because of the S–H, but S is barely more electronegative than C (2.58 vs 2.55): the S–H is only weakly polar and forms weak H-bonds. It's also usually buried inside proteins (alone or in disulfides), so its KD is +2.5. Other textbooks put it with the hydrophobic ones.",
    'Su anillo es poco polar, pero el O–H del fenol forma puentes de H con el agua: KD −1.3, mucho menos hidrofóbica que la Phe (+2.8).':
        'Its ring is not very polar, but the phenol O–H forms H-bonds with water: KD −1.3, much less hydrophobic than Phe (+2.8).',
    'El indol es grande y poco polar, pero su N–H forma puentes de H y suele quedar en la interfase membrana-agua: KD −0.9.':
        'The indole is large and not very polar, but its N–H forms H-bonds and it tends to sit at the membrane-water interface: KD −0.9.',
    'Hidroxiprolina':
        'Hydroxyproline',
    'Gana un OH en el anillo: de No polar a Polar sin carga.':
        'Gains an OH on the ring: from Nonpolar to Polar uncharged.',
    'La prolil 4-hidroxilasa (en el RE) le pone un OH usando vitamina C (ascorbato) como cofactor. La Hyp estabiliza la triple hélice del colágeno; sin vitamina C el colágeno se deshace → escorbuto.':
        'Prolyl 4-hydroxylase (in the ER) adds an OH using vitamin C (ascorbate) as a cofactor. Hyp stabilizes the collagen triple helix; without vitamin C collagen falls apart → scurvy.',
    'Hay vitamina C en la matriz extracelular (C en el mapa).':
        "There's vitamin C in the extracellular matrix (C on the map).",
    'Hidroxilisina':
        'Hydroxylysine',
    'Conserva la carga + (sigue en el grupo básico) y gana un OH en el carbono δ.':
        'Keeps its + charge (stays in the basic group) and gains an OH on the δ carbon.',
    'La lisil hidroxilasa (también dependiente de vitamina C) la forma en el RE. Sus OH reciben azúcares y crean entrecruzamientos que dan resistencia a las fibras de colágeno.':
        'Lysyl hydroxylase (also vitamin C-dependent) makes it in the ER. Its OH groups receive sugars and form cross-links that make collagen fibers strong.',
    'Acetil-lisina':
        'Acetyl-lysine',
    'Pierde la carga +: el amonio se vuelve una amida neutra. De Cargado + a Polar sin carga.':
        'Loses its + charge: the ammonium becomes a neutral amide. From Charged + to Polar uncharged.',
    'Las acetiltransferasas de histonas (HAT) le pasan un acetilo del acetil-CoA. Sin carga +, la histona suelta al ADN (−): la cromatina se abre y los genes se expresan. Las HDAC lo revierten.':
        'Histone acetyltransferases (HATs) transfer an acetyl from acetyl-CoA. Without the + charge, the histone lets go of the DNA (−): chromatin opens up and genes are expressed. HDACs reverse it.',
    'Las HAT actúan en el núcleo; entra por un poro.':
        'HATs act in the nucleus; enter through a pore.',
    'Trimetil-lisina':
        'Trimethyl-lysine',
    'Positiva (+1, permanente)':
        'Positive (+1, permanent)',
    'Sigue siendo + (amonio cuaternario: ya no puede perder la carga ni acetilarse, porque su N no tiene H).':
        'Still + (quaternary ammonium: it can no longer lose its charge or be acetylated, because its N has no H).',
    'Las metiltransferasas de histonas (HMT) usan SAM, derivada de la Met. H3K4me3 marca genes activos; H3K9me3 y H3K27me3, genes silenciados. No cambia la carga, cambia quién se une.':
        "Histone methyltransferases (HMTs) use SAM, derived from Met. H3K4me3 marks active genes; H3K9me3 and H3K27me3, silenced genes. It doesn't change the charge, it changes who binds.",
    'Las HMT actúan en el núcleo.':
        'HMTs act in the nucleus.',
    'Fosfoserina':
        'Phosphoserine',
    'Negativa (≈ −2)':
        'Negative (≈ −2)',
    'Gana un fosfato: de Polar sin carga a Cargado − (≈ −2).':
        'Gains a phosphate: from Polar uncharged to Charged − (≈ −2).',
    'Las Ser/Thr quinasas (PKA, PKC, MAPK…) le transfieren el fosfato γ del ATP. Es el interruptor más común de la célula; las fosfatasas lo quitan.':
        "Ser/Thr kinases (PKA, PKC, MAPK…) transfer ATP's γ phosphate to it. It's the most common switch in the cell; phosphatases remove it.",
    'La mitocondria (◉) recarga ATP.':
        'The mitochondrion (◉) recharges ATP.',
    'Fosfotreonina':
        'Phosphothreonine',
    'Mismas Ser/Thr quinasas que la serina. El motivo pThr-Pro lo reconoce la isomerasa Pin1 y controla el ciclo celular (CDKs).':
        'Same Ser/Thr kinases as serine. The pThr-Pro motif is recognized by the isomerase Pin1 and controls the cell cycle (CDKs).',
    'Fosfotirosina':
        'Phosphotyrosine',
    'El OH del fenol se fosforila: conserva el anillo, pero ahora tiene carga ≈ −2 (Cargado − / Aromático).':
        'The phenol OH gets phosphorylated: it keeps the ring, but now has a ≈ −2 charge (Charged − / Aromatic).',
    'Las tirosina quinasas (como el receptor de insulina, un RTK) la generan. Los dominios SH2 la reconocen con una Arg que forma un puente salino con el fosfato, y así propagan la señal.':
        "Tyrosine kinases (like the insulin receptor, an RTK) produce it. SH2 domains recognize it with an Arg that forms a salt bridge with the phosphate, and that's how they pass the signal on.",
    'Cistina':
        'Cystine',
    'Dos Cys se unen por un enlace S–S covalente y pierden los SH. Lehninger: los residuos unidos por disulfuro son fuertemente hidrofóbicos (no polares).':
        'Two Cys join through a covalent S–S bond and lose their SH. Lehninger: residues linked by a disulfide are strongly hydrophobic (nonpolar).',
    'En el RE (ambiente oxidante) la PDI, proteína disulfuro isomerasa, forma y reacomoda puentes S–S. Estabilizan proteínas que salen de la célula: insulina, anticuerpos, queratina.':
        'In the ER (an oxidizing environment) PDI, protein disulfide isomerase, forms and rearranges S–S bridges. They stabilize proteins that leave the cell: insulin, antibodies, keratin.',
    'El RE es oxidante; lleva otra Cys en el equipo.':
        'The ER is oxidizing; bring another Cys in your team.',
    'γ-carboxiglutamato':
        'γ-carboxyglutamate',
    'Gana un segundo carboxilo en el carbono γ: carga ≈ −2.':
        'Gains a second carboxyl on the γ carbon: charge ≈ −2.',
    'La γ-glutamil carboxilasa (en el RE) usa vitamina K. Los Gla de la protrombina y los factores VII, IX y X atrapan Ca²⁺ y anclan los factores a la membrana: sin vit. K no hay coagulación (la warfarina bloquea este ciclo).':
        "γ-glutamyl carboxylase (in the ER) uses vitamin K. The Gla residues of prothrombin and factors VII, IX and X trap Ca²⁺ and anchor the factors to the membrane: without vit. K there's no clotting (warfarin blocks this cycle).",
    'Hay vitamina K en el retículo (K en el mapa).':
        "There's vitamin K in the reticulum (K on the map).",
    'Asn N-glicosilada':
        'N-glycosyl Asn',
    'Se le une un árbol de azúcares al N de la amida: aún más polar.':
        'A tree of sugars attaches to the amide N: even more polar.',
    'La oligosacariltransferasa (OST) del RE la añade en el secuón N-X-S/T (X ≠ Pro). Los glicanos ayudan al plegamiento (ciclo calnexina/calreticulina) y al control de calidad.':
        "The ER's oligosaccharyltransferase (OST) adds it at the sequon N-X-S/T (X ≠ Pro). Glycans help folding (calnexin/calreticulin cycle) and quality control.",
    'La OST trabaja en el retículo endoplásmico.':
        'OST works in the endoplasmic reticulum.',
    'Ser O-glicosilada':
        'O-glycosyl Ser',
    'Se le une una N-acetilgalactosamina (GalNAc) al O del OH: sigue siendo polar, pero ahora carga un azúcar.':
        "An N-acetylgalactosamine (GalNAc) attaches to the O of the OH: it's still polar, but now carries a sugar.",
    'Las GalNAc-transferasas (GALNT) del Golgi le ponen la GalNAc y luego se alarga a un O-glicano tipo mucina. A diferencia de la N-glicosilación de la Asn (en el RE, sobre el secuón N-X-S/T), no tiene secuencia consenso y empieza en el Golgi. La GalNAc sola es el antígeno Tn, que aparece en muchos tumores.':
        "The Golgi's GalNAc-transferases (GALNTs) add the GalNAc, which is then extended into a mucin-type O-glycan. Unlike Asn N-glycosylation (in the ER, on the N-X-S/T sequon), it has no consensus sequence and starts in the Golgi. GalNAc alone is the Tn antigen, which shows up in many tumors.",
    'Las GALNT trabajan en el aparato de Golgi.':
        'GALNTs work in the Golgi apparatus.',
    'Thr O-glicosilada':
        'O-glycosyl Thr',
    'Se le une una GalNAc al O del OH: sigue siendo polar, pero ahora carga un azúcar.':
        "A GalNAc attaches to the O of the OH: it's still polar, but now carries a sugar.",
    'Mismas GalNAc-transferasas del Golgi; muchas prefieren Thr. En las mucinas, los tramos ricos en Pro, Thr y Ser (PTS) quedan cubiertos de O-glicanos que atrapan agua: así se forma el moco.':
        "Same Golgi GalNAc-transferases; many prefer Thr. In mucins, stretches rich in Pro, Thr and Ser (PTS) get covered with O-glycans that trap water: that's how mucus forms.",
    'Citrulina':
        'Citrulline',
    'Pierde la carga +: el guanidinio se vuelve una urea neutra (de Cargado + a Polar sin carga).':
        'Loses its + charge: the guanidinium becomes a neutral urea (from Charged + to Polar uncharged).',
    'Las PAD (peptidil-arginina deiminasas, dependientes de Ca²⁺) la generan. PAD4 citrulina histonas en las trampas de neutrófilos (NETs). En la artritis reumatoide aparecen anticuerpos anti-CCP. La citrulina libre también es parte del ciclo de la urea.':
        'PADs (peptidyl-arginine deiminases, Ca²⁺-dependent) produce it. PAD4 citrullinates histones in neutrophil extracellular traps (NETs). In rheumatoid arthritis, anti-CCP antibodies appear. Free citrulline is also part of the urea cycle.',
    'Solo requiere nivel.':
        'Only requires level.',
    'Donador de fosfato para las quinasas. Lo da la mitocondria.':
        'Phosphate donor for kinases. The mitochondrion provides it.',
    'Cofactor de las hidroxilasas de Pro y Lys (colágeno).':
        'Cofactor of the Pro and Lys hydroxylases (collagen).',
    'Cofactor de la γ-glutamil carboxilasa (coagulación).':
        'Cofactor of γ-glutamyl carboxylase (clotting).',
    'Membrana (colas lipídicas)':
        'Membrane (lipid tails)',
    'Aquí viven los no polares (y Phe): las hélices transmembrana esconden sus cadenas entre las colas de ácidos grasos, lejos del agua.':
        'The nonpolar ones (and Phe) live here: transmembrane helices hide their side chains among the fatty acid tails, away from water.',
    'Interfase de la membrana':
        'Membrane interface',
    'Cinturón aromático: Trp y Tyr se colocan justo donde las cabezas polares de los lípidos tocan el agua. Su anillo es poco polar, pero su N–H u O–H forma puentes de H con las cabezas.':
        'Aromatic belt: Trp and Tyr sit right where the polar lipid heads meet the water. Their ring is not very polar, but their N–H or O–H forms H-bonds with the heads.',
    'Citosol':
        'Cytosol',
    'Aquí viven los polares: en la superficie de las proteínas solubles forman puentes de H con el agua.':
        'The polar ones live here: on the surface of soluble proteins they form H-bonds with water.',
    'Ribosomas':
        'Ribosomes',
    'Ribosomas libres traduciendo ARNm en el citosol. Sus proteínas ribosomales son muy ricas en Lys: sus cargas + neutralizan los fosfatos (−) del ARN ribosomal. Aquí consigues las Lys para tu NLS; la Arg solo vive dentro del núcleo.':
        'Free ribosomes translating mRNA in the cytosol. Their ribosomal proteins are very rich in Lys: their + charges neutralize the (−) phosphates of ribosomal RNA. Here you get the Lys for your NLS; Arg only lives inside the nucleus.',
    'Núcleo (cromatina)':
        'Nucleus (chromatin)',
    'Las histonas son ricas en Lys y Arg y abrazan al ADN, cargado (−) por sus fosfatos; H3 y H4 son las histonas «ricas en Arg». La Arg solo aparece aquí y en el nucléolo. Para entrar, tu proteína necesita una señal de localización nuclear (NLS).':
        'Histones are rich in Lys and Arg and wrap around DNA, which is (−) because of its phosphates; H3 and H4 are the «Arg-rich» histones. Arg only appears here and in the nucleolus. To get in, your protein needs a nuclear localization signal (NLS).',
    'Nucléolo':
        'Nucleolus',
    'Aquí se ensamblan los ribosomas. La nucleolina y la fibrilarina tienen dominios RGG/GAR (repeticiones Arg-Gly-Gly) que se unen al ARN.':
        'Ribosomes are assembled here. Nucleolin and fibrillarin have RGG/GAR domains (Arg-Gly-Gly repeats) that bind RNA.',
    'Retículo endoplásmico':
        'Endoplasmic reticulum',
    'Aquí viven los ácidos (−): el RE es el almacén de Ca²⁺ de la célula y proteínas como la calreticulina están llenas de Asp y Glu para retenerlo. Su membrana es continua con la envoltura nuclear.':
        "The acidic ones (−) live here: the ER is the cell's Ca²⁺ store, and proteins like calreticulin are full of Asp and Glu to hold onto it. Its membrane is continuous with the nuclear envelope.",
    'Aparato de Golgi':
        'Golgi apparatus',
    'Aquí se recortan y amplían los N-glicanos que la Asn trae del RE, y se añaden O-glicanos (O-GalNAc) al OH de Ser y Thr.':
        'Here the N-glycans that Asn brings from the ER are trimmed and extended, and O-glycans (O-GalNAc) are added to the OH of Ser and Thr.',
    'Lisosoma':
        'Lysosome',
    'pH ≈ 4.5–5: la His (pKR 6) queda protonada (+). Las catepsinas B y L son cisteín-proteasas: su Cys catalítica trabaja junto con una His (díada catalítica).':
        'pH ≈ 4.5–5: His (pKR 6) stays protonated (+). Cathepsins B and L are cysteine proteases: their catalytic Cys works together with a His (catalytic dyad).',
    'Matriz extracelular':
        'Extracellular matrix',
    'Aquí viven Gly y Pro: el colágeno repite Gly-Pro-Hyp. La Gly es la única que cabe en el centro de la triple hélice y la Pro la rigidiza.':
        'Gly and Pro live here: collagen repeats Gly-Pro-Hyp. Gly is the only one that fits in the center of the triple helix, and Pro stiffens it.',
    'Mitocondria':
        'Mitochondrion',
    'La fosforilación oxidativa produce ATP: aquí tu equipo restablece su energía y recargas ATP. También es donde se degradan los aminoácidos ramificados (Val, Leu, Ile).':
        "Oxidative phosphorylation makes ATP: here your team restores its energy and you recharge ATP. It's also where the branched-chain amino acids (Val, Leu, Ile) are broken down.",
    'pH fisiológico':
        'Physiological pH',
    'Sangre ≈ 7.4, citosol ≈ 7.2, lisosoma ≈ 4.5–5.':
        'Blood ≈ 7.4, cytosol ≈ 7.2, lysosome ≈ 4.5–5.',
    'pH al que un grupo está 50% protonado. Si pH < pKa el grupo está mayormente protonado; si pH > pKa, desprotonado.':
        'The pH at which a group is 50% protonated. If pH < pKa the group is mostly protonated; if pH > pKa, deprotonated.',
    'pK1 = α-COOH (~2), pK2 = α-NH3+ (~9–10), pKR = cadena lateral (solo D, E, H, C, Y, K, R).':
        'pK1 = α-COOH (~2), pK2 = α-NH3+ (~9–10), pKR = side chain (only D, E, H, C, Y, K, R).',
    'pI (punto isoeléctrico)':
        'pI (isoelectric point)',
    'pH al que la carga neta es 0. Se calcula promediando los dos pKa que flanquean la especie neutra: ácidos → (pK1 + pKR)/2; básicos → (pK2 + pKR)/2; sin cadena ionizable → (pK1 + pK2)/2.':
        "The pH at which the net charge is 0. It's calculated by averaging the two pKa values that flank the neutral species: acidic → (pK1 + pKR)/2; basic → (pK2 + pKR)/2; no ionizable side chain → (pK1 + pK2)/2.",
    'Carga a pH 7':
        'Charge at pH 7',
    'Asp y Glu (pKR ~4) ya perdieron su H+: son −. Lys y Arg (pKR >10) aún lo tienen: son +. His (pKR 6) está casi siempre neutra.':
        "Asp and Glu (pKR ~4) have already lost their H+: they're −. Lys and Arg (pKR >10) still have it: they're +. His (pKR 6) is almost always neutral.",
    'pKR en proteínas':
        'pKR in proteins',
    'Los pKR de la tabla son del aminoácido libre. Dentro de una proteína cambian según el microambiente (una His o Cys de sitio activo puede moverse varias unidades). Para docking o asignar protonación se usa PROPKA.':
        'The pKR values in the table are for the free amino acid. Inside a protein they shift with the microenvironment (an active-site His or Cys can move several units). For docking or assigning protonation states, PROPKA is used.',
    'Hidropatía (KD)':
        'Hydropathy (KD)',
    'Escala de Kyte-Doolittle: positivo = hidrofóbico (Ile 4.5), negativo = hidrofílico (Arg −4.5).':
        'Kyte-Doolittle scale: positive = hydrophobic (Ile 4.5), negative = hydrophilic (Arg −4.5).',
    'No polar ≠ hidrofóbico':
        'Nonpolar ≠ hydrophobic',
    'No polar habla de la química del grupo R (sin O–H ni N–H, no forma puentes de H). Hidrofóbico habla de cuánto le conviene esconderse del agua, y eso depende de su superficie de C–H. Por eso Gly (no polar) tiene KD −0.4 y Cys (polar) tiene KD +2.5.':
        "Nonpolar describes the chemistry of the R group (no O–H or N–H, it doesn't form H-bonds). Hydrophobic describes how much it pays to hide from water, and that depends on its C–H surface. That's why Gly (nonpolar) has KD −0.4 and Cys (polar) has KD +2.5.",
    'Promedio de la hidropatía de una secuencia. > 0 tiende a estar en membranas; < 0, soluble en agua.':
        'Average hydropathy of a sequence. > 0 tends to be in membranes; < 0, soluble in water.',
    'Carga neta':
        'Net charge',
    'Suma de cargas: +1 por K y R, −1 por D y E (His ≈ 0 a pH 7, ≈ +1 a pH 5).':
        'Sum of charges: +1 for K and R, −1 for D and E (His ≈ 0 at pH 7, ≈ +1 at pH 5).',
    'No lo sintetizamos (o no a la velocidad necesaria). Son 9: His, Ile, Leu, Lys, Met, Phe, Thr, Trp, Val.':
        "We don't synthesize it (or not at the rate needed). There are 9: His, Ile, Leu, Lys, Met, Phe, Thr, Trp, Val.",
    'Condicionalmente esencial':
        'Conditionally essential',
    'Normalmente se sintetiza, pero no alcanza en prematuridad, estrés, enfermedad o crecimiento rápido. Son 6: Arg, Cys, Gln, Gly, Pro, Tyr.':
        'Normally synthesized, but not enough in prematurity, stress, illness or rapid growth. There are 6: Arg, Cys, Gln, Gly, Pro, Tyr.',
    'Son 5: Ala, Asp, Asn, Glu, Ser.':
        'There are 5: Ala, Asp, Asn, Glu, Ser.',
    'Código de 1 letra':
        '1-letter code',
    'Los menos intuitivos: F=Phe, Y=Tyr, W=Trp, N=Asn, Q=Gln, D=Asp, E=Glu, K=Lys, R=Arg.':
        'The least intuitive: F=Phe, Y=Tyr, W=Trp, N=Asn, Q=Gln, D=Asp, E=Glu, K=Lys, R=Arg.',
    'Codón / anticodón':
        'Codon / anticodon',
    'Triplete del ARNm y su complemento en el ARNt (antiparalelo). AUG = Met = inicio.':
        'A triplet in the mRNA and its complement in the tRNA (antiparallel). AUG = Met = start.',
    'Modificación postraduccional':
        'Post-translational modification',
    'Cambio químico tras la traducción: fosforilación, acetilación, hidroxilación, glicosilación…':
        'A chemical change after translation: phosphorylation, acetylation, hydroxylation, glycosylation…',
    'Puente salino':
        'Salt bridge',
    'Atracción entre una carga + y una − (Lys–Asp).':
        'Attraction between a + and a − charge (Lys–Asp).',
    'Las cadenas no polares se juntan porque así liberan agua ordenada a su alrededor.':
        'Nonpolar chains come together because that releases the ordered water around them.',
    'Catión–π':
        'Cation–π',
    'Una carga + (Lys, Arg) se pega a la cara de un anillo aromático (Phe, Tyr, Trp).':
        'A + charge (Lys, Arg) sticks to the face of an aromatic ring (Phe, Tyr, Trp).',
    'Enlace covalente S–S entre dos Cys (oxidación). Lehninger: los residuos unidos así (cistina) son fuertemente hidrofóbicos.':
        'Covalent S–S bond between two Cys (oxidation). Lehninger: residues linked this way (cystine) are strongly hydrophobic.',
    'Clasificación':
        'Classification',
    'Los tipos del juego son los 5 grupos de Lehninger: no polar alifático, aromático, polar sin carga, cargado + y cargado −. Otras fuentes ponen Gly, Cys o Trp en otros grupos según la escala de hidrofobicidad.':
        "The game's types are Lehninger's 5 groups: nonpolar aliphatic, aromatic, polar uncharged, charged + and charged −. Other sources put Gly, Cys or Trp in other groups depending on the hydrophobicity scale.",
    'Motivo RGD':
        'RGD motif',
    'Arg-Gly-Asp: el motivo de la fibronectina que reconocen las integrinas para pegar la célula a la matriz extracelular. Algunos antiplaquetarios imitan este motivo.':
        'Arg-Gly-Asp: the fibronectin motif that integrins recognize to attach the cell to the extracellular matrix. Some antiplatelet drugs mimic this motif.',
    'TRH (tiroliberina)':
        'TRH (thyrotropin-releasing hormone)',
    'El hipotálamo la libera para que la hipófisis secrete TSH. Madura con dos modificaciones: la Gln N-terminal se cicla a piroglutamato y el extremo C queda amidado.':
        'The hypothalamus releases it so the pituitary secretes TSH. It matures with two modifications: the N-terminal Gln cyclizes into pyroglutamate and the C-terminus is amidated.',
    'Sitio de la caspasa-3':
        'Caspase-3 site',
    'La caspasa-3, verdugo de la apoptosis, corta justo después del Asp de DEVD (por ejemplo, en PARP). Las caspasas son cisteín-proteasas que cortan después de un Asp.':
        'Caspase-3, the executioner of apoptosis, cuts right after the Asp of DEVD (for example, in PARP). Caspases are cysteine proteases that cut after an Asp.',
    'Met-encefalina':
        'Met-enkephalin',
    'Opioide endógeno que se une a receptores δ y μ y reduce el dolor. Sale del corte de la proencefalina.':
        "An endogenous opioid that binds δ and μ receptors and reduces pain. It's cut out of proenkephalin.",
    'Leu-encefalina':
        'Leu-enkephalin',
    'Como la Met-encefalina, pero termina en Leu. Su Tyr N-terminal es clave: el fenol de la morfina imita a ese Tyr.':
        "Like Met-enkephalin, but it ends in Leu. Its N-terminal Tyr is key: morphine's phenol mimics that Tyr.",
    'Fragmento central del péptido β-amiloide del Alzheimer. Su parche hidrofóbico (Leu, Val, Phe, Phe) hace que las hebras se apilen en fibras amiloides.':
        "Central fragment of the Alzheimer's β-amyloid peptide. Its hydrophobic patch (Leu, Val, Phe, Phe) makes the strands stack into amyloid fibers.",
    'NLS del antígeno T de SV40':
        'SV40 large T antigen NLS',
    'La NLS clásica, de un virus: las importinas reconocen su parche de Lys y Arg y llevan la proteína al núcleo a través del poro.':
        'The classic NLS, from a virus: importins recognize its patch of Lys and Arg and carry the protein into the nucleus through the pore.',
    'Angiotensina II':
        'Angiotensin II',
    'La ECA la corta de la angiotensina I. Contrae los vasos y sube la presión; los IECA (como el enalapril) bloquean su formación.':
        'ACE cuts it from angiotensin I. It constricts blood vessels and raises blood pressure; ACE inhibitors (like enalapril) block its formation.',
    'Oxitocina':
        'Oxytocin',
    'Hormona de la hipófisis posterior: contracciones del parto y salida de la leche. Sus Cys 1 y 6 forman un disulfuro que cierra un anillo, y el extremo C está amidado.':
        'A posterior pituitary hormone: labor contractions and milk let-down. Its Cys 1 and 6 form a disulfide that closes a ring, and the C-terminus is amidated.',
    'Vasopresina':
        'Vasopressin',
    'Hormona antidiurética: el riñón retiene agua. Difiere de la oxitocina solo en las posiciones 3 (Phe) y 8 (Arg); también tiene el disulfuro Cys1–Cys6.':
        'Antidiuretic hormone: the kidney retains water. It differs from oxytocin only at positions 3 (Phe) and 8 (Arg); it also has the Cys1–Cys6 disulfide.',
    'Bradicinina':
        'Bradykinin',
    'Vasodilatador e inflamatorio. La ECA también la degrada: por eso los IECA pueden causar tos seca.':
        "Vasodilator and pro-inflammatory. ACE also degrades it: that's why ACE inhibitors can cause a dry cough.",
    'Del hipotálamo: hace que la hipófisis libere LH y FSH. Como la TRH, empieza con piroglutamato y termina amidada.':
        'From the hypothalamus: it makes the pituitary release LH and FSH. Like TRH, it starts with pyroglutamate and ends amidated.',
    'Kisspeptina-10':
        'Kisspeptin-10',
    'Activa a las neuronas de GnRH y dispara la pubertad. Termina en Arg-Phe-NH₂, como toda la familia de péptidos RF-amida.':
        'Activates GnRH neurons and triggers puberty. It ends in Arg-Phe-NH₂, like the whole RF-amide peptide family.',
    'Sustancia P':
        'Substance P',
    'Neuropéptido del dolor y la inflamación. Termina en Phe-X-Gly-Leu-Met-NH₂, la firma de las taquicininas.':
        'A neuropeptide of pain and inflammation. It ends in Phe-X-Gly-Leu-Met-NH₂, the signature of tachykinins.',
    'Péptido Tat del VIH-1':
        'HIV-1 Tat peptide',
    'Residuos 47–57 de la proteína Tat del VIH-1: tan rico en Arg que atraviesa membranas. Se usa como péptido penetrante para meter fármacos a las células. Al René-virus le cae bien.':
        "Residues 47–57 of the HIV-1 Tat protein: so rich in Arg that it crosses membranes. It's used as a cell-penetrating peptide to get drugs into cells. The René-virus likes it.",
    'Guardián de la Membrana':
        'Membrane Guardian',
    'Hélice transmembrana':
        'Transmembrane helix',
    'Construye un segmento que pueda atravesar la bicapa: al menos 6 residuos con GRAVY > 1.5.':
        'Build a segment that can cross the bilayer: at least 6 residues with GRAVY > 1.5.',
    'Las hélices transmembrana reales tienen ~20 residuos no polares: ≈ 30 Å, el grosor del núcleo de la bicapa. Así las predice el gráfico de hidropatía de Kyte-Doolittle.':
        "Real transmembrane helices have ~20 nonpolar residues: ≈ 30 Å, the thickness of the bilayer core. That's how the Kyte-Doolittle hydropathy plot predicts them.",
    'Guardiana del Citosol':
        'Cytosol Guardian',
    'Proteína soluble y regulable':
        'Soluble, regulatable protein',
    'Construye una superficie soluble: al menos 6 residuos, GRAVY < −1.0 y al menos un sitio de fosforilación (S, T o Y).':
        'Build a soluble surface: at least 6 residues, GRAVY < −1.0 and at least one phosphorylation site (S, T or Y).',
    'Las proteínas solubles exponen residuos polares al agua. Los S/T/Y expuestos son blancos de quinasas: así se encienden y apagan las vías de señalización.':
        "Soluble proteins expose polar residues to water. Exposed S/T/Y are kinase targets: that's how signaling pathways are turned on and off.",
    'Complejo del Poro Nuclear':
        'Nuclear Pore Complex',
    'Señal de localización nuclear':
        'Nuclear localization signal',
    'Para entrar al núcleo, construye una NLS: entre 4 y 8 residuos con carga neta ≥ +4 (K, R = +1; D, E = −1). Necesitas al menos 4 Lys en tu equipo.':
        'To enter the nucleus, build an NLS: between 4 and 8 residues with net charge ≥ +4 (K, R = +1; D, E = −1). You need at least 4 Lys in your team.',
    'La NLS clásica es PKKKRKV (antígeno T de SV40). Las importinas reconocen ese parche básico y llevan la proteína a través del poro nuclear. Ya puedes cruzar los poros.':
        'The classic NLS is PKKKRKV (SV40 large T antigen). Importins recognize that basic patch and carry the protein through the nuclear pore. You can now cross the pores.',
    'Guardiana del Retículo':
        'Reticulum Guardian',
    'Señal de retención en el RE':
        'ER retention signal',
    'Las proteínas solubles del RE llevan una etiqueta en su extremo C-terminal para no escaparse. Construye un péptido de al menos 4 residuos que termine en esa señal: K-D-E-L.':
        "Soluble ER proteins carry a tag at their C-terminus so they don't escape. Build a peptide of at least 4 residues that ends in that signal: K-D-E-L.",
    'BiP, la PDI y la calreticulina terminan en KDEL. Si escapan al Golgi, el receptor de KDEL las regresa al RE en vesículas COPI.':
        'BiP, PDI and calreticulin end in KDEL. If they escape to the Golgi, the KDEL receptor sends them back to the ER in COPI vesicles.',
    'Guardián del Golgi':
        'Golgi Guardian',
    'Dominio tipo mucina':
        'Mucin-type domain',
    'En el Golgi se añaden O-glicanos al OH de Ser y Thr. Construye un dominio tipo mucina: al menos 6 residuos y al menos 60% de S o T. (La Asn llega del RE ya N-glicosilada; aquí solo se recorta su glicano.)':
        'In the Golgi, O-glycans are added to the OH of Ser and Thr. Build a mucin-type domain: at least 6 residues and at least 60% S or T. (Asn arrives from the ER already N-glycosylated; here its glycan is only trimmed.)',
    'Las mucinas tienen dominios ricos en Pro, Thr y Ser (PTS). En el Golgi, las GalNAc-transferasas ponen O-glicanos en casi todas sus Ser/Thr: la proteína queda cubierta de azúcares y atrapa agua (el moco). La N-glicosilación de la Asn es igual de común, pero empieza antes: la OST del RE la pone durante la traducción sobre el secuón N-X-S/T. Con nivel 5, tus Ser y Thr se pueden O-glicosilar dentro del Golgi (Equipo → V).':
        "Mucins have domains rich in Pro, Thr and Ser (PTS). In the Golgi, GalNAc-transferases put O-glycans on almost all of their Ser/Thr: the protein ends up coated in sugars and traps water (mucus). Asn N-glycosylation is just as common, but it starts earlier: the ER's OST adds it during translation at the N-X-S/T sequon. At level 5, your Ser and Thr can be O-glycosylated inside the Golgi (Team → V).",
    'Guardiana del Lisosoma':
        'Lysosome Guardian',
    'Sensor de pH':
        'pH sensor',
    'Construye un péptido de 3 a 8 residuos casi neutro en el citosol (carga entre −1 y +1 a pH 7.4) que se vuelva claramente positivo en el lisosoma (carga ≥ +2 a pH 5). Se cuentan solo las cadenas laterales.':
        'Build a peptide of 3 to 8 residues that is nearly neutral in the cytosol (charge between −1 and +1 at pH 7.4) and becomes clearly positive in the lysosome (charge ≥ +2 at pH 5). Only side chains count.',
    'La His (pKR 6) es la única cadena lateral que cambia mucho de carga entre pH 7.4 y 5. Así funcionan los péptidos que escapan de endosomas y muchos sensores de pH en proteínas.':
        "His (pKR 6) is the only side chain whose charge changes a lot between pH 7.4 and 5. That's how endosome-escaping peptides and many protein pH sensors work.",
    'Guardián del Colágeno':
        'Collagen Guardian',
    'Hebra de colágeno':
        'Collagen strand',
    'Construye una hebra con el patrón Gly-X-Y: al menos 9 residuos, una Gly cada 3 (puede empezar en la posición 1, 2 o 3) y al menos una P.':
        'Build a strand with the Gly-X-Y pattern: at least 9 residues, a Gly every 3 (it can start at position 1, 2 or 3) and at least one P.',
    'Cada tercer residuo debe ser Gly: es la única cadena lateral (un H) que cabe en el centro de la triple hélice. Las mutaciones de esas Gly causan osteogénesis imperfecta.':
        "Every third residue must be Gly: it's the only side chain (an H) that fits in the center of the triple helix. Mutations in those Gly cause osteogenesis imperfecta.",
    'hélice α 1: C=O(i) ··· H–N(i+4)':
        'α helix 1: C=O(i) ··· H–N(i+4)',
    'hélice α 2':
        'α helix 2',
    'lazo que une las dos hélices':
        'loop joining the two helices',
    'hebra β 1':
        'β strand 1',
    'giro β (Gly–Pro) que dobla la cadena':
        'β turn (Gly–Pro) that bends the chain',
    'hebra β 2: lámina antiparalela':
        'β strand 2: antiparallel sheet',
    'puentes de H entre las hebras':
        'H-bonds between the strands',
    'núcleo hidrofóbico: estado nativo':
        'hydrophobic core: native state',
    'extra: puente salino Lys⁺···⁻Asp':
        'extra: salt bridge Lys⁺···⁻Asp',
    'extra: disulfuro Cys–S–S–Cys':
        'extra: disulfide Cys–S–S–Cys',
    'Anemia falciforme (HbS): en la β-globina, Glu6 → Val (E6V). ¿Qué cambia en ese residuo de la superficie?':
        'Sickle cell anemia (HbS): in β-globin, Glu6 → Val (E6V). What changes in that surface residue?',
    'Pierde una carga − y gana una cadena no polar: la Hb desoxigenada polimeriza por ese parche hidrofóbico':
        'It loses a − charge and gains a nonpolar side chain: deoxygenated Hb polymerizes through that hydrophobic patch',
    'Gana una carga + y forma un puente salino nuevo':
        'It gains a + charge and forms a new salt bridge',
    'Se forma un puente disulfuro entre dos globinas':
        'A disulfide bridge forms between two globins',
    'Pierde un sitio de fosforilación':
        'It loses a phosphorylation site',
    'Glu es Cargado − (pKR 4.25); Val es No polar (KD +4.2). La Val6 encaja en un bolsillo hidrofóbico de otra Hb: se forman fibras y el eritrocito toma forma de hoz.':
        'Glu is Charged − (pKR 4.25); Val is Nonpolar (KD +4.2). Val6 fits into a hydrophobic pocket of another Hb: fibers form and the red blood cell takes on a sickle shape.',
    'Hemoglobina C: Glu6 → Lys (E6K). ¿Cuánto cambia la carga de esa cadena lateral a pH 7?':
        'Hemoglobin C: Glu6 → Lys (E6K). How much does the charge of that side chain change at pH 7?',
    '+2 (de −1 a +1)':
        '+2 (from −1 to +1)',
    'Glu a pH 7 es −1; Lys es +1. Por eso HbC migra distinto en la electroforesis.':
        "Glu at pH 7 is −1; Lys is +1. That's why HbC migrates differently in electrophoresis.",
    'Osteogénesis imperfecta: una Gly del colágeno tipo I (Gly-X-Y) cambia a Ser. ¿Por qué es tan grave?':
        'Osteogenesis imperfecta: a Gly in type I collagen (Gly-X-Y) changes to Ser. Why is it so serious?',
    'La Gly es la única que cabe en el centro de la triple hélice; cualquier cadena lateral la desestabiliza':
        'Gly is the only one that fits in the center of the triple helix; any side chain destabilizes it',
    'La Ser se fosforila y repele a las otras cadenas':
        'Ser gets phosphorylated and repels the other chains',
    'La Ser forma un disulfuro con otra cadena':
        'Ser forms a disulfide with another chain',
    'La Ser vuelve al colágeno demasiado hidrofóbico':
        'Ser makes collagen too hydrophobic',
    'En la triple hélice, cada tercer residuo queda en el eje central, donde solo cabe un H. Sustituir esa Gly rompe el plegamiento: huesos frágiles.':
        'In the triple helix, every third residue sits on the central axis, where only an H fits. Replacing that Gly breaks the folding: brittle bones.',
    'Fibrosis quística: la mutación más común de CFTR (ΔF508) elimina una Phe. ¿Qué le pasa a la proteína?':
        'Cystic fibrosis: the most common CFTR mutation (ΔF508) deletes a Phe. What happens to the protein?',
    'Se pliega mal; el control de calidad del RE la retiene y la manda a degradar (ERAD)':
        'It misfolds; ER quality control holds it back and sends it for degradation (ERAD)',
    'Se vuelve más ácida y precipita en el citosol':
        'It becomes more acidic and precipitates in the cytosol',
    'Pierde su péptido señal y se queda en el citosol':
        'It loses its signal peptide and stays in the cytosol',
    'Gana un sitio de N-glicosilación y se acumula en el Golgi':
        'It gains an N-glycosylation site and builds up in the Golgi',
    'Sin la Phe508 el dominio NBD1 no se pliega bien. Las chaperonas del RE la detectan, la ubiquitinan y el proteasoma la degrada: casi no llega a la membrana.':
        "Without Phe508 the NBD1 domain doesn't fold properly. ER chaperones detect it, it gets ubiquitinated and the proteasome degrades it: almost none reaches the membrane.",
    'KRAS G12D (frecuente en cáncer de páncreas): Gly12 → Asp. ¿Qué cambia?':
        'KRAS G12D (common in pancreatic cancer): Gly12 → Asp. What changes?',
    'Entra una cadena con carga − donde solo había un H: estorba la hidrólisis de GTP y KRAS queda encendida':
        'A side chain with a − charge appears where there was only an H: it gets in the way of GTP hydrolysis and KRAS stays switched on',
    'KRAS pierde su sitio de unión a ATP':
        'KRAS loses its ATP-binding site',
    'Se forma un puente disulfuro que la inactiva':
        'A disulfide bridge forms that inactivates it',
    'Nada: Gly y Asp son del mismo grupo':
        'Nothing: Gly and Asp are in the same group',
    'La Gly12 está pegada al sitio del GTP; cualquier cadena lateral impide que la GAP acelere la hidrólisis. KRAS-GTP sigue mandando señales de proliferación.':
        'Gly12 sits right next to the GTP site; any side chain prevents GAP from speeding up hydrolysis. KRAS-GTP keeps sending proliferation signals.',
    'Fenilcetonuria: en la fenilalanina hidroxilasa, Arg408 → Trp (R408W). ¿Qué se pierde en ese sitio?':
        'Phenylketonuria: in phenylalanine hydroxylase, Arg408 → Trp (R408W). What is lost at that site?',
    'Una carga + que hacía puentes salinos; entra un anillo grande sin carga y la enzima se pliega mal':
        'A + charge that formed salt bridges; a large uncharged ring comes in and the enzyme misfolds',
    'Un sitio de fosforilación':
        'A phosphorylation site',
    'Un puente disulfuro':
        'A disulfide bridge',
    'Un grupo Ácido que unía al cofactor':
        'An Acidic group that bound the cofactor',
    'Arg es Cargado + (pKR 12.5); Trp es Aromático. Sin la enzima, la Phe se acumula y la Tyr se vuelve esencial para el paciente.':
        'Arg is Charged + (pKR 12.5); Trp is Aromatic. Without the enzyme, Phe builds up and Tyr becomes essential for the patient.',
    'Enfermedad de Huntington: la huntingtina tiene demasiadas repeticiones del codón CAG. ¿Qué tramo se alarga en la proteína?':
        "Huntington's disease: huntingtin has too many repeats of the CAG codon. Which stretch gets longer in the protein?",
    'Poliglutamina (CAG = Gln)':
        'Polyglutamine (CAG = Gln)',
    'Polialanina (CAG = Ala)':
        'Polyalanine (CAG = Ala)',
    'Poliserina (CAG = Ser)':
        'Polyserine (CAG = Ser)',
    'Policisteína (CAG = Cys)':
        'Polycysteine (CAG = Cys)',
    'CAG codifica Gln. Con más de ~36 repeticiones, el tramo poli-Q se agrega y daña las neuronas.':
        'CAG encodes Gln. With more than ~36 repeats, the poly-Q stretch aggregates and damages neurons.',
    'p53 R175H (mutación frecuente en cáncer). Arg e His son del grupo básico, ¿por qué la His no sustituye bien a la Arg?':
        "p53 R175H (a common cancer mutation). Arg and His are both in the basic group, so why doesn't His substitute well for Arg?",
    'Con pKR 6 la His casi no tiene carga a pH 7, mientras la Arg (pKR 12.5) siempre es +':
        'With pKR 6, His has almost no charge at pH 7, while Arg (pKR 12.5) is always +',
    'La His es más grande que la Arg':
        'His is larger than Arg',
    'La His es ácida a pH 7':
        'His is acidic at pH 7',
    'La His forma disulfuros':
        'His forms disulfides',
    'Estar en el mismo grupo de Lehninger no hace a dos residuos intercambiables: el pKR decide si la carga existe a pH 7.':
        "Being in the same Lehninger group doesn't make two residues interchangeable: the pKR decides whether the charge exists at pH 7.",
    'El alelo de la HbS se debe a GAG → GUG en el codón 6. ¿Qué tipo de mutación es?':
        'The HbS allele is due to GAG → GUG at codon 6. What type of mutation is it?',
    'De sentido erróneo (missense): Glu → Val':
        'Missense: Glu → Val',
    'Silenciosa':
        'Silent',
    'Sin sentido (nonsense)':
        'Nonsense',
    'Corrimiento del marco de lectura':
        'Frameshift',
    'GAG = Glu y GUG = Val: cambia un aminoácido por otro.':
        'GAG = Glu and GUG = Val: one amino acid is swapped for another.',
    'Un codón UGG (Trp) muta a UGA. ¿Qué le pasa a la proteína?':
        'A UGG codon (Trp) mutates to UGA. What happens to the protein?',
    'UGA es codón de paro: la proteína sale truncada (mutación sin sentido)':
        'UGA is a stop codon: the protein comes out truncated (nonsense mutation)',
    'Nada: UGA también codifica Trp':
        'Nothing: UGA also encodes Trp',
    'Se cambia Trp por Cys':
        'Trp is replaced by Cys',
    'Se corre el marco de lectura':
        'The reading frame shifts',
    'UAA, UAG y UGA son los codones de paro (en mitocondrias humanas UGA sí es Trp, pero no en el citosol).':
        'UAA, UAG and UGA are the stop codons (in human mitochondria UGA does code for Trp, but not in the cytosol).',
    'Un codón CUU (Leu) muta a CUC. ¿Efecto en la proteína?':
        'A CUU codon (Leu) mutates to CUC. Effect on the protein?',
    'Ninguno: CUC también es Leu (mutación silenciosa)':
        'None: CUC is also Leu (silent mutation)',
    'Codón de paro':
        'Stop codon',
    'El código es degenerado: Leu tiene 6 codones (UUA, UUG, CUU, CUC, CUA, CUG).':
        'The code is degenerate: Leu has 6 codons (UUA, UUG, CUU, CUC, CUA, CUG).',
    'Bienvenida':
        'Welcome',
    'Estás en el citosol. Las zonas con símbolos (· ≈ ◦ ∴ ░ ═ ● § ▓ ╳) tienen aminoácidos salvajes. El panel de la derecha muestra quién vive en cada zona. [M] abre el manual.':
        "You're in the cytosol. Areas with symbols (· ≈ ◦ ∴ ░ ═ ● § ▓ ╳) have wild amino acids. The panel on the right shows who lives in each area. [M] opens the manual.",
    'Envoltura nuclear':
        'Nuclear envelope',
    'Doble membrana con poros (O). Las moléculas pequeñas (< ~40 kDa) difunden; las proteínas grandes necesitan una señal de localización nuclear (NLS): un parche rico en Lys y Arg. Afuera solo hay Lys (en los ribosomas ∴): con 4 basta para entrar, y adentro te espera la Arg.':
        "Double membrane with pores (O). Small molecules (< ~40 kDa) diffuse through; large proteins need a nuclear localization signal (NLS): a patch rich in Lys and Arg. Outside there's only Lys (in the ribosomes ∴): 4 are enough to get in, and Arg is waiting inside.",
    'Cara cis (hacia el RE) → cara trans (hacia la membrana). Las proteínas avanzan cisterna por cisterna mientras maduran sus glicanos.':
        'Cis face (toward the ER) → trans face (toward the membrane). Proteins move cisterna by cisterna while their glycans mature.',
    'Pisa sus crestas para recuperar la energía de tu equipo y recargar ATP.':
        "Step on its cristae to restore your team's energy and recharge ATP.",
    'La V-ATPasa bombea H⁺ al interior y baja el pH a ~5. A ese pH la His (pKR 6) está protonada: aquí cuenta como +.':
        'The V-ATPase pumps H⁺ inside and lowers the pH to ~5. At that pH His (pKR 6) is protonated: here it counts as +.',
    'Bicapa lipídica':
        'Lipid bilayer',
    'Cabezas polares (◦) hacia el agua, colas hidrofóbicas (≈) hacia adentro. Mide ~30 Å: justo lo que cubre una hélice α de ~20 residuos hidrofóbicos.':
        "Polar heads (◦) toward the water, hydrophobic tails (≈) inward. It's ~30 Å thick: exactly what an α helix of ~20 hydrophobic residues spans.",
    'Colágeno, elastina y proteoglicanos secretados por los fibroblastos. El colágeno es la proteína más abundante del cuerpo.':
        'Collagen, elastin and proteoglycans secreted by fibroblasts. Collagen is the most abundant protein in the body.',
    'Centrosoma':
        'Centrosome',
    'De aquí salen los microtúbulos (─ │ ╱ ╲): rieles por los que las vesículas viajan del Golgi a la membrana.':
        'Microtubules (─ │ ╱ ╲) grow from here: tracks that vesicles travel along from the Golgi to the membrane.',
    'Ribosomas libres: cada uno lee un ARNm y une aminoácidos con enlaces peptídicos. Sus proteínas ribosomales son ricas en Lys (K).':
        'Free ribosomes: each one reads an mRNA and joins amino acids with peptide bonds. Their ribosomal proteins are rich in Lys (K).',
    'Jugar':
        'Play',
    'Afin.':
        'Affin.',
    'Inter.':
        'Inter.',
    'Modif.':
        'Modif.',
    'Zonas':
        'Areas',
    'Nutr.':
        'Nutr.',
    'Glos.':
        'Gloss.',
    'Chuleta':
        'Cheat sheet',
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
    'lenta':
        'slow',
    'normal':
        'normal',
    'rápida':
        'fast',
    'nombre':
        'name',
    'nivel':
        'level',
    'grupo':
        'group',
    'Vitamina C':
        'Vitamin C',
    'Vitamina K':
        'Vitamin K',
    'M o ?':
        'M or ?',
}
