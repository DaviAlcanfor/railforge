from app.frameworks.base import BaseFramework

from app.enums.commands_types import FrameworkCommands
from app.enums.field_types import FieldType
from app.enums.generates_types import GeneratesType


class NestFramework(BaseFramework):
    NAME = "nestjs"
    DOCKER_IMAGE = "railforge-nest"

    def accepted_types(self) -> list[FieldType]:
        return [
            FieldType.string, 
            FieldType.number, 
            FieldType.boolean, 
            FieldType.date, 
            FieldType.uuid, 
            FieldType.text, 
            FieldType.json
        ]

    def generates(self) -> list[GeneratesType]:
        return [
            GeneratesType.model,
            GeneratesType.service,
            GeneratesType.controller,
            GeneratesType.module,
            GeneratesType.dto,
        ]

    def commands(self) -> FrameworkCommands:
        return FrameworkCommands(
            install="npm install -g @nestjs/cli",
            create_project="nest new {project_name} --package-manager npm --skip-git",
            generate_model="nest generate resource {model_name} --no-spec",
        )