<template>
  <v-card>
    <template v-slot:text>
      <v-text-field v-model="search" label="Search" prepend-inner-icon="mdi-magnify" single-line variant="outlined"
        hide-details />
    </template>
    <v-row>
      <v-col cols="12" sm="6">
        <v-date-input class="mt-5 mx-5" label="Date input time start" v-model="startDate" variant="outlined" />
      </v-col>
      <v-col cols="12" sm="6">
        <v-date-input class="mt-5 mx-5" label="Date input time end" v-model="endDate" variant="outlined" />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-btn @click="fetchLogs" variant="tonal" class="ml-4 mb-5" color="primary">Get These Logs</v-btn>
      </v-col>
    </v-row>
    <div v-if="loading" class="text-center">
      <v-progress-circular indeterminate :size="70" :width="7" color="primary" />
    </div>
    <v-data-table v-if="logs.length" :headers="headers" :items="logs" :search="search" dense />
    <v-card v-else class="text-center pa-8">
      <v-icon size="48" color="grey-lighten-1">mdi-database-off</v-icon>
      <p class="text-h6 mt-2">No logs available</p>
      <p class="text-body-2 text-grey">Select date range and fetch logs to see results</p>
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
import { ref } from 'vue'
import axios from 'axios'
import { useMockLogs } from '@/composables/useMockData'

const url = import.meta.env.VITE_URL_FLASK_API
const startDate = ref(null)
const endDate = ref(null)
const dialog = ref(false)
const errorMessage = ref('')
const headers = [
  { key: 'user_id', title: 'User ID' },
  { key: 'action', title: 'Action' },
  { key: 'component', title: 'Component' },
  { key: 'course_name', title: 'Course Name' },
  { key: 'ip', title: 'IP Address' },
  { key: 'log_id', title: 'Log ID' },
  { key: 'quiz_id', title: 'Quiz ID' },
  { key: 'quiz_name', title: 'Quiz Name' },
  { key: 'target', title: 'Target' },
  { key: 'timecreated', title: 'Time Created' },
  { key: 'user_firstname', title: 'User Firstname' },
]
const search = ref('')
const logs = ref([])
const loading = ref(false)

async function fetchLogs() {
  if (!startDate.value || !endDate.value) {
    errorMessage.value = 'Please select both start and end dates.'
    dialog.value = true
    return
  }
  loading.value = true
  const startTime = Math.floor(new Date(startDate.value).getTime() / 1000)
  const endTime = Math.floor(new Date(endDate.value).getTime() / 1000)
  try {
    const { data } = await axios.get(`${url}/api/get/logs?start_time=${startTime}&end_time=${endTime}`)
    logs.value = data
  } catch (error) {
    logs.value = useMockLogs().value
  } finally {
    loading.value = false
  }
}
</script>
