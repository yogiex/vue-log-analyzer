<template>
    <v-layout class="rounded rounded-md" style="min-height: 100vh;">
      <NavbarLayout />
      <SidebarLayout />
      <v-main>
        <v-container>
          <h1>Data Details Backup Files</h1>
          <v-data-table :headers="headers" :items="dataFiles" :search="search">
            <template v-slot:item.actions="{ item }">
                <a :href="item.url">
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
import { useRoute, useRouter } from 'vue-router';

export default {
  components: { NavbarLayout, SidebarLayout },
  methods: {
    async downloadsFile(){

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
    }
  },
  async onMounted(){
  },
  async mounted() {
    const route = useRoute();
    const id = route.params.id;
    console.log(route.params.id)
    console.log(id)
    const response = await axios.get(`http://180.250.135.11:8443/directory/${id}`);
    this.dataFiles = response.data
  }
}
</script>
