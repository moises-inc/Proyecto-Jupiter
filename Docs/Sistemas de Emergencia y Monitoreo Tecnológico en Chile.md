# **Análisis Multidimensional de Tecnologías de Información, Modelamiento Numérico e Interoperabilidad en la Gestión de Catástrofes: Lecciones del Temporal de Chile de Julio de 2026**

## **Marco Normativo y de Gobernanza en la Gestión del Riesgo de Desastres en Chile**

La gestión estratégica de emergencias de origen natural en Chile ha experimentado una profunda reestructuración jurídica y operativa bajo el amparo de la Ley N° 21.364, la cual sustituyó la antigua Oficina Nacional de Emergencia (ONEMI) por el actual Servicio Nacional de Prevención y Respuesta ante Desastres (SENAPRED)1. Este marco normativo propició la transición desde un enfoque puramente reactivo hacia una aproximación integral basada en la Reducción del Riesgo de Desastres (RRD), articulada a través del Sistema Nacional de Prevención y Respuesta ante Desastres (SINAPRED)2. La gobernanza de este sistema se operativiza por medio del Comité para la Gestión del Riesgo de Desastres (COGRID), organismo colegiado que asume el mando político-técnico en los niveles nacional, regional, provincial y comunal durante un evento adverso4.  
Durante el temporal extremo que afectó a la zona centro-norte de Chile entre el 14 y el 21 de julio de 2026, la efectividad de esta gobernanza tecnológica fue sometida a una rigurosa prueba de campo6. La gravedad del sistema frontal obligó al presidente de la República, José Antonio Kast, a decretar el Estado de Excepción Constitucional de Catástrofe para la Región de Coquimbo y la provincia de Huasco en la Región de Atacama6. Esta declaración excepcional faculta al Ejecutivo para movilizar de manera expedita recursos fiscales, disponer del despliegue de efectivos de las Fuerzas Armadas bajo un mando unificado de la Defensa Nacional y coordinar de forma directa la logística de rescate8.  
A nivel comunal, alcaldes como Daniela Norambuena en La Serena y Ali Manouchehri en Coquimbo lideraron los COGRID locales, enfrentando la saturación de los suelos, el desborde del río Elqui y la activación de quebradas críticas4. Este escenario puso de manifiesto que las decisiones políticas de alertamiento y evacuación dependen directamente de la confiabilidad y velocidad de flujo de los datos provistos por las herramientas tecnológicas de monitoreo4.

## **Tecnologías de Monitoreo, Observación Terrestre y Modelamiento Científico**

La anticipación y el seguimiento en tiempo real de los fenómenos atmosféricos extremos requieren la convergencia de modelamiento numérico de alta resolución, observación satelital continua y redes de sensores hidrométricos terrestres14.

### **Modelamiento Numérico de Escala Regional**

La Dirección Meteorológica de Chile (DMC) y la Dirección General del Territorio Marítimo y de Marina Mercante (Directemar) fundamentan sus proyecciones en el modelo numérico de escala regional **WRF (Weather Research and Forecasting)**15. Este sistema de integración numérica requiere condiciones iniciales y de borde generadas por modelos globales para simular variables meteorológicas clave con un horizonte de cinco días15.  
El modelo WRF permite generar meteogramas específicos, proveyendo información horaria de variables críticas como la precipitación acumulada en milímetros (![][image1]), velocidad y dirección del viento, y humedad relativa15. Durante el evento de julio de 2026, el modelo WRF-DMC y el modelo WRF de la Armada de Chile anticiparon acumulaciones extremas de hasta 350 milímetros en los sectores precordilleranos de la Región de Coquimbo, alertando tempranamente sobre el riesgo inminente de aluviones y crecidas fluviales6.

### **Observación Satelital y Trazado de Tormentas**

La detección y caracterización del sistema frontal en tiempo real se apoyan en los datos del satélite geoestacionario **GOES-19**, operado en conjunto por agencias internacionales y analizado localmente por la DMC15. A bordo del GOES-19, el sensor **ABI (Advanced Baseline Imager)** captura información en 16 canales espectrales15. Para el monitoreo de tormentas severas, destaca el canal 13, que opera en el espectro infrarrojo térmico (en torno a los 10,3 ![][image2]) para estimar la radiación de onda larga emitida por la superficie terrestre y los topes de las nubes, permitiendo deducir la altitud y severidad de las formaciones de nubes convectivas15.  
Este sensor se complementa con el **GLM (Geostationary Lightning Mapper)**, un instrumento geoestacionario diseñado para detectar descargas eléctricas continuas en la atmósfera15. Los datos del GLM se integran en mapas digitales de tormentas eléctricas, proporcionando a los tomadores de decisiones información espacial precisa sobre las zonas con mayor inestabilidad atmosférica15. Adicionalmente, el Centro de Estudios Avanzados en Zonas Áridas (CEAZA) aporta análisis oceanográficos y climáticos locales que optimizan los modelos de predicción costera, mientras que la Universidad de Valparaíso lidera la instalación del primer radar meteorológico del país, tecnología destinada a transformar la micro-predicción de ríos atmosféricos y trombas marinas19.

### **Telemetría de Caudales e Hidrología de Cuencas**

La Dirección General de Aguas (DGA) administra el **Sistema Hidrométrico en Línea**, orientado al monitoreo de embalses, lagos, ríos y pozos a nivel nacional21. Bajo la exigencia de la Resolución DGA N° 1238, los titulares de derechos de aprovechamiento de aguas deben implementar sistemas de **Monitoreo de Extracciones Efectivas (MEE)**23. Los datos se transmiten automáticamente en formato XML al servidor del software de control de la DGA, accesible para fiscalización mediante plataformas digitales dedicadas14.  
En condiciones extremas de escorrentía, las redes de medición utilizan tecnologías diseñadas para operar en entornos hostiles14:

* **Caudalímetros Electromagnéticos Bridados:** Dispositivos que utilizan la ley de inducción de Faraday para medir la velocidad del flujo de agua sin generar obstrucción física en la tubería, garantizando precisión metrológica extrema y previniendo pérdidas de presión hidráulica14.  
* **Sondas Piezométricas de Presión:** Transductores sumergibles que registran las variaciones en la columna de agua para el monitoreo dinámico del nivel de ríos y pozos14.  
* **Dataloggers con Certificación IP68:** Unidades de adquisición de datos herméticas que aseguran la continuidad operativa del equipo incluso bajo inmersión prolongada14.  
* **Redes LoRaWAN y Enlaces Celulares 4G/GPRS:** Protocolos de comunicación que penetran la topografía irregular de los valles fluviales de las provincias de Elqui, Limarí y Choapa, garantizando la transmisión continua de datos hacia los servidores de la DGA y de los Comités de Agua Potable Rural (APR)14.

## **Plataformas de Coordinación, Alerta Temprana y Mitigación de Desastres**

La mitigación de pérdidas humanas y materiales se articula mediante el despliegue de plataformas de software cartográfico y sistemas de alerta masiva georreferenciada, diseñados para orientar tanto a los organismos de emergencia como a la población civil1.

### **Cartografía Interactiva y Alerta Pública de SENAPRED**

