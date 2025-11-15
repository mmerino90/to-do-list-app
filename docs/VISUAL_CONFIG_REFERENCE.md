# Visual Configuration Reference - Monitoring Setup

This document provides visual representations of all configuration files for the monitoring setup.

---

## 1. Prometheus Configuration (`prometheus.yml`)

### File Location
```
to-do-list-app/
└── prometheus.yml  ← This file
```

### Complete Configuration
```yaml
# Prometheus Configuration for To-Do List Application
# This file tells Prometheus what to monitor and how often

# Global settings apply to all jobs
global:
  # How often to scrape (collect) metrics from targets
  scrape_interval: 15s
  
  # How long to wait before timing out a scrape request
  scrape_timeout: 10s
  
  # How often to evaluate alerting rules (if configured)
  evaluation_interval: 15s

# List of what to monitor
scrape_configs:
  # Job name: appears as 'job' label in metrics
  - job_name: 'flask_app'
    
    # Static targets (not using service discovery)
    static_configs:
      # List of endpoints to scrape
      - targets: 
          # Format: hostname:port
          # 'flask_app' is Docker service name from docker-compose.yml
          - 'flask_app:8080'
    
    # Optional: Path to scrape (defaults to /metrics)
    metrics_path: '/metrics'
    
    # Optional: Scheme (defaults to http)
    scheme: 'http'
```

### Visual Representation
```
┌─────────────────────────────────────────────────────────────┐
│                    Prometheus Configuration                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Global Settings:                                           │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ • Scrape Interval: 15 seconds                       │  │
│  │ • Scrape Timeout: 10 seconds                        │  │
│  │ • Evaluation Interval: 15 seconds                   │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  Scrape Jobs:                                               │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Job: flask_app                                      │  │
│  │   ├─ Target: flask_app:8080                        │  │
│  │   ├─ Path: /metrics                                │  │
│  │   ├─ Scheme: http                                  │  │
│  │   └─ Result: Collects all exposed metrics          │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  Every 15 seconds:                                          │
│  Prometheus → http://flask_app:8080/metrics → Store data   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### What This Configuration Does

**Step-by-Step**:
1. **Every 15 seconds**: Prometheus timer triggers
2. **Sends HTTP GET**: `GET http://flask_app:8080/metrics`
3. **Receives Response**: Text format with all metrics
4. **Parses Metrics**: Extracts metric names, values, labels
5. **Stores in Database**: Time-series database with timestamp
6. **Repeats**: Waits 15 seconds, goes back to step 1

**Example Scrape Request**:
```http
GET /metrics HTTP/1.1
Host: flask_app:8080
User-Agent: Prometheus/2.47.0
Accept: application/openmetrics-text; version=1.0.0
```

**Example Response** (what Prometheus receives):
```
# HELP todo_api_request_count_total Total API requests
# TYPE todo_api_request_count_total counter
todo_api_request_count_total{endpoint="/api/tasks",method="GET",status_code="200"} 150.0

# HELP todo_api_request_duration_seconds API request duration
# TYPE todo_api_request_duration_seconds histogram
todo_api_request_duration_seconds_bucket{endpoint="/api/tasks",method="GET",le="0.005"} 120.0
todo_api_request_duration_seconds_bucket{endpoint="/api/tasks",method="GET",le="0.01"} 145.0
```

---

## 2. Docker Compose Configuration (`docker-compose.yml`)

### Monitoring Services Section

