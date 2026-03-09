import { defineStore } from 'pinia'

import { authApi } from '../services/finance'

function normalizeAuthError(error, fallback) {
  const detail = error?.response?.data?.detail
  const status = error?.response?.status
  const code = error?.code
  if (code === 'ERR_NETWORK') return 'Сервер недоступен. Проверьте, что backend запущен на http://127.0.0.1:8000'
  if (status === 404) return 'API не найден (404). Проверьте адрес backend'
  if (status === 422) {
    const first = Array.isArray(detail) ? detail[0] : null
    if (first?.loc?.includes('email')) return 'Введите корректный email'
    if (first?.loc?.includes('password')) return 'Пароль должен быть не короче 8 символов'
    return 'Проверьте корректность введённых данных'
  }
  if (!detail) return fallback
  if (detail === 'Email already registered') return 'Email уже зарегистрирован'
  if (detail === 'Invalid email or password') return 'Неверный email или пароль'
  return detail
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('finance_token') || '',
    loading: false,
    error: '',
  }),
  actions: {
    async login(email, password) {
      this.loading = true
      this.error = ''
      try {
        const { data } = await authApi.login({ email, password })
        this.token = data.access_token
        localStorage.setItem('finance_token', data.access_token)
      } catch (error) {
        this.error = normalizeAuthError(error, 'Ошибка авторизации')
        throw error
      } finally {
        this.loading = false
      }
    },
    async register(email, password) {
      this.loading = true
      this.error = ''
      try {
        const { data } = await authApi.register({ email, password })
        this.token = data.access_token
        localStorage.setItem('finance_token', data.access_token)
      } catch (error) {
        this.error = normalizeAuthError(error, 'Ошибка регистрации')
        throw error
      } finally {
        this.loading = false
      }
    },
    logout() {
      this.token = ''
      localStorage.removeItem('finance_token')
    },
  },
})
