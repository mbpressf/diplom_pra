<script setup>
import { reactive } from 'vue'

const emit = defineEmits(['apply'])

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
  <div class="glass flex flex-wrap items-end gap-3 rounded-xl2 p-4 shadow-card">
    <label class="flex flex-col gap-1 text-sm">
      Дата начала
      <input v-model="form.startDate" type="date" class="rounded-lg border border-softgray bg-white px-3 py-2 dark:bg-slate-800" />
    </label>
    <label class="flex flex-col gap-1 text-sm">
      Дата окончания
      <input v-model="form.endDate" type="date" class="rounded-lg border border-softgray bg-white px-3 py-2 dark:bg-slate-800" />
    </label>
    <button class="rounded-lg bg-brand-700 px-4 py-2 font-semibold text-white transition hover:bg-brand-500" @click="applyFilter">Применить</button>
    <button class="rounded-lg border border-softgray px-4 py-2 font-semibold transition hover:bg-white dark:hover:bg-slate-800" @click="resetFilter">Сбросить</button>
  </div>
</template>
