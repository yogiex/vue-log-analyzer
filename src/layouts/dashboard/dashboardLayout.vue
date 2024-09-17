<template>
  
      <v-layout>
        <NavbarLayout></NavbarLayout>
      <SidebarLayout/>
      <v-main>
        
      </v-main>
      </v-layout>

</template>


<script>
import NavbarLayout from '@/layouts/dashboard/navbarLayout.vue'
import SidebarLayout from '@/layouts/dashboard/sidebarLayout.vue';

export default {
  components: {NavbarLayout, SidebarLayout}
}
</script>

