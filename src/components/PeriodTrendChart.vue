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
const { t, fromBase, money, displayMoney } = useLocale()

const chartData = computed(() => ({
  labels: props.items.map((item) => item.label),
  datasets: [
    {
      label: t('chartIncome'),
      data: props.items.map((item) => fromBase(item.income)),
      borderColor: '#22c55e',
      backgroundColor: 'rgba(34, 197, 94, 0.14)',
      pointRadius: 2.5,
      pointHoverRadius: 4,
      fill: true,
      tension: 0.3,
    },
    {
      label: t('chartExpense'),
      data: props.items.map((item) => fromBase(item.expense)),
      borderColor: '#ef4444',
      backgroundColor: 'rgba(239, 68, 68, 0.12)',
      pointRadius: 2.5,
      pointHoverRadius: 4,
      fill: true,
      tension: 0.3,
    },
    {
      label: t('analyticsNetFlow'),
      data: props.items.map((item) => fromBase(item.balance)),
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59, 130, 246, 0.09)',
      borderDash: [8, 4],
      pointRadius: 2,
      pointHoverRadius: 4,
      fill: false,
      tension: 0.2,
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
            if (!row) return ''
            const field = context.datasetIndex === 0 ? 'income' : context.datasetIndex === 1 ? 'expense' : 'balance'
            return `${context.dataset.label}: ${money(row[field])}`
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
      duration: 900,
      easing: 'easeOutQuart',
    },
  }
})
</script>

<template>
  <div class="h-80">
    <Line :data="chartData" :options="options" />
  </div>
</template>
