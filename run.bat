@echo off

set ENV_NAME=portrait_robot
set SCRIPT_NAME=interface_graphique_final.py

echo Verification de l'environnement Conda...
call conda info --envs | findstr /i "\<%ENV_NAME%\>" >nul

if %errorlevel% neq 0 (
    echo Premier lancement detecte ! Creation de l'environnement "%ENV_NAME%"...
    echo Cela peut prendre quelques minutes.
    call conda env create -f environment.yml
    if %errorlevel% neq 0 (
        echo Erreur lors de la creation de l'environnement.
        pause
        exit /b %errorlevel%
    )
) else (
    echo L'environnement "%ENV_NAME%" est deja pret.
)

echo Lancement de l'application...
call conda activate %ENV_NAME%
python %SCRIPT_NAME%

pause