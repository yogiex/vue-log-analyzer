<template>
  <v-layout class="rounded rounded-md" style="min-height: 100vh;">
    <NavbarLayout />
    <SidebarLayout />
    <v-main>
      <v-card flat title="User Filter">
        <template v-slot:text>
          <v-text-field v-model="search" label="Search" prepend-inner-icon="mdi-magnify" single-line variant="outlined"
            hide-details></v-text-field>
        </template>
        <v-data-table :headers="headers" :items="dataPeserta" :search="search">
          <template v-slot:item.status="{ item }">
            <!-- <div class="">
              <v-chip :text="dataPeserta.status == 'aman' ? 'Warning' : 'Safe'"
                :color="dataPeserta.status == 'aman' ? 'red' : 'green'" class="text-uppercase" label size="small">
              </v-chip>
            </div> -->
          </template>
        </v-data-table>
      </v-card>
    </v-main>
  </v-layout>
</template>

<script>

import NavbarLayout from '@/layouts/dashboard/navbarLayout.vue';
import SidebarLayout from '@/layouts/dashboard/sidebarLayout.vue';
import axios from 'axios';
import { useRoute } from 'vue-router'
let url = import.meta.env.URL_FLASK_API
let dataPeserta = []
export default {
  components: { NavbarLayout, SidebarLayout },
  data() {

    return {
      search: '',
      headers: [
        {
          key: 'id', title: 'ID'
        },
        {
          key: 'attempt_id', title: 'Attempt ID'
        },
        {
          align: 'start',
          key: 'firstname',
          sortable: false,
          title: 'Username',
        },
        { key: 'lastname', title: 'Full Name' },
        { key: 'quiz_name', title: 'Quiz Name' },
        { key: 'timestart', title: 'Time Start' },
        { key: 'timefinish', title: 'Time Finished' },
        { key: 'diff_time_minute', title: 'Durasi Pengerjaan' },
        { key: 'session', title: 'Sesi Pengerjaan' },
        { key: 'score', title: 'Nilai' },
      ],
      dataPeserta: [],
    }
  },
  beforeMount() {

    axios.get(``).then(val => {
      this.dataPeserta = val.data
      console.log(dataPeserta)
    });
    // 
    // axios.get(`http://localhost:3000/big_frame.json`).then(val => {
    //   this.dataPeserta = val.data
    //   console.log(dataPeserta)
    // });
    return { dataPeserta }
  },
}
</script>
