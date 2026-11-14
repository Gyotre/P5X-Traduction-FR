@echo off
title Editeur Facile de Traduction P5X
cd /d "%~dp0"
python "04_Launcher_P5X_FR\editeur_traduction.py"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Une erreur est survenue lors de l'ouverture de l'editeur.
    pause
)
