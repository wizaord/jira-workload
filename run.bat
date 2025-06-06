@echo off
SETLOCAL

REM Vérifiez si Python est installé
WHERE python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    ECHO Python 3 n'est pas installé. Veuillez l'installer.
    EXIT /B 1
)

python -m venv .venv
CALL .venv\Scripts\activate

REM Installez les dépendances
pip install -r requirements.txt

REM Configurez PYTHONPATH
SET PYTHONPATH=%CD%;%PYTHONPATH%

REM Exécutez le script Python
ECHO Exécution du script Python window.py...
python src\main\window.py

ECHO Script Python terminé.

ENDLOCAL
