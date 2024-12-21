<template>
  <v-layout class="rounded rounded-md" style="min-height: 100vh;">
    <NavbarLayout />
    <SidebarLayout />
    <v-main>
      <v-container>
        <v-btn @click="exportToPdf" variant="outlined" color="blue" class="mt-10">
          Download
        </v-btn>
        <div class="w-75 mx-auto" id="element-to-report">
          <v-row>
            <v-col>
              <h1>Learning Management System</h1>
            </v-col>
            <v-col>
              <!-- <v-img :width="195" src="/public/logo-log-analyzer.png"></v-img> -->
              <h1>English Proficiency Test</h1>
            </v-col>
          </v-row>
          <p class="text-justify">Laporan ini disusun berdasarkan hasil analisis log sistem yang berasal dari Log
            Analyzer,
            dengan cakupan periode analisis mulai dari {{ datas.timestart }} hingga {{ datas.timefinish }}. Log sistem
            yang
            dianalisis mencakup berbagai jenis aktivitas, termasuk akses pengguna, perubahan data, interaksi dengan
            server, serta aktivitas lain yang tercatat di dalam sistem.</p>
          <v-row class="bg-blue-lighten-3 mt-5">
            <v-col>
              <p>User ID</p>
            </v-col>
            <v-col>
              <p>{{ datas.userid }}</p>

            </v-col>
          </v-row>
          <v-row class="bg-blue-lighten-5">
            <v-col>
              <p>Firstname</p>
            </v-col>
            <v-col>
              <p>{{ datas.firstname }}</p>
            </v-col>
          </v-row>
          <v-row class="bg-blue-lighten-3">
            <v-col>
              <p>Lastname</p>
            </v-col>
            <v-col>
              <p>{{ datas.lastname }}</p>
            </v-col>
          </v-row>
          <v-row class="bg-blue-lighten-5">
            <v-col>

              <p>Timedate</p>
            </v-col>
            <v-col>
              <p>{{ datas.timedate }}</p>
            </v-col>
          </v-row>
          <v-row class="bg-blue-lighten-3 ">
            <v-col>
              <p>Timestart</p>
            </v-col>
            <v-col>

              <p>{{ datas.timestart }}</p>
            </v-col>
          </v-row>
          <v-row class="bg-blue-lighten-5">
            <v-col>
              <p>Time Finish</p>
            </v-col>
            <v-col>
              <p>{{ datas.timefinish }}</p>
            </v-col>
          </v-row>
          <p class="text-justify mt-10">Sebagai bagian dari proses pelaporan, informasi penting dari log sistem yang
            relevan
            telah diorganisasi dan
            disajikan dengan jelas untuk memudahkan pemahaman. Setiap temuan yang diidentifikasi dalam laporan ini juga
            disertai dengan rekomendasi tindakan mitigasi yang dapat segera diimplementasikan untuk mencegah terjadinya
            kerugian lebih lanjut akibat aktivitas yang mencurigakan atau tindakan kecurangan yang terindikasi.

            Dengan laporan ini, diharapkan semua pihak yang bertanggung jawab terhadap keamanan dan operasional sistem
            dapat bekerja sama untuk memastikan bahwa sistem tetap aman, andal, dan terlindungi dari berbagai potensi
            ancaman yang ada.</p>

        </div>
      </v-container>
      <!-- end of content -->
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
