<template>
  <div>
    <h1 class="text-h4 mb-4">
      <v-icon class="me-2" color="primary">mdi-monitor-dashboard</v-icon>
      Monitoring
    </h1>

    <v-breadcrumbs density="comfortable" divider="›" class="px-0 pt-0 pb-4" :items="[
      { title: 'Dashboard', disabled: false, href: '/dashboard' },
      { title: 'Monitoring', disabled: true },
    ]" />

    <v-card class="pa-4">
      <v-card-item>
        <template #prepend>
          <v-icon color="primary" aria-label="Monitoring">mdi-monitor-dashboard</v-icon>
        </template>
        <v-card-title class="text-h6">Live Monitoring</v-card-title>
      </v-card-item>
      <v-card-text>
        <MonitoringUser />
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import MonitoringUser from '@/components/monitoringUser.vue'
</script>
