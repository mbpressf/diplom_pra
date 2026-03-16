import { defineStore } from 'pinia'

import { authApi } from '../services/finance'
import { useUiStore } from './ui'
import { tFor } from '../utils/locale'

function normalizeAuthError(error, fallback) {
  const uiStore = useUiStore()
  const t = (key) => tFor(uiStore.locale, key)
  const detail = error?.response?.data?.detail
  const status = error?.response?.status
  const code = error?.code
  if (code === 'ERR_NETWORK') return t('authServerUnavailable')
  if (status === 404) return t('authApiMissing')
  if (status === 422) {
    const first = Array.isArray(detail) ? detail[0] : null
    if (first?.loc?.includes('email')) return t('authInvalidEmail')
    if (first?.loc?.includes('password')) return t('authPasswordShort')
    if (first?.loc?.includes('organization_name')) return t('authOrgNameRequired')
    return t('authInvalidData')
  }
  if (!detail) return fallback
  if (detail === 'Email already registered') return t('authAlreadyRegistered')
  if (detail === 'Invalid email or password') return t('authBadLogin')
  if (detail === 'Organization name is required for organization account') return t('authOrgNameRequired')
  return detail
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('finance_token') || '',
    profile: null,
    profileLoaded: false,
    loading: false,
    error: '',
  }),
  getters: {
    isAuthed(state) {
      return !!state.token
    },
    accountType(state) {
      return state.profile?.account_type || 'individual'
    },
    isOrganizationAccount() {
      return this.accountType === 'organization'
    },
  },
  actions: {
    async login(email, password) {
      this.loading = true
      this.error = ''
      try {
        const { data } = await authApi.login({ email, password })
        this.token = data.access_token
        localStorage.setItem('finance_token', data.access_token)
        this.profileLoaded = false
        await this.loadProfile()
      } catch (error) {
        this.error = normalizeAuthError(error, tFor(useUiStore().locale, 'authLoginError'))
        throw error
      } finally {
        this.loading = false
      }
    },
    async register(payload) {
      this.loading = true
      this.error = ''
      try {
        const { data } = await authApi.register(payload)
        this.token = data.access_token
        localStorage.setItem('finance_token', data.access_token)
        this.profileLoaded = false
        await this.loadProfile()
      } catch (error) {
        this.error = normalizeAuthError(error, tFor(useUiStore().locale, 'authRegisterError'))
        throw error
      } finally {
        this.loading = false
      }
    },
    async loadProfile() {
      if (!this.token) {
        this.profile = null
        this.profileLoaded = false
        return null
      }
      try {
        const { data } = await authApi.me()
        this.profile = data
        this.profileLoaded = true
        return data
      } catch (error) {
        this.logout()
        throw error
      }
    },
    logout() {
      this.token = ''
      this.profile = null
      this.profileLoaded = false
      localStorage.removeItem('finance_token')
    },
  },
})
