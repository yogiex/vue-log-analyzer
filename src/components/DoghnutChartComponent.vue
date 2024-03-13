<template>
    <Doughnut :data="chartData" :options="chartOptions" />
</template>
<script>
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
ChartJS.register(ArcElement, Tooltip, Legend)

import { Doughnut } from 'vue-chartjs'
export default {
    components: {Doughnut},
    data() {
        return {
            chartData: {
                labels: ['Low', 'Medium', 'High'],
                datasets: [
                    {
                        backgroundColor: ['#41B883', '#E46651', '#DD1B16'],
                        data: [40, 20, 10]
                    }
                ]
            },
            chartOptions: {
                responsive: true,
                maintainAspectRatio: false
            }
        }
    }
}
</script>
