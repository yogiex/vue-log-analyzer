<template>
    
    <v-layout class="rounded rounded-md" style="min-height: 100vh;">
        <!-- <dashboardLayout>
            <v-layout>
                <h1>tes</h1>
            </v-layout>
        </dashboardLayout> -->
        <NavbarLayout/>
        <SidebarLayout/>
        <v-main>
            <div>
                <v-sheet
                class="d-flex"
                height="54"
                tile
                >
                <v-select
                    v-model="type"
                    :items="types"
                    class="ma-2"
                    label="View Mode"
                    variant="outlined"
                    dense
                    hide-details
                ></v-select>
                <v-select
                    v-model="weekday"
                    :items="weekdays"
                    class="ma-2"
                    label="weekdays"
                    variant="outlined"
                    dense
                    hide-details
                ></v-select>
                </v-sheet>
                <v-sheet>
                <v-calendar
                    ref="calendar"
                    v-model="value"
                    :events="events"
                    :view-mode="type"
                    :weekdays="weekday"
                ></v-calendar>
                </v-sheet>
            </div>
        </v-main>

        
    </v-layout>
</template>

<script>
import DashboardLayout from '@/layouts/dashboard/dashboardLayout.vue'
import NavbarLayout from '@/layouts/dashboard/navbarLayout.vue';
import SidebarLayout from '@/layouts/dashboard/sidebarLayout.vue';
import axios from 'axios';
import { VCalendar } from 'vuetify/labs/VCalendar'
export default {
    components: {DashboardLayout, NavbarLayout, SidebarLayout,VCalendar},
    data: () => ({
         type: 'month',
      types: ['month', 'week', 'day'],
      weekday: [0, 1, 2, 3, 4, 5, 6],
      weekdays: [
        { title: 'Sun - Sat', value: [0, 1, 2, 3, 4, 5, 6] },
        { title: 'Mon - Sun', value: [1, 2, 3, 4, 5, 6, 0] },
        { title: 'Mon - Fri', value: [1, 2, 3, 4, 5] },
        { title: 'Mon, Wed, Fri', value: [1, 3, 5] },
      ],
      value: [new Date()],
      events: [],
      colors: ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1'],
      titles: ['Meeting', 'Holiday', 'PTO', 'Travel', 'Event', 'Birthday', 'Conference', 'Party'],
    }),
    
}
</script>