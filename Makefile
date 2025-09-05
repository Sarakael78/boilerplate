# Makefile for the boilerplate project

.PHONY: help dev prod lint lint-fix test-backend test-frontend clean install-backend install-frontend

# Default target
help:
@echo "Available targets:"
@echo "  dev           - Run development environment"
@echo "  prod          - Run production environment"
@echo "  lint          - Run linters (trunk check)"
@echo "  lint-fix      - Run linters with auto-fix (trunk check --fix)"
@echo "  test-backend  - Run backend tests"
@echo "  test-frontend - Run frontend tests"
@echo "  install-backend   - Install backend dependencies"
@echo "  install-frontend  - Install frontend dependencies"
@echo "  clean         - Clean up build artifacts and caches"

# Development environment
dev:
@echo "Starting development environment..."
./run-dev.sh

# Production environment
prod:
@echo "Starting production environment..."
./run-prod.sh

# Linting
lint:
@echo "Running linters..."
trunk check

lint-fix:
@echo "Running linters with auto-fix..."
trunk check --fix

# Testing
test-backend:
@echo "Running backend tests..."
cd backend && poetry run pytest

test-frontend:
@echo "Running frontend tests..."
cd frontend && npm test

# Dependencies
install-backend:
@echo "Installing backend dependencies..."
cd backend && poetry install

install-frontend:
@echo "Installing frontend dependencies..."
cd frontend && npm install

# Database migrations
migrate:
@echo "Running database migrations..."
cd backend && poetry run alembic upgrade head

migrate-create:
@echo "Creating new migration..."
cd backend && poetry run alembic revision --autogenerate -m "}(message)"

# Clean up
clean:
@echo "Cleaning up build artifacts and caches..."
rm -rf frontend/.next
rm -rf frontend/node_modules/.cache
rm -rf backend/.pytest_cache
rm -rf backend/__pycache__
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Full setup for new developers
setup: install-backend install-frontend migrate
@echo "Project setup complete!"
@echo "Run 'make dev' to start the development environment."
