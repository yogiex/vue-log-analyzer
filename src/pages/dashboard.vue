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
    <v-container>
      <v-row class="mb-6">
        <v-col>
          <v-card
    class="mx-auto"
    max-width="344"
    hover
    color="primary"
  >
    <v-card-item>
      <v-card-title>
        Card title
      </v-card-title>
      <v-card-subtitle>
        Card subtitle secondary text
      </v-card-subtitle>
    </v-card-item>

    <v-card-text>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    </v-card-text>
  </v-card>
        </v-col>
        <v-col>
          <v-card
    class="mx-auto"
    max-width="344"
    hover
    color="primary"
  >
    <v-card-item>
      <v-card-title>
        Card title
      </v-card-title>
      <v-card-subtitle>
        Card subtitle secondary text
      </v-card-subtitle>
    </v-card-item>

    <v-card-text>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    </v-card-text>
  </v-card>
        </v-col>
        <v-col>
          <v-card
    class="mx-auto"
    max-width="344"
    hover
    color="primary"
  >
    <v-card-item>
      <v-card-title>
        Card title
      </v-card-title>
      <v-card-subtitle>
        Card subtitle secondary text
      </v-card-subtitle>
    </v-card-item>

    <v-card-text>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    </v-card-text>
  </v-card>
        </v-col>
        <v-col>
          <v-card
    class="mx-auto"
    max-width="344"
    hover
    color="primary"
  >
    <v-card-item>
      <v-card-title>
        Card title
      </v-card-title>
      <v-card-subtitle>
        Card subtitle secondary text
      </v-card-subtitle>
    </v-card-item>

    <v-card-text>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    </v-card-text>
  </v-card>
        </v-col>
      </v-row>
    </v-container>
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