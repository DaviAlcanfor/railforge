<div align="center">
  <h1>RailForge</h1>

  <img src="https://img.shields.io/badge/FastAPI-0.136-009688?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker" />
  <img src="https://img.shields.io/badge/Ruby_on_Rails-8.1-CC0000?style=for-the-badge&logo=rubyonrails" />
  <img src="https://img.shields.io/badge/NestJS-10-E0234E?style=for-the-badge&logo=nestjs" />
  <img src="https://img.shields.io/badge/Laravel-11-FF2D20?style=for-the-badge&logo=laravel" />

  <p>Generate production-ready APIs from a JSON definition — no framework installation required.</p>
</div>

---

## Supported frameworks

| Framework | Language | Generates |
|-----------|----------|-----------|
| `rails` | Ruby | model, migration, controller, routes |
| `nestjs` | TypeScript | model, service, controller, module, dto |
| `laravel` | PHP | model, migration, controller, routes |

---

## How it works

You define your framework, project name, and models in JSON. RailForge spins up an isolated Docker container with the framework pre-installed, runs the generation commands, compresses the output, and returns a ready-to-use `.tar.gz` archive.

No Ruby, PHP, or Node on your machine. No manual setup. Just download and run.

---

## Running

**Requirements:** Docker Desktop

```bash
git clone https://github.com/DaviAlcanfor/railforge.git
cd railforge
docker compose up
```

All framework images are built automatically on first run.

API → `http://localhost:8000`  
Docs → `http://localhost:8000/docs`

---

## Usage

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "framework": "rails",
    "project_name": "my-api",
    "models": [
      {
        "name": "Player",
        "fields": [
          {"name": "name", "type": "string"},
          {"name": "age", "type": "integer"}
        ]
      }
    ]
  }' \
  --output my-api.tar.gz
```

To check which field types are accepted by each framework:

```bash
curl http://localhost:8000/frameworks/rails
```

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/generate` | Generate an API project |
| `GET` | `/frameworks/` | List all supported frameworks |
| `GET` | `/frameworks/{name}` | Framework details, accepted types, and generates |

**POST /generate — request body:**

```json
{
  "framework": "rails",
  "project_name": "my-api",
  "models": [
    {
      "name": "ModelName",
      "fields": [
        {"name": "field_name", "type": "string"}
      ]
    }
  ]
}
```

---

## Project structure

```
backend/
├── app/
│   ├── config/        # Application settings via Pydantic Settings
│   ├── enums/         # FieldType, GeneratesType, FrameworkType enums
│   ├── frameworks/    # BaseFramework + Rails, NestJS, Laravel implementations
│   ├── routers/       # FastAPI route definitions
│   ├── schemas/       # Pydantic request/response models
│   └── services/      # Business logic and Docker orchestration
├── dockerfiles/       # Pre-built images for each framework
└── main.py            # Application entrypoint with lifespan hooks
```

---

## Generation flow

```
POST /generate
      │
      ▼
 Pydantic validates
 framework + models
      │
      ▼
 Framework registry
 resolves implementation
 (Rails / NestJS / Laravel)
      │
      ▼
 Docker spins up
 framework container
      │
      ├── install framework
      ├── create project
      ├── generate models
      └── run migrations
           │
           ▼
      tar -czf → shared volume (railforge_output)
           │
           ▼
      Alpine container
      reads volume → bytes
           │
           ▼
      StreamingResponse
      → .tar.gz download
           │
           ▼
      containers removed
```
