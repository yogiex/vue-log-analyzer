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
            <v-icon class="me-2" size="small" @click="editItem(item)">
              mdi-pencil
            </v-icon>
            <v-icon size="small" @click="deleteItem(item)">
              mdi-delete
            </v-icon>
          </template>
        </v-data-table>
      </v-card>
    </v-main>
  </v-layout>
</template>

<script>
import NavbarLayout from '@/layouts/dashboard/navbarLayout.vue';
import SidebarLayout from '@/layouts/dashboard/sidebarLayout.vue';
import reporting from '@/components/reporting.vue'
export default {
  components: { reporting, NavbarLayout, SidebarLayout },
  data() {
    return {
      search: '',
      headers: [
        { key: 'lastname', title: 'Full Name' },
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
    axios.get(`http://localhost:3000/example-kasus.json`)
      .then(val => {
        this.kasusPeserta = val.data
        console.log(this.kasusPeserta)
      })
  }
}
</script>
