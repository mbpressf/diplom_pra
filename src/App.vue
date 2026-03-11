<script setup>
import { computed, onMounted } from 'vue'
import { RouterView } from 'vue-router'

import { useLocale } from './composables/useLocale'
import AppHeader from './components/AppHeader.vue'
import LanguageCurrencySwitcher from './components/LanguageCurrencySwitcher.vue'
import MobileTabBar from './components/MobileTabBar.vue'
import { useAuthStore } from './store/auth'
import { useFinanceStore } from './store/finance'
import { useUiStore } from './store/ui'

const authStore = useAuthStore()
const financeStore = useFinanceStore()
const uiStore = useUiStore()
const { t } = useLocale()

const isAuthed = computed(() => !!authStore.token)

onMounted(async () => {
  uiStore.initPreferences()
  if (authStore.token) {
    try {
      await financeStore.bootstrap()
    } catch {
      // Не блокируем рендер приложения, если часть данных временно недоступна.
    }
  }
})
</script>

<template>
  <div class="app-bg min-h-screen overflow-x-hidden">
    <div class="pointer-events-none fixed inset-0 overflow-hidden">
      <div class="ambient-orb ambient-orb-a"></div>
      <div class="ambient-orb ambient-orb-b"></div>
      <div class="ambient-grid"></div>
    </div>
    <AppHeader v-if="isAuthed" />
    <main
      class="relative z-[1] mx-auto max-w-6xl px-4 pt-4 sm:px-6 sm:pt-5 lg:px-8"
      :class="isAuthed ? 'pb-28 md:pb-16' : 'pb-12'"
    >
      <div v-if="!isAuthed" class="mb-4 flex justify-end">
        <LanguageCurrencySwitcher />
      </div>
      <RouterView v-slot="{ Component }">
        <Transition name="route-fade" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>

    <footer
      class="relative z-[1] mx-auto max-w-6xl px-4 sm:px-6 lg:px-8"
      :class="isAuthed ? 'pb-28 md:pb-10' : 'pb-10'"
    >
      <section class="glass rounded-[26px] border border-white/15 p-4 shadow-card sm:p-5">
        <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p class="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500 dark:text-slate-400">{{ t('gratitudeTitle') }}</p>
            <p class="mt-2 text-sm leading-6 text-slate-700 dark:text-slate-300">
              {{ t('gratitudeText') }}
            </p>
          </div>
          <div class="flex flex-wrap gap-2">
            <a
              href="https://github.com/mbpressf"
              target="_blank"
              rel="noreferrer"
              class="rounded-full border border-white/15 bg-white/60 px-4 py-2 text-sm font-medium text-slate-800 transition hover:-translate-y-0.5 hover:bg-white dark:bg-slate-950/40 dark:text-slate-100 dark:hover:bg-slate-900"
            >
              {{ t('githubLabel') }}: @mbpressf
            </a>
            <a
              href="https://t.me/fomixb_v"
              target="_blank"
              rel="noreferrer"
              class="rounded-full border border-white/15 bg-white/60 px-4 py-2 text-sm font-medium text-slate-800 transition hover:-translate-y-0.5 hover:bg-white dark:bg-slate-950/40 dark:text-slate-100 dark:hover:bg-slate-900"
            >
              {{ t('telegramLabel') }}: @fomixb_v
            </a>
          </div>
        </div>
      </section>
    </footer>
    <MobileTabBar v-if="isAuthed" />
  </div>
</template>
