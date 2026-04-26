from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import docker

from app.config.settings import settings
from app.routers import generate_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # making sure theres a ruby img

    client = docker.from_env()
    try:
        client.images.get(settings.RUBY_IMAGE)
        logger.info(f"Image {settings.RUBY_IMAGE} already available")

    except docker.errors.ImageNotFound:
        logger.info(f"Pulling {settings.RUBY_IMAGE}...")

        client.images.pull(settings.RUBY_IMAGE)
        logger.info(f"Image {settings.RUBY_IMAGE} ready")
    
    yield


app = FastAPI(
    title="RailForge",
    description="Generate production-ready Rails APIs",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate_router.router)