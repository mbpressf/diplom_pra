<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'

import { useLocale } from '../composables/useLocale'
import { useAuthStore } from '../store/auth'
import { useFinanceStore } from '../store/finance'
import { useOrgStore } from '../store/orgs'
import { useUiStore } from '../store/ui'

const authStore = useAuthStore()
const financeStore = useFinanceStore()
const orgStore = useOrgStore()
const uiStore = useUiStore()
const route = useRoute()
const router = useRouter()
const menuOpen = ref(false)
const { t } = useLocale()

const personalNav = [
  { to: '/', labelKey: 'navOverview' },
  { to: '/analytics', labelKey: 'navAnalytics' },
  { to: '/vault', labelKey: 'navVault' },
  { to: '/transactions', labelKey: 'navTransactions' },
  { to: '/categories', labelKey: 'navCategories' },
  { to: '/pricing', labelKey: 'navPricing' },
]

const orgNav = [
  { to: '/org', labelKey: 'navOrganization' },
  { to: '/org/reports', labelKey: 'navReports' },
  { to: '/org/exports', labelKey: 'navExports' },
  { to: '/pricing', labelKey: 'navPricing' },
]

const nav = computed(() => (authStore.accountType === 'organization' ? orgNav : personalNav))

const themeLabel = computed(() => (uiStore.theme === 'dark' ? t('themeLight') : t('themeDark')))

watch(
  () => route.fullPath,
  () => {
    menuOpen.value = false
  },
)

function isActive(path) {
  return route.path === path
}

function closeMenu() {
  menuOpen.value = false
}

function logout() {
  authStore.logout()
  financeStore.clear()
  orgStore.clear()
  router.push({ name: 'login' })
}
</script>

<template>
  <header class="sticky top-0 z-40 border-b border-slate-200/90 bg-white/92 py-2 shadow-[0_12px_40px_rgba(15,23,42,0.08)] backdrop-blur-2xl dark:border-slate-800 dark:bg-slate-950/88">
    <div class="mx-auto flex max-w-6xl items-center justify-between gap-3 px-4 sm:px-6 lg:px-8">
      <RouterLink to="/" class="inline-flex items-center gap-3 rounded-full border border-slate-200 bg-white px-3 py-2 text-sm font-semibold tracking-[0.12em] text-slate-900 transition hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100">
        <span class="inline-flex h-9 w-9 items-center justify-center rounded-full bg-[linear-gradient(135deg,#1d4ed8,#0ea5e9)] text-xs font-bold text-white shadow-[0_10px_20px_rgba(37,99,235,0.25)]">Ф</span>
        {{ t('brand') }}
      </RouterLink>

      <nav class="hidden max-w-[calc(100vw-460px)] items-center gap-1 overflow-x-auto lg:flex">
        <RouterLink
          v-for="item in nav"
          :key="item.to"
          :to="item.to"
          class="whitespace-nowrap rounded-full px-3 py-2 text-sm font-medium transition"
          :class="isActive(item.to) ? 'bg-slate-900 text-white shadow-[0_8px_20px_rgba(15,23,42,0.2)] dark:bg-white dark:text-slate-900' : 'text-slate-700 hover:bg-slate-100 dark:text-slate-200 dark:hover:bg-slate-800'"
        >
          {{ t(item.labelKey) }}
        </RouterLink>
      </nav>

      <div class="hidden items-center gap-2 lg:flex">
        <button
          class="rounded-full border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 transition hover:-translate-y-0.5 hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
          @click="uiStore.toggleTheme"
        >
          {{ themeLabel }}
        </button>
        <button
          class="rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:bg-slate-700 dark:bg-white dark:text-slate-900 dark:hover:bg-slate-200"
          @click="logout"
        >
          {{ t('logout') }}
        </button>
      </div>

      <div class="flex items-center gap-2 lg:hidden">
        <button
          class="inline-flex h-10 w-10 items-center justify-center rounded-full border border-slate-300 bg-white text-slate-800 transition hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:hover:bg-slate-800"
          @click="uiStore.toggleTheme"
        >
          <span class="text-lg">{{ uiStore.theme === 'dark' ? '☀' : '☾' }}</span>
        </button>
        <button
          class="relative inline-flex h-10 w-10 items-center justify-center rounded-full border border-slate-300 bg-white text-slate-800 transition hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:hover:bg-slate-800"
          @click="menuOpen = !menuOpen"
        >
          <span class="sr-only">Открыть меню</span>
          <span class="absolute h-0.5 w-5 rounded-full bg-current transition" :class="menuOpen ? 'rotate-45' : '-translate-y-1.5'"></span>
          <span class="absolute h-0.5 w-5 rounded-full bg-current transition" :class="menuOpen ? 'opacity-0' : 'opacity-100'"></span>
          <span class="absolute h-0.5 w-5 rounded-full bg-current transition" :class="menuOpen ? '-rotate-45' : 'translate-y-1.5'"></span>
        </button>
      </div>
    </div>

    <Transition name="route-fade">
      <div v-if="menuOpen" class="fixed inset-0 z-50 lg:hidden" @click="closeMenu">
        <div class="absolute inset-0 bg-slate-900/35 backdrop-blur-sm dark:bg-slate-950/65"></div>
        <div class="absolute right-4 top-[72px] w-[min(300px,calc(100vw-2rem))] rounded-[28px] border border-slate-200 bg-white p-4 shadow-2xl dark:border-slate-800 dark:bg-slate-950" @click.stop>
          <div class="grid gap-2">
            <RouterLink
              v-for="item in nav"
              :key="item.to"
              :to="item.to"
              class="rounded-2xl border border-slate-200 px-4 py-3 text-left text-sm font-medium text-slate-700 transition hover:bg-slate-100 dark:border-slate-700 dark:text-slate-100 dark:hover:bg-slate-800"
              :class="isActive(item.to) ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900' : ''"
            >
              {{ t(item.labelKey) }}
            </RouterLink>
            <button
              class="rounded-2xl border border-slate-200 px-4 py-3 text-left text-sm font-medium text-slate-700 transition hover:bg-slate-100 dark:border-slate-700 dark:text-slate-100 dark:hover:bg-slate-800"
              @click="uiStore.toggleTheme"
            >
              {{ themeLabel }}
            </button>
            <button
              class="rounded-2xl bg-slate-900 px-4 py-3 text-left text-sm font-semibold text-white transition hover:bg-slate-700 dark:bg-white dark:text-slate-900 dark:hover:bg-slate-200"
              @click="logout"
            >
              {{ t('logout') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </header>
</template>
