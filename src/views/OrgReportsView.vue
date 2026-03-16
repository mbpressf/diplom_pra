<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

import { useOrgStore } from '../store/orgs'

const router = useRouter()
const orgStore = useOrgStore()

const form = reactive({
  period_type: 'month',
  end_date: new Date().toISOString().slice(0, 10),
})

const loading = ref(false)
const errorText = ref('')
const successText = ref('')

const selectedOrgId = computed({
  get: () => orgStore.selectedOrgId,
  set: (value) => orgStore.setSelectedOrg(value),
})

const latestReport = computed(() => orgStore.reports[0] || null)

function formatDateTime(value) {
  if (!value) return '—'
  const parsed = new Date(value)
  if (Number.isNaN(parsed.getTime())) return value
  return new Intl.DateTimeFormat('ru-RU', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(parsed)
}

async function bootstrap() {
  await orgStore.fetchOrganizations()
  if (orgStore.selectedOrgId) {
    await orgStore.fetchReports()
  }
}

async function generateReport() {
  if (!orgStore.selectedOrgId) return
  loading.value = true
  errorText.value = ''
  successText.value = ''
  try {
    await orgStore.generateReport({
      period_type: form.period_type,
      end_date: form.end_date || null,
    })
    successText.value = 'Отчёт сформирован и добавлен в историю выгрузок'
  } catch (error) {
    errorText.value = error?.response?.data?.detail || 'Не удалось сформировать отчёт'
  } finally {
    loading.value = false
  }
}

function goToExports(reportRunId) {
  router.push({ path: '/org/exports', query: { report_run_id: String(reportRunId) } })
}

onMounted(async () => {
  await bootstrap()
})

watch(
  () => orgStore.selectedOrgId,
  async (nextId, prevId) => {
    if (!nextId || nextId === prevId) return
    await orgStore.fetchReports()
  },
)
</script>

<template>
  <section class="space-y-5">
    <article class="glass rounded-[28px] border border-white/20 p-5 shadow-card">
      <h1 class="text-2xl font-semibold tracking-tight text-slate-900 dark:text-slate-50">Отчёты организации</h1>
      <p class="mt-2 text-sm text-slate-600 dark:text-slate-300">
        Генерация weekly/monthly отчётов с KPI-снимком и сохранением истории.
      </p>
    </article>

    <article class="glass rounded-[24px] border border-white/20 p-4 shadow-card">
      <div class="grid gap-3 md:grid-cols-[1fr_200px_200px_auto]">
        <select v-model="selectedOrgId" class="rounded-xl border border-white/25 bg-white/70 px-3 py-3 text-sm dark:bg-slate-950/45">
          <option v-if="!orgStore.organizations.length" value="">Нет организаций</option>
          <option v-for="item in orgStore.organizations" :key="item.id" :value="item.id">{{ item.name }}</option>
        </select>
        <select v-model="form.period_type" class="rounded-xl border border-white/25 bg-white/70 px-3 py-3 text-sm dark:bg-slate-950/45">
          <option value="week">Неделя</option>
          <option value="month">Месяц</option>
        </select>
        <input v-model="form.end_date" type="date" class="rounded-xl border border-white/25 bg-white/70 px-3 py-3 text-sm dark:bg-slate-950/45" />
        <button
          :disabled="!orgStore.selectedOrgId || loading"
          class="rounded-xl bg-brand-700 px-4 py-3 text-sm font-semibold text-white transition hover:bg-brand-500 disabled:opacity-60"
          @click="generateReport"
        >
          {{ loading ? 'Формирование...' : 'Сформировать отчёт' }}
        </button>
      </div>
      <p v-if="successText" class="mt-3 rounded-xl border border-emerald-400/30 bg-emerald-500/10 px-3 py-2 text-sm text-emerald-800 dark:text-emerald-200">
        {{ successText }}
      </p>
      <p v-if="errorText" class="mt-3 rounded-xl border border-red-400/30 bg-red-500/10 px-3 py-2 text-sm text-red-700 dark:text-red-200">
        {{ errorText }}
      </p>
    </article>

    <article v-if="latestReport" class="glass rounded-[24px] border border-white/20 p-4 shadow-card">
      <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">Последний KPI-снимок</h2>
      <div class="mt-3 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <div class="rounded-2xl border border-white/20 bg-white/65 p-4 dark:bg-slate-950/40">
          <p class="text-xs uppercase tracking-[0.14em] text-slate-500 dark:text-slate-400">Активные пользователи</p>
          <p class="mt-2 text-lg font-semibold text-slate-900 dark:text-slate-100">{{ latestReport.kpi_snapshot.active_users_count }}</p>
        </div>
        <div class="rounded-2xl border border-white/20 bg-white/65 p-4 dark:bg-slate-950/40">
          <p class="text-xs uppercase tracking-[0.14em] text-slate-500 dark:text-slate-400">Доля high-risk</p>
          <p class="mt-2 text-lg font-semibold text-slate-900 dark:text-slate-100">{{ latestReport.kpi_snapshot.high_risk_share_pct }}%</p>
        </div>
        <div class="rounded-2xl border border-white/20 bg-white/65 p-4 dark:bg-slate-950/40">
          <p class="text-xs uppercase tracking-[0.14em] text-slate-500 dark:text-slate-400">Перерасход</p>
          <p class="mt-2 text-lg font-semibold text-slate-900 dark:text-slate-100">{{ latestReport.kpi_snapshot.overspend_share_pct }}%</p>
        </div>
        <div class="rounded-2xl border border-white/20 bg-white/65 p-4 dark:bg-slate-950/40">
          <p class="text-xs uppercase tracking-[0.14em] text-slate-500 dark:text-slate-400">Delta savings rate</p>
          <p class="mt-2 text-lg font-semibold text-slate-900 dark:text-slate-100">{{ latestReport.kpi_snapshot.savings_rate_delta_vs_prev_period_pct }}%</p>
        </div>
      </div>
    </article>

    <article class="glass rounded-[24px] border border-white/20 p-4 shadow-card">
      <div class="mb-3 flex items-center justify-between gap-3">
        <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">История выгрузок</h2>
        <button class="rounded-xl border border-white/25 px-3 py-2 text-sm hover:bg-white/40 dark:hover:bg-slate-800" @click="orgStore.fetchReports()">
          Обновить
        </button>
      </div>

      <div v-if="orgStore.reportsLoading" class="text-sm text-slate-500 dark:text-slate-400">Загружаем историю...</div>
      <div v-else-if="!orgStore.reports.length" class="rounded-2xl border border-dashed border-slate-300/70 px-4 py-5 text-sm text-slate-600 dark:border-slate-600 dark:text-slate-300">
        Пока нет сформированных отчётов.
      </div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full text-sm">
          <thead class="bg-slate-200/50 dark:bg-slate-800/50">
            <tr>
              <th class="px-3 py-3 text-left">Сформирован</th>
              <th class="px-3 py-3 text-left">Период</th>
              <th class="px-3 py-3 text-left">Активные</th>
              <th class="px-3 py-3 text-left">High-risk</th>
              <th class="px-3 py-3"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in orgStore.reports" :key="item.id" class="border-t border-slate-200/70 dark:border-slate-700">
              <td class="px-3 py-3">{{ formatDateTime(item.generated_at) }}</td>
              <td class="px-3 py-3">{{ item.period_start }} — {{ item.period_end }}</td>
              <td class="px-3 py-3">{{ item.kpi_snapshot.active_users_count }}</td>
              <td class="px-3 py-3">{{ item.kpi_snapshot.high_risk_share_pct }}%</td>
              <td class="px-3 py-3 text-right">
                <button class="rounded-xl bg-brand-700 px-3 py-2 text-sm font-semibold text-white hover:bg-brand-500" @click="goToExports(item.id)">
                  Открыть экспорт
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </article>
  </section>
</template>
