from typing import List
from pydantic import BaseModel, field_validator

from app.enums.field_types import FieldType


class ModelField(BaseModel):
    name: str
    type: FieldType

    @field_validator("name")
    @classmethod
    def name_must_be_snake_case(cls, v):
        if not v.replace("_", "").isalpha():
            raise ValueError("Field name must contain only letters and underscores")
        return v.lower()


class Model(BaseModel):
    name: str
    fields: List[ModelField]

    @field_validator("name")
    @classmethod
    def name_must_be_valid(cls, v):
        if not v.isalpha():
            raise ValueError("Model name must contain only letters")
        return v.capitalize()