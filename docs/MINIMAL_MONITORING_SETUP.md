# Minimal Monitoring Setup - Quick Start Guide

**Time Required**: 5 minutes  
**Prerequisites**: Docker Desktop installed and running

---

## Overview

This is the **simplest possible setup** for monitoring your To-Do List application with Prometheus and Grafana.

```
┌─────────────────┐
│  Flask App      │  Exposes metrics at /metrics
│  (Port 8080)    │
└────────┬────────┘
         │ Scrapes every 15s
         ▼
┌─────────────────┐
│  Prometheus     │  Collects and stores metrics
│  (Port 9090)    │
└────────┬────────┘
         │ Queries metrics
         ▼
┌─────────────────┐
│  Grafana        │  Visualizes metrics in dashboards
│  (Port 3000)    │
└─────────────────┘
```

---

## Step 1: Start Everything (One Command)

```bash
# From project root directory
docker-compose up -d
```

This starts:
- ✅ Flask application (port 8080)
- ✅ PostgreSQL database (port 5432)
- ✅ Prometheus (port 9090)
- ✅ Grafana (port 3000)

**Verify it's running**:
```bash
docker-compose ps
```

You should see all services with status "Up".

---

## Step 2: Access Prometheus (Optional - For Verification)

**URL**: http://localhost:9090

### Quick Check - Verify Metrics Are Being Collected:

1. Open http://localhost:9090/targets
2. You should see:
   ```
   State: UP
   Endpoint: http://flask_app:8080/metrics
   ```

3. Click on "Graph" tab
4. Type: `todo_api_request_count_total`
5. Click "Execute"
6. You should see metrics data ✅

**Screenshot Reference**:
![Prometheus Targets](./screenshots/prometheus-targets.png)

---

## Step 3: Access Grafana

**URL**: http://localhost:3000

**Default Credentials**:
- Username: `admin`
- Password: `admin`

