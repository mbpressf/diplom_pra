<script setup>
import { reactive } from 'vue'

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
  <form class="glass grid grid-cols-1 gap-3 rounded-xl2 p-4 shadow-card md:grid-cols-6" @submit.prevent="submit">
    <input v-model="form.amount" type="number" min="0" step="0.01" required placeholder="Сумма" class="rounded-lg border border-softgray bg-white px-3 py-2 dark:bg-slate-800" />
    <select v-model="form.type" class="rounded-lg border border-softgray bg-white px-3 py-2 dark:bg-slate-800">
      <option value="income">Доход</option>
      <option value="expense">Расход</option>
    </select>
    <select v-model="form.category_id" required class="rounded-lg border border-softgray bg-white px-3 py-2 dark:bg-slate-800">
      <option value="">Категория</option>
      <option v-for="item in categories" :key="item.id" :value="item.id">{{ item.name }}</option>
    </select>
    <input v-model="form.date" type="date" required class="rounded-lg border border-softgray bg-white px-3 py-2 dark:bg-slate-800" />
    <input v-model="form.description" maxlength="255" placeholder="Описание" class="rounded-lg border border-softgray bg-white px-3 py-2 dark:bg-slate-800" />
    <button class="rounded-lg bg-accent px-4 py-2 font-semibold text-white transition hover:-translate-y-0.5 hover:bg-emerald-600">Добавить</button>
  </form>
</template>
