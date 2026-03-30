<template>
  <div class="card hover:shadow-md transition-shadow cursor-pointer" @click="$router.push(`/trips/${trip.id}`)">
    <div class="flex justify-between items-start mb-3">
      <div>
        <h3 class="font-semibold text-lg text-gray-900">{{ trip.title }}</h3>
        <p class="text-primary-600 font-medium">📍 {{ trip.destination }}</p>
      </div>
      <span class="text-xs bg-primary-100 text-primary-700 px-2 py-1 rounded-full font-medium">
        {{ trip.type }}
      </span>
    </div>

    <div class="flex items-center gap-2 text-sm text-gray-500 mb-2 flex-wrap">
      <span>📅 {{ formatDate(trip.startDate) }}</span>
      <span v-if="trip.arrivalTime" class="text-blue-500">✈️ {{ trip.arrivalTime }}</span>
      <span>→</span>
      <span>{{ formatDate(trip.endDate) }}</span>
      <span v-if="trip.departureTime" class="text-blue-500">✈️ {{ trip.departureTime }}</span>
    </div>

    <div class="flex justify-between items-center">
      <RatingStars :score="trip.averageRating ?? 0" readonly />
      <div class="flex gap-2">
        <router-link :to="`/trips/${trip.id}/itinerary`" class="btn-primary text-sm py-1 px-3" @click.stop>
          Ver itinerario
        </router-link>
        <button @click.stop="$emit('delete', trip.id)" class="text-red-500 hover:text-red-700 text-sm px-2">
          🗑
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Trip } from '@/types'
import RatingStars from './RatingStars.vue'

defineProps<{ trip: Trip }>()
defineEmits<{ delete: [id: number] }>()

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' })
}
</script>
