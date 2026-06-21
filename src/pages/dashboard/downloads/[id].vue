<template>
  <div>
    <h1 class="text-h4 mb-4">
      <v-icon class="me-2" color="primary">mdi-file-download</v-icon>
      Backup Details
    </h1>

    <v-breadcrumbs density="comfortable" divider="›" class="px-0 pt-0 pb-4" :items="[
      { title: 'Dashboard', disabled: false, href: '/dashboard' },
      { title: 'Backup', disabled: false, href: '/dashboard/backups' },
      { title: 'Details', disabled: true },
    ]" />

    <v-card class="pa-4">
      <v-card-item>
        <template #prepend>
          <v-icon color="primary" aria-label="Download">mdi-file-download</v-icon>
        </template>
        <v-card-title class="text-h6">Backup Files</v-card-title>
        <template #append>
          <v-text-field
            v-model="search"
            label="Search files..."
            prepend-inner-icon="mdi-magnify"
            single-line
            variant="outlined"
            clearable
            hide-details
            density="compact"
          />
        </template>
      </v-card-item>

      <v-alert
        v-if="error"
        type="error"
        variant="tonal"
        class="mx-4 mb-4"
        title="Failed to load backup files"
        text="Unable to connect to the backend and no mock data available."
        closable
        @click:close="error = false"
      />

      <v-skeleton-loader
        v-if="loading"
        type="table-row-divider@10"
        role="status"
        aria-label="Loading backup files"
      />

      <div v-else aria-live="polite">
        <v-data-table
          v-if="dataFiles.length"
          aria-label="Backup files data table"
          :headers="headers"
          :items="dataFiles"
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
          <template #item.actions="{ item }">
            <v-btn variant="text" size="small" icon :href="item.url" target="_blank" aria-label="Download {{ item.title }}">
              <v-icon>mdi-cloud-download</v-icon>
            </v-btn>
          </template>
        </v-data-table>

        <v-card
          v-if="!dataFiles.length && !error"
          class="text-center pa-8"
          variant="tonal"
        >
          <v-icon size="48" color="medium-emphasis">mdi-database-off</v-icon>
          <p class="text-h6 mt-2 text-medium-emphasis">No backup files found</p>
          <p class="text-body-2 text-disabled">Connect to backend or check mock data source</p>
        </v-card>
      </div>
    </v-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useMockBackupFiles } from '@/composables/useMockData'

const route = useRoute()
const url = import.meta.env.VITE_URL_FLASK_API
const search = ref('')
const headers = [
  { key: 'title', title: 'Title' },
  { key: 'url', title: 'Url' },
  { key: 'actions', title: '', sortable: false },
]
const dataFiles = ref([])
const loading = ref(true)
const error = ref(false)

const customSort = (items, sortBy) => {
  return items.sort((a, b) => {
    for (const s of sortBy) {
      const key = s.key
      const desc = s.order === 'desc'
      const cmp = String(a[key] || '').localeCompare(String(b[key] || ''))
      if (cmp !== 0) return desc ? -cmp : cmp
    }
    return 0
  })
}

onMounted(async () => {
  try {
    const { data } = await axios.get(`${url}/directory/${route.params.id}`)
    dataFiles.value = data
  } catch {
    const mock = useMockBackupFiles()
    if (mock.length) {
      dataFiles.value = mock
    } else {
      error.value = true
    }
  } finally {
    loading.value = false
  }
})
</script>
