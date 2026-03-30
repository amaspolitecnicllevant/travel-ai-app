<template>
  <div class="border border-gray-200 rounded-xl overflow-hidden">
    <div class="bg-primary-600 text-white px-4 py-3 flex items-center gap-2">
      <span class="bg-white text-primary-700 rounded-full w-7 h-7 flex items-center justify-center text-sm font-bold">
        {{ day.day }}
      </span>
      <span class="font-semibold">Día {{ day.day }}</span>
      <span v-if="day.date" class="text-primary-200 text-sm ml-auto">{{ day.date }}</span>
    </div>

    <div class="divide-y divide-gray-100">
      <div
        v-for="(activity, idx) in day.activities"
        :key="idx"
        class="px-4 py-3 flex gap-4 hover:bg-gray-50"
      >
        <div class="text-sm font-medium text-primary-600 w-16 shrink-0 mt-0.5">
          {{ activity.time }}
        </div>
        <div class="flex-1">
          <div class="flex items-center gap-2 mb-1">
            <span class="font-medium text-gray-900">{{ activity.name }}</span>
            <span class="text-xs bg-gray-100 text-gray-500 px-2 py-0.5 rounded-full">
              {{ activity.type }}
            </span>
          </div>
          <p v-if="activity.description" class="text-sm text-gray-600">{{ activity.description }}</p>
          <div class="flex items-center gap-3 mt-1 flex-wrap">
            <span v-if="activity.estimatedCost" class="text-xs text-green-600">
              ~{{ activity.estimatedCost }}€
            </span>
            <span v-if="(activity as any).address" class="text-xs text-gray-400">
              📍 {{ (activity as any).address }}
            </span>
            <span v-if="(activity as any).rating" class="text-xs text-yellow-500">
              ★ {{ (activity as any).rating }}
            </span>
            <span v-if="(activity as any).openingHours" class="text-xs text-gray-400">
              🕐 {{ (activity as any).openingHours }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ItineraryDay } from '@/types'
defineProps<{ day: ItineraryDay }>()
</script>
