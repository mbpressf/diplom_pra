<script setup>
import { computed, reactive } from 'vue'

const props = defineProps({
  categories: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['submit'])

const form = reactive({
  amount: '',
  type: 'expense',
  category_id: '',
  date: new Date().toISOString().slice(0, 10),
  description: '',
})

const uniqueCategories = computed(() => {
  const used = new Set()
  return props.categories.filter((item) => {
    const key = item.name.trim().toLowerCase()
    if (used.has(key)) return false
    used.add(key)
    return true
  })
})

function submit() {
  if (!form.category_id) return
  emit('submit', {
    amount: Number(form.amount),
    type: form.type,
    category_id: Number(form.category_id),
    date: form.date,
    description: form.description,
  })

  form.amount = ''
  form.description = ''
}
</script>

<template>
  <form class="glass grid grid-cols-1 gap-3 rounded-[24px] border border-white/20 p-4 shadow-card sm:grid-cols-2 xl:grid-cols-6" @submit.prevent="submit">
    <input v-model="form.amount" type="number" min="0" step="0.01" required placeholder="Сумма" class="rounded-2xl border border-white/20 bg-white/70 px-4 py-3 dark:bg-slate-950/45" />
    <select v-model="form.type" class="rounded-2xl border border-white/20 bg-white/70 px-4 py-3 dark:bg-slate-950/45">
      <option value="income">Доход</option>
      <option value="expense">Расход</option>
    </select>
    <select v-model="form.category_id" required class="rounded-2xl border border-white/20 bg-white/70 px-4 py-3 dark:bg-slate-950/45">
      <option value="">Категория</option>
      <option v-for="item in uniqueCategories" :key="item.id" :value="item.id">{{ item.name }}</option>
    </select>
    <input v-model="form.date" type="date" required class="rounded-2xl border border-white/20 bg-white/70 px-4 py-3 dark:bg-slate-950/45" />
    <input v-model="form.description" maxlength="255" placeholder="Описание" class="rounded-2xl border border-white/20 bg-white/70 px-4 py-3 dark:bg-slate-950/45" />
    <button class="rounded-2xl bg-gradient-to-r from-accent to-emerald-400 px-4 py-3 font-semibold text-white transition hover:-translate-y-0.5">Добавить</button>
  </form>
</template>
