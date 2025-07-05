#!/bin/bash
set -e

echo "Starting production deployment..."

echo "Bringing down existing containers..."
sudo docker-compose -f docker-compose-prod.yml down --remove-orphans

echo "Building and starting new containers..."
sudo docker-compose --env-file .env.production -f docker-compose-prod.yml up --build -d

echo "Cleaning up dangling images..."
sudo docker image prune -f

echo "Deployment finished successfully!"