<template>
  <v-card variant="tonal" class="">
    <div class="" style="height: 40vh;">
      <Doughnut class="pa-md-1 mx-lg-auto" :data="chartData" :options="chartOptions" />

    </div>
  </v-card>
</template>

<script>
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Doughnut } from 'vue-chartjs'
import axios from 'axios';
// eslint-disable-next-line no-unused-vars
let url = 'http://180.250.135.11:5000'

ChartJS.register(ArcElement, Tooltip, Legend)
export default {
  components: {
    Doughnut
  },
  data() {
    return {
      chartData: {
        labels: ['Low', 'Critical'],
        datasets: [
          {
            backgroundColor: ['#4C9AFF', '#FF4C4C'],
            data: [Math.ceil(Math.random() * 1000000), Math.ceil(Math.random() * 1000000)]
          }
        ]
      },
      chartOptions: {
        responsive: true
      },
      datas: []
    }
  },
  mounted() {
    // axios.get(`${url}/get_summary`)
    //   .then(val => {
    //     val.data.map(v => this.datas.push(v))
    //     this.datas = val.data[1]
    //     console.log(`logging di donnut ${this.datas}`)
    //   })
    axios.get(`http://localhost:3000/allsummary.json`)
      .then(val => {
        this.datas.push(val.data)
        console.log(`logging di donnut ${this.datas}`)
      })
  }

}
</script>

<style lang="scss" scoped></style>
