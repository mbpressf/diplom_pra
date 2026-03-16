<script setup>
import { RouterLink, useRoute } from 'vue-router'

import { useLocale } from '../composables/useLocale'

const route = useRoute()
const { t } = useLocale()

const nav = [
  { to: '/', labelKey: 'navHomeMobile' },
  { to: '/transactions', labelKey: 'navTransactionsMobile' },
  { to: '/analytics', labelKey: 'navAnalyticsMobile' },
  { to: '/vault', labelKey: 'navVaultMobile' },
  { to: '/org', labelKey: 'navOrgMobile' },
]

function isActive(path) {
  return route.path === path
}
</script>

<template>
  <div class="pointer-events-none fixed inset-x-0 bottom-0 z-30 px-4 pb-4 lg:hidden">
    <nav class="pointer-events-auto mx-auto grid max-w-xl grid-cols-5 gap-2 rounded-[24px] border border-white/12 bg-[linear-gradient(180deg,rgba(2,6,23,0.94),rgba(7,15,28,0.88))] p-2 shadow-[0_18px_50px_rgba(2,6,23,0.36)] backdrop-blur-2xl">
      <RouterLink
        v-for="item in nav"
        :key="item.to"
        :to="item.to"
        class="rounded-[18px] px-3 py-3 text-center text-[0.72rem] font-semibold uppercase tracking-[0.14em] transition"
        :class="isActive(item.to) ? 'bg-white text-slate-950 shadow-[0_10px_24px_rgba(255,255,255,0.12)]' : 'text-slate-200/80 hover:bg-white/10 hover:text-white'"
      >
        {{ t(item.labelKey) }}
      </RouterLink>
    </nav>
  </div>
</template>
