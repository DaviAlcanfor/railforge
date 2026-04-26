from enum import StrEnum


class GeneratesType(StrEnum):
    model = "model"
    migration = "migration"
    controller = "controller"
    routes = "routes"
    service = "service"
    module = "module"
    dto = "dto"