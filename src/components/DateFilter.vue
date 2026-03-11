<script setup>
import { reactive } from 'vue'

import { useLocale } from '../composables/useLocale'

const emit = defineEmits(['apply'])
const { t } = useLocale()

const form = reactive({
  startDate: '',
  endDate: '',
})

function applyFilter() {
  emit('apply', { ...form })
}

function resetFilter() {
  form.startDate = ''
  form.endDate = ''
  emit('apply', { ...form })
}
</script>

<template>
  <div class="glass grid gap-3 rounded-[24px] border border-white/20 p-4 shadow-card sm:grid-cols-2 xl:grid-cols-[1fr_1fr_auto_auto] xl:items-end">
    <label class="flex flex-col gap-1 text-sm text-slate-700 dark:text-slate-200">
      {{ t('dateStart') }}
      <input v-model="form.startDate" type="date" class="rounded-2xl border border-white/20 bg-white/70 px-4 py-3 dark:bg-slate-950/45" />
    </label>
    <label class="flex flex-col gap-1 text-sm text-slate-700 dark:text-slate-200">
      {{ t('dateEnd') }}
      <input v-model="form.endDate" type="date" class="rounded-2xl border border-white/20 bg-white/70 px-4 py-3 dark:bg-slate-950/45" />
    </label>
    <button class="rounded-2xl bg-brand-700 px-5 py-3 font-semibold text-white transition hover:-translate-y-0.5 hover:bg-brand-500" @click="applyFilter">{{ t('apply') }}</button>
    <button class="rounded-2xl border border-white/20 px-5 py-3 font-semibold text-slate-700 transition hover:bg-white dark:text-slate-100 dark:hover:bg-slate-800" @click="resetFilter">{{ t('reset') }}</button>
  </div>
</template>