SENAPRED gestiona el **Visor Chile Preparado**, una plataforma interactiva basada en sistemas de información geográfica (SIG) que permite a la ciudadanía y a los equipos tácticos evaluar el nivel de exposición de un punto geográfico frente a amenazas naturales como erupciones volcánicas, incendios forestales o tsunamis25. El visor despliega capas que contienen la red vial, topografía detallada, y la ubicación georreferenciada de infraestructura crítica de respuesta tales como cuarteles de Bomberos, comisarías de Carabineros y centros de salud, además de los planos de evacuación oficiales (puntos de encuentro y vías de escape)25. La base cartográfica se actualiza mediante la recopilación de datos provistos por organismos técnicos como SERNAGEOMIN, CONAF, el IGM y las municipalidades del país25.  
Para la difusión de órdenes de evacuación en terreno, el principal canal tecnológico del Estado es el **Sistema de Alerta de Emergencia (SAE)**1. Su funcionamiento técnico está regulado por la Subsecretaría de Telecomunicaciones (SUBTEL) de acuerdo con la Ley N° 18.168 de Telecomunicaciones y el Decreto N° 601. El SAE opera mediante una **Plataforma Central Unificada (PCU)** que traduce el mensaje de emergencia al protocolo CAP (Common Alerting Protocol)1.  
Esta alerta se transmite a los operadores de telefonía móvil, quienes utilizan tecnología de difusión celular (*Cell Broadcast*) para emitir un mensaje georreferenciado a todos los teléfonos inteligentes que se encuentren dentro del área de cobertura de las antenas seleccionadas para el polígono de emergencia1. Esta arquitectura técnica asegura que los mensajes aparezcan en pantalla con un tono y vibración distintivos, sin verse afectados por la saturación de los canales convencionales de voz o datos móviles1.

| Sistema de Alerta / Tecnología | Ente Administrador | Mecanismo de Transmisión | Dispositivos Receptores | Idiomas / Estándar técnico |
| :---- | :---- | :---- | :---- | :---- |
| **SAE (Sistema de Alerta de Emergencia)** \[cite: 1\] | SENAPRED / SUBTEL (Chile)1 | Difusión Celular (*Cell Broadcast*) mediante Plataforma Central Unificada1. | Dispositivos móviles inteligentes homologados dentro del área georreferenciada1. | Español; protocolo CAP (Common Alerting Protocol)1. |
| **Chile Alerta App** \[cite: 26, 27\] | Privado (Chile Alerta SpA)26 | Notificaciones push de alta prioridad basadas en geolocalización de usuario26. | Smartphones Android e iOS con la aplicación instalada26. | Español; integra APIs de agencias oficiales (CSN, SHOA, DMC)27. |
| **EAS / WEA (Emergency Alert System)** \[cite: 1\] | FCC / FEMA (EE. UU.)1 | Difusión por satélite, radio comercial, televisión y redes celulares georreferenciadas1. | Radios NWR, televisores, receptores satelitales y teléfonos móviles1. | Inglés y Español; estándares de la FCC1. |
| **J-Alert** \[cite: 1\] | Gobierno de Japón1 | Transmisión vía satélite artificial a receptores terrestres y altoparlantes urbanos1. | Altoparlantes municipales, sirenas públicas, televisión, radio y teléfonos1. | Japonés, Inglés, Mandarín, Coreano y Portugués1. |
| **Galileo EWSS (Emergency Warning Satellite Service)** \[cite: 1\] | Unión Europea1 | Enlace de navegación satelital directo (independiente de redes terrestres de telefonía)1. | Receptores y navegadores satelitales compatibles con decodificación EWSS1. | Formato de Mensaje de Alerta Codificado (CAMF) basado en CAP1. |

En el ámbito civil y de forma paralela a los canales del Estado, se ha masificado el uso de aplicaciones móviles privadas como **Chile Alerta**26. Esta app recopila información de diversas agencias gubernamentales y científicas a nivel mundial, proveyendo a sus usuarios un monitor sísmico en tiempo real, boletines meteorológicos, alertas de tsunami del SHOA y alertas volcánicas de SERNAGEOMIN26.  
A través de su red social integrada **Conecta**, los usuarios pueden reportar en tiempo real anomalías locales y emergencias viales mediante un sistema de retroalimentación comunitaria georreferenciada, el cual visualiza los incidentes sobre un mapa en vivo27.

## **Sistemas de Despacho Asistido y Telecomunicaciones de los Organismos de Respuesta Primaria**

La operatividad táctica en terreno de las fuerzas de orden y seguridad y de respuesta ante emergencias depende de arquitecturas informáticas conocidas como CAD (Computer-Aided Dispatch) y de redes robustas de radiocomunicación digital28.

### **Carabineros de Chile: Central de Comunicaciones (CENCO)**

CENCO gestiona los despliegues de la fuerza policial y las coordinaciones de rescate táctico a nivel nacional30. El sistema de atención telefónica del nivel de emergencia **133** canaliza los requerimientos de la población hacia una central provista de un software de **Despacho Asistido por Computador (CAD)**29. El sistema CAD asocia el incidente geográfico con las patrullas terrestres y aéreas disponibles en el cuadrante respectivo, optimizando los tiempos de respuesta operativa29.  
El flujo de información en CENCO integra los siguientes componentes de soporte técnico30:

> 1. **Nivel Alpha 1 (Comando y Control de Videovigilancia):** Desde esta sala de control se operan más de 300 cámaras de vigilancia urbana de alta resolución, facilitando el análisis visual de la inundación de avenidas principales, caída de estructuras y la activación de cursos de agua en zonas residenciales30.  
> 2. **Móviles Satelitales TIC (Tecnologías de la Información y Comunicación):** Unidades móviles de despliegue rápido equipadas con antenas de enlace satelital directo, transceptores de radio VHF, y repetidores de sistemas de radio de tipo trunking, diseñados para garantizar la cobertura de comunicaciones en áreas donde las antenas repetidoras terrestres habituales sufren cortes de suministro eléctrico o daños estructurales30.  
> 3. **Nivel Alpha 2:** Nodo de enlace dedicado a la conexión automatizada con entidades críticas financieras y de valores30.  
> 4. **Restricciones de Geolocalización Activa:** Uno de los principales desafíos operativos de CENCO radica en la restricción legislativa para geolocalizar de manera directa e instantánea los teléfonos móviles que llaman al 13329. Actualmente, Carabineros requiere autorización previa de un juez de garantía o protocolos especiales con las empresas operadoras para rastrear la señal de personas extraviadas en zonas de catástrofe, lo cual incrementa el tiempo de respuesta frente a emergencias con riesgo vital inminente29.

### **Cuerpos de Bomberos de Chile: Centrales de Alarmas y Telecomunicaciones**

Los Cuerpos de Bomberos de Chile, organizaciones autónomas coordinadas por la Junta Nacional de Cuerpos de Bomberos, han digitalizado sus centrales de despacho mediante el uso de plataformas que optimizan el flujo operativo desde la recepción del llamado en el número de emergencia **132**32.

#### **Plataformas de Despacho y Gestión en Bomberos**

La centralización de datos operativos, de personal e inventario cuartelario se procesa por medio de sistemas especializados34. En el Cuerpo de Bomberos de Santiago, por ejemplo, se utiliza un nuevo **Sistema de Despacho Asistido por Computadora (CAD-A)**, el cual integra variables críticas como la asignación inteligente de recursos (bomba, rescate, escala, materiales peligrosos), geolocalización GPS de las unidades de material mayor y mapas de grifos y grillas de agua en línea35. Este sistema cuenta con planes de respaldo que se activan de forma automática, permitiendo la operación del sistema de despacho desde terminales secundarias de telecomunicaciones o directamente desde vehículos de comandancia móviles en el terreno de las emergencias35.  
Por otra parte, se ha desarrollado el software de gestión en la nube **FireCloud Core**, diseñado específicamente para racionalizar las operaciones de los Cuerpos de Bomberos de Chile, con pilotos operativos en el Cuerpo de Bomberos de Viña del Mar34. FireCloud unifica el flujo digital integrando:

* **Bitácora y Guardia Digital:** Traspaso automatizado de novedades de guardia y turnos, eliminando la pérdida de datos operativos clave34.  
* **Gestión del SCI (Sistema de Comando de Incidentes):** Estructuración de los incidentes bajo la terminología de mandos unificados de control34.  
* **Trazabilidad de Equipamiento de Protección Personal (EPP) e Inventarios:** Monitoreo del estado operativo de los recursos y la flota34.  
* **Consolidación de Indicadores de Comandancia:** Reportabilidad inmediata de tiempos de respuesta y dotaciones efectivas34.

