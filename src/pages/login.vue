<template>
  <div>
    <v-img class="mx-auto my-6" max-width="228" src="/logo-log-analyzer.png"></v-img>


    <v-card class="mx-auto pa-12 pb-8" elevation="8" max-width="448" rounded="lg">
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
            <v-btn class="ms-auto" text="Ok" @click="dialog = false"></v-btn>
          </template>
        </v-card>
      </v-dialog>

    </v-card>


  </div>

</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { getAuth, signInWithEmailAndPassword } from 'firebase/auth'
const email = ref('')
const password = ref('')
const router = useRouter()
export default {
  data() {
    return {
      dialog: false,
      email: '',
      password: ''
    }
  },
  methods: {
    login() {
      const auth = getAuth()
      signInWithEmailAndPassword(auth, this.email, this.password)
        .then((data) => {
          router.push('/dashboard')
          console.log(this.email, this.password)

        }).catch((error) => {
          console.log(error.code)
          alert(error.code)
        })
    }
  }
}
// let dialog = false

// const email = ref("")
// const password = ref("")
// const router = useRouter()
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
//       alert(error.code)
//       // dialog = true
//       // ErrorMessage.value = error.code
//     })

// }
</script>