```yaml
# Monitoring Services in Docker Compose
# These services work together to collect and display metrics

services:
  # ====== PROMETHEUS SERVICE ======
  prometheus:
    # Docker image from Docker Hub
    image: prom/prometheus:latest
    
    # Container name (optional, for easier reference)
    container_name: prometheus
    
    # Port mapping: host:container
    ports:
      - "9090:9090"  # Access Prometheus at http://localhost:9090
    
    # Mount configuration file from host into container
    volumes:
      # Format: host_path:container_path:mode
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      # :ro = read-only (Prometheus doesn't modify config)
    
    # Command to run inside container (overrides default)
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'
    
    # Restart policy
    restart: unless-stopped
    
    # Docker network to join
    networks:
      - monitoring

  # ====== GRAFANA SERVICE ======
  grafana:
    # Docker image from Docker Hub
    image: grafana/grafana:latest
    
    # Container name
    container_name: grafana
    
    # Port mapping
    ports:
      - "3000:3000"  # Access Grafana at http://localhost:3000
    
    # Environment variables (configuration)
    environment:
      # Set default admin password
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_SECURITY_ADMIN_USER=admin
      # Allow anonymous access (for demos only!)
      - GF_AUTH_ANONYMOUS_ENABLED=false
      # Set default organization
      - GF_USERS_ALLOW_SIGN_UP=false
    
    # Volumes for persistent data
    volumes:
      # Store Grafana data (dashboards, settings) in named volume
      - grafana-storage:/var/lib/grafana
    
    # Dependencies (start after these services)
    depends_on:
      - prometheus
    
    # Restart policy
    restart: unless-stopped
    
    # Docker network
    networks:
      - monitoring

  # ====== FLASK APP SERVICE (FOR REFERENCE) ======
  flask_app:
    build: .
    container_name: flask_app
    ports:
      - "8080:8080"
    environment:
      - SQLALCHEMY_DATABASE_URI=postgresql://user:password@db:5432/todo_db
    depends_on:
      - db
    networks:
      - monitoring  # Same network as Prometheus!

# ====== NETWORKS ======
networks:
  monitoring:
    driver: bridge  # Default network driver

# ====== VOLUMES ======
volumes:
  grafana-storage:  # Persistent storage for Grafana data
```

### Visual Network Diagram

```
Docker Network: monitoring
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ┌──────────────────┐                                      │
│  │   Flask App      │                                      │
│  │   Port: 8080     │                                      │
│  │   Exposes:       │                                      │
│  │   /metrics       │                                      │
│  └────────┬─────────┘                                      │
│           │                                                 │
│           │ HTTP GET /metrics (every 15s)                  │
│           ▼                                                 │
│  ┌──────────────────┐                                      │
│  │   Prometheus     │                                      │
│  │   Port: 9090     │                                      │
│  │   Stores:        │                                      │
│  │   Time-series DB │                                      │
│  └────────┬─────────┘                                      │
│           │                                                 │
│           │ PromQL queries                                 │
│           ▼                                                 │
│  ┌──────────────────┐                                      │
│  │   Grafana        │                                      │
│  │   Port: 3000     │                                      │
│  │   Displays:      │                                      │
│  │   Dashboards     │                                      │
│  └──────────────────┘                                      │
│           ▲                                                 │
│           │                                                 │
└───────────┼─────────────────────────────────────────────────┘
            │
            │ Access via browser
            │ http://localhost:3000
            │
     ┌──────┴──────┐
     │   Your PC   │
     │   Browser   │
     └─────────────┘
```

### Port Mapping Explanation

```
Host (Your PC)              Docker Container
┌─────────────┐             ┌─────────────┐
│             │             │             │
│ Port 8080   │ ◄─────────► │ Port 8080   │  Flask App
│             │             │             │
│ Port 9090   │ ◄─────────► │ Port 9090   │  Prometheus
│             │             │             │
│ Port 3000   │ ◄─────────► │ Port 3000   │  Grafana
│             │             │             │
└─────────────┘             └─────────────┘

Format: "host_port:container_port"
- host_port: What you access from your browser
- container_port: What the app listens on inside Docker
```

---

## 3. Flask Metrics Configuration (`app/__init__.py`)

### Metrics Instrumentation Code

