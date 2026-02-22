<script setup>
import {
  ArcElement,
  Chart as ChartJS,
  Legend,
  Tooltip,
} from 'chart.js'
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  items: {
    type: Array,
    required: true,
  },
})

const chartData = computed(() => ({
  labels: props.items.map((i) => i.category),
  datasets: [
    {
      data: props.items.map((i) => i.amount),
      backgroundColor: props.items.map((i) => i.color),
      borderWidth: 0,
      hoverOffset: 8,
    },
  ],
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: '#334155',
      },
    },
  },
  animation: {
    duration: 900,
    easing: 'easeOutQuart',
  },
}
</script>

<template>
  <div class="h-80">
    <Doughnut :data="chartData" :options="options" />
  </div>
</template>
