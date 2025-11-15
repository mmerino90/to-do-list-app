# Project Structure

Clean, organized repository structure for the To-Do List application.

## 📁 Root Directory

```
to-do-list-app/
├── 📄 README.md              # Main project documentation
├── 📄 SETUP.md               # Beginner-friendly setup guide
├── 📄 run.py                 # Application entry point
├── 📄 requirements.txt       # Python dependencies
├── 📄 .env.example           # Environment variables template
├── 📄 .env                   # Your local config (not in git)
├── 📄 .gitignore             # Git ignore rules
│
├── 📂 app/                   # Application code
│   ├── __init__.py          # Flask app factory
│   ├── extensions.py        # Flask extensions (SQLAlchemy, etc.)
│   ├── api/                 # REST API endpoints
│   │   ├── health.py        # Health check endpoint
│   │   ├── ping.py          # Simple ping endpoint
│   │   └── tasks.py         # Task CRUD endpoints
│   ├── models/              # Database models
│   │   └── task.py          # Task model
│   ├── schemas/             # Validation schemas
│   │   └── task.py          # Task validation schema
│   ├── services/            # Business logic
│   │   └── task_service.py  # Task service layer
│   ├── utils/               # Utility functions
│   │   ├── constants.py     # Constants and magic numbers
│   │   ├── error_handlers.py # Global error handlers
│   │   └── response_builder.py # HTTP response builder
│   └── web/                 # Web UI routes
│       └── routes.py        # HTML page routes
│
├── 📂 config/                # Configuration
│   ├── settings.py          # App settings by environment
│   └── examples/            # Example/unused configs
│       ├── README.md        # Explains example configs
│       └── .env.test.example # PostgreSQL test config (optional)
│
├── 📂 deployment/            # Deployment configurations
│   ├── README.md            # Deployment documentation
│   ├── docker-compose.yml   # Local full-stack setup
│   ├── Dockerfile           # Container image definition
│   ├── prometheus.yml       # Prometheus scrape config
│   └── Procfile             # Heroku config (legacy, not used)
│
├── 📂 docs/                  # Documentation
│   ├── DOCUMENTATION_INDEX.md        # Complete docs index
│   ├── REPORT.md                     # Comprehensive project report
│   ├── FINAL_PROJECT_REPORT.md       # 6-page technical report
│   ├── MINIMAL_MONITORING_SETUP.md   # Quick monitoring guide
│   ├── VISUAL_CONFIG_REFERENCE.md    # Visual config guide
│   ├── grafana-dashboard.json        # Grafana dashboard export
│   ├── CODE_REFACTORING.md          # SOLID principles applied
│   ├── MONITORING.md                # Full monitoring guide
│   ├── GCP_IAM_SETUP.md             # Cloud deployment setup
│   ├── DATABASE_CONFIG_GUIDE.md     # Database configuration
│   └── [other documentation files]
│
├── 📂 scripts/               # Utility scripts
│   ├── README.md            # Scripts documentation
│   └── setup-grafana.ps1    # Auto-setup Grafana dashboard
│
├── 📂 static/                # Static assets
│   ├── css/
│   │   └── style.css        # Web UI styles
│   └── js/
│       └── tasks.js         # Web UI JavaScript
│
├── 📂 templates/             # HTML templates
│   └── index.html           # Main web UI page
│
├── 📂 tests/                 # Test suite
│   ├── conftest.py          # pytest configuration
│   ├── test_api_errors.py   # API error handling tests
│   ├── test_ping.py         # Ping endpoint tests
│   └── test_tasks.py        # Task CRUD tests
│
├── 📂 .github/               # GitHub configuration
│   └── workflows/           # CI/CD pipelines
│       ├── ci.yml           # Continuous Integration
│       └── cd.yml           # Continuous Deployment
│
└── 📂 [build artifacts]      # Generated (not in git)
    ├── venv/                # Virtual environment
    ├── __pycache__/         # Python cache
    ├── .pytest_cache/       # pytest cache
    ├── .mypy_cache/         # mypy cache
    ├── htmlcov/             # Coverage HTML report
    ├── instance/            # SQLite database (local dev)
    └── .coverage            # Coverage data
```

## 🎯 Key Directories Explained

### `/app` - Application Code
The heart of the application. Follows **clean architecture**:
- **api/** - REST endpoints (presentation layer)
- **services/** - Business logic (service layer)
- **models/** - Database models (data layer)
- **schemas/** - Input validation
- **utils/** - Shared utilities

### `/config` - Configuration Management
- **settings.py** - Environment-based configuration (dev, test, prod)
- **examples/** - Optional/reference configs not actively used

### `/deployment` - Infrastructure as Code
Everything needed to run the app:
- **docker-compose.yml** - Local full-stack setup
- **Dockerfile** - Container image
- **prometheus.yml** - Monitoring configuration
- **Procfile** - Alternative deployment (Heroku, not used)

### `/docs` - Documentation
Comprehensive project documentation (16+ files):
- Setup guides
- Technical reports
- Monitoring guides
- API documentation
- Configuration references

### `/scripts` - Automation Scripts
Utility scripts for development tasks:
- Dashboard setup automation
- Data generation scripts
- Deployment helpers

### `/tests` - Test Suite
pytest-based tests with 82.75% coverage:
- Unit tests for all endpoints
- Integration tests
- Error handling tests

## 🚀 Quick Navigation

**Want to...**

| Goal | Go to |
|------|-------|
| **Understand the project** | `README.md`, `SETUP.md` |
| **Start coding** | `app/` directory |
| **Run locally** | `deployment/docker-compose.yml` |
| **Deploy to cloud** | `.github/workflows/cd.yml` |
| **Read documentation** | `docs/` directory |
| **Run tests** | `tests/` directory |
| **Configure app** | `config/settings.py`, `.env.example` |
| **Add monitoring** | `deployment/prometheus.yml`, `docs/grafana-dashboard.json` |

## 📝 File Naming Conventions

- **Python files**: `snake_case.py`
- **Configuration**: `kebab-case.yml` or `.env`
- **Documentation**: `UPPER_CASE.md`
- **Scripts**: `action-description.ext`

## 🔒 What's in .gitignore

**Never committed:**
- `.env` (secrets)
- `venv/` (virtual environment)
- `__pycache__/` (Python cache)
- `.coverage`, `htmlcov/` (test artifacts)
- `instance/` (local database)

**Always committed:**
- `.env.example` (template)
- Source code (`app/`, `config/`, `tests/`)
- Documentation (`docs/`, `README.md`)
- Deployment configs (`deployment/`)

## 🎨 Why This Structure?

✅ **Separation of Concerns**: Code, config, docs in separate folders  
✅ **Clean Root**: Only essential files at root level  
✅ **Easy Navigation**: Logical grouping by purpose  
✅ **Scalable**: Easy to add new features/docs  
✅ **Professional**: Industry-standard Python project layout  

## 🔄 Comparing to Old Structure

### Before (messy):
```
to-do-list-app/
├── run.py
├── Dockerfile
├── docker-compose.yml
├── prometheus.yml
├── Procfile
├── setup-grafana.ps1
├── .env.test.example
├── app/
├── docs/
├── tests/
└── [20+ other files]
```

### After (organized):
```
to-do-list-app/
├── README.md, SETUP.md
├── run.py, requirements.txt
├── .env.example
├── app/
├── deployment/ ← Deployment files moved here
├── scripts/ ← Scripts moved here
├── config/examples/ ← Unused configs moved here
├── docs/
└── tests/
```

Much cleaner! 🎉
