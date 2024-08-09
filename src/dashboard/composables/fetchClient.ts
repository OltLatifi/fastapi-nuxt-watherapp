import { useRuntimeConfig } from '#app';

export const fetchClient = async (path: string, options = {}) => {
    const config = useRuntimeConfig();

    const defaultOptions = {
        baseURL: config.public.backendURL,
        ...options,
    };

    return $fetch(path, defaultOptions);
};
