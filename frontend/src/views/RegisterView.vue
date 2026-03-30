<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-600 to-primary-900 p-4">
    <div class="bg-white rounded-2xl shadow-xl w-full max-w-md p-8">
      <div class="text-center mb-8">
        <div class="text-5xl mb-3">🌍</div>
        <h1 class="text-2xl font-bold text-gray-900">Crear cuenta</h1>
        <p class="text-gray-500 text-sm mt-1">Empieza a planificar tus viajes con IA</p>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Nombre de usuario</label>
          <input v-model="username" type="text" class="input-field" placeholder="viajero123" required />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input v-model="email" type="email" class="input-field" placeholder="tu@email.com" required />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Contraseña</label>
          <input v-model="password" type="password" class="input-field" placeholder="Mínimo 8 caracteres" minlength="8" required />
        </div>

        <div v-if="errorMsg" class="text-red-600 text-sm bg-red-50 border border-red-200 rounded-lg px-3 py-2">
          {{ errorMsg }}
        </div>

        <button type="submit" class="btn-primary w-full" :disabled="loading">
          {{ loading ? 'Creando cuenta...' : 'Crear cuenta' }}
        </button>
      </form>

      <p class="text-center text-sm text-gray-500 mt-6">
        ¿Ya tienes cuenta?
        <router-link to="/login" class="text-primary-600 hover:underline font-medium">Iniciar sesión</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMsg = ref('')

async function handleRegister() {
  loading.value = true
  errorMsg.value = ''
  try {
    await authStore.register(username.value, email.value, password.value)
    router.push('/dashboard')
  } catch {
    errorMsg.value = 'Error al registrarse. El email puede estar en uso.'
  } finally {
    loading.value = false
  }
}
</script>
