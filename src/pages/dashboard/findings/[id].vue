<template>
  <v-card>
    <v-btn @click="exportToPdf" variant="outlined" color="primary" class="mt-10 ml-4">Download</v-btn>
    <v-skeleton-loader v-if="loading" type="card, article" class="ma-4" />
    <template v-else>
      <v-alert v-if="!datas.userid" type="warning" variant="tonal" class="ma-4">
        Data not found for this finding.
      </v-alert>
      <div v-else class="w-75 mx-auto my-5" id="element-to-report">
        <v-row>
          <v-col><h1 class="text-h5">Learning Management System</h1></v-col>
          <v-col><h2 class="text-h6">English Proficiency Test</h2></v-col>
        </v-row>
        <p class="text-justify">
          Laporan ini disusun berdasarkan hasil analisis log sistem yang berasal dari Log Analyzer,
          dengan cakupan periode analisis mulai dari {{ datas.timestart }} hingga {{ datas.timefinish }}.
        </p>
        <v-row class="bg-blue-lighten-3 mt-5">
          <v-col><p>User ID</p></v-col>
          <v-col><p>{{ datas.userid }}</p></v-col>
        </v-row>
        <v-row class="bg-blue-lighten-5">
          <v-col><p>Firstname</p></v-col>
          <v-col><p>{{ datas.firstname }}</p></v-col>
        </v-row>
        <v-row class="bg-blue-lighten-3">
          <v-col><p>Lastname</p></v-col>
          <v-col><p>{{ datas.lastname }}</p></v-col>
        </v-row>
        <v-row class="bg-blue-lighten-5">
          <v-col><p>Timedate</p></v-col>
          <v-col><p>{{ datas.timedate }}</p></v-col>
        </v-row>
        <v-row class="bg-blue-lighten-3">
          <v-col><p>Timestart</p></v-col>
          <v-col><p>{{ datas.timestart }}</p></v-col>
        </v-row>
        <v-row class="bg-blue-lighten-5">
          <v-col><p>Time Finish</p></v-col>
          <v-col><p>{{ datas.timefinish }}</p></v-col>
        </v-row>
      </div>
    </template>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import html2pdf from 'html2pdf.js'
import { useMockFindings } from '@/composables/useMockData'

const route = useRoute()
const url = import.meta.env.VITE_URL_FLASK_API
const datas = ref({})
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await axios.get(`${url}/api/kasus/${route.params.id}`)
    datas.value = data
  } catch {
    const findings = useMockFindings()
    datas.value = findings.find(f => f.userid == route.params.id) || {}
  } finally {
    loading.value = false
  }
})

function exportToPdf() {
  html2pdf(document.getElementById('element-to-report'), {
    margin: 1,
    filename: (datas.value.timedate || 'report') + '.pdf',
  })
}
</script>
