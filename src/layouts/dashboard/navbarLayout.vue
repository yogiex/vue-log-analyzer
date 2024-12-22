<template>
  <v-app-bar title="Log Analyzer" color="primary" theme="">
    <div class="date-now">
      <h2 id="date"></h2>
    </div>
    <div>
      <v-btn color="">
        <span class="mdi mdi-account-circle"></span>

        <v-menu activator="parent">
          <v-list>
            <v-list-item>
              <v-list-item-title>
                <a href="">
                  <v-btn variant="plain">Edit Account</v-btn>
                </a>
              </v-list-item-title>
              <v-list-item-title>
                <v-btn variant="plain" @click.prevent="onlogout">Sign Out</v-btn>
                <a href="/login">

                </a>
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-btn>

    </div>

  </v-app-bar>
</template>

<script setup>
import { useAuthStore } from '@/store/auth';
import { signOut, getAuth, onAuthStateChanged } from 'firebase/auth'
import { useRouter } from 'vue-router'
const authStore = useAuthStore()
const onlogout = () => {
  authStore.logOut()
}
function updateTime() {
  let currentTime = new Date();
  let m = currentTime.getMonth();
  let d = currentTime.getDay()
  let s = currentTime.getSeconds();
  let y = currentTime.getFullYear();
  let h = currentTime.getHours();
  let mm = currentTime.getMinutes();
  let n = currentTime.toLocaleDateString()
  let fullTime = `${y}/${m}/${d} ${h}:${mm}:${s}`
  // document.getElementById("date").innerHTML = fullTime
}

// const router = useRouter()
// const auth = getAuth()
// console.log(auth, auth.currentUser, auth.currentUser.email)
// const email = auth.currentUser.email

// export default {
//   methods() {
//     const logout = () => {
//       const auth = getAuth()
//       signOut(auth)
//         .then(() => {
//           router.push('/login')
//         }).catch((error) => {
//           console.log(error)
//         })
//     }
//   },
//   props: ['emailUser'],
//   data() {
//     return {
//       isAuthenticated: false,
//       email: null,
//     }
//   }
//   , mounted() {
//     onAuthStateChanged(auth, (user) => {
//       if (this.email == null) {
//         this.isAuthenticated = true;
//       } else {
//         router.push("/login"); // Redirect jika user tidak login
//       }
//     });
//   }
// }
setInterval(updateTime, 1000); // Run updateTime() every second
</script>

<style>
.date-now {
  padding-right: 1rem;
}
</style>