*(You'll be prompted to change password - you can skip this for local development)*

---

## Step 4: Add Prometheus Data Source (One-Time Setup)

### Option A: Automatic Configuration (Recommended)

Run this PowerShell script:
```bash
.\setup-grafana.ps1
```

This automatically:
- Adds Prometheus as data source
- Imports the pre-configured dashboard
- Sets up all 7 visualization panels

### Option B: Manual Configuration (5 minutes)

**4.1 Add Data Source**:

1. In Grafana, click the **gear icon** (⚙️) on the left sidebar
2. Click **"Data Sources"**
3. Click **"Add data source"**
4. Select **"Prometheus"**
5. Enter URL: `http://prometheus:9090`
6. Scroll down and click **"Save & Test"**
7. You should see green checkmark: ✅ "Data source is working"

**Screenshot Reference**:
![Grafana Data Source](./screenshots/grafana-datasource.png)

---

## Step 5: Import Dashboard (2 minutes)

**5.1 Import Pre-Configured Dashboard**:

1. Click **four squares icon** (☷) on left sidebar → **"Dashboards"**
2. Click **"Import"** button (top right)
3. Click **"Upload JSON file"**
4. Select: `docs/grafana-dashboard.json`
5. In "Prometheus" dropdown, select **"Prometheus"**
6. Click **"Import"**

**5.2 Verify Dashboard**:

You should now see a dashboard with 7 panels:
- Request Rate (Time Series)
- Total Requests (Big Number)
- Error Rate (Time Series)
- Response Time p95 (Time Series)
- Average Response Time (Time Series)
- Task Status Distribution (Pie Chart)
- Requests by Endpoint (Bar Chart)

**Screenshot Reference**:
![Grafana Dashboard](./screenshots/grafana-dashboard.png)

---

## Step 6: Generate Test Data (Optional)

If your dashboard shows "No Data", generate some test traffic:

```powershell
# Generate 20 test requests
for ($i=0; $i -lt 20; $i++) { 
    Invoke-WebRequest http://localhost:8080/api/tasks 
}
```

After 15 seconds (Prometheus scrape interval), refresh your Grafana dashboard. You should see data appear! ✅

---

## Troubleshooting

### Problem 1: "No Data" in Grafana

**Solution**:
1. Check Prometheus is collecting data: http://localhost:9090/targets
   - Should show State: UP
2. In Grafana, check data source: Configuration → Data Sources → Prometheus
   - Click "Save & Test" - should show green checkmark
3. Generate test traffic (see Step 6)
4. Wait 15 seconds for Prometheus to scrape
5. Refresh dashboard

### Problem 2: "Connection Refused" to Grafana

**Solution**:
```bash
# Check if Grafana is running
docker-compose ps

# If not running, restart all services
docker-compose down
docker-compose up -d

# Check logs
docker-compose logs grafana
```

### Problem 3: Dashboard Queries Show "N/A"

**Solution**:
The metric names must include `_total` suffix:
- ✅ Correct: `todo_api_request_count_total`
- ❌ Wrong: `todo_api_request_count`

Our pre-configured dashboard (`docs/grafana-dashboard.json`) already has the correct names.

### Problem 4: Services Not Starting

**Solution**:
```bash
# Check Docker Desktop is running
docker version

# Check for port conflicts
netstat -ano | findstr "3000"  # Grafana
netstat -ano | findstr "9090"  # Prometheus

# Remove old containers and start fresh
docker-compose down -v
docker-compose up -d
```

---

## Configuration Files

All configuration is already done! Here's what's configured:

### 1. Prometheus Configuration (`prometheus.yml`)

```yaml
global:
  scrape_interval: 15s      # Scrape metrics every 15 seconds

scrape_configs:
  - job_name: 'flask_app'
    static_configs:
      - targets: ['flask_app:8080']  # Scrape Flask /metrics endpoint
```

**What this does**:
- Every 15 seconds, Prometheus fetches metrics from Flask app
- Metrics stored in time-series database
- Queryable via PromQL (Prometheus Query Language)

### 2. Docker Compose Configuration (`docker-compose.yml`)

```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    depends_on:
      - prometheus
```

**What this does**:
- Starts Prometheus with your config file
- Starts Grafana with default password
- Links them together on Docker network

### 3. Flask Metrics Configuration (`app/__init__.py`)

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest

# Define metrics
REQUEST_COUNT = Counter(
    'todo_api_request_count',
    'Total API requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'todo_api_request_duration_seconds',
    'API request duration',
    ['method', 'endpoint']
)

@app.route('/metrics')
def metrics():
    """Expose metrics in Prometheus format"""
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}
```

**What this does**:
- Defines custom metrics (request count, duration, etc.)
- Exposes them at `/metrics` endpoint in Prometheus format
- Prometheus scrapes this endpoint every 15 seconds

---

## Metrics Available

Your application exposes these metrics:

| Metric Name | Type | Description | Example Query |
|-------------|------|-------------|---------------|
| `todo_api_request_count_total` | Counter | Total requests per endpoint | `rate(todo_api_request_count_total[5m])` |
| `todo_api_request_duration_seconds` | Histogram | Request response times | `histogram_quantile(0.95, ...)` |
| `todo_api_errors_total` | Counter | Total errors by type | `rate(todo_api_errors_total[1h])` |
| `todo_tasks_total` | Gauge | Current task count by status | `todo_tasks_total{status="pending"}` |

**View Raw Metrics**:
Visit http://localhost:8080/metrics to see the raw Prometheus format:

```
# HELP todo_api_request_count_total Total API requests
# TYPE todo_api_request_count_total counter
todo_api_request_count_total{endpoint="/api/tasks",method="GET",status_code="200"} 150.0
todo_api_request_count_total{endpoint="/api/tasks",method="POST",status_code="201"} 45.0

