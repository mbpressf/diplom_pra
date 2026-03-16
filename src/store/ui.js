import { defineStore } from 'pinia'

const THEME_KEY = 'finance_theme'

export const useUiStore = defineStore('ui', {
  state: () => ({
    theme: localStorage.getItem(THEME_KEY) || 'light',
    locale: 'ru',
    usdToRubRate: 1,
    rateDate: '',
    rateFetchedAt: '',
    rateLoading: false,
    rateError: '',
  }),
  actions: {
    initPreferences() {
      document.documentElement.classList.toggle('dark', this.theme === 'dark')
      document.documentElement.lang = 'ru'
    },
    toggleTheme() {
      this.theme = this.theme === 'dark' ? 'light' : 'dark'
      localStorage.setItem(THEME_KEY, this.theme)
      document.documentElement.classList.toggle('dark', this.theme === 'dark')
    },
    async setLocale(locale) {
      this.locale = 'ru'
      document.documentElement.lang = 'ru'
      return locale
    },
    async refreshExchangeRate(force = false) {
      this.rateLoading = false
      this.rateError = ''
      return force
    },
  },
})
