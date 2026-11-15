@echo off
title Envoi de la traduction sur GitHub
cd /d "%~dp0"
echo.
echo ========================================================
echo   ENVOI DU PROJET SUR VOTRE REPO GITHUB
echo ========================================================
echo   Depot : https://github.com/Gyotre/P5X-Traduction-FR
echo.
echo Envoi des modifications sur la branche 'main'...
echo (Si une fenetre de connexion GitHub s'affiche, validez la connexion)
echo.
git push -u origin main
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================================
    echo   ECHEC DE L'ENVOI
    echo.
    echo   Verifiez que :
    echo   1. Votre depot GitHub existe et que vous y avez acces.
    echo   2. Vous etes bien connecte avec le compte 'Gyotre'.
    echo ========================================================
    echo.
    pause
    exit /b 1
)
echo.
echo ========================================================
echo   SUCCES : TOUT LE PROJET A ETE ENVOYE SUR GITHUB !
echo ========================================================
echo.
pause
