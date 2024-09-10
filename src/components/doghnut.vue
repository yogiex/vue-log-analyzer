<template>
        <div class="" style="height: 40vh;">
            <Doughnut :data="chartData" :options="chartOptions" />
        </div>
</template>

<script >
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Doughnut } from 'vue-chartjs'
import axios from 'axios';
let url = 'http://180.250.135.11:5000'

ChartJS.register(ArcElement, Tooltip, Legend)
export default {
    components: {
        Doughnut
    },
    data(){
        return {
            chartData: {
                labels: ['Low', 'Critical'],
                datasets: [
                    {
                        backgroundColor: ['#41B883', '#DD1B16'],
                        data: [10,10]
                    }
                ]
            },
            chartOptions: {
                responsive: true
            },
            datas: []
        }
    },
    mounted(){
        axios.get(`${url}/get_summary`)
             .then(val =>{
                val.data.map(v => this.datas.push(v))
                this.datas = val.data[1]
                console.log(`logging di donnut ${this.datas}`)
             })
    }

}
</script>

<style lang="scss" scoped>

</style>
