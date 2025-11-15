# To-Do List App

> Production-ready Flask To-Do application with REST API, WebUI, comprehensive testing, CI/CD automation, and cloud deployment.

**Status**: ✅ Production-Ready | **Coverage**: 82.75% (Target: 70%) | **Tests**: 10/10 passing  
**Live**: https://github-actions-deployer-570395440561.us-central1.run.app/  
**Repository**: https://github.com/mmerino90/to-do-list-app  
**Last Updated**: November 15, 2025 - Full monitoring stack implemented

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

### Run with Docker Compose (Full Stack)
```powershell
# Start all services (Flask + PostgreSQL + Prometheus + Grafana)
docker-compose up -d

# Access services:
# • Flask App: http://localhost:8080
# • Prometheus: http://localhost:9090
# • Grafana: http://localhost:3000 (admin/admin)

# Stop services
docker-compose down
```

### Deploy to Production
```powershell
# Push to main branch triggers automatic deployment via GitHub Actions
git push origin main

# Or manually trigger deployment:
# GitHub → Actions → Deploy to Cloud Run → Run workflow
```

---

## 📚 Documentation

All documentation has been organized in the [`/docs`](./docs) folder for clean repository structure.

### Getting Started

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **[REPORT.md](./docs/REPORT.md)** ⭐ | Comprehensive project report | 15 min |
| **[FINAL_PROJECT_REPORT.md](./docs/FINAL_PROJECT_REPORT.md)** | Detailed 5-6 page technical report | 20 min |
| **[MINIMAL_MONITORING_SETUP.md](./docs/MINIMAL_MONITORING_SETUP.md)** | Quick monitoring setup (5 min) | 5 min |

### For Developers

- **[docs/MINIMAL_MONITORING_SETUP.md](./docs/MINIMAL_MONITORING_SETUP.md)** — 5-minute Prometheus + Grafana setup
- **[docs/VISUAL_CONFIG_REFERENCE.md](./docs/VISUAL_CONFIG_REFERENCE.md)** — Complete monitoring configuration guide
- **[docs/CODE_REFACTORING.md](./docs/CODE_REFACTORING.md)** — SOLID principles and improvements

### For Monitoring & Operations

- **[docs/MONITORING.md](./docs/MONITORING.md)** — Comprehensive 790+ line monitoring guide
- **[docs/MONITORING_DATA.md](./docs/MONITORING_DATA.md)** — All metrics and deliverables
- **[docs/grafana-dashboard.json](./docs/grafana-dashboard.json)** — Pre-configured dashboard (6 panels)

### Configuration Files

- **[prometheus.yml](./prometheus.yml)** — Prometheus scrape configuration
- **[docker-compose.yml](./docker-compose.yml)** — Full stack definition
- **[.github/workflows/](./github/workflows/)** — CI/CD pipeline definitions

---

## 🎯 Key Features

- ✅ **REST API** (`/api/v1`) - 7 endpoints for CRUD operations
- ✅ **Web UI** - Task management interface (HTML/CSS/JavaScript)
- ✅ **Database** - PostgreSQL 16 (Cloud SQL production, Docker local)
- ✅ **Testing** - pytest with 82.75% code coverage (10/10 tests passing)
- ✅ **Code Quality** - SOLID principles, 26% code reduction, centralized patterns
- ✅ **Monitoring** - Prometheus + Grafana (6-panel dashboard, real-time metrics)
- ✅ **CI/CD** - GitHub Actions (2-3 minute automated deployment)
- ✅ **Deployment** - Google Cloud Run (serverless, auto-scaling, $11/month)
- ✅ **Observability** - Health checks, metrics endpoint, structured logging
- ✅ **Security** - GitHub Secrets, environment variables, no credentials in code

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

## 🚀 Quick Start

### Option 1: Local Development (Flask Only)

