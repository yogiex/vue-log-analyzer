<template>
  <div>
    <v-row>
      <v-col>
        <v-btn
          v-for="s in sessions"
          :key="s.key"
          :variant="activeSession === s.key ? 'tonal' : 'outlined'"
          :color="activeSession === s.key ? 'primary' : 'default'"
          class="ma-2"
          @click="activeSession = s.key"
          aria-label="Filter by {{ s.label }}"
        >
          {{ s.label }}
        </v-btn>
      </v-col>
    </v-row>

    <v-alert
      v-if="error"
      type="error"
      variant="tonal"
      class="mb-4"
      title="Failed to load users"
      text="Unable to load monitoring data."
      closable
      @click:close="error = false"
    />

    <v-skeleton-loader
      v-if="loading"
      type="card@6"
      role="status"
      aria-label="Loading monitoring users"
    />

    <div v-else aria-live="polite" class="d-flex align-content-start flex-wrap">
      <v-card
        v-for="(user, i) in filteredUsers"
        :key="i"
        class="ma-3"
        :elevation="5"
        min-width="200"
        :aria-label="`User card: ${user.nama}`"
      >
        <v-card-item>
          <template #prepend>
            <v-icon :color="user.status === 'bad' ? 'error' : 'success'" aria-hidden="true">
              {{ user.status === 'bad' ? 'mdi-alert-circle' : 'mdi-check-circle' }}
            </v-icon>
          </template>
          <v-card-title class="text-h6">{{ user.nama }}</v-card-title>
        </v-card-item>
        <v-img
          :src="user.img"
          width="150px"
          height="150px"
          class="mx-auto"
          :aria-label="`Avatar of ${user.nama}`"
        >
          <template #placeholder>
            <v-icon size="48" color="medium-emphasis">mdi-account</v-icon>
          </template>
        </v-img>
        <v-card-text class="text-center">
          <v-tooltip :text="user.reason" location="bottom">
            <template #activator="{ props }">
              <v-chip
                v-bind="props"
                :color="user.status === 'bad' ? 'error' : 'success'"
                size="small"
                variant="tonal"
              >
                {{ user.status }}
              </v-chip>
            </template>
          </v-tooltip>
          <p class="text-body-2 text-medium-emphasis mt-2">{{ user.ip_address }}</p>
          <p class="text-caption text-disabled mt-1">{{ user.reason }}</p>
        </v-card-text>
        <v-card-actions class="justify-center">
          <v-btn variant="text" size="small" prepend-icon="mdi-open-in-new" aria-label="View details for {{ user.nama }}">
            Details
          </v-btn>
        </v-card-actions>
      </v-card>

      <v-card
        v-if="!filteredUsers.length && !loading && !error"
        class="text-center pa-8 ma-3 w-100"
        variant="tonal"
      >
        <v-icon size="48" color="medium-emphasis">mdi-account-off</v-icon>
        <p class="text-h6 mt-2 text-medium-emphasis">No users found</p>
        <p class="text-body-2 text-disabled">No monitoring data available for this session</p>
      </v-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useMockMonitoringUsers } from '@/composables/useMockData'

const sessions = [
  { key: 'listening', label: 'Listening' },
  { key: 'grammar', label: 'Grammar' },
  { key: 'reading', label: 'Reading' },
]
const activeSession = ref('listening')
const users = ref([])
const loading = ref(true)
const error = ref(false)

const filteredUsers = computed(() =>
  users.value.filter(u => u.session === activeSession.value)
)

onMounted(async () => {
  try {
    users.value = useMockMonitoringUsers()
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
})
</script>
