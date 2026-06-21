<template>
  <h1 class="text-h4 mb-6">
    <v-icon class="me-2" color="primary">mdi-view-dashboard</v-icon>
    Dashboard Overview
  </h1>

  <v-row v-if="loading" class="mb-6" role="status" aria-label="Loading dashboard data">
    <v-col v-for="n in 4" :key="n" cols="12" sm="6" lg="3">
      <v-skeleton-loader type="card" />
    </v-col>
  </v-row>

  <template v-else>
    <v-alert
      v-if="!summaryData.count_total_steps && !summaryData.count_directory"
      type="info"
      variant="tonal"
      class="mb-4"
      :icon="false"
    >
      <template #prepend>
        <v-icon color="info">mdi-information-outline</v-icon>
      </template>
      <div>
        <p class="text-body-1 font-weight-medium mb-1">No dashboard data yet</p>
        <p class="text-body-2 text-medium-emphasis mb-0">
          Connect to the backend API or switch to demo mode to populate dashboard metrics.
        </p>
      </div>
    </v-alert>

    <v-row class="mb-6">
      <v-col cols="12" sm="6" lg="3">
        <v-card class="pa-4" hover>
          <v-card-item>
            <template #prepend>
              <v-icon size="40" color="primary" aria-hidden="false" aria-label="Database search">mdi-database-search</v-icon>
            </template>
            <v-card-title class="text-h6 text-medium-emphasis">Record Count Step Query</v-card-title>
            <v-card-title class="text-h3 font-weight-bold text-primary">{{ summaryData.count_total_steps }}</v-card-title>
          </v-card-item>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" lg="3">
        <v-card class="pa-4" hover>
          <v-card-item>
            <template #prepend>
              <v-icon size="40" color="secondary" aria-hidden="false" aria-label="Logs">mdi-text-box-search-outline</v-icon>
            </template>
            <v-card-title class="text-h6 text-medium-emphasis">Total Logs</v-card-title>
            <v-card-title class="text-h3 font-weight-bold text-secondary">{{ summaryData.count_directory }}</v-card-title>
          </v-card-item>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" lg="3">
        <v-card class="pa-4" hover>
          <v-card-item>
            <template #prepend>
              <v-icon size="40" color="info" aria-hidden="false" aria-label="Users">mdi-account-multiple</v-icon>
            </template>
            <v-card-title class="text-h6 text-medium-emphasis">Total Users</v-card-title>
            <v-card-title class="text-h3 font-weight-bold text-info">{{ summaryData.count_users }}</v-card-title>
          </v-card-item>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" lg="3">
        <v-card class="pa-4" hover>
          <v-card-item>
            <template #prepend>
              <v-icon size="40" color="success" aria-hidden="false" aria-label="Standard logs">mdi-chart-bell-curve</v-icon>
            </template>
            <v-card-title class="text-h6 text-medium-emphasis">Total Standard Logs</v-card-title>
            <v-card-title class="text-h3 font-weight-bold text-success">{{ summaryData.count_mdl_standard_logs }}</v-card-title>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="6">
        <doghnut />
      </v-col>
      <v-col cols="12" md="6">
        <linechart />
      </v-col>
    </v-row>
  </template>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import doghnut from '@/components/doghnut.vue'
import linechart from '@/components/linechart.vue'
import { useMockSummary } from '@/composables/useMockData'
import axios from 'axios'

const url = import.meta.env.VITE_URL_FLASK_API
const summaryData = ref({ count_total_steps: 0, count_directory: 0, count_users: 0, count_mdl_standard_logs: 0 })
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await axios.get(`${url}/api/summary`)
    summaryData.value = response.data
  } catch {
    summaryData.value = useMockSummary()
  } finally {
    loading.value = false
  }
})
</script>
