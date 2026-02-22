<script setup>
import {
  CategoryScale,
  Chart as ChartJS,
  Filler,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  Tooltip,
} from 'chart.js'
import { computed } from 'vue'
import { Line } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend, Filler)

const props = defineProps({
  items: {
    type: Array,
    required: true,
  },
})

const chartData = computed(() => ({
  labels: props.items.map((i) => i.month),
  datasets: [
    {
      label: 'Доход',
      data: props.items.map((i) => i.income),
      borderColor: '#22c55e',
      backgroundColor: 'rgba(34, 197, 94, 0.2)',
      fill: true,
      tension: 0.35,
    },
    {
      label: 'Расход',
      data: props.items.map((i) => i.expense),
      borderColor: '#ef4444',
      backgroundColor: 'rgba(239, 68, 68, 0.18)',
      fill: true,
      tension: 0.35,
    },
  ],
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false,
  },
  plugins: {
    legend: {
      labels: {
        color: '#334155',
      },
    },
  },
  animation: {
    duration: 950,
    easing: 'easeOutCubic',
  },
}
</script>

<template>
  <div class="h-80">
    <Line :data="chartData" :options="options" />
  </div>
</template>
