<script setup>
import { reactive } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

import { useLocale } from '../composables/useLocale'
import { useAuthStore } from '../store/auth'
import { useFinanceStore } from '../store/finance'
import { useOrgStore } from '../store/orgs'

const authStore = useAuthStore()
const financeStore = useFinanceStore()
const orgStore = useOrgStore()
const router = useRouter()
const { t } = useLocale()

const form = reactive({
  email: '',
  password: '',
})

async function onSubmit() {
  try {
    await authStore.login(form.email, form.password)
    if (authStore.accountType === 'organization') {
      await orgStore.fetchOrganizations()
      router.push('/org')
      return
    }

    try {
      await financeStore.bootstrap()
    } catch {
      // Вход уже успешен; если аналитика временно недоступна, не блокируем переход.
    }
    router.push('/')
  } catch {
    // Ошибка уже сохраняется в store для отображения.
  }
}
</script>

<template>
  <section class="mx-auto mt-10 grid max-w-5xl gap-4 lg:grid-cols-[1.1fr_0.9fr]">
    <article class="bank-hero rounded-[28px] border border-white/55 p-6 shadow-card">
      <p class="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Finpotok enterprise</p>
      <h1 class="mt-3 text-3xl font-semibold tracking-tight text-slate-900">Вход в платформу</h1>
      <p class="mt-3 text-sm leading-6 text-slate-600">
        Для физических лиц доступен персональный кабинет. Для организаций — блок командной аналитики,
        отчётов и экспорта.
      </p>
      <div class="mt-5 grid gap-2 sm:grid-cols-2">
        <div class="rounded-2xl bg-white/80 p-4">
          <p class="text-xs uppercase tracking-[0.14em] text-slate-500">Персональный контур</p>
          <p class="mt-2 text-sm text-slate-700">Операции, аналитика, финансовый сейф, AI-рекомендации.</p>
        </div>
        <div class="rounded-2xl bg-white/80 p-4">
          <p class="text-xs uppercase tracking-[0.14em] text-slate-500">Орг-контур</p>
          <p class="mt-2 text-sm text-slate-700">Командные KPI, weekly/monthly отчёты, CSV/XLSX/PDF.</p>
        </div>
      </div>
    </article>

    <article class="bank-card rounded-[28px] border border-white/65 bg-white/90 p-6 shadow-card">
      <h2 class="text-xl font-semibold text-slate-900">{{ t('loginTitle') }}</h2>

      <form class="mt-5 space-y-3" @submit.prevent="onSubmit">
        <input
          v-model="form.email"
          type="email"
          required
          autocomplete="email"
          :placeholder="t('emailPlaceholder')"
          class="w-full rounded-xl border border-slate-200 bg-white px-3 py-3"
        />
        <input
          v-model="form.password"
          type="password"
          required
          autocomplete="current-password"
          :placeholder="t('passwordPlaceholder')"
          class="w-full rounded-xl border border-slate-200 bg-white px-3 py-3"
        />
        <p v-if="authStore.error" class="text-sm text-red-700">{{ authStore.error }}</p>
        <button :disabled="authStore.loading" class="w-full rounded-xl bg-brand-700 px-4 py-3 font-semibold text-white transition hover:bg-brand-500 disabled:opacity-60">
          {{ t('loginButton') }}
        </button>
      </form>

      <p class="mt-4 text-sm text-slate-600">
        {{ t('noAccount') }}
        <RouterLink to="/register" class="font-semibold text-brand-700 hover:underline">{{ t('registerLink') }}</RouterLink>
      </p>
    </article>
  </section>
</template>
