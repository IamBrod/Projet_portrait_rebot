#!/bin/bash

ENV_NAME="portrait_robot"
SCRIPT_NAME="interface_graphique_final.py"

CONDA_BASE=$(conda info --base)
source "$CONDA_BASE/etc/profile.d/conda.sh"

echo "Vérification de l'environnement Conda..."

if conda info --envs | grep -q "^$ENV_NAME "; then
    echo "L'environnement '$ENV_NAME' est déjà prêt."
else
    echo "Premier lancement détecté ! Création de l'environnement '$ENV_NAME'..."
    echo "Cela peut prendre quelques minutes."
    conda env create -f environment_portable.yml
    if [ $? -ne 0 ]; then
        echo "Erreur lors de la création de l'environnement."
        read -p "Appuyez sur une touche pour quitter..."
        exit 1
    fi
fi

echo "Lancement de l'application..."
conda activate $ENV_NAME
python $SCRIPT_NAME
