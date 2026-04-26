import axios from "axios"
import { type Framework } from "../types/interfaces"
import { FrameworkType } from "../types/enums"
import type { ProjectConfig } from "../types/interfaces"
import { ENDPOINTS } from "./endpoints"

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL
})


export const getFrameworks = async (): Promise<Framework[]> => {
    const response = await api.get<Framework[]>(ENDPOINTS.frameworks.list)
    return response.data
}


export const getFramework = async (name: FrameworkType): Promise<Framework> => {
    const response = await api.get<Framework>(ENDPOINTS.frameworks.detail(name))
    return response.data
}


export const generateProject = async (config: ProjectConfig): Promise<Blob> => {
    const response = await api.post(ENDPOINTS.generate, config, {
        responseType: "blob"
    })
    return response.data
}