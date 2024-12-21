<template>
  <v-layout class="rounded rounded-md" style="min-height: 100vh;">
    <NavbarLayout />
    <SidebarLayout />


    <v-main>
      <v-card-text>
        <v-text-field :loading="loading" density="compact" variant="solo" label="Search" append-inner-icon="mdi-magnify"
          single-line hide-details @click:append-inner="onClick"></v-text-field>
      </v-card-text>
      <v-container>
        <v-row class="mb-6">
          <v-col>
            <v-card class="mx-auto" max-width="344" hover color="primary">
              <v-card-item>
                <v-card-title>
                  Record Count
                </v-card-title>
                <v-card-subtitle>

                </v-card-subtitle>
              </v-card-item>

              <v-card-text>
                <h1>{{ datas.recordCount }}</h1>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col>
            <v-card class="mx-auto" max-width="344" hover color="primary">
              <v-card-item>
                <v-card-title>
                  Total Cases
                </v-card-title>
                <v-card-subtitle>

                </v-card-subtitle>
              </v-card-item>

              <v-card-text>

                <h1>{{ datas.totalCase }}</h1>
              </v-card-text>

            </v-card>
          </v-col>
          <v-col>
            <v-card class="mx-auto" max-width="344" hover color="primary">
              <v-card-item>
                <v-card-title>
                  Total Users
                </v-card-title>
                <v-card-subtitle>
                  <!-- tes -->
                </v-card-subtitle>
              </v-card-item>

              <v-card-text>
                <h1>{{ datas.totalUser }}</h1>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col>
            <v-card class="mx-auto" max-width="344" hover color="primary">
              <v-card-item>
                <v-card-title>
                  Total Request
                </v-card-title>
                <v-card-subtitle>

                </v-card-subtitle>
              </v-card-item>

              <v-card-text>
                <h1>{{ datas.totalRequest }}</h1>
              </v-card-text>
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
  </v-layout>
  <router-view></router-view>
</template>

<script>
import { getAuth } from 'firebase/auth'
import NavbarLayout from '@/layouts/dashboard/navbarLayout.vue';
import SidebarLayout from '@/layouts/dashboard/sidebarLayout.vue';
import doghnut from '@/components/doghnut.vue';
import linechart from '@/components/linechart.vue';
import axios from 'axios';

let url = `${import.meta.env.VITE_APP_URL_ENDPOINT}`
const auth = getAuth();
let datas = []
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
  beforeMount() {
    console.log("tes")
    axios.get(`http://localhost:3000/allsummary.json`).then(val => {
      // console.log(datas)
      // console.log(val.data)
      this.datas = val.data
      console.log(datas)
    });
    return { datas }
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

  // mounted() {
  // axios.get(`${url}/get_summary`)
  //   .then(val => {
  //     val.data.map(v => this.datas.push(v))
  //     this.datas = val.data[1]
  //     console.log(this.datas)
  //   })
  // axios.get(`http://localhost:3000/allsummary.json`)
  //   .then(val => {
  //     console.log(val.data)
  //     this.datas.push(val.data)
  //   })
  // const response = fetch(`http://localhost:3000/allsummary.json`)
  // response.then(val => {
  //   console.log(val)
  // })
  // }
}
</script>

<style></style>
