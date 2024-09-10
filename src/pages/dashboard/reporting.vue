<template>
  <v-layout class="rounded rounded-md" style="min-height: 100vh;">
    <NavbarLayout/>
    <SidebarLayout/>
    <v-main>
      <h1>tes</h1>
    </v-main>
    <reporting/>
  </v-layout>
</template>

<script>
import NavbarLayout from '@/layouts/dashboard/navbarLayout.vue';
import SidebarLayout from '@/layouts/dashboard/sidebarLayout.vue';
import reporting from '@/components/reporting.vue'
export default {
  components: {reporting,NavbarLayout,SidebarLayout}
}
</script>
