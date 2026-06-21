<template>
  <div>
    <h1 class="text-h4 mb-4">
      <v-icon class="me-2" color="primary">mdi-backup-restore</v-icon>
      Backup
    </h1>

    <v-breadcrumbs density="comfortable" divider="›" class="px-0 pt-0 pb-4" :items="[
      { title: 'Dashboard', disabled: false, href: '/dashboard' },
      { title: 'Backup', disabled: true },
    ]" />

    <v-card class="pa-4">
      <v-card-item>
        <template #prepend>
          <v-icon color="primary" aria-label="Backup">mdi-backup-restore</v-icon>
        </template>
        <v-card-title class="text-h6">Backup Files</v-card-title>
        <template #append>
          <v-btn variant="tonal" color="primary" @click="backup" class="mr-2" :loading="backingUp" aria-label="Run backup">
            <v-icon start>mdi-database-export</v-icon>
            Backup
          </v-btn>
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
        text="Unable to connect to the backend and no mock data available. Please try again later."
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
          density="compact"
          hover
          fixed-header
          mobile-breakpoint="sm"
          items-per-page="10"
          :items-per-page-options="[5, 10, 25, 50]"
        >
          <template #header="{ header }">
            <span class="text-uppercase text-caption font-weight-bold">{{ header.title }}</span>
          </template>
          <template #item.date="{ value }">
            {{ formatDate(value) }}
          </template>
          <template #item.actions="{ item }">
            <v-btn variant="text" size="small" icon :to="'/dashboard/backups/' + item.title" aria-label="Download backup file">
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
          <p class="text-body-2 text-disabled">Run a backup to see files here</p>
        </v-card>
      </div>
    </v-card>

    <v-dialog v-model="dialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">Notification</v-card-title>
        <v-card-text>{{ dialogMessage }}</v-card-text>
        <v-card-actions>
          <v-btn color="primary" variant="text" @click="dialog = false">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useMockBackupFiles } from '@/composables/useMockData'

const urlEndpoint = import.meta.env.VITE_URL_FLASK_API
const search = ref('')
const headers = [
  { key: 'title', title: 'Title' },
  { key: 'date', title: 'Date' },
  { key: 'size', title: 'Size' },
  { key: 'url', title: 'Url' },
  { key: 'actions', title: '', sortable: false },
]
const dataFiles = ref([])
const loading = ref(true)
const backingUp = ref(false)
const error = ref(false)
const dialog = ref(false)
const dialogMessage = ref('')

const formatDate = (val) => {
  if (!val) return '-'
  return new Date(val).toLocaleString('id-ID')
}

const customSort = (items, sortBy) => {
  return items.sort((a, b) => {
    for (const s of sortBy) {
      const key = s.key
      const desc = s.order === 'desc'
      let cmp = 0
      if (key === 'date') {
        cmp = new Date(a[key] || 0) - new Date(b[key] || 0)
      } else if (key === 'size') {
        const aVal = parseInt(a[key]) || 0
        const bVal = parseInt(b[key]) || 0
        cmp = aVal - bVal
      } else {
        cmp = String(a[key] || '').localeCompare(String(b[key] || ''))
      }
      if (cmp !== 0) return desc ? -cmp : cmp
    }
    return 0
  })
}

async function fetchFiles() {
  loading.value = true
  error.value = false
  try {
    const { data } = await axios.get(`${urlEndpoint}/directory`)
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
}

async function backup() {
  backingUp.value = true
  try {
    const response = await axios.post(`${urlEndpoint}/dump`)
    dialogMessage.value = response.data || 'Backup completed successfully.'
    dialog.value = true
    await fetchFiles()
  } catch {
    dialogMessage.value = 'Backup failed. Please try again.'
    dialog.value = true
  } finally {
    backingUp.value = false
  }
}

fetchFiles()
</script>
