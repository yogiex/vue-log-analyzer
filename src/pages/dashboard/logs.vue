<template>
    <DashboardLayout>
        <v-container>
            <v-card>
                <template v-slot:text>
                    <v-text-field v-model="search" label="Search" prepend-inner-icon="mdi-magnify" single-line
                        variant="outlined" hide-details>
                    </v-text-field>
                </template>
                <v-row>
                    <v-col><v-date-input class="mt-5 mx-5" label="Date input time start" v-model="startDate"
                            variant="outlined"></v-date-input></v-col>
                    <v-col><v-date-input class="mt-5 mx-5" label="Date input time end" v-model="endDate"
                            variant="outlined"></v-date-input></v-col>
                </v-row>
                <v-row>
                    <v-col>
                        <v-btn @click="fetchLogs" variant="tonal" class="ml-4 mb-5" color="primary">Get These
                            Logs</v-btn>
                    </v-col>
                </v-row>
                <!-- Progress circular -->
                <!-- Progress Circular -->
                <div v-if="loading" class="text-center">
                    <v-progress-circular indeterminate :size="70" :width="7" color="primary"></v-progress-circular>
                </div>
                <!-- end of progress circular -->
                <!--  data tables-->
                <v-data-table :headers="headers" :items="logs" :search="search" dense>

                </v-data-table>
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
            <!-- end of Dialog -->
        </v-container>
    </DashboardLayout>

</template>

<script>

import DashboardLayout from '@/layouts/dashboard/dashboardLayout.vue';
import axios from 'axios';
export default {
    components: {  DashboardLayout },
    data() {
        return {
            startDate: null,
            endDate: null,
            dialog: false,
            errorMessage: "",
            headers: [
                { key: 'user_id', title: ' User ID' },
                { key: 'action', title: ' Action' },
                { key: 'component', title: ' Component' },
                { key: 'course_name', title: ' Course Name' },
                { key: 'ip', title: ' IP Address' },
                { key: 'log_id', title: ' Log ID' },
                { key: 'quiz_id', title: ' Quiz ID' },
                { key: 'quiz_name', title: ' Quiz Name' },
                { key: 'target', title: ' Target' },
                { key: 'timecreated', title: ' Time Created' },
                { key: 'user_firstname', title: 'User Firstname' }
            ],
            search: '',
            logs: [],
            loading: false
        };
    },
    methods: {
        async fetchLogs() {
            if (this.startDate && this.endDate) {
                this.loading = true
                const startTime = Math.floor(new Date(this.startDate).getTime() / 1000);
                const endTime = Math.floor(new Date(this.endDate).getTime() / 1000);

                const apiUrl = `${import.meta.env.VITE_URL_FLASK_API}/api/get/logs?start_time=${startTime}&end_time=${endTime}`;
                try {

                    const response = await axios.get(apiUrl);
                    this.logs = response.data;
                    console.table(response.data)
                    console.log("Fetched logs:", this.logs);


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
                } finally {
                    this.loading = false;
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
