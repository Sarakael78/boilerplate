# Poetry Configuration Guide

## Overview

This project uses Poetry exclusively for Python dependency management. Poetry provides a modern, reliable way to manage Python packages and their dependencies.

## Installation

### Installing Poetry

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Verify installation
poetry --version
```

### Poetry Configuration

```bash
# Configure Poetry to create virtual environments in project directory
poetry config virtualenvs.in-project true

# Configure Poetry to use system Python (optional)
poetry config virtualenvs.prefer-active-python true
```

## Project Structure

```text
backend/
├── pyproject.toml          # Poetry configuration and dependencies
├── poetry.lock            # Locked dependency versions (commit this!)
├── app/                   # Application code
└── tests/                 # Test files
```

## Dependency Management

### Adding Dependencies

```bash
# Add production dependency
poetry add fastapi

# Add development dependency
poetry add --group dev pytest

# Add test dependency
poetry add --group test factory-boy

# Add dependency with specific version
poetry add "fastapi>=0.100.0,<0.200.0"
```

### Removing Dependencies

```bash
# Remove dependency
poetry remove package-name

# Remove from specific group
poetry remove --group dev package-name
```

### Updating Dependencies

```bash
# Update all dependencies
poetry update

# Update specific dependency
poetry update fastapi

# Update dependencies in specific group
poetry update --group dev
```

## Poetry Scripts

The project includes several Poetry scripts for common tasks:

### Development Scripts

```bash
# Start development server
poetry run dev

# Start production server
poetry run start

# Run tests
poetry run test

# Run tests with coverage
poetry run test-cov
```

### Code Quality Scripts

```bash
# Run linting
poetry run lint

# Format code
poetry run format

# Check formatting
poetry run format-check

# Run type checking
poetry run type-check

# Run security checks
poetry run security-check
```

### Database Scripts

```bash
# Run migrations
poetry run migrate

# Create new migration
poetry run migrate-create "migration description"
```

## Dependency Groups

### Production Dependencies (`[tool.poetry.dependencies]`)

Core dependencies required for the application to run:

- `fastapi`: Web framework
- `sqlalchemy`: Database ORM
- `redis`: Caching
- `pydantic-settings`: Configuration management
- `structlog`: Structured logging
- `prometheus-client`: Metrics collection
- `sentry-sdk`: Error tracking
- `celery`: Background tasks

### Development Dependencies (`[tool.poetry.group.dev.dependencies]`)

Tools and dependencies for development:

- `pytest`: Testing framework
- `black`: Code formatting
- `ruff`: Linting
- `mypy`: Type checking
- `isort`: Import sorting
- `safety`: Security scanning

### Test Dependencies (`[tool.poetry.group.test.dependencies]`)

Dependencies specifically for testing:

- `pytest-cov`: Coverage reporting
- `pytest-mock`: Mocking utilities
- `factory-boy`: Test data factories

## Tool Configurations

### Ruff Configuration

```toml
[tool.ruff]
line-length = 88
select = ["E", "W", "F", "I", "C", "B"]
ignore = ["E501"]
```

### Black Configuration

```toml
[tool.black]
line-length = 88
```

### MyPy Configuration

```toml
[tool.mypy]
strict = true
warn_return_any = true
disallow_untyped_defs = true
# ... additional strict settings
```

### Pytest Configuration

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "--strict-markers",
    "--cov=app",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=80"
]
```

## Best Practices

### 1. Lock File Management

- **Always commit `poetry.lock`**: This ensures reproducible builds
- **Don't edit lock file manually**: Let Poetry manage it
- **Update lock file regularly**: Run `poetry update` to get security patches

### 2. Dependency Management

- **Use specific versions**: Avoid using `*` or `^` for critical dependencies
- **Group dependencies properly**: Use appropriate groups for different types of dependencies
- **Keep dependencies minimal**: Only add what you actually need

### 3. Virtual Environments

- **Let Poetry manage environments**: Don't create virtual environments manually
- **Use project-local environments**: Configure `virtualenvs.in-project = true`
- **Activate environments**: Use `poetry shell` or `poetry run`

### 4. Security

- **Regular security scans**: Run `poetry run security-check` regularly
- **Update dependencies**: Keep dependencies updated for security patches
- **Review dependencies**: Understand what you're adding to your project

### 5. Development Workflow

- **Use Poetry scripts**: Leverage the defined scripts for common tasks
- **Consistent environment**: Use Poetry to ensure all developers have the same environment
- **Documentation**: Keep dependency documentation up to date

## Troubleshooting

### Common Issues

#### Poetry Not Found

```bash
# Add Poetry to PATH
export PATH="$HOME/.local/bin:$PATH"
```

#### Virtual Environment Issues

```bash
# Remove existing environment
poetry env remove python

# Create new environment
poetry install
```

#### Lock File Conflicts

```bash
# Regenerate lock file
rm poetry.lock
poetry install
```

#### Dependency Resolution Issues

```bash
# Update Poetry
poetry self update

# Clear cache
poetry cache clear --all pypi
```

### Performance Tips

#### Faster Installation

```bash
# Use system packages when possible
poetry config virtualenvs.prefer-active-python true

# Use faster package index
poetry source add --priority=primary pypi https://pypi.org/simple/
```

#### Parallel Installation

```bash
# Install dependencies in parallel (if supported)
poetry install --no-dev --no-interaction
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
- name: Install Poetry
  uses: snok/install-poetry@v1
  with:
    version: latest
    virtualenvs-create: true
    virtualenvs-in-project: true

- name: Install dependencies
  run: poetry install

- name: Run tests
  run: poetry run test

- name: Run linting
  run: poetry run lint

- name: Run type checking
  run: poetry run type-check

- name: Run security checks
  run: poetry run security-check
```

### Docker Integration

```dockerfile
# Install Poetry
RUN pip install poetry

# Copy Poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy application code
COPY . .
```

## Migration from Other Tools

### From pip/requirements.txt

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Initialize Poetry project
poetry init

# Add dependencies from requirements.txt
cat requirements.txt | xargs -I {} poetry add {}

# Remove requirements.txt
rm requirements.txt
```

### From pipenv

```bash
# Export dependencies
pipenv lock --requirements > requirements.txt

# Initialize Poetry
poetry init

# Add dependencies
cat requirements.txt | xargs -I {} poetry add {}

# Remove Pipfile and Pipfile.lock
rm Pipfile Pipfile.lock
```

## Additional Resources

- [Poetry Documentation](https://python-poetry.org/docs/)
- [Poetry GitHub Repository](https://github.com/python-poetry/poetry)
- [Poetry Best Practices](https://python-poetry.org/docs/basic-usage/)
- [Dependency Management Best Practices](https://python-poetry.org/docs/dependency-specification/)
