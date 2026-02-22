<script setup>
const props = defineProps({
  summary: {
    type: Object,
    required: true,
  },
})

function money(value) {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    maximumFractionDigits: 2,
  }).format(value || 0)
}
</script>

<template>
  <section class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
    <article class="glass animate-floatIn rounded-xl2 p-5 shadow-card transition hover:-translate-y-1">
      <p class="text-sm text-slate-500 dark:text-slate-300">Общий доход</p>
      <p class="mt-2 text-2xl font-bold text-income">{{ money(props.summary.total_income) }}</p>
    </article>
    <article class="glass animate-floatIn rounded-xl2 p-5 shadow-card transition hover:-translate-y-1">
      <p class="text-sm text-slate-500 dark:text-slate-300">Общий расход</p>
      <p class="mt-2 text-2xl font-bold text-expense">{{ money(props.summary.total_expense) }}</p>
    </article>
    <article class="glass animate-floatIn rounded-xl2 p-5 shadow-card transition hover:-translate-y-1">
      <p class="text-sm text-slate-500 dark:text-slate-300">Баланс</p>
      <p class="mt-2 text-2xl font-bold text-brand-700 dark:text-brand-100">{{ money(props.summary.balance) }}</p>
    </article>
    <article class="glass animate-floatIn rounded-xl2 p-5 shadow-card transition hover:-translate-y-1">
      <p class="text-sm text-slate-500 dark:text-slate-300">Процент экономии</p>
      <p class="mt-2 text-2xl font-bold text-accent">{{ props.summary.savings_rate }}%</p>
    </article>
  </section>
</template>
