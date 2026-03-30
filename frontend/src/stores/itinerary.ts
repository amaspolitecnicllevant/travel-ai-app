import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'
import type { Itinerary } from '@/types'

export const useItineraryStore = defineStore('itinerary', () => {
  const itinerary = ref<Itinerary | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchItinerary(tripId: number) {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.get<Itinerary>(`/trips/${tripId}/itinerary`)
      itinerary.value = data
    } catch (e: unknown) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  async function generateItinerary(tripId: number) {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.post<Itinerary>(`/trips/${tripId}/itinerary`, {})
      itinerary.value = data
    } catch (e: unknown) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  async function editItinerary(tripId: number, prompt: string) {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.put<Itinerary>(`/trips/${tripId}/itinerary`, { prompt })
      itinerary.value = data
    } catch (e: unknown) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  return { itinerary, loading, error, fetchItinerary, generateItinerary, editItinerary }
})
