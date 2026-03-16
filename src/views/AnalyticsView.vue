<script setup>
import { computed, ref } from 'vue'

import CategoryBarChart from '../components/CategoryBarChart.vue'
import CumulativeBalanceChart from '../components/CumulativeBalanceChart.vue'
import DateFilter from '../components/DateFilter.vue'
import DoughnutChart from '../components/DoughnutChart.vue'
import KpiCards from '../components/KpiCards.vue'
import PeriodTrendChart from '../components/PeriodTrendChart.vue'
import SkeletonCard from '../components/SkeletonCard.vue'
import WeekdayFlowChart from '../components/WeekdayFlowChart.vue'
import { useLocale } from '../composables/useLocale'
import { useFinanceStore } from '../store/finance'

const financeStore = useFinanceStore()
const { t, money, uiStore } = useLocale()

const granularity = ref('week')

const loading = computed(() => financeStore.loading && !financeStore.ready)

const granularityOptions = computed(() => [
  { value: 'day', label: t('granularityDay') },
  { value: 'week', label: t('granularityWeek') },
  { value: 'month', label: t('granularityMonth') },
])

const localeCode = computed(() => (uiStore.locale === 'en' ? 'en-US' : 'ru-RU'))

const sortedTransactions = computed(() => {
  return [...financeStore.transactions].sort((a, b) => String(a.date).localeCompare(String(b.date)))
})

const periodSeries = computed(() => {
  const buckets = new Map()

  for (const tx of sortedTransactions.value) {
    const amount = Number(tx.amount) || 0
    const date = parseDate(tx.date)
    if (!date) continue

    const bucket = getBucketMeta(date, granularity.value)
    const previous = buckets.get(bucket.key) || {
      key: bucket.key,
      start: bucket.start,
      income: 0,
      expense: 0,
      balance: 0,
      count: 0,
    }

    if (tx.type === 'income') {
      previous.income += amount
    } else {
      previous.expense += amount
    }

    previous.balance = previous.income - previous.expense
    previous.count += 1
    buckets.set(bucket.key, previous)
  }

  return [...buckets.values()]
    .sort((a, b) => a.start - b.start)
    .map((row) => ({
      ...row,
      label: formatBucketLabel(row.start, granularity.value, localeCode.value),
    }))
})

const cumulativeSeries = computed(() => {
  const deltaByDay = new Map()

  for (const tx of sortedTransactions.value) {
    const amount = Number(tx.amount) || 0
    const date = parseDate(tx.date)
    if (!date) continue
    const key = toIsoDay(date)
    const signed = tx.type === 'income' ? amount : -amount
    deltaByDay.set(key, (deltaByDay.get(key) || 0) + signed)
  }

  const keys = [...deltaByDay.keys()].sort()
  let running = 0

  return keys.map((key) => {
    running += deltaByDay.get(key) || 0
    const date = parseDate(key)
    return {
      label: formatBucketLabel(date, 'day', localeCode.value),
      balance: running,
    }
  })
})

const weekdayFlow = computed(() => {
  const labels = [
    t('weekdayMon'),
    t('weekdayTue'),
    t('weekdayWed'),
    t('weekdayThu'),
    t('weekdayFri'),
    t('weekdaySat'),
    t('weekdaySun'),
  ]
  const result = labels.map((label) => ({ label, income: 0, expense: 0 }))

  for (const tx of sortedTransactions.value) {
    const amount = Number(tx.amount) || 0
    const date = parseDate(tx.date)
    if (!date) continue
    const dayIndex = (date.getDay() + 6) % 7
    if (tx.type === 'income') result[dayIndex].income += amount
    else result[dayIndex].expense += amount
  }

  return result
})

const topExpenseCategories = computed(() => {
  return buildTopCategories(sortedTransactions.value, 'expense')
})

const topIncomeCategories = computed(() => {
  return buildTopCategories(sortedTransactions.value, 'income')
})

const averageIncomePerBucket = computed(() => {
  const count = periodSeries.value.length || 1
  return financeStore.summary.total_income / count
})

const averageExpensePerBucket = computed(() => {
  const count = periodSeries.value.length || 1
  return financeStore.summary.total_expense / count
})

const bestPeriod = computed(() => {
  if (!periodSeries.value.length) return null
  return periodSeries.value.reduce((best, row) => (row.balance > best.balance ? row : best), periodSeries.value[0])
})

