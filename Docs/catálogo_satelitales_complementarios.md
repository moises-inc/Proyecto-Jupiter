---
id: 20260730-catalogo-satelitales-complementarios
title: Catálogo de Satélites Complementarios y Fuentes Abiertas NRT — Proyecto Centinela
proyecto: Proyecto_Centinela
fecha: 2026-07-30
type: technical-note
status: listo
tags: [centinela, satelites, goes-18, smap, swot, jpss, sentinel-3, sentinel-6, nrt, datos-abiertos]
---

# 📡 Catálogo de Constelaciones Satelitales Complementarios para Monitoreo NRT

Este documento presenta un inventario exhaustivo de **constelaciones satelitales adicionales y de acceso abierto** que pueden integrarse al pipeline de datos del **Proyecto Centinela** para maximizar la cobertura, precisión física y velocidad de actualización durante catástrofes hidrometeorológicas.

---

## 🌎 1. Satélites Geoestacionarios del Pacífico (Monitoreo del Origen de Tormentas)

### **GOES-18 (NOAA - GOES-West)**
- **Ubicación Orbital:** Cobertura directa sobre el Océano Pacífico Este (ranura $137.2^\circ \text{W}$).
- **Valor para Centinela:** Mientras GOES-19 observa desde la ranura Este, GOES-18 detecta los **ríos atmosféricos y sistemas frontales fríos en pleno Océano Pacífico**, hasta 24 a 48 horas antes de que toquen la costa de la Región de Coquimbo.
- **Frecuencia / Latencia:** Imágenes cada **10 minutos** con disponibilidad en **$< 15$ minutos**.

---

## 💧 2. Satélites de Medición Directa de Humedad de Suelo

### **SMAP (NASA - Soil Moisture Active Passive)**
- **Sensor:** Radiómetro de microondas en Banda L ($1.41 \text{ GHz}$).
- **Valor para Centinela:** Entrega mediciones físicas directas del porcentaje de agua en los primeros 5 cm de suelo a nivel regional. Elimina la necesidad de "adivinar" la saturación de la tierra mediante modelos teóricos.
- **Frecuencia / Latencia NRT:** Cobertura global cada 2-3 días; los productos **SMAP NRT de NASA LANCE** se distribuyen entre **90 a 120 minutos** tras la pasada del satélite.

---

## 🌊 3. Satélites de Altimetría Hidrológica y Ríos

### **SWOT (NASA / CNES - Surface Water and Ocean Topography)**
- **Sensor:** Interferómetro de radar de apertura sintética en Banda Ka (KaRIn).
- **Valor para Centinela:** Mide con precisión centimétrica la altura y volumen de agua en ríos de más de 100 metros de ancho, lagos y embalses (ej: Embalse Puclaro y Embalse La Laguna en el Valle del Elqui).
- **Frecuencia:** Revisitamiento de 21 días (usado para calibrar el volumen base de embalses pre-tormenta).

### **Sentinel-3A/3B (ESA) & Sentinel-6 Michael Freilich (ESA/NASA)**
- **Sensor:** Altimétros de radar SAR (SRAL / Poseidon-4) y Radiómetro de Microondas AMR-C.
- **Valor para Centinela:** El producto temático de hidrología Sentinel-3 (SR_2_LAN_HY) entrega variaciones del nivel de agua en ríos y espejos de agua continentales en **menos de 3 horas** (NRT). Sentinel-6 entrega gránulos de 10 minutos en $< 3$ horas.

---

## 🌪️ 4. Satélites de Ríos Atmosféricos y Perfiles de Humedad

### **Constelación JPSS (NOAA-20 & NOAA-21 / SNPP)**
- **Sensores:**
  - *ATMS (Advanced Technology Microwave Sounder):* Radiómetro de microondas que mide la humedad y temperatura en toda la columna vertical de la atmósfera. Mapea el **Agua Precipitable Total (Vapor Integrado - IVT)**.
  - *VIIRS (Visible Infrared Imaging Radiometer Suite):* Genera mapas diarios y horarios acumulados de desbordes e inundaciones (VCDWDG NRT) a $250 \text{ m}$ de resolución.
- **Frecuencia / Latencia:** La separación de 50 minutos entre NOAA-20 y NOAA-21 permite observaciones continuas con latencia **$< 3 \text{ horas}$**.

### **Terra & Aqua (NASA - MODIS)**
- **Valor para Centinela:** A través de la plataforma NASA LANCE, entregan detecciones NRT de inundaciones y focos de anomalías térmicas en incendios con latencia **$< 3 \text{ horas}$** (y procesamientos ultra-real time URT en $< 60$ segundos).

---

## 📊 Matriz Resumen de Nuevos Satélites Incorporables

| Satélite / Misión | Agencia | Variable Física Clave | Frecuencia Captura | Latencia NRT | Aporte Directo al Modelo Centinela |
| :--- | :---: | :--- | :---: | :---: | :--- |
| **GOES-18** | NOAA | Tasa Lluvia Instantánea en Océano | 10 min | $< 15$ min | Rastrea el avance del frente desde el Pacífico hacia La Serena. |
| **SMAP** | NASA | Humedad Superficial de Suelo (0-5cm) | 2-3 días | **90-120 min** | Calibra el índice de lodosidad y absorción antes de la lluvia. |
| **JPSS (NOAA-20/21)** | NOAA/NASA | Vapor de Agua Total (IVT) / Inundación | 50 min entre pasadas | $< 3$ horas | Detecta si viene un "Río Atmosférico" de alta torrencialidad. |
| **Sentinel-3 / 6** | ESA/NASA | Altimetría NRT de Ríos y Embalses | Gránulos 10 min | $< 3$ horas | Monitorea el volumen en embalses Puclaro y La Laguna. |
| **Terra / Aqua** | NASA | Mapas NRT de Inundación / Reflectancia | Diaria / Horaria | $< 3$ horas | Delimita áreas inundadas en valles mediante NASA LANCE. |

---

## 🔗 Enlaces y Contexto
🔗 [[10_Projects/Proyecto_Centinela/Docs/planificacion_modelo_ml_satelital|Planificación ML Satelital]] | 🔗 [[10_Projects/Proyecto_Centinela/Docs/Investigación de Datos Satelitales en Tiempo Real|Investigación Satelital NRT]] | 🔗 [[90_System/Agent_Sync/Active_Context|Contexto Activo]]


[[10_Projects/Proyecto_Centinela/README.md]]
