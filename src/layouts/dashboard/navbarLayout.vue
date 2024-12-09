<template>
  <v-app-bar title="Log Analyzer" color="primary" theme="">
    <!-- <v-img class="mx-2" max-height="40" src="../../../public/logo-log-analyzer.png">
    </v-img> -->
    <div class="date-now">
      <h2 id="date"></h2>
    </div>
    <div>
      <v-btn color="">
        <span class="mdi mdi-account-circle"></span>
        {{ emailUser }}
        <v-menu activator="parent">
          <v-list>
            <v-list-item>
              <v-list-item-title>
                <a href="">
                  <v-btn variant="plain">Edit Account</v-btn>
                </a>
              </v-list-item-title>
              <v-list-item-title>
                <a href="/login">
                  <v-btn variant="plain">Sign Out</v-btn>
                </a>
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-btn>

    </div>

  </v-app-bar>
</template>

<script>
import { signOut, getAuth, onAuthStateChanged } from 'firebase/auth'
import { useRouter } from 'vue-router'

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
  document.getElementById("date").innerHTML = fullTime
}
const router = useRouter()
const auth = getAuth()
// console.log(auth, auth.currentUser, auth.currentUser.email)
// const email = auth.currentUser.email


export default {
  methods() {
    const logout = () => {
      const auth = getAuth()
      signOut(auth)
        .then(() => {
          router.push('/login')
        }).catch((error) => {
          console.log(error)
        })
    }
  },
  props: ['emailUser'],
  data() {
    return {
      isAuthenticated: false,
      email: null,
    }
  }
  , mounted() {
    onAuthStateChanged(auth, (user) => {
      if (this.email == null) {
        this.isAuthenticated = true;
      } else {
        router.push("/login"); // Redirect jika user tidak login
      }
    });
  }
}
setInterval(updateTime, 1000); // Run updateTime() every second
</script>

<style>
.date-now {
  padding-right: 1rem;
}
</style>
