"""Idioma del juego: español (el del código) o inglés.

Todos los textos se escriben en español y se pasan por tr(). En inglés, tr()
busca la traducción en en.py usando el texto en español como clave; si no la
encuentra, deja el español. Los datos (aminoácidos, zonas, jefes…) se
traducen campo por campo con traducir() al importar cada módulo.

El idioma se elige al iniciar: `aminomon --en` / `aminomon --es`, o desde la
pantalla de título (se recuerda en ~/.aminomon_idioma).
"""

import os
import sys

ARCHIVO = os.path.expanduser("~/.aminomon_idioma")
IDIOMAS = ("es", "en")


def _detectar():
    for arg in sys.argv[1:]:
        if arg in ("--es", "--en"):
            return arg[2:]
    try:
        with open(ARCHIVO, encoding="utf-8") as f:
            idioma = f.read().strip()
    except OSError:
        return "es"
    return idioma if idioma in IDIOMAS else "es"


ACTUAL = _detectar()
EN = {}
if ACTUAL == "en":
    from en import EN


def guardar(idioma):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        f.write(idioma + "\n")


def tr(texto, **valores):
    """Traduce un texto; los {campos} se llenan con valores."""
    if ACTUAL == "en":
        texto = EN.get(texto, texto)
    return texto.format(**valores) if valores else texto


def _traducir_valor(v):
    if isinstance(v, str):
        return tr(v)
    if isinstance(v, list):
        return [_traducir_valor(x) for x in v]
    if isinstance(v, tuple):
        return tuple(_traducir_valor(x) for x in v)
    return v


def traducir(registros, *campos):
    """Traduce en su lugar los campos de texto de cada dict de registros
    (un dict de dicts o una lista de dicts)."""
    if ACTUAL == "es":
        return
    valores = registros.values() if isinstance(registros, dict) else registros
    for r in valores:
        for campo in campos:
            if campo in r:
                r[campo] = _traducir_valor(r[campo])
