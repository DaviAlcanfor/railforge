from dataclasses import dataclass
from typing import Optional


@dataclass
class FrameworkCommands:
    install: str
    create_project: str
    generate_model: str
    migrate: Optional[str] = None