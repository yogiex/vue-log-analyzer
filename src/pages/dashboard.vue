<template>
       <v-layout class="rounded rounded-md" style="min-height: 100vh;">
       <SidebarLayout/>
       <NavbarLayout/>
       
       <!-- <v-main class="d-flex align-center justify-center content-main" >
        
        <h1>tes heloo</h1>
      </v-main> -->
      <v-main>
        <v-card-text>
      <v-text-field
        :loading="loading"
        density="compact"
        variant="solo"
        label="Search templates"
        append-inner-icon="mdi-magnify"
        single-line
        hide-details
        @click:append-inner="onClick"
      ></v-text-field>
    </v-card-text>
      </v-main>
       </v-layout>
</template>

<script>
import dashboardLayout from '@/layouts/dashboard/dashboardLayout.vue';
import NavbarLayout from '@/layouts/dashboard/navbarLayout.vue';
import SidebarLayout from '@/layouts/dashboard/sidebarLayout.vue';

export default {
    components: { dashboardLayout, SidebarLayout, NavbarLayout },
    data: () => ({
        loaded: false,
      loading: false,
    }),
    methods: {
        onClick () {
        this.loading = true

        setTimeout(() => {
          this.loading = false
          this.loaded = true
        }, 2000)
      },
    }
}
</script>

<style>

</style>