#!/bin/bash

# Performance Monitoring Script
# This script monitors application performance and provides insights

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

# Check system resources
check_system_resources() {
	print_status "Checking system resources..."

	# CPU usage
	cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
	echo "CPU Usage: ${cpu_usage}%"

	# Memory usage
	memory_info=$(free -h | grep Mem)
	total_memory=$(echo "${memory_info}" | awk '{print $2}')
	used_memory=$(echo "${memory_info}" | awk '{print $3}')
	available_memory=$(echo "${memory_info}" | awk '{print $7}')
	echo "Memory: ${used_memory}/${total_memory} (${available_memory} available)"

	# Disk usage
	disk_usage=$(df -h . | awk 'NR==2{print $5}' | cut -d'%' -f1)
	echo "Disk Usage: ${disk_usage}%"

	# Check thresholds
	if (($(echo "${cpu_usage} > 80" | bc -l))); then
		print_warning "High CPU usage detected"
	fi

	if (($(echo "${disk_usage} > 85" | bc -l))); then
		print_warning "High disk usage detected"
	fi
}

# Check Docker container performance
check_docker_performance() {
	print_status "Checking Docker container performance..."

	if ! docker info >/dev/null 2>&1; then
		print_warning "Docker is not running"
		return
	fi

	# Get container stats
	echo "Container Resource Usage:"
	docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"

	# Check for containers with high resource usage
	high_cpu_containers=$(docker stats --no-stream --format "{{.Container}}\t{{.CPUPerc}}" | awk '$2 > 80% {print $1}')
	if [[ -n ${high_cpu_containers} ]]; then
		print_warning "High CPU usage detected in containers:"
		echo "${high_cpu_containers}"
	fi
}

# Check application health
check_application_health() {
	print_status "Checking application health..."

	# Check backend health
	if curl -f http://localhost:8000/health >/dev/null 2>&1; then
		print_success "Backend API is healthy"

		# Check response time
		response_time=$(curl -w "%{time_total}" -o /dev/null -s http://localhost:8000/health)
		echo "Backend response time: ${response_time}s"

		if (($(echo "${response_time} > 1.0" | bc -l))); then
			print_warning "Slow backend response time detected"
		fi
	else
		print_error "Backend API is not responding"
	fi

	# Check frontend health
	if curl -f http://localhost:3000 >/dev/null 2>&1; then
		print_success "Frontend is healthy"

		# Check response time
		response_time=$(curl -w "%{time_total}" -o /dev/null -s http://localhost:3000)
		echo "Frontend response time: ${response_time}s"

		if (($(echo "${response_time} > 2.0" | bc -l))); then
			print_warning "Slow frontend response time detected"
		fi
	else
		print_error "Frontend is not responding"
	fi

	# Check database health
	if docker-compose exec -T db pg_isready -U "${POSTGRES_USER:-user}" -d "${POSTGRES_DB:-app_db}" >/dev/null 2>&1; then
		print_success "Database is healthy"
	else
		print_error "Database is not responding"
	fi

	# Check Redis health
	if docker-compose exec -T redis redis-cli ping >/dev/null 2>&1; then
		print_success "Redis is healthy"
	else
		print_error "Redis is not responding"
	fi
}

# Check network performance
check_network_performance() {
	print_status "Checking network performance..."

	# Check localhost connectivity
	if ping -c 3 localhost >/dev/null 2>&1; then
		print_success "Localhost connectivity is good"
	else
		print_error "Localhost connectivity issues detected"
	fi

	# Check Docker network
	if docker network ls | grep -q app-network; then
		print_success "Docker network is configured"
	else
		print_warning "Docker network not found"
	fi
}

# Check log files for errors
check_logs() {
	print_status "Checking application logs for errors..."

	# Check recent Docker logs for errors
	error_count=$(docker-compose logs --tail=100 2>&1 | grep -c -i "error\|exception\|failed")

	if [[ ${error_count} -gt 0 ]]; then
		print_warning "Found ${error_count} error messages in recent logs"
		echo "Recent errors:"
		docker-compose logs --tail=50 2>&1 | grep -i "error\|exception\|failed" | tail -5
	else
		print_success "No recent errors found in logs"
	fi
}

# Generate performance report
generate_report() {
	print_status "Generating performance report..."

	report_file="performance_report_$(date +%Y%m%d_%H%M%S).txt"

	{
		echo "Performance Report - $(date)"
		echo "================================"
		echo ""

		echo "System Resources:"
		echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
		echo "Memory: $(free -h | grep Mem | awk '{print $3 "/" $2 " (" $7 " available)"}')"
		echo "Disk Usage: $(df -h . | awk 'NR==2{print $5}')"
		echo ""

		echo "Application Health:"
		echo "Backend: $(curl -f http://localhost:8000/health >/dev/null 2>&1 && echo "Healthy" || echo "Unhealthy")"
		echo "Frontend: $(curl -f http://localhost:3000 >/dev/null 2>&1 && echo "Healthy" || echo "Unhealthy")"
		echo "Database: $(docker-compose exec -T db pg_isready -U "${POSTGRES_USER:-user}" -d "${POSTGRES_DB:-app_db}" >/dev/null 2>&1 && echo "Healthy" || echo "Unhealthy")"
		echo "Redis: $(docker-compose exec -T redis redis-cli ping >/dev/null 2>&1 && echo "Healthy" || echo "Unhealthy")"
		echo ""

		echo "Response Times:"
		echo "Backend: $(curl -w "%{time_total}" -o /dev/null -s http://localhost:8000/health)s"
		echo "Frontend: $(curl -w "%{time_total}" -o /dev/null -s http://localhost:3000)s"
		echo ""

		echo "Recent Errors:"
		docker-compose logs --tail=100 2>&1 | grep -i "error\|exception\|failed" | tail -10
		echo ""

		echo "Container Resource Usage:"
		docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"

	} >"${report_file}"

	print_success "Performance report saved to: ${report_file}"
}

# Main execution
main() {
	echo "📊 Performance Monitoring"
	echo "======================="
	echo ""

	check_system_resources
	echo ""

	check_docker_performance
	echo ""

	check_application_health
	echo ""

	check_network_performance
	echo ""

	check_logs
	echo ""

	generate_report
	echo ""

	echo "✅ Performance monitoring completed!"
	echo ""
	print_status "Recommendations:"
	echo "  - Monitor resource usage regularly"
	echo "  - Set up alerts for high resource usage"
	echo "  - Optimize slow queries and endpoints"
	echo "  - Consider scaling if needed"
	echo "  - Review error logs regularly"
	echo ""
}

# Run main function
main "$@"
