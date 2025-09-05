#!/bin/bash

# Enhanced Development Startup Script
# This script provides a comprehensive development environment setup

set -euo pipefail # More strict error handling

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
	echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
	echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
	echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
	echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
	if ! docker info >/dev/null 2>&1; then
		print_error "Docker is not running. Please start Docker and try again."
		exit 1
	fi
	print_success "Docker is running"
}

# Function to check if .env file exists and validate it
check_env_file() {
	if [[ ! -f .env ]]; then
		print_warning ".env file not found. Creating from template..."
		if [ ! -f env.example ]; then
			print_error "env.example template not found. Cannot create .env file."
			exit 1
		fi
		cp env.example .env
		print_success "Created .env file from template"
		print_warning "Please review and update the .env file with your configuration"
		print_warning "Especially update SECRET_KEY, POSTGRES_PASSWORD, and other sensitive values"
	else
		print_success ".env file found"
	fi
}

# Function to validate environment variables
validate_env() {
	print_status "Validating environment variables..."

	# Source environment variables safely
	if [[ -f .env ]]; then
		# Use a safer method to source env vars
		set -a
		source .env
		set +a
	fi

	# Check required variables
	required_vars=(
		"POSTGRES_USER"
		"POSTGRES_PASSWORD"
		"POSTGRES_DB"
		"SECRET_KEY"
	)

	missing_vars=()

	for var in "${required_vars[@]}"; do
		if [[ -z "${!var-}" ]]; then
			missing_vars+=("${var}")
		fi
	done

	if [[ ${#missing_vars[@]} -ne 0 ]]; then
		print_error "Missing required environment variables: ${missing_vars[*]}"
		print_warning "Please check your .env file"
		exit 1
	fi

	# Validate SECRET_KEY strength
	if [[ "${#SECRET_KEY}" -lt 32 ]]; then
		print_warning "SECRET_KEY is too short. Recommended minimum length: 32 characters"
	fi

	# Validate password strength
	if [[ "${#POSTGRES_PASSWORD}" -lt 8 ]]; then
		print_warning "POSTGRES_PASSWORD is too short. Recommended minimum length: 8 characters"
	fi

	print_success "Environment variables validated"
}

# Function to check system resources
check_resources() {
	print_status "Checking system resources..."

	# Check available memory
	if command -v free >/dev/null 2>&1; then
		available_memory=$(free -m | awk 'NR==2{printf "%.0f", $7/1024}')
		if [[ "${available_memory}" -lt 2 ]]; then
			print_warning "Low memory available: ${available_memory}GB. Recommended: 4GB+"
		else
			print_success "Memory check passed: ${available_memory}GB available"
		fi
	else
		print_warning "Cannot check memory (free command not available)"
	fi

	# Check available disk space
	if command -v df >/dev/null 2>&1; then
		available_disk=$(df -BG . | awk 'NR==2{print $4}' | sed 's/G//')
		if [[ "${available_disk}" -lt 5 ]]; then
			print_warning "Low disk space: ${available_disk}GB. Recommended: 10GB+"
		else
			print_success "Disk space check passed: ${available_disk}GB available"
		fi
	else
		print_warning "Cannot check disk space (df command not available)"
	fi
}

# Function to setup development environment
setup_dev_environment() {
	print_status "Setting up development environment..."

	# Create necessary directories with proper permissions
	mkdir -p backups logs scripts
	mkdir -p monitoring/grafana/provisioning
	mkdir -p nginx/ssl

	# Set proper permissions
	chmod 755 backups logs scripts
	chmod 700 nginx/ssl # More restrictive for SSL directory

	# Create .gitkeep files to preserve empty directories
	touch backups/.gitkeep logs/.gitkeep scripts/.gitkeep

	print_success "Development environment setup complete"
}

# Function to start services with better error handling
start_services() {
	print_status "Starting development services..."

	# Build and start services
	if ! docker-compose up -d --build; then
		print_error "Failed to start services with docker-compose"
		exit 1
	fi

	# Wait for services to be healthy
	print_status "Waiting for services to be ready..."

	# Wait for database with better error handling
	timeout=60
	print_status "Waiting for database..."
	while [[ "$timeout" -gt 0 ]]; do
		if docker-compose exec -T db pg_isready -U "${POSTGRES_USER:-user}" -d "${POSTGRES_DB:-app_db}" >/dev/null 2>&1; then
			print_success "Database is ready"
			break
		fi
		sleep 1
		timeout=$((timeout - 1))
		if [[ "$timeout" -eq 0 ]]; then
			print_error "Database failed to start within 60 seconds"
			docker-compose logs db
			exit 1
		fi
	done

	# Wait for Redis with better error handling
	timeout=30
	print_status "Waiting for Redis..."
	while [[ "$timeout" -gt 0 ]]; do
		if docker-compose exec -T redis redis-cli ping >/dev/null 2>&1; then
			print_success "Redis is ready"
			break
		fi
		sleep 1
		timeout=$((timeout - 1))
		if [[ "$timeout" -eq 0 ]]; then
			print_error "Redis failed to start within 30 seconds"
			docker-compose logs redis
			exit 1
		fi
	done

	# Wait for backend with better error handling
	timeout=60
	print_status "Waiting for backend API..."
	while [[ "$timeout" -gt 0 ]]; do
		if curl -f http://localhost:8000/health >/dev/null 2>&1; then
			print_success "Backend API is ready"
			break
		fi
		sleep 1
		timeout=$((timeout - 1))
		if [[ "$timeout" -eq 0 ]]; then
			print_error "Backend API failed to start within 60 seconds"
			docker-compose logs backend
			exit 1
		fi
	done

	# Wait for frontend with better error handling
	timeout=60
	print_status "Waiting for frontend..."
	while [[ "$timeout" -gt 0 ]]; do
		if curl -f http://localhost:3000 >/dev/null 2>&1; then
			print_success "Frontend is ready"
			break
		fi
		sleep 1
		timeout=$((timeout - 1))
		if [[ "$timeout" -eq 0 ]]; then
			print_error "Frontend failed to start within 60 seconds"
			docker-compose logs frontend
			exit 1
		fi
	done
}

# Function to run database migrations
run_migrations() {
	print_status "Running database migrations..."

	if docker-compose exec -T backend poetry run alembic upgrade head; then
		print_success "Database migrations completed"
	else
		print_warning "Database migrations failed or no migrations found"
		print_warning "You may need to initialize the database with: docker-compose exec backend poetry run alembic init alembic"
	fi
}

# Function to show service status
show_status() {
	print_status "Service Status:"
	echo ""

	# Check service health
	services=("nginx" "frontend" "backend" "db" "redis" "adminer")

	for service in "${services[@]}"; do
		if docker-compose ps "${service}" | grep -q "Up"; then
			echo -e "  ${GREEN}✓${NC} ${service} is running"
		else
			echo -e "  ${RED}✗${NC} ${service} is not running"
		fi
	done

	echo ""
	print_status "Service URLs:"
	echo "  Frontend:     http://localhost"
	echo "  Backend API:  http://localhost:8000"
	echo "  API Docs:     http://localhost:8000/docs"
	echo "  Database:     http://localhost:8080"
	echo "  Prometheus:   http://localhost:9090"
	echo "  Grafana:      http://localhost:3001"
	echo ""
}

# Function to run code quality checks
run_quality_checks() {
	print_status "Running code quality checks..."

	if command -v trunk >/dev/null 2>&1; then
		if trunk check --fix; then
			print_success "Code quality checks passed"
		else
			print_warning "Code quality checks found issues"
			print_warning "Run 'trunk check' to see detailed issues"
		fi
	else
		print_warning "Trunk not installed. Skipping code quality checks"
		print_warning "Install Trunk: https://docs.trunk.io/getting-started/installation"
	fi
}

# Function to check for security issues
security_check() {
	print_status "Running security checks..."

	# Check for common security issues
	if [[ -f .env ]]; then
		if grep -q "your-super-secret-key-change-this-in-production" .env; then
			print_warning "Using default SECRET_KEY. Please change it in production."
		fi

		if grep -q "password" .env && ! grep -q "POSTGRES_PASSWORD=password" .env; then
			print_warning "Using weak database password. Please use a strong password."
		fi
	fi

	# Check Docker security
	if docker version | grep -q "rootless"; then
		print_success "Docker is running in rootless mode (more secure)"
	else
		print_warning "Docker is running as root. Consider using rootless mode for better security."
	fi
}

# Main execution
main() {
	echo "🚀 Starting Enhanced Development Environment"
	echo "============================================="
	echo ""

	# Pre-flight checks
	check_docker
	check_env_file
	check_resources
	security_check

	# Load environment variables
	if [[ -f .env ]]; then
		set -a
		source .env
		set +a
	fi

	validate_env
	setup_dev_environment
	run_quality_checks

	# Start services
	start_services
	run_migrations

	echo ""
	echo "🎉 Development environment is ready!"
	echo "====================================="
	echo ""

	show_status

	echo ""
	print_status "Useful commands:"
	echo "  View logs:     docker-compose logs -f [service]"
	echo "  Stop services: docker-compose down"
	echo "  Restart:       docker-compose restart [service]"
	echo "  Shell access:  docker-compose exec [service] bash"
	echo "  Security scan: docker-compose exec backend poetry run safety check"
	echo ""
}

# Run main function
main "$@"
