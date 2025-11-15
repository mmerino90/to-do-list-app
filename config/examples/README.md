# Configuration Examples

This folder contains example configuration files that are **not currently used** in the main application but kept for reference.

## Files

### `.env.test.example`
Template for testing with PostgreSQL database.

**Purpose**: If you want to run tests against a real PostgreSQL database instead of SQLite.

**Current behavior**: Tests use in-memory SQLite (no setup needed).

**To use this:**
1. Copy to project root: `Copy-Item config/examples/.env.test.example .env.test`
2. Edit `.env.test` with your test database credentials
3. Configure test suite to use PostgreSQL instead of SQLite
4. Add to `.gitignore` (already done)

**Example content:**
```dotenv
POSTGRES_USER=test_user
POSTGRES_PASSWORD=test_password
POSTGRES_DB=test_todo_db
DATABASE_URL=postgresql://test_user:test_password@localhost:5432/test_todo_db
FLASK_ENV=testing
```

**Note**: This is advanced usage. For most cases, SQLite testing is sufficient.

## Why These Are Examples

These files represent **alternative configurations** or **optional features**:
- Not required for basic functionality
- Not actively maintained
- Kept for reference or future use
- Safe to delete if you don't need them

## Active Configuration

For the main application configuration, see:
- `/.env.example` - Main development template
- `/deployment/` - Docker and deployment configs
- `/config/settings.py` - Application settings
