from enum import StrEnum

class FieldType(StrEnum):
    # comuns
    string = "string"
    integer = "integer"
    boolean = "boolean"
    text = "text"
    float = "float"
    date = "date"
    datetime = "datetime"
    
    # nestjs
    number = "number"
    uuid = "uuid"
    
    # laravel
    biginteger = "biginteger"
    timestamp = "timestamp"
    json = "json"
    decimal = "decimal"