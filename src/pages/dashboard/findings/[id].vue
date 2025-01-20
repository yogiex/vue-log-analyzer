<template>
  <DashboardLayout>
    <v-container>
      <v-card>
        <v-btn>
          
        </v-btn>
        <v-btn @click="exportToPdf" variant="outlined" color="blue" class="mt-10 ml-4">
          Download
        </v-btn>
        <div class="w-75 mx-auto my-5" id="element-to-report">
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
            dianalisis mencakup berbagai jenis aktivitas.</p>
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
          <p class="text-justify mt-10">
            Berdasarkan temuan di atas, peserta [nama peserta] dengan ID [ID peserta] diduga kuat telah melakukan
            tindakan kecurangan selama pelaksanaan ujian EPrT. Kami merekomendasikan tindakan lebih lanjut sesuai dengan
            kebijakan yang berlaku untuk menjaga integritas dan kredibilitas ujian.

            Pelapor:
            [nama pelapor atau sistem]
            [unit/divisi terkait]
            [contact informasi, jika diperlukan]
          </p>

        </div>
      </v-card>
    </v-container>
  </DashboardLayout>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios';
import { useRoute } from 'vue-router'
import html2pdf from 'html2pdf.js'
import DashboardLayout from '@/layouts/dashboard/dashboardLayout.vue';

let datas = []
export default {
  components: { DashboardLayout },
  data() {
    return {
      datas: []
    };
  },

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
