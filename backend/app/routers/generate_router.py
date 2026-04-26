from fastapi import APIRouter
from app.services.generator_service import GeneratorService
from fastapi.responses import StreamingResponse
import io

from app.schemas.project import ProjectConfig
from app.config import settings

router = APIRouter()

@router.post("/generate")
def generate(config: ProjectConfig):
    
    generator = GeneratorService(config)
    output = generator.generate()
    
    return StreamingResponse(
        io.BytesIO(output),
        media_type="application/x-tar",
        headers={"Content-Disposition": f"attachment; filename={config.project_name}.tar.gz"}
    )