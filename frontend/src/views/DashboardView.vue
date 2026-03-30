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
    <div v-if="showCreateModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 overflow-y-auto">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg p-6 my-4">
        <h2 class="text-xl font-bold mb-5">Nuevo viaje</h2>

        <form @submit.prevent="handleCreate" class="space-y-4">
          <!-- Title -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Título del viaje</label>
            <input v-model="newTrip.title" type="text" class="input-field" placeholder="Vacaciones en Málaga" required />
          </div>

          <!-- Destination with suggestions -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Destino</label>
            <input
              v-model="newTrip.destination"
              type="text"
              class="input-field"
              list="destinations-list"
              placeholder="Málaga, Marbella, Ronda..."
              required
            />
            <datalist id="destinations-list">
              <option v-for="d in DESTINATIONS" :key="d" :value="d" />
            </datalist>
            <p v-if="isLocalDestination" class="text-xs text-green-600 mt-1">
              ✓ Destino con base de datos local — itinerario con lugares reales
            </p>
          </div>

          <!-- Trip type -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de viaje</label>
            <select v-model="newTrip.type" class="input-field">
              <option value="familiar">Familiar 👨‍👩‍👧</option>
              <option value="romantico">Romántico 💑</option>
              <option value="aventura">Aventura 🏔️</option>
              <option value="cultural">Cultural 🏛️</option>
              <option value="mochilero">Mochilero 🎒</option>
              <option value="negocios">Negocios 💼</option>
            </select>
          </div>

          <!-- Dates -->
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Fecha de llegada</label>
              <input v-model="newTrip.startDate" type="date" class="input-field" required />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Fecha de salida</label>
              <input v-model="newTrip.endDate" type="date" class="input-field" required />
            </div>
          </div>

          <!-- Flight times -->
          <div class="bg-blue-50 border border-blue-100 rounded-xl p-4 space-y-3">
            <p class="text-sm font-semibold text-blue-800 flex items-center gap-2">
              ✈️ Horarios de vuelo
            </p>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">
                  Llegada (hora local)
                </label>
                <input
                  v-model="newTrip.arrivalTime"
                  type="time"
                  class="input-field text-sm"
                  placeholder="14:30"
                />
                <p class="text-xs text-gray-400 mt-0.5">El itinerario empieza desde esta hora</p>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">
                  Salida (hora local)
                </label>
                <input
                  v-model="newTrip.departureTime"
                  type="time"
                  class="input-field text-sm"
                  placeholder="18:00"
                />
                <p class="text-xs text-gray-400 mt-0.5">El itinerario termina antes de esta hora</p>
              </div>
            </div>
          </div>

          <div v-if="createError" class="text-red-600 text-sm bg-red-50 border border-red-200 rounded-lg px-3 py-2">
            {{ createError }}
          </div>

          <div class="flex gap-3 pt-2">
            <button type="button" @click="closeModal" class="btn-secondary flex-1">Cancelar</button>
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
import { ref, computed, onMounted, reactive } from 'vue'
import { useTripsStore } from '@/stores/trips'
import TripCard from '@/components/TripCard.vue'

const DESTINATIONS = [
  'Málaga', 'Benalmádena', 'Marbella', 'Torremolinos',
  'Fuengirola', 'Nerja', 'Ronda'
]

const LOCAL_DESTINATIONS = DESTINATIONS.map(d => d.toLowerCase())

const tripsStore = useTripsStore()
const showCreateModal = ref(false)
const creating = ref(false)
const createError = ref('')

const newTrip = reactive({
  title: '',
  destination: '',
  type: 'familiar',
  startDate: '',
  endDate: '',
  arrivalTime: '',
  departureTime: ''
})

const isLocalDestination = computed(() =>
  LOCAL_DESTINATIONS.some(d =>
    d.includes(newTrip.destination.toLowerCase()) ||
    newTrip.destination.toLowerCase().includes(d)
  ) && newTrip.destination.length > 2
)

onMounted(() => tripsStore.fetchTrips())

async function handleCreate() {
  creating.value = true
  createError.value = ''
  try {
    await tripsStore.createTrip({
      title: newTrip.title,
      destination: newTrip.destination,
      type: newTrip.type,
      startDate: newTrip.startDate,
      endDate: newTrip.endDate,
      arrivalTime: newTrip.arrivalTime || undefined,
      departureTime: newTrip.departureTime || undefined
    })
    closeModal()
  } catch {
    createError.value = 'Error al crear el viaje. Inténtalo de nuevo.'
  } finally {
    creating.value = false
  }
}

function closeModal() {
  showCreateModal.value = false
  Object.assign(newTrip, {
    title: '', destination: '', type: 'familiar',
    startDate: '', endDate: '', arrivalTime: '', departureTime: ''
  })
  createError.value = ''
}

async function handleDelete(id: number) {
  if (confirm('¿Eliminar este viaje?')) {
    await tripsStore.deleteTrip(id)
  }
}
</script>
