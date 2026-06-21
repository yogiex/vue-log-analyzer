<template>
  <div>
    <h1 class="text-h4 mb-4">
      <v-icon class="me-2" color="primary">mdi-account-multiple</v-icon>
      Users
    </h1>

    <v-breadcrumbs density="comfortable" divider="›" class="px-0 pt-0 pb-4" :items="[
      { title: 'Dashboard', disabled: false, href: '/dashboard' },
      { title: 'Users', disabled: true },
    ]" />

    <v-card class="pa-4">
      <v-card-item>
        <template #prepend>
          <v-icon color="primary" aria-label="Users">mdi-account-multiple</v-icon>
        </template>
        <v-card-title class="text-h6">User Filter</v-card-title>
        <template #append>
          <v-text-field
            v-model="search"
            label="Search users..."
            prepend-inner-icon="mdi-magnify"
            single-line
            variant="outlined"
            hide-details
            density="compact"
          />
        </template>
      </v-card-item>

      <v-skeleton-loader
        v-if="loading"
        type="table-row-divider@10"
        role="status"
        aria-label="Loading users data"
      />

      <div v-else aria-live="polite">
        <v-data-table
          v-if="dataPeserta.length"
          aria-label="Users data table"
          :headers="headers"
          :items="dataPeserta"
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
            {{ formatDate(value) }}
          </template>
          <template #item.timefinish="{ value }">
            {{ formatDate(value) }}
          </template>
          <template #item.diff_time_minute="{ value }">
            {{ formatDuration(value) }}
          </template>
          <template #item.score="{ value }">
            <span :class="scoreClass(value)">{{ value.toLocaleString('id-ID') }}</span>
          </template>
          <template #item.status="{ value }">
            <v-chip :color="value === 'aman' ? 'success' : 'error'" size="x-small" variant="tonal">
              {{ value }}
            </v-chip>
          </template>
          <template #item.actions>
            <v-btn icon size="x-small" variant="text" aria-label="View user details">
              <v-icon>mdi-eye</v-icon>
            </v-btn>
          </template>
        </v-data-table>

        <v-alert
          v-if="error"
          type="error"
          variant="tonal"
          class="mt-4"
          title="Failed to load data"
          text="Unable to connect to the backend and no mock data available. Please try again later."
          closable
          @click:close="error = false"
        />

        <v-card
          v-if="!dataPeserta.length && !error"
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
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useMockUsers } from '@/composables/useMockData'

const url = import.meta.env.VITE_URL_FLASK_API
const search = ref('')
const headers = [
  { key: 'id', title: 'ID' },
  { key: 'attempt_id', title: 'Attempt ID' },
  { key: 'firstname', title: 'Username' },
  { key: 'lastname', title: 'Full Name' },
  { key: 'quiz_name', title: 'Quiz' },
  { key: 'status', title: 'Status' },
  { key: 'timestart', title: 'Time Start' },
  { key: 'timefinish', title: 'Time Finished' },
  { key: 'diff_time_minute', title: 'Duration' },
  { key: 'session', title: 'Session' },
  { key: 'score', title: 'Score' },
  { key: 'actions', title: '', sortable: false },
]
const dataPeserta = ref([])
const loading = ref(true)
const error = ref(false)

const formatDate = (val) => val || '-'

const formatDuration = (minutes) => {
  if (minutes == null) return '-'
  const h = Math.floor(minutes / 60)
  const m = minutes % 60
  if (h > 0) return `${h}h ${m}m`
  return `${m} min`
}

const scoreClass = (value) => {
  if (value >= 400) return 'text-success font-weight-bold'
  if (value >= 300) return 'text-warning font-weight-bold'
  return 'text-error font-weight-bold'
}

const customSort = (items, sortBy) => {
  return items.sort((a, b) => {
    for (const s of sortBy) {
      const key = s.key
      const desc = s.order === 'desc'
      let cmp = 0
      if (key === 'timestart' || key === 'timefinish') {
        cmp = new Date(a[key]) - new Date(b[key])
      } else if (key === 'score' || key === 'diff_time_minute') {
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
    const { data } = await axios.get(`${url}/api/daftar_peserta`)
    dataPeserta.value = data
  } catch {
    const mock = useMockUsers().value
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
