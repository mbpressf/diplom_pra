<script setup>
import { computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

import { useAuthStore } from '../store/auth'
import { useFinanceStore } from '../store/finance'
import { useUiStore } from '../store/ui'

const authStore = useAuthStore()
const financeStore = useFinanceStore()
const uiStore = useUiStore()
const router = useRouter()

const nav = [
  { to: '/', label: 'Дашборд' },
  { to: '/transactions', label: 'Транзакции' },
  { to: '/categories', label: 'Категории' },
]

const themeLabel = computed(() => (uiStore.theme === 'dark' ? 'Светлая тема' : 'Тёмная тема'))

function logout() {
  authStore.logout()
  financeStore.clear()
  router.push('/login')
}
</script>

<template>
  <header class="sticky top-0 z-10 border-b border-white/40 bg-white/60 py-3 backdrop-blur-xl dark:border-slate-700/60 dark:bg-slate-900/65">
    <div class="mx-auto flex max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
      <RouterLink to="/" class="text-lg font-bold tracking-tight text-brand-700 dark:text-brand-100">ФинПоток</RouterLink>
      <nav class="flex items-center gap-2">
        <RouterLink
          v-for="item in nav"
          :key="item.to"
          :to="item.to"
          class="rounded-lg px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-brand-100 hover:text-brand-700 dark:text-slate-200 dark:hover:bg-slate-800"
        >
          {{ item.label }}
        </RouterLink>
      </nav>
      <div class="flex items-center gap-2">
        <button
          class="rounded-lg border border-slate-300 px-3 py-2 text-sm font-medium transition hover:-translate-y-0.5 hover:bg-white dark:border-slate-600 dark:hover:bg-slate-800"
          @click="uiStore.toggleTheme"
        >
          {{ themeLabel }}
        </button>
        <button
          class="rounded-lg bg-brand-700 px-3 py-2 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:bg-brand-500"
          @click="logout"
        >
          Выйти
        </button>
      </div>
    </div>
  </header>
</template>
