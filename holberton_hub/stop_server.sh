#!/bin/bash

cd /var/www/vhosts/holberton_hub

if [ -f django.pid ]; then
    kill $(cat django.pid)
    rm django.pid
fi

if [ -f ngrok.pid ]; then
    kill $(cat ngrok.pid)
    rm ngrok.pid
fi

# Pour être sûr que tout est arrêté
pkill ngrok
pkill -f "python manage.py runserver"

echo "Services stopped"
