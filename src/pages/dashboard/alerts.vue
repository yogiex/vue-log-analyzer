<template>
  <v-row>
    <v-col cols="12" sm="6" md="4">
      <v-text-field v-model="label" label="Label" prepend-icon="mdi-filter" variant="outlined" />
    </v-col>
    <v-col cols="12" sm="6" md="4">
      <v-select v-model="status" label="Status" :items="['Open', 'Closed', 'On Progress']" variant="outlined" />
    </v-col>
  </v-row>
  <v-skeleton-loader v-if="loading" type="table" />
  <template v-else>
    <v-data-table v-if="dataPeserta.length" :headers="headers" :items="dataPeserta" :search="search">
      <template v-slot:item.status="{ item }">
        <div class="text-center">
          <v-chip :color="item.status == 'terindikasi' ? 'error' : 'success'"
            :text="item.status == 'terindikasi' ? 'Aman' : 'Terindikasi'" class="text-uppercase" label size="small" />
        </div>
      </template>
      <template v-slot:item.track_progress="{ item }">
        <div class="text-end">
          <v-select v-model="item.track_progress" :items="['OPEN', 'CLOSED']" variant="outlined" />
        </div>
      </template>
    </v-data-table>
    <v-card v-else class="text-center pa-8">
      <v-icon size="48" color="grey-lighten-1">mdi-database-off</v-icon>
      <p class="text-h6 mt-2">No data available</p>
      <p class="text-body-2 text-grey">Connect to backend or check mock data source</p>
    </v-card>
  </template>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useMockAlerts } from '@/composables/useMockData'

const url = import.meta.env.VITE_URL_FLASK_API
const search = ref('')
const label = ref('')
const status = ref(null)
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
  { key: 'track_progress', title: 'Progress' },
]
const dataPeserta = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await axios.get(`${url}/api/get_cases`)
    dataPeserta.value = data
  } catch {
    dataPeserta.value = useMockAlerts()
  } finally {
    loading.value = false
  }
})
</script>
