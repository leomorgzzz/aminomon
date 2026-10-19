#!/usr/bin/env python3
"""Pruebas automáticas de Aminomon (no necesitan terminal ni curses).

    python3 pruebas/correr.py

Revisa lo que no se ve sin jugar:
  1. todos los módulos importan, en español y en inglés;
  2. cada tr("…") tiene su traducción y ninguno recibe un f-string (con un
     f-string la clave nunca coincide);
  3. una misma clave no tiene dos traducciones distintas en traduccion/;
  4. los datos ya traducidos (aminoácidos, zonas, jefes…) no quedan en español,
     ni los grupos de las interacciones;
  5. en el examen del René-virus la correcta no es casi siempre la más larga;
  6. solo hay símbolos que la consola de Windows sabe dibujar (WGL4);
  7. la lógica: el ribosoma ofrece el ARNt correcto, cada ARNm codifica su
     péptido, en la titulación se llega a todos los puntos y una partida vieja
     carga.
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

# un {campo} que falta o sobra en el inglés hace que tr() falle al formatear
_campo = re.compile(r"{(\w+)[^}]*}")
campos_mal = [f"{k[:60]!r}" for k, (_, v) in vistas.items()
              if set(_campo.findall(k)) != set(_campo.findall(v))]
revisar("cada traducción tiene los mismos {campos} que el español", not campos_mal,
        "\n".join(campos_mal[:10]))

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

# los grupos de las interacciones del grupo R pasan por tr() con una variable,
# así que la prueba 2 no los ve (y un nombre sin acentos no lo detecta la prueba 4)
_grupos = set()
for n in ast.walk(ast.parse(open(os.path.join(RAIZ, "datos.py"), encoding="utf-8").read())):
    if (isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "INTERACCIONES_R"
            and isinstance(n.value, ast.Dict)):
        _grupos |= {g for v in ast.literal_eval(n.value).values() for _, g, _ in v}
sin_trad = sorted(g for g in _grupos if g not in EN and g not in IGUALES)
revisar("los grupos de las interacciones tienen traducción", not sin_trad, ", ".join(sin_trad))

# ------------------------------------- 5. la respuesta larga no se delata
# Si la correcta suele ser la opción más larga, se adivina sin saber.
for idioma_ in ("es", "en"):
    codigo = ("import sys; sys.argv = ['x', '--%s']\n"
              "import jefes\n"
              "print(sum(len(m['correcta']) > max(map(len, m['otras'])) for m in jefes.MUTACIONES),"
              " len(jefes.MUTACIONES))") % idioma_
    r = subprocess.run([sys.executable, "-c", codigo], cwd=RAIZ, capture_output=True, text=True,
                       env=dict(os.environ, HOME=tempfile.mkdtemp()))
    largas, total = map(int, r.stdout.split())
    revisar(f"la correcta del René-virus casi nunca es la más larga ({idioma_})",
            largas <= total * 0.3, f"{largas} de {total} preguntas")

# ------------------------------------------------------------ 6. símbolos
malos = wgl4.revisar([RAIZ])
revisar("solo símbolos WGL4 (los que dibuja la consola de Windows)", not malos,
        "\n".join(f"{ch} U+{ord(ch):04X}  {' '.join(l[:3])}" for ch, l in sorted(malos.items())))

# ------------------------------------------------------------- 7. lógica
import json  # noqa: E402
import random  # noqa: E402

import aminodex  # noqa: E402
import posgame  # noqa: E402
import progreso  # noqa: E402
import sintesis  # noqa: E402

# el ribosoma siempre ofrece el ARNt correcto, sin aminoácidos repetidos, y
# cada anticodón se aparea de verdad con un codón de su aminoácido
random.seed(1)
malos_arnt = []
for cod in list(jefes.CODIGO) + ["UGA*"]:
    correcta = "U" if cod == "UGA*" else None
    cod = cod[:3]
    for _ in range(30):
        ops = sintesis.opciones_arnt(cod, correcta)
        aas = [aa for aa, _ in ops]
        esperado = correcta or jefes.CODIGO[cod]
        if len(set(aas)) != len(aas) or len(ops) != 4:
            malos_arnt.append(f"{cod}: {ops}")
        if esperado != "*" and esperado not in aas:
            malos_arnt.append(f"{cod}: falta {esperado} en {ops}")
        for aa, anti in ops:
            par = sintesis._comp(anti)
            if aa != "U" and jefes.CODIGO.get(par) != aa:
                malos_arnt.append(f"{cod}: {aa} con anticodón {anti}")
revisar("el ribosoma ofrece el ARNt correcto y anticodones que sí se aparean", not malos_arnt,
        "\n".join(sorted(set(malos_arnt))[:10]))

# el ARNm de cada encargo se traduce de vuelta a su péptido
malos_arn = []
for seq in [p["seq"] for p in datos.PEPTIDOS.values()] + [sintesis.SELENO["seq"]]:
    for _ in range(20):
        cods = sintesis._arn(seq)
        leido = "".join("U" if c == "UGA" and i <= len(seq) else jefes.CODIGO[c]
                        for i, c in enumerate(cods))
        if leido != "M" + seq + "*" or cods[0] != "AUG":
            malos_arn.append(f"{seq}: {cods}")
revisar("el ARNm de cada encargo codifica su péptido (y la Sec va en UGA)", not malos_arn,
        "\n".join(malos_arn[:5]))

# en la titulación se puede llegar a cada pK y al pI, en pantallas chicas y grandes
inalcanzables = []
for alto, ancho in ((24, 80), (30, 100), (42, 130)):
    h, w = max(10, min(22, alto - 12)), max(30, min(72, ancho - 40))
    for aa in "GAVDEKHC":
        a = datos.AMINOACIDOS[aa]
        camino = posgame._camino(aa, 3, 7, h, w, len(posgame._pks(aa)))
        puntos = {"pK1": a["pk1"], "pK2": a["pk2"], "pI": a["pi"]}
        if a["pkr"]:
            puntos["pKR"] = a["pkr"]
        for k, v in puntos.items():
            tol = max(0.3, 0.6 * 14 / (h - 1)) if k == "pI" else 0.3
            if min(abs(p[2] - v) for p in camino) > tol:
                inalcanzables.append(f"{ancho}×{alto} {aa} {k}")
revisar("en la titulación se puede llegar a todos los pK y al pI", not inalcanzables,
        ", ".join(inalcanzables))

# una partida de una versión vieja (sin campos nuevos y con 2 péptidos del
# catálogo viejo) carga y se puede usar
viejo = {"pos": [60, 24], "equipo": [{"id": "K", "nivel": 5, "xp": 0, "energia": 10},
                                      {"id": "Zzz", "nivel": 3, "xp": 0, "energia": 5}],
         "capturados": {"K": 1}, "vistos": ["K"], "evos_vistas": [], "objetos": {"ATP": 1},
         "insignias": [], "zonas_visitadas": [], "fallos": {}, "aciertos": {},
         "terminado": True, "doctorado": True, "peptidos": ["nls", "bradi"]}
with open(progreso.ARCHIVO, "w", encoding="utf-8") as f:
    json.dump(viejo, f)
try:
    j = progreso.cargar()
    problemas = []
    if [m["id"] for m in j["equipo"]] != ["K"]:
        problemas.append("el equipo no quitó el residuo desconocido")
    if sintesis.hechos(j) != 1 or sintesis.capitulo(j) != 0:
        problemas.append(f"encargos hechos {sintesis.hechos(j)}, capítulo {sintesis.capitulo(j)}")
    progreso.pendientes(j)
    progreso.todo_completo(j)
    aminodex.entradas(j, "aa")
    if len(aminodex.entradas(j, "pep")) != len(sintesis.HISTORIA):
        problemas.append("la pestaña de péptidos no muestra solo los encargos")
except Exception as e:  # noqa: BLE001
    problemas = [repr(e)]
revisar("una partida vieja carga y se puede usar", not problemas, "\n".join(problemas))

print()
print(f"{len(fallas)} prueba(s) fallaron." if fallas else "Todo bien.")
sys.exit(1 if fallas else 0)
