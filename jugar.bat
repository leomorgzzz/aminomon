@echo off
rem Abre el juego en Windows con doble clic. Necesita Python 3 (python.org).
chcp 65001 >nul
where py >nul 2>nul
if %errorlevel%==0 (py -3 "%~dp0aminomon.py" %*) else (python "%~dp0aminomon.py" %*)
if errorlevel 1 pause
