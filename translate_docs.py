import os

base_dir = '/mnt/9b846436-0407-4e80-b8af-5417ffbdee8e/ObsidianVault/10_Projects/Proyecto_Centinela'
agent_sync_dir = '/mnt/9b846436-0407-4e80-b8af-5417ffbdee8e/ObsidianVault/90_System/Agent_Sync'

readme_content = """# ⚡ Proyecto Júpiter: Sistema de Alerta Temprana e Inteligencia Hidrometeorológica

Inspirado en Júpiter Pluvio (dios romano de la lluvia y las nubes). Este proyecto es un sistema de alerta temprana e inteligencia hidrometeorológica en tiempo real para La Serena, Chile, utilizando datos satelitales.

## Arquitectura del Sistema

```mermaid
graph TD
    A[Ingesta de Datos] --> B[Ingeniería de Características]
    B -->|SCS-CN y Tiempo de Anticipación del Pronóstico| C[Clasificador ML]
    C -->|Ensemble de Random Forest| D[Escáner Espacial]
    D -->|Cuadrícula de 20 Sectores WGS84| E[Dashboard Dual]
    E --> F[Dashboard en Tiempo Real]
    E --> G[Dashboard de Demostración]
```

## Detalles de Machine Learning (Aprendizaje Automático)
El sistema utiliza un enfoque de Machine Learning para la predicción de inundaciones:
- **Características**: Incluye varios parámetros hidrometeorológicos.
- **Modelo**: Ensemble de Random Forest (Bosque Aleatorio) para una clasificación robusta.
- **Hidrología**: Integra la fórmula hidrológica SCS-CN (Curve Number o Número de Curva del Servicio de Conservación de Suelos) para la estimación de escorrentía.
- **Estimaciones de Tiempo (Lead Time Forecast)**: 
  - Pronósticos de anticipación de +1h, +3h y +6h.
  - Calcula la **Llegada del Pico** (ETA Peak - tiempo estimado para la inundación máxima).
  - Calcula la **Hora de Paso Seguro / Calma** (ETA Clearance - cuando las aguas retroceden a niveles seguros).

## Guía de Instalación y Ejecución Local

1. Clonar el repositorio.
2. Instalar las dependencias (por ejemplo, `pip install -r requirements.txt`).
3. Ejecutar el servidor:
   ```bash
   python3 server.py
   ```
4. Acceder a los paneles de control (dashboards):
   - Tiempo Real: `http://localhost:8000/`
   - Demostración: `http://localhost:8000/demo`

## Suite de PyTest
Para ejecutar las pruebas automatizadas (automated tests):
```bash
pytest tests/ -v
```
"""

wiki_01 = """# 01. Visión General de la Arquitectura

## Diseño Completo del Sistema

El Proyecto Júpiter está diseñado como un sistema modular de alerta temprana en tiempo real.

### Componentes
1. **Ingesta de Datos**: Recopila datos satelitales e hidrometeorológicos de diversas fuentes.
2. **Ingeniería de Características**: Procesa los datos en crudo para convertirlos en características accionables (features), utilizando modelos hidrológicos como el SCS-CN.
3. **Clasificador de Machine Learning**: Un modelo de Random Forest (Bosque Aleatorio) que predice los riesgos de inundación basándose en las características generadas.
4. **Escáner Espacial**: Mapea las predicciones a través de una cuadrícula de 20 zonas con coordenadas WGS84.
5. **Dashboard (Panel de Control)**: Presenta los datos a través de una consola en Tiempo Real (NRT - Near Real-Time) y un entorno de simulación (Demo).

## Flujos de Datos
- Datos Crudos -> Módulo de Ingesta -> Datos Procesados
- Datos Procesados -> Ingeniería de Características -> Vectores de Características
- Vectores de Características -> Modelo ML -> Predicciones de Riesgo
- Predicciones de Riesgo -> Escáner Espacial -> Alertas Zonales
- Alertas Zonales -> Dashboard -> Interfaz de Usuario
"""

