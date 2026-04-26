from app.frameworks.rails_framework import RailsFramework
from app.frameworks.nest_framework import NestFramework
from app.frameworks.laravel_framework import LaravelFramework
from app.frameworks.base import BaseFramework

FRAMEWORKS: dict[str, BaseFramework] = {
    RailsFramework.NAME: RailsFramework(),
    NestFramework.NAME: NestFramework(),
    LaravelFramework.NAME: LaravelFramework(),
}

def get_framework(name: str) -> BaseFramework:
    framework = FRAMEWORKS.get(name)
    
    if not framework:
        raise ValueError(f"Framework '{name}' not supported. Available: {list(FRAMEWORKS.keys())}")
    
    return framework