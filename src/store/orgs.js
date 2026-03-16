import { defineStore } from 'pinia'

import { orgApi } from '../services/finance'

const ORG_SELECTED_KEY = 'finance_selected_org_id'

function readSelectedOrgId() {
  const raw = localStorage.getItem(ORG_SELECTED_KEY)
  const parsed = Number(raw)
  return Number.isFinite(parsed) && parsed > 0 ? parsed : null
}

function saveSelectedOrgId(value) {
  if (!value) {
    localStorage.removeItem(ORG_SELECTED_KEY)
    return
  }
  localStorage.setItem(ORG_SELECTED_KEY, String(value))
}

function parseFilenameFromHeaders(headers, fallback) {
  const disposition = headers?.['content-disposition'] || headers?.['Content-Disposition'] || ''
  const match = disposition.match(/filename\*?=(?:UTF-8''|\"?)([^\";]+)/i)
  if (match?.[1]) {
    try {
      return decodeURIComponent(match[1].replace(/\"/g, '').trim())
    } catch {
      return match[1].replace(/\"/g, '').trim()
    }
  }
  return fallback
}

function triggerBlobDownload(data, filename) {
  const url = window.URL.createObjectURL(new Blob([data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', filename)
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}

export const useOrgStore = defineStore('orgs', {
  state: () => ({
    organizations: [],
    reports: [],
    dashboard: null,
    selectedOrgId: readSelectedOrgId(),
    loading: false,
    dashboardLoading: false,
    reportsLoading: false,
  }),
  getters: {
    selectedOrg(state) {
      return state.organizations.find((item) => item.id === state.selectedOrgId) || null
    },
    hasOrganizations(state) {
      return state.organizations.length > 0
    },
  },
  actions: {
    setSelectedOrg(orgId) {
      const value = Number(orgId)
      this.selectedOrgId = Number.isFinite(value) && value > 0 ? value : null
      saveSelectedOrgId(this.selectedOrgId)
      this.dashboard = null
      this.reports = []
    },
    async fetchOrganizations() {
      this.loading = true
      try {
        const { data } = await orgApi.listMy()
        this.organizations = data

        if (!this.selectedOrgId || !this.organizations.some((item) => item.id === this.selectedOrgId)) {
          this.selectedOrgId = this.organizations[0]?.id || null
          saveSelectedOrgId(this.selectedOrgId)
        }
      } finally {
        this.loading = false
      }
    },
    async createOrganization(payload) {
      const { data } = await orgApi.create(payload)
      await this.fetchOrganizations()
      this.setSelectedOrg(data.id)
      return data
    },
    async joinOrganization(payload) {
      const { data } = await orgApi.join(payload)
      await this.fetchOrganizations()
      this.setSelectedOrg(data.id)
      return data
    },
    async fetchDashboard(params = {}) {
      if (!this.selectedOrgId) return null
      this.dashboardLoading = true
      try {
        const { data } = await orgApi.dashboard(this.selectedOrgId, params)
        this.dashboard = data
        return data
      } finally {
        this.dashboardLoading = false
      }
    },
    async fetchReports(orgId = null) {
      const targetOrgId = Number(orgId) || this.selectedOrgId
      if (!targetOrgId) return []
      this.reportsLoading = true
      try {
        const { data } = await orgApi.listReports(targetOrgId)
        this.reports = data
        return data
      } finally {
        this.reportsLoading = false
      }
    },
    async generateReport(payload) {
      if (!this.selectedOrgId) return null
      const { data } = await orgApi.generateReport(this.selectedOrgId, payload)
      this.reports = [data, ...this.reports]
      return data
    },
    async downloadUsersCsv(params = {}, orgId = null) {
      const targetOrgId = Number(orgId) || this.selectedOrgId
      if (!targetOrgId) return
      const response = await orgApi.exportUsersCsv(targetOrgId, params)
      const filename = parseFilenameFromHeaders(response.headers, 'org-users.csv')
      triggerBlobDownload(response.data, filename)
    },
    async downloadReportXlsx(params = {}, orgId = null) {
      const targetOrgId = Number(orgId) || this.selectedOrgId
      if (!targetOrgId) return
      const response = await orgApi.exportReportXlsx(targetOrgId, params)
      const filename = parseFilenameFromHeaders(response.headers, 'org-report.xlsx')
      triggerBlobDownload(response.data, filename)
    },
    async downloadReportPdf(params = {}, orgId = null) {
      const targetOrgId = Number(orgId) || this.selectedOrgId
      if (!targetOrgId) return
      const response = await orgApi.exportReportPdf(targetOrgId, params)
      const filename = parseFilenameFromHeaders(response.headers, 'org-report.pdf')
      triggerBlobDownload(response.data, filename)
    },
    clear() {
      this.organizations = []
      this.reports = []
      this.dashboard = null
      this.selectedOrgId = null
      this.loading = false
      this.dashboardLoading = false
      this.reportsLoading = false
      localStorage.removeItem(ORG_SELECTED_KEY)
    },
  },
})
