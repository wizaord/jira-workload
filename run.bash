#!/bin/bash

# Vérifiez si Python est installé
if ! command -v python3 &> /dev/null
then
    echo "Python 3 n'est pas installé. Veuillez l'installer."
    exit 1
fi

# si le venv n'est pas installé, installez-le
if ! python3 -m venv --help &> /dev/null
then
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt

export PYTHONPATH="$(pwd):$PYTHONPATH"

# Exécutez le script Python
echo "Exécution du script Python window.py..."
python3 src/main/window.py

echo "Script Python terminé."
