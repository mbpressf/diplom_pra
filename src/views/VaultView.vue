<script setup>
import { useLocale } from '../composables/useLocale'
import VaultPanel from '../components/VaultPanel.vue'
import { useFinanceStore } from '../store/finance'

const financeStore = useFinanceStore()
const { t } = useLocale()
</script>

<template>
  <section class="space-y-4 sm:space-y-5">
    <article class="glass rounded-[28px] border border-white/20 p-5 shadow-card">
      <h1 class="text-2xl font-semibold tracking-tight text-slate-900 dark:text-slate-50">{{ t('vaultPageTitle') }}</h1>
      <p class="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">{{ t('vaultPageText') }}</p>
    </article>
    <VaultPanel :vault="financeStore.vault" />
  </section>
</template>
