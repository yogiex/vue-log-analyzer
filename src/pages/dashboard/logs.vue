<template>
    <v-layout class="rounded rounded-md" style="min-height: 100vh;">
        <NavbarLayout/>
        <SidebarLayout/>
        <v-main>
            <v-container>
                <v-card>
                    <v-row>
                        <v-col><v-date-input class="mt-5 mx-5" label="Date input time start" v-model="startDate" variant="outlined"></v-date-input></v-col>
                        <v-col><v-date-input class="mt-5 mx-5" label="Date input time end" v-model="endDate" variant="outlined"></v-date-input></v-col>
                    </v-row>
                    <v-row>
                        <v-col>
                            <v-btn @click="fetchLogs" variant="tonal" class="ml-4 mb-5" color="primary">Get These Logs</v-btn>
                        </v-col>
                    </v-row>
                </v-card>
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
            </v-container>
        </v-main>
    </v-layout>
</template>

<script>

import dashboardLayout from '@/layouts/dashboard/dashboardLayout.vue';
import NavbarLayout from '@/layouts/dashboard/navbarLayout.vue';
import SidebarLayout from '@/layouts/dashboard/sidebarLayout.vue';
import axios from 'axios';
export default {
    components: { dashboardLayout, SidebarLayout, NavbarLayout },
    data() {
    return {
        startDate: null, 
        endDate: null, 
        dialog: false,
        errorMessage: "",
    };
  },
  methods: {
    async fetchLogs() {
        if (this.startDate && this.endDate) {
                
                const startTime = Math.floor(new Date(this.startDate).getTime() / 1000);
                const endTime = Math.floor(new Date(this.endDate).getTime() / 1000);

                
                const apiUrl = `${import.meta.env.VITE_URL_FLASK_API}/api/get/logs?start_time=${startTime}&end_time=${endTime}`;

                try {
                    
                    const response = await axios.get(apiUrl);
                    const logs = response.data;
                    console.log("Fetched logs:", logs);
                    
                    
                    } catch (error) {
                    // Handle errors and show modal
                    console.error("Error fetching logs:", error);
                    this.dialog = true; // Show the dialog
                    if (error.response) {
                        this.errorMessage = error.response.data.message || "Server error occurred.";
                    } else if (error.request) {
                        this.errorMessage = "No response received from the server.";
                    } else {
                        this.errorMessage = error.message || "An error occurred.";
                    }
                }
            } else {
                console.warn("Please select both start and end dates.");
                this.errorMessage = "Please select both start and end dates.";
                this.dialog = true; // Open the dialog
            }
        }
  },
}
</script>
