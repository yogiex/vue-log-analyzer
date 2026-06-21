<template>
  <v-app-bar flat elevation="0" color="primary">
    <v-app-bar-nav-icon @click="drawer = !drawer" aria-label="Toggle navigation sidebar" />
    <v-app-bar-title class="text-h6 font-weight-medium">
      Log Analyzer
    </v-app-bar-title>
    <v-spacer />
    <div class="text-body-2 text-white mr-4 d-none d-sm-block">
      {{ currentTime }}
    </div>
    <v-menu>
      <template #activator="{ props }">
        <v-btn icon v-bind="props" aria-label="User account menu">
          <v-icon>mdi-account-circle</v-icon>
        </v-btn>
      </template>
      <v-list density="compact">
        <v-list-subheader>{{ user.email }}</v-list-subheader>
        <v-list-item v-if="!isLoggedIn" to="/login">
          <template #prepend><v-icon>mdi-login</v-icon></template>
          <v-list-item-title>Login</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="isLoggedIn" @click="onLogout">
          <template #prepend><v-icon>mdi-logout</v-icon></template>
          <v-list-item-title>Sign Out</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script setup>
import { ref, inject, computed, onMounted, onUnmounted } from 'vue'
import { useAuth } from '@/composables/useAuth'

const { user, isLoggedIn, logout } = useAuth()

const drawer = inject('drawer')
const now = ref(new Date())

const currentTime = computed(() => {
  return now.value.toLocaleString('id-ID', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
})

let timer
onMounted(() => {
  timer = setInterval(() => {
    now.value = new Date()
  }, 1000)
})
onUnmounted(() => {
  clearInterval(timer)
})

function onLogout() {
  logout()
}
</script>
