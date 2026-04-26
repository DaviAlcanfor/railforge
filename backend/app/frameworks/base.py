from abc import ABC, abstractmethod

from app.enums.commands_types import FrameworkCommands
from app.enums.field_types import FieldType
from app.enums.generates_types import GeneratesType



class BaseFramework(ABC):
    NAME: str
    DOCKER_IMAGE: str
    WORK_DIR: str = "/projects"

    @abstractmethod
    def accepted_types(self) -> list[FieldType]: 
        ...

    @abstractmethod
    def generates(self) -> list[GeneratesType]: 
        ...

    @abstractmethod
    def commands(self) -> FrameworkCommands: 
        ...