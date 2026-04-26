from app.frameworks.base import BaseFramework

from app.enums.commands_types import FrameworkCommands
from app.enums.field_types import FieldType
from app.enums.generates_types import GeneratesType


class LaravelFramework(BaseFramework):
    NAME = "laravel"
    DOCKER_IMAGE = "railforge-laravel"

    def accepted_types(self) -> list[FieldType]:
        return [
            FieldType.string, 
            FieldType.integer, 
            FieldType.boolean, 
            FieldType.text, 
            FieldType.float, 
            FieldType.date, 
            FieldType.datetime, 
            FieldType.biginteger, 
            FieldType.timestamp, 
            FieldType.json, 
            FieldType.decimal,
        ]

    def generates(self) -> list[GeneratesType]:
        return [
            GeneratesType.model,
            GeneratesType.migration,
            GeneratesType.controller,
            GeneratesType.routes,
        ]

    def commands(self) -> FrameworkCommands:
        return FrameworkCommands(
            install="composer create-project laravel/laravel {project_name}",
            create_project="composer create-project laravel/laravel {project_name}",
            generate_model="php artisan make:model {model_name} --migration --controller --resource",
            migrate="php artisan migrate"
        )