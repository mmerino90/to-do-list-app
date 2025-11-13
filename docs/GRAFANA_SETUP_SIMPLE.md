# Configuración Rápida de Grafana - Paso a Paso

## 1. Acceder a Grafana
1. Abre: **http://localhost:3000**
2. Login:
   - Usuario: `admin`
   - Contraseña: `admin`

---

## 2. Agregar Data Source (Prometheus)

### Paso 1: Ir a Settings
- Haz click en el icono de **engranaje** (⚙️) en la barra izquierda
- Selecciona **Data Sources**

### Paso 2: Crear nueva Data Source
- Click en **+ Add data source**
- Selecciona **Prometheus**

### Paso 3: Configurar Prometheus
Completa estos campos:

| Campo | Valor |
|-------|-------|
| Name | `Prometheus` |
| URL | `http://prometheus:9090` |
| Access | `Server` |

### Paso 4: Guardar
- Click en **Save & test**
- Deberías ver: ✓ "Data source is working"

---

## 3. Importar Dashboard

### Opción Rápida (Recomendada):

1. Ve a: **http://localhost:3000/admin/users** (ignora este error si aparece)

2. Click en el icono **"+"** en la barra izquierda

3. Selecciona **Import**

4. En el campo de texto **JSON Dashboard**:
   - Abre el archivo: `docs/grafana-dashboard.json`
   - Copia TODO el contenido
   - Pégalo en el cuadro de texto

5. Click fuera del texto para validar

6. Deberías ver un preview del dashboard

7. En **Select the Prometheus data source**:
   - Elige **Prometheus**

8. Click en **Import**

---

## 4. Ver el Dashboard

Después de importar, deberías ver los gráficos con datos:

✅ **Requests Per Second** - Gauge con número
✅ **Error Rate** - Gauge con porcentaje  
✅ **P95 Latency** - Gauge con tiempo
✅ **Request Rate by Endpoint** - Línea con datos
✅ **Error Rate by Endpoint** - Línea
✅ **HTTP Status Distribution** - Barras
✅ **Latency Percentiles** - Múltiples líneas

---

## Troubleshooting Rápido

### Si no ves datos después de importar:

1. **Verifica que Prometheus tenga datos:**
   - Abre: http://localhost:9090
   - Escribe en el search: `todo_api_request_count_total`
   - Click en **Execute**
   - Deberías ver resultados

2. **Si Prometheus está vacío:**
   - Haz más requests al API:
   ```bash
   # PowerShell
   for ($i = 1; $i -le 10; $i++) { 
       Invoke-WebRequest -Uri "http://localhost:8080/api/v1/tasks" -UseBasicParsing
       Start-Sleep -Milliseconds 200
   }
   ```
   - Espera 20 segundos
   - Vuelve a revisar Prometheus

3. **Si aún sin datos en Grafana:**
   - Recarga la página del dashboard (F5)
   - Verifica que la data source sea "Prometheus" (icono verde al lado del nombre)
   - Si no sale verde, re-conecta la data source

---

## URLs Útiles

- **Grafana Home**: http://localhost:3000
- **Prometheus**: http://localhost:9090
- **API Health**: http://localhost:8080/api/v1/health
- **API Metrics**: http://localhost:8080/api/v1/metrics

