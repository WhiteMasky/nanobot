---
name: docker
description: "Manage Docker containers, images, volumes, and networks. Build, run, debug containers."
metadata: {"nanobot":{"emoji":"🐳","requires":{"bins":["docker"]}}}
---

# Docker Skill

Manage Docker containers, images, and deployments.

## Container Management

### Run Container
```bash
# Basic run
docker run -d --name myapp nginx:latest

# Run with port mapping
docker run -d -p 8080:80 --name web nginx

# Run with volume mount
docker run -d -v /host/data:/container/data --name app myimage

# Run with environment variables
docker run -d -e NODE_ENV=production -e PORT=3000 --name api node:18
```

### Container Operations
```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop container
docker stop myapp

# Start container
docker start myapp

# Restart container
docker restart myapp

# Remove container
docker rm myapp

# Remove all stopped containers
docker container prune -f
```

### View Logs
```bash
# View logs
docker logs myapp

# Follow logs (live)
docker logs -f myapp

# Last N lines
docker logs --tail 100 myapp

# With timestamps
docker logs -t myapp
```

### Execute Commands
```bash
# Run command in running container
docker exec -it myapp bash

# Run specific command
docker exec myapp ls -la /app

# Run as specific user
docker exec -u root myapp bash
```

## Image Management

### List and Pull
```bash
# List images
docker images

# Pull image
docker pull nginx:latest

# Pull specific version
docker pull python:3.11-slim

# Search images
docker search nginx
```

### Build Images
```bash
# Build from Dockerfile
docker build -t myapp:1.0 .

# Build with build args
docker build --build-arg VERSION=1.0 -t myapp .

# Build without cache
docker build --no-cache -t myapp .

# Build from specific Dockerfile
docker build -f Dockerfile.prod -t myapp:prod .
```

### Image Operations
```bash
# Tag image
docker tag myapp:1.0 myapp:latest

# Push to registry
docker push myregistry.com/myapp:1.0

# Remove image
docker rmi myapp:1.0

# Remove dangling images
docker image prune -f

# Remove all unused images
docker image prune -a -f
```

### Save/Load Images
```bash
# Save to tar
docker save -o myapp.tar myapp:1.0

# Load from tar
docker load -i myapp.tar

# Export container
docker export -o container.tar myapp

# Import from tar
docker import container.tar myimage:1.0
```

## Docker Compose

### Basic Commands
```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# List services
docker compose ps

# Rebuild and restart
docker compose up -d --build

# Scale service
docker compose up -d --scale web=3
```

### Cleanup
```bash
# Remove all (containers, networks, images)
docker compose down -v --rmi all

# Remove orphaned containers
docker compose up -d --remove-orphans
```

## Volume Management

```bash
# List volumes
docker volume ls

# Create volume
docker volume create mydata

# Inspect volume
docker volume inspect mydata

# Remove volume
docker volume rm mydata

# Remove unused volumes
docker volume prune -f
```

## Network Management

```bash
# List networks
docker network ls

# Create network
docker network create mynet

# Connect container to network
docker network connect mynet myapp

# Inspect network
docker network inspect mynet

# Remove network
docker network rm mynet
```

## Debugging

### Inspect Container
```bash
# Full inspection
docker inspect myapp

# Get IP address
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' myapp

# Get ports
docker inspect -f '{{json .NetworkSettings.Ports}}' myapp
```

### Resource Usage
```bash
# Container stats
docker stats

# One-time stats
docker stats --no-stream

# Disk usage
docker system df

# Detailed disk usage
docker system df -v
```

### Cleanup
```bash
# Remove everything unused
docker system prune -a -f

# Include volumes
docker system prune -a -f --volumes
```

## Common Patterns

### Development Environment
```bash
docker run -d \
  --name dev \
  -v $(pwd):/app \
  -v node_modules:/app/node_modules \
  -p 3000:3000 \
  -e NODE_ENV=development \
  node:18 tail -f /dev/null
```

### Database Setup
```bash
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=myapp \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:15
```

### Redis Cache
```bash
docker run -d \
  --name redis \
  -p 6379:6379 \
  -v redisdata:/data \
  redis:7 --appendonly yes
```

### Nginx Reverse Proxy
```bash
docker run -d \
  --name nginx \
  -p 80:80 \
  -v ./nginx.conf:/etc/nginx/nginx.conf \
  -v ./sites:/etc/nginx/sites-enabled \
  nginx:latest
```

## Tips

- Use `.dockerignore` to exclude files from build context
- Tag images with version and `latest`
- Use multi-stage builds to reduce image size
- Run containers with `--rm` for temporary tasks
- Use health checks in production
- Store secrets in environment variables or secrets manager
- Use Docker Compose for multi-container apps
