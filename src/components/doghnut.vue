<template>
        <div class="" style="height: 40vh;">
            <Doughnut :data="chartData" :options="chartOptions" />
        </div>
</template>

<script >
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Doughnut } from 'vue-chartjs'
ChartJS.register(ArcElement, Tooltip, Legend)
export default {
    components: {
        Doughnut
    },
    data: () => ({
        chartData: {
            labels: ['Low', 'Critical'],
            datasets: [
            {
                backgroundColor: ['#41B883', '#DD1B16'],
                data: [40, 20]
            }
            ]
            },
            chartOptions: {
                // responsive: true
            }
        }),

}
</script>

<style lang="scss" scoped>

</style>