wiki_02 = """# 02. Modelo de Machine Learning e Hidrología

## Modelo de Random Forest (Bosque Aleatorio)
El motor predictivo central es un clasificador de Random Forest. Este método de ensamble proporciona una alta precisión y maneja de forma excelente las relaciones no lineales, lo cual es crucial para los datos meteorológicos complejos.

## Ingeniería de Características (Feature Engineering)
Las características se derivan de los datos hidrometeorológicos crudos. Las características generadas más importantes incluyen:
- Intensidad de la lluvia (mm/h)
- Precipitación acumulada
- Índice de humedad del suelo

## Hidrología de Número de Curva (SCS-CN)
El método del Número de Curva del Servicio de Conservación de Suelos (SCS-CN) se utiliza para estimar la escorrentía directa de los eventos de precipitación. Tiene en cuenta:
- Tipo de suelo
- Uso de la tierra
- Condición hidrológica

## Tiempo de Anticipación del Pronóstico (Lead Time Forecast)
El sistema calcula los tiempos de anticipación de los pronósticos (+1h, +3h, +6h), permitiendo a las autoridades prepararse con antelación. Esto incluye predecir la **Llegada del Pico** (ETA Peak - tiempo estimado para la máxima inundación) y la **Hora de Paso Seguro / Calma** (ETA Clearance - cuando el agua retrocede y es seguro retornar).
"""

wiki_03 = """# 03. Escáner de Cuadrícula Espacial

## Cuadrícula de 20 Sectores WGS84
El área monitoreada (La Serena, Chile) se divide en 20 sectores distintos utilizando coordenadas WGS84. Este enfoque granular y detallado permite emitir advertencias de riesgo altamente localizadas.

## Tiempos de Concentración
Para cada sector, se calcula el Tiempo de Concentración (Tc). Este es el tiempo requerido para que la escorrentía viaje desde el punto hidráulicamente más distante de la cuenca hasta el punto de interés (el sector en cuestión).

## Recuperación y Calma (Clearance Recovery)
El sistema modela la fase de recuperación y limpieza, prediciendo cuándo un área volverá a ser segura después de un evento de inundación. Esto contribuye directamente al cálculo de la "Hora de Paso Seguro / Calma" (ETA Clearance).
"""

wiki_04 = """# 04. Dashboard y Reportes SCI-201

## Consola en Tiempo Real (NRT)
La consola de Tiempo Casi Real (Near Real-Time o NRT) es la interfaz principal para el monitoreo activo. Muestra flujos de datos en vivo, niveles de riesgo actuales en los 20 sectores de la cuadrícula y las alertas activas en curso.

## Simulación de Demostración (Demo)
Se incluye un panel de demostración para simular eventos de inundación con fines de capacitación, entrenamiento y presentación. Utiliza datos históricos o fabricados para demostrar las capacidades del sistema sin tener que esperar a que ocurra un evento meteorológico real.

## Bitácora de Incidentes SCI-201
El sistema integra un generador automatizado de bitácoras SCI-201 (Incident Briefing o Resumen del Incidente). Esto asegura que se mantenga el estándar de informes del Sistema de Comando de Incidentes durante las emergencias, facilitando enormemente la coordinación táctica y el análisis posterior al evento.
"""