```python
from flask import Flask
from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY
import time

# ====== METRIC DEFINITIONS ======

# Counter: Monotonically increasing value (resets on restart)
REQUEST_COUNT = Counter(
    name='todo_api_request_count',
    documentation='Total number of API requests',
    labelnames=['method', 'endpoint', 'status_code']
)

# Histogram: Distribution of values (response times)
REQUEST_DURATION = Histogram(
    name='todo_api_request_duration_seconds',
    documentation='API request duration in seconds',
    labelnames=['method', 'endpoint'],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)
)

# Counter: Track errors
ERROR_COUNT = Counter(
    name='todo_api_errors',
    documentation='Total number of API errors',
    labelnames=['method', 'endpoint', 'error_type']
)

# Gauge: Value that can go up or down (current task count)
TASK_COUNT = Gauge(
    name='todo_tasks',
    documentation='Current number of tasks',
    labelnames=['status']
)

def create_app():
    app = Flask(__name__)
    
    # ====== METRICS ENDPOINT ======
    @app.route('/metrics')
    def metrics():
        """
        Expose metrics in Prometheus format.
        This endpoint is scraped by Prometheus every 15 seconds.
        """
        return generate_latest(REGISTRY), 200, {
            'Content-Type': 'text/plain; charset=utf-8'
        }
    
    # ====== BEFORE REQUEST (Track Start Time) ======
    @app.before_request
    def before_request():
        """Record start time for each request"""
        from flask import g
        g.start_time = time.time()
    
    # ====== AFTER REQUEST (Record Metrics) ======
    @app.after_request
    def after_request(response):
        """
        After each request, record metrics.
        This runs after the request is processed but before sending response.
        """
        from flask import request, g
        
        # Calculate request duration
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            
            # Record duration in histogram
            REQUEST_DURATION.labels(
                method=request.method,
                endpoint=request.endpoint or 'unknown'
            ).observe(duration)
        
        # Increment request counter
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.endpoint or 'unknown',
            status_code=response.status_code
        ).inc()
        
        # Track errors (4xx and 5xx status codes)
        if response.status_code >= 400:
            error_type = '4xx' if response.status_code < 500 else '5xx'
            ERROR_COUNT.labels(
                method=request.method,
                endpoint=request.endpoint or 'unknown',
                error_type=error_type
            ).inc()
        
        return response
    
    # ====== UPDATE TASK COUNT (Example) ======
    def update_task_metrics():
        """
        Update task count gauge.
        Call this after creating/updating/deleting tasks.
        """
        from app.models.task import Task
        
        # Count pending tasks
        pending_count = Task.query.filter_by(status='pending').count()
        TASK_COUNT.labels(status='pending').set(pending_count)
        
        # Count completed tasks
        completed_count = Task.query.filter_by(status='completed').count()
        TASK_COUNT.labels(status='completed').set(completed_count)
    
    return app
```

### Visual Flow Diagram

```
Request Flow with Metrics:

1. Client Request
   │
   ▼
┌──────────────────────┐
│ @app.before_request  │  ← Record start time (g.start_time)
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Process Request      │  ← Your route handler (e.g., get_tasks())
│ (Route Handler)      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ @app.after_request   │  ← Record metrics:
│                      │    • Calculate duration
│                      │    • Increment REQUEST_COUNT
│                      │    • Observe REQUEST_DURATION
│                      │    • Track errors if status >= 400
└──────────┬───────────┘
           │
           ▼
   Response to Client


Metrics Endpoints:
┌──────────────────────┐
│ GET /metrics         │  ← Prometheus scrapes this
│                      │    Returns all metrics in text format
│ Response:            │
│ todo_api_request_... │
│ todo_api_request_... │
│ todo_tasks_total{... │
└──────────────────────┘
```

### Metric Types Explained

