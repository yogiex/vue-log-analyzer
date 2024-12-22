<template>
  <div>
    <v-img class="mx-auto my-6" max-width="228" src="/logo-log-analyzer.png"></v-img>

    <form @submit.prevent="onSubmit">
      <v-card class="mx-auto pa-12 pb-8" elevation="8" max-width="448" rounded="lg">
        <div class="text-subtitle-1 text-medium-emphasis">Account</div>

        <v-text-field density="compact" placeholder="Email address" prepend-inner-icon="mdi-email-outline"
          variant="outlined" v-model="credentials.email"></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
          Password

          <a class="text-caption text-decoration-none text-blue" href="/login" rel="noopener noreferrer" target="_blank">
            Forgot login password?</a>
        </div>

        <v-text-field :type="visible ? 'text' : 'password'" density="compact" placeholder="Enter your password"
          prepend-inner-icon="mdi-lock-outline" variant="outlined" v-model="credentials.password"></v-text-field>

        <v-card class="mb-12" color="surface-variant" variant="tonal">
        </v-card>

        <v-btn block class="mb-8" color="blue" size="large" variant="tonal" type="submit">
          Log In
        </v-btn>

        <v-dialog v-model="dialog" width="auto">
          <v-card max-width="400" prepend-icon="mdi-update" text="Authentication failed! Invalid credentials."
            title="Auth Error">
            <template v-slot:actions>
              <v-btn class="ms-auto" text="Ok" @click="dialog"></v-btn>
            </template>
          </v-card>
        </v-dialog>

      </v-card>
    </form>
    <!-- <v-card class="mx-auto pa-12 pb-8" elevation="8" max-width="448" rounded="lg">
      <div class="text-subtitle-1 text-medium-emphasis">Account</div>

      <v-text-field density="compact" placeholder="Email address" prepend-inner-icon="mdi-email-outline"
        variant="outlined" v-model="email"></v-text-field>

      <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
        Password

        <a class="text-caption text-decoration-none text-blue" href="/login" rel="noopener noreferrer" target="_blank">
          Forgot login password?</a>
      </div>

      <v-text-field :type="visible ? 'text' : 'password'" density="compact" placeholder="Enter your password"
        prepend-inner-icon="mdi-lock-outline" variant="outlined" v-model="password"></v-text-field>

      <v-card class="mb-12" color="surface-variant" variant="tonal">
      </v-card>

      <v-btn block class="mb-8" color="blue" size="large" variant="tonal" @click="login">
        Log In
      </v-btn>

      <v-dialog v-model="dialog" width="auto">
        <v-card max-width="400" prepend-icon="mdi-update" text="Authentication failed! Invalid credentials."
          title="Auth Error">
          <template v-slot:actions>
            <v-btn class="ms-auto" text="Ok" @click="dialog"></v-btn>
          </template>
        </v-card>
      </v-dialog>

    </v-card> -->


  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { getAuth, signInWithEmailAndPassword } from 'firebase/auth'
import { useAuthStore } from '../store/auth'
const authStore = useAuthStore()
let dialog = false
const router = useRouter()
const onSubmit = () => {
  authStore.loginUser(credentials)
  console.log(credentials)
  console.log("on submit clicked")

}
const credentials = reactive({
  email: '',
  password: ''
})
onMounted(() => {
  authStore.init()
})

// const login = () => {
//   const auth = getAuth()
//   signInWithEmailAndPassword(auth, email.value, password.value)
//     .then((data) => {
//       console.log(email.value, password.value)
//       console.log('login successfull')
//       console.log(auth.currentUser)
//       console.log(auth.currentUser.email)
//       router.push('/dashboard')
//     })
//     .catch((error) => {
//       console.log(email.value, password.value)
//       console.log(error.code)
//       // alert(error.code)
//       dialog = false
//       // ErrorMessage.value = error.code
//     })

// }
</script>
