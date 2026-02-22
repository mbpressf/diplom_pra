<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import DateFilter from '../components/DateFilter.vue'
import TransactionForm from '../components/TransactionForm.vue'
import { useFinanceStore } from '../store/finance'

const financeStore = useFinanceStore()
const importInput = ref(null)
const router = useRouter()

const commonCategories = [
  { name: 'Зарплата', color: '#22C55E' },
  { name: 'Подработка', color: '#10B981' },
  { name: 'Инвестиции', color: '#0EA5E9' },
  { name: 'Продукты', color: '#EF4444' },
  { name: 'Кафе и рестораны', color: '#F97316' },
  { name: 'Транспорт', color: '#3B82F6' },
  { name: 'Жилье', color: '#8B5CF6' },
  { name: 'Коммунальные услуги', color: '#6366F1' },
]

function formatMoney(value) {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(value)
}

function typeLabel(type) {
  return type === 'income' ? 'Доход' : 'Расход'
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
  for (const category of commonCategories) {
    if (!existing.has(category.name.trim().toLowerCase())) {
      await financeStore.addCategory(category)
    }
  }
}
</script>

<template>
  <section class="space-y-5">
    <div class="flex flex-wrap gap-2">
      <button class="rounded-lg bg-brand-700 px-4 py-2 text-sm font-semibold text-white transition hover:bg-brand-500" @click="exportCsv">Экспорт CSV</button>
      <button class="rounded-lg bg-accent px-4 py-2 text-sm font-semibold text-white transition hover:bg-emerald-600" @click="triggerImport">Импорт CSV</button>
      <input ref="importInput" type="file" accept=".csv" class="hidden" @change="onImport" />
    </div>

    <DateFilter @apply="applyFilter" />
    <article v-if="financeStore.categories.length === 0" class="glass rounded-xl2 p-4 shadow-card">
      <h2 class="text-lg font-semibold">Нет категорий</h2>
      <p class="mt-1 text-sm text-slate-600 dark:text-slate-300">Сначала создайте хотя бы одну категорию, чтобы добавлять доходы и расходы.</p>
      <div class="mt-3 flex flex-wrap gap-2">
        <button class="rounded-lg bg-accent px-4 py-2 text-sm font-semibold text-white transition hover:bg-emerald-600" @click="addCommonCategories">
          Добавить частые категории
        </button>
        <button class="rounded-lg border border-softgray px-4 py-2 text-sm font-semibold transition hover:bg-white dark:hover:bg-slate-800" @click="router.push('/categories')">
          Перейти в категории
        </button>
      </div>
    </article>
    <TransactionForm v-else :categories="financeStore.categories" @submit="onSubmit" />

    <article class="glass overflow-hidden rounded-xl2 shadow-card">
      <table class="min-w-full text-sm">
        <thead class="bg-slate-200/50 dark:bg-slate-800/50">
          <tr>
            <th class="px-4 py-3 text-left">Дата</th>
            <th class="px-4 py-3 text-left">Тип</th>
            <th class="px-4 py-3 text-left">Категория</th>
            <th class="px-4 py-3 text-left">Описание</th>
            <th class="px-4 py-3 text-left">Сумма</th>
            <th class="px-4 py-3"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in financeStore.transactions" :key="item.id" class="border-t border-slate-200/70 transition hover:bg-white/50 dark:border-slate-700 dark:hover:bg-slate-800/60">
            <td class="px-4 py-3">{{ item.date }}</td>
            <td class="px-4 py-3">
              <span :class="item.type === 'income' ? 'text-income' : 'text-expense'" class="font-semibold">{{ typeLabel(item.type) }}</span>
            </td>
            <td class="px-4 py-3">{{ item.category?.name }}</td>
            <td class="px-4 py-3">{{ item.description || '-' }}</td>
            <td class="px-4 py-3 font-semibold">{{ formatMoney(item.amount) }}</td>
            <td class="px-4 py-3 text-right">
              <button class="rounded-md px-2 py-1 text-expense transition hover:bg-red-100 dark:hover:bg-red-950" @click="onDelete(item.id)">Удалить</button>
            </td>
          </tr>
        </tbody>
      </table>
    </article>
  </section>
</template>
