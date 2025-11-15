# Scripts

Utility scripts for development and setup.

## Available Scripts

### `setup-grafana.ps1`
PowerShell script to automate Grafana dashboard setup.

**Purpose**: Imports the Grafana dashboard JSON automatically.

**Usage:**
```powershell
.\scripts\setup-grafana.ps1
```

**What it does:**
1. Waits for Grafana to be ready
2. Configures Prometheus as data source
3. Imports dashboard from `docs/grafana-dashboard.json`

**Requirements:**
- Docker Compose must be running
- Grafana accessible at http://localhost:3000

## Adding New Scripts

When adding new scripts:
1. Place them in this folder
2. Document them in this README
3. Use clear naming: `action-description.ext`
4. Add usage examples

## Script Guidelines

- **PowerShell scripts**: Use `.ps1` extension
- **Bash scripts**: Use `.sh` extension
- **Python scripts**: Use `.py` extension
- Always include help text or comments
- Test on clean environment before committing