```
┌────────────────────────────────────────────────────────────┐
│                    METRIC TYPES                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ 1. COUNTER (Monotonically Increasing)                     │
│    ┌─────────────────────────────────────────────────┐   │
│    │  Value can only increase (or reset on restart)  │   │
│    │  Example: Total requests                        │   │
│    │                                                  │   │
│    │  Time: 0s   10s   20s   30s   40s              │   │
│    │  Value: 0 → 5 → 12 → 18 → 25                   │   │
│    │                              ╱                   │   │
│    │                          ╱                       │   │
│    │                      ╱                           │   │
│    │                  ╱                               │   │
│    │              ╱                                   │   │
│    │  ────────────────────────────────────────       │   │
│    └─────────────────────────────────────────────────┘   │
│                                                            │
│ 2. GAUGE (Can Go Up or Down)                              │
│    ┌─────────────────────────────────────────────────┐   │
│    │  Value can increase or decrease                 │   │
│    │  Example: Current task count                    │   │
│    │                                                  │   │
│    │  Time: 0s   10s   20s   30s   40s              │   │
│    │  Value: 5 → 8 → 6 → 10 → 7                     │   │
│    │          ╱╲    ╱╲                               │   │
│    │         ╱  ╲  ╱  ╲                              │   │
│    │        ╱    ╲╱    ╲╱╲                           │   │
│    │  ─────────────────────────────────────────      │   │
│    └─────────────────────────────────────────────────┘   │
│                                                            │
│ 3. HISTOGRAM (Distribution of Values)                     │
│    ┌─────────────────────────────────────────────────┐   │
│    │  Tracks distribution of values in buckets       │   │
│    │  Example: Response time distribution            │   │
│    │                                                  │   │
│    │  Bucket     Count                               │   │
│    │  < 0.01s    ████████████ 120                    │   │
│    │  < 0.05s    ████████ 80                         │   │
│    │  < 0.1s     ████ 40                             │   │
│    │  < 0.5s     ██ 20                               │   │
│    │  < 1.0s     █ 5                                 │   │
│    │                                                  │   │
│    │  Enables: p50, p95, p99 calculations            │   │
│    └─────────────────────────────────────────────────┘   │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 4. Grafana Dashboard JSON Structure

### Dashboard File: `docs/grafana-dashboard.json`

The dashboard JSON is large (~500 lines), but here's the structure:

```json
{
  "dashboard": {
    "title": "To-Do List API Monitoring",
    "uid": "todo-api-monitoring",
    "tags": ["flask", "api", "monitoring"],
    "timezone": "browser",
    "refresh": "5s",
    
    "panels": [
      {
        "id": 1,
        "title": "Request Rate",
        "type": "timeseries",
        "targets": [
          {
            "expr": "rate(todo_api_request_count_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "id": 2,
        "title": "Total Requests",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(todo_api_request_count_total)"
          }
        ]
      }
      // ... 5 more panels
    ]
  }
}
```

### Panel Configuration Visual

```
┌──────────────────────────────────────────────────────────────┐
│                    Panel Configuration                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Panel ID: 1                                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Title: Request Rate                                    │ │
│  │ Type: Time Series (line graph)                        │ │
│  │                                                        │ │
│  │ Query (PromQL):                                       │ │
│  │ ┌────────────────────────────────────────────────┐   │ │
│  │ │ rate(todo_api_request_count_total[5m])         │   │ │
│  │ └────────────────────────────────────────────────┘   │ │
│  │                                                        │ │
│  │ What this query does:                                 │ │
│  │ • Takes todo_api_request_count_total metric          │ │
│  │ • Calculates rate over 5 minutes                     │ │
│  │ • Result: Requests per second                        │ │
│  │                                                        │ │
│  │ Legend: {{method}} {{endpoint}}                       │ │
│  │ • Shows: "GET /api/tasks", "POST /api/tasks", etc.   │ │
│  │                                                        │ │
│  │ Visualization:                                         │ │
│  │   ┌────────────────────────────────────────────┐     │ │
│  │   │                        ╱╲                  │     │ │
│  │   │                  ╱╲   ╱  ╲                 │     │ │
│  │   │            ╱╲   ╱  ╲_╱    ╲                │     │ │
│  │   │      _____╱  ╲_╱            ╲              │     │ │
│  │   │                                            │     │ │
│  │   │  0 ──────────────────────────────────────  │     │ │
│  │   │      00:00  01:00  02:00  03:00  04:00    │     │ │
│  │   └────────────────────────────────────────────┘     │ │
│  └────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### PromQL Query Examples

