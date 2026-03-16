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

import { useLocale } from '../composables/useLocale'
import { useUiStore } from '../store/ui'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend, Filler)

const props = defineProps({
  items: {
    type: Array,
    required: true,
  },
})

const uiStore = useUiStore()
const { fromBase, money, displayMoney, t } = useLocale()

const chartData = computed(() => ({
  labels: props.items.map((item) => item.label),
  datasets: [
    {
      label: t('analyticsRunningBalance'),
      data: props.items.map((item) => fromBase(item.balance)),
      borderColor: '#0ea5e9',
      backgroundColor: 'rgba(14, 165, 233, 0.16)',
      fill: true,
      tension: 0.22,
      pointRadius: 2,
      pointHoverRadius: 4,
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
      tooltip: {
        callbacks: {
          label(context) {
            const row = props.items[context.dataIndex]
            return `${t('analyticsRunningBalance')}: ${money(row?.balance || 0)}`
          },
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: textColor,
          maxRotation: 0,
          autoSkip: true,
        },
        grid: {
          color: gridColor,
        },
      },
      y: {
        ticks: {
          color: textColor,
          callback(value) {
            return displayMoney(value)
          },
        },
        grid: {
          color: gridColor,
        },
      },
    },
    animation: {
      duration: 850,
      easing: 'easeOutCubic',
    },
  }
})
</script>

<template>
  <div class="h-72">
    <Line :data="chartData" :options="options" />
  </div>
</template>
