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


        <v-data-table :headers="headers" :items="dataPeserta" :search="search">
          <template v-slot:item.status="{ item }">
            <div class="">
              <v-chip :color="dataPeserta.status == 'terindikasi' ? 'green' : 'red'"
                :text="dataPeserta.status == 'terindikasi' ? 'Aman' : 'Terindikasi'" class="text-uppercase" label
                size="small"></v-chip>
            </div>
          </template>
        </v-data-table>



      </v-card>
    </v-main>
  </v-layout>
</template>

<script>

import NavbarLayout from '@/layouts/dashboard/navbarLayout.vue';
import SidebarLayout from '@/layouts/dashboard/sidebarLayout.vue';
import { faker } from '@faker-js/faker';
import axios from 'axios';

let url = `${import.meta.env.VITE_APP_URL_ENDPOINT}`
let currentTime = new Date();
let m = currentTime.getMonth();
let d = currentTime.getDay()
let s = currentTime.getSeconds();
let y = currentTime.getFullYear();
let h = currentTime.getHours();
let mm = currentTime.getMinutes();
let n = currentTime.toLocaleDateString()
let fullTime = `${y}/${m}/${d} ${h}:${mm}:${s}`

const start = faker.date.soon();
const end = faker.date.soon({ refDate: start });


const dataPeserta = [
  {
    userid: faker.string.uuid(),
    firstname: faker.string.firstname,
    lastname: faker.string.lastname,
    timestart: start,
    timefinish: end,
    timedate: fullTime,
    time_taken: faker.date.between({ from: start, to: end }),
    score: faker.number.int({ min: 20, max: 45 }),
    status: 'Terindikasi'
  },
  {
    userid: faker.string.uuid(),
    firstname: faker.string.firstname,
    lastname: faker.string.lastname,
    timestart: start,
    timefinish: end,
    timedate: fullTime,
    time_taken: faker.date.between({ from: start, to: end }),
    score: faker.number.int({ min: 20, max: 45 }),
    status: 'Terindikasi'
  },
  {
    userid: faker.string.uuid(),
    firstname: faker.string.firstname,
    lastname: faker.string.lastname,
    timestart: start,
    timefinish: end,
    timedate: fullTime,
    time_taken: faker.date.between({ from: start, to: end }),
    score: faker.number.int({ min: 20, max: 45 }),
    status: 'Terindikasi'
  }
]
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
      dataPeserta: [],
    }
  },
  mounted() {
    // axios.get(`${url}/api/get_cases`)
    //   .then(val => {
    //     val.data.map(v => this.dataPeserta.push(v))
    //     this.dataPeserta = val.data
    //     console.log(this.dataPeserta)
    //   })
    dataPeserta.map(val => {
      this.dataPeserta.push(val)
    })
  }
}
</script>
