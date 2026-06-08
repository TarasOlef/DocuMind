# DocuMind AI

Plataforma backend empresarial para RAG documental.

## El Problema
Muchas empresas tienen documentación interna dispersa en PDFs, manuales, contratos, procedimientos, políticas, guías técnicas, documentos legales, bases de conocimiento o documentación de producto. Los empleados pierden mucho tiempo buscando información y muchas veces no saben qué documento contiene la respuesta correcta.

## La Solución: DocuMind AI
DocuMind AI permite subir documentos, procesarlos, convertirlos en conocimiento consultable y hacer preguntas en lenguaje natural. Las respuestas están basadas únicamente en el contenido real de los documentos e incluyen fuentes/citas trazables.

## Features Planeadas
- JWT Auth.
- Roles y permisos.
- Upload documental.
- Extracción de texto.
- Chunking.
- Embeddings.
- PostgreSQL + pgvector.
- Búsqueda semántica.
- RAG.
- Respuestas con citas.
- Historial de preguntas.
- Auditoría.
- Docker.
- Testing.

## Stack Técnico
- Python 3.11+
- FastAPI
- PostgreSQL + pgvector
- SQLAlchemy + Alembic
- Pytest
- Docker & Docker Compose

## Arquitectura (Clean Architecture / Hexagonal)
El proyecto está estructurado separando las preocupaciones (Clean Architecture):
- `domain`: Reglas de negocio y entidades puras. No depende de ningún framework o base de datos.
- `application`: Casos de uso y lógica de aplicación. Orquesta las peticiones entre puertos.
- `infrastructure`: Adaptadores concretos para bases de datos (SQLAlchemy), LLMs, procesamiento de documentos, etc.
- `api`: Capa fina de transporte (FastAPI).
- `shared`: Configuración, logging, errores y utilidades transversales.

### Estructura de carpetas
```text
documind-ai/
├── app/
│   ├── api/
│   ├── application/
│   ├── domain/
│   ├── infrastructure/
│   └── shared/
├── alembic/
├── docker/
├── tests/
├── .env.example
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## Estado del proyecto
Fase inicial / bootstrap. Se ha configurado la base, pero aún no se han implementado entidades del dominio ni el motor RAG.

## Ejecución local con Docker

1. Copiar archivo de entorno:
   ```bash
   cp .env.example .env
   ```
2. Levantar la aplicación y la base de datos (PostgreSQL con pgvector):
   ```bash
   docker compose up --build
   ```

## Healthcheck

Puedes comprobar que la API funciona visitando:
`GET http://localhost:8000/api/health`

## Tests

Para correr los tests en el entorno local (requiere instalar las dependencias con `pip install -e .[dev]`):
```bash
pytest
```

## Security Note
- **Nunca** subir el archivo `.env` a control de versiones.
- **Nunca** incluir API keys reales en `.env.example` o repositorios de código.
- Los providers fake se utilizan para entornos locales y demostraciones.

## Roadmap
- [x] Phase 1: Bootstrap backend (FastAPI, Clean Architecture, Docker, CI base).
- [ ] Phase 2: Auth y persistencia base.
- [ ] Phase 3: Gestión de Documents.
- [ ] Phase 4: Document Processing & Embeddings.
- [ ] Phase 5: RAG y generación de respuestas.
- [ ] Phase 6: Audit logs y refactor avanzado.
