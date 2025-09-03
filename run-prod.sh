#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting the production environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "Docker does not seem to be running, please start it and try again."
  exit 1
fi

# Check for production environment file
if [ ! -f .env.production ]; then
    echo "Production environment file .env.production not found."
    echo "Please create it based on env.example"
    exit 1
fi

# Check for production docker-compose file
if [ ! -f docker-compose.prod.yml ]; then
    echo "Production docker-compose file not found."
    exit 1
fi

echo "Building and starting production containers..."
docker-compose -f docker-compose.prod.yml up --build -d

echo "----------------------------------------"
echo "Production environment is UP and RUNNING."
echo "Application: http://localhost"
echo "Grafana: http://localhost:3001 (admin/admin)"
echo "Prometheus: http://localhost:9090"
echo "----------------------------------------"
echo "To view logs, run: docker-compose -f docker-compose.prod.yml logs -f"
echo "To stop the environment, run: docker-compose -f docker-compose.prod.yml down"
