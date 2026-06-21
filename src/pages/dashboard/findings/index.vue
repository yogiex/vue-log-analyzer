<template>
  <v-card flat>
    <v-card-title>User Filter</v-card-title>
    <v-card-text>
      <v-text-field v-model="search" label="Search" prepend-inner-icon="mdi-magnify" single-line variant="outlined"
        hide-details class="mb-4" />
      <v-row>
        <v-col cols="12" sm="6">
          <v-date-input label="Date input time start" v-model="startDate" variant="outlined" />
        </v-col>
        <v-col cols="12" sm="6">
          <v-date-input label="Date input time end" v-model="endDate" variant="outlined" />
        </v-col>
      </v-row>
    </v-card-text>
    <div v-if="loading" class="text-center pa-4">
      <v-progress-circular indeterminate :size="70" :width="7" color="primary" />
    </div>
    <v-btn class="ml-4 mb-4" variant="outlined" color="primary" @click="syncAttempts">Findings</v-btn>
    <v-data-table v-if="kasusPeserta.length" :headers="headers" :items="kasusPeserta" :search="search">
      <template v-slot:item.status="{ item }">
        <v-chip :color="item.status == 1 ? 'error' : 'success'"
          :text="item.status == 1 ? 'Dishonest' : 'Honest'" class="text-uppercase" label size="small" />
      </template>
      <template v-slot:item.action="{ item }">
        <v-btn variant="text" size="small" :to="'/dashboard/findings/' + item.userid">
          <v-icon class="me-2" size="small">mdi-cloud-print</v-icon>
          Download
        </v-btn>
      </template>
    </v-data-table>
    <v-card v-else-if="!loading" class="text-center pa-8">
      <v-icon size="48" color="grey-lighten-1">mdi-database-off</v-icon>
      <p class="text-h6 mt-2">No findings available</p>
      <p class="text-body-2 text-grey">Sync attempts to populate findings data</p>
    </v-card>
    <v-dialog v-model="dialog" width="auto">
      <v-card max-width="400">
        <v-card-title class="text-h6">Error</v-card-title>
        <v-card-text>{{ errorMessage }}</v-card-text>
        <v-card-actions>
          <v-btn class="ms-auto" text @click="dialog = false">Ok</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useMockFindings } from '@/composables/useMockData'

const url = import.meta.env.VITE_URL_FLASK_API
const search = ref('')
const headers = [
  { key: 'userid', title: 'User ID' },
  { align: 'start', key: 'firstname', sortable: false, title: 'Username' },
  { key: 'lastname', title: 'Full Name' },
  { key: 'timestart', title: 'Time Start' },
  { key: 'timefinish', title: 'Time Finished' },
  { key: 'timedate', title: 'Time Date' },
  { key: 'time_taken', title: 'Durasi Pengerjaan' },
  { key: 'score', title: 'Nilai' },
  { key: 'status', title: 'Status' },
  { key: 'action', title: 'Actions' },
]
const kasusPeserta = ref([])
const loading = ref(false)
const startDate = ref(null)
const endDate = ref(null)
const dialog = ref(false)
const errorMessage = ref('')

onMounted(async () => {
  try {
    const { data } = await axios.get(`${url}/api/daftar_peserta`)
    kasusPeserta.value = data
  } catch {
    kasusPeserta.value = useMockFindings()
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
