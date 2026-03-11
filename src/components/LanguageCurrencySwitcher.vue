<script setup>
import { computed } from 'vue'

import { useLocale } from '../composables/useLocale'

const { uiStore, t, rateValue } = useLocale()

const props = defineProps({
  compact: {
    type: Boolean,
    default: false,
  },
})

const rateInfoText = computed(() => t('rateInfo', { rate: rateValue(uiStore.usdToRubRate) }))
const rateDateText = computed(() => (uiStore.rateDate ? t('rateDate', { date: uiStore.rateDate }) : ''))

async function changeLocale(locale) {
  await uiStore.setLocale(locale)
}
</script>

<template>
  <div :class="props.compact ? 'space-y-1' : 'space-y-2'">
    <div class="inline-flex rounded-full border border-white/15 bg-white/8 p-1">
      <button
        type="button"
        class="rounded-full px-3 py-1.5 text-xs font-semibold uppercase tracking-[0.14em] transition"
        :class="uiStore.locale === 'ru' ? 'bg-white text-slate-950' : 'text-slate-200 hover:bg-white/10 hover:text-white'"
        :disabled="uiStore.rateLoading"
        @click="changeLocale('ru')"
      >
        {{ t('languageRu') }}
      </button>
      <button
        type="button"
        class="rounded-full px-3 py-1.5 text-xs font-semibold uppercase tracking-[0.14em] transition"
        :class="uiStore.locale === 'en' ? 'bg-white text-slate-950' : 'text-slate-200 hover:bg-white/10 hover:text-white'"
        :disabled="uiStore.rateLoading"
        @click="changeLocale('en')"
      >
        {{ t('languageEn') }}
      </button>
    </div>

    <div v-if="uiStore.locale === 'en'" class="text-[0.68rem] leading-5 text-slate-300">
      <p>{{ uiStore.rateLoading ? t('rateLoading') : rateInfoText }}</p>
      <template v-if="!props.compact">
        <p v-if="rateDateText" class="text-slate-400">{{ rateDateText }}</p>
        <p v-if="uiStore.rateError" class="text-amber-300">{{ t('rateFallback') }}</p>
      </template>
    </div>
  </div>
</template>
