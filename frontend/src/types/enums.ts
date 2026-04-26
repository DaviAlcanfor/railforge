export enum FrameworkType {
    Rails = "rails",
    NestJS = "nestjs",
    Laravel = "laravel"
}

export enum FieldType {
    string = "string",
    integer = "integer",
    boolean = "boolean",
    text = "text",
    float = "float",
    date = "date",
    datetime = "datetime",
    number = "number",
    uuid = "uuid",
    biginteger = "biginteger",
    timestamp = "timestamp",
    json = "json",
    decimal = "decimal"
}

export enum GeneratesType {
    model = "model", 
    migration = "migration", 
    controller = "controller", 
    routes = "routes", 
    service = "service", 
    module = "module", 
    dto = "dto"
}