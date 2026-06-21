<template>
  <v-card>
    <v-card-title>
      <v-btn variant="tonal" color="primary" @click="backup" class="mr-4">Backup</v-btn>
    </v-card-title>
    <v-card-text>
      <v-text-field v-model="search" label="Search" prepend-inner-icon="mdi-magnify" single-line variant="outlined"
        hide-details />
    </v-card-text>
    <div v-if="loading" class="text-center pa-4">
      <v-progress-circular indeterminate :size="70" :width="7" color="primary" />
    </div>
    <v-data-table v-if="dataFiles.length" :headers="headers" :items="dataFiles" :search="search" dense>
      <template v-slot:item.actions="{ item }">
        <v-btn variant="text" size="small" icon :to="'/dashboard/backups/' + item.title" aria-label="Download backup file">
          <v-icon>mdi-cloud-print</v-icon>
        </v-btn>
      </template>
    </v-data-table>
    <v-card v-else-if="!loading" class="text-center pa-8">
      <v-icon size="48" color="grey-lighten-1">mdi-database-off</v-icon>
      <p class="text-h6 mt-2">No backup files found</p>
      <p class="text-body-2 text-grey">Run a backup to see files here</p>
    </v-card>
    <v-dialog v-model="dialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">Notification</v-card-title>
        <v-card-text>{{ dialogMessage }}</v-card-text>
        <v-card-actions>
          <v-btn color="primary" text @click="dialog = false">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useMockBackupFiles } from '@/composables/useMockData'

const urlEndpoint = import.meta.env.VITE_URL_FLASK_API
const search = ref('')
const headers = [
  { key: 'title', title: 'Title' },
  { key: 'url', title: 'Url' },
  { key: 'actions', title: 'Actions' },
]
const dataFiles = ref([])
const loading = ref(false)
const dialog = ref(false)
const dialogMessage = ref('')

onMounted(async () => {
  try {
    const { data } = await axios.get(`${urlEndpoint}/directory`)
    dataFiles.value = data
  } catch {
    dataFiles.value = useMockBackupFiles()
  }
})

async function backup() {
  loading.value = true
  try {
    const response = await axios.post(`${urlEndpoint}/dump`)
    dialogMessage.value = response.data || 'Backup completed successfully.'
    dialog.value = true
    try {
      const { data } = await axios.get(`${urlEndpoint}/directory`)
      dataFiles.value = data
    } catch {
      dataFiles.value = useMockBackupFiles()
    }
  } catch {
    dialogMessage.value = 'Backup failed. Please try again.'
    dialog.value = true
  } finally {
    loading.value = false
  }
}
</script>
