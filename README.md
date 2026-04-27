<div align="center">
  
  <h1>RailForge</h1>

  <img src="https://img.shields.io/badge/FastAPI-0.136-009688?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react" />
  <img src="https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript" />
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker" />
  <img src="https://img.shields.io/badge/Ruby_on_Rails-8.1-CC0000?style=for-the-badge&logo=rubyonrails" />
  <img src="https://img.shields.io/badge/NestJS-10-E0234E?style=for-the-badge&logo=nestjs" />
  <img src="https://img.shields.io/badge/Laravel-11-FF2D20?style=for-the-badge&logo=laravel" />

  <p>Generate production-ready API projects from a JSON definition — no framework installation required.</p>
</div>

---

## What it solves

Setting up a new API project from scratch takes time. You install the framework, configure the project, generate models, run migrations — before writing a single line of business logic.

RailForge automates that entire bootstrap process. You describe your project in JSON, pick a framework, and download a ready-to-run project archive in seconds. No Ruby, PHP, or Node needed on your machine.

---

## How it works

1. You open the UI, select a framework and describe your models in JSON
2. RailForge sends the definition to a FastAPI backend
3. The backend spins up an isolated Docker container with the chosen framework pre-installed
4. Inside the container, the framework CLI generates the project, models and migrations
5. The output is compressed and returned as a `.tar.gz` download
6. The container is removed

---

## Running

**Requirements:** Docker Desktop installed and running.

```bash
git clone https://github.com/DaviAlcanfor/railforge.git
cd railforge
docker compose up
```

All framework images are built automatically on first run — this may take a few minutes.

Open `http://localhost:3000` to use the UI.

---

## Supported frameworks

| Framework | Language | What gets generated |
|-----------|----------|---------------------|
| Rails | Ruby | models, migrations, controllers, routes |
| NestJS | TypeScript | modules, controllers, services, DTOs |
| Laravel | PHP | models, migrations, controllers, resources |

---

## Usage

Select a framework using the radio buttons on the left, then paste your project definition in the editor:

```json
{
  "project_name": "my-api",
  "models": [
    {
      "name": "Player",
      "fields": [
        {"name": "name", "type": "string"},
        {"name": "age", "type": "integer"},
        {"name": "active", "type": "boolean"}
      ]
    }
  ]
}
```

Click **Download** to generate and download the project as a `.tar.gz` archive.

The right panel shows the accepted field types and what the selected framework generates, so you don't need to memorize anything.

---

## API

If you prefer to use the API directly:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "framework": "rails",
    "project_name": "my-api",
    "models": [{"name": "Player", "fields": [{"name": "name", "type": "string"}]}]
  }' \
  --output my-api.tar.gz
```

Interactive docs at `http://localhost:8000/docs`.

---

## Technology choices

**FastAPI** — async Python framework with automatic validation via Pydantic. The JSON schema is validated before any container is spun up, so invalid payloads are rejected immediately.

**Docker SDK** — each generation runs in an isolated container using the framework's own CLI. This means no framework needs to be installed on the host machine, and generations don't interfere with each other.

**Shared volume** — instead of copying files directly from the container (which has throughput limitations on Windows), the generated project is compressed into a shared Docker volume and read by a lightweight Alpine container. This avoids named pipe bottlenecks.

**React + TypeScript** — the frontend fetches available frameworks and their accepted types from the API, so the reference panel always reflects what the backend actually supports. No hardcoded values on the client.

---

## Project structure

```
railforge/
├── backend/
│   ├── app/
│   │   ├── config/       # Pydantic Settings
│   │   ├── enums/        # FieldType, GeneratesType, FrameworkType
│   │   ├── frameworks/   # BaseFramework + Rails, NestJS, Laravel
│   │   ├── routers/      # FastAPI endpoints
│   │   ├── schemas/      # Request/response models
│   │   └── services/     # Docker orchestration
│   ├── dockerfiles/      # Pre-built framework images
│   └── main.py
└── frontend/
    └── src/
        ├── components/   # FrameworkSelector, ModelEditor, ReferencePanel
        ├── services/     # Axios API client
        └── types/        # Enums and interfaces
```
