from pydantic import BaseModel, field_validator
from typing import List

from app.schemas.model_schema import RailsModel


class ProjectConfig(BaseModel):
    project_name: str
    models: List[RailsModel]

    @field_validator("project_name")
    @classmethod
    def project_name_must_be_valid(cls, v):
        if not v.replace("-", "").replace("_", "").isalpha():
            raise ValueError("Project name must contain only letters, hyphens or underscores")
        return v.lower().replace(" ", "-")