A nivel administrativo, los Cuerpos de Bomberos implementan el software **Manager+**37. Este sistema estandariza la contabilidad interna en línea, facilitando la auditoría y rendición de cuentas financieras, asegurando la transparencia en la administración de recursos fiscales asignados a la institución37.

#### **Interoperabilidad de Radiocomunicaciones: Red P25**

Para el soporte de voz táctica, Bomberos de Chile implementa de manera progresiva el estándar de comunicación digital por radiofrecuencia **APCO P25 (Project 25\)**31. Este sistema opera en canales encriptados que garantizan una alta fidelidad en la voz incluso en entornos de alta interferencia acústica o lluvia extrema, características ausentes en las antiguas bandas analógicas VHF31.  
El sistema P25 permite una interoperabilidad directa entre los carros de Bomberos, oficiales de comandancia y la Central de Comunicaciones (CENCO) de Carabineros, optimizando el enlace interinstitucional31. No obstante, su despliegue completo requiere importantes inversiones fiscales y la coordinación con los Gobiernos Regionales para financiar el equipamiento de los cuerpos rurales más apartados del país31.

#### **Protocolos de Recepción y Despacho Radial de Bomberos**

Las Centrales de Alarmas y Comunicaciones, como la del Cuerpo de Bomberos de Punta Arenas (CACBPA), operan bajo estrictos estándares normativos para la catalogación y despacho de incidentes, sirviendo como modelo técnico de referencia nacional33. El protocolo establece que la operadora debe clasificar la emergencia mediante preguntas estandarizadas y activar las frecuencias radiales de la Red Regional de Emergencia33.  
El proceso de comunicación por radio se estructura bajo un lenguaje codificado estricto para mitigar la ambigüedad en el canal de voz33:

* **Clave 0-6:** Instrucción de despacho que ordena a las unidades de material mayor dirigirse al lugar del siniestro utilizando dispositivos de alarmas acústicas y luminosas activas33.  
* **Clave 6-0:** Solicitud de confirmación o repetición del mensaje emitido por la Central de Alarmas33.  
* **Clave 6-2:** Transmisión formalizada de la dirección geográfica del incidente, detallando la calle principal, numeración exacta e intersecciones críticas33.

## **Análisis de Fallas de Infraestructura Crítica e Interoperabilidad en la Catástrofe de Julio de 2026**

La magnitud del temporal que asoló a la Región de Coquimbo a partir del 15 de julio de 2026 expuso deficiencias estructurales en las obras de mitigación previas, cortes generalizados en servicios básicos e interrupciones críticas en los sistemas de enlace que soportan la toma de decisiones8.

                                  \+------------------------+  
                                  |   Sistema Frontal      |  
                                  |  Precipitaciones \>100mm|  
                                  \+-----------+------------+  
                                              |  
                                              v  
                                  \+------------------------+  
                                  | Saturación de Suelos e |  
                                  | Incremento de Caudales |  
                                  \+-----------+------------+  
                                              |  
                                              v  
                             \+----------------+----------------+  
                             |                                 |  
                             v                                 v  
               \+---------------------------+     \+---------------------------+  
               |  Activación de Quebradas  |     |   Crecida del Río Elqui   |  
               | (Santa Gracia, El Romero) |     |   Niveles de Turbiedad \>20x|  
               \+-------------+-------------+     \+-------------+-------------+  
                             |                                 |  
                             v                                 v  
               \+---------------------------+     \+---------------------------+  
               | Aluviones e Inundaciones  |     |  Colapso de Captaciones   |  
               |       (El Islón)          |     |     y Cortes de Agua      |  
               \+-------------+-------------+     \+-------------+-------------+  
                             |                                 |  
                             v                                 v  
               \+---------------------------+     \+---------------------------+  
               |   Cortes de Rutas, Red    |     |   Despliegue de Puntos    |  
               |  Eléctrica y Vuelos Aero  |     |   Alternativos y Tanques  |  
               \+---------------------------+     \+---------------------------+

### **El Aluvión de El Islón y la Activación de la Quebrada Santa Gracia**

El domingo 19 de julio de 2026 se registró la activación súbita de la quebrada Santa Gracia en el sector de El Islón, comuna de La Serena4. Este fenómeno generó un aluvión masivo que arrasó con zonas residenciales de la periferia de la ciudad, provocando la destrucción completa de entre 30 y 50 viviendas y daños severos en un centenar de estructuras habitacionales40. La desconexión vial de El Islón, que sirve como ruta estructurante entre La Serena y los sectores rurales del Valle de Elqui, dejó aisladas a más de 90 personas y provocó la pérdida del tendido de distribución eléctrica local4.  
Este incidente desató intensas críticas ciudadanas dirigidas al biministro de Obras Públicas y Transportes, Louis de Grange, y a la alcaldesa Daniela Norambuena, motivadas por la tardanza en el despliegue de maquinaria pesada para el despeje de cauces y la ausencia de personal militar en las horas previas a la catástrofe, cuando el sistema frontal ya saturaba los suelos de la región4. El debate público evidenció que el retraso administrativo de cinco días para decretar el Estado de Catástrofe inmovilizó el mando unificado de las Fuerzas Armadas para operaciones preventivas de remoción de tierra13.

### **Colapso Tecnológico de la Sanitaria Aguas del Valle**

El caudal del río Elqui experimentó un incremento exponencial, arrastrando una alta carga de sedimentos, rocas y material aluvial fino38. La turbiedad registrada sobrepasó en más de 20 veces el límite máximo aceptable de operación de las plantas de tratamiento de la sanitaria Aguas del Valle, lo cual forzó la detención total del proceso de potabilización43.  
La situación empeoró tras la inundación física y pérdida de energía eléctrica en instalaciones de captación críticas, obligando a evacuar al personal técnico de la empresa y bloqueando los accesos viales por la acumulación de barro y lodo12. Esto impidió que los equipos operacionales de la sanitaria ingresaran de manera segura a realizar la evaluación de daños y restablecer las conexiones, extendiendo de forma indefinida el horizonte técnico de reposición del suministro de agua potable42.  
Para atenuar la emergencia y asegurar el abastecimiento mínimo de agua potable en la conurbación de La Serena y Coquimbo, Aguas del Valle coordinó un plan de contingencia alternativo que comprendió el despliegue de más de 100 estanques estacionarios de distribución de agua y el envío de camiones aljibe a las zonas residenciales afectadas42. La cobertura del corte de suministro abarcó amplios sectores residenciales de ambas comunas:

| Comuna | Sectores Residenciales Afectados sin Suministro de Agua | Puntos de Abastecimiento Alternativo Implementados | Canales de Soporte y Consulta Activos |
| :---- | :---- | :---- | :---- |
| **La Serena** \[cite: 43, 44\] | Cerro Grande, San Joaquín, Barrio Universitario, Colina El Pino, El Milagro, La Florida, Vista Hermosa y La Pampa43. | Más de 100 estanques estacionarios distribuidos en puntos críticos y rutas de camiones aljibe42. | Fono Clientes: 600 400 4444\. WhatsApp: \+56 9 9900 0325 (Soporte Operativo 24 horas)42. |
| **Coquimbo** \[cite: 43, 44\] | Peñuelas, Punta Mira, San Juan43. | Tanques de distribución fijos y rotación de camiones aljibe de emergencia42. | Fono Clientes: 600 400 4444\. WhatsApp: \+56 9 9900 0325 (Soporte Operativo 24 horas)42. |

### **Destrucción de Conectividad Vial, Aérea y Sanitaria**

El desastre no se limitó al suministro de agua potable, sino que inhabilitó de manera generalizada las comunicaciones y transportes de la Región de Coquimbo38:

* **Ruta 5 Norte (Km 499):** Un alud de barro, rocas de gran tonelaje y escombros interrumpió de manera total el tránsito de la principal vía terrestre de conexión del país, requiriendo el despliegue de excavadoras y cargadores frontales de la sociedad concesionaria Ruta del Algarrobo para despejar al menos una vía provisoria38.  
* **Aeropuerto La Florida (La Serena):** El frente de mal tiempo, caracterizado por ráfagas de viento de hasta 60 ![][image3] y nula visibilidad, obligó a la Dirección General de Aeronáutica Civil (DGAC) y a las aerolíneas LATAM, SKY y JetSMART a suspender la totalidad de las operaciones aéreas hacia y desde la ciudad de La Serena, aislando por vía aérea a la zona afectada46.  
* **Hospital de La Serena:** La estructura hospitalaria sufrió el colapso del muro perimetral de deslinde con la cancha del recinto asistencial, ubicado en la Población Minas, paralelo a la calle Juan de Dios Pení, producto del empuje hidrostático del agua acumulada en las calzadas aledañas49.  
* **Hospital de Ovalle:** El frente climático penetró en la infraestructura del hospital, provocando filtraciones de agua y daños materiales en las dependencias asistenciales, limitando temporalmente su capacidad operativa de respuesta sanitaria ante heridos45.

## **Propuestas Técnicas de Optimización e Interoperabilidad de Sistemas**

La superación de las brechas de datos identificadas durante el temporal de julio de 2026 requiere la implementación de soluciones técnicas basadas en arquitecturas de integración de sistemas y sensores autónomos4.

### **Modelo Matemático de Vulnerabilidad Sistémica de Cuenca**

Para evaluar la resiliencia tecnológica de una cuenca frente a desbordes y aluviones, se propone la formulación del Índice de Vulnerabilidad Sistémica de Cuenca (![][image4]), expresado formalmente mediante la siguiente ecuación:  
![][image5]  
Donde:

* ![][image6] es el índice adimensional de riesgo hidrológico, derivado de la saturación de los suelos y el caudal máximo instantáneo proyectado por el modelo WRF15.  
* ![][image7] es el tiempo de latencia en la toma de decisiones políticas y difusión de alertas (expresado en horas desde la detección del umbral crítico por la DGA hasta la activación efectiva del SAE)1.  
* ![][image8] es el coeficiente de integración tecnológica entre las bases de datos de despacho asistido (CENCO CAD, Viper y FireCloud), con un rango cerrado ![][image9]29.  
* ![][image10] es el índice de intensidad de sensores telemétricos con transmisión IP68/LoRaWAN instalados de manera efectiva a lo largo de las quebradas de la cuenca14.

La ecuación indica que para mitigar la vulnerabilidad sistémica de la conurbación (![][image4]), el Estado debe reducir la latencia de alerta (![][image7]) incrementando tanto el coeficiente de interoperabilidad de los sistemas de respuesta (![][image8]) como la red física de sensores telemétricos de advertencia temprana (![][image10])1.

### **Arquitectura de Integración Táctica Interinstitucional**

La principal propuesta técnica de integración radica en el desarrollo de una **Plataforma Unificada de Despacho Multiagencia (PUDM)** basada en servicios web seguros y APIs estructuradas bajo el protocolo estándar de intercambio CAP (Common Alerting Protocol)1. Esta arquitectura permitirá la integración en tiempo real de los sistemas CAD de las diversas agencias de respuesta29:

\+--------------------------------------------------------------------------+  
|                       ORGANISMOS DE MONITOREO                            |  
|  \- DMC (Modelos WRF, GOES-19 Infrarrojo/GLM)                  |  
|  \- DGA (XML Telemetría Caudal, Presión MEE)               |  
\+------------------------------------+-------------------------------------+  
                                     |  
                                     v (Protocolo CAP / Web Services)  
\+--------------------------------------------------------------------------+  
|               PLATAFORMA UNIFICADA MULTIAGENCIA (PUDM)                   |  
|  \- Motor de Geolocalización Activa e Inmediata de Llamadas    |  
|  \- Análisis de Tránsito y Rutas Logísticas de Ayuda (MTT) \[cite: 50\]      |  
\+------------------------------------+-------------------------------------+  
                                     |  
           \+-------------------------+-------------------------+  
           |                         |                         |  
           v                         v                         v  
\+-----------------------+ \+-----------------------+ \+-----------------------+  
|   CARABINEROS CAD     | |     BOMBEROS CAD      | |    SENAPRED / SAE     |  
| \- CENCO CAD| | \- Viper    | | \- Cell Broadcast    |  
| \- CCTV Alpha 1 \[cite: | | \- FireCloud| |   (SUBTEL) |  
|   68\]                 | | \- Red P25  | | \- Visor Preparado   |  
| \- Móvil Satelital TIC | | \- CACBPA   | |            |  
\+-----------------------+ \+-----------------------+ \+-----------------------+

Esta estructura mitiga la fragmentación de bases de datos operacionales, permitiendo que un evento ingresado al sistema 133 de Carabineros con coordenadas satelitales estimadas se replique de forma automática e inmediata en los terminales de despacho Viper de las centrales 132 de Bomberos, optimizando el despacho conjunto de unidades especializadas ante aluviones o colapso de edificaciones29.  
La implementación de esta arquitectura integrada, sumada al fortalecimiento de las capacidades telemétricas de monitoreo físico a nivel de cuenca, transformará de manera sustancial la eficiencia del ecosistema de seguridad civil chileno, protegiendo la vida humana y la infraestructura crítica del país ante la inminente reactivación de dinámicas climáticas severas6.

#### **Fuentes citadas**

