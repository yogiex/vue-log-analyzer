<template>
  <div>
    <h1 class="text-h4 mb-4">
      <v-icon class="me-2" color="primary">mdi-text-box-search-outline</v-icon>
      Logs
    </h1>

    <v-breadcrumbs density="comfortable" divider="›" class="px-0 pt-0 pb-4" :items="[
      { title: 'Dashboard', disabled: false, href: '/dashboard' },
      { title: 'Logs', disabled: true },
    ]" />

    <v-card class="pa-4">
      <v-card-item>
        <template #prepend>
          <v-icon color="primary" aria-label="Logs">mdi-text-box-search-outline</v-icon>
        </template>
        <v-card-title class="text-h6">Log Filter</v-card-title>
        <template #append>
          <v-text-field
            v-model="search"
            label="Search logs..."
            prepend-inner-icon="mdi-magnify"
            single-line
            variant="outlined"
            clearable
            hide-details
            density="compact"
            :persistent-hint="searchHint"
          />
        </template>
      </v-card-item>

      <v-card-text class="pb-0">
        <v-row>
          <v-col cols="12" sm="6">
            <v-date-input label="Start date" v-model="startDate" variant="outlined" />
          </v-col>
          <v-col cols="12" sm="6">
            <v-date-input label="End date" v-model="endDate" variant="outlined" />
          </v-col>
        </v-row>

        <v-row v-if="logs.length">
          <v-col cols="12" sm="6" md="3">
            <v-select
              v-model="actionFilter"
              label="Action"
              :items="actionOptions"
              clearable
              variant="outlined"
              density="comfortable"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-select
              v-model="componentFilter"
              label="Component"
              :items="componentOptions"
              clearable
              variant="outlined"
              density="comfortable"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-select
              v-model="courseFilter"
              label="Course"
              :items="courseOptions"
              clearable
              variant="outlined"
              density="comfortable"
              hide-details
            />
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-select
              v-model="quizFilter"
              label="Quiz"
              :items="quizOptions"
              clearable
              variant="outlined"
              density="comfortable"
              hide-details
            />
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" class="d-flex ga-2">
            <v-btn @click="fetchLogs" variant="tonal" color="primary">
              <v-icon start>mdi-filter</v-icon>
              Get These Logs
            </v-btn>
            <v-btn
              v-if="hasActiveFilters"
              @click="clearFilters"
              variant="text"
              color="text-secondary"
              size="small"
            >
              Clear all filters
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>

      <v-alert
        v-if="error"
        type="error"
        variant="tonal"
        class="mx-4 mb-4"
        title="Failed to load logs"
        :text="errorMessage"
        closable
        @click:close="error = false"
      />

      <v-skeleton-loader
        v-if="loading"
        type="table-row-divider@10"
        role="status"
        aria-label="Loading logs data"
      />

      <div v-else aria-live="polite">
        <v-data-table
          v-if="logs.length"
          aria-label="Logs data table"
          :headers="headers"
          :items="filteredLogs"
          :search="search"
          :custom-key-sort="customSort"
          density="comfortable"
          hover
          fixed-header
          mobile-breakpoint="sm"
          items-per-page="10"
          :items-per-page-options="[5, 10, 25, 50, 100]"
        >
          <template #header="{ header }">
            <span class="text-uppercase text-caption font-weight-bold">{{ header.title }}</span>
          </template>
          <template #item.action="{ value }">
            <v-chip :color="chipColor(value)" size="x-small" variant="tonal">
              {{ value }}
            </v-chip>
          </template>
          <template #item.timecreated="{ value }">
            {{ value || '-' }}
          </template>
          <template #item.actions>
            <v-btn icon size="x-small" variant="text" aria-label="View log details">
              <v-icon>mdi-eye</v-icon>
            </v-btn>
          </template>
        </v-data-table>

        <v-card
          v-if="!logs.length && !loading && !error"
          class="text-center pa-8"
          variant="tonal"
        >
          <v-icon size="48" color="medium-emphasis">mdi-database-off</v-icon>
          <p class="text-h6 mt-2 text-medium-emphasis">No logs available</p>
          <p class="text-body-2 text-disabled">Select date range and fetch logs to see results</p>
        </v-card>
      </div>
    </v-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useMockLogs } from '@/composables/useMockData'

