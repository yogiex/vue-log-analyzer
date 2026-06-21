<template>
  <div>
    <h1 class="text-h4 mb-4">
      <v-icon class="me-2" color="primary">mdi-file-find</v-icon>
      Findings
    </h1>

    <v-breadcrumbs density="comfortable" divider="›" class="px-0 pt-0 pb-4" :items="[
      { title: 'Dashboard', disabled: false, href: '/dashboard' },
      { title: 'Findings', disabled: true },
    ]" />

    <v-card class="pa-4">
      <v-card-item>
        <template #prepend>
          <v-icon color="primary" aria-label="Findings">mdi-file-find</v-icon>
        </template>
        <v-card-title class="text-h6">Sync Attempts</v-card-title>
        <template #append>
          <v-text-field
            v-model="search"
            label="Search findings..."
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
          <v-col cols="12" sm="6">
            <v-date-input label="Date input time start" v-model="startDate" variant="outlined" />
          </v-col>
          <v-col cols="12" sm="6">
            <v-date-input label="Date input time end" v-model="endDate" variant="outlined" />
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" class="d-flex ga-2">
            <v-btn variant="tonal" color="primary" @click="syncAttempts" :loading="loading">
              <v-icon start>mdi-sync</v-icon>
              Sync Attempts
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>

      <v-alert
        v-if="fetchError"
        type="error"
        variant="tonal"
        class="mx-4 mb-4"
        title="Failed to load findings"
        text="Unable to connect to the backend and no mock data available. Please try again later."
        closable
        @click:close="fetchError = false"
      />

      <v-skeleton-loader
        v-if="pageLoading"
        type="table-row-divider@10"
        role="status"
        aria-label="Loading findings data"
      />

      <div v-else aria-live="polite">
        <v-data-table
          v-if="kasusPeserta.length"
          aria-label="Findings data table"
          :headers="headers"
          :items="kasusPeserta"
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
            <v-chip :color="value == 1 ? 'error' : 'success'" size="x-small" variant="tonal">
              {{ value == 1 ? 'Dishonest' : 'Honest' }}
            </v-chip>
          </template>
          <template #item.action="{ item }">
            <v-btn variant="text" size="small" :to="'/dashboard/findings/' + item.userid" aria-label="View finding details">
              <v-icon class="me-1" size="small">mdi-cloud-print</v-icon>
              Download
            </v-btn>
          </template>
        </v-data-table>

        <v-card
          v-if="!kasusPeserta.length && !fetchError"
          class="text-center pa-8"
          variant="tonal"
        >
          <v-icon size="48" color="medium-emphasis">mdi-database-off</v-icon>
          <p class="text-h6 mt-2 text-medium-emphasis">No findings available</p>
          <p class="text-body-2 text-disabled">Sync attempts to populate findings data</p>
        </v-card>
      </div>
    </v-card>

    <v-dialog v-model="dialog" width="auto">
      <v-card max-width="400">
        <v-card-title class="text-h6">Error</v-card-title>
        <v-card-text>{{ errorMessage }}</v-card-text>
        <v-card-actions>
          <v-btn variant="text" @click="dialog = false">Ok</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useMockFindings } from '@/composables/useMockData'

const url = import.meta.env.VITE_URL_FLASK_API
const search = ref('')
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
  { key: 'action', title: 'Actions', sortable: false },
]
const kasusPeserta = ref([])
const loading = ref(false)
const pageLoading = ref(true)
const fetchError = ref(false)
const startDate = ref(null)
const endDate = ref(null)
const dialog = ref(false)
const errorMessage = ref('')

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
    const { data } = await axios.get(`${url}/api/daftar_peserta`)
    kasusPeserta.value = data
  } catch {
    const mock = useMockFindings()
    if (mock.length) {
      kasusPeserta.value = mock
    } else {
      fetchError.value = true
    }
  } finally {
    pageLoading.value = false
  }
})

async function syncAttempts() {
  if (!startDate.value || !endDate.value) {
    errorMessage.value = 'Please select both start and end dates.'
    dialog.value = true
    return
  }
  loading.value = true
  const startTime = Math.floor(new Date(startDate.value).getTime() / 1000)
  const endTime = Math.floor(new Date(endDate.value).getTime() / 1000)
  try {
    await axios.post(`${url}/api/sync-attempts?start_time=${startTime}&end_time=${endTime}`)
  } catch (error) {
    errorMessage.value = error.response?.data?.message || error.message || 'Server error occurred.'
    dialog.value = true
  } finally {
    loading.value = false
  }
}
</script>
