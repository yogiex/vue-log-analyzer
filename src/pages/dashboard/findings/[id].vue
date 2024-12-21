<template>
  <v-layout class="rounded rounded-md" style="min-height: 100vh;">
    <NavbarLayout />
    <SidebarLayout />
    <v-main>
      <div id="element-to-report">
        <v-container>
          <v-row>
            <v-col>
              <h1>
                User ID
              </h1>
            </v-col>
            <v-col>
              <h1>{{ datas.userid }}</h1>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <h1>
                Firstname
              </h1>
            </v-col>
            <v-col>
              <h1>{{ datas.firstname }}</h1>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <h1>
                Lastname
              </h1>
            </v-col>
            <v-col>
              <h1>{{ datas.lastname }}</h1>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <h1>
                Timedate
              </h1>
            </v-col>
            <v-col>
              <h1>{{ datas.timedate }}</h1>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <h1>
                Timestart
              </h1>
            </v-col>
            <v-col>
              <h1>{{ datas.timestart }}</h1>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <h1>
                Time finish
              </h1>
            </v-col>
            <v-col>
              <h1>{{ datas.timefinish }}</h1>
            </v-col>
          </v-row>
        </v-container>
        <v-btn @click="exportToPdf">
          Download
        </v-btn>
      </div>
    </v-main>
  </v-layout>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios';
import { useRoute } from 'vue-router'
import html2pdf from 'html2pdf.js'
import NavbarLayout from '@/layouts/dashboard/navbarLayout.vue';
import SidebarLayout from '@/layouts/dashboard/sidebarLayout.vue';

let datas = []
export default {
  components: { NavbarLayout, SidebarLayout },
  data() {
    return {
      datas: []
    };
  },
  // beforeMounted() {
  //     let route = useRoute();
  //     axios.get(`http://localhost:3000/example-kasus.json`).then(val => {
  //         val.data.forEach((element, idx) => {
  //             if (element.userid == route.params.id) {
  //                 this.datas = element;
  //             }
  //         });
  //         console.log(this.datas);
  //     });
  // },
  methods: {
    exportToPdf() {
      html2pdf(document.getElementById('element-to-report'), {
        margin: 1,
        filename: this.datas.timedate + ".jpg"
      });
    }
  },
  // ----------------------------------------------------------


  beforeMount() {
    console.log("tes")
    let route = useRoute();
    axios.get(`http://localhost:3000/example-kasus.json`).then(val => {
      val.data.forEach((element, idx) => {
        if (element.userid == route.params.id) {
          this.datas = element;
        }
      });
      console.log(this.datas);
    });
    return { datas }
  },


}
</script>

<style lang="scss" scoped></style>
