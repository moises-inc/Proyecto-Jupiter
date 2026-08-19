# Contributing to Proyecto Júpiter

¡Gracias por tu interés en contribuir a **Proyecto Júpiter**! Este proyecto es de código abierto bajo la **Apache License 2.0** y busca fortalecer la resiliencia hidrometeorológica de La Serena, Chile. Tu ayuda — código, datos, documentación o reportes de bugs — es bienvenida.

## Cómo Reportar un Bug

1. Revisa primero los issues existentes para evitar duplicados.
2. Abre un issue incluyendo:
   - **Descripción clara y concisa** del problema.
   - **Pasos para reproducirlo** (mínimo reproducible).
   - Comportamiento **esperado** vs. **observado**.
   - Entorno: versión de Python (`python3 --version`), sistema operativo y *output* del comando o stack trace.
3. Indica si el bug afecta al modelo ML, al escáner espacial, a la API o al dashboard.

## Cómo Contribuir Código

### 1. Fork y Branch

- Haz *fork* del repositorio y crea una rama descriptiva desde `main`:
  ```bash
  git checkout -b feat/descripcion-corta
  ```

### 2. Estándares de Código

- **Python 3.10+** y estilo **PEP 8**.
- Documenta funciones públicas con *docstrings* (inglés o español, consistente con la zona del código).
- No agregues comentarios redundantes; documenta el *porqué*, no el *qué*.
- Mantén la arquitectura modular existente: `ML_Models/src/{features,inference,ingesters,models}` y `Dashboard/server.py`.

### 3. Test-Driven Development (TDD)

Todo cambio de comportamiento DEBE incluir o actualizar pruebas en `ML_Models/tests/`:

```bash
# Ejecuta la suite completa (38 tests) antes de enviar tu PR
pytest ML_Models/tests/ -v
```

- Todas las pruebas nuevas deben pasar de forma aislada y en conjunto.
- No se fusionan cambios que rompan la suite o reduzcan la cobertura sin justificación.

### 4. Commits

- Mensajes en español o inglés, formato convencional:
  ```bash
  git commit -m "feat(spatial-scanner): añade peso geotécnico FS al score del sector"
  git commit -m "fix(ingest): maneja timeout de estaciones CEAZAMET"
  git commit -m "docs(readme): actualiza tabla de micro-sectores WGS84"
  ```
- Nunca commitees secretos, API keys, archivos temporales (`*.pdf` de difusión, auxiliares LaTeX) ni modelos entrenados de gran tamaño sin aprobación.

### 5. Pull Request

- Describe el objetivo, los cambios y el resultado de `pytest ML_Models/tests/ -v` (debe ser **38/38**).
- Vincula el issue que resuelve (si existe).
- Mantén el PR pequeño y enfocado; se revisará por pares antes de fusionar.

## Guía para Contribuidores de Datos/Documentación

- Actualiza `Docs/wiki/*.md` cuando cambies arquitectura o modelos.
- Si agregas fuentes de datos públicas (SENAPRED, CEAZAMET, GOES), documenta licencia y atribución.
- Para investigación académica, actualiza `CITATION.cff` solo bajo revisión del mantenedor.

## Código de Conducta

Sé respetuoso, constructivo y empático. Las aportaciones deben mejorar la seguridad pública y el bien común; no se aceptan usos que pongan en riesgo a las personas.

---
🔗 [[Home]]