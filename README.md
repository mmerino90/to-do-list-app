git clone https://github.com/mmerino90/to-do-list-app.git
to-do-list-app/
# To-Do List App

This repository contains a refactored, modular Flask To-Do application intended to be
maintainable and production-ready. The app uses an application factory, SQLAlchemy for
persistence, Pydantic for validation, and includes structured error handling and metrics.

## Features

- REST API under `/api/v1` for tasks (CRUD)
- Web UI served under `/ui`
- SQLite (SQLAlchemy) for persistence
- Pydantic schemas for request validation
- Prometheus metrics endpoint (`/api/v1/metrics`)
- Centralized error handlers and structured logging

## Prerequisites

- Python 3.11+
- Git

## Local development (Windows PowerShell)

1. Clone the repo and change directory:

```powershell
git clone https://github.com/mmerino90/to-do-list-app.git
cd to-do-list-app
```

2. Create and activate a virtual environment:

```powershell
python -m venv .\venv
.\venv\Scripts\Activate.ps1
```

3. Install project dependencies:

```powershell
pip install -r requirements.txt
```

4. Create a `.env` file (do NOT commit this file). Example contents:

```env
SECRET_KEY=dev-secret-key
FLASK_ENV=development
DATABASE_URL=sqlite:///todo.db
LOG_LEVEL=DEBUG
# DEBUG_METRICS=1
```

5. Run the app (development):

```powershell
python run.py
```

Open the frontend at http://127.0.0.1:5000/ui and the API under `/api/v1`.

## Testing

Run unit and integration tests and show coverage for the `app` package:

```powershell
pytest --cov=app --cov-report=term-missing
```

## Linting & type checks

Run the linters locally:

```powershell
python -m flake8 .
python -m mypy app --ignore-missing-imports
```

## Continuous Integration

This repository includes a GitHub Actions workflow `.github/workflows/ci.yml` that
installs dependencies, runs linters, executes tests and uploads coverage.

## Project layout

- `run.py` — development entrypoint (calls the application factory)
- `app/` — application package (factory, blueprints, models, services, schemas, utils)
- `config/` — configuration classes and environment loading
- `static/`, `templates/` — UI assets and templates
- `tests/` — pytest tests

## Notes

- Keep secrets out of source control; use `.env` locally and a secrets manager in prod.
- For production deploy behind a WSGI server (gunicorn or waitress) and set `FLASK_ENV=production`.
- If you want stronger deduplication for create requests, consider an idempotency-key pattern.

If you'd like, I can:
- Add a `.env.example` documenting required env vars.
- Add a production `wsgi.py` and a Dockerfile.
- Add CI status badges to this README.
