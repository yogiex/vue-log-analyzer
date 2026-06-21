<template>
  <div>
    <h1 class="text-h4 mb-4">
      <v-icon class="me-2" color="primary">mdi-calendar</v-icon>
      Calendar
    </h1>

    <v-breadcrumbs density="comfortable" divider="›" class="px-0 pt-0 pb-4" :items="[
      { title: 'Dashboard', disabled: false, href: '/dashboard' },
      { title: 'Calendar', disabled: true },
    ]" />

    <v-card class="pa-4">
      <v-card-item>
        <template #prepend>
          <v-icon color="primary" aria-label="Calendar">mdi-calendar</v-icon>
        </template>
        <v-card-title class="text-h6">Event Calendar</v-card-title>
      </v-card-item>

      <v-card-text>
        <v-sheet class="d-flex flex-wrap ga-2 mb-4" rounded="0">
          <v-select
            v-model="type"
            :items="types"
            label="View Mode"
            variant="outlined"
            density="compact"
            hide-details
            class="flex-shrink-0"
            style="min-width: 140px"
            aria-label="Calendar view mode"
          />
          <v-select
            v-model="weekday"
            :items="weekdays"
            label="Weekdays"
            variant="outlined"
            density="compact"
            hide-details
            class="flex-shrink-0"
            style="min-width: 160px"
            aria-label="Weekday display mode"
          />
        </v-sheet>

        <v-alert
          v-if="error"
          type="error"
          variant="tonal"
          class="mb-4"
          title="Failed to load events"
          text="Unable to load calendar events. Please try again later."
          closable
          @click:close="error = false"
        />

        <v-skeleton-loader
          v-if="loading"
          type="image"
          height="400"
          role="status"
          aria-label="Loading calendar"
        />

        <div v-else aria-live="polite">
          <v-sheet>
            <v-calendar ref="calendar" v-model="value" :events="events" :view-mode="type" :weekdays="weekday" />
          </v-sheet>

          <v-card
            v-if="!events.length"
            class="text-center pa-8 mt-4"
            variant="tonal"
          >
            <v-icon size="48" color="medium-emphasis">mdi-calendar-blank</v-icon>
            <p class="text-h6 mt-2 text-medium-emphasis">No events scheduled</p>
            <p class="text-body-2 text-disabled">Add events to see them on the calendar</p>
          </v-card>
        </div>
      </v-card-text>
    </v-card>
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
const error = ref(false)

onMounted(() => {
  try {
    events.value = useMockCalendarEvents()
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
})
</script>
