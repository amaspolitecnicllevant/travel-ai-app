<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Mis viajes</h1>
        <p class="text-gray-500 text-sm mt-1">Gestiona y planifica tus aventuras</p>
      </div>
      <button @click="showCreateModal = true" class="btn-primary flex items-center gap-2">
        <span class="text-lg">+</span> Nuevo viaje
      </button>
    </div>

    <!-- Loading -->
    <div v-if="tripsStore.loading" class="flex justify-center py-16">
      <div class="animate-spin text-4xl">⏳</div>
    </div>

    <!-- Empty state -->
    <div v-else-if="tripsStore.trips.length === 0" class="text-center py-16">
      <div class="text-6xl mb-4">🗺️</div>
      <h2 class="text-xl font-semibold text-gray-700 mb-2">Aún no tienes viajes</h2>
      <p class="text-gray-500 mb-6">Crea tu primer viaje y deja que la IA genere un itinerario</p>
      <button @click="showCreateModal = true" class="btn-primary">Crear mi primer viaje</button>
    </div>

    <!-- Trip grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <TripCard
        v-for="trip in tripsStore.trips"
        :key="trip.id"
        :trip="trip"
        @delete="handleDelete"
      />
    </div>

    <!-- Create Trip Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md p-6">
        <h2 class="text-xl font-bold mb-5">Nuevo viaje</h2>

        <form @submit.prevent="handleCreate" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Título</label>
            <input v-model="newTrip.title" type="text" class="input-field" placeholder="Vacaciones en París" required />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Destino</label>
            <input v-model="newTrip.destination" type="text" class="input-field" placeholder="París, Francia" required />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de viaje</label>
            <select v-model="newTrip.type" class="input-field">
              <option value="familiar">Familiar</option>
              <option value="romantico">Romántico</option>
              <option value="aventura">Aventura</option>
              <option value="cultural">Cultural</option>
              <option value="negocios">Negocios</option>
              <option value="mochilero">Mochilero</option>
            </select>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Inicio</label>
              <input v-model="newTrip.startDate" type="date" class="input-field" required />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Fin</label>
              <input v-model="newTrip.endDate" type="date" class="input-field" required />
            </div>
          </div>

          <div v-if="createError" class="text-red-600 text-sm bg-red-50 rounded-lg px-3 py-2">
            {{ createError }}
          </div>

          <div class="flex gap-3 pt-2">
            <button type="button" @click="showCreateModal = false" class="btn-secondary flex-1">Cancelar</button>
            <button type="submit" class="btn-primary flex-1" :disabled="creating">
              {{ creating ? 'Creando...' : 'Crear viaje' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useTripsStore } from '@/stores/trips'
import TripCard from '@/components/TripCard.vue'

const tripsStore = useTripsStore()
const showCreateModal = ref(false)
const creating = ref(false)
const createError = ref('')

const newTrip = reactive({
  title: '',
  destination: '',
  type: 'familiar',
  startDate: '',
  endDate: ''
})

onMounted(() => tripsStore.fetchTrips())

async function handleCreate() {
  creating.value = true
  createError.value = ''
  try {
    await tripsStore.createTrip({ ...newTrip })
    showCreateModal.value = false
    Object.assign(newTrip, { title: '', destination: '', type: 'familiar', startDate: '', endDate: '' })
  } catch {
    createError.value = 'Error al crear el viaje. Inténtalo de nuevo.'
  } finally {
    creating.value = false
  }
}

async function handleDelete(id: number) {
  if (confirm('¿Eliminar este viaje?')) {
    await tripsStore.deleteTrip(id)
  }
}
</script>
