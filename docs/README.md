# Project Template Documentation

## Overview

This is a production-ready, secure, and scalable full-stack application template built with modern technologies and best practices. The template provides a solid foundation for building web applications with comprehensive security, monitoring, and development tools.

## Architecture

### Technology Stack

#### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Zustand**: Lightweight state management
- **React Query**: Server state management
- **Axios**: HTTP client

#### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM
- **PostgreSQL**: Primary database
- **Redis**: Caching and session storage
- **Alembic**: Database migrations
- **Poetry**: Exclusive Python dependency management

#### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Reverse proxy
- **Prometheus**: Metrics collection
- **Grafana**: Monitoring dashboards
- **Trunk**: Code quality tools

### Security Features

#### Authentication & Authorization
- JWT-based authentication with secure token handling
- Role-based access control (RBAC)
- Session management with automatic cleanup
- API key management with rotation capabilities
- Multi-factor authentication support

#### Data Protection
- Password hashing with bcrypt (12+ salt rounds)
- Input validation and sanitization
- SQL injection prevention through ORM
- XSS protection with Content Security Policy
- CSRF protection for state-changing operations

#### Infrastructure Security
- Non-root container users
- Security headers (HSTS, CSP, etc.)
- Rate limiting to prevent abuse
- HTTPS enforcement in production
- Secrets management through environment variables

### Performance Optimizations

#### Backend Performance
- Database connection pooling
- Redis caching for frequently accessed data
- Async/await for I/O operations
- Background task processing
- Query optimization with proper indexing

#### Frontend Performance
- Code splitting and lazy loading
- Image optimization with Next.js Image component
- Font optimization and system font usage
- Bundle size optimization
- Service worker for offline functionality

#### Database Performance
- Proper indexing strategy
- Query optimization
- Connection pooling
- Read replicas support
- Database partitioning for large datasets

## Development Workflow

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- Poetry (Python dependency manager)
- Git

### Getting Started

1. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd project_template
   ```

3. **Set up environment**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Start development environment**
   ```bash
   ./run-dev.sh
   ```

4. **Access the application**
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Database Admin: http://localhost:8080
   - Monitoring: http://localhost:9090 (Prometheus), http://localhost:3001 (Grafana)

### Development Commands

```bash
# Development
./run-dev.sh                    # Start development environment
./run-prod.sh                   # Start production environment

# Code Quality
trunk check                     # Run all linting and formatting checks
trunk fmt                       # Format code
trunk check --fix              # Fix auto-fixable issues

# Security
./scripts/security-check.sh    # Run security checks
./scripts/performance-monitor.sh # Monitor performance

# Backend (from backend directory)
poetry install                  # Install dependencies
poetry run pytest              # Run tests
poetry run alembic upgrade head # Run migrations
poetry run dev                 # Start development server
poetry run lint                # Run linting
poetry run format              # Format code
poetry run type-check          # Run type checking
poetry run security-check      # Run security checks

# Frontend (from frontend directory)
npm install                     # Install dependencies
npm run dev                     # Start development server
npm run build                   # Build for production
npm run lint                    # Run linting
```

## Project Structure

```
project_template/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # API routes and endpoints
│   │   ├── core/              # Configuration, security, and core utilities
│   │   ├── db/                # Database setup and session management
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas for validation
│   │   ├── services/          # Business logic and external integrations
│   │   └── utils/             # Utility functions and helpers
│   ├── tests/                 # Test files
│   └── pyproject.toml         # Python dependencies and configuration
├── frontend/                  # Next.js frontend
│   ├── app/                  # Next.js app directory (App Router)
│   ├── components/           # Reusable React components
│   ├── hooks/                # Custom React hooks
│   ├── lib/                  # Utilities, API client, and configurations
│   ├── types/                # TypeScript type definitions
│   └── utils/                # Utility functions
├── nginx/                    # Reverse proxy configuration
├── monitoring/               # Prometheus and Grafana configurations
├── docs/                     # Project documentation
├── scripts/                  # Utility scripts
│   ├── security-check.sh     # Security validation script
│   ├── performance-monitor.sh # Performance monitoring script
│   └── init-db.sql           # Database initialization script
├── .cursor/                  # Cursor IDE rules and configurations
└── docker-compose.yml        # Development environment orchestration
```

## Configuration

### Environment Variables

The application uses environment variables for configuration. Key variables include:

#### Application Configuration
- `APP_NAME`: Application name
- `APP_VERSION`: Application version
- `APP_ENV`: Environment (development, staging, production)
- `DEBUG`: Debug mode (set to false in production)
- `LOG_LEVEL`: Logging level (INFO, WARNING, ERROR, CRITICAL)

#### Database Configuration
- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password (use strong password)
- `POSTGRES_DB`: Database name
- `DATABASE_URL`: Full database connection URL

#### Security Configuration
- `SECRET_KEY`: Strong secret key for JWT signing (minimum 32 characters)
- `JWT_ALGORITHM`: JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token expiration time
- `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token expiration time
- `PASSWORD_SALT_ROUNDS`: Password hashing salt rounds (12+)

#### Redis Configuration
- `REDIS_HOST`: Redis host
- `REDIS_PORT`: Redis port
- `REDIS_PASSWORD`: Redis password (recommended for production)
- `REDIS_URL`: Full Redis connection URL

