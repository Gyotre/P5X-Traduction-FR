@echo off
title Mise a jour de la traduction P5X
cd /d "%~dp0"
echo.
echo ========================================================
echo   COMPILATION ET MISE A JOUR DU JEU P5X EN COURS...
echo ========================================================
echo.
python "03_Outils_Traduction\convertisseur_json.py"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================================
    echo   ECHEC DE LA COMPILATION - voir le message ci-dessus.
    echo ========================================================
    echo.
    pause
    exit /b 1
)
echo.
echo ========================================================
echo   TERMINE AVEC SUCCES !
echo   Astuce : Si le jeu est ouvert, appuyez sur Alt + R.
echo ========================================================
echo.
pause
