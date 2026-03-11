<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import { useLocale } from '../composables/useLocale'
import DateFilter from '../components/DateFilter.vue'
import TransactionForm from '../components/TransactionForm.vue'
import { useFinanceStore } from '../store/finance'

const financeStore = useFinanceStore()
const importInput = ref(null)
const router = useRouter()
const { t, money, shortDate, uiStore } = useLocale()

const commonCategoryPresets = [
  { names: { ru: 'Зарплата', en: 'Salary' }, aliases: ['зарплата', 'salary'], color: '#22C55E' },
  { names: { ru: 'Подработка', en: 'Side hustle' }, aliases: ['подработка', 'side hustle'], color: '#10B981' },
  { names: { ru: 'Инвестиции', en: 'Investments' }, aliases: ['инвестиции', 'investments'], color: '#0EA5E9' },
  { names: { ru: 'Продукты', en: 'Groceries' }, aliases: ['продукты', 'groceries'], color: '#EF4444' },
  { names: { ru: 'Кафе и рестораны', en: 'Dining out' }, aliases: ['кафе и рестораны', 'dining out'], color: '#F97316' },
  { names: { ru: 'Транспорт', en: 'Transport' }, aliases: ['транспорт', 'transport'], color: '#3B82F6' },
  { names: { ru: 'Жилье', en: 'Housing' }, aliases: ['жилье', 'housing'], color: '#8B5CF6' },
  { names: { ru: 'Коммунальные услуги', en: 'Utilities' }, aliases: ['коммунальные услуги', 'utilities'], color: '#6366F1' },
]

const localizedCommonCategories = computed(() =>
  commonCategoryPresets.map((item) => ({
    name: item.names[uiStore.locale],
    color: item.color,
    aliases: item.aliases,
  })),
)

function typeLabel(type) {
  return type === 'income' ? t('income') : t('expense')
}

async function onSubmit(payload) {
  await financeStore.addTransaction(payload)
}

async function onDelete(id) {
  await financeStore.deleteTransaction(id)
}

async function applyFilter(payload) {
  await financeStore.setDateRange(payload.startDate, payload.endDate)
}

async function exportCsv() {
  await financeStore.exportCsv()
}

async function triggerImport() {
  importInput.value?.click()
}

async function onImport(event) {
  const file = event.target.files?.[0]
  if (!file) return
  await financeStore.importCsv(file)
  event.target.value = ''
}

async function addCommonCategories() {
  const existing = new Set(financeStore.categories.map((item) => item.name.trim().toLowerCase()))
  for (const category of localizedCommonCategories.value) {
    if (!category.aliases.some((alias) => existing.has(alias))) {
      await financeStore.addCategory({ name: category.name, color: category.color })
    }
  }
}
</script>

