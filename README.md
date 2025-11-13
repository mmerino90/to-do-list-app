# To-Do List App

> Production-ready Flask To-Do application with REST API, WebUI, comprehensive testing, CI/CD automation, and cloud deployment.

**Status**: ✅ Production-Ready | **Coverage**: 82.75% (Target: 70%) | **Tests**: 10/10 passing  
**Live**: https://github-actions-deployer-570395440561.us-central1.run.app/  
**Repository**: https://github.com/mmerino90/to-do-list-app  
**Last Updated**: November 13, 2025

---

## 🚀 Quick Start

### Local Development (Windows PowerShell)

```powershell
# Clone repository
git clone https://github.com/mmerino90/to-do-list-app.git
cd to-do-list-app

# Setup
python -m venv .\venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run application
python run.py

# Visit: http://127.0.0.1:5000/
```

### Run Tests
```powershell
pytest --cov=app --cov-report=term-missing
```

### Run Full Monitoring Stack
```bash
docker-compose up
# Flask: http://localhost:5000
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)
```

---

## 📚 Documentation

All documentation has been organized in the [`/docs`](./docs) folder for clean repository structure.

### Getting Started

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **[00_DELIVERABLES_SUMMARY](./docs/00_DELIVERABLES_SUMMARY.md)** | Overview of all deliverables | 5 min |
| **[REPORT](./docs/REPORT.md)** ⭐ | Main technical report (5-6 pages) | 20 min |
| **[DOCUMENTATION_INDEX](./docs/DOCUMENTATION_INDEX.md)** | Complete navigation guide | 10 min |

### For Developers

- **[docs/README.md](./docs/README.md)** — Setup, testing, deployment instructions
- **[docs/TEST_DEPLOYMENT_REPORT.md](./docs/TEST_DEPLOYMENT_REPORT.md)** — Detailed test results and metrics
- **[docs/DEPLOYMENT_PIPELINE.md](./docs/DEPLOYMENT_PIPELINE.md)** — CI/CD pipeline guide

### For Verification

- **[docs/REQUIREMENTS_CHECKLIST.md](./docs/REQUIREMENTS_CHECKLIST.md)** — All requirements verified
- **[docs/DELIVERABLES_VERIFICATION.md](./docs/DELIVERABLES_VERIFICATION.md)** — Detailed verification
- **[docs/PROJECT_COMPLETION.md](./docs/PROJECT_COMPLETION.md)** — Executive summary

### For Operations

- **[docs/GCP_IAM_SETUP.md](./docs/GCP_IAM_SETUP.md)** — Google Cloud configuration
- **[docs/DEPLOYMENT_STATUS.md](./docs/DEPLOYMENT_STATUS.md)** — Current deployment status
- **[docs/URGENT_GCP_IAM_FIX.md](./docs/URGENT_GCP_IAM_FIX.md)** — Quick fixes

---

## 🎯 Key Features

- ✅ **REST API** (`/api/v1`) for CRUD operations on tasks
- ✅ **Web UI** for task management (HTML/CSS/JavaScript)
- ✅ **Database**: SQLite (development), PostgreSQL (production)
- ✅ **Testing**: pytest with 82.75% code coverage
- ✅ **Code Quality**: Black formatting, Flake8 linting, type hints
- ✅ **Monitoring**: Prometheus metrics + Grafana dashboards
- ✅ **CI/CD**: GitHub Actions (automatic testing and deployment)
- ✅ **Deployment**: Google Cloud Run (serverless)
- ✅ **Health Checks**: `/api/v1/health` endpoint
- ✅ **SOLID Principles**: Layered architecture, clean code

---

## 📊 Project Metrics

| Metric | Value | Target |
|--------|-------|--------|
| **Code Coverage** | 82.75% | ≥70% ✅ |
| **Unit Tests** | 10/10 | All passing ✅ |
| **API Endpoints** | 7 | All functional ✅ |
| **CI/CD Workflows** | 2 | Both working ✅ |
| **Documentation** | 14 files | Complete ✅ |
| **Deployment Status** | Live | Operational ✅ |

---

## 🔧 Architecture

### Application Layers
```
┌─────────────────────────────────────────┐
│         Web UI & API Routes              │
│  (Flask Blueprints, Flask-RESTful)      │
├─────────────────────────────────────────┤
│         Business Logic Layer             │
│  (TaskService - CRUD operations)        │
├─────────────────────────────────────────┤
│         Data Access Layer                │
│  (SQLAlchemy ORM, Task Model)           │
├─────────────────────────────────────────┤
│         Configuration Layer              │
│  (Environment-specific settings)        │
├─────────────────────────────────────────┤
│         Database                         │
│  (SQLite / PostgreSQL)                  │
└─────────────────────────────────────────┘
```

