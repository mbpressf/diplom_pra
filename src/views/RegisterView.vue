<script setup>
import { reactive } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

import { useAuthStore } from '../store/auth'
import { useFinanceStore } from '../store/finance'

const authStore = useAuthStore()
const financeStore = useFinanceStore()
const router = useRouter()

const form = reactive({
  email: '',
  password: '',
})

async function onSubmit() {
  try {
    await authStore.register(form.email, form.password)
    await financeStore.bootstrap()
    router.push('/')
  } catch {
    // Ошибка уже хранится в store.
  }
}
</script>

<template>
  <section class="mx-auto mt-16 max-w-md rounded-xl2 p-6 shadow-card glass">
    <h1 class="text-2xl font-bold text-brand-700 dark:text-brand-100">Создание аккаунта</h1>

    <form class="mt-6 space-y-3" @submit.prevent="onSubmit">
      <input v-model="form.email" type="email" required placeholder="Электронная почта" class="w-full rounded-lg border border-softgray bg-white px-3 py-2 dark:bg-slate-800" />
      <input v-model="form.password" type="password" minlength="6" required placeholder="Пароль" class="w-full rounded-lg border border-softgray bg-white px-3 py-2 dark:bg-slate-800" />
      <p v-if="authStore.error" class="text-sm text-expense">{{ authStore.error }}</p>
      <button :disabled="authStore.loading" class="w-full rounded-lg bg-accent px-4 py-2 font-semibold text-white transition hover:bg-emerald-600 disabled:opacity-60">Зарегистрироваться</button>
    </form>

    <p class="mt-4 text-sm text-slate-600 dark:text-slate-300">
      Уже есть аккаунт?
      <RouterLink to="/login" class="font-semibold text-brand-700 hover:underline dark:text-brand-100">Войти</RouterLink>
    </p>
  </section>
</template>
