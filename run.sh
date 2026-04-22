#!/bin/bash

ENV_NAME="portrait_robot"
SCRIPT_NAME="interface_graphique_final.py"

echo "Recherche de Conda sur votre système..."

# Liste des chemins d'installation par défaut de Conda sur Mac/Linux
CONDA_PATHS=(
    "$HOME/miniconda3/etc/profile.d/conda.sh"
    "$HOME/anaconda3/etc/profile.d/conda.sh"
    "$HOME/opt/miniconda3/etc/profile.d/conda.sh"
    "$HOME/opt/anaconda3/etc/profile.d/conda.sh"
    "/opt/miniconda3/etc/profile.d/conda.sh"
    "/opt/anaconda3/etc/profile.d/conda.sh"
    "/usr/local/miniconda3/etc/profile.d/conda.sh"
    "/usr/local/anaconda3/etc/profile.d/conda.sh"
)

CONDA_FOUND=false

# On parcourt les dossiers pour trouver le script d'activation
for path in "${CONDA_PATHS[@]}"; do
    if [ -f "$path" ]; then
        echo "Conda trouvé : $path"
        source "$path"
        CONDA_FOUND=true
        break
    fi
done

# Plan B : Si on n'a pas trouvé dans les dossiers par défaut, mais que la commande conda marche quand même
if [ "$CONDA_FOUND" = false ] && command -v conda &> /dev/null; then
    echo "Conda trouvé dans le PATH système."
    CONDA_BASE=$(conda info --base)
    source "$CONDA_BASE/etc/profile.d/conda.sh"
    CONDA_FOUND=true
fi

# Si on n'a vraiment rien trouvé
if [ "$CONDA_FOUND" = false ]; then
    echo "ERREUR : Impossible de trouver Anaconda ou Miniconda sur votre système."
    echo "Veuillez vérifier votre installation."
    read -p "Appuyez sur Entrée pour quitter..."
    exit 1
fi

echo "Vérification de l'environnement $ENV_NAME..."

# Vérifie si l'environnement existe
if conda info --envs | grep -q "^$ENV_NAME "; then
    echo "L'environnement '$ENV_NAME' est déjà prêt."
else
    echo ""
    echo "--- PREMIER LANCEMENT ---"
    echo "Création de l'environnement '$ENV_NAME'..."
    echo "Cela peut prendre quelques minutes, veuillez patienter."
    mamda env create -f environment_portable.yml
    
    if [ $? -ne 0 ]; then
        echo "Erreur lors de la création de l'environnement."
        read -p "Appuyez sur Entrée pour quitter..."
        exit 1
    fi
fi

echo ""
echo "Lancement de l'application..."
conda activate "$ENV_NAME"
python "$SCRIPT_NAME"

read -p "Appuyez sur Entrée pour quitter..."
