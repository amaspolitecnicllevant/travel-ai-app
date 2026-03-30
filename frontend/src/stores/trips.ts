import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'
import type { Trip, Rating } from '@/types'

export const useTripsStore = defineStore('trips', () => {
  const trips = ref<Trip[]>([])
  const currentTrip = ref<Trip | null>(null)
  const ratings = ref<Rating[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchTrips() {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.get<Trip[]>('/trips')
      trips.value = data
    } catch (e: unknown) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  async function fetchTrip(id: number) {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.get<Trip>(`/trips/${id}`)
      currentTrip.value = data
    } catch (e: unknown) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  async function createTrip(trip: Omit<Trip, 'id' | 'userId' | 'averageRating'>) {
    const { data } = await api.post<Trip>('/trips', trip)
    trips.value.push(data)
    return data
  }

  async function updateTrip(id: number, updates: Partial<Trip>) {
    const { data } = await api.put<Trip>(`/trips/${id}`, updates)
    const idx = trips.value.findIndex(t => t.id === id)
    if (idx !== -1) trips.value[idx] = data
    currentTrip.value = data
    return data
  }

  async function deleteTrip(id: number) {
    await api.delete(`/trips/${id}`)
    trips.value = trips.value.filter(t => t.id !== id)
  }

  async function fetchRatings(tripId: number) {
    const { data } = await api.get<Rating[]>(`/trips/${tripId}/ratings`)
    ratings.value = data
  }

  async function addRating(tripId: number, score: number, comment?: string) {
    const { data } = await api.post<Rating>(`/trips/${tripId}/ratings`, { score, comment })
    ratings.value.push(data)
    return data
  }

  return {
    trips, currentTrip, ratings, loading, error,
    fetchTrips, fetchTrip, createTrip, updateTrip, deleteTrip,
    fetchRatings, addRating
  }
})
