@echo off
title Launcher Persona 5 The Phantom X FR
cd /d "%~dp0"
python "launcher_p5x.py"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Une erreur est survenue lors de l'execution du launcher.
    pause
)
