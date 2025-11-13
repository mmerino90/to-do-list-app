# ⚡ Configuración Inmediata de Grafana (5 minutos)

## PASO 1: Abre Grafana
```
http://localhost:3000
```
- Usuario: `admin`
- Contraseña: `admin`

---

## PASO 2: Configura Data Source (2 minutos)

1. **Click en el icono ⚙️ (Settings)** en la barra izquierda
2. **Click en Data Sources**
3. **Click en "+ Add data source"**
4. Busca y **selecciona "Prometheus"**

### Llena los campos:
```
Name:              Prometheus
URL:               http://prometheus:9090
Access:            Server
Scrape interval:   15s
```

5. **Scroll down** y click en **"Save & test"**
6. Deberías ver: ✅ **"Data source is working"**

---

## PASO 3: Crear Dashboard Manualmente (3 minutos)

### Opción A: Dashboard Simple (RECOMENDADO)

1. Click en **"+"** en la barra izquierda
2. Click en **"Import"**
3. Pega el siguiente JSON en el cuadro grande:

```json
{
  "dashboard": {
    "title": "To-Do App Metrics",
    "panels": [
      {
        "title": "Total Requests",
        "targets": [
          {
            "expr": "sum(rate(todo_api_request_count_total[5m]))"
          }
        ],
        "type": "gauge"
      },
      {
        "title": "Errors",
        "targets": [
          {
            "expr": "sum(rate(todo_api_error_count_total[5m]))"
          }
        ],
        "type": "gauge"
      },
      {
        "title": "Request Timeline",
        "targets": [
          {
            "expr": "rate(todo_api_request_count_total[5m])"
          }
        ],
        "type": "timeseries"
      }
    ]
  }
}
```

4. Selecciona **"Prometheus"** como data source
5. Click **"Import"**

### Opción B: Dashboard Alternativo

Si la opción A no funciona:

1. Abre: `docs/grafana-dashboard-simple.json`
2. Copia TODO el contenido
3. En Grafana: Click **"+"** → **"Import"**
4. Pega el JSON
5. Click **"Import"**

---

## PASO 4: Generar Datos (1 minuto)

Para que veas datos en los gráficos, haz requests a tu API:

```powershell
# Haz 10 requests
for ($i = 1; $i -le 10; $i++) {
    Invoke-WebRequest -Uri "http://localhost:8080/api/v1/tasks" -UseBasicParsing | Out-Null
    Start-Sleep -Milliseconds 200
}
```

---

## PASO 5: Visualiza en Grafana

1. Abre el dashboard que creaste
2. Espera 20 segundos (tiempo que tarda Prometheus en scrapear)
3. Deberías ver los gráficos con **datos reales** 📊

---

## ✅ Verificación Rápida

### Si FUNCIONA:
- ✓ Ves números en los "gauges"
- ✓ Ves líneas en los gráficos
- ✓ Los datos se actualizan cada 5 segundos

### Si NO FUNCIONA:

**Verifica Prometheus directamente:**
1. Abre: http://localhost:9090
2. En el buscador, escribe: `todo_api_request_count_total`
3. Click **"Execute"**

Si ves resultados → El problema está en Grafana (reinicia la página)
Si NO ves resultados → Haz más requests a la API y espera 20 segundos

---

## URLs Importantes

| Servicio | URL | Usuario | Contraseña |
|----------|-----|---------|-----------|
| Grafana | http://localhost:3000 | admin | admin |
| Prometheus | http://localhost:9090 | - | - |
| API | http://localhost:8080 | - | - |
| API Tasks | http://localhost:8080/api/v1/tasks | - | - |
| API Metrics | http://localhost:8080/api/v1/metrics | - | - |

---

## Troubleshooting

### "No data in time range"
→ Haz más requests a la API y espera 20 segundos

### "Data source is not available"
→ Ve a Settings → Data Sources → Verifica "Prometheus" esté verde ✓

### "Error loading query"
→ Recarga la página (F5)

### Grafana se ve roto
→ Limpia cache: Ctrl+Shift+Delete → Refresca

---

## Queries Útiles para Copiar/Pegar

```promql
# Total requests per second
sum(rate(todo_api_request_count_total[5m]))

# Total errors per second
sum(rate(todo_api_error_count_total[5m]))

# Error rate percentage
(sum(rate(todo_api_error_count_total[5m])) / sum(rate(todo_api_request_count_total[5m]))) * 100

# Requests by endpoint
rate(todo_api_request_count_total[5m])

# All request counts
todo_api_request_count_total
```

---

¿Completaste todos los pasos? 🚀

