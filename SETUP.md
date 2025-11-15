# Setup Guide for Beginners

> **Complete step-by-step instructions to get this To-Do app running on your computer**

## What You'll Get

- ✅ A working To-Do List web application
- ✅ Ability to create, edit, and delete tasks
- ✅ Professional REST API
- ✅ (Optional) Full monitoring dashboard

---

## Choose Your Setup Path

### 🟢 Easy Mode: Python Only (5 minutes)
**Best for**: Just trying out the app, no Docker needed  
**You get**: Working app with SQLite database  
**Monitoring**: No

### 🔵 Full Mode: Docker Compose (10 minutes)
**Best for**: Complete production-like setup  
**You get**: App + PostgreSQL + Prometheus + Grafana  
**Monitoring**: Yes (6-panel dashboard)

---

## 🟢 Easy Mode Setup (Python Only)

### Step 1: Install Python

1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or newer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click Install

**Verify installation:**
```powershell
python --version
# Should show: Python 3.11.x or higher
```

### Step 2: Download the Project

**Option A: Using Git**
```powershell
git clone https://github.com/mmerino90/to-do-list-app.git
cd to-do-list-app
```

**Option B: Download ZIP**
1. Go to https://github.com/mmerino90/to-do-list-app
2. Click green "Code" button → "Download ZIP"
3. Extract ZIP file
4. Open PowerShell/Terminal in that folder

### Step 3: Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate it
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Windows CMD:
# venv\Scripts\activate.bat

# Mac/Linux:
# source venv/bin/activate

# You should see (venv) before your prompt
```

**Troubleshooting**: If you get "execution policy" error on Windows:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 4: Install Dependencies

```powershell
pip install -r requirements.txt
# Wait 30-60 seconds for installation...
```

### Step 5: Run the App!

```powershell
python run.py
```

You should see:
```
 * Running on http://127.0.0.1:8080
 * Press CTRL+C to quit
```

### Step 6: Use the App

Open your browser and go to: **http://127.0.0.1:8080**

You should see the To-Do List interface! Try:
- ✅ Click "Add Task" to create a new task
- ✅ Click task text to edit it
- ✅ Click "Delete" to remove a task
- ✅ Tasks are saved in `instance/todo.db` (SQLite database)

**API Endpoints:**
- Get all tasks: http://127.0.0.1:8080/api/v1/tasks
- Health check: http://127.0.0.1:8080/api/v1/health

### Step 7: Run Tests (Optional)

```powershell
pytest --cov=app
```

You should see:
```
====== 10 passed in 2.15s ======
Coverage: 82.75%
```

### Stop the App

Press **CTRL+C** in the terminal where app is running.

---

## 🔵 Full Mode Setup (Docker Compose)

### Step 1: Install Docker Desktop

1. Go to https://www.docker.com/products/docker-desktop/
2. Download Docker Desktop for your OS
3. Install and restart computer if prompted
4. Open Docker Desktop and wait for it to start

**Verify installation:**
```powershell
docker --version
# Should show: Docker version 20.x.x or higher
```

### Step 2: Download the Project

Same as Easy Mode Step 2 above.

### Step 3: Create Your .env File

```powershell
# Copy the template
# Windows PowerShell:
Copy-Item .env.example .env

