r"""Caritas: una por aminoácido, del color de su grupo de Lehninger.

El grupo también se nota en la cara: los cargados llevan su carga en los
cachetes (+ o −), los aromáticos lentes de anillo y los polares gotitas de agua
(°). El «pelo» recuerda la cadena lateral: la Met lleva su codón AUG, la Cys
su S-H, los ácidos su COO y los básicos su N.

Cada carita mide 5 filas × 11 columnas: el pelo, la frente, los ojos, la boca
con los cachetes y la barbilla.
"""

import datos

CACHETES = {"alifatico": ("", ""), "aromatico": ("", ""), "polar": ("°", "°"),
            "acido": ("−", "−"), "basico": ("+", "+")}

# (pelo de 11 columnas, ojos de 3, boca de 3)
CARAS = {
    "G": (r"     .     ", r"• •", r"___"),
    "A": (r"    _._    ", r"^ ^", r"\_/"),
    "V": (r"    \|/    ", r"- -", r"\_/"),
    "L": (r"   \\|//   ", r"° °", r"\_/"),
    "I": (r"   //|\\   ", r"o o", r"\_/"),
    "M": (r"   [AUG]   ", r"^ ^", r"\o/"),
    "P": (r"    @@@    ", r"- -", r"~~~"),
    "F": (r"   .-O-.   ", r"o o", r"\_/"),
    "Y": (r"   .-O-OH  ", r"o o", r"\o/"),
    "W": (r"  .-O=O-.  ", r"o o", r"\_/"),
    "S": (r"     OH    ", r"• •", r"\_/"),
    "T": (r"   CH3 OH  ", r"• •", r"\_/"),
    "C": (r"    S-H    ", r"> <", r"\_/"),
    "N": (r"   C=O     ", r"^ ^", r"\_/"),
    "Q": (r"  -C=O     ", r"^ ^", r"\o/"),
    "D": (r"    COO    ", r"> <", r"\_/"),
    "E": (r"   -COO    ", r"> <", r"\o/"),
    "K": (r"   ~~~NH3  ", r"^ ^", r"\_/"),
    "R": (r"   ~~=NH2  ", r"^ ^", r"\o/"),
    "H": (r"    (N)    ", r"o o", r"\_/"),
}


def carita(c):
    """Las 5 filas (11 columnas cada una) de la carita del aminoácido c."""
    pelo, ojos, boca = CARAS.get(c, ("           ", "^ ^", r"\_/"))
    grupo = datos.AMINOACIDOS[c]["grupo"]
    izq, der = CACHETES[grupo]
    o1, o2 = ojos[0], ojos[2]
    if grupo == "aromatico":
        fila_ojos = " / (" + o1 + ")(" + o2 + ")\\ "      # lentes de anillo
    else:
        fila_ojos = " /  " + o1 + " " + o2 + "  \\ "
    return [pelo.ljust(11)[:11],
            '  .-"""-.  ',
            fila_ojos,
            "|" + izq.rjust(2) + " " + boca + " " + der.ljust(2) + "|",
            "  '-...-'  "]
