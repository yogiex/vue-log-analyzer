<template>
    <v-layout class="rounded rounded-md">
        <NavbarViews/>
        <SidebarViews/>
        <v-main class="d-flex align-center justify-center" style="min-height: 300px;">
            <v-container
    class="fill-height"
    fluid
    style="min-height: 434px"
  >
    <v-fade-transition mode="out-in">
      <v-row>
        <v-col cols="6">
          <v-card>
            <v-img
              src="https://picsum.photos/350/165?random"
              height="325"
              class="bg-grey-lighten-2"
            ></v-img>
            <v-card-title class="text-h6">
              height
            </v-card-title>
          </v-card>
        </v-col>

        <v-col cols="6">
          <v-card>
            <v-img
              src="https://picsum.photos/350/165?random"
              height="325"
              cover
              class="bg-grey-lighten-2"
            ></v-img>
            <v-card-title class="text-h6">
              height with cover
            </v-card-title>
          </v-card>
        </v-col>

        <v-col cols="6">
          <v-card>
            <v-img
              src="https://picsum.photos/350/165?random"
              max-height="325"
              class="bg-grey-lighten-2"
            ></v-img>
            <v-card-title class="text-h6">
              max-height
            </v-card-title>
          </v-card>
        </v-col>
        


        <v-col cols="6">
          <v-card>
            
            <v-card-title class="text-h6">
              max-height with cover
            </v-card-title>
            <v-card-tex>
                <BarChartViewVue/>
            </v-card-tex>
            
          </v-card>
        </v-col>
      </v-row>
    </v-fade-transition>
  </v-container>
    </v-main>
    </v-layout>
    
    <!-- <h1>this is dashboard views</h1> -->

</template>

<script>
import SidebarViews from '../views/dashboard/SidebarViews.vue';
import NavbarViews from '../views/dashboard/NavbarViews.vue';
import BarChartViewVue from '../views/dashboard/BarChartView.vue';
import Chart from 'chart.js/auto'
export default {
    name: 'DashboardComponents',
    components: {
        SidebarViews,
        NavbarViews,
        BarChartViewVue
    },
    mounted(){
        console.log('mounted log')
        
  }
}


</script>