const worstPeriod = computed(() => {
  if (!periodSeries.value.length) return null
  return periodSeries.value.reduce((worst, row) => (row.balance < worst.balance ? row : worst), periodSeries.value[0])
})

async function applyFilter(payload) {
  await financeStore.setDateRange(payload.startDate, payload.endDate)
}

function parseDate(value) {
  if (!value) return null
  const date = new Date(`${value}T00:00:00`)
  if (Number.isNaN(date.getTime())) return null
  return date
}

function toIsoDay(date) {
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
}

function getStartOfWeek(date) {
  const copy = new Date(date)
  copy.setHours(0, 0, 0, 0)
  const diff = (copy.getDay() + 6) % 7
  copy.setDate(copy.getDate() - diff)
  return copy
}

function getBucketMeta(date, mode) {
  if (mode === 'day') {
    const start = new Date(date)
    start.setHours(0, 0, 0, 0)
    return { key: toIsoDay(start), start }
  }

  if (mode === 'week') {
    const start = getStartOfWeek(date)
    return { key: toIsoDay(start), start }
  }

  const start = new Date(date.getFullYear(), date.getMonth(), 1)
  return {
    key: `${start.getFullYear()}-${String(start.getMonth() + 1).padStart(2, '0')}`,
    start,
  }
}

function formatBucketLabel(date, mode, locale) {
  if (!date) return ''

  if (mode === 'day') {
    return new Intl.DateTimeFormat(locale, { day: '2-digit', month: 'short' }).format(date)
  }

  if (mode === 'week') {
    const weekStart = new Date(date)
    const weekEnd = new Date(date)
    weekEnd.setDate(weekEnd.getDate() + 6)
    const startLabel = new Intl.DateTimeFormat(locale, { day: '2-digit', month: 'short' }).format(weekStart)
    const endLabel = new Intl.DateTimeFormat(locale, { day: '2-digit', month: 'short' }).format(weekEnd)
    return `${startLabel} - ${endLabel}`
  }

  return new Intl.DateTimeFormat(locale, { month: 'short', year: 'numeric' }).format(date)
}

function buildTopCategories(transactions, txType) {
  const map = new Map()

  for (const tx of transactions) {
    if (tx.type !== txType) continue
    const amount = Number(tx.amount) || 0
    const categoryName = tx.category?.name || t('category')
    const prev = map.get(categoryName) || {
      category: categoryName,
      amount: 0,
      color: tx.category?.color || (txType === 'income' ? '#22c55e' : '#ef4444'),
    }
    prev.amount += amount
    map.set(categoryName, prev)
  }

  return [...map.values()].sort((a, b) => b.amount - a.amount).slice(0, 7)
}
</script>

