"""Logros: metas de reconocimiento que se anuncian al volver al mapa y se ven
en la Aminodex (tecla L). Se calculan con el estado de la partida, así que
también se ganan con partidas viejas."""

import curses

import datos
import dibujo as d
import preguntas
import progreso
from idioma import tr


def _capturados(j):
    return sum(1 for c in datos.ORDEN if j["capturados"].get(c))


def _amidas(j):
    """Gln/Asn: 10 aciertos de nombre sin haberlas confundido nunca."""
    a = j["aciertos"]
    conf = j.get("confusiones", {})
    return a.get("Q:nombre", 0) + a.get("N:nombre", 0) >= 10 and not (
        conf.get("Q>N") or conf.get("N>Q"))


# (clave, nombre, cómo se gana, condición)
LOGROS = [
    ("tres", "Primer equipo", "Ten 3 aminoácidos capturados.", lambda j: _capturados(j) >= 3),
    ("diez", "Medio camino", "Captura 10 de los 20.", lambda j: _capturados(j) >= 10),
    ("veinte", "Aminodex completa", "Captura los 20 aminoácidos estándar.",
     lambda j: _capturados(j) >= 20),
    ("dom5", "Ojo entrenado", "Domina 5 aminoácidos (nombre y los dos códigos).",
     lambda j: preguntas.dominados(j) >= 5),
    ("dom20", "Los 20 dominados", "Domina los 20 aminoácidos.",
     lambda j: preguntas.dominados(j) >= 20),
    ("amidas", "Ni Gln ni Asn me engañan", "Acierta 10 veces Gln o Asn sin confundirlas nunca.",
     _amidas),
    ("reloj15", "Contrarreloj", "Haz 15 aciertos en el contrarreloj de 60 s.",
     lambda j: j.get("records", {}).get("reloj", 0) >= 15),
    ("repaso", "Al día", "Termina el repaso de hoy (nada pendiente).",
     lambda j: bool(j.get("leitner")) and not progreso.para_hoy(j)),
    ("insignias", "Todas las insignias", "Vence a los jefes de la célula.",
     lambda j: len(j["insignias"]) >= 7),
    ("doctorado", "Doctorado", "Aprueba el examen final del René-virus.",
     lambda j: bool(j.get("doctorado"))),
]


def nuevos(juego):
    """Los logros recién ganados (y los marca como ganados)."""
    ganados = juego.setdefault("logros", [])
    salida = []
    for clave, nombre, _, cond in LOGROS:
        if clave not in ganados and cond(juego):
            ganados.append(clave)
            salida.append(nombre)
    return salida


def anunciar(win, juego, redibujar=None):
    """Un aviso por logro nuevo; redibujar() limpia lo de atrás para que los
    avisos no se encimen con el anterior."""
    for nombre in nuevos(juego):
        if redibujar:
            redibujar()
        else:
            win.erase()
        d.popup(win, tr("¡Logro desbloqueado! {nombre}", nombre=tr(nombre)), tr("Logro"),
                ancho=50, attr=d.c("bien"))


def mostrar(win, juego):
    ganados = juego.get("logros", [])
    lineas = []
    for clave, nombre, como, _ in LOGROS:
        marca = "√" if clave in ganados else "·"
        lineas.append(f"{marca} {tr(nombre)}: {tr(como)}")
    win.erase()
    d.popup(win, "\n".join(lineas), tr("Logros · {n}/{total}", n=len(ganados), total=len(LOGROS)),
            ancho=76)
    curses.flushinp()
