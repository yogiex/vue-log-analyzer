<template>
  <DashboardLayout>
    <v-container>
      <v-card>
        <v-btn class="ml-3 my-3" variant="tonal" @click="backup()">
          Backup!!
        </v-btn>
        <template v-slot:text>
          <v-text-field v-model="search" label="Search" prepend-inner-icon="mdi-magnify" single-line variant="outlined"
            hide-details></v-text-field>
        </template>
        <!-- Progress Circular -->
        <div v-if="loading" class="text-center">
          <v-progress-circular indeterminate :size="70" :width="7" color="primary"></v-progress-circular>
        </div>
        <!-- end of progress circular -->
        <v-data-table :headers="headers" :items="dataFiles" :search="search" dense>
          <template v-slot:item.actions="{ item }">
            <a :href="'/dashboard/downloads/' + item.title">
              <v-icon>mdi-cloud-print</v-icon>
            </a>
          </template>
        </v-data-table>
        <!-- start of dialog modal -->
        <!-- Modal for Notifications -->
        <v-dialog v-model="dialog" max-width="400">
          <v-card>
            <v-card-title class="text-h6">Notification</v-card-title>
            <v-card-text>{{ dialogMessage }}</v-card-text>
            <v-card-actions>
              <v-btn color="primary" text @click="dialog = false">OK</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <!-- end of dialog modal -->
      </v-card>

    </v-container>
  </DashboardLayout>
</template>

<script>
import DashboardLayout from '@/layouts/dashboard/dashboardLayout.vue';

import axios from 'axios';
let urlEndpoint = import.meta.env.VITE_URL_FLASK_API
let dataFiles = []
export default {
  components: { DashboardLayout },
  methods: {
    async backup() {
      this.loading = true; // Start loading
      try {
        const response = await axios.post(`${urlEndpoint}/dump`);
        console.log(response);
        this.dialogMessage = response.data || 'Backup completed successfully.'; // Set success message
        this.dialog = true; // Show dialog

        // Fetch updated directory after backup
        try {
          const directoryResponse = await axios.get(`${urlEndpoint}/directory`);
          this.dataFiles = directoryResponse.data; // Populate the data table
          console.log('Fetched data files:', directoryResponse.data);
        } catch (directoryError) {
          console.error('Error fetching data files:', directoryError);
          this.dialogMessage = 'Backup completed, but failed to load updated data files.';
          this.dialog = true;
        }
      } catch (error) {
        console.error('Error during backup:', error);
        this.dialogMessage = 'Backup failed. Please try again.'; // Set error message
        this.dialog = true; // Show dialog
      } finally {
        this.loading = false; // Stop loading
      }
    },
  },
  data() {

    return {
      search: '',
      headers: [
        { key: 'title', title: 'Title ' },
        { key: 'url', title: 'Url' },
        { key: 'actions', title: 'Actions' },
      ],
      dataFiles: [],
      downloadLink: [],
      loading: false,
      dialog: false,
      dialogMessage: ''
    }
  },
  async mounted() {
  },
  async beforeMount() {
    const response = await axios.get(`${urlEndpoint}/directory`)
    // response
    this.dataFiles = response.data
    console.log(response.data)
    console.log(`${urlEndpoint}/directory`)


  }
}
</script>
