<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <button @click="$router.back()" class="text-primary-600 hover:underline text-sm flex items-center gap-1 mb-1">
          ← Volver al viaje
        </button>
        <h1 class="text-2xl font-bold text-gray-900">Itinerario IA</h1>
      </div>
      <button
        v-if="!itineraryStore.itinerary"
        @click="handleGenerate"
        class="btn-primary flex items-center gap-2"
        :disabled="itineraryStore.loading"
      >
        <span>✨</span> {{ itineraryStore.loading ? 'Generando...' : 'Generar itinerario' }}
      </button>
    </div>

    <!-- Loading -->
    <div v-if="itineraryStore.loading" class="text-center py-16">
      <div class="text-5xl mb-4 animate-bounce">🤖</div>
      <p class="text-gray-600 font-medium">La IA está creando tu itinerario...</p>
      <p class="text-gray-400 text-sm mt-2">Esto puede tardar unos segundos</p>
    </div>

    <!-- No itinerary yet -->
    <div v-else-if="!itineraryStore.itinerary" class="text-center py-16">
      <div class="text-6xl mb-4">🗺️</div>
      <h2 class="text-xl font-semibold text-gray-700 mb-2">Sin itinerario</h2>
      <p class="text-gray-500 mb-6">Genera un itinerario con IA basado en tu destino y fechas</p>
    </div>

    <template v-else>
      <!-- Budget summary -->
      <div v-if="itineraryStore.itinerary.totalBudget" class="card mb-6 flex items-center gap-3">
        <span class="text-2xl">💰</span>
        <div>
          <p class="text-sm text-gray-500">Presupuesto estimado</p>
          <p class="font-bold text-lg text-gray-900">
            {{ itineraryStore.itinerary.totalBudget }}{{ itineraryStore.itinerary.currency ?? '€' }}
          </p>
        </div>
      </div>

      <!-- AI Edit prompt -->
      <div class="card mb-6">
        <h2 class="font-semibold text-gray-900 mb-3">Editar con IA</h2>
        <div class="flex gap-3">
          <input
            v-model="editPrompt"
            type="text"
            class="input-field flex-1"
            placeholder='Ej: "Hacer el día 2 más relajado" o "Añadir más gastronomía"'
            @keyup.enter="handleEdit"
          />
          <button
            @click="handleEdit"
            class="btn-primary whitespace-nowrap"
            :disabled="!editPrompt.trim() || itineraryStore.loading"
          >
            ✨ Editar
          </button>
        </div>
      </div>

      <!-- Days -->
      <div class="space-y-4">
        <ItineraryDay
          v-for="day in itineraryStore.itinerary.days"
          :key="day.day"
          :day="day"
        />
      </div>

      <!-- Regenerate -->
      <div class="mt-6 text-center">
        <button @click="handleGenerate" class="btn-secondary" :disabled="itineraryStore.loading">
          🔄 Regenerar itinerario
        </button>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useItineraryStore } from '@/stores/itinerary'
import ItineraryDay from '@/components/ItineraryDay.vue'

const route = useRoute()
const itineraryStore = useItineraryStore()
const editPrompt = ref('')
const tripId = Number(route.params.id)

onMounted(() => itineraryStore.fetchItinerary(tripId))

async function handleGenerate() {
  await itineraryStore.generateItinerary(tripId)
}

async function handleEdit() {
  if (!editPrompt.value.trim()) return
  await itineraryStore.editItinerary(tripId, editPrompt.value)
  editPrompt.value = ''
}
</script>