**1. Install Python 3.11+**  
Download from [python.org](https://www.python.org/downloads/)

**2. Create Virtual Environment**
```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Run Application**
```bash
python run.py
```

**5. Access Application**
- Web UI: http://localhost:8080
- API: http://localhost:8080/api/v1/tasks
- Health Check: http://localhost:8080/api/v1/health

**Database**: SQLite (auto-created at `instance/todo.db`)

---

### Option 2: Full Stack with Docker Compose (Recommended)

Includes: Flask app + PostgreSQL + Prometheus + Grafana

**1. Install Docker Desktop**  
Download from [docker.com](https://www.docker.com/products/docker-desktop/)

**2. Start All Services**
```powershell
docker-compose up -d
```

**Wait 30 seconds for all services to start...**

**3. Verify Services**
```powershell
docker-compose ps
```

Expected output:
```
NAME              SERVICE      STATUS
prometheus        prometheus   Up
grafana           grafana      Up
to-do-db          db           Up
to-do-web         web          Up
```

**4. Access Services**

| Service | URL | Credentials |
|---------|-----|-------------|
| **Web UI** | http://localhost:8080 | - |
| **API** | http://localhost:8080/api/v1/tasks | - |
| **Metrics** | http://localhost:8080/api/v1/metrics | - |
| **Prometheus** | http://localhost:9090 | - |
| **Grafana** | http://localhost:3000 | admin / admin |

**5. Import Grafana Dashboard**

1. Open http://localhost:3000 (login: `admin` / `admin`)
2. Go to: **Dashboards** → **Import**
3. Click **Upload JSON file**
4. Select: `docs/grafana-dashboard.json`
5. Click **Import**
6. Dashboard shows 6 panels with real-time metrics

**6. Stop Services**
```powershell
docker-compose down
```

**Need help?** See [`docs/MINIMAL_MONITORING_SETUP.md`](./docs/MINIMAL_MONITORING_SETUP.md)

---

## 📝 Running Tests

### Quick Test

```bash
# Activate virtual environment first
pytest
```

### Complete Test Suite

```bash
# Run all tests with coverage report
pytest --cov=app --cov-report=term-missing

# Expected output:
# ====== 10 passed in 2.15s ======
# Coverage: 82.75%
```

### Test Individual Components

```bash
# Test specific file
pytest tests/test_tasks.py -v

# Test specific function
pytest tests/test_tasks.py::test_create_task -v

# Test with verbose output
pytest -v --tb=short

# Test and show print statements
pytest -s
```

### Generate HTML Coverage Report

```bash
# Generate interactive HTML report
pytest --cov=app --cov-report=html

# Open in browser
# Windows: start htmlcov/index.html
# Mac: open htmlcov/index.html
# Linux: xdg-open htmlcov/index.html
```

### Coverage Requirements

✅ **Minimum**: 70%  
✅ **Current**: 82.75%  
✅ **CI/CD**: Blocks deployment if below 70%

---

## 🌐 Deployment Guide

### Deploy to Google Cloud Run

**Prerequisites**:
1. Google Cloud account ([free tier available](https://cloud.google.com/free))
2. GCP project created
3. Billing enabled
4. GitHub repository

**Step-by-Step Deployment**:

#### 1. Set Up Google Cloud SQL

```bash
# Install gcloud CLI
# Download from: https://cloud.google.com/sdk/docs/install

# Login to GCP
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Create PostgreSQL instance
gcloud sql instances create todo-postgres \
  --database-version=POSTGRES_16 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --root-password=YOUR_SECURE_PASSWORD

# Create database
gcloud sql databases create todo_db --instance=todo-postgres

# Get connection name
gcloud sql instances describe todo-postgres --format="value(connectionName)"
# Save this - you'll need it!
```

#### 2. Configure GitHub Secrets

Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these secrets:

| Secret Name | Value | Where to Get It |
|-------------|-------|----------------|
| `GCP_PROJECT_ID` | Your GCP project ID | GCP Console → Project Info |
| `GCP_SA_KEY` | Service account JSON key | See steps below |
| `PROD_DATABASE_URL` | `postgresql://USER:PASS@/DB?host=/cloudsql/CONNECTION_NAME` | Use your Cloud SQL details |

**Create Service Account Key**:
```bash
# Create service account
gcloud iam service-accounts create github-deployer \
  --display-name="GitHub Actions Deployer"

# Grant permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"

# Create key
gcloud iam service-accounts keys create key.json \
  --iam-account=github-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com

# Copy entire contents of key.json to GCP_SA_KEY secret
# Then delete key.json (never commit this!)
```

#### 3. Update Workflow File

Edit `.github/workflows/cd.yml`:

```yaml
env:
  GCP_PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
  GCP_REGION: us-central1
  SERVICE_NAME: your-app-name  # Change this to your desired name
```

#### 4. Deploy

```bash
# Push to main branch
git add .
git commit -m "feat: Configure Cloud Run deployment"
git push origin main
```

GitHub Actions will automatically:
1. Run tests (must pass)
2. Build Docker image
3. Push to Google Container Registry
4. Deploy to Cloud Run
5. Run health check

**Total time**: 2-3 minutes ⚡

#### 5. Verify Deployment

Check GitHub Actions:
- Go to your repo → **Actions** tab
- Look for green checkmark ✅

Get your URL:
```bash
gcloud run services describe your-app-name \
  --region=us-central1 \
  --format="value(status.url)"
```

Visit the URL to see your live application!

### Deployment Troubleshooting

**Problem**: "Permission denied" error  
**Solution**: Verify service account has `roles/run.admin` and `roles/storage.admin`

**Problem**: "Database connection failed"  
**Solution**: Check `PROD_DATABASE_URL` format and Cloud SQL instance is running

**Problem**: "Build failed" error  
**Solution**: Check `requirements.txt` has all dependencies and tests pass locally

**Problem**: "Service timeout"  
**Solution**: Increase Cloud Run timeout: `--timeout=60s` in deploy command

**More help**: See [`docs/GCP_IAM_SETUP.md`](./docs/GCP_IAM_SETUP.md) and [`docs/FINAL_PROJECT_REPORT.md`](./docs/FINAL_PROJECT_REPORT.md)

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

## 📊 Monitoring Dashboard

### Access Grafana

1. Start full stack: `docker-compose up -d`
2. Open http://localhost:3000 (login: `admin` / `admin`)
3. Import dashboard: `docs/grafana-dashboard.json`

### Dashboard Panels (6 total)

| Panel | Metric | Purpose |
|-------|--------|---------|
| **Request Rate** | Requests per second | Monitor traffic patterns |
| **Total Requests** | Cumulative count | Overall usage |
| **Error Rate** | Errors per second | Detect issues |
| **Response Time p95** | 95th percentile latency | Performance SLA |
| **Avg Response Time** | Mean latency | Overall speed |
| **Requests by Endpoint** | Per-endpoint usage | Identify popular APIs |

### Test Monitoring

Generate test traffic:
```powershell
# Windows PowerShell
for ($i=1; $i -le 50; $i++) {
    Invoke-WebRequest http://localhost:8080/api/v1/tasks
    Start-Sleep -Milliseconds 100
}
```

```bash
# Linux/Mac
for i in {1..50}; do
    curl http://localhost:8080/api/v1/tasks
    sleep 0.1
done
```

Dashboard auto-refreshes every 5 seconds with new data.

**Setup Guide**: [`docs/MINIMAL_MONITORING_SETUP.md`](./docs/MINIMAL_MONITORING_SETUP.md)

---

## 📞 Support & Documentation

### Core Documentation

| Document | Description |
|----------|-------------|
| [`docs/REPORT.md`](./docs/REPORT.md) | 📋 **Comprehensive project summary** - improvements, architecture, results |
| [`docs/FINAL_PROJECT_REPORT.md`](./docs/FINAL_PROJECT_REPORT.md) | 📊 Detailed technical report (6 pages) |
| [`docs/MINIMAL_MONITORING_SETUP.md`](./docs/MINIMAL_MONITORING_SETUP.md) | ⚡ 5-minute monitoring quick start |
| [`docs/VISUAL_CONFIG_REFERENCE.md`](./docs/VISUAL_CONFIG_REFERENCE.md) | 🎨 Visual configuration guide with diagrams |
| [`docs/DOCUMENTATION_INDEX.md`](./docs/DOCUMENTATION_INDEX.md) | 📚 Complete documentation index |

### Setup & Configuration

- **Environment Setup**: See "🚀 Quick Start" section above
- **Docker Setup**: [`docs/MINIMAL_MONITORING_SETUP.md`](./docs/MINIMAL_MONITORING_SETUP.md)
- **Deployment**: [`docs/GCP_IAM_SETUP.md`](./docs/GCP_IAM_SETUP.md)
- **Database Config**: [`docs/DATABASE_CONFIG_GUIDE.md`](./docs/DATABASE_CONFIG_GUIDE.md)

### Troubleshooting

**Issue**: Tests failing locally  
**Solution**: Check [`docs/TEST_DEPLOYMENT_REPORT.md`](./docs/TEST_DEPLOYMENT_REPORT.md)

**Issue**: Deployment errors  
**Solution**: See [`docs/GCP_IAM_SETUP.md`](./docs/GCP_IAM_SETUP.md)

**Issue**: Monitoring not working  
**Solution**: See troubleshooting in [`docs/MINIMAL_MONITORING_SETUP.md`](./docs/MINIMAL_MONITORING_SETUP.md)

**Issue**: Database connection problems  
**Solution**: Check [`docs/DATABASE_CONFIG_GUIDE.md`](./docs/DATABASE_CONFIG_GUIDE.md)

---

## 🎯 Project Status

✅ **Production-Ready**: Live on Google Cloud Run  
✅ **High Quality**: 82.75% test coverage, SOLID principles  
✅ **Fully Automated**: 2-3 minute CI/CD deployment  
✅ **Observable**: Prometheus + Grafana monitoring  
✅ **Well-Documented**: 16+ documentation files  
✅ **Cost-Effective**: ~$11/month infrastructure  

**Live URL**: https://github-actions-deployer-570395440561.us-central1.run.app/

---

## 📄 License

This project is open source and available under the MIT License.

---

**Last Updated**: November 15, 2025 | **Status**: ✅ Production-Ready | **Version**: 1.0
