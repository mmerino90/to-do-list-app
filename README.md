# To-Do List Appgit clone https://github.com/mmerino90/to-do-list-app.git

to-do-list-app/

Production-ready Flask To-Do application with REST API, WebUI, comprehensive testing, CI/CD automation, and monitoring.# To-Do List App



## FeaturesThis repository contains a refactored, modular Flask To-Do application intended to be

maintainable and production-ready. The app uses an application factory, SQLAlchemy for

- **REST API** under `/api/v1` for CRUD operations on taskspersistence, Pydantic for validation, and includes structured error handling and metrics.

- **Web UI** (index.html, JavaScript) for task management

- **SQLAlchemy ORM** with SQLite (local dev) and PostgreSQL (production on Cloud SQL)## Features

- **Pydantic schemas** for request/response validation

- **Health checks** and Prometheus metrics endpoints- REST API under `/api/v1` for tasks (CRUD)

- **Comprehensive testing** (pytest, 82% coverage)- Web UI served under `/ui`

- **GitHub Actions CI/CD** with automated tests, Docker builds, and Cloud Run deployment- SQLite (SQLAlchemy) for persistence

- **Monitoring** via Prometheus + Grafana (docker-compose)- Pydantic schemas for request validation

- **Structured error handling** and centralized logging- Prometheus metrics endpoint (`/api/v1/metrics`)

- **Production-ready** deployment on Google Cloud Run- Centralized error handlers and structured logging



## Tech Stack## Prerequisites



- **Framework**: Flask 3.0.0, Flask-SQLAlchemy 3.1.1- Python 3.11+

- **Database**: SQLite (development), PostgreSQL (production on Cloud SQL)- Git

- **Testing**: pytest 7.4.3, pytest-cov 4.1.0 (82% coverage achieved)

- **Code Quality**: black 23.11.0, mypy 1.7.0, flake8 6.1.0## Local development (Windows PowerShell)

- **Monitoring**: prometheus-flask-exporter 0.22.4, Grafana

- **Deployment**: Google Cloud Run with Cloud SQL1. Clone the repo and change directory:

- **CI/CD**: GitHub Actions

- **Container**: Docker with Cloud Run buildpack```powershell

git clone https://github.com/mmerino90/to-do-list-app.git

## Prerequisitescd to-do-list-app

```

- Python 3.11+ (or 3.10 for CI matrix)

- Git2. Create and activate a virtual environment:

- Docker & Docker Compose (for local monitoring)

- Google Cloud CLI (for Cloud Run deployment)```powershell

python -m venv .\venv

## Quick Start: Local Development (Windows PowerShell).\venv\Scripts\Activate.ps1

```

```powershell

git clone https://github.com/mmerino90/to-do-list-app.git3. Install project dependencies:

cd to-do-list-app

python -m venv .\venv```powershell

.\venv\Scripts\Activate.ps1pip install -r requirements.txt

pip install -r requirements.txt```

python run.py

```4. Create a `.env` file (do NOT commit this file). Example contents:



Then visit:```env

- **Web UI**: http://127.0.0.1:5000/SECRET_KEY=dev-secret-key

- **API**: http://127.0.0.1:5000/api/v1/tasksFLASK_ENV=development

- **Health**: http://127.0.0.1:5000/api/v1/healthDATABASE_URL=sqlite:///todo.db

LOG_LEVEL=DEBUG

## Testing# DEBUG_METRICS=1

```

All tests use SQLite in-memory database for isolation:

5. Run the app (development):

```powershell

# Run all tests with coverage```powershell

pytest --cov=app --cov-report=html --cov-report=term-missingpython run.py

```

# Run specific tests

pytest tests/test_tasks.py -vOpen the frontend at http://127.0.0.1:5000/ui and the API under `/api/v1`.



# Run single test## Testing

pytest tests/test_tasks.py::test_create_task -v

```Run unit and integration tests and show coverage for the `app` package:



**Current Coverage: 82%** (Target: 70% ✓)```powershell

pytest --cov=app --cov-report=term-missing

## Local Monitoring with Docker Compose```



```powershell## Linting & type checks

docker-compose up

```Run the linters locally:



Access:```powershell

- **Web App**: http://localhost:8080python -m flake8 .

- **Prometheus**: http://localhost:9090 (metrics)python -m mypy app --ignore-missing-imports

- **Grafana**: http://localhost:3000 (admin/admin)```



Configure Grafana:## Continuous Integration

1. Add Prometheus data source: http://prometheus:9090

2. Import or create dashboards for request rate, latency, errorsThis repository includes a GitHub Actions workflow `.github/workflows/ci.yml` that

installs dependencies, runs linters, executes tests and uploads coverage.

## Code Quality

## Project layout

```powershell

# Lint- `run.py` — development entrypoint (calls the application factory)

python -m flake8 .- `app/` — application package (factory, blueprints, models, services, schemas, utils)

python -m mypy app --ignore-missing-imports- `config/` — configuration classes and environment loading

- `static/`, `templates/` — UI assets and templates

# Format- `tests/` — pytest tests

python -m black .

```## Notes



## API Endpoints- Keep secrets out of source control; use `.env` locally and a secrets manager in prod.