# HELP todo_api_request_duration_seconds API request duration
# TYPE todo_api_request_duration_seconds histogram
todo_api_request_duration_seconds_bucket{endpoint="/api/tasks",method="GET",le="0.005"} 120.0
todo_api_request_duration_seconds_bucket{endpoint="/api/tasks",method="GET",le="0.01"} 145.0
```

---

## Dashboard Panels Explained

### 1. Request Rate (Time Series)
**Query**: `rate(todo_api_request_count_total[5m])`
- Shows requests per second over time
- Grouped by endpoint (GET /api/tasks, POST /api/tasks, etc.)
- **Use Case**: Identify traffic patterns, detect spikes

### 2. Total Requests (Stat Panel)
**Query**: `sum(todo_api_request_count_total)`
- Single big number showing total requests since startup
- **Use Case**: Quick health check - is app receiving traffic?

### 3. Error Rate (Time Series)
**Query**: `rate(todo_api_errors_total[5m])`
- Shows errors per second
- Red line to highlight issues
- **Use Case**: Detect when errors start happening

### 4. Response Time p95 (Time Series)
**Query**: `histogram_quantile(0.95, rate(todo_api_request_duration_seconds_bucket[5m]))`
- 95th percentile latency (95% of requests are faster than this)
- **Use Case**: Ensure performance SLA (e.g., 95% of requests < 500ms)

### 5. Average Response Time (Time Series)
**Query**: `rate(todo_api_request_duration_seconds_sum[5m]) / rate(todo_api_request_duration_seconds_count[5m])`
- Mean response time across all endpoints
- **Use Case**: Track overall application performance

### 6. Task Status Distribution (Pie Chart)
**Query**: `todo_tasks_total`
- Shows breakdown of pending vs completed tasks
- Updates in real-time
- **Use Case**: Business metrics - how many tasks are active?

### 7. Requests by Endpoint (Bar Gauge)
**Query**: `sum by (endpoint) (todo_api_request_count_total)`
- Horizontal bars showing requests per endpoint
- **Use Case**: Identify most-used APIs

---

## Next Steps

### For Development:
1. ✅ Setup complete! Keep `docker-compose up -d` running
2. ✅ Access Grafana at http://localhost:3000
3. ✅ Dashboard updates automatically every 5 seconds

### For Production:
Consider these hosted alternatives (no local setup needed):

**Option 1: Google Cloud Monitoring**
- ✅ Native Cloud Run integration
- ✅ No infrastructure to manage
- ✅ Free tier: 150 GB logs/month
- Setup: Export `/metrics` to Cloud Monitoring

**Option 2: Grafana Cloud**
- ✅ Managed Prometheus + Grafana
- ✅ Free tier: 10,000 series, 14-day retention
- ✅ Pre-built dashboards
- Setup: Configure `remote_write` in Prometheus

**Option 3: Datadog/New Relic**
- ✅ Full APM (Application Performance Monitoring)
- ✅ Automatic instrumentation
- ✅ AI-powered anomaly detection
- Cost: $15-30/month per host

---

## Summary

**What you get with this setup**:
- ✅ Real-time metrics visualization
- ✅ Request rate, response times, error tracking
- ✅ Business metrics (task counts)
- ✅ Historical data (15 days retention)
- ✅ Zero code changes (already instrumented)

**Total setup time**: 5 minutes  
**Maintenance**: None (runs in background)  
**Cost**: Free (local Docker containers)

**Access Points**:
- Application: http://localhost:8080
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

---

## Screenshots

The following screenshots show what you should see at each step:

### 1. Prometheus Targets (Step 2)
![Prometheus showing Flask app target as UP](./screenshots/prometheus-targets.png)

### 2. Grafana Data Source Configuration (Step 4)
![Grafana data source configuration screen](./screenshots/grafana-datasource.png)

### 3. Grafana Dashboard Import (Step 5)
![Grafana dashboard import screen](./screenshots/grafana-import.png)

### 4. Complete Dashboard (Final Result)
![Full Grafana dashboard with 7 panels showing metrics](./screenshots/grafana-dashboard.png)

**Note**: Screenshots are for reference. Your actual dashboard will show real data from your application.

---

## Quick Reference Card

```
┌──────────────────────────────────────────────────────────┐
│                  MONITORING QUICK START                  │
├──────────────────────────────────────────────────────────┤
│ 1. Start:     docker-compose up -d                       │
│ 2. Grafana:   http://localhost:3000 (admin/admin)       │
│ 3. Add Data:  Configuration → Data Sources → Prometheus │
│               URL: http://prometheus:9090                │
│ 4. Import:    Upload docs/grafana-dashboard.json        │
│ 5. Test:      for($i=0;$i -lt 20;$i++){curl ...}       │
├──────────────────────────────────────────────────────────┤
│ Troubleshooting:                                         │
│ • No data? Wait 15s for Prometheus scrape               │
│ • Connection refused? docker-compose restart grafana     │
│ • Metrics wrong? Check _total suffix in queries          │
└──────────────────────────────────────────────────────────┘
```

---

**Questions?** See detailed guides:
- `docs/MONITORING.md` - Complete 790+ line guide
- `docs/GRAFANA_MANUAL.md` - Step-by-step with explanations
- `docs/MONITORING_DATA.md` - All metrics documentation
