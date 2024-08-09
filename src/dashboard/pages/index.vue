<script setup lang="ts">
    import { locationService } from '~/services/locationService';
    import { useLocationStore } from "~/stores/location"

    const locationStore = useLocationStore()

    const showModal = ref < bool > (false)
    const cities = ref < City[] > ([])
    const selectedCity = ref < City | null > (null)

    const fetchCitites = async () => {
        try {
            const request = await locationService.getCities();
            cities.value = request

        } catch (err) {
            console.error('Fetch error:', err);
        }
    }

    const saveLocation = async () => {
        const locations = locationStore.locations
        const value = selectedCity.value

        if (locations && locations.some(el => el.name === value.name)) {
            showModal.value = false
            return
        }

        try {
            const body = {
                name: value.name,
                latitude: value.latitude,
                longitude: value.longitude
            }

            const request: LocationAndForecast = await locationService.createLocation(body);
            showModal.value = false
            await locationStore.addLocation(request)
        } catch (err) {
            console.error('Fetch error:', err);
        }
    }

    onMounted(() => {
        fetchCitites()
    })

    const modalUi = {
        overlay: {
            base: 'fixed inset-0 transition-opacity',
            background: 'bg-white/10 dark:bg-white/10',
        }
    }


</script>

<template>
    <div class="bg-neutral-900 w-screen h-screen px-4 md:px-32">
        <div class="max-w-7xl mx-auto">
            <Header />
            <div class="flex justify-between items-center mt-12 mb-8">
                <h2 class="font-bold text-3xl">Locations</h2>
                <UButton @click="showModal=true" icon="i-heroicons-plus-small-solid" color="black" variant="solid"
                    class="px-4 py-2">
                    Add Location
                </UButton>
            </div>
            <Table />
            <UModal v-model="showModal" :ui="modalUi">
                <div class="p-4 flex flex-col gap-4">
                    <p class="text-xl font-semibold">Add Location</p>
                    <UInputMenu :ui="inputUI" v-model="selectedCity" :options="cities" placeholder="Select a city"
                        by="id" option-attribute="name" :search-attributes="['name', 'country']"
                        icon="i-heroicons-magnifying-glass-20-solid">
                    </UInputMenu>
                    <UButton :disabled="!selectedCity" @click="saveLocation" color="black" variant="solid"
                        class="px-4 py-2 justify-center">
                        Add Location
                    </UButton>
                </div>
            </UModal>

        </div>
    </div>
</template>

<style>
    /* Doing weird and risky stuff to customize the components */
    .w-full {
        width: 100%;
        position: relative !important;
        transform: unset !important;
    }

    ul {
        margin-top: 0.5rem !important;
    }
</style>