# 📘 Bitácora de Hallazgos, Correcciones y Lecciones Aprendidas (Post-Fase de Prueba)
**Proyecto Júpiter — Sistema de Alerta Temprana e Inteligencia Hidrometeorológica**  
**Área de Cobertura:** La Serena / Valle del Elqui  
**Período de Prueba Real:** 30 de Julio a 01 de Agosto de 2026  

---

## 📌 1. Objetivos de esta Bitácora
Esta nota documenta de manera sistemática y continua todos los hallazgos técnicos, errores detectados en tiempo real, ajustes matemáticos de calibración e integración de nuevas fuentes de datos durante la **Fase de Prueba Real en Terreno**. Su propósito es servir como insumo principal para el análisis post-evento junto a Bomberos, la COGRID y el equipo de desarrollo.

---

## 🛠️ 2. Registro Sistemático de Hallazgos y Correcciones

### 🔴 Hallazgo 1: Sobreescala y Falsa Alerta Roja por Corrección EnKF No Normalizada
- **Fecha/Hora de Detección:** 31 de Julio de 2026, 09:24 AM
- **Síntoma Observado:** El semáforo comunal saltó repentinamente de **8.7% (Verde)** a **88.1% (Alerta Roja)** en el Centro Histórico con solo $2.5\text{ mm}$ de lluvia acumulada.
- **Causa Raíz Identificada:** 
  - En `spatial_scanner.py`, la variable de innovación de terreno `enkf_corr` (que mide milímetros reales observados, ej: $1.3\text{ mm}$ en Pan de Azúcar) se sumaba directamente como valor flotante no acotado dentro del `base_score` (fórmula acotada en la escala $[0.0, 1.0]$):
    ```python
    base_score = (... + enkf_corr) # Error: Suma directa de 1.3 a una escala 0-1
    ```
- **Solución Implementada:**
  1. Normalización acotada de la corrección EnKF: `0.05 * min(1.0, enkf_corr / 10.0)`.
  2. Implementación de **Reglas de Coherencia Física Inviolables**:
     - Si $P_{24h} < 10.0\text{ mm}$ y $Q < 1.0\text{ mm}$ y $FS \ge 1.0 \implies$ Score acotado estrictamente a **máximo 25.0% (VERDE)**.
     - Si $P_{24h} < 25.0\text{ mm}$ y $Q < 5.0\text{ mm}$ y $FS \ge 1.0 \implies$ Score acotado a **máximo 55.0% (AMARILLA)**.
     - La **Alerta Roja (> 70.0%)** requiere condición física crítica comprobada ($P_{24h} \ge 25\text{ mm}$ o $Q \ge 5.0\text{ mm}$ o inestabilidad de ladera $FS < 1.0$).
- **Archivos Modificados:** `ML_Models/src/inference/spatial_scanner.py`

---

### 🟡 Hallazgo 2: Ingesta Incompleta por Cambio de Formato en Estaciones CEAZAMET
- **Fecha/Hora de Detección:** 31 de Julio de 2026, 08:04 AM
- **Síntoma Observado:** Existía llovizna en terreno en La Serena, pero el módulo CEAZAMET reportaba `None` (0.0 mm) para las estaciones locales.
- **Causa Raíz Identificada:**
  - El parseador `parse_ceazamet_html()` en `ingest_ceazamet.py` buscaba tablas HTML (`<table>`). Sin embargo, el endpoint AJAX de popups de CEAZAMET (`pop_estacion_info.php`) entrega texto plano formateado (`<strong>Precip.:</strong>0.1 T2m:13.1°C`) sin etiquetas de tabla. Además, CEAZAMET omite la etiqueta `Precip.:` cuando la lluvia es $0.0\text{ mm}$.
- **Solución Implementada:**
  1. Extractor con expresiones regulares (Regex) capaz de capturar tanto texto plano como tablas HTML.
  2. Asignación por defecto de `precipitation_mm = 0.0` cuando la estación está online pero omite la etiqueta por ausencia de precipitación acumulada.
- **Resultado:** Las 7 estaciones locales de La Serena (`LSC`, `CGR`, `5`, `3`, `9`, `6`, `4`) quedaron **100% online en tiempo real**.
- **Archivos Modificados:** `ML_Models/src/ingesters/ingest_ceazamet.py`

---

