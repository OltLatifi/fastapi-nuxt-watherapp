<script setup lang="ts">
    import { locationService } from '~/services/locationService';
    import { useLocationStore } from '@/stores/location'

    const locationStore = useLocationStore()

    interface Props {
        showModal: bool,
        currentLocation: LocationCurrent
    }

    const emit = defineEmits(['close'])
    const props = defineProps < Props > ()

    const showDeleteModal = ref < boolean > (props.showModal);


    watch(showDeleteModal, async (newVal, oldVal) => {
        if (!newVal) {
            emit("close")
        }
    })
    const deleteLocation = async (id) => {
        try {
            const request = await locationService.deleteLocation(id);
            locationStore.setLocations(locationStore.locations?.filter(el => el.location.id !== id))
            emit("close")
        } catch (err) {
            console.error('Fetch error:', err);
        }
    }

    const ui = {
        overlay: {
            base: 'fixed inset-0 transition-opacity',
            background: 'bg-white/10 dark:bg-white/10',
        }
    }

</script>

<template>
    <UModal v-model="showDeleteModal" :ui="ui">
        <div class="p-4 flex flex-col gap-4">
            <p>Are you sure you want to delete the "{{ currentLocation.location.name }}" location?</p>
            <UButton @click="deleteLocation( currentLocation.location.id )" color="black" variant="solid"
                class="px-4 py-2 w-fit">
                Confirm
            </UButton>
        </div>
    </UModal>
</template>