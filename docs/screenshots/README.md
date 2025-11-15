# Screenshots Reference Guide

This directory contains reference screenshots for the monitoring setup process.

## Screenshot List

### 1. `prometheus-targets.png`
**Shows**: Prometheus targets page showing Flask app status as "UP"
**URL**: http://localhost:9090/targets
**What to verify**:
- State: UP (green)
- Endpoint: http://flask_app:8080/metrics
- Last Scrape: within last 15 seconds

**Expected View**:
```
Endpoint: http://flask_app:8080/metrics
State: UP
Labels: job="flask_app"
Last Scrape: 2s ago
Scrape Duration: 5.2ms
```

---

### 2. `grafana-datasource.png`
**Shows**: Grafana data source configuration screen
**URL**: http://localhost:3000/datasources/new
**What to verify**:
- Data source type: Prometheus
- URL: http://prometheus:9090
- Access: Server (default)
- Green banner: "Data source is working" ✅

**Key Settings**:
```
Name: Prometheus
Type: Prometheus
URL: http://prometheus:9090
Access: Server (default)
Scrape interval: 15s
Query timeout: 60s
HTTP Method: POST
```

---

### 3. `grafana-import.png`
**Shows**: Grafana dashboard import screen
**URL**: http://localhost:3000/dashboard/import
**What to verify**:
- "Upload JSON file" button visible
- After upload: Preview of 7 panels shown
- Prometheus dropdown: "Prometheus" selected

**Import Process**:
```
1. Click "Import"
2. Click "Upload JSON file"
3. Select: docs/grafana-dashboard.json
4. Dashboard name: "To-Do List API Monitoring"
5. Folder: General
6. Prometheus: Select "Prometheus"
7. Click "Import"
```

---

### 4. `grafana-dashboard.png`
**Shows**: Complete Grafana dashboard with all 7 panels displaying data
**URL**: http://localhost:3000/d/todo-api-monitoring
**What to verify**:
- All 7 panels showing data (not "No Data")
- Time range: Last 6 hours (adjustable top-right)
- Auto-refresh: 5s (top-right dropdown)

**Expected Panels** (left to right, top to bottom):
```
Row 1:
┌─────────────────────────┐  ┌──────────────┐
│ Request Rate            │  │ Total        │
│ (Time Series - Lines)   │  │ Requests     │
│                         │  │ (Big Number) │
└─────────────────────────┘  └──────────────┘

Row 2:
┌─────────────────────────┐  ┌─────────────────────────┐
│ Error Rate              │  │ Response Time (p95)     │
│ (Time Series - Red)     │  │ (Time Series - Orange)  │
└─────────────────────────┘  └─────────────────────────┘

Row 3:
┌─────────────────────────┐  ┌─────────────────────────┐
│ Average Response Time   │  │ Task Status Distribution│
│ (Time Series - Blue)    │  │ (Pie Chart)             │
└─────────────────────────┘  └─────────────────────────┘

Row 4:
┌──────────────────────────────────────────────────────┐
│ Requests by Endpoint                                  │
│ (Horizontal Bar Chart)                                │
│ ████████████████ GET /api/tasks          150         │
│ ████████ POST /api/tasks                  45         │
│ ██ GET /api/health                        12         │
└──────────────────────────────────────────────────────┘
```

---

## How to Take Your Own Screenshots

If you want to create your own screenshots for documentation:

### Windows (Snipping Tool):
1. Press `Win + Shift + S`
2. Select area to capture
3. Screenshot copied to clipboard
4. Paste into image editor and save

### Chrome DevTools:
1. Press `F12` to open DevTools
2. Press `Ctrl + Shift + P`
3. Type "screenshot"
4. Select "Capture full size screenshot"

### Recommended Filenames:
- `prometheus-targets.png` - Prometheus targets page
- `prometheus-metrics.png` - Prometheus graph view
- `grafana-login.png` - Grafana login screen
- `grafana-datasource.png` - Data source configuration
- `grafana-datasource-success.png` - Green "Data source is working" banner
- `grafana-import.png` - Dashboard import screen
- `grafana-dashboard.png` - Full dashboard view
- `grafana-panel-request-rate.png` - Close-up of request rate panel
- `grafana-panel-errors.png` - Close-up of error rate panel

---

## Text-Based Visual References

If you prefer text-based representations, here are the key screens:

