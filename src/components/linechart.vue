<template>
    <div class="" style="height: 40vh;">
        <Line :data="chartData" :options="chartOptions" />
    </div>
</template>

<script>
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)
export default {
    components: {
        Line
    },
    data:() => ({
        chartData: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
            datasets: [
             {
                label: 'Timeline',
                backgroundColor: '#f87979',
                data: [40, 39, 10, 40, 39, 80, 40]
             }
            ]   
        },
        chartOptions: {
            responsive: true,
            
        }
    }),
}

</script>

<style lang="scss" scoped>

</style>