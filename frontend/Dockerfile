# Stage 1: Install dependencies
FROM node:18-alpine as deps

WORKDIR /app

COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
RUN \
  if [ -f yarn.lock ]; then yarn install --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then yarn global add pnpm && pnpm i --frozen-lockfile; \
  else echo "Lockfile not found." && exit 1; \
  fi

# Stage 2: Build the final image
FROM node:18-alpine

WORKDIR /app

# Copy dependencies and source code
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# The command to run the application is specified in docker-compose.yml
