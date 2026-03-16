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
  account_type: 'individual',
  organization_name: '',
  organization_industry: '',
})

async function onSubmit() {
  try {
    await authStore.register({
      email: form.email,
      password: form.password,
      account_type: form.account_type,
      organization_name: form.account_type === 'organization' ? form.organization_name : undefined,
      organization_industry: form.account_type === 'organization' ? form.organization_industry : undefined,
    })

    if (authStore.accountType === 'organization') {
      await orgStore.fetchOrganizations()
      router.push('/org')
      return
    }

    try {
      await financeStore.bootstrap()
    } catch {
      // Регистрация уже прошла успешно; если аналитика временно недоступна, не блокируем вход.
    }
    router.push('/')
  } catch {
    // Ошибка уже хранится в store.
  }
}
</script>

<template>
  <section class="mx-auto mt-10 max-w-3xl space-y-4">
    <article class="bank-hero rounded-[28px] border border-white/55 p-6 shadow-card">
      <h1 class="text-2xl font-semibold tracking-tight text-slate-900">{{ t('registerTitle') }}</h1>
      <p class="mt-2 text-sm text-slate-600">Выберите тип аккаунта: личный кабинет или организационный контур.</p>
    </article>

    <article class="bank-card rounded-[28px] border border-white/65 bg-white/90 p-6 shadow-card">
      <form class="space-y-4" @submit.prevent="onSubmit">
        <div class="inline-flex rounded-xl border border-slate-200 bg-slate-100 p-1">
          <button
            type="button"
            class="rounded-lg px-4 py-2 text-sm font-semibold transition"
            :class="form.account_type === 'individual' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-600'"
            @click="form.account_type = 'individual'"
          >
            Я человек
          </button>
          <button
            type="button"
            class="rounded-lg px-4 py-2 text-sm font-semibold transition"
            :class="form.account_type === 'organization' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-600'"
            @click="form.account_type = 'organization'"
          >
            Я организация
          </button>
        </div>

        <input v-model="form.email" type="email" required :placeholder="t('emailPlaceholder')" class="w-full rounded-xl border border-slate-200 bg-white px-3 py-3" />
        <input v-model="form.password" type="password" minlength="8" required :placeholder="t('passwordMinPlaceholder')" class="w-full rounded-xl border border-slate-200 bg-white px-3 py-3" />

        <div v-if="form.account_type === 'organization'" class="grid gap-3 sm:grid-cols-2">
          <input
            v-model="form.organization_name"
            required
            maxlength="120"
            placeholder="Название организации"
            class="w-full rounded-xl border border-slate-200 bg-white px-3 py-3"
          />
          <input
            v-model="form.organization_industry"
            maxlength="120"
            placeholder="Отрасль (опционально)"
            class="w-full rounded-xl border border-slate-200 bg-white px-3 py-3"
          />
        </div>

        <p v-if="authStore.error" class="text-sm text-red-700">{{ authStore.error }}</p>
        <button :disabled="authStore.loading" class="w-full rounded-xl bg-accent px-4 py-3 font-semibold text-white transition hover:bg-emerald-600 disabled:opacity-60">
          {{ t('registerButton') }}
        </button>
      </form>

      <p class="mt-4 text-sm text-slate-600">
        {{ t('haveAccount') }}
        <RouterLink to="/login" class="font-semibold text-brand-700 hover:underline">{{ t('loginButton') }}</RouterLink>
      </p>
    </article>
  </section>
</template>