# Mac/Linux:
cp .env.example .env
```

### Step 4: Edit .env File

Open `.env` in any text editor (Notepad, VS Code, etc.) and change the password:

**Before:**
```dotenv
POSTGRES_PASSWORD=your_secure_password_here
DATABASE_URL=postgresql://postgres:your_secure_password_here@db:5432/todo
```

**After (example):**
```dotenv
POSTGRES_PASSWORD=MySecurePass123!
DATABASE_URL=postgresql://postgres:MySecurePass123!@db:5432/todo
```

⚠️ **IMPORTANT**: Make sure password matches in BOTH lines!

Save and close the file.

### Step 5: Start All Services

```powershell
docker-compose up -d
```

**What happens:**
- Downloads Docker images (first time only, 2-3 minutes)
- Starts 4 services: Flask app, PostgreSQL, Prometheus, Grafana
- Shows status of each service

**Wait 30 seconds**, then check if everything is running:

```powershell
docker-compose ps
```

You should see all 4 services as "Up" or "Up (healthy)":
```
NAME         SERVICE      STATUS
grafana      grafana      Up
prometheus   prometheus   Up
to-do-db     db           Up (healthy)
to-do-web    web          Up
```

### Step 6: Access the Services

Open your browser and visit:

| What | URL | Login |
|------|-----|-------|
| **📱 Web App** | http://localhost:8080 | No login needed |
| **📊 API** | http://localhost:8080/api/v1/tasks | No login needed |
| **📈 Prometheus** | http://localhost:9090 | No login needed |
| **📊 Grafana** | http://localhost:3000 | admin / admin |

### Step 7: Setup Grafana Dashboard (Optional but Cool!)

1. Open http://localhost:3000
2. Login: `admin` / `admin` (skip password change for now)
3. Click **Dashboards** (left sidebar)
4. Click **Import** (top right)
5. Click **Upload JSON file**
6. Select file: `docs/grafana-dashboard.json` from the project folder
7. Click **Import**

You now have a 6-panel dashboard showing:
- ✅ Request rate
- ✅ Total requests
- ✅ Error rate
- ✅ Response time (p95)
- ✅ Average response time
- ✅ Requests by endpoint

**Generate some test data:**
```powershell
# Run this to generate traffic for the dashboard
for ($i=1; $i -le 50; $i++) {
    Invoke-WebRequest http://localhost:8080/api/v1/tasks
    Start-Sleep -Milliseconds 100
}
```

Refresh the Grafana dashboard to see the data!

### Step 8: Stop All Services

```powershell
docker-compose down
```

This stops and removes all containers. Your data is preserved in Docker volumes.

**To start again:**
```powershell
docker-compose up -d
```

---

## 🆘 Troubleshooting

### Python Issues

**Problem**: `python: command not found`  
**Solution**: Install Python and make sure "Add to PATH" was checked during installation. Restart terminal.

**Problem**: `cannot import name 'create_app'`  
**Solution**: Make sure you're in the project folder (`cd to-do-list-app`) and virtual environment is activated.

**Problem**: Virtual environment activation fails on Windows  
**Solution**: 
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Docker Issues

**Problem**: `docker: command not found`  
**Solution**: Install Docker Desktop and make sure it's running (check system tray icon).

**Problem**: `port 8080 already in use`  
**Solution**: Stop any other services using port 8080, or change port in `docker-compose.yml`:
```yaml
ports:
  - "8081:8080"  # Use port 8081 instead
```

**Problem**: `connection refused` to database  
**Solution**: 
1. Check passwords match in `.env` file
2. Wait longer (database takes 30-60 seconds to start)
3. Check database is healthy: `docker-compose ps`

**Problem**: Services won't start  
**Solution**: 
```powershell
# Stop everything
docker-compose down

# Remove old volumes (⚠️ deletes data!)
docker-compose down -v

# Start fresh
docker-compose up -d
```

### Application Issues

**Problem**: Web page won't load  
**Solution**: 
1. Make sure app is running (check terminal output)
2. Try http://localhost:8080 instead of http://127.0.0.1:8080
3. Clear browser cache (Ctrl+Shift+R)

**Problem**: Tasks not saving  
**Solution**: 
- **Python mode**: Check `instance/todo.db` file was created
- **Docker mode**: Check database container is healthy: `docker-compose ps`

**Problem**: Grafana dashboard shows "No Data"  
**Solution**: 
1. Generate test traffic (see Step 7 above)
2. Wait 15 seconds (Prometheus scrapes every 15s)
3. Check Prometheus is collecting data: http://localhost:9090

---

## 📚 Next Steps

Once you have the app running:

1. **Learn the API**: Check out [`docs/README.md`](./docs/README.md)
2. **Read the Code**: Start with `app/api/tasks.py` to see how endpoints work
3. **Run Tests**: `pytest --cov=app` to see test coverage
4. **Modify the Code**: Make changes and see them live!
5. **Deploy to Cloud**: Follow deployment guide in main README.md

---

## 🎓 Learning Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **PostgreSQL Tutorial**: https://www.postgresqltutorial.com/
- **Docker Getting Started**: https://docs.docker.com/get-started/
- **REST API Best Practices**: https://restfulapi.net/

---

## ✅ Success Checklist

After setup, you should be able to:

- [ ] Access the web app at http://localhost:8080
- [ ] Create a new task via UI
- [ ] View all tasks via API: http://localhost:8080/api/v1/tasks
- [ ] Run tests and see 10/10 passing
- [ ] (Docker mode) Access Grafana dashboard
- [ ] (Docker mode) See metrics in Prometheus

If you can check all these boxes, congratulations! 🎉 You've successfully set up the To-Do List app!

---

**Need more help?** Check the full [README.md](./README.md) or open an issue on GitHub.
