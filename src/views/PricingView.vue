<script setup>
const plans = [
  {
    name: 'Free',
    price: '0 ₽ / мес',
    badge: 'Для всех пользователей',
    features: [
      'Учёт доходов и расходов',
      'Базовая аналитика и графики',
      'Базовые AI-подсказки',
      'CSV экспорт/импорт',
    ],
    accent: 'border-slate-300/70',
  },
  {
    name: 'Pro',
    price: '249 ₽ / мес',
    badge: 'Расширенный личный режим',
    features: [
      'Персональные AI-сценарии на 30/90 дней',
      'Продвинутые предупреждения о рисках',
      'Приоритетная обработка AI-запросов',
      'История персональных рекомендаций',
    ],
    accent: 'border-brand-500/35',
  },
  {
    name: 'B2B',
    price: '9 900 ₽ / мес + 99 ₽/активного',
    badge: 'Организациям',
    features: [
      'Кабинет организации и командные KPI',
      'Отчёты weekly/monthly',
      'Экспорт CSV/XLSX/PDF',
      'Обезличенная аналитика и риск-скрининг',
    ],
    accent: 'border-emerald-500/35',
  },
]
</script>

<template>
  <section class="space-y-5">
    <article class="bank-hero rounded-[28px] border border-white/50 p-6 shadow-card">
      <h1 class="text-2xl font-semibold tracking-tight text-slate-900">Тарифы</h1>
      <p class="mt-2 max-w-3xl text-sm text-slate-600">
        Базовый режим остаётся бесплатным. Монетизация строится на Pro-функциях и организационных лицензиях.
      </p>
    </article>

    <article class="grid gap-4 md:grid-cols-3">
      <section
        v-for="plan in plans"
        :key="plan.name"
        class="bank-card rounded-[24px] border bg-white/85 p-5 shadow-card"
        :class="plan.accent"
      >
        <p class="text-xs uppercase tracking-[0.16em] text-slate-500">{{ plan.badge }}</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-900">{{ plan.name }}</h2>
        <p class="mt-2 text-lg font-semibold text-slate-800">{{ plan.price }}</p>

        <ul class="mt-4 space-y-2 text-sm text-slate-700">
          <li v-for="feature in plan.features" :key="feature" class="rounded-xl bg-slate-100/70 px-3 py-2">
            {{ feature }}
          </li>
        </ul>
      </section>
    </article>
  </section>
</template>
