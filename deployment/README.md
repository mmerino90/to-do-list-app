# Deployment Configuration

This folder contains all deployment-related configuration files.

## Files

### `docker-compose.yml`
Full-stack deployment configuration with 4 services:
- **db**: PostgreSQL 16 database
- **web**: Flask application
- **prometheus**: Metrics collection
- **grafana**: Metrics visualization

**Usage:**
```powershell
# From project root
cd deployment
docker-compose up -d

# Or from project root
docker-compose -f deployment/docker-compose.yml up -d
```

### `Dockerfile`
Container image definition for Flask application.

**Build manually:**
```powershell
docker build -t todo-app .
```

### `prometheus.yml`
Prometheus scrape configuration.
- Scrapes Flask app metrics every 15 seconds
- Endpoint: `http://web:8080/api/v1/metrics`

### `Procfile`
**Legacy file for Heroku deployment** (not currently used).

This project deploys to **Google Cloud Run** via GitHub Actions.
The Procfile is kept for reference or alternative Heroku deployments.

**Format:**
```
web: gunicorn -w 4 -b 0.0.0.0:8080 --timeout 120 run:app
```

## Quick Commands

```powershell
# Start all services
cd deployment
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

## Environment Variables

Docker Compose reads from `../.env` (project root).
Make sure `.env` exists before running:

```powershell
# From project root
Copy-Item .env.example .env
# Edit .env with your passwords
```

## Production Deployment

This folder is for **local development only**.

Production deployment uses:
- **GitHub Actions**: `.github/workflows/cd.yml`
- **Google Cloud Run**: Serverless container platform
- **Cloud SQL**: Managed PostgreSQL database

See main [README.md](../README.md) for production deployment guide.
