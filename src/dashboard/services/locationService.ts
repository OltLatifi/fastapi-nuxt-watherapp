import { fetch } from "~/composables/fetch"
import type { LocationCreate, LocationAndForecast } from "~/types/types"

export const locationService = {
    async getLocations() {
        const { data: locations } = await fetch<LocationAndForecast[]>("/locations/", {
            method: "GET"
        })
        return {
            data: locations.value,
        }
    },
    async getForecast(id: number) {
        const data = await fetchClient("/forecast/" + id, {
            method: "GET"
        })
        return data
    },
    async getCities() {
        const data = await fetchClient("/locations/cities", {
            method: "GET"
        })
        return data
    },
    async createLocation(body: LocationCreate) {
        console.log(body)
        const data = await fetchClient("/locations/", {
            method: "POST",
            body: body
        })
        return data
    },
    async deleteLocation(id: number) {
        const { data: message } = await fetch("/locations/" + id, {
            method: "DELETE"
        })
        return {
            data: message.value,
        }
    },
}