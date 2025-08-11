docker-compose down
docker image prune -f
docker-compose build --no-cache
docker-compose up -d