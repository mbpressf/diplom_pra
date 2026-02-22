<script setup>
import { computed } from 'vue'

import DateFilter from '../components/DateFilter.vue'
import DoughnutChart from '../components/DoughnutChart.vue'
import KpiCards from '../components/KpiCards.vue'
import LineChart from '../components/LineChart.vue'
import SkeletonCard from '../components/SkeletonCard.vue'
import { useFinanceStore } from '../store/finance'

const financeStore = useFinanceStore()

const loading = computed(() => financeStore.loading && !financeStore.ready)

async function applyFilter(payload) {
  await financeStore.setDateRange(payload.startDate, payload.endDate)
}
</script>

<template>
  <section class="space-y-5">
    <DateFilter @apply="applyFilter" />

    <div v-if="loading" class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
      <SkeletonCard v-for="item in 4" :key="item" />
    </div>
    <KpiCards v-else :summary="financeStore.summary" />

    <div class="grid grid-cols-1 gap-5 xl:grid-cols-2">
      <article class="glass rounded-xl2 p-5 shadow-card">
        <h2 class="mb-4 text-lg font-semibold">Распределение по категориям</h2>
        <DoughnutChart :items="financeStore.byCategory" />
      </article>
      <article class="glass rounded-xl2 p-5 shadow-card">
        <h2 class="mb-4 text-lg font-semibold">Динамика по месяцам</h2>
        <LineChart :items="financeStore.byMonth" />
      </article>
    </div>
  </section>
</template>
