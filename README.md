# DevOps Final Project 🚀

Este proyecto es una aplicación **Flask** sencilla que sirve como laboratorio de prácticas de DevOps.  
Su objetivo es demostrar cómo integrar una aplicación web con **Prometheus**, **Grafana**, **Node Exporter** y **Alertmanager** para monitorización y alertas, además de aplicar buenas prácticas de contenedores, CI/CD y calidad de código.

---

## Mienbros del grupo:
 - **Nombre:** Miembro 1  
   **Correo:** miembro.1z@ctag.com
 - **Nombre:** Miembro 2  
   **Correo:** miembro.2z@ctag.com
 - **Nombre:** Miembro 3  
   **Correo:** miembro.3z@ctag.com
 - **Nombre:** Miembro 4  
   **Correo:** miembro.4@ctag.com

---

## 📌 Características principales
- Aplicación web en **Python/Flask** con endpoints:
  - `/` → saludo y contador de visitas.
  - `/health` → estado de salud.
  - `/info` → información de la aplicación.
  - `/calculate` → cálculo con latencia simulada.
- Métricas expuestas en formato **Prometheus**:
  - `app_visits_total`: contador de visitas.
  - `app_errors_total`: contador de errores.
  - `request_latency_seconds`: histograma de latencia por endpoint.
  - `calculate_duration_seconds`: histograma de duración del cálculo.
- **Dockerfile** para construir la imagen de la aplicación.
- **docker-compose.yml** para levantar la aplicación.
- **docker-compose.monitoring.yml** para desplegar Prometheus, Grafana, Node Exporter y Alertmanager.
- Dashboards de Grafana preconfigurados para visualizar métricas.
- Workflows de CI/CD y análisis de calidad con SonarQube.

---

## 📂 Estructura del proyecto

```bash
devops-final-project/
├── app.py                         # Aplicación principal Flask
├── Dockerfile                     # Imagen Docker para la app
├── docker-compose.yml             # Despliegue de la app Flask
├── docker-compose.monitoring.yml # Stack de monitorización (Prometheus, Grafana, etc.)

├── prometheus/
│   ├── prometheus.yml             # Configuración de Prometheus
│   ├── alert.rules.yml            # Reglas de alerta Prometheus
│   └── alertmanager.yml           # Configuración de Alertmanager

├── grafana/
│   └── dashboard.json             # Dashboard de Grafana con paneles predefinidos

├── tests/
│   └── test_app.py                # Pruebas unitarias para la app Flask

├── .github/
│   └── workflows/
│       └── ci.yml                 # Workflow de CI/CD con GitHub Actions

└── README.md                      # Documentación del proyecto

```

---

## 🚀 Instalación y ejecución

### 1. Construir la imagen de la aplicación
```bash
docker build -t flask-app:latest .
```

### 2. Lanzar la aplicación
```bash
docker run -d --name flask-app -p 5000:5000 flask-app:latest
La aplicación estará disponible en http://localhost:5000.
```

### 3. Levantar el stack de monitorización
```bash
docker compose -f docker-compose.monitoring.yml up -d
Servicios desplegados:

Prometheus → http://localhost:9090

Grafana → http://localhost:3010

Node Exporter → http://localhost:9100

Alertmanager → http://localhost:9093
```

---

## 📊 Métricas Prometheus
### Aplicación Flask
 - app_visits_total → visitas acumuladas.
 - app_errors_total → errores acumulados.
 - request_latency_seconds → latencia por endpoint.
 - calculate_duration_seconds → duración del cálculo.

### Node Exporter
 - node_cpu_seconds_total → uso de CPU.
 - node_memory_MemAvailable_bytes → memoria disponible.
 - node_filesystem_size_bytes → tamaño de disco.
 - node_network_receive_bytes_total / node_network_transmit_bytes_total → tráfico de red.

---

## 🚨 Alertas configuradas
En alert.rules.yml se definen reglas como:
 - HighRequestLatency → latencia p95 > 2s.
 - HighErrorRate → tasa de errores > 0.1 req/s.
 - HighCPUUsage → CPU > 80%.
 - LowMemoryAvailable → memoria disponible < 20%.
 - HighDiskUsage → disco > 85%.

Alertmanager recibe estas alertas y las envia grafana.

---

## 📈 Dashboard Grafana
El dashboard (grafana/dashboard.json) incluye paneles para:
 - Total de visitas y errores.
 - Requests por endpoint.
 - Latencia promedio y percentiles.
 - Duración del cálculo.
 - Uso de CPU, memoria, disco y red (Node Exporter).
 - Estado de las alertas (Alertmanager).

---

## 🛠️ CI/CD y calidad
 - GitHub Actions: workflows en .github/workflows para integración continua.
 - SonarQube: análisis estático de calidad de código.
 - Docker: despliegue reproducible y portable.

---
