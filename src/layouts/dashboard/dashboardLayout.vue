<template>

  <v-layout>
    <NavbarLayout emailUser:auth.currentUser.email />
    <SidebarLayout />
    <v-main>

    </v-main>
  </v-layout>

</template>


<script>
import NavbarLayout from '@/layouts/dashboard/navbarLayout.vue'
import SidebarLayout from '@/layouts/dashboard/sidebarLayout.vue';
import { getAuth, onAuthStateChanged } from 'firebase/auth'
import { useRouter } from 'vue-router'



const router = useRouter()
const auth = getAuth()
export default {
  data() {
    return {}
  },
  components: { NavbarLayout, SidebarLayout },
  mounted() {
    onAuthStateChanged(auth, (user) => {
      if (this.email == null) {
        this.isAuthenticated = true;
      } else {
        router.push("/login"); // Redirect jika user tidak login
      }
    });

  }
}
</script>
