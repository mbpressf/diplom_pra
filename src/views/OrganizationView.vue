<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

import { useLocale } from '../composables/useLocale'
import { useOrgStore } from '../store/orgs'

const router = useRouter()
const orgStore = useOrgStore()
const { money } = useLocale()

const createForm = reactive({
  name: '',
  industry: '',
})
const joinForm = reactive({
  invite_code: '',
  consent: true,
})

const periodType = ref('month')
const range = reactive({
  startDate: '',
  endDate: '',
})

const createLoading = ref(false)
const joinLoading = ref(false)
const notice = ref('')
const errorText = ref('')

const selectedOrgId = computed({
  get: () => orgStore.selectedOrgId,
  set: (value) => orgStore.setSelectedOrg(value),
})

const dashboard = computed(() => orgStore.dashboard)

const kpiItems = computed(() => {
  if (!dashboard.value) return []
  return [
    { key: 'active_users_count', label: 'Активные пользователи', value: dashboard.value.active_users_count },
    { key: 'median_income_rub', label: 'Медианный доход', value: money(dashboard.value.median_income_rub) },
    { key: 'median_expense_rub', label: 'Медианный расход', value: money(dashboard.value.median_expense_rub) },
    { key: 'median_savings_rate_pct', label: 'Медианный savings rate', value: `${dashboard.value.median_savings_rate_pct}%` },
    { key: 'overspend_share_pct', label: 'Доля перерасхода', value: `${dashboard.value.overspend_share_pct}%` },
    { key: 'high_risk_share_pct', label: 'Доля high-risk', value: `${dashboard.value.high_risk_share_pct}%` },
    { key: 'top5_expense_categories_share_pct', label: 'Топ-5 категорий расходов', value: `${dashboard.value.top5_expense_categories_share_pct}%` },
    { key: 'savings_rate_delta_vs_prev_period_pct', label: 'Delta к прошлому периоду', value: `${dashboard.value.savings_rate_delta_vs_prev_period_pct}%` },
  ]
})

function dashboardParams() {
  const params = { period_type: periodType.value }
  if (range.startDate && range.endDate) {
    params.start_date = range.startDate
    params.end_date = range.endDate
  }
  return params
}

async function loadDashboard() {
  if (!orgStore.selectedOrgId) return
  await orgStore.fetchDashboard(dashboardParams())
}

async function createOrganization() {
  createLoading.value = true
  notice.value = ''
  errorText.value = ''
  try {
    await orgStore.createOrganization(createForm)
    createForm.name = ''
    createForm.industry = ''
    notice.value = 'Организация создана'
    await loadDashboard()
  } catch (error) {
    errorText.value = error?.response?.data?.detail || 'Не удалось создать организацию'
  } finally {
    createLoading.value = false
  }
}

async function joinOrganization() {
  joinLoading.value = true
  notice.value = ''
  errorText.value = ''
  try {
    await orgStore.joinOrganization(joinForm)
    joinForm.invite_code = ''
    joinForm.consent = true
    notice.value = 'Вы присоединились к организации'
    await loadDashboard()
  } catch (error) {
    errorText.value = error?.response?.data?.detail || 'Не удалось вступить в организацию'
  } finally {
    joinLoading.value = false
  }
}

async function refreshAll() {
  await orgStore.fetchOrganizations()
  if (orgStore.selectedOrgId) {
    await Promise.all([loadDashboard(), orgStore.fetchReports()])
  }
}

onMounted(async () => {
  await refreshAll()
})

watch(
  () => orgStore.selectedOrgId,
  async (nextId, prevId) => {
    if (!nextId || nextId === prevId) return
    await Promise.all([loadDashboard(), orgStore.fetchReports()])
  },
)
</script>

