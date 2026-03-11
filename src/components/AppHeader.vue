<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'

import { useLocale } from '../composables/useLocale'
import { useAuthStore } from '../store/auth'
import { useFinanceStore } from '../store/finance'
import { useUiStore } from '../store/ui'
import LanguageCurrencySwitcher from './LanguageCurrencySwitcher.vue'

const authStore = useAuthStore()
const financeStore = useFinanceStore()
const uiStore = useUiStore()
const route = useRoute()
const router = useRouter()
const menuOpen = ref(false)
const { t } = useLocale()

const nav = [
  { to: '/', labelKey: 'navOverview' },
  { to: '/analytics', labelKey: 'navAnalytics' },
  { to: '/vault', labelKey: 'navVault' },
  { to: '/transactions', labelKey: 'navTransactions' },
  { to: '/categories', labelKey: 'navCategories' },
]

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
  router.push('/login')
}
</script>

<template>
  <header class="sticky top-0 z-40 border-b border-white/10 bg-[linear-gradient(135deg,rgba(5,10,22,0.92),rgba(7,20,38,0.78))] py-2 shadow-[0_10px_60px_rgba(2,6,23,0.28)] backdrop-blur-2xl">
    <div class="mx-auto flex max-w-6xl items-center justify-between gap-3 px-4 sm:px-6 lg:px-8">
      <RouterLink to="/" class="inline-flex items-center gap-3 rounded-full border border-white/10 bg-white/8 px-3 py-2 text-sm font-semibold tracking-[0.16em] text-white transition hover:bg-white/12">
        <span class="inline-flex h-9 w-9 items-center justify-center rounded-full bg-[linear-gradient(135deg,#2563eb,#06b6d4,#10b981)] text-xs font-bold text-white shadow-[0_10px_25px_rgba(14,165,233,0.35)]">Ф</span>
        {{ t('brand') }}
      </RouterLink>

      <nav class="hidden items-center gap-2 lg:flex">
        <RouterLink
          v-for="item in nav"
          :key="item.to"
          :to="item.to"
          class="rounded-full px-4 py-2 text-sm font-medium transition"
          :class="isActive(item.to) ? 'bg-white text-slate-950 shadow-[0_8px_20px_rgba(255,255,255,0.18)]' : 'text-slate-200/85 hover:bg-white/10 hover:text-white'"
        >
          {{ t(item.labelKey) }}
        </RouterLink>
      </nav>

      <div class="hidden items-center gap-2 lg:flex">
        <LanguageCurrencySwitcher compact />
        <button
          class="rounded-full border border-white/15 px-4 py-2 text-sm font-medium text-slate-100 transition hover:-translate-y-0.5 hover:bg-white/10"
          @click="uiStore.toggleTheme"
        >
          {{ themeLabel }}
        </button>
        <button
          class="rounded-full bg-white px-4 py-2 text-sm font-semibold text-slate-900 transition hover:-translate-y-0.5 hover:bg-slate-100"
          @click="logout"
        >
          {{ t('logout') }}
        </button>
      </div>

      <div class="flex items-center gap-2 lg:hidden">
        <button
          class="inline-flex h-10 w-10 items-center justify-center rounded-full border border-white/12 bg-white/10 text-white transition hover:bg-white/15"
          @click="uiStore.toggleTheme"
        >
          <span class="text-lg">{{ uiStore.theme === 'dark' ? '☀' : '☾' }}</span>
        </button>
        <button
          class="relative inline-flex h-10 w-10 items-center justify-center rounded-full border border-white/12 bg-white/10 text-white transition hover:bg-white/15"
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
        <div class="absolute inset-0 bg-slate-950/55 backdrop-blur-sm"></div>
        <div class="absolute right-4 top-[72px] w-[min(280px,calc(100vw-2rem))] rounded-[28px] border border-white/12 bg-[linear-gradient(180deg,rgba(2,6,23,0.96),rgba(7,15,28,0.92))] p-4 shadow-2xl backdrop-blur-2xl" @click.stop>
          <div class="grid gap-2">
            <RouterLink
              v-for="item in nav"
              :key="item.to"
              :to="item.to"
              class="rounded-2xl border border-white/12 px-4 py-3 text-left text-sm font-medium text-slate-100 transition hover:bg-white/10"
              :class="isActive(item.to) ? 'bg-white text-slate-950' : ''"
            >
              {{ t(item.labelKey) }}
            </RouterLink>
            <button
              class="rounded-2xl border border-white/12 px-4 py-3 text-left text-sm font-medium text-slate-100 transition hover:bg-white/10"
              @click="uiStore.toggleTheme"
            >
              {{ themeLabel }}
            </button>
            <LanguageCurrencySwitcher />
            <button
              class="rounded-2xl bg-white px-4 py-3 text-left text-sm font-semibold text-slate-900 transition hover:bg-slate-100"
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
