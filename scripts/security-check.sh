#!/bin/bash

# Security Check Script
# This script performs security checks on the project

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Check for security vulnerabilities in dependencies
check_dependencies() {
	print_status "Checking for security vulnerabilities in dependencies..."

	# Check Python dependencies
	if command -v safety >/dev/null 2>&1; then
		if docker-compose exec -T backend poetry run safety check; then
			print_success "Python dependencies security check passed"
		else
			print_warning "Python dependencies have security vulnerabilities"
		fi
	else
		print_warning "Safety not installed. Install with: pip install safety"
	fi

	# Check Node.js dependencies
	if command -v npm >/dev/null 2>&1; then
		cd frontend
		if npm audit --audit-level=moderate; then
			print_success "Node.js dependencies security check passed"
		else
			print_warning "Node.js dependencies have security vulnerabilities"
		fi
		cd ..
	fi
}

# Check for secrets in code
check_secrets() {
	print_status "Checking for secrets in code..."

	if command -v gitleaks >/dev/null 2>&1; then
		if gitleaks detect --source . --verbose; then
			print_success "No secrets found in code"
		else
			print_error "Secrets found in code! Please review and remove them."
			exit 1
		fi
	else
		print_warning "Gitleaks not installed. Install from: https://github.com/zricethezav/gitleaks"
	fi
}

# Check Docker images for vulnerabilities
check_docker_security() {
	print_status "Checking Docker images for vulnerabilities..."

	if command -v trivy >/dev/null 2>&1; then
		# Check all images used in docker-compose
		images=("postgres:15-alpine" "redis:7-alpine" "nginx:alpine" "prom/prometheus:latest" "grafana/grafana:latest" "adminer:latest")

		for image in "${images[@]}"; do
			print_status "Scanning ${image}..."
			if trivy image --severity HIGH,CRITICAL "${image}"; then
				print_success "No high/critical vulnerabilities found in ${image}"
			else
				print_warning "Vulnerabilities found in ${image}"
			fi
		done
	else
		print_warning "Trivy not installed. Install from: https://github.com/aquasecurity/trivy"
	fi
}

# Check environment variables
check_env_security() {
	print_status "Checking environment variables for security issues..."

	if [[ -f .env ]]; then
		# Check for weak passwords
		if grep -q "password" .env && ! grep -q "POSTGRES_PASSWORD=password" .env; then
			print_warning "Using weak database password. Please use a strong password."
		fi

		# Check for default secret key
		if grep -q "your-super-secret-key-change-this-in-production" .env; then
			print_error "Using default SECRET_KEY. Please change it immediately!"
			exit 1
		fi

		# Check secret key length
		if [[ -f .env ]]; then
			SECRET_KEY=$(grep "^SECRET_KEY=" .env | cut -d'=' -f2)
			if [[ ${#SECRET_KEY} -lt 32 ]]; then
				print_warning "SECRET_KEY is too short. Recommended minimum length: 32 characters"
			fi
		fi

		print_success "Environment variables security check completed"
	else
		print_warning ".env file not found"
	fi
}

# Check SSL/TLS configuration
check_ssl_config() {
	print_status "Checking SSL/TLS configuration..."

	if [[ -d "nginx/ssl" ]]; then
		if [[ -f "nginx/ssl/cert.pem" ]] && [[ -f "nginx/ssl/key.pem" ]]; then
			print_success "SSL certificates found"

			# Check certificate validity
			if command -v openssl >/dev/null 2>&1; then
				if openssl x509 -checkend 86400 -noout -in nginx/ssl/cert.pem; then
					print_success "SSL certificate is valid"
				else
					print_warning "SSL certificate will expire soon or is invalid"
				fi
			fi
		else
			print_warning "SSL certificates not found. HTTPS will not work in production."
		fi
	else
		print_warning "SSL directory not found"
	fi
}

# Check file permissions
check_permissions() {
	print_status "Checking file permissions..."

	# Check for world-writable files
	if find . -type f -perm -002 -not -path "./.git/*" -not -path "./node_modules/*" -not -path "./__pycache__/*" | grep -q .; then
		print_warning "Found world-writable files:"
		find . -type f -perm -002 -not -path "./.git/*" -not -path "./node_modules/*" -not -path "./__pycache__/*"
	else
		print_success "No world-writable files found"
	fi

	# Check for files with execute permission
	if find . -type f -perm -111 -not -path "./.git/*" -not -path "./node_modules/*" -not -path "./__pycache__/*" -not -name "*.sh" | grep -q .; then
		print_warning "Found files with execute permission:"
		find . -type f -perm -111 -not -path "./.git/*" -not -path "./node_modules/*" -not -path "./__pycache__/*" -not -name "*.sh"
	else
		print_success "No unexpected executable files found"
	fi
}

# Main execution
main() {
	echo "🔒 Running Security Checks"
	echo "=========================="
	echo ""

	check_dependencies
	echo ""

	check_secrets
	echo ""

	check_docker_security
	echo ""

	check_env_security
	echo ""

	check_ssl_config
	echo ""

	check_permissions
	echo ""

	echo "✅ Security checks completed!"
	echo ""
	print_status "Recommendations:"
	echo "  - Keep dependencies updated"
	echo "  - Use strong passwords and secret keys"
	echo "  - Enable HTTPS in production"
	echo "  - Regularly scan for vulnerabilities"
	echo "  - Monitor logs for suspicious activity"
	echo ""
}

# Run main function
main "$@"
