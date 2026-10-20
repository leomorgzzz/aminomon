"""Idioma del juego: español (el del código) o inglés.

Todos los textos se escriben en español y se pasan por tr(). En inglés, tr()
busca la traducción en en.py usando el texto en español como clave; si no la
encuentra, deja el español. Los datos (aminoácidos, zonas, jefes…) se
traducen campo por campo con traducir() al importar cada módulo.

El idioma se elige al iniciar: `aminomon --en` / `aminomon --es`, o desde la
pantalla de título (se recuerda en ~/.aminomon_idioma). La primera vez se usa
el del sistema: español si está en español, inglés en cualquier otro caso.
"""

import locale
import os
import subprocess
import sys

ARCHIVO = os.path.expanduser("~/.aminomon_idioma")
IDIOMAS = ("es", "en")


def _del_sistema():
    nombres = [os.environ.get(v, "") for v in ("LC_ALL", "LC_MESSAGES", "LANG", "LANGUAGE")]
    try:
        nombres.append(locale.getlocale()[0] or "")
    except ValueError:
        pass
    if sys.platform == "win32":
        try:
            import ctypes
            if ctypes.windll.kernel32.GetUserDefaultUILanguage() & 0x3FF == 0x0A:
                return "es"
        except Exception:  # noqa: BLE001
            pass
    elif sys.platform == "darwin":
        try:
            nombres.append(subprocess.run(["defaults", "read", "-g", "AppleLocale"],
                                          capture_output=True, text=True, timeout=2).stdout)
        except Exception:  # noqa: BLE001
            pass
    for n in nombres:
        n = n.strip().lower()
        if n and n not in ("c", "posix", "c.utf-8"):
            return "es" if n.startswith(("es", "spanish")) else "en"
    return "en"


def _detectar():
    for arg in sys.argv[1:]:
        if arg in ("--es", "--en"):
            return arg[2:]
    try:
        with open(ARCHIVO, encoding="utf-8") as f:
            idioma = f.read().strip()
    except OSError:
        return _del_sistema()
    return idioma if idioma in IDIOMAS else _del_sistema()


ACTUAL = _detectar()
EN = {}
if ACTUAL == "en":
    from en import EN


def guardar(idioma):
    try:
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            f.write(idioma + "\n")
    except OSError:
        pass                    # se cambia igual; solo no se recuerda


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
