<template>
    <div class="bg-stone-700 rounded-xl w-full h-fit py-3 px-5 flex justify-between">
        <div class="flex gap-2 items-center">
            <img class="w-16" alt="Weather Icon" :src="loadWeatherIcon(cardProps.weatherCode)" />
            <p class="font-semibold text-xl">{{ day }}</p>
        </div>

        <div class="flex flex-col gap-1 items-start justify-center min-w-fit w-24">
            <div class="flex gap-4 justify-between w-full">
                <p class="text-left text-stone-500">Min.</p>
                <span>{{ cardProps.minTemp }} °C</span>
            </div>
            <div class="flex gap-4 justify-between w-full">
                <p class="text-left text-stone-500">Max.</p>
                <span>{{ cardProps.maxTemp }} °C</span>
            </div>
        </div>
    </div>
</template>


<script setup lang="ts">

    interface CardProps {
        date: string;
        weatherCode: number;
        minTemp: number;
        maxTemp: number;
    }

    const cardProps = defineProps < CardProps > ()

    const options: Intl.DateTimeFormatOptions = {
        weekday: 'long'
    };

    const day = computed(() => {
        const date = new Date(cardProps.date);
        return date.toLocaleDateString('en-US', options);
    });

</script>