<template>
  <section class="space-y-5">
    <article class="glass rounded-[28px] border border-white/20 p-5 shadow-card">
      <div class="grid gap-4 lg:grid-cols-[1.2fr_0.8fr] lg:items-center">
        <div>
          <h1 class="text-2xl font-semibold tracking-tight text-slate-900 dark:text-slate-50">{{ t('transactionsTitle') }}</h1>
          <p class="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">
            {{ t('transactionsText') }}
          </p>
        </div>
        <div class="grid gap-3 sm:grid-cols-2">
          <div class="rounded-3xl border border-brand-500/20 bg-brand-500/10 p-4">
            <p class="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-300">{{ t('transactionsCanSpend') }}</p>
            <p class="mt-2 text-xl font-semibold text-brand-700 dark:text-brand-100">{{ money(financeStore.vault.available_to_spend || 0) }}</p>
          </div>
          <div class="rounded-3xl border border-emerald-400/25 bg-emerald-500/10 p-4">
            <p class="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-300">{{ t('transactionsInSafe') }}</p>
            <p class="mt-2 text-xl font-semibold text-accent">{{ money(financeStore.vault.balance || 0) }}</p>
          </div>
        </div>
      </div>
    </article>

    <div class="flex flex-col gap-2 sm:flex-row sm:flex-wrap">
      <button class="rounded-2xl bg-brand-700 px-4 py-3 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:bg-brand-500" @click="exportCsv">{{ t('exportCsv') }}</button>
      <button class="rounded-2xl bg-accent px-4 py-3 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:bg-emerald-600" @click="triggerImport">{{ t('importCsv') }}</button>
      <input ref="importInput" type="file" accept=".csv" class="hidden" @change="onImport" />
    </div>

    <DateFilter @apply="applyFilter" />
    <article v-if="financeStore.categories.length === 0" class="glass rounded-xl2 p-4 shadow-card">
      <h2 class="text-lg font-semibold">{{ t('noCategoriesTitle') }}</h2>
      <p class="mt-1 text-sm text-slate-600 dark:text-slate-300">{{ t('noCategoriesText') }}</p>
      <div class="mt-3 flex flex-wrap gap-2">
        <button class="rounded-lg bg-accent px-4 py-2 text-sm font-semibold text-white transition hover:bg-emerald-600" @click="addCommonCategories">
          {{ t('addCommonCategories') }}
        </button>
        <button class="rounded-lg border border-softgray px-4 py-2 text-sm font-semibold transition hover:bg-white dark:hover:bg-slate-800" @click="router.push('/categories')">
          {{ t('goToCategories') }}
        </button>
      </div>
    </article>
    <TransactionForm v-else :categories="financeStore.categories" @submit="onSubmit" />

    <div class="grid gap-3 md:hidden">
      <article
        v-for="item in financeStore.transactions"
        :key="item.id"
        class="glass rounded-[24px] border border-white/20 p-4 shadow-card"
      >
        <div class="flex items-start justify-between gap-3">
          <div>
            <p class="text-sm font-semibold text-slate-900 dark:text-slate-50">{{ item.category?.name }}</p>
            <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">{{ shortDate(item.date) }}</p>
          </div>
          <span :class="item.type === 'income' ? 'text-income' : 'text-expense'" class="text-sm font-semibold">{{ typeLabel(item.type) }}</span>
        </div>
        <p class="mt-3 text-sm text-slate-600 dark:text-slate-300">{{ item.description || t('noDescription') }}</p>
        <div class="mt-4 flex items-center justify-between gap-3">
          <p class="text-lg font-semibold text-slate-900 dark:text-slate-50">{{ money(item.amount) }}</p>
          <button class="rounded-xl bg-red-500/10 px-3 py-2 text-sm font-medium text-expense transition hover:bg-red-500/20" @click="onDelete(item.id)">{{ t('delete') }}</button>
        </div>
      </article>
    </div>

    <article class="glass hidden overflow-hidden rounded-[28px] border border-white/20 shadow-card md:block">
      <table class="min-w-full text-sm">
        <thead class="bg-slate-200/50 dark:bg-slate-800/50">
          <tr>
            <th class="px-4 py-3 text-left">{{ t('date') }}</th>
            <th class="px-4 py-3 text-left">{{ t('type') }}</th>
            <th class="px-4 py-3 text-left">{{ t('category') }}</th>
            <th class="px-4 py-3 text-left">{{ t('description') }}</th>
            <th class="px-4 py-3 text-left">{{ t('amount') }}</th>
            <th class="px-4 py-3"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in financeStore.transactions" :key="item.id" class="border-t border-slate-200/70 transition hover:bg-white/50 dark:border-slate-700 dark:hover:bg-slate-800/60">
            <td class="px-4 py-3">{{ shortDate(item.date) }}</td>
            <td class="px-4 py-3">
              <span :class="item.type === 'income' ? 'text-income' : 'text-expense'" class="font-semibold">{{ typeLabel(item.type) }}</span>
            </td>
            <td class="px-4 py-3">{{ item.category?.name }}</td>
            <td class="px-4 py-3">{{ item.description || t('noDescription') }}</td>
            <td class="px-4 py-3 font-semibold">{{ money(item.amount) }}</td>
            <td class="px-4 py-3 text-right">
              <button class="rounded-md px-2 py-1 text-expense transition hover:bg-red-100 dark:hover:bg-red-950" @click="onDelete(item.id)">{{ t('delete') }}</button>
            </td>
          </tr>
        </tbody>
      </table>
    </article>
  </section>
</template>
