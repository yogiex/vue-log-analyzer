<template>
  <v-card variant="tonal">
    <v-card-item>
      <v-card-title class="text-h6">Status Distribution</v-card-title>
      <v-card-subtitle class="text-body-2 text-medium-emphasis">Participant honesty classification</v-card-subtitle>
    </v-card-item>
    <div style="height: 35vh;" role="img" aria-label="Donut chart showing distribution of participant status">
      <Doughnut :data="chartData" :options="chartOptions" />
    </div>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Doughnut } from 'vue-chartjs'
import { useMockChartData } from '@/composables/useMockData'
import { COLORS } from '@/theme/colors'

ChartJS.register(ArcElement, Tooltip, Legend)

const mock = useMockChartData()

const chartData = computed(() => ({
  labels: mock.donutLabels,
  datasets: [
    {
      backgroundColor: mock.donutColors,
      hoverBackgroundColor: [COLORS.hover.primary, COLORS.hover.secondary],
      data: mock.donutData,
      borderWidth: 0,
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
      callbacks: {
        label(context) {
          const total = context.dataset.data.reduce((a, b) => a + b, 0)
          const value = context.parsed
          const pct = ((value / total) * 100).toFixed(1)
          return ` ${context.label}: ${value} (${pct}%)`
        },
      },
    },
  },
}
</script>

<style lang="scss" scoped></style>
