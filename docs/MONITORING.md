# Monitoring & Observability Setup

## Overview
This document describes the monitoring infrastructure for the to-do-list-app, including Prometheus metrics collection and Grafana visualization.

## Architecture

```
┌─────────────────┐
│  Flask App      │
│ (port 8080)     │
└────────┬────────┘
         │ Exposes metrics at /api/v1/metrics
         ▼
┌─────────────────┐
│  Prometheus     │
│ (port 9090)     │
│ Scrapes every   │
│ 15 seconds      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Grafana        │
│ (port 3000)     │
│ Visualizes      │
│ metrics         │
└─────────────────┘
```

## Components

### 1. Prometheus (`prometheus.yml`)
- **Purpose**: Metrics collection and storage
- **Scrape Interval**: 15 seconds
- **Metrics Endpoint**: `http://localhost:8080/api/v1/metrics`
- **Local Access**: http://localhost:9090
- **Data Retention**: Default 15 days
- **Port**: 9090

### 2. Grafana (`docker-compose.yml`)
- **Purpose**: Visualization and dashboard creation
- **Admin Credentials**: 
  - Username: `admin`
  - Password: `admin`
- **Local Access**: http://localhost:3000
- **Port**: 3000
- **Features**:
  - Pre-configured Prometheus data source
  - Custom dashboard creation
  - Alert management
  - Multi-user support

### 3. Flask Application Metrics
The app exposes three Prometheus metrics at `/api/v1/metrics`:

#### a) Request Count
```
todo_api_request_count{method="GET|POST|PUT|DELETE", endpoint="...", http_status="200|404|500"}
```
- **Type**: Counter
- **Purpose**: Track total API requests by method, endpoint, and status
- **Example**: Total GET requests to `/tasks` returning 200

#### b) Request Latency
```
todo_api_request_latency_seconds{method="GET|POST|PUT|DELETE", endpoint="..."}
```
- **Type**: Histogram
- **Purpose**: Measure response time distribution
- **Buckets**: Automatically generates percentiles (p50, p95, p99)
- **Example**: 95th percentile response time for POST requests

#### c) Error Count
```
todo_api_error_count{method="GET|POST|PUT|DELETE", endpoint="...", http_status="422|500"}
```
- **Type**: Counter
- **Purpose**: Track errors by type and endpoint
- **Example**: Total 422 validation errors on POST `/tasks`

## Local Setup

### Starting the Stack
```bash
docker-compose up -d
```

### Accessing Services

1. **Flask App**: http://localhost:8080
   - Main application UI
   - API endpoints

2. **Prometheus**: http://localhost:9090
   - Query interface
   - Example queries:
     ```
     # Total requests per endpoint
     sum by (endpoint) (rate(todo_api_request_count[5m]))
     
     # Error rate
     sum by (endpoint) (rate(todo_api_error_count[5m])) / sum by (endpoint) (rate(todo_api_request_count[5m]))
     
     # P95 latency
     histogram_quantile(0.95, rate(todo_api_request_latency_seconds_bucket[5m]))
     ```

3. **Grafana**: http://localhost:3000
   - Admin dashboard
   - Create custom visualizations
   - Set up alerts

## Cloud Deployment (Google Cloud Run)

### Current Limitations
- **Prometheus**: Not deployed to Cloud Run (local development only)
- **Grafana**: Not deployed to Cloud Run (local development only)
- **Metrics Endpoint**: Available at `/api/v1/metrics` but not scraped in production

### Production Monitoring Options

#### Option 1: Google Cloud Monitoring (Recommended)
```yaml
- Native GCP integration
- Automatic metric collection
- Built-in dashboards
- Alert management via Google Cloud Alerting
- Cost: Included in GCP pricing
```

#### Option 2: Third-Party Services
- **Datadog**: Advanced monitoring, APM
- **New Relic**: Full observability platform
- **Elastic Cloud**: ELK stack in cloud
- **Grafana Cloud**: Hosted Grafana with data persistence

