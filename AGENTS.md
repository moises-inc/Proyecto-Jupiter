# AGENTS.md (OpenCode & Agent Environment)

Este archivo configura las reglas de comportamiento, autodeclaración de habilidades y directrices de prevención de desbordamiento de tokens para agentes en este espacio de trabajo.

---

## 🛠️ Descubrimiento de Habilidades (Agent Skills)

El sistema cuenta con el paquete de habilidades de desarrollo de software `agent-skills` instalado globalmente en:
`~/.gemini/config/plugins/agent-skills/skills/`


### Reglas Críticas de Selección:
1. **Analizar la Intención:** Antes de realizar cualquier acción, comprueba si la solicitud mapea con alguna de las habilidades del directorio.
2. **Ejecutar la Habilidad:** Si una habilidad coincide, lee su archivo `SKILL.md` y sigue estrictamente su ciclo de diseño (especificación, planificación, tests TDD, implementación y revisión).
3. **Prohibido Implementar Directamente:** No saltes a escribir código o realizar cambios sin antes haber completado las fases de diseño y planificación indicadas por la habilidad.

---

## 🌐 Navegación y Automatización Web Eficiente (Playwright)

1. **Priorizar `playwright-cli`:** Para ahorrar ventana de contexto, evita usar herramientas MCP pesadas si la tarea puede realizarse con `playwright-cli` desde la consola.
2. **No Inyectar DOMs Completos:** Trabaja buscando selectores o elementos clave específicos.

---

## 📦 Directrices de Publicación Open-Source
1. **Seguridad y Cero Secretos:** Nunca expongas credenciales, API keys privadas ni rutas absolutas locales sensibles.
2. **Licencia:** Proyecto Júpiter utiliza **Apache License 2.0**.
3. **Calidad:** Todos los tests en `ML_Models/tests/` deben mantenerse al 100% de aprobación.
