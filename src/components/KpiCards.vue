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
    <article class="glass animate-floatIn rounded-[28px] border border-white/20 p-5 shadow-card transition duration-300 hover:-translate-y-1 hover:shadow-2xl">
      <p class="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-300">Доход за выбранный период</p>
      <p class="mt-2 text-2xl font-bold text-income">{{ money(props.summary.total_income) }}</p>
    </article>
    <article class="glass animate-floatIn rounded-[28px] border border-white/20 p-5 shadow-card transition duration-300 hover:-translate-y-1 hover:shadow-2xl">
      <p class="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-300">Расход за выбранный период</p>
      <p class="mt-2 text-2xl font-bold text-expense">{{ money(props.summary.total_expense) }}</p>
    </article>
    <article class="glass animate-floatIn rounded-[28px] border border-white/20 p-5 shadow-card transition duration-300 hover:-translate-y-1 hover:shadow-2xl">
      <p class="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-300">Чистый итог периода</p>
      <p class="mt-2 text-2xl font-bold text-brand-700 dark:text-brand-100">{{ money(props.summary.balance) }}</p>
    </article>
    <article class="glass animate-floatIn rounded-[28px] border border-white/20 p-5 shadow-card transition duration-300 hover:-translate-y-1 hover:shadow-2xl">
      <p class="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-300">После расходов осталось</p>
      <p class="mt-2 text-2xl font-bold text-accent">{{ props.summary.savings_rate }}%</p>
      <p class="mt-2 text-sm text-slate-500 dark:text-slate-400">Это процент дохода, который не был потрачен в выбранном периоде.</p>
    </article>
  </section>
</template>
