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
