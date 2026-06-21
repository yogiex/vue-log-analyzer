<template>
  <v-main>
    <v-row no-gutters class="fill-height" style="height: 100vh">
      <v-col cols="12" md="6" class="d-flex flex-column align-center justify-center pa-8 left-panel">
      <div class="text-center">
        <v-icon size="64" color="white" class="mb-4">mdi-chart-box-outline</v-icon>

        <h1 class="text-h3 font-weight-bold text-white mb-2">Vue Log Analyzer</h1>
        <p class="text-h6 text-medium-emphasis text-white mb-6">
          LMS Log Analysis & Cheating Detection
        </p>

        <v-divider class="my-6 mx-auto" color="white" opacity="0.3" style="max-width: 240px;" />

        <v-list class="bg-transparent text-left mx-auto" style="max-width: 340px;">
          <v-list-item prepend-icon="mdi-monitor-dashboard" class="text-white mb-2" density="comfortable">
            <template v-slot:title>
              <span class="text-body-1">Real-time User Monitoring</span>
            </template>
            <template v-slot:subtitle>
              <span class="text-caption text-white text-medium-emphasis">Track active sessions and user behavior</span>
            </template>
          </v-list-item>

          <v-list-item prepend-icon="mdi-magnify-expand" class="text-white mb-2" density="comfortable">
            <template v-slot:title>
              <span class="text-body-1">Cheating Detection</span>
            </template>
            <template v-slot:subtitle>
              <span class="text-caption text-white text-medium-emphasis">Identify suspicious patterns and anomalies</span>
            </template>
          </v-list-item>

          <v-list-item prepend-icon="mdi-chart-timeline-variant" class="text-white" density="comfortable">
            <template v-slot:title>
              <span class="text-body-1">Advanced Analytics</span>
            </template>
            <template v-slot:subtitle>
              <span class="text-caption text-white text-medium-emphasis">Comprehensive reporting and data visualization</span>
            </template>
          </v-list-item>
        </v-list>
      </div>

      <div class="mt-auto text-caption text-white text-medium-emphasis pb-4">
        &copy; 2026 Vue Log Analyzer
      </div>
    </v-col>

    <v-col cols="12" md="6" class="d-flex flex-column align-center justify-center pa-8 bg-surface">
      <div style="max-width: 420px; width: 100%;">
        <h2 class="text-h4 font-weight-bold mb-1">Welcome Back</h2>
        <p class="text-body-1 text-medium-emphasis mb-6">
          Sign in to your account to continue
        </p>

        <v-form ref="formRef" @submit.prevent="onSubmit" fast-fail>
          <v-text-field
            v-model="email"
            label="Email"
            placeholder="Enter your email"
            prepend-inner-icon="mdi-email-outline"
            :rules="emailRules"
            autocomplete="email"
            class="mb-4"
          />

          <v-text-field
            v-model="password"
            label="Password"
            placeholder="Enter your password"
            prepend-inner-icon="mdi-lock-outline"
            :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
            :type="showPassword ? 'text' : 'password'"
            :rules="passwordRules"
            autocomplete="current-password"
            class="mb-4"
            @click:append-inner="showPassword = !showPassword"
          />

          <v-checkbox
            v-model="remember"
            label="Remember me"
            density="comfortable"
            hide-details
            class="mb-4"
          />

          <v-alert
            v-if="error"
            type="error"
            variant="tonal"
            closable
            class="mb-4"
            @click:close="error = ''"
          >
            {{ error }}
          </v-alert>

          <v-btn
            block
            size="large"
            color="primary"
            type="submit"
            :loading="loading"
            class="mb-4"
          >
            Sign In
          </v-btn>
        </v-form>

        <div class="d-flex align-center my-4">
          <v-divider />
          <span class="text-caption text-medium-emphasis mx-3">or</span>
          <v-divider />
        </div>

        <v-btn
          block
          variant="outlined"
          color="primary"
          size="large"
          prepend-icon="mdi-account-circle-outline"
          :disabled="loading"
          @click="handleGuestLogin"
        >
          Continue as Guest
        </v-btn>

        <p class="text-center text-body-2 mt-4 mb-0">
          <a href="#" class="text-primary text-decoration-none" @click.prevent>Forgot password?</a>
        </p>
      </div>
      </v-col>
    </v-row>
  </v-main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

const { login } = useAuth()
const router = useRouter()

const formRef = ref(null)
const email = ref('')
const password = ref('')
const showPassword = ref(false)
const remember = ref(false)
const loading = ref(false)
const error = ref('')

const emailRules = [
  v => !!v || 'Email is required',
  v => /.+@.+/.test(v) || 'Enter a valid email',
]

const passwordRules = [
  v => !!v || 'Password is required',
]

onMounted(() => {
  const saved = localStorage.getItem('vue-la-remembered-email')
  if (saved) {
    email.value = saved
    remember.value = true
  }
})

function handleGuestLogin() {
  login({ email: 'guest@demo.local', password: 'guest' })
  router.push('/dashboard')
}

async function onSubmit() {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  loading.value = true
  error.value = ''

  if (remember.value) {
    localStorage.setItem('vue-la-remembered-email', email.value)
  } else {
    localStorage.removeItem('vue-la-remembered-email')
  }

  login({ email: email.value, password: password.value })
  router.push('/dashboard')
}
</script>

<style scoped>
.left-panel {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)) 0%, rgb(var(--v-theme-primary-darken-2)) 50%, rgb(var(--v-theme-primary-darken-4)) 100%);
}
</style>