### 🌊 Hallazgo 3: Propagación Espacial Diferenciada por Tiempo de Avance ($T_c$)
- **Fecha/Hora de Detección:** 31 de Julio de 2026, 08:27 AM
- **Síntoma/Consulta:** Dudas operacionales sobre por qué el escáner mostraba el pico de impacto a las **11:30 AM** en Pueblo Islón y a las **13:30 - 14:00 hrs** en el Centro Histórico y Ruta 5.
- **Análisis Hidrológico Validado:**
  - **Cuenca Alta / Quebradas (Pueblo Islón, Lambert):** $T_c = 1.5\text{h}$. El agua responde rápido en la ladera y llega a las **11:30 AM**.
  - **Zona Urbana / Colectores (Centro, Balmaceda, Peñuelas):** $T_c = 3.5\text{h}$ a $4.0\text{h}$. El agua de la cuenca alta tarda entre 3.5 y 4 horas en recorrer el valle y acumularse en los sumideros bajos de la ciudad.
- **Lección Aprendida:** El escaneo espacial por 35 micro-zonas demuestra ser altamente efectivo al entregar ventanas temporales diferenciadas para cada sector, en lugar de un único horario plano para toda la ciudad.

---

### 🇨🇱 Hallazgo 4: Integración de Fuentes Institucionales Chilenas (SENAPRED y DMC)
- **Fecha/Hora de Detección:** 31 de Julio de 2026, 09:32 AM
- **Requerimiento:** Incorporación de avisos meteorológicos de la DMC y alertas oficiales de SENAPRED para dar respaldo institucional al modelo ML.
- **Solución Implementada:**
  - Desarrollo del nuevo módulo `ML_Models/src/ingesters/ingest_senapred.py`.
  - Ingesta programática de las alertas de SENAPRED (ATP, Amarilla, Roja para Coquimbo) y avisos de la DMC (A364-3 por lluvia y A365-3 por rachas de viento de 60-80 km/h en la costa).
- **Archivos Creados:** `ML_Models/src/ingesters/ingest_senapred.py`

---

### 🟢 Hallazgo 5: Naturaleza de las Micro-Variaciones Dentro de la Banda de Alerta Verde (ej. 8.7% vs 2.7%)
- **Fecha/Hora de Detección:** 31 de Julio de 2026, 10:02 AM
- **Consulta Operacional:** El usuario notó que el score osciló de **8.7%** a **2.7%** tras un reporte enviado y consultó si constituía una falla del sistema.
- **Explicación Técnica & Análisis de Invarianza:**
  - **No representa una falla.** La **Alerta Verde Comunal** abarca todo el rango continuo de $[0.0\%, 40.0\%]$. Cualquier valor dentro de esta banda representa la misma condición operativa: *Monitoreo estable sin necesidad de despliegue de emergencia*.
  - **Causa del Ajuste (2.7%):** La variación responde a la aplicación de la refactorización convexa $\sum w_i = 1.0$, que depuró el ruido residual en la puntuación base.
  - **Recomendación para Reportes a Autoridades:** En comunicaciones verbales a Bomberos/COGRID, se recomienda reportar la **Categoría de Alerta (Verde Comunal < 10%)** en lugar de variaciones decimales instantáneas para evitar confusión innecesaria.

---

## 📈 3. Puntos de Análisis para la Evaluación Post-Prueba Real

| Tema a Evaluar | Situación en Prueba Real | Propuesta Post-Prueba |
|---|---|---|
| **Suavizado Temporal (EMA)** | Implementado en `spatial_scanner.py` ($\alpha_{\text{onset}} = 0.45, \alpha_{\text{decay}} = 0.10$). | Validar la curva de decaimiento post-tormenta en la noche. |
| **Banda de Histeresis** | Histeresis del 8% activa en `spatial_scanner.py`. | Confirmar ausencia de *flickering* durante el frente del 31-Julio. |
| **Ponderación Convexa** | Pesos ajustados a $\sum w_i = 1.0$. | Validar la matriz de pesos con datos históricos post-evento. |
| **Integración CEAZAMET** | Ingesta activa por AJAX popup. | Evaluar solicitud de API Key o Web Service directo con la directiva de CEAZA. |
| **Integración SENAPRED/DMC** | Ingestor `ingest_senapred.py` activo. | Automatizar la alerta institucional en el frontend UI. |