#### CORS Configuration
- `CORS_ORIGINS`: Allowed origins for CORS
- `CORS_ALLOW_CREDENTIALS`: Allow credentials in CORS
- `CORS_ALLOW_METHODS`: Allowed HTTP methods
- `CORS_ALLOW_HEADERS`: Allowed headers

### Security Best Practices

1. **Environment Variables**
   - Never commit secrets to version control
   - Use strong, unique passwords
   - Rotate secrets regularly
   - Use different secrets for different environments

2. **Database Security**
   - Use strong passwords
   - Enable SSL/TLS connections
   - Implement proper access controls
   - Regular backups with encryption

3. **Application Security**
   - Validate all inputs
   - Use parameterized queries
   - Implement rate limiting
   - Enable security headers
   - Regular security audits

4. **Infrastructure Security**
   - Use non-root containers
   - Regular vulnerability scanning
   - Network segmentation
   - Monitoring and alerting

## Monitoring and Observability

### Metrics Collection
- **Prometheus**: Collects application and system metrics
- **Grafana**: Visualizes metrics and creates dashboards
- **Custom Metrics**: Application-specific metrics for business logic

### Logging
- **Structured Logging**: JSON-formatted logs with correlation IDs
- **Log Levels**: Configurable log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **Log Aggregation**: Centralized log collection and analysis

### Health Checks
- **Application Health**: Health check endpoints for all services
- **Database Health**: Database connectivity and performance checks
- **External Dependencies**: Health checks for external services

### Alerting
- **Performance Alerts**: Alerts for high response times
- **Error Alerts**: Alerts for application errors
- **Resource Alerts**: Alerts for high resource usage

## Deployment

### Development Deployment
```bash
./run-dev.sh
```

### Production Deployment
```bash
./run-prod.sh
```

### Environment-Specific Configurations

#### Development
- Debug mode enabled
- Hot reloading
- Detailed error messages
- Local database and Redis

#### Production
- Debug mode disabled
- Optimized builds
- Error tracking
- Production database and Redis
- SSL/TLS encryption
- CDN for static assets

## Testing

### Backend Testing
```bash
cd backend
poetry run pytest
poetry run pytest --cov=app --cov-report=html
```

### Frontend Testing
```bash
cd frontend
npm test
npm run test:coverage
```

### End-to-End Testing
```bash
npm run test:e2e
```

### Test Coverage Requirements
- Minimum 80% test coverage
- Unit tests for all business logic
- Integration tests for API endpoints
- End-to-end tests for critical user journeys

## Code Quality

### Linting and Formatting
- **Python**: Ruff, Black, isort, mypy
- **TypeScript**: ESLint, Prettier
- **General**: Trunk for unified code quality management

### Poetry Best Practices
- **Dependency Management**: Use Poetry exclusively for Python dependencies
- **Lock File**: Always commit `poetry.lock` for reproducible builds
- **Groups**: Use Poetry groups for development and test dependencies
- **Scripts**: Use Poetry scripts for common commands (`poetry run dev`, `poetry run test`)
- **Virtual Environments**: Poetry manages virtual environments automatically
- **Updates**: Use `poetry update` to update dependencies safely

### Code Review Guidelines
- All code must pass linting checks
- TypeScript strict mode enabled
- Python type hints required
- Security best practices enforced
- Performance considerations reviewed

### Documentation Standards
- API documentation with OpenAPI/Swagger
- Code comments for complex logic
- README files for all major components
- Architecture decision records (ADRs)

## Troubleshooting

### Common Issues

#### Development Environment
1. **Docker not running**
   - Start Docker Desktop
   - Check Docker service status

2. **Port conflicts**
   - Check if ports are already in use
   - Modify port configuration in .env

3. **Database connection issues**
   - Check database container status
   - Verify environment variables
   - Check database logs

4. **Build failures**
   - Clear Docker cache: `docker system prune`
   - Rebuild containers: `docker-compose build --no-cache`

#### Production Issues
1. **High resource usage**
   - Monitor container resource usage
   - Optimize database queries
   - Implement caching strategies

2. **Security vulnerabilities**
   - Run security checks: `./scripts/security-check.sh`
   - Update dependencies
   - Review security configurations

3. **Performance issues**
   - Monitor performance: `./scripts/performance-monitor.sh`
   - Optimize database queries
   - Implement caching
   - Scale horizontally if needed

### Log Analysis
- Check application logs: `docker-compose logs [service]`
- Monitor error rates and patterns
- Use log correlation IDs for debugging
- Set up log aggregation for production

## Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run code quality checks: `trunk check --fix`
5. Run tests: `poetry run pytest` (backend) and `npm test` (frontend)
6. Submit a pull request

### Code Standards
- All code must pass `trunk check`
- TypeScript strict mode enabled
- Python type hints required
- Test coverage minimum 80%
- Security best practices enforced

### Documentation
- Update documentation for new features
- Include API documentation changes
- Update README files as needed
- Create architecture decision records for major changes

## Support and Maintenance

### Regular Maintenance Tasks
- Update dependencies regularly
- Monitor security advisories
- Review and update documentation
- Performance monitoring and optimization
- Security audits and penetration testing

### Support Channels
- GitHub Issues for bug reports
- Documentation for setup and usage
- Security issues should be reported privately

### Updates and Upgrades
- Regular dependency updates with security patches
- Framework updates following release notes
- Database migrations for schema changes
- Backward compatibility considerations

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