const url = import.meta.env.VITE_URL_FLASK_API
const startDate = ref(null)
const endDate = ref(null)
const search = ref('')
const logs = ref([])
const loading = ref(false)
const error = ref(false)
const errorMessage = ref('')

const actionFilter = ref(null)
const componentFilter = ref(null)
const courseFilter = ref(null)
const quizFilter = ref(null)

const headers = [
  { key: 'log_id', title: 'Log ID' },
  { key: 'user_id', title: 'User ID' },
  { key: 'action', title: 'Action' },
  { key: 'component', title: 'Component' },
  { key: 'course_name', title: 'Course Name' },
  { key: 'ip', title: 'IP' },
  { key: 'quiz_name', title: 'Quiz' },
  { key: 'timecreated', title: 'Time Created' },
  { key: 'target', title: 'Target' },
  { key: 'actions', title: '', sortable: false },
]

const uniqueValues = (key) => [...new Set(logs.value.map(l => l[key]).filter(Boolean))]
const actionOptions = computed(() => uniqueValues('action'))
const componentOptions = computed(() => uniqueValues('component'))
const courseOptions = computed(() => uniqueValues('course_name'))
const quizOptions = computed(() => uniqueValues('quiz_name'))

const filteredLogs = computed(() => {
  let result = logs.value
  if (actionFilter.value) result = result.filter(l => l.action === actionFilter.value)
  if (componentFilter.value) result = result.filter(l => l.component === componentFilter.value)
  if (courseFilter.value) result = result.filter(l => l.course_name === courseFilter.value)
  if (quizFilter.value) result = result.filter(l => l.quiz_name === quizFilter.value)
  return result
})

const hasActiveFilters = computed(() =>
  actionFilter.value || componentFilter.value || courseFilter.value || quizFilter.value
)

const searchHint = computed(() => {
  if (!search.value || !logs.value.length) return ''
  const q = search.value.toLowerCase()
  const match = filteredLogs.value.filter(l =>
    Object.values(l).some(v => String(v).toLowerCase().includes(q))
  ).length
  return `Found ${match} of ${filteredLogs.value.length} results`
})

const clearFilters = () => {
  actionFilter.value = null
  componentFilter.value = null
  courseFilter.value = null
  quizFilter.value = null
}

const chipColor = (action) => {
  const map = { created: 'success', updated: 'info', deleted: 'error', submitted: 'primary', viewed: 'default' }
  return map[action] || 'default'
}

const customSort = (items, sortBy) => {
  return items.sort((a, b) => {
    for (const s of sortBy) {
      const key = s.key
      const desc = s.order === 'desc'
      let cmp = 0
      if (key === 'timecreated') {
        cmp = new Date(a[key]) - new Date(b[key])
      } else {
        cmp = String(a[key] || '').localeCompare(String(b[key] || ''))
      }
      if (cmp !== 0) return desc ? -cmp : cmp
    }
    return 0
  })
}

async function fetchLogs() {
  if (!startDate.value || !endDate.value) {
    errorMessage.value = 'Please select both start and end dates.'
    error.value = true
    return
  }
  loading.value = true
  error.value = false
  const startTime = Math.floor(new Date(startDate.value).getTime() / 1000)
  const endTime = Math.floor(new Date(endDate.value).getTime() / 1000)
  try {
    const { data } = await axios.get(`${url}/api/get/logs?start_time=${startTime}&end_time=${endTime}`)
    logs.value = data
  } catch {
    logs.value = useMockLogs().value
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  logs.value = useMockLogs().value
})
</script>
