#!/bin/bash
set -e

echo "Starting production deployment..."

echo "Bringing down existing containers..."
docker-compose -f docker-compose-prod.yml down

echo "Building and starting new containers..."

docker-compose --env-file .env.production -f docker-compose-prod.yml up --build -d

echo "Cleaning up dangling images..."
docker image prune -f

echo "Deployment finished successfully!"