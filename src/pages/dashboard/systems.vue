<template>
  <div>
    <h1 class="text-h4 mb-4">
      <v-icon class="me-2" color="primary">mdi-server</v-icon>
      Systems
    </h1>

    <v-breadcrumbs density="comfortable" divider="›" class="px-0 pt-0 pb-4" :items="[
      { title: 'Dashboard', disabled: false, href: '/dashboard' },
      { title: 'Systems', disabled: true },
    ]" />

    <v-row>
      <v-col cols="12" md="6">
        <v-card variant="tonal">
          <v-card-item>
            <template #prepend>
              <v-icon color="primary" aria-label="System info">mdi-information</v-icon>
            </template>
            <v-card-title class="text-h6">System Information</v-card-title>
          </v-card-item>
          <v-list>
            <v-list-item title="Version" subtitle="1.0.0" />
            <v-list-item title="Status" subtitle="Operational">
              <template #append>
                <v-chip color="success" size="small" variant="tonal">Active</v-chip>
              </template>
            </v-list-item>
            <v-list-item title="Last Backup" subtitle="2026-06-21 02:00 AM" />
            <v-list-item title="Uptime" subtitle="14 days 6 hours" />
          </v-list>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card variant="tonal">
          <v-card-item>
            <template #prepend>
              <v-icon color="primary" aria-label="Configuration">mdi-cog</v-icon>
            </template>
            <v-card-title class="text-h6">Configuration</v-card-title>
          </v-card-item>
          <v-list>
            <v-list-item title="Auto Sync" subtitle="Enabled">
              <template #append>
                <v-switch v-model="autoSync" hide-details density="compact" aria-label="Toggle auto sync" />
              </template>
            </v-list-item>
            <v-list-item title="Notification" subtitle="Email alerts">
              <template #append>
                <v-switch v-model="notifications" hide-details density="compact" aria-label="Toggle notifications" />
              </template>
            </v-list-item>
            <v-list-item title="Log Retention" subtitle="90 days" />
            <v-list-item title="Data Refresh" subtitle="Every 5 minutes" />
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const autoSync = ref(true)
const notifications = ref(true)
</script>
