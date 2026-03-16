<script setup>
import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  Tooltip,
} from 'chart.js'
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'

import { useLocale } from '../composables/useLocale'
import { useUiStore } from '../store/ui'

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend)

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
      label: t('chartIncome'),
      data: props.items.map((item) => fromBase(item.income)),
      backgroundColor: 'rgba(34, 197, 94, 0.7)',
      borderRadius: 8,
      borderSkipped: false,
    },
    {
      label: t('chartExpense'),
      data: props.items.map((item) => fromBase(item.expense)),
      backgroundColor: 'rgba(239, 68, 68, 0.7)',
      borderRadius: 8,
      borderSkipped: false,
    },
  ],
}))

const options = computed(() => {
  const textColor = uiStore.theme === 'dark' ? '#e2e8f0' : '#334155'
  const gridColor = uiStore.theme === 'dark' ? 'rgba(148, 163, 184, 0.16)' : 'rgba(148, 163, 184, 0.25)'

  return {
    responsive: true,
    maintainAspectRatio: false,
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
            const field = context.datasetIndex === 0 ? 'income' : 'expense'
            return `${context.dataset.label}: ${money(row?.[field] || 0)}`
          },
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
    <Bar :data="chartData" :options="options" />
  </div>
</template>
