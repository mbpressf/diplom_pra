<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

import { useLocale } from '../composables/useLocale'
import { useFinanceStore } from '../store/finance'

const financeStore = useFinanceStore()
const { t, money } = useLocale()

const budgetHealthText = computed(() => {
  if (financeStore.vault.available_to_spend < 0) {
    return t('budgetHealthNegative')
  }
  if (financeStore.vault.available_to_spend < 5000) {
    return t('budgetHealthLow')
  }
  return t('budgetHealthGood')
})
</script>

<template>
  <section class="space-y-4 sm:space-y-5">
    <article class="glass dashboard-hero relative overflow-hidden rounded-[30px] border border-white/15 p-5 shadow-card sm:p-6">
      <div class="absolute inset-y-0 right-0 hidden w-1/3 bg-gradient-to-l from-cyan-400/15 via-emerald-400/10 to-transparent lg:block"></div>
      <div class="relative z-[1] space-y-3">
        <div class="inline-flex items-center rounded-full border border-white/15 bg-white/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-slate-700 dark:text-slate-300">
          {{ t('overviewBadge') }}
        </div>
        <h1 class="display-type text-2xl font-semibold tracking-tight text-slate-950 dark:text-slate-50 sm:text-4xl">
          {{ t('overviewTitle') }}
        </h1>
        <p class="max-w-3xl text-sm leading-6 text-slate-600 dark:text-slate-300">
          {{ t('overviewText') }}
        </p>
      </div>
    </article>

    <article class="glass rounded-[28px] border border-white/20 p-4 shadow-card sm:p-5">
      <div class="grid gap-3 sm:grid-cols-3">
        <div class="rounded-3xl border border-white/15 bg-white/68 p-4 dark:bg-slate-950/38">
          <p class="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-400">{{ t('dashboardCapitalNow') }}</p>
          <p class="mt-2 text-xl font-semibold text-slate-900 dark:text-slate-50">{{ money(financeStore.vault.net_balance || 0) }}</p>
        </div>
        <div class="rounded-3xl border border-emerald-400/25 bg-emerald-500/10 p-4">
          <p class="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-300">{{ t('dashboardInSavings') }}</p>
          <p class="mt-2 text-xl font-semibold text-accent">{{ money(financeStore.vault.balance || 0) }}</p>
        </div>
        <div class="rounded-3xl border border-brand-500/20 bg-brand-500/10 p-4">
          <p class="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-300">{{ t('dashboardFreeNow') }}</p>
          <p class="mt-2 text-xl font-semibold text-brand-700 dark:text-brand-100">{{ money(financeStore.vault.available_to_spend || 0) }}</p>
        </div>
      </div>
      <p class="mt-4 text-sm leading-6 text-slate-600 dark:text-slate-300">{{ budgetHealthText }}</p>
    </article>

    <article class="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
      <RouterLink to="/analytics" class="glass rounded-[24px] border border-white/20 p-4 shadow-card transition hover:-translate-y-1">
        <p class="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-300">{{ t('overviewCardAnalyticsTitle') }}</p>
        <p class="mt-2 text-sm text-slate-700 dark:text-slate-200">{{ t('overviewCardAnalyticsText') }}</p>
      </RouterLink>
      <RouterLink to="/vault" class="glass rounded-[24px] border border-white/20 p-4 shadow-card transition hover:-translate-y-1">
        <p class="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-300">{{ t('overviewCardVaultTitle') }}</p>
        <p class="mt-2 text-sm text-slate-700 dark:text-slate-200">{{ t('overviewCardVaultText') }}</p>
      </RouterLink>
      <RouterLink to="/transactions" class="glass rounded-[24px] border border-white/20 p-4 shadow-card transition hover:-translate-y-1">
        <p class="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-300">{{ t('overviewCardTransactionsTitle') }}</p>
        <p class="mt-2 text-sm text-slate-700 dark:text-slate-200">{{ t('overviewCardTransactionsText') }}</p>
      </RouterLink>
      <RouterLink to="/categories" class="glass rounded-[24px] border border-white/20 p-4 shadow-card transition hover:-translate-y-1">
        <p class="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-300">{{ t('overviewCardCategoriesTitle') }}</p>
        <p class="mt-2 text-sm text-slate-700 dark:text-slate-200">{{ t('overviewCardCategoriesText') }}</p>
      </RouterLink>
    </article>
  </section>
</template>
