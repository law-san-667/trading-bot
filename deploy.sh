# deploy.sh
#!/bin/bash
set -e

echo "Déploiement du bot de trading..."

# Mettre à jour le système
sudo apt-get update
sudo apt-get upgrade -y

# Installer les dépendances système
sudo apt-get install -y python3-pip python3-venv docker.io docker-compose git

# Démarrer Docker
sudo systemctl start docker
sudo systemctl enable docker

# Cloner le repo (à commenter après la première exécution)
# git clone votre-repo-url
# cd votre-repo

# Mettre à jour le code
git pull origin main

# Copier le fichier .env si nécessaire
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Fichier .env créé. Veuillez le configurer avec vos paramètres."
    exit 1
fi

# Construire et démarrer les conteneurs
sudo docker-compose up -d --build

echo "Déploiement terminé!"