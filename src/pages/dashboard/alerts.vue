<template>
  <div>
    <h1 class="text-h4 mb-4">
      <v-icon class="me-2" color="primary">mdi-alert-circle-outline</v-icon>
      Alerts
    </h1>

    <v-breadcrumbs density="comfortable" divider="›" class="px-0 pt-0 pb-4" :items="[
      { title: 'Dashboard', disabled: false, href: '/dashboard' },
      { title: 'Alerts', disabled: true },
    ]" />

    <v-card class="pa-4">
      <v-card-item>
        <template #prepend>
          <v-icon color="primary" aria-label="Alerts">mdi-alert-circle-outline</v-icon>
        </template>
        <v-card-title class="text-h6">Alert Filter</v-card-title>
        <template #append>
          <v-text-field
            v-model="search"
            label="Search alerts..."
            prepend-inner-icon="mdi-magnify"
            single-line
            variant="outlined"
            clearable
            hide-details
            density="compact"
          />
        </template>
      </v-card-item>

      <v-card-text class="pb-0">
        <v-row>
          <v-col cols="12" sm="6" md="3">
            <v-text-field v-model="labelFilter" label="Label" prepend-icon="mdi-filter" variant="outlined" clearable hide-details density="comfortable" />
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-select v-model="statusFilter" label="Status" :items="statusOptions" variant="outlined" clearable hide-details density="comfortable" />
          </v-col>
        </v-row>
      </v-card-text>

      <v-alert
        v-if="error"
        type="error"
        variant="tonal"
        class="mx-4 mb-4"
        title="Failed to load alerts"
        text="Unable to connect to the backend and no mock data available. Please try again later."
        closable
        @click:close="error = false"
      />

      <v-skeleton-loader
        v-if="loading"
        type="table-row-divider@10"
        role="status"
        aria-label="Loading alerts data"
      />

      <div v-else aria-live="polite">
        <v-data-table
          v-if="filteredAlerts.length"
          aria-label="Alerts data table"
          :headers="headers"
          :items="filteredAlerts"
          :search="search"
          :custom-key-sort="customSort"
          density="comfortable"
          hover
          fixed-header
          mobile-breakpoint="sm"
          items-per-page="10"
          :items-per-page-options="[5, 10, 25, 50]"
        >
          <template #header="{ header }">
            <span class="text-uppercase text-caption font-weight-bold">{{ header.title }}</span>
          </template>
          <template #item.timestart="{ value }">
            {{ value || '-' }}
          </template>
          <template #item.timefinish="{ value }">
            {{ value || '-' }}
          </template>
          <template #item.timedate="{ value }">
            {{ value || '-' }}
          </template>
          <template #item.score="{ value }">
            <span :class="scoreClass(value)">{{ (value || 0).toLocaleString('id-ID') }}</span>
          </template>
          <template #item.status="{ value }">
            <v-chip :color="value === 'terindikasi' ? 'error' : 'success'" size="x-small" variant="tonal">
              {{ value }}
            </v-chip>
          </template>
          <template #item.track_progress="{ item }">
            <v-select v-model="item.track_progress" :items="trackOptions" variant="outlined" density="compact" hide-details />
          </template>
        </v-data-table>

        <v-card
          v-if="!filteredAlerts.length && !error"
          class="text-center pa-8"
          variant="tonal"
        >
          <v-icon size="48" color="medium-emphasis">mdi-database-off</v-icon>
          <p class="text-h6 mt-2 text-medium-emphasis">No data available</p>
          <p class="text-body-2 text-disabled">Connect to backend or check mock data source</p>
        </v-card>
      </div>
    </v-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useMockAlerts } from '@/composables/useMockData'

const url = import.meta.env.VITE_URL_FLASK_API
const search = ref('')
const labelFilter = ref('')
const statusFilter = ref(null)
const dataPeserta = ref([])
const loading = ref(true)
const error = ref(false)

const statusOptions = ['Open', 'Closed', 'On Progress']
const trackOptions = ['open', 'closed', 'on_progress']

const headers = [
  { key: 'userid', title: 'User ID' },
  { key: 'firstname', title: 'Username' },
  { key: 'lastname', title: 'Full Name' },
  { key: 'timestart', title: 'Time Start' },
  { key: 'timefinish', title: 'Time Finished' },
  { key: 'timedate', title: 'Time Date' },
  { key: 'time_taken', title: 'Duration' },
  { key: 'score', title: 'Score' },
  { key: 'status', title: 'Status' },
  { key: 'track_progress', title: 'Progress' },
]

const scoreClass = (value) => {
  if (value >= 400) return 'text-success font-weight-bold'
  if (value >= 300) return 'text-warning font-weight-bold'
  return 'text-error font-weight-bold'
}

const filteredAlerts = computed(() => {
  let result = dataPeserta.value
  if (labelFilter.value) {
    const q = labelFilter.value.toLowerCase()
    result = result.filter(a =>
      String(a.firstname).toLowerCase().includes(q) ||
      String(a.lastname).toLowerCase().includes(q)
    )
  }
  if (statusFilter.value) {
    result = result.filter(a => a.track_progress === statusFilter.value.toLowerCase())
  }
  return result
})

const customSort = (items, sortBy) => {
  return items.sort((a, b) => {
    for (const s of sortBy) {
      const key = s.key
      const desc = s.order === 'desc'
      let cmp = 0
      if (key === 'timestart' || key === 'timefinish' || key === 'timedate') {
        cmp = new Date(a[key] || 0) - new Date(b[key] || 0)
      } else if (key === 'score' || key === 'time_taken') {
        cmp = (a[key] || 0) - (b[key] || 0)
      } else {
        cmp = String(a[key] || '').localeCompare(String(b[key] || ''))
      }
      if (cmp !== 0) return desc ? -cmp : cmp
    }
    return 0
  })
}

onMounted(async () => {
  try {
    const { data } = await axios.get(`${url}/api/get_cases`)
    dataPeserta.value = data
  } catch {
    const mock = useMockAlerts()
    if (mock.length) {
      dataPeserta.value = mock
    } else {
      error.value = true
    }
  } finally {
    loading.value = false
  }
})
</script>
