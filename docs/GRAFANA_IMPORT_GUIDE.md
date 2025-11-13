# Grafana Dashboard Import Guide

## Complete Step-by-Step Instructions

### Prerequisites
- Grafana running at http://localhost:3000
- Prometheus running at http://localhost:9090
- Docker Compose services started with `docker-compose up -d`

---

## Part 1: Add Prometheus Data Source

### Step 1.1: Access Grafana Settings
1. Open http://localhost:3000 in your browser
2. Login with credentials:
   - **Username**: `admin`
   - **Password**: `admin`
3. You'll see the Grafana home dashboard

### Step 1.2: Navigate to Data Sources
1. Click the **Settings icon** (⚙️) in the left sidebar
2. From the dropdown menu, select **Data Sources**
   - Alternative: You can also use the search bar at the top (type "Data Sources")

### Step 1.3: Create New Data Source
1. Click the **+ Add data source** button (top right)
2. You'll see a list of available data source types
3. Select **Prometheus** from the list
   - It should be near the top of the list

### Step 1.4: Configure Prometheus Connection
Fill in the following fields:

| Field | Value | Notes |
|-------|-------|-------|
| **Name** | `Prometheus` | Display name in Grafana |
| **URL** | `http://prometheus:9090` | Docker Compose service name and port |
| **Access** | `Server` | Access method (server-side proxy) |
| **Scrape Interval** | `15s` | Match prometheus.yml setting |
| **Query Timeout** | `60s` | Default timeout for queries |

**Important**: Use `http://prometheus:9090` (service name), not `localhost:9090`
- From Grafana container, `localhost` refers to the container itself
- `prometheus` is the Docker Compose service name

### Step 1.5: Test Connection
1. Scroll down to find the **Save & test** button
2. Click **Save & test**
3. You should see: **"✓ Data source is working"** message
   - If it fails, check that Prometheus container is running: `docker-compose ps`

### Step 1.6: Verify Success
1. You should see: **"Data source updated"** confirmation message
2. The Prometheus data source is now available for dashboards

---

## Part 2: Import the Dashboard

### Step 2.1: Access Dashboard Import
1. Click the **"+"** icon in the left sidebar
2. Select **Import**
   - Alternative: Use search bar and search for "import"

### Step 2.2: Import Dashboard JSON

**Option A: Upload JSON File (Recommended)**
1. Click **Upload JSON file**
2. Navigate to your repository: `/docs/grafana-dashboard.json`
3. Select the file and open it
4. The JSON will automatically populate in the text area

**Option B: Paste JSON Content**
1. Copy the entire contents of `docs/grafana-dashboard.json`
2. Paste into the text area labeled "JSON Dashboard"
3. Click outside the text area to validate

**Option C: Use URL**
1. If dashboard is hosted online, paste the URL
2. Click **Load**

### Step 2.3: Configure Import Settings
After uploading/pasting, you'll see an import options dialog:

| Setting | Value | Notes |
|---------|-------|-------|
| **Name** | `To-Do App Metrics Dashboard` | Display name in Grafana |
| **Folder** | `General` | Where to save the dashboard |
| **Unique ID** | `todo-app-dashboard` | Unique identifier |

### Step 2.4: Select Data Source
1. Look for the section: **"Select the Prometheus data source"**
2. In the dropdown that appears, select **Prometheus**
3. This links all the dashboard panels to your Prometheus instance

### Step 2.5: Import Dashboard
1. Click the **Import** button
2. Wait for the import to complete (should be instant)
3. You'll be redirected to the newly imported dashboard

---

## Part 3: Verify Dashboard

### Step 3.1: Check Dashboard Panels
You should see 7 panels populate with data:

1. **Requests Per Second** (top-left gauge)
   - Shows current request rate
   - Green = < 80 req/s, Red = > 80 req/s

2. **Error Rate** (top-middle gauge)
   - Shows percentage of failed requests
   - Green = < 5%, Yellow = 5-10%, Red = > 10%

3. **P95 Latency** (top-right gauge)
   - Shows 95th percentile response time
   - Green = < 0.5s, Yellow = 0.5-1s, Red = > 1s

4. **Request Rate by Endpoint** (middle-left graph)
   - Line chart showing requests over time
   - Broken down by endpoint (GET/POST/PUT/DELETE)

5. **Error Rate by Endpoint** (middle-right graph)
   - Shows error rate trend per endpoint
   - Helps identify which endpoints have issues

6. **Requests by HTTP Status Code** (bottom-left bar chart)
   - Stacked bars showing 200/201/204/404/422/500 distribution
   - Helps categorize success vs error types

7. **Latency Percentiles by Endpoint** (bottom-right graph)
   - Shows p50/p95/p99 latency trends
   - Helps track performance changes over time

### Step 3.2: Generate Test Data
To see data in the dashboard:

1. Make some API requests to your app:
   ```bash
   # Get all tasks
   curl http://localhost:8080/api/v1/tasks
   
   # Create a task
   curl -X POST http://localhost:8080/api/v1/tasks \
     -H "Content-Type: application/json" \
     -d '{"title":"Test Task","description":"Testing"}'
   
   # Try an error
   curl http://localhost:8080/api/v1/tasks/999
   ```

