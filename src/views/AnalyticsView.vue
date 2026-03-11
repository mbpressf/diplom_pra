<script setup>
import { computed } from 'vue'

import DateFilter from '../components/DateFilter.vue'
import DoughnutChart from '../components/DoughnutChart.vue'
import KpiCards from '../components/KpiCards.vue'
import LineChart from '../components/LineChart.vue'
import SkeletonCard from '../components/SkeletonCard.vue'
import { useLocale } from '../composables/useLocale'
import { useFinanceStore } from '../store/finance'

const financeStore = useFinanceStore()
const { t } = useLocale()

const loading = computed(() => financeStore.loading && !financeStore.ready)

async function applyFilter(payload) {
  await financeStore.setDateRange(payload.startDate, payload.endDate)
}
</script>

<template>
  <section class="space-y-4 sm:space-y-5">
    <article class="glass rounded-[28px] border border-white/20 p-5 shadow-card">
      <h1 class="text-2xl font-semibold tracking-tight text-slate-900 dark:text-slate-50">{{ t('analyticsTitle') }}</h1>
      <p class="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">{{ t('analyticsText') }}</p>
    </article>

    <DateFilter @apply="applyFilter" />

    <div v-if="loading" class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
      <SkeletonCard v-for="item in 4" :key="item" />
    </div>
    <KpiCards v-else :summary="financeStore.summary" />

    <div class="grid grid-cols-1 gap-4 xl:grid-cols-2">
      <article class="glass rounded-[28px] border border-white/20 p-4 shadow-card sm:p-5">
        <div class="mb-4 flex items-center justify-between gap-3">
          <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">{{ t('dashboardCategoryShare') }}</h2>
          <span class="rounded-full border border-white/15 bg-white/10 px-3 py-1 text-xs font-medium text-slate-600 dark:text-slate-300">{{ t('dashboardCategoryHint') }}</span>
        </div>
        <DoughnutChart :items="financeStore.byCategory" />
      </article>
      <article class="glass rounded-[28px] border border-white/20 p-4 shadow-card sm:p-5">
        <div class="mb-4 flex items-center justify-between gap-3">
          <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">{{ t('dashboardMonthlyTrend') }}</h2>
          <span class="rounded-full border border-white/15 bg-white/10 px-3 py-1 text-xs font-medium text-slate-600 dark:text-slate-300">{{ t('dashboardMonthlyHint') }}</span>
        </div>
        <LineChart :items="financeStore.byMonth" />
      </article>
    </div>
  </section>
</template>
