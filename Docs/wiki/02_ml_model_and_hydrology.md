# 02. Modelo de Machine Learning e Hidrología

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
