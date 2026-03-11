<script setup>
import {
  ArcElement,
  Chart as ChartJS,
  Legend,
  Tooltip,
} from 'chart.js'
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'

import { useLocale } from '../composables/useLocale'
import { useUiStore } from '../store/ui'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  items: {
    type: Array,
    required: true,
  },
})

const uiStore = useUiStore()
const { fromBase, money } = useLocale()

const chartData = computed(() => ({
  labels: props.items.map((i) => i.category),
  datasets: [
    {
      data: props.items.map((i) => fromBase(i.amount)),
      backgroundColor: props.items.map((i) => i.color),
      borderWidth: 0,
      hoverOffset: 8,
    },
  ],
}))

const options = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  cutout: '66%',
  plugins: {
    legend: {
      labels: {
        color: uiStore.theme === 'dark' ? '#e2e8f0' : '#334155',
      },
    },
    tooltip: {
      callbacks: {
        label(context) {
          return `${context.label}: ${money(props.items[context.dataIndex]?.amount || 0)}`
        },
      },
    },
  },
  animation: {
    duration: 900,
    easing: 'easeOutQuart',
  },
}))
</script>

<template>
  <div class="h-80">
    <Doughnut :data="chartData" :options="options" />
  </div>
</template>
