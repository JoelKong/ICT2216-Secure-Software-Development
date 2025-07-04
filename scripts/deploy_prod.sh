#!/bin/bash
set -e

echo "Starting production deployment..."

# Create dummy certificate files if they don't exist to allow Nginx to start
if [ ! -f "./certbot/conf/live/theleonardodrhere.onthewifi.com/fullchain.pem" ]; then
  echo "Creating dummy certificate for initial Nginx start..."
  sudo mkdir -p ./certbot/conf/live/theleonardodrhere.onthewifi.com
  sudo openssl req -x509 -nodes -newkey rsa:4096 -days 1 \
    -keyout ./certbot/conf/live/theleonardodrhere.onthewifi.com/privkey.pem \
    -out ./certbot/conf/live/theleonardodrhere.onthewifi.com/fullchain.pem \
    -subj "/CN=localhost"
fi

echo "Bringing down existing containers..."
docker-compose -f docker-compose-prod.yml down --remove-orphans

echo "Building and starting new containers..."
docker-compose --env-file .env.production -f docker-compose-prod.yml up --build -d

echo "Cleaning up dangling images..."
docker image prune -f

echo "Deployment finished successfully!"