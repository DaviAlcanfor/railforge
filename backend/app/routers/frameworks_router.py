from fastapi import APIRouter, HTTPException
from app.frameworks.registry import FRAMEWORKS, get_framework
from app.enums.framework_types import FrameworkType

router = APIRouter(prefix="/frameworks", tags=["frameworks"])


@router.get("/")
def list_frameworks():
    return [
        {
            "name": framework.NAME,
            "generates": framework.generates(),
            "accepted_types": framework.accepted_types(),
        }
        for framework in FRAMEWORKS.values()
    ]


@router.get("/{name}")
def get_framework_detail(name: FrameworkType):
    try:
        framework = get_framework(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {
        "name": framework.NAME,
        "generates": framework.generates(),
        "accepted_types": framework.accepted_types(),
        "commands": framework.commands(),
    }