#!/usr/bin/env powershell
# Script para configurar Grafana automáticamente

$GRAFANA_URL = "http://localhost:3000"
$PROMETHEUS_URL = "http://prometheus:9090"

Write-Host "🔧 Configurando Grafana automáticamente..." -ForegroundColor Cyan
Write-Host ""

# 1. Crear Data Source
Write-Host "1. Agregando Prometheus como Data Source..." -ForegroundColor Yellow

$datasource = @{
    name = "Prometheus"
    type = "prometheus"
    url = $PROMETHEUS_URL
    access = "proxy"
    isDefault = $true
    jsonData = @{}
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$GRAFANA_URL/api/datasources" `
        -Method POST `
        -Headers @{
            "Content-Type" = "application/json"
            "Authorization" = "Bearer admin:admin"
        } `
        -Body $datasource `
        -UseBasicParsing
    
    Write-Host "   ✓ Data Source creada: $($response.StatusCode)" -ForegroundColor Green
    $dsid = ($response.Content | ConvertFrom-Json).id
    Write-Host "   ✓ Data Source ID: $dsid" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Error: $_" -ForegroundColor Red
}

Write-Host ""

# 2. Crear Dashboard
Write-Host "2. Creando Dashboard..." -ForegroundColor Yellow

$dashboard = @{
    dashboard = @{
        title = "To-Do App Metrics"
        tags = @("todo-app", "monitoring")
        timezone = "browser"
        panels = @(
            @{
                id = 1
                title = "Requests Per Second"
                type = "gauge"
                gridPos = @{x=0; y=0; w=6; h=8}
                targets = @(@{expr="sum(rate(todo_api_request_count_total[5m]))"})
                fieldConfig = @{
                    defaults = @{
                        color = @{mode="thresholds"}
                        unit = "reqps"
                    }
                }
            },
            @{
                id = 2
                title = "Errors Per Second"
                type = "gauge"
                gridPos = @{x=6; y=0; w=6; h=8}
                targets = @(@{expr="sum(rate(todo_api_error_count_total[5m]))"})
                fieldConfig = @{
                    defaults = @{
                        color = @{mode="thresholds"}
                        unit = "errps"
                    }
                }
            },
            @{
                id = 3
                title = "Request Timeline"
                type = "timeseries"
                gridPos = @{x=0; y=8; w=12; h=8}
                targets = @(@{expr="rate(todo_api_request_count_total[5m])"})
            }
        )
        schemaVersion = 38
        version = 0
    }
    overwrite = $true
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-WebRequest -Uri "$GRAFANA_URL/api/dashboards/db" `
        -Method POST `
        -Headers @{
            "Content-Type" = "application/json"
            "Authorization" = "Bearer admin:admin"
        } `
        -Body $dashboard `
        -UseBasicParsing
    
    Write-Host "   ✓ Dashboard creado: $($response.StatusCode)" -ForegroundColor Green
    $dashboard_url = ($response.Content | ConvertFrom-Json).url
    Write-Host "   ✓ URL: $GRAFANA_URL$dashboard_url" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Error: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "✅ Configuración completada!" -ForegroundColor Green
Write-Host ""
Write-Host "Abre Grafana:" -ForegroundColor Cyan
Write-Host "   $GRAFANA_URL" -ForegroundColor White

