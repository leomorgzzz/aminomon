# Contributing / Cómo ayudar

*English below.*

## Español

Lo que más ayuda, en este orden:

1. **Correcciones de contenido**: un pKa, un pI, una estructura o una
   explicación que esté mal o se entienda mal. Usa el Issue «Contenido
   científico».
2. Ideas para nuevas formas de reconocer estructuras: Issue «Idea».
3. Errores y problemas gráficos: Issue «Bug / Error» con una captura y el tamaño
   de tu terminal.

Para cambiar código:

```bash
python3 pruebas/correr.py   # tienen que pasar todas
```

- Solo biblioteca estándar de Python (más `windows-curses` en Windows).
- Los textos se escriben en español dentro de `tr("…")`; la traducción va en
  `traduccion/en_<módulo>.py` con el texto en español como clave. La prueba
  avisa si falta alguna.
- Los valores vienen de Lehninger (25 °C) y la hidropatía de Kyte-Doolittle.
- Solo símbolos que dibuja la consola de Windows (la prueba lo revisa).
- Commits en español, en pasado y directos, como los que ya hay.

Para publicar una versión: un `git push` **no** llega a Windows ni a macOS.
El instalador y el aviso «Actualizar a…» salen de la última versión en
Releases, que se crea al subir una etiqueta:

```bash
git tag v1.7 && git push origin v1.7   # pruebas en 3 sistemas, compila y publica
```

## English

What helps most, in this order:

1. **Content fixes**: a pKa, pI, structure or explanation that is wrong or
   unclear. Use the "Science content" issue.
2. Ideas for new ways to practice recognizing structures: "Idea".
3. Bugs and display problems: "Bug / Error" with a screenshot and your terminal
   size.

To change code, run `python3 pruebas/correr.py` (all must pass). Standard
library only; texts are written in Spanish inside `tr("…")` and translated in
`traduccion/en_<module>.py`; values come from Lehninger (25 °C); commit
messages are in Spanish, past tense, like the existing ones.

A `git push` does not reach the Windows/macOS builds: push a new tag
(`git tag v1.7 && git push origin v1.7`) to build and publish a release.
