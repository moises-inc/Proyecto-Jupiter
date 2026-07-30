---
id: 20260730-planificacion-modelo-ml-satelital
title: Planificación del Modelo de Machine Learning Satelital — Proyecto Centinela
proyecto: Proyecto_Centinela
fecha: 2026-07-30
type: technical-note
status: en-proceso
tags: [centinela, ml, machine-learning, satelital, la-serena, agosto-2026, desarrollo]
---

# 🧠 Planificación del Modelo de Machine Learning Satelital (Pruebas Agosto 2026)

Este documento establece la hoja de ruta técnica, arquitectura de datos y estrategia de validación para el desarrollo del **Modelo de Machine Learning de Alerta Temprana del Proyecto Centinela**, basado **exclusivamente en datos satelitales y teledetección NRT (Near Real-Time)**, diseñado para ser probado durante los eventos de lluvias extremas proyectados para **finales de agosto de 2026** en La Serena y la Región de Coquimbo.

---

## 🎯 1. Contexto y Decisión Estratégica (Feedback Bomberos)

Tras la reunión con el equipo de Bomberos y expertos en el Sistema de Comando de Incidentes (SCI):
1. **Validación del Concepto:** Se confirmó que la solución es inédita a nivel local en La Serena y ataca los problemas críticos de prevención y gestión de emergencias.
2. **Pivote Operacional Temporal:** Debido a la urgencia de probar la herramienta en las lluvias intensas de **finales de agosto de 2026** y a la falta de sensores físicos IoT desplegados en terreno, el modelo se construirá **100% analizando datos satelitales NRT y teledetección abierta**.
3. **Plazo de Ejecución:** ~3 a 4 semanas de desarrollo e integración antes de la llegada del frente de mal tiempo.

---

## 🛰️ 2. Fuentes de Datos Satelitales y Meteorológicos NRT

```mermaid
graph TD
    subgraph "Fuentes Satelitales & NRT (Entradas)"
        A[Open-Meteo API / NRT Reanalysis] -->|Precipitación, T°, Viento, Humedad| D[Pipeline de Ingesta Python]
        B[GOES-19 ABI / RRQPE] -->|Tasa de Lluvia Instantánea 10 min| D
        C[GPM IMERG Early Run] -->|Precipitación Acumulada 30 min| D
    end

    subgraph "Ingeniería de Características (Features)"
        D --> E[Índice Precipitación Antecedente - API 24/72/120h]
        D --> F[Estimación Isoterma Cero Alta]
        D --> G[Delta de Torrencialidad 3h / 6h]
    end

    subgraph "Modelo Predictivo (Inferencia)"
        E --> H[Modelo Scikit-Learn / XGBoost]
        F --> H
        G --> H
        H --> I[Score de Riesgo 0-100%]
        H --> J[Semáforo por Sector: Verde / Amarillo / Rojo]
    end
```

### Variables de Entrada del Modelo ($X$):
1. **Precipitación Acumulada Móvil:** 1h, 3h, 6h, 12h, 24h, 72h y 120h ($mm$).
2. **Índice de Precipitación Antecedente (API):** $API_t = P_t + k \cdot API_{t-1}$ (mide saturación previa del suelo).
3. **Tasa de Lluvia Instantánea Satelital (GOES-19 RRQPE):** $mm/h$.
4. **Isoterma Cero Estimada:** Altitud ($m.n.m.$) para prever escorrentía líquida en alta cordillera.
5. **Velocidad y Ráfagas de Viento:** $km/h$ (para estimación indirecta de riesgo de caídas).

### Variables de Salida ($Y$):
- **Continuous Overflow Risk Score ($0.0 - 1.0$):** Probabilidad de desborde/aluvión en cuencas críticas (Río Elqui y Quebrada Santa Gracia/Pueblo Islón).
- **Semáforo Táctico SCI:** `VERDE` (Estable), `AMARILLO` (Preparación/Pre-alerta), `ROJO` (Evacuación/Riesgo Inminente).

---

## 🗓️ 3. Cronograma de Desarrollo (4 Semanas)

```mermaid
gantt
    title Hoja de Ruta - Modelo ML Satelital Centinela (Agosto 2026)
    dateFormat  YYYY-MM-DD
    section Semana 1: Data Ingestion
    API Open-Meteo & Sat Ingester         :active, w1a, 2026-07-30, 7d
    Dataset Histórico (Julio 2026)       :w1b, 2026-08-01, 5d
    section Semana 2: Features & ML
    Feature Engineering (API, Isoterma)  :w2a, 2026-08-06, 5d
    Entrenamiento RandomForest/XGBoost   :w2b, 2026-08-09, 5d
    section Semana 3: Backtesting & Tuning
    Validación con Temporal Julio 2026    :w3a, 2026-08-14, 5d
    Optimizador de Umbrales SCI          :w3b, 2026-08-17, 5d
    section Semana 4: Monitoreo Vivo
    Script Inferencia NRT Final          :w4a, 2026-08-20, 5d
    Monitoreo Evento de Lluvias Agosto   :w4b, 2026-08-23, 8d
```

---

## 🛠️ 4. Arquitectura de Archivos en `/ML_Models/`

```
ML_Models/
├── data/
│   ├── raw/                 # Archivos CSV/JSON de descargas de Open-Meteo y Satélites
│   └── processed/           # Datasets procesados con features calculadas
├── src/
│   ├── ingesters/           # ingester_open_meteo.py, ingester_goes19.py
│   ├── features/            # feature_engineering.py
│   ├── models/              # train_model.py, evaluate_model.py
│   └── inference/           # run_live_prediction.py
├── trained_models/          # centinela_floods_v1.joblib
└── requirements.txt         # pandas, numpy, scikit-learn, xgboost, joblib, requests
```

---

## 🧪 5. Criterios de Éxito para las Pruebas de Agosto

1. **Backtesting Exitoso:** Al correr el modelo con los datos del 19 de julio de 2026 (aluvión de Pueblo Islón), el modelo debe haber marcado `ROJO` con **al menos 3 horas de anticipación**.
2. **Cero Fallos de Memoria:** Inferencia ejecutable en CPU con consumo $<100$ MB de RAM y tiempo de respuesta $<1$ segundo.
3. **Evaluación en Tiempo Real en Agosto:** Generar reportes diarios/horarios durante el evento de finales de agosto, comparando las alertas del modelo contra lo observado en terreno por Bomberos.

---

## 🔗 Enlaces y Contexto
🔗 [[10_Projects/Proyecto_Centinela/Docs/Proyecto_Centinela_OnePager|One-Pager Proyecto Centinela]] | 🔗 [[10_Projects/Proyecto_Centinela/Docs/Estudio_Caso_La_Serena_Lluvias|Estudio Caso La Serena]] | 🔗 [[90_System/Agent_Sync/Active_Context|Contexto Activo]]
