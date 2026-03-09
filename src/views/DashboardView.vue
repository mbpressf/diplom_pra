<script setup>
import { computed } from 'vue'

import DateFilter from '../components/DateFilter.vue'
import DoughnutChart from '../components/DoughnutChart.vue'
import KpiCards from '../components/KpiCards.vue'
import LineChart from '../components/LineChart.vue'
import SkeletonCard from '../components/SkeletonCard.vue'
import VaultPanel from '../components/VaultPanel.vue'
import { useFinanceStore } from '../store/finance'

const financeStore = useFinanceStore()

const loading = computed(() => financeStore.loading && !financeStore.ready)
const budgetHealthText = computed(() => {
  if (financeStore.vault.available_to_spend < 0) {
    return 'Свободный баланс ушел в минус. Стоит вернуть часть денег из сейфа или снизить расходы.'
  }
  if (financeStore.vault.available_to_spend < 5000) {
    return 'Свободных денег немного. Сейф уже помогает держать дисциплину, но запас на месяц пока небольшой.'
  }
  return 'Баланс выглядит устойчиво: есть свободные деньги и отдельный накопительный резерв.'
})
const capitalEquationText = computed(() => {
  const format = new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' })
  return `${format.format(financeStore.vault.balance || 0)} + ${format.format(financeStore.vault.available_to_spend || 0)} = ${format.format(financeStore.vault.net_balance || 0)}`
})

async function applyFilter(payload) {
  await financeStore.setDateRange(payload.startDate, payload.endDate)
}
</script>

<template>
  <section class="space-y-4 sm:space-y-5">
    <article class="glass dashboard-hero relative overflow-hidden rounded-[30px] border border-white/15 p-5 shadow-card sm:p-6">
      <div class="absolute inset-y-0 right-0 hidden w-1/3 bg-gradient-to-l from-cyan-400/15 via-emerald-400/10 to-transparent lg:block"></div>
      <div class="relative z-[1] grid gap-5 lg:grid-cols-[1.3fr_0.7fr] lg:items-end">
        <div class="space-y-3">
          <div class="inline-flex items-center rounded-full border border-white/15 bg-white/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-slate-700 dark:text-slate-300">
            Финансовая карта
          </div>
          <div>
            <h1 class="display-type text-2xl font-semibold tracking-tight text-slate-950 dark:text-slate-50 sm:text-4xl">
              Общий капитал виден сразу, а накопления отделены от повседневных трат.
            </h1>
            <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-600 dark:text-slate-300">
              Здесь две логики одновременно: текущие деньги сейчас и финансовая статистика за выбранный период. Сейф всегда показывает текущую картину, а KPI ниже относятся к фильтру по датам.
            </p>
          </div>
          <div class="rounded-3xl border border-white/15 bg-slate-950/8 p-3.5 dark:bg-white/5 sm:p-4">
            <p class="text-sm font-medium text-slate-700 dark:text-slate-200">Как программа считает деньги</p>
            <p class="mt-2 text-base font-semibold text-slate-900 dark:text-slate-100">{{ capitalEquationText }}</p>
            <p class="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">{{ budgetHealthText }}</p>
          </div>
        </div>

        <div class="hidden gap-3 lg:grid">
          <div class="rounded-3xl border border-white/15 bg-white/68 p-4 dark:bg-slate-950/38">
            <p class="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-400">Общий капитал сейчас</p>
            <p class="mt-2 text-xl font-semibold text-slate-900 dark:text-slate-50 sm:text-2xl">
              {{ new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(financeStore.vault.net_balance || 0) }}
            </p>
          </div>
          <div class="rounded-3xl border border-emerald-400/25 bg-emerald-500/10 p-4">
            <p class="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-300">В накоплениях</p>
            <p class="mt-2 text-xl font-semibold text-accent sm:text-2xl">
              {{ new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(financeStore.vault.balance || 0) }}
            </p>
          </div>
          <div class="rounded-3xl border border-brand-500/20 bg-brand-500/10 p-4">
            <p class="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-300">Свободно сейчас</p>
            <p class="mt-2 text-xl font-semibold text-brand-700 dark:text-brand-100 sm:text-2xl">
              {{ new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(financeStore.vault.available_to_spend || 0) }}
            </p>
          </div>
        </div>
      </div>
    </article>

    <VaultPanel :vault="financeStore.vault" />

    <DateFilter @apply="applyFilter" />

    <div v-if="loading" class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
      <SkeletonCard v-for="item in 4" :key="item" />
    </div>
    <KpiCards v-else :summary="financeStore.summary" />

    <div class="grid grid-cols-1 gap-4 xl:grid-cols-2">
      <article class="glass rounded-[28px] border border-white/20 p-4 shadow-card sm:p-5">
        <div class="mb-4 flex items-center justify-between gap-3">
          <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">Распределение по категориям</h2>
          <span class="rounded-full border border-white/15 bg-white/10 px-3 py-1 text-xs font-medium text-slate-600 dark:text-slate-300">Куда уходят деньги</span>
        </div>
        <DoughnutChart :items="financeStore.byCategory" />
      </article>
      <article class="glass rounded-[28px] border border-white/20 p-4 shadow-card sm:p-5">
        <div class="mb-4 flex items-center justify-between gap-3">
          <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">Динамика по месяцам</h2>
          <span class="rounded-full border border-white/15 bg-white/10 px-3 py-1 text-xs font-medium text-slate-600 dark:text-slate-300">Темп доходов и расходов</span>
        </div>
        <LineChart :items="financeStore.byMonth" />
      </article>
    </div>
  </section>
</template>