> 1. Sistemas de Alerta de Emergencias \- BCN, [https://www.bcn.cl/obtienearchivo?id=repositorio/10221/36509/1/Sistemas\_Alerta\_Emergencias\_SUP\_142380.pdf](https://www.bcn.cl/obtienearchivo?id=repositorio/10221/36509/1/Sistemas_Alerta_Emergencias_SUP_142380.pdf)  
> 2. APRUEBA REGLAMENTO ORGÁNICO FUNCIONAL, ESTABLECE ORGANIZACIÓN INTERNA Y DE FUNCIONAMIENTO DEL SERVICIO NACIONAL DE PREV \- Senapred, [https://archivos.senapred.gob.cl/main.html?download\&weblink=ebeaa3993c98cc69af3d9c975b7d1db2\&realfilename=ROF$20SENAPRED$202023$20RES$20EX$20N$20616$20DEL$2005JUN2023.pdf](https://archivos.senapred.gob.cl/main.html?download&weblink=ebeaa3993c98cc69af3d9c975b7d1db2&realfilename=ROF$20SENAPRED$202023$20RES$20EX$20N$20616$20DEL$2005JUN2023.pdf)  
> 3. INFORME ESTADÍSTICO ANUAL DE SENAPRED 2022, [https://energia.gob.cl/sites/default/files/documentos/20240214\_informe\_estadistico\_2022\_vfinal\_pagenumber.pdf](https://energia.gob.cl/sites/default/files/documentos/20240214_informe_estadistico_2022_vfinal_pagenumber.pdf)  
> 4. [https://www.adnradio.cl/2026/07/20/donde-estaban-los-militares-vecinos-increpan-al-biministro-de-grange-durante-visita-a-zona-afectada-por-aluvion/](https://www.adnradio.cl/2026/07/20/donde-estaban-los-militares-vecinos-increpan-al-biministro-de-grange-durante-visita-a-zona-afectada-por-aluvion/)  
> 5. Región del Maule \- SENAPRED | Servicio Nacional de Prevención y Respuesta ante Desastres, [https://www.senapred.cl/category/region-del-maule/](https://www.senapred.cl/category/region-del-maule/)  
> 6. Temporal de Chile de 2026 \- Wikipedia, la enciclopedia libre, [https://es.wikipedia.org/wiki/Temporal\_de\_Chile\_de\_2026](https://es.wikipedia.org/wiki/Temporal_de_Chile_de_2026)  
> 7. Sistema frontal en Chile: hasta cuándo llueve en Santiago, cómo avanza el temporal y qué pasará con las clases, [https://elpais.com/chile/2026-07-21/sistema-frontal-en-chile-como-avanza-desde-el-norte-hasta-cuando-dura-la-lluvia-en-santiago-y-que-pasara-con-las-clases.html](https://elpais.com/chile/2026-07-21/sistema-frontal-en-chile-como-avanza-desde-el-norte-hasta-cuando-dura-la-lluvia-en-santiago-y-que-pasara-con-las-clases.html)  
> 8. Chile declaró el estado de catástrofe tras un temporal que dejó al menos 10 muertos y más de 1.100 viviendas destruidas, [https://www.infobae.com/america/america-latina/2026/07/21/chile-declaro-el-estado-de-catastrofe-tras-un-temporal-que-dejo-al-menos-10-muertos-y-mas-de-1100-viviendas-destruidas/](https://www.infobae.com/america/america-latina/2026/07/21/chile-declaro-el-estado-de-catastrofe-tras-un-temporal-que-dejo-al-menos-10-muertos-y-mas-de-1100-viviendas-destruidas/)  
> 9. Alcaldesa de La Serena pide decretar Zona de Catástrofe tras reportar “11 desaparecidos”, [https://www.pauta.cl/actualidad/2026/07/20/alcaldesa-de-la-serena-pide-decretar-zona-de-catastrofe-tras-reportar-11-desaparecidos.html](https://www.pauta.cl/actualidad/2026/07/20/alcaldesa-de-la-serena-pide-decretar-zona-de-catastrofe-tras-reportar-11-desaparecidos.html)  
> 10. Catástrofe en Región de Coquimbo deja 5 muertos y 10 desaparecidos en La Serena, [https://www.elobservatodo.cl/noticia/sociedad/catastrofe-en-region-de-coquimbo-deja-5-muertos-y-10-desaparecidos-en-la-serena](https://www.elobservatodo.cl/noticia/sociedad/catastrofe-en-region-de-coquimbo-deja-5-muertos-y-10-desaparecidos-en-la-serena)  
> 11. [https://www.eldinamo.cl/pais/2026/07/20/sistema-frontal-alcaldesa-reporta-15-personas-desaparecidas-y-otras-90-aisladas-en-la-serena/](https://www.eldinamo.cl/pais/2026/07/20/sistema-frontal-alcaldesa-reporta-15-personas-desaparecidas-y-otras-90-aisladas-en-la-serena/)  
> 12. Municipalidad de La Serena pide decretar Estado de Catástrofe por grave emergencia climática \- Nuevo Poder, [https://www.nuevopoder.cl/municipalidad-de-la-serena-pide-decretar-estado-de-catastrofe-por-grave-emergencia-climatica/](https://www.nuevopoder.cl/municipalidad-de-la-serena-pide-decretar-estado-de-catastrofe-por-grave-emergencia-climatica/)  
> 13. Lentitud en medio del desastre: Tras cinco días de emergencia gobierno decreta Estado de Excepción | El Mostrador, [https://www.elmostrador.cl/noticias/pais/2026/07/21/lentitud-en-medio-del-desastre-tras-5-dias-de-emergencia-gobierno-decreta-estado-de-excepcion/](https://www.elmostrador.cl/noticias/pais/2026/07/21/lentitud-en-medio-del-desastre-tras-5-dias-de-emergencia-gobierno-decreta-estado-de-excepcion/)  
> 14. Medidores Digitales de Agua y Telemetría APR Coquimbo, Ovalle, Valle de Elqui, [https://www.sistemanacionalapr.com/telemetria-y-medidores-inteligentes-cuarta-region-ovalle-coquimbo-valle-de-elqui](https://www.sistemanacionalapr.com/telemetria-y-medidores-inteligentes-cuarta-region-ovalle-coquimbo-valle-de-elqui)  
> 15. Satélite/Modelo \- Servicios Climáticos, [https://climatologia.meteochile.gob.cl/application/index/menuTematicoModeloSatelite](https://climatologia.meteochile.gob.cl/application/index/menuTematicoModeloSatelite)  
> 16. PORTAL DE SERVICIOS CLIMÁTICOS, [https://climatologia.meteochile.gob.cl/application/requerimiento/producto/RE0005](https://climatologia.meteochile.gob.cl/application/requerimiento/producto/RE0005)  
> 17. Modelo Numérico \- WRF | \- Servicio Meteorológico de la Armada, [https://meteoarmada.directemar.cl/meteo/site/edic/base/port/Modelo.html](https://meteoarmada.directemar.cl/meteo/site/edic/base/port/Modelo.html)  
> 18. Se acerca el quinto sistema frontal al Norte Chico: A partir de esta hora se intensificará la lluvia en Coquimbo \- Megatiempo, [https://www.megatiempo.cl/pronostico/13252-lluvia-coquimbo-manana-martes-21-de-julio-2026-1ab.html](https://www.megatiempo.cl/pronostico/13252-lluvia-coquimbo-manana-martes-21-de-julio-2026-1ab.html)  
> 19. Bots atacan a alcaldes de Coquimbo y La Serena por criticar al gobierno en medio de la emergencia \- El Coquimbano, [https://www.elcoquimbano.cl/2026/07/20/bots-atacan-a-alcaldes-de-coquimbo-y-la-serena-por-criticar-al-gobierno-en-medio-de-la-emergencia/](https://www.elcoquimbano.cl/2026/07/20/bots-atacan-a-alcaldes-de-coquimbo-y-la-serena-por-criticar-al-gobierno-en-medio-de-la-emergencia/)  
> 20. Chile tendrá su primer radar meteorológico: Universidad de Valparaíso lidera el proyecto que transformará la investigación y la gestión climática del país, [https://www.uv.cl/archivo-noticias-uv/28540-chile-tendra-su-primer-radar-meteorologico-universidad-de-valparaiso-lidera-el-proyecto-que-transformara-la-investigacion-y-la-gestion-climatica-del-pais](https://www.uv.cl/archivo-noticias-uv/28540-chile-tendra-su-primer-radar-meteorologico-universidad-de-valparaiso-lidera-el-proyecto-que-transformara-la-investigacion-y-la-gestion-climatica-del-pais)  
> 21. Sistema Hidrométrico en Línea | Dirección General de Aguas \- DGA, [https://dga.mop.gob.cl/sistema-hidrometrico-en-linea/](https://dga.mop.gob.cl/sistema-hidrometrico-en-linea/)  
> 22. DGA suma nueva estación de monitoreo de embalses y lagos en la Región del Maule, [https://dga.mop.gob.cl/dga-suma-nueva-estacion-de-monitoreo-de-embalses-y-lagos-en-la-region-del-maule/](https://dga.mop.gob.cl/dga-suma-nueva-estacion-de-monitoreo-de-embalses-y-lagos-en-la-region-del-maule/)  
> 23. PREGUNTAS FRECUENTES \- DGA, [https://dga.mop.gob.cl/uploads/sites/13/2024/08/preguntas\_frecuentes\_aguas\_superficiales.pdf](https://dga.mop.gob.cl/uploads/sites/13/2024/08/preguntas_frecuentes_aguas_superficiales.pdf)  
> 24. Telemetría y Monitoreo de Pozos de Agua \- Hach Chile, [https://cl.hach.com/monitoreo-de-pozos](https://cl.hach.com/monitoreo-de-pozos)  
> 25. Visor Chile Preparado \- SENAPRED | Servicio Nacional de Prevención y Respuesta ante Desastres, [https://senapred.cl/visor-chile-preparado/](https://senapred.cl/visor-chile-preparado/)  
> 26. Chile Alerta: Descarga la App en tu dispositivo Android o iOS, [https://app.chilealerta.com/](https://app.chilealerta.com/)  
> 27. Descarga la App en tu dispositivo Android o iOS \- Chile Alerta, [https://app.chilealerta.com/e/terms.html](https://app.chilealerta.com/e/terms.html)  
> 28. departamento de inspeccion \- DT, [https://dt.gob.cl/transparencia/Circ-2000-208-2024\_Proced-JEX-Centrales-Comunica-Bomberos.pdf](https://dt.gob.cl/transparencia/Circ-2000-208-2024_Proced-JEX-Centrales-Comunica-Bomberos.pdf)  
> 29. Zoom al 133 de Carabineros: 1 minuto con 27 segundos de espera y cuatro de cada cinco llamados no generan procedimientos \- La Tercera, [https://www.latercera.com/la-tercera-pm/noticia/zoom-al-133-de-carabineros-1-minuto-con-27-segundos-de-espera-y-cuatro-de-cada-cinco-llamados-no-generan-procedimientos/](https://www.latercera.com/la-tercera-pm/noticia/zoom-al-133-de-carabineros-1-minuto-con-27-segundos-de-espera-y-cuatro-de-cada-cinco-llamados-no-generan-procedimientos/)  
> 30. edicion abril 2012 by ISRAEL \- Issuu, [https://issuu.com/carabinerosdechile/docs/684\_abril\_2012/38](https://issuu.com/carabinerosdechile/docs/684_abril_2012/38)  
> 31. “El sistema P25 en Bomberos de Chile es una realidad” Presidente Nacional en visita a Cenco, [https://www.bomberos.cl/contenidos/home-noticias/el-sistema-p25-en-bomberos-de-chile-es-una-realidad-presidente-nacional-en-visita-a-cenco](https://www.bomberos.cl/contenidos/home-noticias/el-sistema-p25-en-bomberos-de-chile-es-una-realidad-presidente-nacional-en-visita-a-cenco)  
> 32. Escritorio Virtual \- Bomberos de Chile, [https://www.bomberos.cl/sist/escritorio\_virtual/](https://www.bomberos.cl/sist/escritorio_virtual/)  
> 33. “RECEPCIÓN DE LA ALARMA Y PROCESO DE DESPACHO” \- Cuerpo de Bomberos de Punta Arenas, [https://www.bomberospuntaarenas.cl/wp-content/uploads/2020/11/C.3.6-Recepcion-de-la-Alarma-y-Proceso-de-Despacho-v0.2.pdf](https://www.bomberospuntaarenas.cl/wp-content/uploads/2020/11/C.3.6-Recepcion-de-la-Alarma-y-Proceso-de-Despacho-v0.2.pdf)  
> 34. FireCloud | Plataforma Operativa para Cuerpos de Bomberos, [https://firecloud.cl/](https://firecloud.cl/)  
> 35. CBS | Sistema de Despacho Asistido por Computadora, [https://www.cbs.cl/wp-content/uploads/2021/12/2020-055-Establece-Sistema-de-Despacho-Asistido-por-Computadora.pdf](https://www.cbs.cl/wp-content/uploads/2021/12/2020-055-Establece-Sistema-de-Despacho-Asistido-por-Computadora.pdf)  
> 36. VIPER llega con su software de gestión de emergencias a Ecuador, [https://blog.viper.cl/viper-llega-con-su-software-de-gesti%C3%B3n-de-emergencias-a-ecuador-m%C3%A9xico-y-colombia-y-alista-chatbot-con-ia](https://blog.viper.cl/viper-llega-con-su-software-de-gesti%C3%B3n-de-emergencias-a-ecuador-m%C3%A9xico-y-colombia-y-alista-chatbot-con-ia)  
> 37. “Manager \+”: comenzó a implementarse el nuevo software contable para los Cuerpos de Bomberos, [https://www.bomberos.cl/contenidos/manager-comenzo-a-implementarse-el-nuevo-software-contable-para-los-cuerpos-de-bomberos](https://www.bomberos.cl/contenidos/manager-comenzo-a-implementarse-el-nuevo-software-contable-para-los-cuerpos-de-bomberos)  
> 38. Gobierno decreta estado de catástrofe para Coquimbo y provincia del Huasco por estragos de las lluvias más intensas en 39 años \- La Tercera, [https://www.latercera.com/nacional/noticia/gobierno-decreta-estado-de-catastrofe-para-coquimbo-y-provincia-del-huasco-por-estragos-de-las-lluvias-mas-intensas-en-39-anos/](https://www.latercera.com/nacional/noticia/gobierno-decreta-estado-de-catastrofe-para-coquimbo-y-provincia-del-huasco-por-estragos-de-las-lluvias-mas-intensas-en-39-anos/)  
> 39. “¿Dónde estaban los militares?”: vecinos increpan al biministro De Grange durante visita a zona afectada por aluvión \- ADN Radio, [https://www.adnradio.cl/2026/07/20/donde-estaban-los-militares-vecinos-increpan-al-biministro-de-grange-durante-visita-a-zona-afectada-por-aluvion/?outputType=amp](https://www.adnradio.cl/2026/07/20/donde-estaban-los-militares-vecinos-increpan-al-biministro-de-grange-durante-visita-a-zona-afectada-por-aluvion/?outputType=amp)  
> 40. Vecinos de El Islón alertaron a Gustavo Huerta para que no quedara atrapado: "Aquí podíamos quedar aislados" \- Meganoticias, [https://www.meganoticias.cl/amp/nacional/527492-gustavo-huerta-alerta-vecinos-el-islon-aluvion-despacho-meganoticias-21-07-2026.html](https://www.meganoticias.cl/amp/nacional/527492-gustavo-huerta-alerta-vecinos-el-islon-aluvion-despacho-meganoticias-21-07-2026.html)  
> 41. VIDEO|"¿Dónde estaban los militares?": Mujer increpa a biministro De Grange durante punto de prensa, video pertenece a transmisión de CHV Noticias \- Diario El Centro, [https://www.diarioelcentro.cl/2026/07/20/videodonde-estaban-los-militares-mujer-increpa-a-biministro-de-grange-durante-punto-de-prensa-video-pertenece-a-transmision-de-chv-noticias/](https://www.diarioelcentro.cl/2026/07/20/videodonde-estaban-los-militares-mujer-increpa-a-biministro-de-grange-durante-punto-de-prensa-video-pertenece-a-transmision-de-chv-noticias/)  
> 42. Corte de agua en La Serena y Coquimbo se extiende: ¿Hay plazo para reponer el servicio?, [https://www.elobservatodo.cl/noticia/sociedad/corte-de-agua-en-la-serena-y-coquimbo-se-extiende-hay-plazo-para-reponer-el-servici](https://www.elobservatodo.cl/noticia/sociedad/corte-de-agua-en-la-serena-y-coquimbo-se-extiende-hay-plazo-para-reponer-el-servici)  
> 43. Aguas del Valle confirmó suspensión del suministro en sectores de Coquimbo y La Serena, [https://www.cooperativa.cl/noticias/pais/region-de-coquimbo/aguas-del-valle-confirmo-suspension-del-suministro-en-sectores-de/2026-07-19/131706.html](https://www.cooperativa.cl/noticias/pais/region-de-coquimbo/aguas-del-valle-confirmo-suspension-del-suministro-en-sectores-de/2026-07-19/131706.html)  
> 44. Anuncian corte parcial de agua potable en sectores de La Serena y Coquimbo \- TVN, [https://www.tvn.cl/noticias/datos-y-servicios/anuncian-corte-parcial-de-agua-potable-en-sectores-de-la-serena-y-coquimbo](https://www.tvn.cl/noticias/datos-y-servicios/anuncian-corte-parcial-de-agua-potable-en-sectores-de-la-serena-y-coquimbo)  
> 45. Sistema frontal se reactiva esta tarde: Coquimbo y La Serena suman daños y cortes de agua | El Mostrador, [https://www.elmostrador.cl/noticias/pais/2026/07/19/sistema-frontal-se-reactiva-esta-tarde-coquimbo-y-la-serena-suman-danos-y-cortes-de-agua/](https://www.elmostrador.cl/noticias/pais/2026/07/19/sistema-frontal-se-reactiva-esta-tarde-coquimbo-y-la-serena-suman-danos-y-cortes-de-agua/)  
> 46. Chile.- Lluvias dejan superávit de 38% en La Serena y continuarán hasta el martes, [https://www.notichile.cl/chile/noticia-chile-lluvias-dejan-superavit-38-serena-continuaran-martes-20260719225038.html](https://www.notichile.cl/chile/noticia-chile-lluvias-dejan-superavit-38-serena-continuaran-martes-20260719225038.html)  
> 47. Reporte del tiempo hoy 21 de julio para la Región de Coquimbo | La Serena Online, [https://laserenaonline.cl/2026/07/21/reporte-del-tiempo-hoy-21-de-julio-para-la-region-de-coquimbo/](https://laserenaonline.cl/2026/07/21/reporte-del-tiempo-hoy-21-de-julio-para-la-region-de-coquimbo/)  
> 48. Suspenden todos los vuelos a La Serena por sistema frontal \- Chócale, [https://chocale.cl/2026/07/suspenden-todos-los-vuelos-a-la-serena-por-sistema-frontal/](https://chocale.cl/2026/07/suspenden-todos-los-vuelos-a-la-serena-por-sistema-frontal/)  
> 49. Registran impactantes inundaciones en La Serena tras el temporal \- CNN Chile, [https://www.cnnchile.com/pais/registran-impactantes-inundaciones-en-la-serena-tras-el-temporal/](https://www.cnnchile.com/pais/registran-impactantes-inundaciones-en-la-serena-tras-el-temporal/)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACIAAAAZCAYAAABU+vysAAABD0lEQVR4Xu2UMU5CQRRFX0JjgTtQtkDLAky0spFEN0FC6GAzFBa6AaOJNaFArAgFLEJbaOA+573vZeLPhGhh8U5yihnmTObPD18kCILg9wzgJ9zBjvkK3+EbbMEhfIJz2DedvNe21P9IA44kbTQ2T+y3KVzDGxu34dY8t7m817bUa+v9AZdyeCPOI1zQ+FTSOtU3V7hn6nptua/wjfQaVecBvtC4Kd8H6dI890xdry33Ff/mIBeSFpyZzj18prG+ez/ILc1zz9T12nJf4U+UH0SfiDfiG+GNuGfq+uJBjnk1dzR/7KvRlvsvenApacHMvJb0v/+AG0nfhSs4sXXqStL3Ie+1LfXaeh8EQfAn7AGWR26f4q1h8QAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAbCAYAAABr/T8RAAABV0lEQVR4Xu3UPyiFYRQG8JM/gxKTkn8jyWRhdFMmoZuRDLIoWSzKyIhkNDEYKSsxyJ/BJmSRUoqNTDLwPN7n7R73u4a7fErfU7/hPZ3ve29951yzLFmy/Ke0wZXUuPoSzLrzHLzCC/TBPlzDoTTAKhzACQyGx37PJDyKzzOMu3MlLMIHrEO1PMgNdKuX7+S5QkpmE3YlphM+od3VmFHVu1ztXHZcbcBCX6OUzD3MSwx/8ZM7x8SL613tVNZcrd9CX7Mk0mShIScxG7DnzjEjFvprXe1Y/MU5C30tksifXTxsoYHT7Ceag7EAvTAhTN6SF3OCqayLOaVs6BBmWrUxWIZWYeI3rtOZOZNS35irSolw546ssIvbFlaIw3UBU4XW752+tfBCTjH3lM+/C9dvy8Kzl+rjO+jHTlfBGwz5YhrpscLIp5oZuCsuphH+F68UF7NkyVJuvgBRoFxoQjhvmAAAAABJRU5ErkJggg==>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAZCAYAAABzVH1EAAACLElEQVR4Xu2XTYhNYRjH/2KhSKMoCxSzFmUnDaF8ZSXERuxthGHBDjMblCjJRmHhKymRr+x8lKywoGRjYTJmRGHB/9/zHPOcZ869uN3mdmfmV7+673Pec8/5v+d933MvME5TOZILjbCY7qEH8oERYgHdnYuNsI2+pl/zgRHiIJ3nn4/RX8GOotO/MGqCiJ1oXZALqb3VbasgC2HrM7LebSjIdrQmiHaruanW1CBLMDRPX9BZ9BL97j6APcXb9C29TGfSM/Seqz4rUJsJ9EouktWurr2c3qVP6UU6fahbNQryLbRn0/ewkSmYQm+4A7ApoZuZQX/SJ3T+n97AXvostDNddF8uohzkPJ0Mu46+qzv0q0RBfsBOko9QDlHQ6w7SSaH+iZ4IbbEJdjNTU73gJO3MRZSDaGYUXKXXQ7sSBdGo3nQ/wkY60+O+SnX1z6O7EdVBNLpSU6aKGGROqGv6jq0gWsRb3Of0XKmHcdh9mer1gkxLdW0Acn+qF6xxda7WaoGCaH3WZQf9ENrLYF+0NtTEUfd/guQt9JQbRzuitSmrgmi21EVbaQwitN29Q/mCxWLXT5pIP4YH2YzhQSbSO24tYpD4jrmGvwQ5RN/ATnzoLqJ9XvsCC3oWFlaqrjm+jt73trbr47BAUutI9cd0FYyV4XgVu2BPW+pcvT82wN5Xn2H3outqQGTLOA17wrWmVVugnepWLrYjS9G6P29NRSHiT5i2ZdQEGWdM8Rv6K5+G+HPceQAAAABJRU5ErkJggg==>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAcCAYAAABh2p9gAAAA9klEQVR4Xu3SMQtBURgG4GMgZSMGg/wBG4NSwqTkH5gMMkk2AxaJxUIZTP6AxGZXVqtRGQ0MJvGefPicuLd7Upb71lO37z19dW5HCDu/iA9WcGV2kGJnkuRE/RZirP+YBdmrBUsbKurwW8bkAi6l85OlMjdMg8grhd8r0SWm1+QpErkwzuZBGBJLyRK5MM/mffG6sqX8fGGEyIVlNqs+T1iMl8iFLZrJ/+Z8HNDNGUaQgLTSaWUDM6irhW7mcICQWlDc0IOmeP0awwzE/YF/SwYmEBX/WmgW+RKmcISC0llOANb0LR9/jXVa8UAHSpADx3ttx45WbkIjMPScrTuUAAAAAElFTkSuQmCC>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAABCCAYAAADqrIpKAAADxElEQVR4Xu3dS8jlYxwH8MedcanBxm1Q45JLYRYaJeOyEAsbySULKVnIWCBC3mQhl7KRS66hKFHGZTJ2rkWUhZE0szFDsrAiNvyenv9xnvN03td7znnH+df7+dS3839+z+mc7dPz//9/T0oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAq9Uxkd8if0c+i/wa+Taypv4SAADz9VZkZ2SvbnxRZMtwGgCAecu7a1dW46Mjr1RjAADmLC/Y1nbXZ0a2Rg4fTk/ttlRusebfH+SWkW8AALAsuyL3RR6O/JTKQmslPB+5OHJJZFOXwcIQAIBlOiNybTX+MPJ5Nd4v8nE1HifvnN3YFitPtYXOz5Fz2iIAAKNuiqyvxrsj31Tj7PFm3NoW2dgWK9+3hc6PkX3aIgAAo15sxnm3LO+y1a5uxpM4OZXfHCe/nQoA0Ht5l2nwQP66qj7ojXZDVVtJz6bhf+QdslO7+t2p9GEb3CY9K3JId52fdZvUk5FHq/H2yLnd9dlVHQCgt45IZdH0clO/I/JQU5uHzd3nhsgb9cSUdnSf+6Zh3zcAgF7Li5bfU9nlqn0S2b+pzcNr3ecTkevqiSm91H1eGrk8ckA1BwDQW+9E/qjGx1XXAAD0wDNp9MH8/HwZAAA9kl8syAu23PPshWZuTzmyZwEA6LV8EkBesN0cOaWZ21O+7lHuTwAAPZdbauQF2+Z24j/sHbkzlWOlFsvx/34bAICZ7GwLnfMit6f/b+cNAIAJ5Sa2+aio3LcMAICe2ZJKn7Z8GPuBzdxKyud5Xh95N5X/+iqVhr5tM99Z/JDKbd984PtjzRwAAEs4KvJFZG1Tz4urq5raLDalxc8UBQBgCW9Gjm2L4a9UFnMr5d5kwQYAMLGNafFF1HNtYUbvp3I7FACAZcotQfJxWNvbiSnlt1jXtMXKNG1LAABWtXWpLKJebyfGyG1FlrI+8mcaHuw+Tv6vDW0RAICl5cXaL20xPN0WOvnorJxpfNCM72rGAACMcUJkRxq9lflI5LTu+uDIA5FDIxdEXk3l5YHcBmQSp0cWuuvcpuSeyK7IhYMvAACwuNxv7cvI1siDkcOquctSud15UDdeGE4ty0mRT1N5Vu67yLaunnvKjdvZAwBgCvntzitSWbTtjlwzOj2VhcitkfObOgAAU3gvcmIqz659lMqO26zyou/ttggAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKwq/wCB1Z/RIRWg/QAAAABJRU5ErkJggg==>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAbCAYAAACJISRoAAABUElEQVR4Xu3UPShFYRgH8Ec+MxmYlLLJYDJZ3HyV0WhSd5VFYlIMPhaKwcDGIimDDFIkmzIgXymDyUZMJv5Pz//N21NX7j2nO+j861fvfZ5z7nve97wdkSwJskA38AVPcASP8AJL1BxuKCVlmSRkSGySXFRrhXN6hvqoV1Lm4RWqXD2sRB+gy/WKzgns+SJyQXdQ63p/jm6B+oSxqN4k9q4eqCPqFZ1e0u1YE9saffnhdwMlyjR9QCVrFbALy+GipDmkU1efEFtNI4XUwRYcRLVfoyfpnVZcb11skhaKMwUzrlYwZZmkU+yP1IjrhS9AOH1x9qHf1QpGnyhM0u5696xX0wAMix2ON5iEOdgIN/jk4Ep+JlDHMBpd0y32OTmjWbFTp6u/FTsAusLrcEOaGYdFjgdhNeqllh3o43gbeiBPqeUSajjeFPv0tFGWLP8l38AlVPBIDvTtAAAAAElFTkSuQmCC>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABIAAAAaCAYAAAC6nQw6AAAAz0lEQVR4XmNgGAWjgHrAHYhvAvF/HLgPoRQ3UAXiDUDsBcQOUHwFiHOA2AXKl4YoxQ8igVgSyhaH4iMIafJAChRPRZdAAqFQ/BGI5dDk4GApFGeiSyABXii+iy4BA8xA/BKK7dDkkIErFC9AE4cDKwZELAmgyekC8SYgbgLivVCchKICCYAk9kMxMmAH4utAbATln4JiFbgKIoETAySNgQAPEN+DYpJBCBDPR2IvguJgIGaCKSIGiADxPgZIklgAZYNwMpIaogDVDBoFgw0AANPmLUT/m1cxAAAAAElFTkSuQmCC>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABoAAAAbCAYAAABiFp9rAAABR0lEQVR4Xu3UvSuFURzA8V/yLgNhI68DZptBYbIoKYMUxWxXymCwWBmUwVspZbgWpEikWIxKJPEniIXv6fwezv313OJ6rsX91qee55yn+9zOPfeI5Eu4YkziALe4wDHa0KHmP5/+RTl/Ubu6xj2GUaZz1djFsxrV8R/XiEd1iPK0Wd8g3lWTmft2+3hQNWYuyi3ZncqqXvHfclplqh4zKqv28IYqlZMK8IJLO5F0zeKXbdVOxDRlB8SvRqcdjKsSr9iyE6YuzNpBag2uS3EW3Kf1Zy9y7Yjf1iXK1iB+iTJt+6gebNjBsBY8YU25IyiqG9uoC8Zc7ndZxJLej+EcmxhRsbkPWlZXSGEO4ygMnouawADWg7ET8UdY4q2gT68rxC9/4rlNdINa8cvbL1/LPqQSyZ0gp+JPcfend+fgERZQpPLl+w99AE9pQCaksGO/AAAAAElFTkSuQmCC>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEkAAAAZCAYAAAB9/QMrAAACGklEQVR4Xu2YzytFQRTHjx9l5UeshJ0Vkl9JYSfWLLFSFoqdDWWhJAuF7LARFhYkGwuxVn7+G0oWFkoS55gzOW/M3GbeeLx0P/Wp15nbud85777evRcgJeUnKUD30Dm0nv3vtILa75a54KIQ3TGLSDG6jd6hl+hk5nIiRewIem6shZBtH1t2W366OLxIh+SBa0ir6CaoE5agx+hsxhF2rtEj9hZUyGyI6WPLbssfNaRa9AVtE7VB9AnUiUkfdkFtNpaQPq7sMr8makgT6DtaLWqdXOtlfQjZXBIhfVzZZX5N1JAWQTUsF7Umro2yPoRsLomQPq7sMr8makhroBqWiloj16ZYH6jvlVnMgpA+ruwyvyZqSMvw/UQNXAsZUsgVkERIH1d2mV8TNST6F6CGFaLWzLVh1gfa3I1ZzIKQPq7sMr8mHZKo5WRIQ6Aa1ohaF9folp70gTZH9zixhPRxZZf5NVFDqgTVsF3U6D7jAdTxpKZMfDZJ2lwd60NSHzq/zODKLvNrooZEbIC6cyXo0WAfXfpa/mQGvUc7jLqGNkePBib96Bs7bqzZcPUZALVxckzUbdlt+aOHRM0XQK1doOuQ+S0Q8+gz2iJqK+gp+wjqWz1DD8QxfegreyjqEp8+rmHbstvyRw8p1+ifLV0lf0XeD6mHnTYXfpG8HhK96Dthq4y13ySvh1SMdrN/STokD7yHlL7jTknJOR/hVLkknQlT8wAAAABJRU5ErkJggg==>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAcCAYAAAC+lOV/AAAAyElEQVR4XmNgGAUroPgzEP8H4t9AfByIFZEVEQJFDBDNZugSxICVQPwGiJnRJYgBz4B4NbogIaAKxSAnl6DJEQTRUAzSbIUmRxBQpHkyFP8EYnY0OYLgNBQfRJcgBPiA+C8U96LJgcB2KBZGlwABDwaIX0E4DE0OZPAlKMYKGhkQmmWQxO2BeA0Q74PiXCQ5hkggvsaA0AjCe4E4D0kNyBuwmEABFGkmBhwFYnkoJgnwAPENJD7IpUQDDgZIvPdBsSiq9CgYAgAALQIzTwGT8eQAAAAASUVORK5CYII=>

---
## 🔗 Conexiones
* [[10_Projects/Proyecto_Centinela/Knowledge/proyecto_centinela|Dashboard Proyecto Centinela]]
* [[Home|Panel de Control Unificado]]
