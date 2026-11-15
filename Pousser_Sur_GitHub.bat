@echo off
title Envoi de la traduction sur GitHub
cd /d "%~dp0"
echo.
echo ========================================================
echo   ENVOI DU PROJET SUR VOTRE REPO GITHUB
echo ========================================================
echo   Depot : https://github.com/Gyotre/P5X-Traduction-FR
echo.

:: 1. Prendre en compte tous les fichiers ajoutes ou modifies
git add -A

:: 2. Demander un message de mise a jour (ou message par defaut)
echo Entrez une description de vos modifications (optionnel) :
set /p MSG="Message [Entree = 'Mise a jour des traductions'] : "
if "%MSG%"=="" set MSG=Mise a jour des traductions

:: 3. Creer le commit si des fichiers ont change
git commit -m "%MSG%" > nul 2>&1

:: 4. Recuperer d'eventuels ajouts distants et envoyer
echo.
echo Envoi des modifications sur GitHub en cours...
git pull --rebase origin main > nul 2>&1
git push origin main

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================================
    echo   ECHEC DE L'ENVOI
    echo.
    echo   Verifiez que vous avez acces au depot GitHub et
    echo   que vous etes bien connecte avec le compte 'Gyotre'.
    echo ========================================================
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================================
echo   SUCCES : TOUTES VOS MODIFICATIONS SONT EN LIGNE !
echo   Lien : https://github.com/Gyotre/P5X-Traduction-FR
echo ========================================================
echo.
pause