---

## 📄 4. Registro de Commits y Cambios en Repositorio

- `bb9637f`: Integración de módulos v6.0 (Geotecnia FS, Nowcasting Radar, Muskingum-Cunge, PINNs, EnKF).
- `2610007`: Incorporación de sección "Fuentes de Datos del Modelo" en informe LaTeX.
- `a8f0b45`: Corrección sintáctica LaTeX e informe PDF compilado.
- `f8a8475`: Corrección de parseo regex para estaciones CEAZAMET y acoplamiento de terreno.
- `a860c6f`: Corrección de ponderación EnKF y reglas de coherencia física inviolables.
- `bbc8be6`: Bitácora inicial de hallazgos y módulo ingestor `ingest_senapred.py`.
- `7982143`: Refactorización de estabilización convexa, EMA adaptativo, histeresis del 8% y test suite `test_stability.py`.
- `f079db5`: Registro de Hallazgo 5 sobre micro-variaciones dentro de banda Verde.

---

### 🔴 Hallazgo 6 (CRÍTICO): Crecida de Río en Pueblo Islón / El Romero Sin Detección Anticipada
- **Fecha/Hora de Detección:** 31 de Julio de 2026, 12:14 PM
- **Síntoma Observado:** Reportes de crecida de río, inundaciones en Islón, El Romero y quebradas adyacentes. El sistema mostraba solo un 25% de riesgo para esas zonas y no emitió anticipación.
- **Causa Raíz Identificada (Doble Punto Ciego):**
  1. **Regla de acotamiento rígida:** La regla de seguridad física acotaba el score a máximo 25% si $P_{24h} < 10\text{ mm}$ a nivel local. Pero la precipitación que genera la crecida cae en la cuenca alta (600-1200 m.s.n.m.) y baja por gravedad. El sensor NRT local asignado a Islón no detectaba esa lluvia.
  2. **Escorrentía calculada solo con lluvia local:** `direct_Q` usaba únicamente la precipitación del sector específico, ignorando el caudal del río que baja de aguas arriba (`muskingum_q`) y la corrección EnKF de terreno.
- **Solución Implementada:**
  1. **Escorrentía Hidrológica Efectiva:** `effective_hydro_q = max(direct_Q, muskingum_q, enkf_corr)` — integra agua local + caudal fluvial aguas arriba.
  2. **Excepción para Sectores de Río/Quebrada:** Los sectores clasificados como `Precordillera / Ribereño`, `Quebrada Norte`, `Valle Precordillerano` ya NO se acotan al 25% cuando hay crecida aguas arriba (`effective_hydro_q >= 2.0`).
  3. **Boost de Urgencia Fluvial:** Si `effective_hydro_q >= 2.0` o `enkf_corr >= 5.0`, el score se eleva automáticamente a mínimo 75% (Alerta Roja).
- **Lección Aprendida:** En cuencas semi-áridas como La Serena, la lluvia que genera inundaciones **no siempre cae donde inunda**. El modelo debe considerar siempre la propagación hidrológica aguas arriba-abajo.
- **Archivos Modificados:** `ML_Models/src/inference/spatial_scanner.py`

---

### 🟠 Hallazgo 7: Interrupción del Servicio CEAZAMET Durante el Peak de la Tormenta
- **Fecha/Hora de Detección:** 31 de Julio de 2026, 12:16 PM
- **Síntoma Observado:** Las 7 estaciones CEAZAMET reportan `stations_online: 0` y `ceazamet_available: False`. El servicio se interrumpió justo durante el momento de mayor intensidad del frente.
- **Impacto:** Al perder la telemetría de terreno, el modelo quedó dependiendo exclusivamente de los datos satelitales NRT (que tienen resolución más gruesa y latencia de ~30 min), perdiendo la capacidad de detectar acumulaciones locales en tiempo real.
- **Lección Aprendida:** Se necesita un mecanismo de **resiliencia ante caída de fuentes de datos**, que al detectar la pérdida de CEAZAMET active automáticamente un factor de incertidumbre que aumente el score base como compensación (principio de precaución).
- **Propuesta Post-Prueba:** Implementar `uncertainty_boost` cuando `ceazamet_available = False`: incrementar el score base un +15% como margen de seguridad ante falta de observación de terreno.
