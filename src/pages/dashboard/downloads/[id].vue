<template>
  <div>
    <h1 class="text-h4 mb-4">Data Details Backup Files</h1>
    <v-skeleton-loader v-if="loading" type="table" />
    <template v-else>
      <v-data-table v-if="dataFiles.length" :headers="headers" :items="dataFiles" :search="search">
        <template v-slot:item.actions="{ item }">
          <v-btn variant="text" size="small" icon :href="item.url" target="_blank" aria-label="Download file">
            <v-icon>mdi-cloud-print</v-icon>
          </v-btn>
        </template>
      </v-data-table>
      <v-card v-else class="text-center pa-8">
        <v-icon size="48" color="grey-lighten-1">mdi-database-off</v-icon>
        <p class="text-h6 mt-2">No backup files found</p>
        <p class="text-body-2 text-grey">Connect to backend or check mock data source</p>
      </v-card>
    </template>
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
  { key: 'actions', title: 'Actions' },
]
const dataFiles = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await axios.get(`${url}/directory/${route.params.id}`)
    dataFiles.value = data
  } catch {
    dataFiles.value = useMockBackupFiles()
  } finally {
    loading.value = false
  }
})
</script>
