<script setup lang="ts">
    import { locationService } from '~/services/locationService';
    import { useLocationStore } from '@/stores/location'

    const locationStore = useLocationStore()

    interface Props {
        showSidebar: bool,
        currentDays: Forecast
    }

    const emit = defineEmits(['close'])
    const props = defineProps < Props > ()

    const showSidebar = ref < boolean > (props.showSidebar);

    console.log(props.currentDays)


    watch(showSidebar, async (newVal, oldVal) => {
        if (!newVal) {
            emit("close")
        }
    })

    const ui = {
        overlay: {
            base: 'fixed inset-0 transition-opacity',
            background: 'bg-white/10 dark:bg-white/10',
        }
    }


</script>

<template>
    <USlideover v-model="showSidebar" :ui="ui">
        <div class="p-4 flex flex-col gap-2 bg-neutral-800 h-screen px-8 overflow-y-auto">
            <div>
                <div class="flex justify-between">
                    <h4 class="text-2xl font-bold">{{ currentDays.name }}</h4>
                    <UButton color="gray" variant="ghost" icon="i-heroicons-x-mark-20-solid" class="close-button"
                        size="2xs" @click="showSidebar = false" />
                </div>
                <p class="text-gray-200 mt-6">This Week</p>
            </div>
            <div class="flex flex-col gap-4">
                <div v-for="(el, index) in currentDays.dates.split(',')" :key="el">
                    <Day :date="el" :weatherCode="currentDays.weather_codes.split(',')[index]"
                        :minTemp="currentDays.min_temps.split(',')[index]"
                        :maxTemp="currentDays.max_temps.split(',')[index]" />
                </div>
            </div>
        </div>
    </USlideover>
</template>