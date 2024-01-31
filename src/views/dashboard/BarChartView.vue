<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export default {
  name: 'BarChartView',
  components: { Bar },
  data() {
    return {
      chartData: {
            labels: [
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December'
         ],
        datasets: [ {
            label: 'Data One',
            backgroundColor: '#f87979',
            data: [40, 20, 12, 39, 10, 40, 39, 80, 40, 20, 12, 11]
            } ]
      },
        chartOptions: {
            responsive: true,
            maintainAspectRatio: false
      },
      
    }
  }
}
</script>

<template>
    <Bar :data="chartData" :options="chartOptions" />
  </template>
  
 
  