guia_operativa = """---
id: 20260730-guia-operativa-prueba-viernes
title: Guía de Operación para la Prueba en Vivo de este Viernes — Proyecto Júpiter
proyecto: Proyecto_Jupiter
fecha: 2026-07-30
type: operational-guide
status: listo
tags: [jupiter, prueba-en-vivo, lluvias-viernes, la-serena, puesto-de-mando, bomberos]
---

# 🌧️ Guía de Operación: Prueba en Vivo durante el Evento de Lluvias de este Viernes

Este documento establece la **Guía Operativa de Terreno** para poner a prueba el primer prototipo funcional del **Proyecto Júpiter** durante el frente de precipitaciones pronosticado para este **Viernes en La Serena y la Región de Coquimbo**.

---

## ⚙️ 1. Configuración del Servidor y Tasa de Ingesta NRT (5 Minutos)

El servidor ha sido configurado para ejecutar una **tarea en segundo plano cada 5 minutos (300 segundos)** que descarga los datos satelitales NRT y recalcula la matriz de riesgo para las 8 zonas de La Serena.

```mermaid
graph TD
    A[Satélites GOES-19 / GPM / Open-Meteo] -->|Cada 5 Minutos| B[Worker Background Thread server.py]
    B -->|Features & ML| C[Matriz de Riesgo 8 Zonas La Serena]
    C -->|Auto-Refresco Cada 5s| D[Dashboard Web http://localhost:8000]
    D -->|Exportar 1-Clic| E[Informe de Emergencia SCI-201 PDF]
```

---

## 📋 2. Pasos de Operación para este Viernes

### **Paso A: Iniciar la Plataforma en la Laptop**
1. Abrir la terminal y navegar a la carpeta del Dashboard:
   ```bash
   cd "/mnt/9b846436-0407-4e80-b8af-5417ffbdee8e/ObsidianVault/10_Projects/Proyecto_Centinela/Dashboard"
   ```
2. Ejecutar el servidor web local:
   ```bash
   python3 server.py
   ```
3. Abrir el navegador e ingresar a: **`http://localhost:8000`**.

---

### **Paso B: Pauta de Verificación durante la Tormenta del Viernes**

| Hora de Evaluación | Qué Observar en el Dashboard | Qué Verificar en Terreno con Bomberos |
| :---: | :--- | :--- |
| **08:00 AM (Inicio Frente)** | Confirmar que la tasa de refresco muestra `SISTEMA EN VIVO NRT (DESCARGA: CADA 5 MIN)`. | Comparar la tasa de lluvia $mm/h$ del Dashboard con las observaciones visuales del cielo y reportes radiales. |
| **12:00 PM (Pico Lluvia)** | Revisar si la Isoterma Cero sube de los $3.000 \text{ m.n.m.}$ y si el sector **Pueblo Islón / Quebrada Santa Gracia** pasa a `AMARILLO` o `ROJO`. | Consultar con Bomberos si hay aumento de caudal en el Río Elqui o quebradas. |
| **16:00 PM (Acumulado 24h)** | Verificar el Semáforo de **Pasos Bajo Nivel en Ruta 5 Km 490-500** y **Las Compañías**. | Confirmar anegamientos viales reportados en redes/radios contra la predicción del Dashboard. |

---

### **Paso C: Generación de Informe Oficial SCI-201 (PDF)**
Si durante la lluvia de este viernes el Comandante de Incidentes o la municipalidad solicita un reporte consolidado:
1. Hacer clic en el botón superior: **`📄 Generar Informe SCI-201 (PDF)`**.
2. Guardar o imprimir el PDF resumen con los 4 KPIs, el mapa de zonas y las recomendaciones tácticas.

---

## 🔗 Enlaces y Contexto
🔗 [[10_Projects/Proyecto_Centinela/Docs/diseno_dashboard_puesto_mando|Diseño Dashboard Táctico]] | 🔗 [[10_Projects/Proyecto_Centinela/Docs/planificacion_modelo_ml_satelital|Planificación ML Satelital]] | 🔗 [[90_System/Agent_Sync/Active_Context|Contexto Activo]]
"""