<template>
  <section class="space-y-5">
    <article class="glass rounded-[28px] border border-white/20 p-5 shadow-card">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 class="text-2xl font-semibold tracking-tight text-slate-900 dark:text-slate-50">Организация</h1>
          <p class="mt-2 text-sm text-slate-600 dark:text-slate-300">
            B2B-контур: подключайте сотрудников, считайте KPI и формируйте регулярные отчёты.
          </p>
        </div>
        <div class="rounded-2xl border border-emerald-400/35 bg-emerald-500/10 px-4 py-3 text-sm font-medium text-emerald-800 dark:text-emerald-200">
          Тариф: 9 900 ₽/мес + 99 ₽ за активного
        </div>
      </div>
    </article>

    <article class="grid gap-4 xl:grid-cols-2">
      <form class="glass rounded-[24px] border border-white/20 p-4 shadow-card" @submit.prevent="createOrganization">
        <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">Создать организацию</h2>
        <div class="mt-3 space-y-3">
          <input
            v-model="createForm.name"
            maxlength="120"
            required
            placeholder="Название организации"
            class="w-full rounded-2xl border border-white/20 bg-white/70 px-4 py-3 dark:bg-slate-950/45"
          />
          <input
            v-model="createForm.industry"
            maxlength="120"
            placeholder="Отрасль (опционально)"
            class="w-full rounded-2xl border border-white/20 bg-white/70 px-4 py-3 dark:bg-slate-950/45"
          />
          <button
            type="submit"
            :disabled="createLoading"
            class="w-full rounded-2xl bg-brand-700 px-4 py-3 text-sm font-semibold text-white transition hover:bg-brand-500 disabled:opacity-60"
          >
            {{ createLoading ? 'Создание...' : 'Создать и открыть' }}
          </button>
        </div>
      </form>

      <form class="glass rounded-[24px] border border-white/20 p-4 shadow-card" @submit.prevent="joinOrganization">
        <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">Вступить по invite-коду</h2>
        <div class="mt-3 space-y-3">
          <input
            v-model="joinForm.invite_code"
            maxlength="32"
            required
            placeholder="INVITE CODE"
            class="w-full rounded-2xl border border-white/20 bg-white/70 px-4 py-3 uppercase dark:bg-slate-950/45"
          />
          <label class="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300">
            <input v-model="joinForm.consent" type="checkbox" class="h-4 w-4" />
            Даю согласие на обезличенную аналитику
          </label>
          <button
            type="submit"
            :disabled="joinLoading"
            class="w-full rounded-2xl bg-accent px-4 py-3 text-sm font-semibold text-white transition hover:bg-emerald-600 disabled:opacity-60"
          >
            {{ joinLoading ? 'Подключение...' : 'Вступить' }}
          </button>
        </div>
      </form>
    </article>

    <p v-if="notice" class="rounded-2xl border border-emerald-400/30 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-800 dark:text-emerald-200">{{ notice }}</p>
    <p v-if="errorText" class="rounded-2xl border border-red-400/30 bg-red-500/10 px-4 py-3 text-sm text-red-700 dark:text-red-200">{{ errorText }}</p>

    <article class="glass rounded-[24px] border border-white/20 p-4 shadow-card">
      <div class="mb-3 flex flex-wrap items-center justify-between gap-3">
        <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">Мои организации</h2>
        <button class="rounded-xl border border-white/25 px-3 py-2 text-sm font-medium hover:bg-white/40 dark:hover:bg-slate-800" @click="refreshAll">
          Обновить
        </button>
      </div>

      <div v-if="!orgStore.hasOrganizations" class="rounded-2xl border border-dashed border-slate-300/70 px-4 py-5 text-sm text-slate-600 dark:border-slate-600 dark:text-slate-300">
        Пока нет организаций. Создайте новую или вступите по invite-коду.
      </div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full text-sm">
          <thead class="bg-slate-200/50 dark:bg-slate-800/50">
            <tr>
              <th class="px-3 py-3 text-left">Организация</th>
              <th class="px-3 py-3 text-left">Роль</th>
              <th class="px-3 py-3 text-left">Invite-код</th>
              <th class="px-3 py-3 text-left"></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in orgStore.organizations"
              :key="item.id"
              class="border-t border-slate-200/70 dark:border-slate-700"
            >
              <td class="px-3 py-3">
                <p class="font-semibold text-slate-900 dark:text-slate-50">{{ item.name }}</p>
                <p v-if="item.industry" class="text-xs text-slate-500 dark:text-slate-400">{{ item.industry }}</p>
              </td>
              <td class="px-3 py-3">{{ item.member_role }}</td>
              <td class="px-3 py-3"><span class="rounded bg-slate-900/5 px-2 py-1 text-xs dark:bg-white/10">{{ item.invite_code }}</span></td>
              <td class="px-3 py-3 text-right">
                <button
                  class="rounded-xl px-3 py-2 text-sm font-semibold"
                  :class="selectedOrgId === item.id ? 'bg-brand-700 text-white' : 'border border-white/25 hover:bg-white/40 dark:hover:bg-slate-800'"
                  @click="selectedOrgId = item.id"
                >
                  {{ selectedOrgId === item.id ? 'Выбрана' : 'Выбрать' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </article>

    <article v-if="orgStore.selectedOrgId" class="glass rounded-[24px] border border-white/20 p-4 shadow-card">
      <div class="mb-4 flex flex-wrap items-end justify-between gap-3">
        <div>
          <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">Dashboard организации</h2>
          <p class="text-sm text-slate-600 dark:text-slate-300">Обезличенные KPI по сотрудникам и рискам.</p>
        </div>
        <div class="flex flex-wrap gap-2">
          <select v-model="periodType" class="rounded-xl border border-white/25 bg-white/70 px-3 py-2 text-sm dark:bg-slate-950/45">
            <option value="week">Неделя</option>
            <option value="month">Месяц</option>
          </select>
          <input v-model="range.startDate" type="date" class="rounded-xl border border-white/25 bg-white/70 px-3 py-2 text-sm dark:bg-slate-950/45" />
          <input v-model="range.endDate" type="date" class="rounded-xl border border-white/25 bg-white/70 px-3 py-2 text-sm dark:bg-slate-950/45" />
          <button class="rounded-xl bg-brand-700 px-3 py-2 text-sm font-semibold text-white hover:bg-brand-500" @click="loadDashboard">
            Применить
          </button>
        </div>
      </div>

      <div v-if="orgStore.dashboardLoading" class="text-sm text-slate-500 dark:text-slate-400">Загружаем KPI...</div>
      <div v-else-if="dashboard" class="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <div
          v-for="item in kpiItems"
          :key="item.key"
          class="rounded-2xl border border-white/20 bg-white/65 p-4 dark:bg-slate-950/40"
        >
          <p class="text-xs uppercase tracking-[0.14em] text-slate-500 dark:text-slate-400">{{ item.label }}</p>
          <p class="mt-2 text-lg font-semibold text-slate-900 dark:text-slate-100">{{ item.value }}</p>
        </div>
      </div>
    </article>

    <article v-if="orgStore.selectedOrgId" class="glass rounded-[24px] border border-white/20 p-4 shadow-card">
      <div class="flex flex-wrap gap-2">
        <button class="rounded-xl bg-brand-700 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-500" @click="router.push('/org/reports')">
          Перейти в отчёты
        </button>
        <button class="rounded-xl bg-accent px-4 py-2 text-sm font-semibold text-white hover:bg-emerald-600" @click="router.push('/org/exports')">
          Перейти в экспорт
        </button>
      </div>
    </article>
  </section>
</template>
