import api from './api'

export const authApi = {
  register: (payload) => api.post('/auth/register', payload),
  login: (payload) => api.post('/auth/login', payload),
}

export const categoryApi = {
  list: () => api.get('/categories'),
  create: (payload) => api.post('/categories', payload),
  update: (id, payload) => api.put(`/categories/${id}`, payload),
}

export const transactionApi = {
  list: (params) => api.get('/transactions', { params }),
  create: (payload) => api.post('/transactions', payload),
  remove: (id) => api.delete(`/transactions/${id}`),
  exportCsv: (params) => api.get('/transactions/export/csv', { params, responseType: 'blob' }),
  importCsv: (formData) => api.post('/transactions/import/csv', formData),
}

export const analyticsApi = {
  summary: (params) => api.get('/analytics/summary', { params }),
  byCategory: (params) => api.get('/analytics/by-category', { params }),
  byMonth: (params) => api.get('/analytics/by-month', { params }),
}

export const vaultApi = {
  get: () => api.get('/vault'),
  update: (payload) => api.put('/vault', payload),
  deposit: (payload) => api.post('/vault/deposit', payload),
  withdraw: (payload) => api.post('/vault/withdraw', payload),
}

export const orgApi = {
  create: (payload) => api.post('/orgs', payload),
  join: (payload) => api.post('/orgs/join', payload),
  listMy: () => api.get('/orgs/me'),
  dashboard: (orgId, params) => api.get(`/orgs/${orgId}/dashboard`, { params }),
  generateReport: (orgId, payload) => api.post(`/orgs/${orgId}/reports/generate`, payload),
  listReports: (orgId) => api.get(`/orgs/${orgId}/reports`),
  exportUsersCsv: (orgId, params) => api.get(`/orgs/${orgId}/exports/users.csv`, { params, responseType: 'blob' }),
  exportReportXlsx: (orgId, params) => api.get(`/orgs/${orgId}/exports/report.xlsx`, { params, responseType: 'blob' }),
  exportReportPdf: (orgId, params) => api.get(`/orgs/${orgId}/exports/report.pdf`, { params, responseType: 'blob' }),
}
