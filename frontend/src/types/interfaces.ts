import { FieldType, FrameworkType, GeneratesType } from "./enums"

export interface ModelField {
    name: string
    type: FieldType
}

export interface Model {
    name: string
    fields: ModelField[]
}

export interface Framework {
    name: FrameworkType
    accepted_types: FieldType[]
    generates: GeneratesType[]
}

export interface ProjectConfig {
    framework: FrameworkType
    project_name: string
    models: Model[]
}