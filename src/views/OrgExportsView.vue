<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { useOrgStore } from '../store/orgs'

const route = useRoute()
const orgStore = useOrgStore()

const filters = reactive({
  period_type: 'month',
  start_date: '',
  end_date: '',
  report_run_id: '',
})

const loading = ref(false)
const errorText = ref('')

const selectedOrgId = computed({
  get: () => orgStore.selectedOrgId,
  set: (value) => orgStore.setSelectedOrg(value),
})

const exportParams = computed(() => {
  const params = { period_type: filters.period_type }

  if (filters.report_run_id) {
    params.report_run_id = Number(filters.report_run_id)
    return params
  }

  if (filters.start_date && filters.end_date) {
    params.start_date = filters.start_date
    params.end_date = filters.end_date
  }

  return params
})

function resetError() {
  errorText.value = ''
}

async function download(kind) {
  if (!orgStore.selectedOrgId) return
  loading.value = true
  errorText.value = ''
  try {
    if (kind === 'csv') await orgStore.downloadUsersCsv(exportParams.value)
    if (kind === 'xlsx') await orgStore.downloadReportXlsx(exportParams.value)
    if (kind === 'pdf') await orgStore.downloadReportPdf(exportParams.value)
  } catch (error) {
    errorText.value = error?.response?.data?.detail || 'Не удалось выполнить экспорт'
  } finally {
    loading.value = false
  }
}

async function bootstrap() {
  await orgStore.fetchOrganizations()
  if (orgStore.selectedOrgId) {
    await orgStore.fetchReports()
  }
}

onMounted(async () => {
  await bootstrap()
  const reportRunId = String(route.query.report_run_id || '')
  if (reportRunId) {
    filters.report_run_id = reportRunId
  }
})

watch(
  () => orgStore.selectedOrgId,
  async (nextId, prevId) => {
    if (!nextId || nextId === prevId) return
    await orgStore.fetchReports()
    filters.report_run_id = ''
    resetError()
  },
)
</script>

<template>
  <section class="space-y-5">
    <article class="glass rounded-[28px] border border-white/20 p-5 shadow-card">
      <h1 class="text-2xl font-semibold tracking-tight text-slate-900 dark:text-slate-50">Экспорт</h1>
      <p class="mt-2 text-sm text-slate-600 dark:text-slate-300">
        Выгружайте обезличенные данные сотрудников и управленческие отчёты в CSV, XLSX и PDF.
      </p>
    </article>

    <article class="glass rounded-[24px] border border-white/20 p-4 shadow-card">
      <div class="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        <select v-model="selectedOrgId" class="rounded-xl border border-white/25 bg-white/70 px-3 py-3 text-sm dark:bg-slate-950/45">
          <option v-if="!orgStore.organizations.length" value="">Нет организаций</option>
          <option v-for="item in orgStore.organizations" :key="item.id" :value="item.id">{{ item.name }}</option>
        </select>

        <select v-model="filters.report_run_id" class="rounded-xl border border-white/25 bg-white/70 px-3 py-3 text-sm dark:bg-slate-950/45" @change="resetError">
          <option value="">Период вручную</option>
          <option v-for="run in orgStore.reports" :key="run.id" :value="String(run.id)">
            #{{ run.id }} · {{ run.period_start }} — {{ run.period_end }}
          </option>
        </select>

        <select v-model="filters.period_type" class="rounded-xl border border-white/25 bg-white/70 px-3 py-3 text-sm dark:bg-slate-950/45" :disabled="!!filters.report_run_id" @change="resetError">
          <option value="week">Неделя</option>
          <option value="month">Месяц</option>
        </select>

        <button class="rounded-xl border border-white/25 px-3 py-3 text-sm hover:bg-white/40 dark:hover:bg-slate-800" @click="orgStore.fetchReports()">
          Обновить историю
        </button>
      </div>

      <div class="mt-3 grid gap-3 md:grid-cols-2">
        <input v-model="filters.start_date" type="date" :disabled="!!filters.report_run_id" class="rounded-xl border border-white/25 bg-white/70 px-3 py-3 text-sm dark:bg-slate-950/45" @change="resetError" />
        <input v-model="filters.end_date" type="date" :disabled="!!filters.report_run_id" class="rounded-xl border border-white/25 bg-white/70 px-3 py-3 text-sm dark:bg-slate-950/45" @change="resetError" />
      </div>

      <p class="mt-3 text-xs text-slate-500 dark:text-slate-400">
        Если выбран report run, период берётся из истории. Иначе используется выбранный period type и диапазон дат.
      </p>

      <div class="mt-4 flex flex-wrap gap-2">
        <button :disabled="loading || !orgStore.selectedOrgId" class="rounded-xl bg-brand-700 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-500 disabled:opacity-60" @click="download('csv')">
          Скачать CSV
        </button>
        <button :disabled="loading || !orgStore.selectedOrgId" class="rounded-xl bg-emerald-600 px-4 py-2 text-sm font-semibold text-white hover:bg-emerald-500 disabled:opacity-60" @click="download('xlsx')">
          Скачать XLSX
        </button>
        <button :disabled="loading || !orgStore.selectedOrgId" class="rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-700 disabled:opacity-60" @click="download('pdf')">
          Скачать PDF
        </button>
      </div>

      <p v-if="errorText" class="mt-3 rounded-xl border border-red-400/30 bg-red-500/10 px-3 py-2 text-sm text-red-700 dark:text-red-200">{{ errorText }}</p>
    </article>
  </section>
</template>
