Project file index — one-line description per file

- run.py: Application entrypoint that creates and runs the Flask app via the application factory.
- requirements.txt: Pinned Python dependencies required to run and develop the project.
- README.md: Project documentation and setup instructions for contributors and users.
- .gitignore: Files and directories excluded from version control (venv, DB, .env, logs, editor files).

- config/settings.py: Environment-backed configuration classes (Development/Testing/Production) and logging setup.

- app/__init__.py: Application factory that initializes extensions, registers blueprints, and creates DB tables.
- app/models/task.py: SQLAlchemy Task model definition and `db = SQLAlchemy()` instance.
- app/schemas/task.py: Pydantic request/response schemas for Task objects (create/update/DB shapes).
- app/services/task_service.py: TaskService encapsulating CRUD business logic and DB operations.
- app/api/tasks.py: API blueprint mounted at /api/v1 providing health, tasks CRUD, and metrics endpoints.
- app/web/routes.py: UI blueprint that renders `templates/index.html` for the web frontend.
- app/utils/error_handlers.py: Custom APIError/NotFoundError classes and centralized error handler registration.

- templates/index.html: Main frontend template — references static CSS/JS and provides the UI markup.

- static/js/tasks.js: Client-side JS moved from the template; fetches and manages tasks via the API.
- static/css/style.css: Main stylesheet for the app's UI components and layout.

- tests/conftest.py: Pytest fixtures to create a test app, test client, and test database setup/teardown.
- tests/test_tasks.py: Integration tests for task API endpoints (CRUD operations).

Notes:
- `app.py` (legacy single-file app) has been removed; the project now uses `run.py` + the `app/` package.
- Keep `.env` out of the repo; add `.env.example` if you want to document environment variables.
