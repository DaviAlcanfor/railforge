from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import docker

from app.frameworks.registry import FRAMEWORKS
from app.routers import generate_router
from app.routers import frameworks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    client = docker.from_env()
    
    for framework in FRAMEWORKS.values():
        try:
            client.images.get(framework.DOCKER_IMAGE)
            logger.info(f"Image {framework.DOCKER_IMAGE} already available")
        except docker.errors.ImageNotFound:
            logger.info(f"Image {framework.DOCKER_IMAGE} not found — build it with: docker build -f backend/dockerfiles/Dockerfile.{framework.NAME} -t {framework.DOCKER_IMAGE} backend/")

    yield


app = FastAPI(
    title="RailForge",
    description="Generate production-ready APIs",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate_router.router)
app.include_router(frameworks_router.router)