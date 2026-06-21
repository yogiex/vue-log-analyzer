<template>
  <v-card flat title="User Filter">
    <template v-slot:text>
      <v-text-field v-model="search" label="Search" prepend-inner-icon="mdi-magnify" single-line variant="outlined"
        hide-details />
    </template>
    <v-skeleton-loader v-if="loading" type="table" />
    <template v-else>
      <v-data-table v-if="dataPeserta.length" :headers="headers" :items="dataPeserta" :search="search" />
      <v-card v-else class="text-center pa-8">
        <v-icon size="48" color="grey-lighten-1">mdi-database-off</v-icon>
        <p class="text-h6 mt-2">No data available</p>
        <p class="text-body-2 text-grey">Connect to backend or check mock data source</p>
      </v-card>
    </template>
  </v-card>
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
  { align: 'start', key: 'firstname', sortable: false, title: 'Username' },
  { key: 'lastname', title: 'Full Name' },
  { key: 'quiz_name', title: 'Quiz Name' },
  { key: 'timestart', title: 'Time Start' },
  { key: 'timefinish', title: 'Time Finished' },
  { key: 'diff_time_minute', title: 'Durasi Pengerjaan' },
  { key: 'session', title: 'Sesi Pengerjaan' },
  { key: 'score', title: 'Nilai' },
]
const dataPeserta = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await axios.get(`${url}/api/daftar_peserta`)
    dataPeserta.value = data
  } catch {
    dataPeserta.value = useMockUsers().value
  } finally {
    loading.value = false
  }
})
</script>
