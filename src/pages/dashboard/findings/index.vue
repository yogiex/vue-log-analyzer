<!-- eslint-disable vue/valid-v-slot -->
<template>
  <DashboardLayout>
    <v-container>
      <v-card flat title="User Filter">
        <v-btn class="ml-4" variant="outlined" color="primary" @click="storeDb">Findings</v-btn>
        <v-row>
          <v-col>
            <v-date-input class="mt-5 mx-5" label="Date input time start" v-model="startDate"
              variant="outlined">
            </v-date-input>
          </v-col>
          <v-col>
            <v-date-input class="mt-5 mx-5" label="Date input time end" v-model="endDate"
              variant="outlined">
            </v-date-input>
            
          </v-col>
          
        </v-row>
        
        <!-- Progress Circular -->
        <div v-if="loading" class="text-center">
          <v-progress-circular indeterminate :size="70" :width="7" color="primary"></v-progress-circular>
        </div>
        <!-- end of progress circular -->
        <template v-slot:text>
          <v-text-field v-model="search" label="Search" prepend-inner-icon="mdi-magnify" single-line variant="outlined"
            hide-details></v-text-field>
        </template>


        <v-data-table :headers="headers" :items="kasusPeserta" :search="search">
          <template v-slot:item.status="{ item }">
            <div class="">
              <v-chip :color="kasusPeserta.status == 1 ? 'red' : 'green'"
                :text="kasusPeserta.status == 1 ? 'Dishonest' : 'Honest'" class="text-uppercase" label
                size="small"></v-chip>
            </div>
          </template>
          <template v-slot:item.action="{ item }">
            <a :href="'/dashboard/findings/' + item.userid">
              <v-icon class="me-2" size="small">
                mdi-cloud-print
              </v-icon>
              Download
            </a>
          </template>
        </v-data-table>
        <!-- Error Dialog -->
        <v-dialog v-model="dialog" width="auto">
          <v-card max-width="400">
            <v-card-title class="text-h6">Error</v-card-title>
            <v-card-text>{{ errorMessage }}</v-card-text>
            <v-card-actions>
              <v-btn class="ms-auto" text @click="dialog = false">Ok</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <!-- end of Dialog -->
      </v-card>
    </v-container>
  </DashboardLayout>
</template>

<script>

import DashboardLayout from '@/layouts/dashboard/dashboardLayout.vue';

import axios from 'axios';

let url = `${import.meta.env.VITE_URL_FLASK_API}`
export default {
  components: { DashboardLayout },
  data() {
    return {
      search: '',
      headers: [
        { key: 'userid', title: 'User ID' },
        {
          align: 'start',
          key: 'firstname',
          sortable: false,
          title: 'Username',
        },
        { key: 'lastname', title: 'Full Name' },
        { key: 'timestart', title: 'Time Start' },
        { key: 'timefinish', title: 'Time Finished' },
        { key: 'timedate', title: 'Time Date' },
        { key: 'time_taken', title: 'Durasi Pengerjaan' },
        { key: 'score', title: 'Nilai' },
        { key: 'status', title: 'Status' },
        {
          key: 'action',
          title: 'Actions'
        }
      ],
      kasusPeserta: [],
      loading: false,
      startDate: null,
      endDate: null,
      dialog: false,
      errorMessage: ''
    }
  },
  mounted() {


  },
  async beforeMount() {
    try {
      const response = await axios.get(`${url}/api/daftar_peserta`)
      this.kasusPeserta = response.data
      console.log(response.data)
    } catch (error) {

    }
  },
  methods: {
    printToDoc(id) {
      alert(id)
    },
    async storeDb() {
      
      if (this.startDate && this.endDate) {
        
        const startTime = Math.floor(new Date(this.startDate).getTime() / 1000);
        const endTime = Math.floor(new Date().getTime() / 1000);
        try {
          const response = await axios.post(`${url}/api/sync-attempts?start_time=${startTime}&end_time=${endTime}`)
          console.log(response.data)
          this.loading = true
        } catch (error) {
          console.error("Error fetching logs:", error);
          this.dialog = true; // Show the dialog
          if (error.response) {
            this.errorMessage = error.response.data.message || "Server error occurred.";
          } else if (error.request) {
            this.errorMessage = "No response received from the server.";
          } else {
            this.errorMessage = error.message || "An error occurred.";
          }
        } finally {
          this.loading = false
        }
      } else {
        console.warn("Please select both start and end dates.");
        this.errorMessage = "Please select both start and end dates.";
        this.dialog = true; // Open the dialog
      }
    }
  }
}
</script>
