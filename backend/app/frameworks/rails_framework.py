from app.frameworks.base import BaseFramework

from app.enums.commands_types import FrameworkCommands
from app.enums.field_types import FieldType
from app.enums.generates_types import GeneratesType


class RailsFramework(BaseFramework):
    NAME = "rails"
    DOCKER_IMAGE = "railforge-rails"

    def accepted_types(self) -> list[FieldType]:
        return list(FieldType)

    def generates(self) -> list[GeneratesType]:
        return [
            GeneratesType.model,
            GeneratesType.migration,
            GeneratesType.controller,
            GeneratesType.routes,
        ]

    def commands(self) -> FrameworkCommands:
        return FrameworkCommands(
            install="gem install rails --no-document",
            create_project="rails new {project_name} --api",
            generate_model="rails generate model {model_name} {fields}",
            migrate="rails db:migrate"
        )