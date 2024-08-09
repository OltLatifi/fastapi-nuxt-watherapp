<script setup lang="ts">
    import { ref, onMounted } from 'vue';
    import { locationService } from '~/services/locationService';
    import type { LocationCurrent, LocationDaily } from "~/types/types";
    import { useLocationStore } from '@/stores/location';

    const locationStore = useLocationStore();

    const loading = ref < boolean > (true);
    const showSidebar = ref < boolean > (false);
    const showDeleteModal = ref < boolean > (false);
    const currentLocation = ref < LocationCurrent > ({});
    const currentDays = ref < Forecast > ({});
    const days = ref < Array < string >> ([]);

    const columns = ref([
        {
            key: 'name',
            label: 'Location'
        },
        {
            key: 'actionButton',
            label: '',
        },
    ]);

    const fetchLocations = async () => {
        loading.value = true;

        try {
            await locationStore.fetchLocations();
            loading.value = false;

            const options: Intl.DateTimeFormatOptions = {
                weekday: 'long',
            };

            days.value = locationStore.locations[0]?.forecast.dates.split(",").map(el => {
                const date = new Date(el);
                return date.toLocaleDateString('en-US', options);
            });


            columns.value = [
                {
                    key: 'name',
                    label: 'Location'
                },
                ...days.value.map(dateString => ({
                    key: dateString,
                    label: dateString
                })),
                {
                    key: 'actionButton',
                    label: '',
                }
            ];
        } catch (error) {
            console.error('Error fetching locations:', error);
            loading.value = false;
        }
    };

    const getMinTemp = (row, day) => {
        const index = days.value.indexOf(day);
        return index !== -1 ? row.forecast.min_temps.split(",")[index] : 'N/A';
    };

    const getMaxTemp = (row, day) => {
        const index = days.value.indexOf(day);
        return index !== -1 ? row.forecast.max_temps.split(",")[index] : 'N/A';
    };

    const getWeatherCode = (row, day) => {
        const index = days.value.indexOf(day);
        return index !== -1 ? row.forecast.weather_codes.split(",")[index] : 999;
    };

    onMounted(() => {
        fetchLocations();
    });

    const tableUI = {
        wrapper: 'rounded-md',
        divide: 'divide-y-1 divide-x-0',
        base: 'max-h-[800px] overflow-y-auto',
        thead: 'bg-neutral-700',
        tbody: 'bg-neutral-800 divide-y divide-neutral-500 dark:divide-neutral-500',
    };

    const getForecast = async (id) => {
        try {
            const request = await locationService.getForecast(id);
            currentDays.value = request;
            showSidebar.value = true;
        } catch (err) {
            console.error('Fetch error:', err);
        }
    };
</script>


<template>
    <UTable :ui="tableUI" :loading="loading" :columns="columns" :rows="locationStore.locations">
        <!-- Location column slot -->
        <template #name-data="{ row }">
            <div class="flex items-center gap-2 cursor-pointer" @click="getForecast(row.location.id)">
                <img alt="Weather Icon" :src="loadWeatherIcon(getWeatherCode(row, days[0]))" />
                <span class="location-name">{{ row.location.name }}</span>
            </div>
        </template>

        <!-- Dynamic columns for days -->
        <template v-for="day in days" :key="day" v-slot:[`${day}-data`]="{ row }">
            <p class="py-1">Min: <span class="text-neutral-200">{{ getMinTemp(row, day) }} °C</span></p>
            <p class="py-1">Max: <span class="text-neutral-200">{{ getMaxTemp(row, day) }} °C</span></p>
        </template>

        <!-- Action Button column slot -->
        <template #actionButton-data="{ row }">
            <div class="flex justify-end items-center">
                <button @click="showDeleteModal = true; currentLocation = row;">
                    <UIcon name="i-heroicons-trash" class="w-5 h-5" />
                </button>
            </div>
        </template>
    </UTable>

    <DeleteModal v-if="showDeleteModal" :showModal="showDeleteModal" :currentLocation="currentLocation"
        @close="showDeleteModal=false" />

    <Sidebar v-if="showSidebar" :showSidebar="showSidebar" :currentDays="currentDays" @close="showSidebar=false" />
</template>