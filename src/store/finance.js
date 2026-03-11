import { defineStore } from 'pinia'

import { analyticsApi, categoryApi, transactionApi, vaultApi } from '../services/finance'

const CACHE_KEY = 'finance_cache_v1'

function toParams(range) {
  const params = {}
  if (range.startDate) params.start_date = range.startDate
  if (range.endDate) params.end_date = range.endDate
  return params
}

export const useFinanceStore = defineStore('finance', {
  state: () => ({
    categories: [],
    transactions: [],
    summary: {
      total_income: 0,
      total_expense: 0,
      balance: 0,
      savings_rate: 0,
    },
    byCategory: [],
    byMonth: [],
    vault: {
      id: null,
      name: '',
      balance: 0,
      target_amount: 0,
      net_balance: 0,
      available_to_spend: 0,
      progress_percent: 0,
    },
    filters: {
      startDate: '',
      endDate: '',
    },
    loading: false,
    ready: false,
  }),
  actions: {
    hydrateCache() {
      const raw = localStorage.getItem(CACHE_KEY)
      if (!raw) return
      try {
        const parsed = JSON.parse(raw)
        this.categories = parsed.categories || []
        this.transactions = parsed.transactions || []
        this.summary = parsed.summary || this.summary
        this.byCategory = parsed.byCategory || []
        this.byMonth = parsed.byMonth || []
        this.vault = parsed.vault || this.vault
      } catch {
        localStorage.removeItem(CACHE_KEY)
      }
    },
    persistCache() {
      localStorage.setItem(
        CACHE_KEY,
        JSON.stringify({
          categories: this.categories,
          transactions: this.transactions,
          summary: this.summary,
          byCategory: this.byCategory,
          byMonth: this.byMonth,
          vault: this.vault,
        }),
      )
    },
    async bootstrap() {
      this.hydrateCache()
      await this.refreshAll()
      this.ready = true
    },
    async refreshAll() {
      this.loading = true
      try {
        const params = toParams(this.filters)
        const [catRes, txRes, sumRes, bcRes, bmRes, vaultRes] = await Promise.allSettled([
          categoryApi.list(),
          transactionApi.list(params),
          analyticsApi.summary(params),
          analyticsApi.byCategory(params),
          analyticsApi.byMonth(params),
          vaultApi.get(),
        ])

        if (catRes.status === 'fulfilled') this.categories = catRes.value.data
        if (txRes.status === 'fulfilled') this.transactions = txRes.value.data
        if (sumRes.status === 'fulfilled') this.summary = sumRes.value.data
        if (bcRes.status === 'fulfilled') this.byCategory = bcRes.value.data
        if (bmRes.status === 'fulfilled') this.byMonth = bmRes.value.data
        if (vaultRes.status === 'fulfilled') this.vault = vaultRes.value.data

        this.persistCache()
      } finally {
        this.loading = false
      }
    },
    async setDateRange(startDate, endDate) {
      this.filters.startDate = startDate
      this.filters.endDate = endDate
      await this.refreshAll()
    },
    async addCategory(payload) {
      await categoryApi.create(payload)
      await this.refreshAll()
    },
    async updateCategory(id, payload) {
      await categoryApi.update(id, payload)
      await this.refreshAll()
    },
    async addTransaction(payload) {
      await transactionApi.create(payload)
      await this.refreshAll()
    },
    async deleteTransaction(id) {
      await transactionApi.remove(id)
      await this.refreshAll()
    },
    async exportCsv() {
      const params = toParams(this.filters)
      const { data } = await transactionApi.exportCsv(params)
      const url = window.URL.createObjectURL(new Blob([data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'transactions.csv')
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    },
    async importCsv(file) {
      const formData = new FormData()
      formData.append('file', file)
      await transactionApi.importCsv(formData)
      await this.refreshAll()
    },
    async updateVault(payload) {
      const { data } = await vaultApi.update(payload)
      this.vault = data
      this.persistCache()
      await this.refreshAll()
    },
    async depositToVault(amount) {
      const { data } = await vaultApi.deposit({ amount })
      this.vault = data
      this.persistCache()
      await this.refreshAll()
    },
    async withdrawFromVault(amount) {
      const { data } = await vaultApi.withdraw({ amount })
      this.vault = data
      this.persistCache()
      await this.refreshAll()
    },
    clear() {
      this.categories = []
      this.transactions = []
      this.byCategory = []
      this.byMonth = []
      this.summary = {
        total_income: 0,
        total_expense: 0,
        balance: 0,
        savings_rate: 0,
      }
      this.vault = {
        id: null,
        name: '',
        balance: 0,
        target_amount: 0,
        net_balance: 0,
        available_to_spend: 0,
        progress_percent: 0,
      }
      localStorage.removeItem(CACHE_KEY)
    },
  },
})
