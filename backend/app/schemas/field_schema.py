from enum import Enum

class FieldType(str, Enum):
    string = "string"
    integer = "integer"
    boolean = "boolean"
    text = "text"
    float = "float"
    date = "date"
    datetime = "datetime"

