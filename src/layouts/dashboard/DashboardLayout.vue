<template>
  <div>
    <NavbarLayout />
    <SidebarLayout />
    <v-main>
      <v-container fluid class="pa-6">
        <router-view />
      </v-container>
    </v-main>
  </div>
</template>

<script setup>
import { ref, provide } from 'vue'
import NavbarLayout from '@/layouts/dashboard/NavbarLayout.vue'
import SidebarLayout from '@/layouts/dashboard/SidebarLayout.vue'

const drawer = ref(true)
provide('drawer', drawer)
</script>
