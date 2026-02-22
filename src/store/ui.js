import { defineStore } from 'pinia'

export const useUiStore = defineStore('ui', {
  state: () => ({
    theme: localStorage.getItem('finance_theme') || 'light',
  }),
  actions: {
    initTheme() {
      document.documentElement.classList.toggle('dark', this.theme === 'dark')
    },
    toggleTheme() {
      this.theme = this.theme === 'dark' ? 'light' : 'dark'
      localStorage.setItem('finance_theme', this.theme)
      document.documentElement.classList.toggle('dark', this.theme === 'dark')
    },
  },
})
