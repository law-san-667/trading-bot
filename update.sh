# update.sh
#!/bin/bash
set -e

echo "Mise à jour du bot de trading..."

# Arrêter les conteneurs
sudo docker-compose down

# Récupérer les dernières modifications
git pull origin main

# Reconstruire et redémarrer les conteneurs
sudo docker-compose up -d --build

echo "Mise à jour terminée!"