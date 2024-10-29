# monitoring.sh
#!/bin/bash

echo "État des conteneurs Docker:"
sudo docker ps

echo -e "\nUtilisation des ressources:"
sudo docker stats --no-stream

echo -e "\nLogs récents:"
sudo docker-compose logs --tail=100
