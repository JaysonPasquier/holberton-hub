#!/bin/bash

cd /var/www/vhosts/holberton_hub

# Fonction pour enregistrer les événements avec horodatage
log_event() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Vérifier si le script est déjà en cours d'exécution
if [ -f check_server.lock ]; then
    PID=$(cat check_server.lock)
    if ps -p $PID > /dev/null; then
        log_event "Une autre instance est déjà en cours d'exécution"
        exit 1
    fi
fi

# Créer le fichier de verrouillage
echo $$ > check_server.lock

# Nettoyer à la sortie
trap 'rm -f check_server.lock' EXIT

# Vérifier l'environnement virtuel
if [ ! -d "venv" ]; then
    log_event "Environnement virtuel manquant. Réinstallation..."
    ./start_env.sh
fi

# Vérifier si les processus existent
if [ ! -f django.pid ] || [ ! -f ngrok.pid ] || ! ps -p $(cat django.pid 2>/dev/null) > /dev/null || ! ps -p $(cat ngrok.pid 2>/dev/null) > /dev/null; then
    log_event "Un ou plusieurs services sont arrêtés. Redémarrage..."
    ./stop_server.sh
    ./start_server.sh
    sleep 10
fi

# Vérifier si Django répond
if ! curl -s http://localhost:8000 > /dev/null; then
    log_event "Django ne répond pas. Redémarrage..."
    ./stop_server.sh
    ./start_server.sh
    sleep 10
fi

# Vérifier si ngrok répond
if ! curl -s http://localhost:4040/api/tunnels > /dev/null; then
    log_event "Ngrok ne répond pas. Redémarrage..."
    ./stop_server.sh
    ./start_server.sh
    sleep 10
fi

# Vérifier si l'URL a changé
CURRENT_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*' | cut -d'"' -f4)
STORED_URL=$(cat current_url.txt 2>/dev/null || echo "")

if [ "$CURRENT_URL" != "$STORED_URL" ]; then
    log_event "Nouvelle URL Ngrok détectée : $CURRENT_URL"
    echo $CURRENT_URL > current_url.txt
fi

# Afficher le statut actuel
log_event "Services en cours d'exécution"
log_event "URL Ngrok actuelle : $CURRENT_URL"

# Vérifier l'espace disque
DISK_USAGE=$(df -h . | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 90 ]; then
    log_event "ATTENTION: Espace disque critique ($DISK_USAGE%)"
fi

# Nettoyer les vieux logs si nécessaire
find . -name "*.log" -size +100M -exec truncate -s 50M {} \;
