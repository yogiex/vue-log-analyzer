<!-- eslint-disable vue/valid-v-slot -->
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


        <v-data-table :headers="headers" :items="kasusPeserta" :search="search">
          <template v-slot:item.status="{ item }">
            <div class="">
              <v-chip :color="kasusPeserta.status == 'terindikasi' ? 'green' : 'red'"
                :text="kasusPeserta.status == 'terindikasi' ? 'Aman' : 'Terindikasi'" class="text-uppercase" label
                size="small"></v-chip>
            </div>
          </template>
          <template v-slot:item.action="{ item }">
            <!-- <v-icon class="me-2" size="small" @click="printToDoc(item.userid)">
              mdi-cloud-print
            </v-icon> -->
            <a :href="'/dashboard/findings/' + item.userid">
              <v-icon class="me-2" size="small">
                mdi-cloud-print
              </v-icon>
              Download
            </a>
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

let url = `${import.meta.env.VITE_APP_URL_ENDPOINT}`
export default {
  components: { NavbarLayout, SidebarLayout },
  data() {
    return {
      search: '',
      headers: [
        { key: 'userid', title: 'User ID' },
        {
          align: 'start',
          key: 'firstname',
          sortable: false,
          title: 'Username',
        },
        { key: 'lastname', title: 'Full Name' },
        { key: 'timestart', title: 'Time Start' },
        { key: 'timefinish', title: 'Time Finished' },
        { key: 'timedate', title: 'Time Date' },
        { key: 'time_taken', title: 'Durasi Pengerjaan' },
        { key: 'score', title: 'Nilai' },
        { key: 'status', title: 'Status' },
        {
          key: 'action',
          title: 'Actions'
        }
      ],
      kasusPeserta: [],
    }
  },
  mounted() {
    // axios.get(`${url}/api/get_cases`)
    //   .then(val => {
    //     val.data.map(v => this.dataPeserta.push(v))
    //     this.dataPeserta = val.data
    //     console.log(this.dataPeserta)
    //   })
    // dataPeserta.map(val => {
    //   this.dataPeserta.push(val)
    // })
    axios.get(`http://localhost:3000/example-kasus.json`)
      .then(val => {
        this.kasusPeserta = val.data
        console.log(this.kasusPeserta)
      })
  },
  methods: {
    printToDoc(id) {
      alert(id)
    }
  }
}
</script>
