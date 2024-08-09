import { useFetch } from "#app"

type useFetchType = typeof useFetch

export const fetch: useFetchType = (path, options = {}) => {
    const config = useRuntimeConfig()

    options.baseURL = config.public.backendURL
    return useFetch(path, options)
}