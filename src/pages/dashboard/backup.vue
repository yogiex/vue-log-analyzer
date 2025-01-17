<template>
  <v-layout class="rounded rounded-md" style="min-height: 100vh;">
    <NavbarLayout />
    <SidebarLayout />
    <v-main>
      <v-container>
        <h1>
          Backup Data
        </h1>
        <v-btn variant="tonal" @click="backup()">
          Backup!!
        </v-btn>
        <template v-slot:text>
          <v-text-field v-model="search" label="Search" prepend-inner-icon="mdi-magnify" single-line variant="outlined"
            hide-details></v-text-field>
        </template>
        <v-data-table :headers="headers" :items="dataFiles" :search="search">
          <template v-slot:item.actions="{ item }">
            <a :href="'/dashboard/downloads/' + item.title">
              <v-icon>mdi-cloud-print</v-icon>
            </a>
          </template>
        </v-data-table>
      </v-container>
    </v-main>

  </v-layout>
</template>

<script>
import NavbarLayout from '@/layouts/dashboard/navbarLayout.vue';
import SidebarLayout from '@/layouts/dashboard/sidebarLayout.vue';
import axios from 'axios';
let urlEndpoint = import.meta.env.URL_FLASK_API
let dataFiles = []
export default {
  components: { NavbarLayout, SidebarLayout },
  methods: {
    async backup() {
      console.log(import.meta.env)
      // const response = await axios.post(`${urlEndpoint}/dump`)
      const response = await axios.post(`http://180.250.135.11:8443/dump`)
      console.log(urlEndpoint)
      console.log(response)
      alert(response.data)
      window.location.reload();
    }
  },
  data() {

    return {
      search: '',
      headers: [
        { key: 'title', title: 'Title ' },
        { key: 'url', title: 'Url' },
        { key: 'actions', title: 'Actions' },
      ],
      dataFiles: [],
      downloadLink: []
    }
  },
  async mounted() {
  },
  async beforeMount() {
    // axios.get(`${urlEndpoint}/directory`)
    //   .then(val => {
    //       val.data.map(v => this.dataFiles.push(v))
    //       this.dataFiles = val.data
    //       console.log(val)
    //       console.log(this.dataFiles)
    //   })
  // const response = await axios.get(`${urlEndpoint}/directory`)
  const response = await axios.get('http://180.250.135.11:8443/directory')
  // response
  this.dataFiles = response.data
  console.log(response.data)
  console.log(`${urlEndpoint}/directory`)

    
  }
}
</script>
