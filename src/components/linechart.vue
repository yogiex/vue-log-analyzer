<template>
  <v-card variant="tonal">
    <v-card-item>
      <v-card-title class="text-h6">Cases Per Month</v-card-title>
      <v-card-subtitle class="text-body-2 text-medium-emphasis">Monthly trend of flagged cases</v-card-subtitle>
    </v-card-item>
    <div style="height: 35vh;" role="img" aria-label="Line chart showing monthly case trend">
      <Line :data="chartData" :options="chartOptions" />
    </div>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'
import { Line } from 'vue-chartjs'
import { useMockChartData } from '@/composables/useMockData'
import { COLORS } from '@/theme/colors'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
)

const mock = useMockChartData()

const chartData = computed(() => ({
  labels: mock.lineLabels,
  datasets: [
    {
      label: mock.lineLabel,
      backgroundColor: COLORS.chart.fillPrimary,
      borderColor: COLORS.primary,
      borderWidth: 2,
      pointBackgroundColor: COLORS.primary,
      pointBorderColor: COLORS.surface,
      pointBorderWidth: 2,
      pointRadius: 4,
      pointHoverRadius: 6,
      fill: true,
      tension: 0.3,
      data: mock.lineData,
    }
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        padding: 20,
        usePointStyle: true,
      },
    },
    tooltip: {
      backgroundColor: COLORS.chartTooltip,
      padding: 12,
      cornerRadius: 4,
    },
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: { maxTicksLimit: 6 },
    },
    y: {
      beginAtZero: true,
      grid: { color: COLORS.chartGrid },
      ticks: { precision: 0 },
    },
  },
}
</script>

<style lang="scss" scoped></style>
