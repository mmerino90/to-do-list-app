# ---- Base image ----
FROM python:3.11-slim

# Prevents Python from writing .pyc and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Workdir
WORKDIR /app

# System deps (if you use psycopg2 or similar, add build-essential, libpq-dev, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (better caching)
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && pip install -r requirements.txt && pip install gunicorn

# Copy the rest
COPY . /app

# Cloud Run expects the server to listen on $PORT; default to 8080 for local runs
ENV PORT=8080

# Choose your app entrypoint:
# If your Flask app exposes `app = Flask(__name__)` in app/__init__.py, use APP_MODULE=app:app
# If you have a factory `create_app()`, set APP_MODULE='app:create_app()'
ENV APP_MODULE=app:create_app()


# Start with gunicorn, binding to 0.0.0.0:$PORT
CMD exec gunicorn --workers 2 --threads 4 --timeout 120 --bind 0.0.0.0:${PORT} "${APP_MODULE}"
