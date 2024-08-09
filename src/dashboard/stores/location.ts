import { defineStore } from 'pinia'
import { locationService } from '~/services/locationService';
import type { LocationAndForecast } from "~/types/types"

export const useLocationStore = defineStore('location', () => {
    const locations = ref<LocationAndForecast[]>([]);

    async function fetchLocations() {
        try {
            const request = await locationService.getLocations();
            setLocations(request.data!)
        } catch (err) {
            console.error('Fetch error:', err);
        }
    }

    function setLocations(data: LocationAndForecast[]) {
        locations.value = data
    }

    function addLocation(data: LocationAndForecast) {
        locations.value = [...locations.value, data]
    }

    return { locations, setLocations, addLocation, fetchLocations }
})  