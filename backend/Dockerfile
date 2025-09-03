# Stage 1: Install dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy only dependency files to leverage Docker cache
COPY poetry.lock pyproject.toml ./

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-root --no-dev

# Stage 2: Build the final image
FROM python:3.11-slim

WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application source code
COPY . .

# The command to run the application is specified in docker-compose.yml
