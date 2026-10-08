"""Estado de la partida, guardado en ~/.aminomon.json, equipo y experiencia."""

import json
import os

import datos
from idioma import tr

ARCHIVO = os.path.expanduser("~/.aminomon.json")


def nuevo_juego(pos):
    return dict(
        pos=list(pos),
        equipo=[],
        capturados={},        # código de 1 letra -> veces capturado
        vistos=[],            # estructuras ya vistas (nombre aún oculto)
        evos_vistas=[],
        objetos={"ATP": 2, "Vitamina C": 0, "Vitamina K": 0},
        insignias=[],
        zonas_visitadas=[],
        carteles_leidos=[],
        fallos={},            # "K:carga" -> n
        aciertos={},
        terminado=False,
        recompensas=[],       # avisos y regalos del René-virus ya entregados
        peptidos=[],          # encargos de síntesis cumplidos (post-juego)
    )


def guardar(juego):
    tmp = ARCHIVO + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(juego, f, ensure_ascii=False, indent=1)
    os.replace(tmp, ARCHIVO)


def cargar():
    try:
        with open(ARCHIVO, encoding="utf-8") as f:
            juego = json.load(f)
    except (OSError, ValueError):
        return None
    # partidas de versiones anteriores
    base = nuevo_juego((0, 0))
    for k, v in base.items():
        juego.setdefault(k, v)
    for k, v in base["objetos"].items():
        juego["objetos"].setdefault(k, v)
    juego["equipo"] = [m for m in juego["equipo"]
                       if m["id"] in datos.AMINOACIDOS or m["id"] in datos.MODIFICACIONES]
    return juego


# ------------------------------------------------------------- aminomones
def energia_max(mon):
    f = datos.forma(mon["id"])
    return 30 + mon["nivel"] * 5 + int(f["masa"] // 15)


def nuevo_mon(fid, nivel):
    mon = dict(id=fid, nivel=nivel, xp=0)
    mon["energia"] = energia_max(mon)
    return mon


def xp_necesaria(mon):
    return 10 + mon["nivel"] * 10


def dar_xp(mon, cantidad):
    """Suma experiencia; devuelve mensajes de subida de nivel."""
    mensajes = []
    mon["xp"] += cantidad
    while mon["xp"] >= xp_necesaria(mon):
        mon["xp"] -= xp_necesaria(mon)
        mon["nivel"] += 1
        mon["energia"] = energia_max(mon)
        nombre = datos.forma(mon["id"])["nombre"]
        mensajes.append(tr("{nombre} sube al nivel {nivel}.", nombre=nombre, nivel=mon["nivel"]))
        if modificaciones_posibles(mon):
            mensajes.append(tr("{nombre} ya puede modificarse (Equipo [E] → V).", nombre=nombre))
    return mensajes


def curar_equipo(juego):
    for m in juego["equipo"]:
        m["energia"] = energia_max(m)


def capturar(juego, aa, nivel):
    juego["capturados"][aa] = juego["capturados"].get(aa, 0) + 1
    if aa not in juego["vistos"]:
        juego["vistos"].append(aa)
    juego["equipo"].append(nuevo_mon(aa, nivel))


def capturado(juego, aa):
    return juego["capturados"].get(aa, 0) > 0


def aminodex_completa(juego):
    return all(capturado(juego, c) for c in datos.ORDEN)


def modificaciones_completas(juego):
    return all(e in juego["evos_vistas"] for e in datos.MODIFICACIONES)


def conteo_equipo(juego):
    """Cuántos residuos de cada aminoácido estándar hay en el equipo. Un
    residuo modificado cuenta como su aminoácido base y la cistina, como dos
    Cys."""
    conteo = {}
    for m in juego["equipo"]:
        base = datos.forma(m["id"])["base"]
        conteo[base] = conteo.get(base, 0) + (2 if m["id"] == "Cis" else 1)
    return conteo


# ------------------------------------------- modificación postraduccional
def modificaciones_posibles(mon):
    if mon["id"] not in datos.AMINOACIDOS:
        return []
    return datos.modificaciones_de(mon["id"])


def requisitos(juego, mon, evo_id, zona_actual):
    """Lista de (texto, cumplido) para la modificación."""
    req = datos.MODIFICACIONES[evo_id]["req"]
    lista = [(tr("Nivel {req} (tiene {nivel})", req=req["nivel"], nivel=mon["nivel"]),
              mon["nivel"] >= req["nivel"])]
    if "objeto" in req:
        n = juego["objetos"].get(req["objeto"], 0)
        lista.append((tr("1 {objeto} (tienes {n})", objeto=tr(req["objeto"]), n=n), n >= 1))
    if "zona" in req:
        nombre = datos.ZONAS[req["zona"]]["nombre"]
        dentro = zona_actual == req["zona"] or (req["zona"] == "nucleo" and zona_actual == "nucleolo")
        lista.append((tr("Estar en: {zona}", zona=nombre), dentro))
    if req.get("otra_cys"):
        otras = sum(1 for m in juego["equipo"] if m["id"] == "C" and m is not mon)
        lista.append((tr("Otra Cys en el equipo"), otras >= 1))
    return lista


def modificar(juego, mon, evo_id):
    req = datos.MODIFICACIONES[evo_id]["req"]
    if "objeto" in req:
        juego["objetos"][req["objeto"]] -= 1
    if req.get("otra_cys"):
        for m in juego["equipo"]:
            if m["id"] == "C" and m is not mon:
                juego["equipo"].remove(m)
                break
    mon["id"] = evo_id
    mon["energia"] = energia_max(mon)
    if evo_id not in juego["evos_vistas"]:
        juego["evos_vistas"].append(evo_id)


# ------------------------------------------------------- repaso espaciado
def registrar(juego, clave, acierto):
    d = juego["aciertos"] if acierto else juego["fallos"]
    d[clave] = d.get(clave, 0) + 1


def peso(juego, clave):
    return max(0.5, 1 + 2 * juego["fallos"].get(clave, 0)
               - 0.5 * juego["aciertos"].get(clave, 0))
