#!/bin/bash

# Aller dans le bon répertoire
cd /var/www/vhosts/holberton_hub

# Tuer les anciennes instances
pkill ngrok
pkill -f "python manage.py runserver"

# Activer l'environnement virtuel
source venv/bin/activate

# Vérifier les dépendances
if ! python -c "import django" &> /dev/null; then
    echo "Django not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Démarrer Django en arrière-plan avec nohup
echo "Starting Django server..."
nohup python manage.py runserver 0.0.0.0:8000 > django.log 2>&1 &
DJANGO_PID=$!

# Attendre que Django démarre
echo "Waiting for Django to start..."
sleep 5
if ! curl -s http://localhost:8000 > /dev/null; then
    echo "Error: Django server is not responding!"
    cat django.log
    exit 1
fi

# Démarrer ngrok en arrière-plan
echo "Starting ngrok..."
nohup ngrok http 8000 > ngrok.log 2>&1 &
NGROK_PID=$!

# Attendre que ngrok démarre
sleep 3

# Sauvegarder les PIDs pour pouvoir arrêter les services plus tard
echo $DJANGO_PID > django.pid
echo $NGROK_PID > ngrok.pid

# Afficher l'URL ngrok
echo "NGrok URL:"
curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*' | cut -d'"' -f4

echo "Services started in background!"
echo "To stop the services, run: ./stop_server.sh"
