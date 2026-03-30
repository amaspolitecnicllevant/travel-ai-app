<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div v-if="tripsStore.loading" class="flex justify-center py-16">
      <div class="animate-spin text-4xl">⏳</div>
    </div>

    <template v-else-if="tripsStore.currentTrip">
      <!-- Back + Actions -->
      <div class="flex items-center justify-between mb-6">
        <button @click="$router.back()" class="text-primary-600 hover:underline text-sm flex items-center gap-1">
          ← Volver
        </button>
        <router-link :to="`/trips/${trip.id}/itinerary`" class="btn-primary">
          Ver itinerario IA
        </router-link>
      </div>

      <!-- Trip header -->
      <div class="card mb-6">
        <div class="flex justify-between items-start">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">{{ trip.title }}</h1>
            <p class="text-primary-600 font-medium text-lg mt-1">📍 {{ trip.destination }}</p>
          </div>
          <span class="bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-sm font-medium">
            {{ trip.type }}
          </span>
        </div>
        <div class="flex gap-6 mt-4 text-sm text-gray-500">
          <span>📅 {{ formatDate(trip.startDate) }} → {{ formatDate(trip.endDate) }}</span>
          <span>🗓 {{ tripDays }} días</span>
        </div>
      </div>

      <!-- Ratings section -->
      <div class="card mb-6">
        <h2 class="font-semibold text-gray-900 mb-4">Valoraciones</h2>

        <div v-if="tripsStore.ratings.length > 0" class="space-y-3 mb-4">
          <div v-for="r in tripsStore.ratings" :key="r.id" class="flex items-center gap-3">
            <RatingStars :score="r.score" readonly />
            <span v-if="r.comment" class="text-sm text-gray-600">{{ r.comment }}</span>
          </div>
        </div>
        <p v-else class="text-gray-500 text-sm mb-4">Sin valoraciones aún.</p>

        <!-- Add rating -->
        <div class="border-t border-gray-100 pt-4">
          <p class="text-sm font-medium text-gray-700 mb-2">Tu valoración:</p>
          <div class="flex items-center gap-3">
            <RatingStars v-model="myRating" />
            <input v-model="myComment" type="text" class="input-field flex-1" placeholder="Comentario (opcional)" />
            <button @click="submitRating" class="btn-primary whitespace-nowrap" :disabled="myRating === 0">
              Valorar
            </button>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useTripsStore } from '@/stores/trips'
import RatingStars from '@/components/RatingStars.vue'

const route = useRoute()
const tripsStore = useTripsStore()

const myRating = ref(0)
const myComment = ref('')

const tripId = Number(route.params.id)

const trip = computed(() => tripsStore.currentTrip!)

const tripDays = computed(() => {
  if (!trip.value) return 0
  const start = new Date(trip.value.startDate)
  const end = new Date(trip.value.endDate)
  return Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24))
})

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' })
}

async function submitRating() {
  if (myRating.value === 0) return
  await tripsStore.addRating(tripId, myRating.value, myComment.value || undefined)
  myRating.value = 0
  myComment.value = ''
}

onMounted(async () => {
  await tripsStore.fetchTrip(tripId)
  await tripsStore.fetchRatings(tripId)
})
</script>
