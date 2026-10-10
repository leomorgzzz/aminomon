"""Traducción al inglés de los textos de combate.py."""

EN = {
    '─pirrolidina':
        '─pyrrolidine',
    'pirrolidina─':
        'pyrrolidine─',
    '─CH2─fenilo':
        '─CH2─phenyl',
    'fenilo─CH2─':
        'phenyl─CH2─',
    '─fenol─OH':
        '─phenol─OH',
    'HO─fenol─':
        'HO─phenol─',
    '─indol(N─H)':
        '─indole(N─H)',
    '(H─N)indol─':
        '(H─N)indole─',
    '─guanidinio+':
        '─guanidinium+',
    '+guanidinio─':
        '+guanidinium─',
    '─imidazol(H+)':
        '─imidazole(H+)',
    '(H+)imidazol─':
        '(H+)imidazole─',
    '─pirrolidina─OH':
        '─pyrrolidine─OH',
    'HO─pirrolidina─':
        'HO─pyrrolidine─',
    '─fenil─O─PO3²−':
        '─phenyl─O─PO3²−',
    '²−O3P─O─fenil─':
        '²−O3P─O─phenyl─',
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
    '¿Solo C/H? ¿anillo? ¿OH/SH/amida? ¿NH3+? ¿COO−?':
        'Only C/H? ring? OH/SH/amide? NH3+? COO−?',
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
}
