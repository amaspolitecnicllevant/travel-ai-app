<template>
  <div class="flex items-center gap-1">
    <button
      v-for="star in 5"
      :key="star"
      :class="[
        'text-xl transition-colors',
        star <= (hoveredStar || modelValue) ? 'text-yellow-400' : 'text-gray-300',
        readonly ? 'cursor-default' : 'cursor-pointer hover:text-yellow-400'
      ]"
      :disabled="readonly"
      @mouseenter="!readonly && (hoveredStar = star)"
      @mouseleave="!readonly && (hoveredStar = 0)"
      @click="!readonly && $emit('update:modelValue', star)"
    >
      ★
    </button>
    <span v-if="showValue && modelValue" class="text-sm text-gray-500 ml-1">
      {{ modelValue.toFixed(1) }}
    </span>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

withDefaults(defineProps<{
  modelValue?: number
  score?: number
  readonly?: boolean
  showValue?: boolean
}>(), {
  modelValue: 0,
  score: 0,
  readonly: false,
  showValue: false
})

defineEmits<{ 'update:modelValue': [value: number] }>()

const hoveredStar = ref(0)
</script>
