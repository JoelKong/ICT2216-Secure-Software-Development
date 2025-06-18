#!/bin/bash
set -e

echo "Starting production deployment..."

# Create frontend .env.production from environment variables
echo "Creating frontend .env.production file..."
cat <<EOF > frontend/.env.production
VITE_API_ENDPOINT=${VITE_API_ENDPOINT}
EOF

# Create backend .env.production from environment variables
echo "Creating backend .env.production file..."
cat <<EOF > backend/.env.production
SECRET_KEY=${SECRET_KEY}
JWT_SECRET_KEY=${JWT_SECRET_KEY}
SQLALCHEMY_DATABASE_URI=${SQLALCHEMY_DATABASE_URI}
FRONTEND_ROUTE=${FRONTEND_ROUTE}
EOF

echo "Bringing down existing containers..."
docker-compose -f docker-compose-prod.yml down

echo "Building and starting new containers..."
docker-compose -f docker-compose-prod.yml up -d --build

echo "Deployment finished successfully!"