# 01. Visión General de la Arquitectura

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


[[10_Projects/Proyecto_Centinela/README.md]]

---
🔗 [[Home]]