active_context = """# Contexto Activo — Proyecto Júpiter (Modelo ML Satelital para Agosto 2026)

**Estado:** Activo (Fase 1 - Planificación y Construcción del Modelo ML Satelital).
**Hito:** Diseño de Arquitectura de Datos, Ingesta NRT Satelital y Hoja de Ruta para Pruebas en Lluvias de Agosto.
**Agente Activo:** Antigravity 2.0 (Orquestador de Sistemas & Ingeniero de IA).

## Archivos Clave
- [planificacion_modelo_ml_satelital.md](file:///mnt/9b846436-0407-4e80-b8af-5417ffbdee8e/ObsidianVault/10_Projects/Proyecto_Centinela/Docs/planificacion_modelo_ml_satelital.md) — Planificación del Modelo ML Satelital (Pruebas Agosto 2026).
- [catálogo_satelitales_complementarios.md](file:///mnt/9b846436-0407-4e80-b8af-5417ffbdee8e/ObsidianVault/10_Projects/Proyecto_Centinela/Docs/catálogo_satelitales_complementarios.md) — Catálogo de Satélites NRT Adicionales.
- [analisis_precision_satelital_ml.md](file:///mnt/9b846436-0407-4e80-b8af-5417ffbdee8e/ObsidianVault/10_Projects/Proyecto_Centinela/Docs/analisis_precision_satelital_ml.md) — Análisis de Precisión Satelital y Mecanismo ML.
- [index_realtime.html](file:///mnt/9b846436-0407-4e80-b8af-5417ffbdee8e/ObsidianVault/10_Projects/Proyecto_Centinela/Dashboard/static/index_realtime.html) — Consola Operacional En Vivo NRT con Radar Satelital, Rutas de Evacuación, Alarma Sonora y Bitácora SCI.
- [demo.html](file:///mnt/9b846436-0407-4e80-b8af-5417ffbdee8e/ObsidianVault/10_Projects/Proyecto_Centinela/Dashboard/static/demo.html) — Consola Demostrativa Interactiva para Presentaciones ante Bomberos y Autoridades.
- [guia_operativa_prueba_viernes.md](file:///mnt/9b846436-0407-4e80-b8af-5417ffbdee8e/ObsidianVault/10_Projects/Proyecto_Centinela/Docs/guia_operativa_prueba_viernes.md) — Guía Operativa para la Prueba en Vivo de este Viernes.
- [diseno_dashboard_puesto_mando.md](file:///mnt/9b846436-0407-4e80-b8af-5417ffbdee8e/ObsidianVault/10_Projects/Proyecto_Centinela/Docs/diseno_dashboard_puesto_mando.md) — Diseño del Dashboard Táctico para Puesto de Mando (SCI).
- [spatial_scanner.py](file:///mnt/9b846436-0407-4e80-b8af-5417ffbdee8e/ObsidianVault/10_Projects/Proyecto_Centinela/ML_Models/src/inference/spatial_scanner.py) — Mapeo y Escaneo Espacial Completo (8 Zonas de La Serena).
- [Proyecto_Centinela_OnePager.md](file:///mnt/9b846436-0407-4e80-b8af-5417ffbdee8e/ObsidianVault/10_Projects/Proyecto_Centinela/Docs/Proyecto_Centinela_OnePager.md) — One-Pager del Proyecto Júpiter.
- [Estudio_Caso_La_Serena_Lluvias.md](file:///mnt/9b846436-0407-4e80-b8af-5417ffbdee8e/ObsidianVault/10_Projects/Proyecto_Centinela/Docs/Estudio_Caso_La_Serena_Lluvias.md) — Datos empíricos del Temporal de La Serena (Julio 2026).
- [diseno_presentacion_latex.md](file:///mnt/9b846436-0407-4e80-b8af-5417ffbdee8e/ObsidianVault/10_Projects/Proyecto_Centinela/Docs/diseno_presentacion_latex.md) — Diseño de Presentación Beamer & TikZ para Bomberos.
- [Task_Board.md](file:///mnt/9b846436-0407-4e80-b8af-5417ffbdee8e/ObsidianVault/90_System/Agent_Sync/Task_Board.md) — Tablero de Tareas Abiertas.

## Resumen del Trabajo en Curso
1. **Validación Positiva con Bomberos:** La propuesta fue acogida con gran entusiasmo por el equipo de Bomberos y SCI de La Serena, destacando que es un enfoque inédito y de alto valor para la gestión local.
2. **Pivote a Modelo ML Satelital NRT:** Se acordó priorizar al 100% la creación del modelo de Machine Learning basado exclusivamente en datos satelitales (GOES-19, GPM IMERG, Open-Meteo NRT) postergando los sensores físicos IoT.
3. **Horizonte de Pruebas (Finales de Agosto 2026):** Se proyecta completar el entrenamiento, calibración con datos de julio y empaquetado del script de inferencia en ~3 semanas para poner a prueba el modelo durante los eventos de lluvias intensas de finales de agosto.

---
🔗 [[10_Projects/Proyecto_Centinela/Docs/planificacion_modelo_ml_satelital|Planificación ML Satelital]] | 🔗 [[90_System/Agent_Sync/Task_Board|Task Board]]
"""

import codecs

files_to_write = {
    os.path.join(base_dir, 'README.md'): readme_content,
    os.path.join(base_dir, 'Docs/wiki/01_architecture_overview.md'): wiki_01,
    os.path.join(base_dir, 'Docs/wiki/02_ml_model_and_hydrology.md'): wiki_02,
    os.path.join(base_dir, 'Docs/wiki/03_spatial_grid_scanner.md'): wiki_03,
    os.path.join(base_dir, 'Docs/wiki/04_dashboard_and_sci201.md'): wiki_04,
    os.path.join(base_dir, 'Docs/guia_operativa_prueba_viernes.md'): guia_operativa,
    os.path.join(agent_sync_dir, 'Active_Context.md'): active_context,
}

for path, content in files_to_write.items():
    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Translation completed successfully.")
