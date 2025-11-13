# 📊 Configuración Manual de Grafana - Paso a Paso Visual

## INSTRUCCIÓN RÁPIDA: SIN CÓDIGO

Simplemente sigue estos 5 pasos en Grafana:

### PASO 1️⃣: Abre Grafana
```
http://localhost:3000
Admin / admin
```

### PASO 2️⃣: Data Source

1. Click en **⚙️ Settings** (barra izquierda)
2. Click en **Data Sources**
3. Click en **+ Add data source** (arriba a la derecha)
4. Click en **Prometheus**

Completa:
- **Name**: `Prometheus`
- **URL**: `http://prometheus:9090`
- **Access**: `Server` (en el dropdown)

Click **Save & test** (abajo)

Expected: ✅ **"Data source is working"**

---

### PASO 3️⃣: Dashboard

1. Click en **+** (barra izquierda)
2. Click en **New** (si aparece) o **Create Dashboard**
3. Click en **Add a new panel**

---

### PASO 4️⃣: Panel 1 - Total Requests

En la nueva pantalla:

**Arriba a la izquierda** donde dice **Prometheus** → Verifica que diga **"Prometheus"**

**En el área de PromQL** (donde dice "Run queries"), pega:
```
sum(rate(todo_api_request_count_total[5m]))
```

**Abajo a la derecha**, en el panel **Options**:
- **Title**: `Requests Per Second`
- **Type**: `Gauge`

Click **Apply**

---

### PASO 5️⃣: Agregar más Panels (Opcional)

Si quieres más gráficos:

1. Click **+ Add panel**
2. Pega otra query:

```promql
# Errors per second
sum(rate(todo_api_error_count_total[5m]))
```

3. Cambia **Title** y **Type** según necesites

---

## ✅ RESULTADO ESPERADO

Deberías ver:
- ✓ Números en los gauges
- ✓ Gráficos actualizándose en tiempo real
- ✓ Líneas subiendo y bajando

---

## ❌ SI NO FUNCIONA

### Opción A: Verificar Prometheus
1. Abre http://localhost:9090
2. Busca: `todo_api_request_count_total`
3. Click **Execute**
4. ¿Ves resultados? → Si sí, recarga Grafana (F5)

### Opción B: Hacer más requests
```powershell
for ($i = 1; $i -le 30; $i++) { 
    Invoke-WebRequest -Uri "http://localhost:8080/api/v1/tasks" -UseBasicParsing | Out-Null
}
```
Luego espera 20 segundos y actualiza Grafana.

### Opción C: Reiniciar todo
```powershell
docker-compose down
docker-compose up -d
```

---

## 📚 Queries de Ejemplo

Copia y pega en Grafana:

```promql
# Total requests
sum(rate(todo_api_request_count_total[5m]))

# Errors
sum(rate(todo_api_error_count_total[5m]))

# Por endpoint
rate(todo_api_request_count_total[5m])

# Error rate %
(sum(rate(todo_api_error_count_total[5m])) / sum(rate(todo_api_request_count_total[5m]))) * 100

# Latencia
rate(todo_api_request_latency_seconds_sum[5m]) / rate(todo_api_request_latency_seconds_count[5m])
```

---

¿Funcionó? 🎉

