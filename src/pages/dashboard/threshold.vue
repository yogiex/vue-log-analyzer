<template>
  <div>
    <h1 class="text-h4 mb-4">
      <v-icon class="me-2" color="primary">mdi-tune</v-icon>
      Thresholds
    </h1>

    <v-breadcrumbs density="comfortable" divider="›" class="px-0 pt-0 pb-4" :items="[
      { title: 'Dashboard', disabled: false, href: '/dashboard' },
      { title: 'Thresholds', disabled: true },
    ]" />

    <v-card class="pa-4">
      <v-card-item>
        <template #prepend>
          <v-icon color="primary" aria-label="Thresholds">mdi-tune</v-icon>
        </template>
        <v-card-title class="text-h6">Configure Thresholds</v-card-title>
      </v-card-item>

      <v-card-text>
        <v-alert
          v-if="error"
          type="error"
          variant="tonal"
          class="mb-4"
          title="Failed to load thresholds"
          text="Unable to load threshold configuration."
          closable
          @click:close="error = false"
        />

        <v-alert
          v-if="successMessage"
          type="success"
          variant="tonal"
          class="mb-4"
          :text="successMessage"
          closable
          @click:close="successMessage = ''"
        />

        <v-skeleton-loader
          v-if="loading"
          type="card@3"
          role="status"
          aria-label="Loading thresholds"
        />

        <div v-else aria-live="polite">
          <v-row>
            <v-col v-for="(item, i) in thresholds" :key="item.key" cols="12" md="4">
              <v-card variant="tonal" class="pa-4">
                <v-card-item>
                  <v-card-title class="text-subtitle-1 font-weight-bold">{{ item.title }}</v-card-title>
                </v-card-item>
                <v-card-text>
                  <v-text-field
                    v-model="item.value"
                    variant="outlined"
                    label="Insert Threshold"
                    type="number"
                    :min="item.min"
                    :max="item.max"
                    hide-details="auto"
                    density="comfortable"
                    aria-label="Threshold value for {{ item.title }}"
                  />
                </v-card-text>
                <v-card-actions>
                  <v-btn
                    color="primary"
                    variant="tonal"
                    @click="submitThreshold(i)"
                    :disabled="!item.value"
                    aria-label="Submit {{ item.title }}"
                  >
                    Submit
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>

          <v-card
            v-if="!thresholds.length && !loading && !error"
            class="text-center pa-8 mt-4"
            variant="tonal"
          >
            <v-icon size="48" color="medium-emphasis">mdi-tune-vertical</v-icon>
            <p class="text-h6 mt-2 text-medium-emphasis">No thresholds configured</p>
            <p class="text-body-2 text-disabled">Add thresholds to see them here</p>
          </v-card>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useMockThresholds } from '@/composables/useMockData'

const STORAGE_KEY = 'vue-log-analyzer-thresholds'

const thresholds = ref([])
const loading = ref(true)
const error = ref(false)
const successMessage = ref('')

function loadThresholds() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      thresholds.value = JSON.parse(saved)
    } else {
      thresholds.value = useMockThresholds()
    }
  } catch {
    error.value = true
    thresholds.value = []
  } finally {
    loading.value = false
  }
}

function submitThreshold(index) {
  const item = thresholds.value[index]
  if (!item.value || item.value < item.min || item.value > item.max) return
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(thresholds.value))
    successMessage.value = `${item.title} saved successfully.`
  } catch {
    error.value = true
  }
}

onMounted(loadThresholds)
</script>
