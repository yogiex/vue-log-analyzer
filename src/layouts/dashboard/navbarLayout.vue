<template>
  <v-app-bar title="Log Analyzer" color="primary" theme="">
    <div class="date-now">
      <h2 id="date"></h2>
    </div>
    <div>
      <p>{{ email }}</p>
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
import { onMounted } from 'vue'
const email = ref(null); // Reactive variable for email
const authStore = useAuthStore()
const onlogout = () => {
  authStore.logOut()
}
onMounted: {
  const auth = getAuth();
  onAuthStateChanged(auth, (userDetails) => {
    if (userDetails && userDetails.email) {
      email.value = userDetails.email; // Set email if user is valid
      console.log(`User is logged in as: ${email.value}`);
    } else {
      console.warn('No valid user detected. Redirecting to login.');
      router.push('/login'); // Redirect to login if no user is found
    }
  });
}
function updateTime() {
  const currentTime = new Date();
  const y = currentTime.getFullYear();
  const m = currentTime.getMonth() + 1;
  const d = currentTime.getDate();
  const h = currentTime.getHours().toString().padStart(2, '0');
  const mm = currentTime.getMinutes().toString().padStart(2, '0');
  const s = currentTime.getSeconds().toString().padStart(2, '0');
  const fullTime = `${y}/${m}/${d} ${h}:${mm}:${s}`;
  const dateElement = document.getElementById("date");
  if (dateElement) {
    dateElement.innerHTML = fullTime;
  }
}

setInterval(updateTime, 1000);

</script>

<style>
.date-now {
  padding-right: 1rem;
}
</style>
