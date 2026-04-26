export const ENDPOINTS = {
    frameworks: {
      list: "/frameworks/",
      detail: (name: string) => `/frameworks/${name}`,
    },
    generate: "/generate",
}