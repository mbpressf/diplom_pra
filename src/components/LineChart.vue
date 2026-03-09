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

import { useUiStore } from '../store/ui'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend, Filler)

const props = defineProps({
  items: {
    type: Array,
    required: true,
  },
})

const uiStore = useUiStore()

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

const options = computed(() => {
  const textColor = uiStore.theme === 'dark' ? '#e2e8f0' : '#334155'
  const gridColor = uiStore.theme === 'dark' ? 'rgba(148, 163, 184, 0.16)' : 'rgba(148, 163, 184, 0.25)'

  return {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      legend: {
        labels: {
          color: textColor,
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: textColor,
        },
        grid: {
          color: gridColor,
        },
      },
      y: {
        ticks: {
          color: textColor,
        },
        grid: {
          color: gridColor,
        },
      },
    },
    animation: {
      duration: 950,
      easing: 'easeOutCubic',
    },
  }
})
</script>

<template>
  <div class="h-80">
    <Line :data="chartData" :options="options" />
  </div>
</template>