### Tech Stack

- **Framework**: Flask 3.0.0 + Flask-SQLAlchemy 3.1.1
- **Database**: PostgreSQL 16 (Cloud SQL, production)
- **Testing**: pytest 7.4.3, pytest-cov 4.1.0
- **Code Quality**: Black 23.11.0, Flake8 6.1.0, mypy 1.7.0
- **Monitoring**: Prometheus 0.22.4, Grafana
- **Deployment**: Docker, Google Cloud Run
- **CI/CD**: GitHub Actions

---

## 🌐 Live Application

**Web UI**: https://github-actions-deployer-570395440561.us-central1.run.app/

**Available Endpoints**:
- 🏠 Web UI: `/` or `/ui`
- 📋 Get Tasks: `GET /api/v1/tasks`
- ➕ Create Task: `POST /api/v1/tasks`
- ✏️ Update Task: `PUT /api/v1/tasks/:id`
- 🗑️ Delete Task: `DELETE /api/v1/tasks/:id`
- 💚 Health: `GET /api/v1/health`
- 📊 Metrics: `GET /api/v1/metrics`
- 🏓 Ping: `GET /api/v1/ping`

---

## ⚙️ Environment Configuration

### Security: Why .env is in .gitignore

**The `.env` file contains sensitive information:**
- Database credentials
- API keys
- Secret keys
- Connection strings

**These should NEVER be committed to version control**, even for a public repository.

**How it works**:
1. `.env` is in `.gitignore` → Never committed to git
2. `.env.example` is in repository → Shows what variables are needed
3. For production: Use GitHub Secrets and Cloud Run environment variables
4. For local development: Copy `.env.example` to `.env` and fill in YOUR values

**Local Setup**:
```bash
# Copy template
cp .env.example .env

# Edit .env with your local values
# (This file will never be committed)
```

**Production Setup**:
- GitHub Actions uses `secrets.PROD_DATABASE_URL`
- Cloud Run environment variables set via secrets
- No credentials in code or git history

### Available Configuration

**`.env.example`** (safe to commit - template only):
```properties
FLASK_APP=run.py
FLASK_ENV=development
LOG_LEVEL=INFO
```

**`.env.test.example`** (safe to commit - test template):
```properties
POSTGRES_USER=test_user
POSTGRES_PASSWORD=test_password
DATABASE_URL=postgresql://test_user:test_password@db:5432/test_todo_db
```

---

## 🚦 CI/CD Pipeline

### Continuous Integration (`.github/workflows/ci.yml`)
Runs on every push and pull request:
- ✅ Tests on Python 3.10 & 3.11
- ✅ Coverage check (minimum 70%)
- ✅ Code quality checks
- ✅ Docker image build

### Continuous Deployment (`.github/workflows/cd.yml`)
Runs on main branch (after CI passes):
- ✅ Build Docker image
- ✅ Push to Google Container Registry
- ✅ Deploy to Google Cloud Run
- ✅ Verify deployment with health check

---

## 📝 Running Tests

```bash
# Run all tests with coverage
pytest --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_tasks.py -v

# Run single test
pytest tests/test_tasks.py::test_create_task -v

# Generate HTML coverage report
pytest --cov=app --cov-report=html
# Open: htmlcov/index.html
```

---

## 🔐 Security Best Practices

✅ **What we do**:
- Never commit `.env` files to git
- Use `.gitignore` to prevent accidental commits
- Use GitHub Secrets for CI/CD credentials
- Use Cloud Run environment variables for production
- Provide `.env.example` as template
- All credentials stored securely

✅ **What you should do**:
- Never share your `.env` file
- Never commit credentials to git
- Use unique passwords for different environments
- Rotate credentials regularly
- Use GitHub Secrets for all sensitive data

---

## 📞 Support

For detailed information, see the [documentation folder](./docs/):

- **Setup help**: See [`docs/README.md`](./docs/README.md)
- **Deployment issues**: See [`docs/GCP_IAM_SETUP.md`](./docs/GCP_IAM_SETUP.md)
- **Test failures**: See [`docs/TEST_DEPLOYMENT_REPORT.md`](./docs/TEST_DEPLOYMENT_REPORT.md)
- **Full navigation**: See [`docs/DOCUMENTATION_INDEX.md`](./docs/DOCUMENTATION_INDEX.md)

---

## 📄 License

This project is open source.

---

**Project Status**: ✅ Production-Ready | **Last Updated**: November 13, 2025
