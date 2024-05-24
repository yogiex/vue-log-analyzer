<template>
        <Doughnut :data="chartData" :options="chartOptions" />
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
            labels: ['Low', 'Medium', 'Critical'],
            datasets: [
            {
                backgroundColor: ['#41B883', '#E46651', '#DD1B16'],
                data: [40, 20, 80]
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