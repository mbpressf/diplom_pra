<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

import { useLocale } from '../composables/useLocale'
import { useAuthStore } from '../store/auth'

const route = useRoute()
const authStore = useAuthStore()
const { t } = useLocale()

const personalNav = [
  { to: '/', labelKey: 'navHomeMobile' },
  { to: '/transactions', labelKey: 'navTransactionsMobile' },
  { to: '/analytics', labelKey: 'navAnalyticsMobile' },
  { to: '/vault', labelKey: 'navVaultMobile' },
  { to: '/pricing', labelKey: 'navPricingMobile' },
]

const orgNav = [
  { to: '/org', labelKey: 'navOrgMobile' },
  { to: '/org/reports', labelKey: 'navReportsMobile' },
  { to: '/org/exports', labelKey: 'navExportsMobile' },
  { to: '/pricing', labelKey: 'navPricingMobile' },
]

const nav = computed(() => (authStore.accountType === 'organization' ? orgNav : personalNav))

function isActive(path) {
  return route.path === path
}
</script>

<template>
  <div class="pointer-events-none fixed inset-x-0 bottom-0 z-30 px-4 pb-4 lg:hidden">
    <nav class="pointer-events-auto mx-auto grid max-w-xl gap-2 rounded-[24px] border border-slate-200 bg-white/96 p-2 shadow-[0_18px_50px_rgba(15,23,42,0.14)] backdrop-blur-2xl dark:border-slate-800 dark:bg-slate-950/92" :class="authStore.accountType === 'organization' ? 'grid-cols-4' : 'grid-cols-5'">
      <RouterLink
        v-for="item in nav"
        :key="item.to"
        :to="item.to"
        class="rounded-[18px] px-3 py-3 text-center text-[0.72rem] font-semibold uppercase tracking-[0.14em] transition"
        :class="isActive(item.to) ? 'bg-slate-900 text-white shadow-[0_10px_24px_rgba(15,23,42,0.22)] dark:bg-white dark:text-slate-900' : 'text-slate-700 hover:bg-slate-100 dark:text-slate-200 dark:hover:bg-slate-800'"
      >
        {{ t(item.labelKey) }}
      </RouterLink>
    </nav>
  </div>
</template>
