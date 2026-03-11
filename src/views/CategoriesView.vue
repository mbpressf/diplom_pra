<script setup>
import { computed, reactive, ref } from 'vue'

import { useLocale } from '../composables/useLocale'
import { useFinanceStore } from '../store/finance'

const financeStore = useFinanceStore()
const editingId = ref(null)
const statusText = ref('')
const statusType = ref('') // success | error
const { t, uiStore } = useLocale()

const form = reactive({
  name: '',
  color: '#10B981',
})

const commonCategoryPresets = [
  { names: { ru: 'Зарплата', en: 'Salary' }, aliases: ['зарплата', 'salary'], color: '#22C55E' },
  { names: { ru: 'Подработка', en: 'Side hustle' }, aliases: ['подработка', 'side hustle'], color: '#10B981' },
  { names: { ru: 'Инвестиции', en: 'Investments' }, aliases: ['инвестиции', 'investments'], color: '#0EA5E9' },
  { names: { ru: 'Продукты', en: 'Groceries' }, aliases: ['продукты', 'groceries'], color: '#EF4444' },
  { names: { ru: 'Кафе и рестораны', en: 'Dining out' }, aliases: ['кафе и рестораны', 'dining out'], color: '#F97316' },
  { names: { ru: 'Транспорт', en: 'Transport' }, aliases: ['транспорт', 'transport'], color: '#3B82F6' },
  { names: { ru: 'Жилье', en: 'Housing' }, aliases: ['жилье', 'housing'], color: '#8B5CF6' },
  { names: { ru: 'Коммунальные услуги', en: 'Utilities' }, aliases: ['коммунальные услуги', 'utilities'], color: '#6366F1' },
  { names: { ru: 'Здоровье', en: 'Health' }, aliases: ['здоровье', 'health'], color: '#EC4899' },
  { names: { ru: 'Развлечения', en: 'Fun' }, aliases: ['развлечения', 'fun'], color: '#F59E0B' },
]

const existingCategoryNames = computed(() => new Set(financeStore.categories.map((i) => i.name.trim().toLowerCase())))
const missingCommonCategories = computed(() =>
  commonCategoryPresets
    .map((item) => ({
      name: item.names[uiStore.locale],
      color: item.color,
      aliases: item.aliases,
    }))
    .filter((item) => !item.aliases.some((alias) => existingCategoryNames.value.has(alias))),
)

async function createCategory() {
  if (!form.name.trim()) return
  statusText.value = ''
  try {
    await financeStore.addCategory({ name: form.name, color: form.color })
    form.name = ''
    form.color = '#10B981'
    statusType.value = 'success'
    statusText.value = t('categoryCreated')
  } catch (error) {
    statusType.value = 'error'
    statusText.value = error?.response?.data?.detail || t('categoryCreateError')
  }
}

function startEdit(item) {
  editingId.value = item.id
  form.name = item.name
  form.color = item.color
}

async function saveEdit() {
  if (!editingId.value) return
  statusText.value = ''
  try {
    await financeStore.updateCategory(editingId.value, { name: form.name, color: form.color })
    editingId.value = null
    form.name = ''
    form.color = '#10B981'
    statusType.value = 'success'
    statusText.value = t('categorySaved')
  } catch (error) {
    statusType.value = 'error'
    statusText.value = error?.response?.data?.detail || t('categorySaveError')
  }
}

async function addCommonCategory(item) {
  if (item.aliases.some((alias) => existingCategoryNames.value.has(alias))) return
  await financeStore.addCategory({ name: item.name, color: item.color })
}

async function addAllCommonCategories() {
  for (const item of missingCommonCategories.value) {
    await financeStore.addCategory({ name: item.name, color: item.color })
  }
}
</script>

<template>
  <section class="space-y-5">
    <article class="glass rounded-xl2 p-4 shadow-card">
      <h2 class="text-lg font-semibold">{{ editingId ? t('editCategory') : t('createCategory') }}</h2>
      <div class="mt-3 flex flex-wrap items-end gap-3">
        <label class="flex flex-col gap-1 text-sm">
          {{ t('categoryName') }}
          <input v-model="form.name" type="text" :placeholder="t('categoryNamePlaceholder')" class="rounded-lg border border-softgray bg-white px-3 py-2 dark:bg-slate-800" />
        </label>
        <label class="flex flex-col gap-1 text-sm">
          {{ t('color') }}
          <input v-model="form.color" type="color" class="h-10 w-20 rounded-lg border border-softgray bg-white px-1 py-1 dark:bg-slate-800" />
        </label>
        <button
          class="rounded-lg bg-accent px-4 py-2 font-semibold text-white transition hover:bg-emerald-600"
          @click="editingId ? saveEdit() : createCategory()"
        >
          {{ editingId ? t('save') : t('create') }}
        </button>
      </div>
      <p
        v-if="statusText"
        class="mt-3 text-sm"
        :class="statusType === 'error' ? 'text-expense' : 'text-income'"
      >
        {{ statusText }}
      </p>
    </article>

    <article class="glass rounded-xl2 p-4 shadow-card">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <h2 class="text-lg font-semibold">{{ t('commonCategories') }}</h2>
        <button
          class="rounded-lg border border-softgray px-3 py-2 text-sm font-semibold transition hover:bg-white disabled:cursor-not-allowed disabled:opacity-50 dark:hover:bg-slate-800"
          :disabled="missingCommonCategories.length === 0"
          @click="addAllCommonCategories"
        >
          {{ t('addAll') }}
        </button>
      </div>
      <div class="mt-3 flex flex-wrap gap-2">
        <button
          v-for="item in missingCommonCategories"
          :key="item.name"
          class="rounded-full border border-softgray px-3 py-1.5 text-sm font-medium transition hover:-translate-y-0.5 hover:bg-white disabled:cursor-not-allowed disabled:opacity-45 dark:hover:bg-slate-800"
          @click="addCommonCategory(item)"
        >
          <span class="mr-2 inline-block h-2.5 w-2.5 rounded-full align-middle" :style="{ backgroundColor: item.color }"></span>
          {{ item.name }}
        </button>
      </div>
    </article>

    <section class="grid grid-cols-1 gap-3 md:grid-cols-2 lg:grid-cols-3">
      <article v-for="item in financeStore.categories" :key="item.id" class="glass rounded-xl2 p-4 shadow-card transition hover:-translate-y-1">
        <div class="flex items-center justify-between">
          <h3 class="font-semibold">{{ item.name }}</h3>
          <span class="h-4 w-4 rounded-full" :style="{ backgroundColor: item.color }"></span>
        </div>
        <button class="mt-3 rounded-lg border border-softgray px-3 py-1 text-sm transition hover:bg-white dark:hover:bg-slate-800" @click="startEdit(item)">{{ t('edit') }}</button>
      </article>
    </section>
  </section>
</template>