#### Option 3: Self-Hosted Prometheus Stack
```yaml
- Deploy Prometheus/Grafana to Cloud Run or Compute Engine
- Configure Cloud Run metrics endpoint
- Maintain persistent storage for Prometheus
- More control but increased operational overhead
```

## Creating Dashboards in Grafana

### Step 1: Access Grafana
1. Navigate to http://localhost:3000
2. Login with `admin/admin`
3. Click "+" → "Dashboard"

### Step 2: Add Prometheus Data Source
1. Settings (gear icon) → Data Sources
2. Add → Prometheus
3. URL: `http://prometheus:9090`
4. Save & Test

### Step 3: Create Panels

#### Panel 1: Request Rate
- **Metric**: `sum(rate(todo_api_request_count[5m]))`
- **Visualization**: Graph/Stat
- **Title**: "Requests per Second"

#### Panel 2: Error Rate
- **Metric**: `sum(rate(todo_api_error_count[5m]))`
- **Visualization**: Graph
- **Title**: "Error Rate"

#### Panel 3: Latency (P95)
- **Metric**: `histogram_quantile(0.95, rate(todo_api_request_latency_seconds_bucket[5m]))`
- **Visualization**: Gauge
- **Title**: "P95 Latency (seconds)"

#### Panel 4: Endpoint Performance
- **Metric**: `sum by (endpoint) (rate(todo_api_request_count[5m]))`
- **Visualization**: Pie Chart
- **Title**: "Requests by Endpoint"

## Metrics Query Examples

### SLO Monitoring
```
# 99.9% availability (0.1% error rate)
sum(rate(todo_api_error_count[5m])) / sum(rate(todo_api_request_count[5m])) < 0.001

# Response time SLO (p99 < 500ms)
histogram_quantile(0.99, rate(todo_api_request_latency_seconds_bucket[5m])) < 0.5
```

### Troubleshooting
```
# Requests by status code
sum by (http_status) (rate(todo_api_request_count[5m]))

# Error rate by endpoint
sum by (endpoint) (rate(todo_api_error_count[5m])) / sum by (endpoint) (rate(todo_api_request_count[5m]))

# Slowest endpoints (avg latency)
sum by (endpoint) (rate(todo_api_request_latency_seconds_sum[5m])) / sum by (endpoint) (rate(todo_api_request_latency_seconds_count[5m]))
```

## Alert Rules

### Example Alert Rules (for future implementation)

```yaml
groups:
  - name: todo-app
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: sum(rate(todo_api_error_count[5m])) / sum(rate(todo_api_request_count[5m])) > 0.05
        for: 5m
        annotations:
          summary: "High error rate detected"
          
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(todo_api_request_latency_seconds_bucket[5m])) > 1
        for: 5m
        annotations:
          summary: "P95 latency exceeds 1 second"
          
      - alert: HighErrorCount
        expr: sum(rate(todo_api_error_count[5m])) > 5
        for: 5m
        annotations:
          summary: "More than 5 errors per second"
```

## Key Metrics to Monitor

| Metric | Threshold | Action |
|--------|-----------|--------|
| Error Rate | > 5% | Investigate logs |
| P95 Latency | > 1s | Check database/resources |
| 5xx Errors | > 10/min | Page on-call engineer |
| 4xx Errors | > 100/min | Review validation rules |
| Request Rate | > 1000/min | Check scaling |

## Files

- **`prometheus.yml`** - Prometheus configuration
- **`docker-compose.yml`** - Grafana service definition
- **`app/api/tasks.py`** - Metric collection code
- **`docs/MONITORING.md`** - This file

## Next Steps

1. ✅ Local monitoring set up with Docker Compose
2. 📋 Configure Cloud Monitoring for production
3. 📊 Create production dashboard in Grafana Cloud
4. 🔔 Set up alert rules for SLO monitoring
5. 📈 Track business metrics (task completion, user activity)

## Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Dashboard](https://grafana.com/docs/grafana/latest/)
- [Google Cloud Monitoring](https://cloud.google.com/monitoring/docs)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/instrumentation/)
