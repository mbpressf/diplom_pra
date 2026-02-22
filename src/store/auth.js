import { defineStore } from 'pinia'

import { authApi } from '../services/finance'

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
        this.error = error?.response?.data?.detail || 'Ошибка авторизации'
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
        this.error = error?.response?.data?.detail || 'Ошибка регистрации'
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
