#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting the development environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "Docker does not seem to be running, please start it and try again."
  exit 1
fi

# Check for docker-compose.yml
if [ ! -f docker-compose.yml ]; then
    echo "docker-compose.yml not found in the current directory."
    exit 1
fi

echo "Building and starting containers with Docker Compose..."
# Use --build to ensure images are rebuilt if Dockerfile changes
# Use -d to run in detached mode
docker-compose up --build -d

echo "----------------------------------------"
echo "Development environment is UP and RUNNING."
echo "Backend should be available at: http://localhost:8000"
echo "Frontend should be available at: http://localhost:3000"
echo "----------------------------------------"
echo "To view logs, run: docker-compose logs -f"
echo "To stop the environment, run: docker-compose down"
