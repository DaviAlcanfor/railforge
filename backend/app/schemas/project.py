from pydantic import BaseModel, field_validator
from typing import List
from app.schemas.model_schema import Model
from app.frameworks.registry import get_framework



def _validate_project_name(name: str) -> bool:
    return name.replace("-", "").replace("_", "").isalpha()


def _normalize_name(name: str) -> str:
    return name.lower().replace(" ", "-")


class ProjectConfig(BaseModel):
    framework: str
    project_name: str
    models: List[Model]

    @field_validator("framework")
    @classmethod
    def framework_must_be_valid(cls, framework):

        get_framework(framework)
        return framework


    @field_validator("project_name")
    @classmethod
    def project_name_must_be_valid(cls, name):

        if not _validate_project_name(name):
            raise ValueError("Project name must contain only letters, hyphens or underscores")

        return _normalize_name(name)