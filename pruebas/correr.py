#!/usr/bin/env python3
"""Pruebas automáticas de Aminomon (no necesitan terminal ni curses).

    python3 pruebas/correr.py

Revisa lo que no se ve sin jugar:
  1. todos los módulos importan, en español y en inglés;
  2. cada tr("…") tiene su traducción y ninguno recibe un f-string (con un
     f-string la clave nunca coincide);
  3. una misma clave no tiene dos traducciones distintas en traduccion/;
  4. los datos ya traducidos (aminoácidos, zonas, jefes…) no quedan en español;
  5. solo hay símbolos que la consola de Windows sabe dibujar (WGL4).
Sale con código 1 si algo falla.
"""

import ast
import glob
import os
import re
import subprocess
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)

import wgl4  # noqa: E402

# textos que se escriben igual en inglés y por eso no están en traduccion/
IGUALES = {"No", "GRAVY > 1.5", "GRAVY < −1.0", "1L", "3L"}
# acentos o palabras que solo pueden ser español
ESPANOL = re.compile(r"[áéíóúñ¿¡]|\b(el|la|los|las|del|que|con|para|una|por)\b", re.I)

fallas = []


def revisar(nombre, condicion, detalle=""):
    print(("ok    " if condicion else "FALLA ") + nombre)
    if not condicion:
        fallas.append(nombre)
        if detalle:
            print("      " + str(detalle).replace("\n", "\n      "))


MODULOS = sorted(os.path.basename(f)[:-3] for f in glob.glob(os.path.join(RAIZ, "*.py"))
                 if os.path.basename(f) != "aminomon.py")
CODIGO = [f for f in sorted(glob.glob(os.path.join(RAIZ, "*.py")))
          if os.path.basename(f) not in ("en.py", "idioma.py")]

# ------------------------------------------------------------ 1. importar
for idioma_ in ("es", "en"):
    codigo = ("import sys; sys.argv = ['x', '--%s']\n"
              "import importlib\n"
              "for m in %r: importlib.import_module(m)\n") % (idioma_, MODULOS)
    r = subprocess.run([sys.executable, "-c", codigo], cwd=RAIZ, capture_output=True, text=True,
                       env=dict(os.environ, HOME=tempfile.mkdtemp()))
    revisar(f"los módulos importan ({idioma_})", r.returncode == 0, r.stderr[-1500:])

# ------------------------------------------------------- 2. llamadas a tr
from en import EN  # noqa: E402

faltan, fstrings = [], []
for f in CODIGO:
    for n in ast.walk(ast.parse(open(f, encoding="utf-8").read())):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "tr" and n.args:
            a, donde = n.args[0], f"{os.path.basename(f)}:{n.lineno}"
            if isinstance(a, ast.Constant) and isinstance(a.value, str):
                if a.value not in EN and a.value not in IGUALES:
                    faltan.append(f"{donde}: {a.value[:80]!r}")
            elif isinstance(a, ast.JoinedStr):
                fstrings.append(donde)
revisar("todo tr(\"…\") tiene traducción", not faltan, "\n".join(faltan[:20]))
revisar("ningún tr() recibe un f-string (usa tr(\"… {campo}\", campo=…))", not fstrings,
        "\n".join(fstrings))

# ---------------------------------------------------- 3. claves repetidas
vistas, choques = {}, []
for f in sorted(glob.glob(os.path.join(RAIZ, "traduccion", "en_*.py"))):
    mod = {}
    exec(open(f, encoding="utf-8").read(), mod)
    for k, v in mod["EN"].items():
        if k in vistas and vistas[k][1] != v:
            choques.append(f"{k[:60]!r}: {vistas[k][0]} y {os.path.basename(f)}")
        vistas.setdefault(k, (os.path.basename(f), v))
revisar("ninguna clave tiene dos traducciones distintas", not choques, "\n".join(choques))

# ------------------------------------------------ 4. datos en inglés
sys.argv = ["x", "--en"]
os.environ["HOME"] = tempfile.mkdtemp()
import datos  # noqa: E402
import jefes  # noqa: E402

REGISTROS = [(datos.MOVIMIENTOS, ("nombre", "desc", "ciencia")),
             (datos.TIPOS, ("nombre", "corto", "desc")),
             (datos.AMINOACIDOS, ("nombre", "carga", "nutricion", "pista")),
             (datos.MODIFICACIONES, ("nombre", "carga", "cambio", "bio", "pista")),
             (datos.ZONAS, ("nombre", "por_que")), (datos.PEPTIDOS, ("nombre", "bio")),
             (jefes.JEFES, ("nombre", "reto", "desc", "bio")),
             (jefes.MUTACIONES, ("texto", "correcta", "otras", "expl"))]
en_espanol = set()


def buscar(v):
    if isinstance(v, str):
        if ESPANOL.search(v.replace("René", "")):
            en_espanol.add(v[:90])
    elif isinstance(v, (list, tuple)):
        for x in v:
            buscar(x)


for registros, campos in REGISTROS:
    for r in (registros.values() if isinstance(registros, dict) else registros):
        for campo in campos:
            buscar(r.get(campo))
revisar("los datos en inglés no quedan en español", not en_espanol,
        "\n".join(repr(t) for t in sorted(en_espanol)[:20]))

# ------------------------------------------------------------ 5. símbolos
malos = wgl4.revisar([RAIZ])
revisar("solo símbolos WGL4 (los que dibuja la consola de Windows)", not malos,
        "\n".join(f"{ch} U+{ord(ch):04X}  {' '.join(l[:3])}" for ch, l in sorted(malos.items())))

print()
print(f"{len(fallas)} prueba(s) fallaron." if fallas else "Todo bien.")
sys.exit(1 if fallas else 0)