```
┌──────────────────────────────────────────────────────────────┐
│                  PromQL Query Examples                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 1. Request Rate (req/sec over 5 minutes)                    │
│    rate(todo_api_request_count_total[5m])                   │
│    ↓                                                         │
│    GET /api/tasks: 0.5 req/s                                │
│    POST /api/tasks: 0.2 req/s                               │
│                                                              │
│ 2. Total Requests (all time)                                │
│    sum(todo_api_request_count_total)                        │
│    ↓                                                         │
│    1,247 requests                                            │
│                                                              │
│ 3. Error Rate (errors/sec over 5 minutes)                   │
│    rate(todo_api_errors_total[5m])                          │
│    ↓                                                         │
│    0.002 errors/s                                            │
│                                                              │
│ 4. Response Time p95 (95th percentile)                      │
│    histogram_quantile(0.95,                                 │
│      rate(todo_api_request_duration_seconds_bucket[5m]))    │
│    ↓                                                         │
│    45ms (95% of requests faster than this)                  │
│                                                              │
│ 5. Average Response Time                                     │
│    rate(todo_api_request_duration_seconds_sum[5m]) /        │
│    rate(todo_api_request_duration_seconds_count[5m])        │
│    ↓                                                         │
│    28ms average                                              │
│                                                              │
│ 6. Current Task Count by Status                             │
│    todo_tasks_total                                          │
│    ↓                                                         │
│    {status="pending"}: 25                                    │
│    {status="completed"}: 43                                  │
│                                                              │
│ 7. Requests per Endpoint (all time)                         │
│    sum by (endpoint) (todo_api_request_count_total)         │
│    ↓                                                         │
│    /api/tasks: 856                                           │
│    /api/health: 25                                           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 5. Complete System Diagram

```
┌───────────────────────────────────────────────────────────────────────┐
│                     COMPLETE MONITORING SYSTEM                        │
└───────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ 1. USER INTERACTION                                                  │
│                                                                      │
│     User Browser  ─────── HTTP Request ─────► Flask App             │
│     (Port 8080)                                (Port 8080)           │
│                                                                      │
│     Examples:                                                        │
│     GET  http://localhost:8080/api/tasks                            │
│     POST http://localhost:8080/api/tasks                            │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 2. FLASK APP (Metrics Instrumentation)                              │
│                                                                      │
│     @app.before_request   ← Record start time                       │
│     @app.route('/api/...')  ← Process request                       │
│     @app.after_request    ← Record metrics:                         │
│                              • REQUEST_COUNT.inc()                   │
│                              • REQUEST_DURATION.observe()            │
│                              • ERROR_COUNT.inc() (if error)          │
│                                                                      │
│     /metrics endpoint     ← Exposes all metrics in Prometheus format│
└─────────────────────────────────────────────────────────────────────┘
                                │
                                │ Every 15 seconds
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 3. PROMETHEUS (Metrics Collection)                                  │
│    (Port 9090)                                                       │
│                                                                      │
│     Configuration (prometheus.yml):                                 │
│     ┌─────────────────────────────────────────────────────────┐    │
│     │ scrape_interval: 15s                                    │    │
│     │ targets: ['flask_app:8080']                             │    │
│     └─────────────────────────────────────────────────────────┘    │
│                                                                      │
│     Actions:                                                         │
│     1. HTTP GET http://flask_app:8080/metrics                       │
│     2. Parse response (metric names, values, labels)                │
│     3. Store in time-series database with timestamp                 │
│     4. Repeat every 15 seconds                                      │
│                                                                      │
│     Database:                                                        │
│     ┌────────────────────────────────────────────────────────┐     │
│     │ Time       │ Metric                      │ Value        │     │
│     ├────────────────────────────────────────────────────────┤     │
│     │ 12:00:00   │ request_count{...}          │ 100         │     │
│     │ 12:00:15   │ request_count{...}          │ 105         │     │
│     │ 12:00:30   │ request_count{...}          │ 112         │     │
│     │ ...        │ ...                         │ ...         │     │
│     └────────────────────────────────────────────────────────┘     │
│                                                                      │
│     Web UI: http://localhost:9090                                   │
│     • View raw metrics                                              │
│     • Execute PromQL queries                                        │
│     • Check target status                                           │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                │ PromQL queries
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 4. GRAFANA (Visualization)                                          │
│    (Port 3000)                                                       │
│                                                                      │
│     Configuration:                                                   │
│     • Data Source: Prometheus (http://prometheus:9090)             │
│     • Dashboard: Imported from grafana-dashboard.json               │
│                                                                      │
│     Actions:                                                         │
│     1. Every 5 seconds (auto-refresh):                              │
│        - Send PromQL queries to Prometheus                          │
│        - Receive metric data                                        │
│        - Render visualizations                                      │
│                                                                      │
│     Dashboard Panels (7 total):                                     │
│     ┌─────────────────────────────────────────────────────────┐    │
│     │ 1. Request Rate      (Line Graph)                       │    │
│     │ 2. Total Requests    (Big Number)                       │    │
│     │ 3. Error Rate        (Line Graph)                       │    │
│     │ 4. Response Time p95 (Line Graph)                       │    │
│     │ 5. Avg Response Time (Line Graph)                       │    │
│     │ 6. Task Distribution (Pie Chart)                        │    │
│     │ 7. Requests/Endpoint (Bar Chart)                        │    │
│     └─────────────────────────────────────────────────────────┘    │
│                                                                      │
│     Web UI: http://localhost:3000                                   │
│     Login: admin / admin                                            │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 5. USER VIEWS DASHBOARD                                             │
│                                                                      │
│     Browser ─────── http://localhost:3000 ──────► Grafana           │
│                                                                      │
│     Sees:                                                            │
│     • Real-time metrics (updates every 5s)                          │
│     • Historical trends (up to 15 days)                             │
│     • Performance insights                                          │
│     • Error tracking                                                │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 6. Data Flow Timeline

```
┌────────────────────────────────────────────────────────────────────┐
│                    60-SECOND TIMELINE                              │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│ T+0s: User makes API request                                      │
│       └─► Flask processes request (50ms)                          │
│       └─► Metrics recorded: COUNT++, DURATION.observe(0.05)       │
│                                                                    │
│ T+5s: Grafana auto-refresh                                        │
│       └─► Queries Prometheus: "What's the request rate?"          │
│       └─► Prometheus: "0.2 req/s over last 5 minutes"            │
│       └─► Grafana updates dashboard                               │
│                                                                    │
│ T+10s: Another user request                                       │
│       └─► Flask processes (45ms)                                  │
│       └─► Metrics updated                                         │
│                                                                    │
│ T+15s: Prometheus scrapes /metrics                                │
│       └─► HTTP GET http://flask_app:8080/metrics                  │
│       └─► Receives: request_count=2, duration_bucket[0.05]=2      │
│       └─► Stores in database with timestamp: 2024-01-15 12:00:15 │
│                                                                    │
│ T+20s: Grafana auto-refresh                                       │
│       └─► Dashboard updates with new data                         │
│                                                                    │
│ T+30s: Prometheus scrapes again                                   │
│       └─► request_count=5 (3 more requests happened)              │
│       └─► Stores with new timestamp                               │
│                                                                    │
│ T+45s: Prometheus scrapes                                         │
│                                                                    │
│ T+60s: Prometheus scrapes (4th scrape in 1 minute)               │
│       └─► Complete 1-minute worth of data collected               │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## Summary

**Configuration Files**:
1. ✅ `prometheus.yml` - What to monitor, how often (15s interval)
2. ✅ `docker-compose.yml` - Service definitions, networking, ports
3. ✅ `app/__init__.py` - Metrics instrumentation in Flask
4. ✅ `docs/grafana-dashboard.json` - Pre-configured visualizations

**Data Flow**:
```
User Request → Flask (record metrics) → /metrics endpoint →
Prometheus (scrape every 15s) → Time-series DB →
Grafana (query via PromQL) → Dashboard (visualize)
```

**Access Points**:
- Flask App: http://localhost:8080
- Raw Metrics: http://localhost:8080/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

**Setup Time**: 5 minutes with `docker-compose up -d` + dashboard import

---

*For step-by-step setup instructions, see `MINIMAL_MONITORING_SETUP.md`*