<template>
  <section class="space-y-4 sm:space-y-5">
    <article class="glass rounded-[28px] border border-white/20 p-5 shadow-card">
      <h1 class="text-2xl font-semibold tracking-tight text-slate-900 dark:text-slate-50">{{ t('analyticsTitleExtended') }}</h1>
      <p class="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">{{ t('analyticsTextExtended') }}</p>
    </article>

    <DateFilter @apply="applyFilter" />

    <article class="glass rounded-[24px] border border-white/20 p-4 shadow-card">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <p class="text-sm font-medium text-slate-700 dark:text-slate-200">{{ t('analyticsGranularityLabel') }}</p>
        <div class="inline-flex rounded-full border border-white/15 bg-white/55 p-1 dark:bg-slate-950/35">
          <button
            v-for="option in granularityOptions"
            :key="option.value"
            type="button"
            class="rounded-full px-4 py-2 text-sm font-semibold transition"
            :class="granularity === option.value ? 'bg-brand-700 text-white shadow-[0_10px_24px_rgba(37,99,235,0.28)]' : 'text-slate-700 hover:bg-white dark:text-slate-200 dark:hover:bg-slate-800'"
            @click="granularity = option.value"
          >
            {{ option.label }}
          </button>
        </div>
      </div>
    </article>

    <div v-if="loading" class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
      <SkeletonCard v-for="item in 4" :key="item" />
    </div>
    <KpiCards v-else :summary="financeStore.summary" />

    <article class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <div class="glass rounded-[24px] border border-white/20 p-4 shadow-card">
        <p class="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-300">{{ t('analyticsAvgIncome') }}</p>
        <p class="mt-2 text-xl font-semibold text-income">{{ money(averageIncomePerBucket) }}</p>
      </div>
      <div class="glass rounded-[24px] border border-white/20 p-4 shadow-card">
        <p class="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-300">{{ t('analyticsAvgExpense') }}</p>
        <p class="mt-2 text-xl font-semibold text-expense">{{ money(averageExpensePerBucket) }}</p>
      </div>
      <div class="glass rounded-[24px] border border-white/20 p-4 shadow-card">
        <p class="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-300">{{ t('analyticsBestPeriod') }}</p>
        <p class="mt-2 text-sm font-semibold text-slate-900 dark:text-slate-100">
          {{ bestPeriod ? `${bestPeriod.label} • ${money(bestPeriod.balance)}` : '—' }}
        </p>
      </div>
      <div class="glass rounded-[24px] border border-white/20 p-4 shadow-card">
        <p class="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-300">{{ t('analyticsWorstPeriod') }}</p>
        <p class="mt-2 text-sm font-semibold text-slate-900 dark:text-slate-100">
          {{ worstPeriod ? `${worstPeriod.label} • ${money(worstPeriod.balance)}` : '—' }}
        </p>
      </div>
    </article>

    <article class="glass rounded-[28px] border border-white/20 p-4 shadow-card sm:p-5">
      <div class="mb-4 flex items-center justify-between gap-3">
        <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">{{ t('analyticsTrendByPeriod') }}</h2>
        <span class="rounded-full border border-white/15 bg-white/10 px-3 py-1 text-xs font-medium text-slate-600 dark:text-slate-300">{{ t('analyticsNetFlow') }}</span>
      </div>
      <PeriodTrendChart :items="periodSeries" />
    </article>

    <div class="grid grid-cols-1 gap-4 xl:grid-cols-2">
      <article class="glass rounded-[28px] border border-white/20 p-4 shadow-card sm:p-5">
        <div class="mb-4 flex items-center justify-between gap-3">
          <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">{{ t('analyticsRunningBalance') }}</h2>
          <span class="rounded-full border border-white/15 bg-white/10 px-3 py-1 text-xs font-medium text-slate-600 dark:text-slate-300">{{ t('analyticsBalanceDynamics') }}</span>
        </div>
        <CumulativeBalanceChart :items="cumulativeSeries" />
      </article>
      <article class="glass rounded-[28px] border border-white/20 p-4 shadow-card sm:p-5">
        <div class="mb-4 flex items-center justify-between gap-3">
          <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">{{ t('dashboardCategoryShare') }}</h2>
          <span class="rounded-full border border-white/15 bg-white/10 px-3 py-1 text-xs font-medium text-slate-600 dark:text-slate-300">{{ t('dashboardCategoryHint') }}</span>
        </div>
        <DoughnutChart :items="financeStore.byCategory" />
      </article>
    </div>

    <div class="grid grid-cols-1 gap-4 xl:grid-cols-2">
      <article class="glass rounded-[28px] border border-white/20 p-4 shadow-card sm:p-5">
        <div class="mb-4 flex items-center justify-between gap-3">
          <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">{{ t('analyticsWeekdayFlow') }}</h2>
          <span class="rounded-full border border-white/15 bg-white/10 px-3 py-1 text-xs font-medium text-slate-600 dark:text-slate-300">{{ t('analyticsPatternHint') }}</span>
        </div>
        <WeekdayFlowChart :items="weekdayFlow" />
      </article>
      <article class="glass rounded-[28px] border border-white/20 p-4 shadow-card sm:p-5">
        <div class="mb-4 flex items-center justify-between gap-3">
          <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">{{ t('analyticsTopExpenseCategories') }}</h2>
          <span class="rounded-full border border-white/15 bg-white/10 px-3 py-1 text-xs font-medium text-slate-600 dark:text-slate-300">{{ t('dashboardCategoryHint') }}</span>
        </div>
        <CategoryBarChart :items="topExpenseCategories" />
      </article>
    </div>

    <article class="glass rounded-[28px] border border-white/20 p-4 shadow-card sm:p-5">
      <div class="mb-4 flex items-center justify-between gap-3">
        <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">{{ t('analyticsTopIncomeCategories') }}</h2>
        <span class="rounded-full border border-white/15 bg-white/10 px-3 py-1 text-xs font-medium text-slate-600 dark:text-slate-300">{{ t('analyticsIncomeHint') }}</span>
      </div>
      <CategoryBarChart :items="topIncomeCategories" />
    </article>
  </section>
</template>
