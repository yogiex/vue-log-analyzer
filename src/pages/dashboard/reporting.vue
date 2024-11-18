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
import reporting from '@/components/reporting.vue'
const datas = [
  {

  }
]
export default {
  components: { reporting, NavbarLayout, SidebarLayout }
}
</script>