### Prometheus Targets Page
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Prometheus > Targets                                   ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                        ┃
┃ flask_app (1/1 up)                                     ┃
┃ ┌────────────────────────────────────────────────┐   ┃
┃ │ Endpoint: http://flask_app:8080/metrics        │   ┃
┃ │ State: UP ✓                                    │   ┃
┃ │ Labels: job="flask_app"                        │   ┃
┃ │ Last Scrape: 2.153s ago                        │   ┃
┃ │ Scrape Duration: 5.234ms                       │   ┃
┃ │ Error: none                                    │   ┃
┃ └────────────────────────────────────────────────┘   ┃
┃                                                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

### Grafana Data Source Configuration
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Data Sources / Prometheus                             ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                        ┃
┃ Settings                                               ┃
┃                                                        ┃
┃ Name                                                   ┃
┃ ┌────────────────────────────────────────────────┐   ┃
┃ │ Prometheus                                     │   ┃
┃ └────────────────────────────────────────────────┘   ┃
┃                                                        ┃
┃ HTTP                                                   ┃
┃ ┌───────────────────────────────────────────���────┐   ┃
┃ │ URL: http://prometheus:9090                    │   ┃
┃ └────────────────────────────────────────────────┘   ┃
┃                                                        ┃
┃ Access: ⦿ Server (default)   ○ Browser               ┃
┃                                                        ┃
┃ ┌─────────────────┐  ┌──────────────┐               ┃
┃ │ Save & Test     │  │ Delete       │               ┃
┃ └─────────────────┘  └──────────────┘               ┃
┃                                                        ┃
┃ ✓ Data source is working                              ┃
┃                                                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

### Grafana Dashboard (Simplified View)
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ To-Do List API Monitoring          🔄 5s  ⏱ Last 6 hours   ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                               ┃
┃ ┌──────────────────────────────────┐  ┌─────────────────┐  ┃
┃ │ Request Rate                     │  │ Total Requests  │  ┃
┃ │                        ╱╲        │  │                 │  ┃
┃ │                  ╱╲   ╱  ╲       │  │      1,247      │  ┃
┃ │            ╱╲   ╱  ╲_╱    ╲      │  │                 │  ┃
┃ │      _____╱  ╲_╱            ╲    │  │  requests       │  ┃
┃ │  0.5 req/s                       │  └─────────────────┘  ┃
┃ └──────────────────────────────────┘                       ┃
┃                                                               ┃
┃ ┌──────────────────────────────────┐  ┌─────────────────┐  ┃
┃ │ Error Rate                       │  │ Response Time   │  ┃
┃ │                                  │  │ (p95)           │  ┃
┃ │  0.002 errors/s                  │  │                 │  ┃
┃ │  ________________                │  │       ╱╲        │  ┃
┃ │                                  │  │  ____╱  ╲___    │  ┃
┃ │                                  │  │  45ms           │  ┃
┃ └──────────────────────────────────┘  └─────────────────┘  ┃
┃                                                               ┃
┃ ┌──────────────────────────────────┐  ┌─────────────────┐  ┃
┃ │ Average Response Time            │  │ Task Status     │  ┃
┃ │                                  │  │                 │  ┃
┃ │           ╱╲                     │  │    ◗ 35%       │  ┃
┃ │      ____╱  ╲____                │  │  ◖             │  ┃
┃ │  28ms                            │  │    65%         │  ┃
┃ │                                  │  │  Pending ◗     │  ┃
┃ │                                  │  │  Completed ◖   │  ┃
┃ └──────────────────────────────────┘  └─────────────────┘  ┃
┃                                                               ┃
┃ ┌───────────────────────────────────────────────────────┐  ┃
┃ │ Requests by Endpoint                                  │  ┃
┃ │                                                       │  ┃
┃ │ GET /api/tasks      ███████████████████    856       │  ┃
┃ │ POST /api/tasks     ████████               234       │  ┃
┃ │ PUT /api/tasks      ███                     87       │  ┃
┃ │ DELETE /api/tasks   ██                      45       │  ┃
┃ │ GET /api/health     █                       25       │  ┃
┃ └───────────────────────────────────────────────────────┘  ┃
┃                                                               ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## Placeholder Images

Until real screenshots are added, you can use these ASCII art representations in your documentation or create simple mockups using:

- **Draw.io**: https://app.diagrams.net/
- **Excalidraw**: https://excalidraw.com/
- **Figma**: https://figma.com/

Or simply run the actual setup and take screenshots yourself! The setup takes only 5 minutes.

---

## Contributing Screenshots

If you take screenshots and want to add them to this repository:

1. Take screenshots at 1920x1080 resolution (or similar)
2. Save as PNG format
3. Use descriptive filenames (see list above)
4. Place in `docs/screenshots/` directory
5. Update `MINIMAL_MONITORING_SETUP.md` with actual image links

**Image Link Format**:
```markdown
![Alt text description](./screenshots/filename.png)
```