2. Refresh the dashboard (press `F5` or click refresh button)
3. You should see data appear in the panels within 15-30 seconds

### Step 3.3: Verify Prometheus Scraping
1. Open Prometheus UI: http://localhost:9090
2. Click **Status** → **Targets**
3. You should see:
   - **Job**: `to-do-list-app`
   - **State**: `UP` (green)
   - **Endpoint**: `http://web:8080/api/v1/metrics`
4. This confirms Prometheus is collecting metrics

---

## Part 4: Customize Dashboard

### Edit Dashboard
1. Click the **Edit** button (pencil icon) at the top
2. You can now modify panels:
   - Resize panels: Drag the bottom-right corner
   - Edit panel: Click the panel title, then **Edit**
   - Delete panel: Click the panel title, then **Delete**
   - Add new panel: Click **Add Panel** at the top

### Update Queries
To modify what a panel shows:

1. Click on a panel
2. Click **Edit**
3. Under **Metrics**, you can change the PromQL query
4. Example queries you can use:

```promql
# Request rate (current)
sum(rate(todo_api_request_count[5m]))

# Error rate percentage
(sum(rate(todo_api_error_count[5m])) / sum(rate(todo_api_request_count[5m]))) * 100

# Average latency
sum(rate(todo_api_request_latency_seconds_sum[5m])) / sum(rate(todo_api_request_latency_seconds_count[5m]))

# Requests per endpoint (last hour)
sum by (endpoint) (increase(todo_api_request_count[1h]))
```

### Save Changes
1. Click **Save** button at the top
2. Enter a dashboard version message (optional)
3. Click **Save** to confirm

---

## Troubleshooting

### Dashboard Shows No Data

**Problem**: All panels show "No Data"

**Solutions**:
1. Check if Prometheus data source is configured:
   - Settings → Data Sources → Verify Prometheus shows "✓ Data source is working"

2. Make sure API requests are being made:
   - `curl http://localhost:8080/api/v1/health`
   - Should return `{"status": "healthy"}`

3. Check Prometheus is scraping metrics:
   - http://localhost:9090 → Status → Targets
   - Job should be UP (green)

4. Wait 15-30 seconds for first metrics:
   - Prometheus scrapes every 15 seconds
   - Data needs to accumulate before graphs appear

### Prometheus Data Source Connection Failed

**Problem**: "Unable to connect to Prometheus"

**Solutions**:
1. Check Prometheus is running:
   ```bash
   docker-compose ps
   # Should show prometheus is UP
   ```

2. Check the URL is correct:
   - Use `http://prometheus:9090` (not `localhost`)
   - From Grafana's container perspective, `prometheus` is the service name

3. Restart both services:
   ```bash
   docker-compose restart prometheus grafana
   ```

4. Check logs:
   ```bash
   docker-compose logs prometheus
   docker-compose logs grafana
   ```

### JSON Import Fails

**Problem**: "Error importing dashboard"

**Solutions**:
1. Ensure JSON is valid:
   - Open `grafana-dashboard.json` in a text editor
   - Should start with `{` and end with `}`

2. Try Option B (paste content directly):
   - Copy entire file content
   - Paste in text area
   - Click outside to validate

3. Clear browser cache:
   - Press `Ctrl + Shift + Delete`
   - Clear cached files
   - Reload Grafana

4. Check Grafana logs:
   ```bash
   docker-compose logs grafana
   ```

### Panels Show Empty Time Range

**Problem**: "No data in time range"

**Solutions**:
1. Adjust time range selector (top right):
   - Click time range dropdown
   - Select **Last 6 hours** or **Last 24 hours**

2. Create more test data:
   - Make additional API calls to populate metrics
   - Wait 30-60 seconds for Prometheus to scrape

3. Check metric retention:
   - Prometheus default retention: 15 days
   - If data is too old, it will be deleted

---

## Quick Reference

### Grafana URLs
- **Grafana Home**: http://localhost:3000
- **Settings**: http://localhost:3000/admin/settings
- **Data Sources**: http://localhost:3000/admin/datasources
- **Dashboard List**: http://localhost:3000/dashboards

### Prometheus URLs
- **Prometheus UI**: http://localhost:9090
- **Metrics Endpoint**: http://localhost:8080/api/v1/metrics
- **Query Console**: http://localhost:9090/graph
- **Targets**: http://localhost:9090/targets

### Useful Docker Commands
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs grafana
docker-compose logs prometheus
docker-compose logs web

# Check running services
docker-compose ps

# Restart a service
docker-compose restart grafana
```

### Common PromQL Queries
```
# Request rate per endpoint
sum by (endpoint) (rate(todo_api_request_count[5m]))

# Error percentage
(sum(rate(todo_api_error_count[5m])) / sum(rate(todo_api_request_count[5m]))) * 100

# P99 latency
histogram_quantile(0.99, rate(todo_api_request_latency_seconds_bucket[5m]))

# Total requests since restart
sum(todo_api_request_count)
```

---

## Next Steps

1. ✅ Add Prometheus data source to Grafana
2. ✅ Import `grafana-dashboard.json`
3. ✅ Verify dashboard displays metrics
4. 📊 Create additional dashboards for business metrics
5. 🔔 Set up alert rules for SLO monitoring
6. ☁️ Migrate to Grafana Cloud for production

