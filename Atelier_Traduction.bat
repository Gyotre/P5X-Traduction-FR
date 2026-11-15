@echo off
title Atelier de traduction P5X
cd /d "%~dp0"
python "03_Atelier_Traduction\traducteur_p5x.py"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Une erreur est survenue lors de l'ouverture de l'atelier.
    pause
)
