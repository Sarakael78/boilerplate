# Modern Full-Stack Application Template

A production-ready, secure, and scalable full-stack application template built with modern technologies and best practices.

## 🚀 Features

- **Modern Tech Stack**: Next.js 14, FastAPI, PostgreSQL, Redis

- **Security First**: Comprehensive security practices and configurations

- **Production Ready**: Docker, monitoring, logging, and CI/CD

- **Developer Experience**: Hot reloading, code quality tools, and comprehensive documentation

- **Scalable Architecture**: Microservices-ready with proper separation of concerns

- **Real Implementation Examples**: Complete authentication, file upload, and CRUD operations

- **Advanced Features**: Rate limiting, audit logging, error boundaries, and loading states

## 🏗️ Tech Stack

### Frontend

- **Framework**: Next.js 14 with App Router

- **Language**: TypeScript with strict mode

- **Styling**: Tailwind CSS with utility-first approach

- **State Management**: Zustand for client state, React Query for server state

- **UI Components**: **Shadcn UI** with **Radix UI** primitives for a customizable, accessible component system.

- **Authentication**: Complete login/register forms with validation. A specific front-end library isn't stated as secure authentication relies on back-end logic. The front end's role is to send credentials to the back end and securely store the returned JWT (e.g., via HTTP-only cookies).

- **Error Handling**: Comprehensive error boundaries using **React's built-in APIs** for a lightweight solution.

- **Loading States**: Multiple loading variants (spinner, skeleton, overlay) using **React Suspense** and Next.js `loading.js`.

### Backend

- **Framework**: FastAPI with async/await support

- **Language**: Python 3.11 with type hints

- **Dependency Management**: Poetry (exclusive Python package manager)

- **Database**: PostgreSQL 15 with SQLAlchemy ORM

- **Caching**: Redis with connection pooling

- **Authentication**: **`python-jose`** for JWT-based auth and **`passlib`** for bcrypt password hashing.

- **File Upload**: Complete file upload system using **`python-multipart`**, **`Pillow`** for image processing, and **`boto3`** for S3 storage.

- **Rate Limiting**: **`fastapi-limiter`** with Redis-based rate limiting.

- **Audit Logging**: Comprehensive audit trail using **`loguru`** and **`contextvars`**.

### Infrastructure

- **Containerization**: Docker & Docker Compose

- **Reverse Proxy**: Nginx with SSL support

- **Monitoring**: Prometheus & Grafana

- **CI/CD**: GitHub Actions with Trunk

- **Code Quality**: Ruff, Black, ESLint, Prettier

---

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose

- Node.js 18+ (for local development)

- Python 3.11+ (for local development)

- Git

### Installation

1.  **Clone the repository**:

    ```
    git clone <repository-url>
    cd project_template



    ```

2.  **Set up environment**:

    ```
    cp env.example .env
    # Edit .env with your configuration



    ```

3.  **Start development environment**:

    ```
    ./run-dev.sh



    ```

4.  **Access the application**:
    - Frontend: http://localhost

    - Backend API: http://localhost:8000

    - API Documentation: http://localhost:8000/docs

    - Database Admin: http://localhost:8080

    - Monitoring: http://localhost:9090 (Prometheus), http://localhost:3001 (Grafana)

---

## 🛠️ Development

### Available Scripts

```bash
# Development
./run-dev.sh          # Start development environment
./run-prod.sh         # Start production environment

# Code Quality
trunk check           # Run all linting and formatting checks
trunk fmt             # Format code
trunk check --fix     # Fix auto-fixable issues

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
npm install           # Install dependencies
npm run dev           # Start development server
npm run build         # Build for production
npm run lint          # Run linting
```

### Project Structure

```
project_template/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes and endpoints
│   │   ├── core/           # Configuration, security, and core utilities
│   │   ├── db/             # Database setup and session management
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas for validation
│   │   ├── services/       # Business logic and external integrations
│   │   └── utils/          # Utility functions and helpers
│   ├── tests/              # Test files
│   └── pyproject.toml      # Python dependencies and configuration
├── frontend/               # Next.js frontend
│   ├── app/               # Next.js app directory (App Router)
│   ├── components/        # Reusable React components
│   ├── hooks/             # Custom React hooks
│   ├── lib/               # Utilities, API client, and configurations
│   ├── types/             # TypeScript type definitions
│   └── utils/             # Utility functions
├── nginx/                 # Reverse proxy configuration
├── monitoring/            # Prometheus and Grafana configurations
├── docs/                  # Project documentation
├── scripts/               # Utility scripts
├── .cursor/               # Cursor IDE rules and configurations
└── docker-compose.yml     # Development environment orchestration
```

---

## 🔒 Security Features

- **Authentication**: JWT-based with secure token handling and refresh tokens
- **Authorization**: Role-based access control (RBAC)
- **Input Validation**: Comprehensive server-side validation with Pydantic
- **SQL Injection Prevention**: Parameterized queries and ORM usage
- **XSS Protection**: Content Security Policy and input sanitization
- **CSRF Protection**: CSRF tokens for state-changing operations
- **Rate Limiting**: API rate limiting to prevent abuse with Redis backend
- **HTTPS Enforcement**: SSL/TLS configuration for production
- **Secret Management**: Environment-based secret management
- **Container Security**: Non-root users and security options
- **Audit Logging**: Comprehensive audit trail for security and compliance
- **File Upload Security**: File type validation, size limits, and secure storage

---

## 📊 Monitoring & Observability

- **Application Metrics**: Prometheus metrics collection
- **Visualization**: Grafana dashboards
- **Logging**: Structured logging with correlation IDs
- **Health Checks**: Comprehensive health check endpoints
- **Error Tracking**: Error monitoring and alerting
- **Performance Monitoring**: Response time and throughput tracking

---

## 🚀 Deployment

### Development

```bash
./run-dev.sh
```

### Production

```bash
./run-prod.sh
```

### Environment Configuration

The application uses environment variables for configuration. Key variables:

- `SECRET_KEY`: Strong secret key for JWT signing
- `POSTGRES_PASSWORD`: Database password
- `REDIS_PASSWORD`: Redis password (recommended for production)
- `DEBUG`: Debug mode (set to false in production)
- `LOG_LEVEL`: Logging level (INFO, WARNING, ERROR, CRITICAL)

See `env.example` for complete configuration options.

---

## 🧪 Testing

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
# Run E2E tests (if configured)
npm run test:e2e
```

---

## 📚 Documentation

- **API Documentation**: Available at `/docs` when backend is running
- **Architecture Decisions**: See `/docs/architecture/`
- **Setup Guides**: See `/docs/setup/`
- **Deployment Guides**: See `/docs/deployment/`

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run code quality checks: `trunk check --fix`
5. Run tests: `poetry run pytest` (backend) and `npm test` (frontend)
6. Submit a pull request

### Code Quality Standards

- All code must pass `trunk check`
- TypeScript strict mode enabled
- Python type hints required
- Test coverage minimum 80%
- Security best practices enforced

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

- **Issues**: Create an issue in the repository
- **Documentation**: Check `/docs/` directory
- **Security**: Report security issues privately

---

## 🔄 Updates

- **Dependencies**: Regularly updated with security patches
- **Framework Updates**: Follow latest Next.js and FastAPI releases
- **Security Updates**: Automated security scanning in CI/CD
- **Performance**: Continuous performance monitoring and optimization
