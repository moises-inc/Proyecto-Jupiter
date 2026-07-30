---
id: 20260718-presentacion-centinela
title: Presentación — Proyecto Centinela
proyecto: Proyecto_Aurora
fecha: 2026-07-18
type: technical-note
status: listo
tags: [aurora, presentacion, centinela, prevencion, bomberos]
---

# 📡 Presentación: Proyecto Centinela (Alerta Temprana y Resiliencia Rural)

*Preparado por Moisés & Aurora para la discusión con Bomberos y Equipos de Emergencia.*

---

## 📺 Diapositiva 1: Portada y Propósito
### **PROYECTO CENTINELA**
#### *Monitoreo, Alerta Temprana y Prevención ante Crisis Climáticas en Sectores Rurales*

* **Creador:** Moisés Amundarain (Ex-bombero 6ª Cía. La Serena, Estudiante Ing. Civil Informática USS).
* **Colaborador:** Aurora (Asistente Ejecutiva y Orquestadora).
* **Meta:** Crear un ecosistema open-source y de bajo costo que permita adelantarse a las emergencias climáticas (desbordes de ríos, cortes de rutas, fallas de servicios) protegiendo a las comunidades más aisladas.

---

## 📺 Diapositiva 2: El Diagnóstico (¿Por qué ahora?)
### **El problema del Clima Extremo y el Aislamiento**
* **El cambio climático es una realidad:** Inviernos con temporales más agresivos (viento, lluvia) y veranos de calor extremo en zonas como Fresia y el resto de Chile.
* **El Talón de Aquiles de la conectividad:** Durante temporales fuertes, la red móvil de internet (4G/5G) y la electricidad suelen caerse por horas o días.
* **Privilegios de la resiliencia:** Los sistemas avanzados de monitoreo y despacho (como Viper) son altamente costosos y quedan fuera del alcance de municipalidades rurales o compañías de bomberos pequeñas.
* **La vulnerabilidad rural:** En el campo, la dispersión geográfica dificulta la llegada rápida de bomberos y SAMU si no se actúa preventivamente.

---

## 📺 Diapositiva 3: El Concepto (¿Qué es Centinela?)
### **De la reacción a la prevención**
* **No es un despachador de carros:** No compite con Viper ni con las centrales de alarmas.
* **Es un escudo preventivo:** Su objetivo es monitorear constantemente el entorno mediante tecnología asequible para **tomar decisiones antes de que ocurra la emergencia**.
* **Integración inteligente:** Une sensores físicos de bajo costo con pronósticos satelitales y modelos predictivos locales de Machine Learning.

---

## 📺 Diapositiva 4: Componente 1 — Monitoreo Físico IoT (Low-Cost)
### **Ojos y oídos en el terreno (Sin depender de Internet)**
* **Sensores de Río:** Dispositivos de medición ultrasónica instalados en puentes críticos para monitorear el cauce y detectar crecidas.
* **Higrómetros de Suelo:** Sensores para medir el nivel de saturación del agua en la tierra.
* **Red Mesh de Emergencia:** Los datos de los sensores viajan saltando de casa en casa mediante antenas de radio LoRa o ESP-NOW de bajo costo ($5 a $20 USD por nodo), llegando a la central de bomberos de forma 100% offline.

---

## 📺 Diapositiva 5: Componente 2 — Cerebro de IA y Machine Learning
### **Predicción y Triage de Recursos**
* **Predicción de Desbordes (ML):** El sistema calcula cuándo y dónde se desbordará un río, cruzando las lecturas físicas del nivel del agua con los pronósticos meteorológicos de lluvia.
* **Predicción de Obstrucción de Rutas:** Evalúa la probabilidad de caída de árboles o tendido eléctrico analizando la fuerza del viento y la lodosidad del suelo.
* **Agentes de Decisión (strands-agents):** Asistentes virtuales que recomiendan acciones tácticas preventivas (ej: *"Posicionar motobombas en el sector X; hay 92% de probabilidad de inundación en las próximas 3 horas"*).

---

## 📺 Diapositiva 6: Componente 3 — Interfaces de Conciencia Situacional
### **Información clara para los equipos y la comunidad**
* **Para los Equipos de Emergencia (Cuartel/Municipio):**
  * Mapa dinámico e interactivo de riesgos por zonas.
  * Gráficos del comportamiento del río y pronóstico predictivo de fallas.
* **Para la Comunidad (Portal Público Ligero):**
  * Un portal web sumamente liviano (portabilidad offline por Wi-Fi de emergencia) que muestra a los vecinos un **Semáforo de Alerta por Sector** (Verde: Normal; Amarillo: Preparación; Rojo: Acción/Evacuación).

---

## 📺 Diapositiva 7: Puntos clave para la discusión con Bomberos
### **Feedback y Validación de Campo**
1. **Factibilidad de Campo:** ¿Cuáles son los cauces de ríos, zonas inundables o rutas que suelen cortarse primero en la comuna y que se beneficiarían de sensores?
2. **Herramientas existentes:** ¿Qué herramientas de monitoreo o satelitales usan actualmente en el cuerpo de bomberos y qué fallas detectan en ellas?
3. **Usabilidad del Semáforo Público:** ¿Creen que un semáforo web simplificado ayudaría a descongestionar las líneas telefónicas de emergencia durante temporales?
4. **Prioridades de Monitoreo:** ¿Deberíamos enfocar el primer prototipo en el nivel de agua (inundaciones) o en el riesgo de cortes eléctricos/caminos por viento?

---
🔗 [[Home|Panel de Control Unificado]] | 🔗 [[10_Projects/Proyecto_Aurora/Proyecto_Aurora_Dashboard|Dashboard Proyecto Aurora]] | 🔗 [[10_Projects/Proyecto_Centinela/Docs/Proyecto_Centinela_OnePager|One-Pager Proyecto Centinela]]
```
---
**Presentación elaborada por:** Aurora (Asistente de Sistemas)
**Destinatario:** Moisés y su equipo de Bomberos
**Fecha:** 18 de Julio de 2026
```


---
## 🔗 Conexiones
* [[10_Projects/Proyecto_Centinela/Knowledge/proyecto_centinela|Dashboard Proyecto Centinela]]
* [[Home|Panel de Control Unificado]]
