import { defineStore } from 'pinia'

import { fetchUsdRubRate } from '../services/exchange'
import { FALLBACK_USD_TO_RUB } from '../utils/locale'

const LOCALE_KEY = 'finance_locale'
const THEME_KEY = 'finance_theme'
const RATE_CACHE_KEY = 'finance_exchange_rate'

function readRateCache() {
  try {
    return JSON.parse(localStorage.getItem(RATE_CACHE_KEY) || '{}')
  } catch {
    return {}
  }
}

export const useUiStore = defineStore('ui', {
  state: () => ({
    theme: localStorage.getItem(THEME_KEY) || 'light',
    locale: localStorage.getItem(LOCALE_KEY) || 'ru',
    usdToRubRate: Number(readRateCache().usdToRubRate) || FALLBACK_USD_TO_RUB,
    rateDate: readRateCache().date || '',
    rateFetchedAt: readRateCache().fetchedAt || '',
    rateLoading: false,
    rateError: '',
  }),
  actions: {
    initPreferences() {
      document.documentElement.classList.toggle('dark', this.theme === 'dark')
      document.documentElement.lang = this.locale === 'en' ? 'en' : 'ru'

      if (this.locale === 'en') {
        void this.refreshExchangeRate()
      }
    },
    toggleTheme() {
      this.theme = this.theme === 'dark' ? 'light' : 'dark'
      localStorage.setItem(THEME_KEY, this.theme)
      document.documentElement.classList.toggle('dark', this.theme === 'dark')
    },
    async setLocale(locale) {
      this.locale = locale === 'en' ? 'en' : 'ru'
      localStorage.setItem(LOCALE_KEY, this.locale)
      document.documentElement.lang = this.locale

      if (this.locale === 'en') {
        await this.refreshExchangeRate(true)
      }
    },
    async refreshExchangeRate(force = false) {
      if (this.rateLoading) return

      const now = Date.now()
      const lastFetched = this.rateFetchedAt ? Date.parse(this.rateFetchedAt) : 0
      const isFresh = lastFetched && now - lastFetched < 1000 * 60 * 60 * 6

      if (!force && isFresh) return

      this.rateLoading = true
      this.rateError = ''
      try {
        const payload = await fetchUsdRubRate()
        this.usdToRubRate = payload.usdToRubRate
        this.rateDate = payload.date
        this.rateFetchedAt = payload.fetchedAt
        localStorage.setItem(RATE_CACHE_KEY, JSON.stringify(payload))
      } catch (error) {
        this.rateError = error?.message || 'rate_error'
      } finally {
        this.rateLoading = false
      }
    },
  },
})