- For production deploy behind a WSGI server (gunicorn or waitress) and set `FLASK_ENV=production`.

| Method | Endpoint | Purpose |- If you want stronger deduplication for create requests, consider an idempotency-key pattern.

|--------|----------|---------|

| GET | `/api/v1/tasks` | List all tasks |If you'd like, I can:

| POST | `/api/v1/tasks` | Create task |- Add a `.env.example` documenting required env vars.

| GET | `/api/v1/tasks/<id>` | Get task |- Add a production `wsgi.py` and a Dockerfile.

| PUT | `/api/v1/tasks/<id>` | Update task |- Add CI status badges to this README.

| DELETE | `/api/v1/tasks/<id>` | Delete task |
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/metrics` | Prometheus metrics |
| GET | `/api/v1/ping` | Ping endpoint |

## GitHub Actions CI/CD

### Continuous Integration (.github/workflows/ci.yml)
- Runs on push/PR to `main`
- Tests on Python 3.10 & 3.11
- Fails if coverage < 70%
- Builds Docker image on main push

### Continuous Deployment (.github/workflows/cd.yml)
- Runs after CI passes
- Builds & pushes Docker image to GCR
- Deploys to Google Cloud Run with Cloud SQL

**Current Deployment**: https://github-actions-deployer-570395440561.us-central1.run.app/

## Configuration

Environment variables (set in `.env` or secrets):
- `FLASK_ENV` — development/production
- `SECRET_KEY` — Flask secret
- `LOG_LEVEL` — DEBUG/INFO/WARNING
- `SQLALCHEMY_DATABASE_URI` — (Cloud Run sets this)
- `DATABASE_URL` — (Legacy; dev .env)

Config classes in `config/settings.py`:
- **DevelopmentConfig**: SQLite, debug mode
- **TestingConfig**: In-memory SQLite, isolated tests
- **ProductionConfig**: PostgreSQL from env, hardened

## Project Structure

```
.github/workflows/    → CI/CD pipelines (ci.yml, cd.yml)
app/
  ├── __init__.py     → App factory
  ├── extensions.py   → SQLAlchemy, Prometheus
  ├── api/            → API endpoints (tasks, health, ping, metrics)
  ├── models/         → ORM models (task.py)
  ├── schemas/        → Pydantic schemas (validation)
  ├── services/       → Business logic (task_service.py)
  ├── utils/          → Error handlers
  └── web/            → Web UI routes
config/               → Settings (development, test, production)
tests/                → Pytest tests (conftest, test_*.py)
static/               → CSS/JavaScript assets
templates/            → Jinja2 templates
Dockerfile            → Cloud Run image
Procfile              → Cloud Run buildpack entrypoint
docker-compose.yml    → Local dev + monitoring stack
prometheus.yml        → Prometheus scrape config
requirements.txt      → Python dependencies
run.py                → Development server
```

## Deployment to Cloud Run

### Setup
1. Create Google Cloud project with Cloud Run, Cloud SQL, Container Registry
2. Create PostgreSQL instance on Cloud SQL
3. Export service account key JSON
4. Add GitHub secrets: `GCP_SA_KEY`, `PROD_DATABASE_URL`

### Deploy
Push to `main` branch → GitHub Actions automatically:
- Builds Docker image
- Pushes to Google Container Registry
- Deploys to Cloud Run with Cloud SQL connection
- Verifies `/api/v1/health` endpoint

## Troubleshooting

**Tests fail with "could not translate host name 'db'"**
- Ensure `FLASK_CONFIG=testing` is set before app import in `conftest.py` ✓

**Prometheus not scraping**
- Check `prometheus.yml` target is reachable: `curl http://web:8080/api/v1/metrics`
- View Prometheus UI: http://localhost:9090

**Cloud Run deployment fails**
- Verify secrets `GCP_SA_KEY` and `PROD_DATABASE_URL` are set
- Check service account has Cloud Run Developer + Cloud SQL Client roles
- View logs: `gcloud run services describe <service> --region us-central1`

## Performance & Best Practices

- ✓ Database connection pooling (pool_pre_ping, pool_recycle)
- ✓ Structured logging with file rotation (production)
- ✓ Prometheus metrics with 15s scrape interval
- ✓ Centralized error handlers (consistent JSON responses)
- ✓ Test fixtures with context managers (clean DB state)
- ✓ Environment variables for all secrets (no hardcoded config)

## Requirements Met

| Requirement | Status | Details |
|-------------|--------|---------|
| Code Quality & Testing (70% coverage) | ✅ | 82% coverage, all 10 tests passing, SQLite isolation |
| Continuous Integration | ✅ | `.github/workflows/ci.yml` — tests, coverage check, Docker build |
| Continuous Deployment | ✅ | `.github/workflows/cd.yml` — auto-deploy to Cloud Run after CI |
| Monitoring & Health Checks | ✅ | `/api/v1/health` ✓, `/api/v1/metrics` (Prometheus) ✓, Grafana dashboards |
| Documentation | ✅ | README (you are here) + REPORT.md with architecture & decisions |

## License

MIT License

## Questions?

Open an issue on GitHub or check the REPORT.md for architecture details.
