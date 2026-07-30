# 03. Escáner de Cuadrícula Espacial

## Cuadrícula de 35 Sectores WGS84
El área monitoreada (La Serena, Chile) se divide en 35 sectores distintos utilizando coordenadas WGS84. Este enfoque granular y detallado, sumado a una ventana de pronóstico extendida (lead time) de 6 a 12 horas, permite emitir advertencias de riesgo altamente localizadas.

## Tiempos de Concentración
Para cada sector, se calcula el Tiempo de Concentración (Tc). Este es el tiempo requerido para que la escorrentía viaje desde el punto hidráulicamente más distante de la cuenca hasta el punto de interés (el sector en cuestión).

## Recuperación y Calma (Clearance Recovery)
El sistema modela la fase de recuperación y limpieza, prediciendo cuándo un área volverá a ser segura después de un evento de inundación. Esto contribuye directamente al cálculo de la "Hora de Paso Seguro / Calma" (ETA Clearance).
