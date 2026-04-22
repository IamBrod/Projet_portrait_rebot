@echo off

set ENV_NAME=portrait_robot
set SCRIPT_NAME=interface_graphique_final.py

echo Recherche de Conda sur votre ordinateur...

:: On cherche le script d'activation de Conda dans les dossiers d'installation par defaut
set CONDA_ACTIVATE=
for %%P in (
    "%USERPROFILE%\miniconda3"
    "%USERPROFILE%\anaconda3"
    "%USERPROFILE%\AppData\Local\continuum\miniconda3"
    "%USERPROFILE%\AppData\Local\continuum\anaconda3"
    "C:\ProgramData\Miniconda3"
    "C:\ProgramData\Anaconda3"
    "C:\miniconda3"
    "C:\anaconda3"
) do (
    if exist "%%~P\Scripts\activate.bat" (
        set CONDA_ACTIVATE="%%~P\Scripts\activate.bat"
        goto conda_found
    )
)

:: Si on arrive ici, c'est que Conda n'a pas ete trouve
echo ERREUR : Impossible de trouver Anaconda ou Miniconda sur votre systeme.
echo Assurez-vous que l'un d'eux est installe dans un dossier par defaut.
pause
exit /b 1

:conda_found
echo Conda trouve ! Initialisation...
call %CONDA_ACTIVATE% base

echo Verification de l'environnement %ENV_NAME%...
call conda info --envs | findstr /i "\<%ENV_NAME%\>" >nul

if %errorlevel% neq 0 (
    echo.
    echo --- PREMIER LANCEMENT ---
    echo Creation de l'environnement "%ENV_NAME%"...
    echo Cela peut prendre quelques minutes, veuillez patienter.
    call conda env create -f environment.yml
    if %errorlevel% neq 0 (
        echo Erreur lors de la creation de l'environnement.
        pause
        exit /b %errorlevel%
    )
) else (
    echo L'environnement "%ENV_NAME%" est deja pret.
)

echo.
echo Lancement de l'application...
call conda activate %ENV_NAME%
python %SCRIPT_NAME%

pause
