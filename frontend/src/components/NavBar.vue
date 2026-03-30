<template>
  <nav class="bg-white border-b border-gray-200 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <router-link to="/dashboard" class="flex items-center gap-2 text-primary-700 font-bold text-xl">
          <span class="text-2xl">✈️</span>
          Travel AI
        </router-link>

        <div class="flex items-center gap-4">
          <span class="text-sm text-gray-500">{{ authStore.user?.username }}</span>
          <button @click="handleLogout" class="btn-secondary text-sm">
            Cerrar sesión
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>
