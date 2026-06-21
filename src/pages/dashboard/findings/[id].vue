<template>
  <div>
    <h1 class="text-h4 mb-4">
      <v-icon class="me-2" color="primary">mdi-file-find</v-icon>
      Finding Detail
    </h1>

    <v-breadcrumbs density="comfortable" divider="›" class="px-0 pt-0 pb-4" :items="[
      { title: 'Dashboard', disabled: false, href: '/dashboard' },
      { title: 'Findings', disabled: false, href: '/dashboard/findings' },
      { title: 'Detail', disabled: true },
    ]" />

    <v-card class="pa-4">
      <v-card-item>
        <template #prepend>
          <v-icon color="primary" aria-label="Finding detail">mdi-file-find</v-icon>
        </template>
        <v-card-title class="text-h6">Report Detail</v-card-title>
        <template #append>
          <v-btn @click="exportToPdf" variant="tonal" color="primary" aria-label="Download report as PDF">
            <v-icon start>mdi-download</v-icon>
            Download
          </v-btn>
        </template>
      </v-card-item>

      <v-alert
        v-if="error"
        type="error"
        variant="tonal"
        class="mx-4 mb-4"
        title="Failed to load finding"
        text="Unable to load this finding detail. It may not exist or the data source is unavailable."
        closable
        @click:close="error = false"
      />

      <v-skeleton-loader
        v-if="loading"
        type="card, article"
        class="ma-4"
        role="status"
        aria-label="Loading finding detail"
      />

      <template v-else>
        <v-alert v-if="!datas.userid && !error" type="warning" variant="tonal" class="mx-4 mb-4">
          Data not found for this finding.
        </v-alert>

        <div v-if="datas.userid" ref="reportElement" class="pa-4" aria-live="polite">
          <v-row>
            <v-col><h1 class="text-h5">Learning Management System</h1></v-col>
            <v-col class="text-right"><h2 class="text-h6">English Proficiency Test</h2></v-col>
          </v-row>
          <p class="text-justify text-body-1 mt-4">
            Laporan ini disusun berdasarkan hasil analisis log sistem yang berasal dari Log Analyzer,
            dengan cakupan periode analisis mulai dari {{ datas.timestart }} hingga {{ datas.timefinish }}.
          </p>

          <v-table class="mt-6">
            <thead>
              <tr>
                <th class="text-uppercase text-caption font-weight-bold">Field</th>
                <th class="text-uppercase text-caption font-weight-bold">Value</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, i) in reportRows" :key="i">
                <td class="font-weight-medium">{{ row.label }}</td>
                <td>{{ row.value }}</td>
              </tr>
            </tbody>
          </v-table>
        </div>
      </template>
    </v-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import html2pdf from 'html2pdf.js'
import { useMockFindings } from '@/composables/useMockData'

const route = useRoute()
const url = import.meta.env.VITE_URL_FLASK_API
const datas = ref({})
const loading = ref(true)
const error = ref(false)
const reportElement = ref(null)

const reportRows = computed(() => {
  const d = datas.value
  if (!d.userid) return []
  return [
    { label: 'User ID', value: d.userid },
    { label: 'Firstname', value: d.firstname },
    { label: 'Lastname', value: d.lastname },
    { label: 'Timedate', value: d.timedate },
    { label: 'Timestart', value: d.timestart },
    { label: 'Time Finish', value: d.timefinish },
  ]
})

onMounted(async () => {
  try {
    const { data } = await axios.get(`${url}/api/kasus/${route.params.id}`)
    datas.value = data
  } catch {
    const findings = useMockFindings()
    const found = findings.find(f => f.userid == route.params.id)
    if (found) {
      datas.value = found
    } else {
      error.value = true
    }
  } finally {
    loading.value = false
  }
})

function exportToPdf() {
  if (!reportElement.value) return
  html2pdf(reportElement.value, {
    margin: 1,
    filename: (datas.value.timedate || 'report') + '.pdf',
  })
}
</script>
