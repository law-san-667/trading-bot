# setup_server.sh
#!/bin/bash
set -e

# Mettre à jour le système
sudo apt-get update
sudo apt-get upgrade -y

# Installer les dépendances nécessaires
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git \
    python3-pip \
    python3-venv \
    nginx \
    certbot \
    python3-certbot-nginx

# Installer Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Installer Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Configurer l'utilisateur actuel pour Docker
sudo usermod -aG docker $USER

# Démarrer et activer Docker
sudo systemctl start docker
sudo systemctl enable docker

# Créer la structure des dossiers
mkdir -p ~/trading-bot/{logs,data}

echo "Configuration de base terminée!"
echo "N'oubliez pas de vous déconnecter et reconnecter pour appliquer les changements de groupe Docker"

