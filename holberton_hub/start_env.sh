#!/bin/bash

# S'assurer que python3-full est installé
if ! dpkg -l | grep -q python3-full; then
    echo "Installing python3-full..."
    apt install python3-full -y
fi

# Supprimer l'ancien environnement virtuel s'il existe
if [ -d "venv" ]; then
    echo "Removing old virtual environment..."
    rm -rf venv
fi

# Créer un nouvel environnement virtuel
echo "Creating fresh virtual environment..."
python3 -m venv venv

# Activer l'environnement virtuel
echo "Activating virtual environment..."
source venv/bin/activate

# Installer/mettre à jour les dépendances
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Virtual environment is ready!"
echo "To deactivate, type 'deactivate'"
