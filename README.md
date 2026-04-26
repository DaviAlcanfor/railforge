<div align="center">
  <h1>RailForge</h1>

  <img src="https://img.shields.io/badge/FastAPI-0.136-009688?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker" />
  <img src="https://img.shields.io/badge/Ruby_on_Rails-8.1-CC0000?style=for-the-badge&logo=rubyonrails" />
</div>

Generate production-ready Ruby on Rails APIs from a JSON definition — no Ruby installation required.

---

## How it works

You define your project name and models in JSON. RailForge spins up an isolated Docker container with Rails pre-installed, runs the generation commands, compresses the output, and returns a ready-to-use `.tar.gz` archive.
POST /generate  →  Docker container  →  rails new + models  →  .tar.gz download

No Ruby on your machine. No manual setup. Just download and run.

---

## Running

**Requirements:** Docker Desktop

```bash
git clone https://github.com/DaviAlcanfor/railforge.git
cd railforge

docker build -f backend/Dockerfile.rails -t railforge-rails backend/
docker compose up
```

API → `http://localhost:8000`  
Docs → `http://localhost:8000/docs`

---

## Usage

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
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
  }' \
  --output my-api.tar.gz
```

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/generate` | Generate a Rails API project |

**Request body:**

```json
{
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

**Supported field types:** `string`, `integer`, `boolean`, `text`, `float`, `date`, `datetime`

---

## Project Structure
backend/
├── app/
│   ├── config/        # Application settings via Pydantic Settings
│   ├── routers/       # FastAPI route definitions
│   ├── schemas/       # Pydantic request/response models
│   └── services/      # Business logic and Docker orchestration
├── Dockerfile.rails   # Pre-built Rails image for faster generation
└── main.py            # Application entrypoint with lifespan hooks

---

## How generation works

1. FastAPI receives the project definition and validates it with Pydantic
2. A `railforge-rails` container runs `rails new` and `rails generate model` for each model
3. The generated project is compressed into a `.tar.gz` inside a shared Docker volume
4. A lightweight Alpine container reads the archive and streams it back
5. The generation container is removed after each run
