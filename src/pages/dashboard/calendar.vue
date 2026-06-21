<template>
  <div>
    <v-sheet class="d-flex" height="54" tile>
      <v-select v-model="type" :items="types" class="ma-2" label="View Mode" variant="outlined" dense
        hide-details />
      <v-select v-model="weekday" :items="weekdays" class="ma-2" label="weekdays" variant="outlined" dense
        hide-details />
    </v-sheet>
    <v-skeleton-loader v-if="loading" type="image" height="400" />
    <template v-else>
      <v-sheet>
        <v-calendar ref="calendar" v-model="value" :events="events" :view-mode="type" :weekdays="weekday" />
      </v-sheet>
      <v-card v-if="!events.length" class="text-center pa-8 mt-4">
        <v-icon size="48" color="grey-lighten-1">mdi-calendar-blank</v-icon>
        <p class="text-h6 mt-2">No events scheduled</p>
        <p class="text-body-2 text-grey">Add events to see them on the calendar</p>
      </v-card>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { VCalendar } from 'vuetify/labs/VCalendar'
import { useMockCalendarEvents } from '@/composables/useMockData'

const type = ref('month')
const types = ['month', 'week', 'day']
const weekday = ref([0, 1, 2, 3, 4, 5, 6])
const weekdays = [
  { title: 'Sun - Sat', value: [0, 1, 2, 3, 4, 5, 6] },
  { title: 'Mon - Sun', value: [1, 2, 3, 4, 5, 6, 0] },
  { title: 'Mon - Fri', value: [1, 2, 3, 4, 5] },
  { title: 'Mon, Wed, Fri', value: [1, 3, 5] },
]
const value = ref([new Date()])
const events = ref([])
const loading = ref(true)

onMounted(() => {
  events.value = useMockCalendarEvents()
  loading.value = false
})
</script>
