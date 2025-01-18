<template>
  <v-layout class="rounded rounded-md" style="min-height: 100vh;">
    <NavbarLayout />
    <SidebarLayout />
    <!-- main section -->
    <v-main>
      <v-container>
        <v-row class="mb-6">
          <v-col>
            <v-card class="mx-auto" max-width="344" hover color="primary">
              <v-card-item>
                <v-card-title>
                  Record Count Step Query
                </v-card-title>
                <v-card-title>
                  <h1>{{ datas.count_total_steps }}</h1>
                </v-card-title>
              </v-card-item>
            </v-card>
          </v-col>
          <v-col>
            <v-card class="mx-auto" max-width="344" hover color="primary">
              <v-card-item>
                <v-card-title>
                  Total Logs
                </v-card-title>
                <v-card-title>
                  <h1>{{ datas.count_directory }}</h1>
                </v-card-title>
              </v-card-item>
            </v-card>
          </v-col>
          <v-col>
            <v-card class="mx-auto" max-width="344" hover color="primary">
              <v-card-item>
                <v-card-title>
                  Total Users
                </v-card-title>


              <v-card-title>
                <h1>{{ datas.count_users }}</h1>
              </v-card-title>
            </v-card-item>
            </v-card>
          </v-col>
          <v-col>
            <v-card class="mx-auto" max-width="344" hover color="primary">
              <v-card-item>
                <v-card-title>
                  Total Standar Logs
                </v-card-title>
              
              <v-card-title>
                <h1>{{ datas.count_mdl_standard_logs }}</h1>
              </v-card-title>
            </v-card-item>
            </v-card>
          </v-col>
        </v-row>
        <!-- end of cards -->

        <!-- start chartjs -->
        <div class="h-25">
          <v-row>
            <v-col>
              <doghnut />
            </v-col>
            <v-col>
              <linechart />
            </v-col>
          </v-row>
        </div>
        <!-- end of chartjs -->

        <!-- data tables -->
        <v-row>
          <v-col>
            <v-data-table :items="items"></v-data-table>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
    <!-- end of main section -->
  </v-layout>
  <router-view></router-view>
</template>

<script>
import { getAuth } from 'firebase/auth'
import { useAuthStore } from '@/store/auth'
import NavbarLayout from '@/layouts/dashboard/navbarLayout.vue';
import SidebarLayout from '@/layouts/dashboard/sidebarLayout.vue';
import doghnut from '@/components/doghnut.vue';
import linechart from '@/components/linechart.vue';
import axios from 'axios';

let url = import.meta.env.VITE_URL_FLASK_API
const auth = getAuth();

const authStore = useAuthStore
export default {
  components: { SidebarLayout, NavbarLayout, doghnut, linechart },
  data() {
    return {
      loaded: false,
      loading: false,
      datas: [],
      isAuthenticated: false,
    }
  },
  async beforeMount() {
    authStore().init()
    const response = await axios.get(`${url}/api/summary`)
    this.datas = response.data
    console.table(response.data)
  },
  methods: {
    onClick() {
      this.loading = true
      setTimeout(() => {
        this.loading = false
        this.loaded = true
      }, 2000)
    },
  },

  async mounted() {
    const response = await axios.get(`${url}/api/summary`)
    this.datas = response.data
    console.table(response.data)
  }
}
</script>

<style></style>
