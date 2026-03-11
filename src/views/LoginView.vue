<script setup>
import { reactive } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

import { useLocale } from '../composables/useLocale'
import { useAuthStore } from '../store/auth'
import { useFinanceStore } from '../store/finance'

const authStore = useAuthStore()
const financeStore = useFinanceStore()
const router = useRouter()
const { t } = useLocale()

const form = reactive({
  email: '',
  password: '',
})

async function onSubmit() {
  try {
    await authStore.login(form.email, form.password)
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
  <section class="mx-auto mt-16 max-w-md rounded-xl2 p-6 shadow-card glass">
    <h1 class="text-2xl font-bold text-brand-700 dark:text-brand-100">{{ t('loginTitle') }}</h1>

    <form class="mt-6 space-y-3" @submit.prevent="onSubmit">
      <input v-model="form.email" type="email" required autocomplete="email" :placeholder="t('emailPlaceholder')" class="w-full rounded-lg border border-softgray bg-white px-3 py-2 dark:bg-slate-800" />
      <input v-model="form.password" type="password" required autocomplete="current-password" :placeholder="t('passwordPlaceholder')" class="w-full rounded-lg border border-softgray bg-white px-3 py-2 dark:bg-slate-800" />
      <p v-if="authStore.error" class="text-sm text-expense">{{ authStore.error }}</p>
      <button :disabled="authStore.loading" class="w-full rounded-lg bg-brand-700 px-4 py-2 font-semibold text-white transition hover:bg-brand-500 disabled:opacity-60">{{ t('loginButton') }}</button>
    </form>

    <p class="mt-4 text-sm text-slate-600 dark:text-slate-300">
      {{ t('noAccount') }}
      <RouterLink to="/register" class="font-semibold text-accent hover:underline">{{ t('registerLink') }}</RouterLink>
    </p>
  </section>
</template>
