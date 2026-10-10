"""Traducción al inglés: texto en español (el que aparece en el código) →
texto en inglés. Lo usa idioma.tr(). Las traducciones viven en
traduccion/en_<módulo>.py, una por cada módulo del juego. Si cambias un texto
en español en el código, actualiza su clave en el archivo de ese módulo; si
falta una traducción, el juego muestra el español."""

from traduccion import en_aminodex
from traduccion import en_aminomon
from traduccion import en_animaciones
from traduccion import en_combate
from traduccion import en_datos
from traduccion import en_dibujo
from traduccion import en_equipo
from traduccion import en_jefes
from traduccion import en_manual
from traduccion import en_mapa
from traduccion import en_preguntas
from traduccion import en_progreso

EN = {}
for _m in (en_aminodex, en_aminomon, en_animaciones, en_combate, en_datos, en_dibujo, en_equipo, en_jefes, en_manual, en_mapa, en_preguntas, en_progreso):
    EN.update(_m.EN)
